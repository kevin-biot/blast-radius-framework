#!/usr/bin/env python3
"""Export observed ACS decisions and tool outcomes as a BRF evidence bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from .validate_json_schema import ROOT_DIR, load_json, make_validator, structural_errors
    from .fetch_acs_schemas import BASE, CACHE, COMMIT
except ImportError:
    from validate_json_schema import ROOT_DIR, load_json, make_validator, structural_errors
    from fetch_acs_schemas import BASE, CACHE, COMMIT

from referencing import Registry, Resource


def acs_validators():
    manifest = load_json(CACHE / "manifest.json")
    if manifest["upstream_commit"] != COMMIT or manifest["schema_base"] != BASE:
        raise ValueError("ACS cache has the wrong source revision")
    resources = {}
    for path, digest in manifest["files"].items():
        target = (CACHE / path).resolve()
        if not target.is_relative_to(CACHE.resolve()):
            raise ValueError("invalid cache path")
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError(f"ACS cache integrity mismatch: {path}")
        schema = load_json(target)
        if schema["$id"] != BASE + path:
            raise ValueError("ACS cache schema ID mismatch")
        resources[schema["$id"]] = Resource.from_contents(schema)
    registry = Registry().with_resources(resources.items())
    return {name: make_validator(resources[BASE + name].contents, registry)
            for name in ("request-envelope.json", "response-envelope.json", "hooks/tool-call-request.json")}


def require_valid(validator, instance):
    errors = structural_errors(validator, instance)
    if errors:
        raise ValueError("; ".join(errors))


def export_bundle(transcript, validators, input_sha256):
    if transcript.get("source_kind") not in {"local_fixture", "captured_acs"}:
        raise ValueError("source_kind must be local_fixture or captured_acs")
    if any(not isinstance(transcript.get(key), str) or not transcript[key].strip()
           for key in ("policy_snapshot_id", "target_revision")):
        raise ValueError("policy snapshot and target revision are required")
    events = transcript.get("events")
    if not isinstance(events, list) or not events:
        raise ValueError("at least one observed event is required")
    records, seen = [], set()
    for event in events:
        request = event["request"]
        require_valid(validators["request-envelope.json"], request)
        if request["method"] != "steps/toolCallRequest" or request["params"]["acs_version"] != "0.1.0":
            raise ValueError("only ACS 0.1.0 steps/toolCallRequest is implemented")
        require_valid(validators["hooks/tool-call-request.json"], request["params"]["payload"])
        request_id = request["params"]["request_id"]
        if request_id in seen:
            raise ValueError("duplicate request ID")
        seen.add(request_id)
        observation = event["observation"]
        executed = observation["executed"]
        if type(executed) is not bool or observation.get("outcome") not in {"succeeded", "blocked", "failed"}:
            raise ValueError("tool outcome must be explicit, with a boolean executed field")
        response = event.get("response")
        if response is None:
            if not observation.get("policy_service_error"):
                raise ValueError("missing response requires a recorded policy-service error")
            decision, policy_bound = "service_unavailable", False
        else:
            require_valid(validators["response-envelope.json"], response)
            result = response.get("result", {})
            if response["id"] != request["id"] or result.get("request_id") != request_id:
                raise ValueError("ACS response correlation mismatch")
            if result.get("type") != "final" or result.get("acs_version") != "0.1.0":
                raise ValueError("a final ACS 0.1.0 disposition is required")
            decision = result["decision"]
            policy_bound = any(ref.get("policy_version") == transcript["policy_snapshot_id"]
                               for ref in result.get("policy_references", []))
        # The host deliberately pauses all other dispositions; it does not apply modify/ask/defer.
        consistent = (not executed or decision == "allow") and observation["outcome"] in ({"succeeded", "failed"} if executed else {"blocked"})
        status = "pass" if consistent else "fail"
        if status == "pass" and decision == "allow" and not executed:
            status = "inconclusive"
        if status == "pass" and response is not None and not policy_bound:
            status = "inconclusive"
        records.append({"request_id": request_id, "session_id": request["params"]["metadata"]["session_id"],
                        "decision": decision, "executed": executed, "outcome": observation["outcome"],
                        "policy_bound": policy_bound, "status": status})
    statuses = {record["status"] for record in records}
    status = "fail" if "fail" in statuses else "inconclusive" if "inconclusive" in statuses else "pass"
    return {"bundle_version": "0.1", "source_kind": transcript["source_kind"],
            "created_at": datetime.now(timezone.utc).isoformat(), "upstream_commit": COMMIT,
            "input_sha256": input_sha256, "policy_snapshot_id": transcript["policy_snapshot_id"],
            "target_revision": transcript["target_revision"], "evaluation_status": status,
            "records": records, "brf_evidence_relevance": ["I6 default-deny assessment; not completion of I6-T1 token tests"],
            "limits": ["No ACS conformance certification, wire-signature verification or independent anchor verification.",
                       "Tool outcomes are supplied observations; their truth and completeness require independent audit.",
                       "No production hook-bypass, revocation, tenant-isolation or statistical failure-rate claim.",
                       "A pass concerns observed dispatch decisions, not tool success or the full I6 invariant.",
                       "modify, ask and defer pause this host; their full workflows are not implemented."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        raw = args.transcript.read_bytes()
        bundle = export_bundle(load_json(args.transcript), acs_validators(), hashlib.sha256(raw).hexdigest())
        schema = load_json(ROOT_DIR / "spec/acs-evidence.schema.json")
        require_valid(make_validator(schema), bundle)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(bundle, indent=2) + "\n")
        print(f"{bundle['evaluation_status'].upper()} {args.output}")
        return int(bundle["evaluation_status"] != "pass")
    except Exception as exc:
        print(f"ERROR: {exc}. Fetch schemas with python3 tools/fetch_acs_schemas.py if needed.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
