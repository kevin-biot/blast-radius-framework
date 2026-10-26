#!/usr/bin/env python3
"""Compare fixed proposals with no mediation, shape checks and a real OPA gate."""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path

try:
    from .evidence_common import digest, write_evidence
    from .evaluation_evidence import bundle
    from .install_opa_local import ASSETS, TARGET, VERSION, file_digest
    from .validate_json_schema import ROOT_DIR, decode_json, load_json, make_validator, structural_errors
except ImportError:
    from evidence_common import digest, write_evidence
    from evaluation_evidence import bundle
    from install_opa_local import ASSETS, TARGET, VERSION, file_digest
    from validate_json_schema import ROOT_DIR, decode_json, load_json, make_validator, structural_errors

FIXTURE = ROOT_DIR / "examples/opa-boundary"
MODES = ("unmediated", "schema_only", "opa_enforced")


def verified_opa():
    expected = ASSETS[(platform.system(), platform.machine())][1]
    if file_digest(TARGET) != expected:
        raise ValueError("OPA binary does not match the pinned digest")
    return TARGET


def opa_decision(action, context, opa, policy):
    try:
        result = subprocess.run([str(opa), "eval", "--format=json", "--stdin-input", "--data", str(policy), "data.brf.allow"],
                                input=json.dumps({"action": action, "context": context}), text=True,
                                capture_output=True, timeout=5)
        if result.returncode:
            return False, True
        values = decode_json(result.stdout).get("result", [])
        if len(values) != 1 or len(values[0].get("expressions", [])) != 1:
            return False, True
        value = values[0]["expressions"][0].get("value")
        if type(value) is not bool:
            return False, True
        return value, False
    except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError):
        return False, True


def run_case(mode, case, base_context, opa=TARGET, policy=FIXTURE / "policy.rego"):
    if mode not in MODES:
        raise ValueError("unknown comparison mode")
    context = dict(base_context, **case.get("context", {}), spent=0)
    validator = make_validator(load_json(FIXTURE / "action.schema.json"))
    receipts, error = [], False
    expected = case["expected_allow"]
    if len(expected) != len(case["actions"]) or any(type(flag) is not bool for flag in expected):
        raise ValueError("each proposal needs an explicit independent fixture expectation")
    for index, action in enumerate(case["actions"]):
        allowed = mode == "unmediated" or not structural_errors(validator, action)
        if allowed and mode == "opa_enforced":
            allowed, failed = opa_decision(action, context, opa, policy)
            error |= failed
        if allowed and action.get("tool") == "ledger.increment" and type(action.get("amount")) is int:
            receipts.append({"index": index, "tenant": action["tenant"], "amount": action["amount"]})
            context["spent"] += action["amount"]
    expected_receipts = [{"index": i, "tenant": action["tenant"], "amount": action["amount"]}
                         for i, action in enumerate(case["actions"]) if expected[i]]
    return {"sample_id": case["id"], "sample_id_type": "string", "epoch": 1, "mode": mode,
            "task_success": receipts == expected_receipts, "boundary_violation": any(not expected[r["index"]] for r in receipts),
            "error": error, "receipts": receipts}


def fixture_provenance():
    files = {str(path.relative_to(ROOT_DIR)): digest(path.read_bytes()) for path in
             (FIXTURE / "scenarios.json", FIXTURE / "action.schema.json", FIXTURE / "policy.rego", Path(__file__),
              ROOT_DIR / "tools/run_inspect_demo.py", ROOT_DIR / "tools/evaluation_evidence.py")}
    revision = "sha256:" + digest(json.dumps(files, sort_keys=True).encode())
    return "sha256:" + files["examples/opa-boundary/policy.rego"], revision, files


def comparison():
    opa = verified_opa()
    workload_raw = (FIXTURE / "scenarios.json").read_bytes()
    workload = decode_json(workload_raw.decode())
    policy, revision, files = fixture_provenance()
    records = [run_case(mode, case, workload["context"], opa) for mode in MODES for case in workload["scenarios"]]
    if fixture_provenance()[1] != revision:
        raise ValueError("fixture code, policy or workload changed during the comparison")
    source = {"sha256": digest(workload_raw), "producer": "OPA fixed-proposal comparison", "producer_version": VERSION,
              "task": "tenant/amount/scope/expiry/budget boundaries", "model": "none; fixed proposals",
              "configuration": {"modes": list(MODES), "artifact_digests": files, "opa_sha256": file_digest(opa)}}
    return bundle("BRF-OPA-fixture", "local_fixture", source, policy, revision, records, len(records))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        result = comparison()
        inputs = {ROOT_DIR / path for path in result["source"]["configuration"]["artifact_digests"]}
        if args.output.resolve() in {path.resolve() for path in inputs | {TARGET}}:
            raise ValueError("output must not replace the policy, workload, runner or OPA binary")
        write_evidence(result, "evaluation-evidence.schema.json", args.output, args.overwrite)
        for mode in MODES:
            selected = [r for r in result["records"] if r["mode"] == mode]
            print(f"{mode}: {sum(r['task_success'] for r in selected)}/{len(selected)} fixture expectations matched; "
                  f"{sum(r['boundary_violation'] for r in selected)} violation cases; {sum(r['error'] for r in selected)} errors")
        return int(result["summary"]["evaluation_status"] != "pass")
    except Exception as exc:
        print(f"ERROR: {exc}; install pinned OPA with python3 tools/install_opa_local.py", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
