#!/usr/bin/env python3
"""Run actual Inspect logging/scoring on fixed OPA-boundary proposals, without an LLM."""
from __future__ import annotations

import argparse
from pathlib import Path

from inspect_ai import Task, eval
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import Score, scorer
from inspect_ai.solver import solver

try:
    from .inspect_evidence import export_log
    from .evidence_common import write_evidence
    from .opa_comparison import FIXTURE, MODES, fixture_provenance, run_case, verified_opa
    from .validate_json_schema import load_json
except ImportError:
    from inspect_evidence import export_log
    from evidence_common import write_evidence
    from opa_comparison import FIXTURE, MODES, fixture_provenance, run_case, verified_opa
    from validate_json_schema import load_json


@solver
def fixed_proposals():
    async def solve(state, generate):
        state.metadata["brf_observation"] = run_case(state.metadata["mode"], state.metadata["case"], state.metadata["context"])
        state.completed = True
        return state
    return solve


@scorer(metrics=[])
def task_success():
    async def score(state, target):
        result = state.metadata["brf_observation"]
        return Score(value=result["task_success"], metadata={"brf_error": result["error"]})
    return score


@scorer(metrics=[])
def boundary_violation():
    async def score(state, target):
        return Score(value=state.metadata["brf_observation"]["boundary_violation"])
    return score


def run_demo(log_dir, mode="opa_enforced", log_format="eval"):
    if mode == "opa_enforced":
        verified_opa()
    policy, revision, _ = fixture_provenance()
    workload = load_json(FIXTURE / "scenarios.json")
    samples = [Sample(id=case["id"], input="Execute this fixed-proposal boundary fixture; no model generation.",
                      metadata={"case": case, "context": workload["context"], "mode": mode})
               for case in workload["scenarios"]]
    task = Task(name="brf_fixed_proposals", dataset=MemoryDataset(samples, name="brf-boundary-v1"),
                solver=fixed_proposals(), scorer=[task_success(), boundary_violation()],
                metadata={"brf": {"source_kind": "local_fixture", "policy_snapshot_id": policy, "target_revision": revision}})
    logs = eval(task, model="mockllm/model", display="none", notification=False,
                log_dir=str(log_dir), log_format=log_format, max_samples=1)
    if len(logs) != 1 or logs[0].status != "success":
        raise RuntimeError("Inspect fixture did not complete successfully")
    if fixture_provenance()[1] != revision:
        raise ValueError("fixture changed while Inspect was running")
    return Path(logs[0].location)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mode", choices=MODES, default="opa_enforced")
    parser.add_argument("--log-format", choices=("eval", "json"), default="eval")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    location = run_demo(args.log_dir, args.mode, args.log_format)
    result = export_log(location)
    write_evidence(result, "evaluation-evidence.schema.json", args.output, args.overwrite)
    print(f"Inspect log: {location}")
    print(f"{result['summary']['evaluation_status'].upper()}: {result['summary']['record_count']} fixed-proposal scores; no LLM called")
    return int(result["summary"]["evaluation_status"] != "pass")


if __name__ == "__main__":
    raise SystemExit(main())
