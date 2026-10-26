#!/usr/bin/env python3
"""Run a bounded local host fixture through ACS-shaped allow, deny and outage cases."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

try:
    from .acs_evidence import acs_validators, require_valid
except ImportError:
    from acs_evidence import acs_validators, require_valid

POLICY = "brf-demo-policy-v1"
SESSION = str(uuid5(NAMESPACE_URL, "brf-acs-local-fixture"))


def request(case, amount):
    return {"jsonrpc": "2.0", "id": case, "method": "steps/toolCallRequest", "params": {
        "acs_version": "0.1.0", "request_id": str(uuid5(NAMESPACE_URL, "brf-demo/" + case)),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": {"agent_id": "brf-demo-agent", "session_id": SESSION, "environment": "development"},
        "payload": {"tool": {"name": "ledger.increment"}, "arguments": {"amount": {"value": amount}}}}}


def guardian(req):
    amount = req["params"]["payload"]["arguments"]["amount"]["value"]
    decision = "allow" if type(amount) is int and 1 <= amount <= 3 else "deny"
    return {"jsonrpc": "2.0", "id": req["id"], "result": {
        "type": "final", "acs_version": "0.1.0", "request_id": req["params"]["request_id"],
        "decision": decision, "reasoning": "Local fixture permits integer increments from 1 to 3.",
        "policy_references": [{"policy_id": "increment-bound", "policy_version": POLICY}]}}


def host(req, policy_service, ledger):
    """Only an explicit allow may dispatch the fixture's one tool."""
    validators = acs_validators()
    require_valid(validators["request-envelope.json"], req)
    require_valid(validators["hooks/tool-call-request.json"], req["params"]["payload"])
    if (req["method"] != "steps/toolCallRequest" or req["params"]["acs_version"] != "0.1.0"
            or req["params"]["payload"]["tool"]["name"] != "ledger.increment"):
        raise ValueError("unsupported request; tool blocked")
    try:
        response = policy_service(req)
    except (TimeoutError, ConnectionError) as exc:
        return {"request": req, "response": None, "observation": {
            "executed": False, "outcome": "blocked", "policy_service_error": str(exc)}}
    require_valid(validators["response-envelope.json"], response)
    result = response.get("result", {})
    if (response["id"] != req["id"] or result.get("request_id") != req["params"]["request_id"]
            or result.get("type") != "final" or result.get("acs_version") != "0.1.0"):
        raise ValueError("uncorrelated or unsupported policy response; tool blocked")
    if not any(ref.get("policy_version") == POLICY for ref in result.get("policy_references", [])):
        raise ValueError("missing expected policy snapshot; tool blocked")
    allowed = result["decision"] == "allow"
    if allowed:
        ledger.append(req["params"]["payload"]["arguments"]["amount"]["value"])
    return {"request": req, "response": response,
            "observation": {"executed": allowed, "outcome": "succeeded" if allowed else "blocked"}}


def unavailable(_):
    raise ConnectionError("fixture: policy service unreachable")


def demo():
    ledger = []
    events = [host(request("allowed", 2), guardian, ledger),
              host(request("denied", 100), guardian, ledger),
              host(request("unavailable", 2), unavailable, ledger)]
    if ledger != [2]:
        raise AssertionError("a denied or unavailable-policy action reached the tool")
    return {"source_kind": "local_fixture", "policy_snapshot_id": POLICY,
            "target_revision": "brf-demo-host-v1", "events": events}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(demo(), indent=2) + "\n")
    print(f"Ran allow, deny and policy-outage fixture; only the allowed action executed: {args.output}")


if __name__ == "__main__":
    main()
