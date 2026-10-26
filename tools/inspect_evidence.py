#!/usr/bin/env python3
"""Export explicit task/violation scores through Inspect's native log API."""
from __future__ import annotations

import argparse
import importlib.metadata
import sys
from pathlib import Path

try:
    from .evidence_common import digest, write_evidence
    from .evaluation_evidence import bundle
    from .validate_json_schema import decode_json
except ImportError:
    from evidence_common import digest, write_evidence
    from evaluation_evidence import bundle
    from validate_json_schema import decode_json

INSPECT_VERSION = "0.3.283"


def binary_score(value, positive=None, negative=None):
    if type(value) is bool:
        return value
    if type(value) in {int, float} and value in (0, 1):
        return bool(value)
    if isinstance(value, str) and positive is not None and negative is not None:
        if positive == negative:
            raise ValueError("positive and negative score labels must differ")
        if value == positive:
            return True
        if value == negative:
            return False
    return None


def export_log(path, task_score="task_success", violation_score="boundary_violation",
               policy=None, revision=None, task_labels=(None, None), violation_labels=(None, None)):
    if task_score == violation_score:
        raise ValueError("task and violation scores must be distinct")
    for labels in (task_labels, violation_labels):
        if (labels[0] is None) != (labels[1] is None) or labels[0] is not None and labels[0] == labels[1]:
            raise ValueError("supply distinct positive/negative labels together")
    if importlib.metadata.version("inspect-ai") != INSPECT_VERSION:
        raise ValueError("use the pinned optional integration environment")
    from inspect_ai.log import read_eval_log

    raw = path.read_bytes()
    if path.suffix == ".json":
        decode_json(raw.decode("utf-8"))
    log = read_eval_log(str(path))
    if digest(path.read_bytes()) != digest(raw):
        raise ValueError("Inspect log changed during import")
    declared = log.eval.metadata.get("brf", {}) if log.eval.metadata else {}
    for key, supplied in (("policy_snapshot_id", policy), ("target_revision", revision)):
        if supplied is not None and key in declared and declared[key] != supplied:
            raise ValueError(f"CLI and log disagree on {key}")
    policy = policy or declared.get("policy_snapshot_id")
    revision = revision or declared.get("target_revision")
    records, seen = [], set()
    for sample in log.samples or []:
        key = (type(sample.id).__name__, sample.id, sample.epoch)
        if key in seen:
            raise ValueError("duplicate Inspect sample ID/epoch")
        seen.add(key)
        scores = sample.scores or {}
        records.append({"sample_id": str(sample.id), "sample_id_type": "integer" if type(sample.id) is int else "string",
            "epoch": sample.epoch,
            "task_success": binary_score(scores[task_score].value, *task_labels) if task_score in scores else None,
            "boundary_violation": binary_score(scores[violation_score].value, *violation_labels) if violation_score in scores else None,
            "error": sample.error is not None or sample.invalidation is not None or sample.limit is not None
                     or any((scores[key].metadata or {}).get("brf_error") is True
                            for key in (task_score, violation_score) if key in scores)})
    planned = log.results.total_samples if log.results else None
    source = {"sha256": digest(raw), "producer": "inspect-ai", "producer_version": INSPECT_VERSION,
        "task": log.eval.task, "model": log.eval.model,
        "configuration": {"task_score": task_score, "violation_score": violation_score,
                          "task_labels": list(task_labels), "violation_labels": list(violation_labels),
                          "log_status": log.status, "log_version": log.version, "invalidated": log.invalidated,
                          "task_version": log.eval.task_version, "eval_id": log.eval.eval_id, "run_id": log.eval.run_id,
                          "generation": {key: getattr(log.eval.model_generate_config, key) for key in
                                         ("temperature", "top_p", "top_k", "seed", "max_tokens")
                                         if getattr(log.eval.model_generate_config, key) is not None}}}
    return bundle("Inspect", declared.get("source_kind", "supplied_evaluation"), source, policy, revision,
                  records, planned, log.status == "success" and not log.invalidated)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task-score", default="task_success")
    parser.add_argument("--violation-score", default="boundary_violation")
    parser.add_argument("--policy-snapshot-id")
    parser.add_argument("--target-revision")
    for prefix in ("task", "violation"):
        parser.add_argument(f"--{prefix}-positive")
        parser.add_argument(f"--{prefix}-negative")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        if args.output.resolve() == args.log.resolve():
            raise ValueError("output must not replace the Inspect log")
        result = export_log(args.log, args.task_score, args.violation_score, args.policy_snapshot_id,
                            args.target_revision, (args.task_positive, args.task_negative),
                            (args.violation_positive, args.violation_negative))
        write_evidence(result, "evaluation-evidence.schema.json", args.output, args.overwrite)
        print(f"{result['summary']['evaluation_status'].upper()}: {result['summary']['record_count']} samples; descriptive scores only")
        return int(result["summary"]["evaluation_status"] != "pass")
    except Exception as exc:
        print(f"ERROR: {exc}. Use .tools/integration-env/bin/python after installing optional integrations.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
