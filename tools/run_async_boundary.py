#!/usr/bin/env python3
"""Measure retry, budget and revocation effects with explicit race barriers."""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from http.client import RemoteDisconnected
from pathlib import Path
from urllib.error import URLError

try:
    from .evidence_common import write_evidence
    from .execution_fixture import Tool, artifact_paths, artifacts, bundle, case
except ImportError:
    from evidence_common import write_evidence
    from execution_fixture import Tool, artifact_paths, artifacts, bundle, case


def run(directory):
    directory = Path(directory).resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    paths = artifact_paths(("run_async_boundary.py",))
    before, cases = artifacts(paths), []

    def record(name, tool, expected, checks, violation=False, residual=0):
        result = case(name, expected, tool.observe(), violation=violation, residual=residual)
        result["checks"] = checks
        result["expectation_met"] &= all(checks.values())
        cases.append(result)

    with Tool(directory / "retry") as tool:
        payload = {"operation_id": "retry", "amount": 1}
        first, second = tool.call("/commit", payload), tool.call("/commit", payload)
        record("sequential_retry", tool, 1, {"same_receipt": first[1].get("seq") == second[1].get("seq"),
            "first_committed": first[0] == 200, "retry_replayed": second[0] == 200 and second[1].get("replayed") is True})

    with Tool(directory / "lost-response") as tool:
        disconnected = False
        try:
            tool.call("/commit", {"operation_id": "lost", "amount": 1, "drop_response": True})
        except (RemoteDisconnected, ConnectionResetError, URLError):
            disconnected = True
        prior = tool.observe()
        status, receipt = tool.call("/commit", {"operation_id": "lost", "amount": 1})
        record("retry_after_lost_response", tool, 1, {"response_lost": disconnected,
            "effect_preceded_retry": len(prior["receipts"]) == 1,
            "retry_replayed": status == 200 and receipt.get("replayed") is True})

    with Tool(directory / "key-conflict") as tool:
        tool.call("/commit", {"operation_id": "same", "amount": 1})
        status, _ = tool.call("/commit", {"operation_id": "same", "amount": 2})
        record("conflicting_idempotency_payload", tool, 1, {"conflict_rejected": status == 409})

    for same_key, mode in [(True, "atomic"), (False, "atomic"), (False, "check_then_commit")]:
        name = "concurrent_same_key" if same_key else "aggregate_budget_" + mode
        with Tool(directory / name, mode) as tool, ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(tool.call, "/commit", {"operation_id": "same" if same_key else f"op-{i}",
                "amount": 1 if same_key else 2, "wait_before": "both"}) for i in range(2)]
            tool.wait_for(2)
            tool.call("/release", {"gate": "both"})
            results = [future.result(timeout=8) for future in futures]
            if same_key:
                checks = {"both_returned": all(s == 200 for s, _ in results),
                          "one_replay": sum(r.get("replayed") is True for _, r in results) == 1}
                expected = 1
            else:
                checks = {"expected_statuses": sorted(s for s, _ in results) == ([200, 403] if mode == "atomic" else [200, 200])}
                expected = 2 if mode == "atomic" else 4
            record(name, tool, expected, checks, violation=not same_key and mode != "atomic")

    with Tool(directory / "queued-revoke") as tool:
        tool.call("/revoke", {"reason": "queued work lost its runtime grant"})
        status, _ = tool.call("/commit", {"operation_id": "queued", "amount": 1})
        record("revoked_before_dispatch", tool, 0, {"commit_denied": status == 403})

    for mode in ("atomic", "check_then_commit"):
        with Tool(directory / ("inflight-" + mode), mode) as tool, ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(tool.call, "/commit", {"operation_id": "inflight", "amount": 1, "wait_before": "revoke"})
            tool.wait_for(1)
            tool.call("/revoke", {"reason": "grant withdrawn while request is in flight"})
            tool.call("/release", {"gate": "revoke"})
            status, _ = future.result(timeout=8)
            record("revoked_inflight_" + mode, tool, 0 if mode == "atomic" else 1,
                   {"expected_status": status == (403 if mode == "atomic" else 200)}, violation=mode != "atomic")

    with Tool(directory / "post-commit-revoke") as tool, ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(tool.call, "/commit", {"operation_id": "committed", "amount": 1, "wait_after": "response"})
        tool.wait_for(1, "after_commit")
        prior = tool.observe()
        tool.call("/revoke", {"reason": "revoke after durable commit, before response"})
        tool.call("/release", {"gate": "response"})
        status, _ = future.result(timeout=8)
        later, _ = tool.call("/commit", {"operation_id": "later", "amount": 1})
        record("revocation_does_not_undo_committed_effect", tool, 1,
               {"effect_visible_before_revocation": prior["spent"] == 1, "original_response_delivered": status == 200,
                "new_effect_denied": later == 403, "grant_inactive": not tool.observe()["active"]}, residual=1)

    with Tool(directory / "no-credential") as tool:
        status, _ = tool.call("/commit", {"operation_id": "unauthorized", "amount": 1}, token="no-fixture-token")
        record("direct_call_without_fixture_credential", tool, 0, {"unauthorized": status == 401})
    return bundle("async_boundary", cases, before, paths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True, help="new directory for private runtime artifacts")
    args = parser.parse_args()
    try:
        result = run(args.run_dir)
        write_evidence(result, "execution-evidence.schema.json", args.run_dir / "evidence.json")
        print(f"{len(result['cases'])} cases; expectations met: {result['expectations_met']}; "
              f"observed violation cases: {result['boundary_violation_cases']}")
        return 0 if result["expectations_met"] else 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
