"""Conservative summaries for explicitly scored evaluation records."""
from __future__ import annotations

try:
    from .evidence_common import now
except ImportError:
    from evidence_common import now


def summarize(records, planned, source_complete):
    if not records:
        raise ValueError("evaluation contains no samples")
    known = [r for r in records if r["task_success"] is not None and r["boundary_violation"] is not None and not r["error"]]
    violations = sum(r["boundary_violation"] is True for r in records)
    complete = source_complete and len(known) == len(records) and planned is not None and planned == len(records)
    return {"record_count": len(records), "complete_records": len(known),
            "unknown_or_error_records": len(records) - len(known),
            "task_successes": sum(r["task_success"] is True for r in records),
            "violation_records": violations, "planned_samples": planned,
            "evaluation_status": "fail" if violations else "pass" if complete else "inconclusive"}


def bundle(source_format, source_kind, source, policy, revision, records, planned=None, complete=True):
    if any(not isinstance(v, str) or not v.strip() for v in (policy, revision)):
        raise ValueError("nonempty policy snapshot and target revision are required")
    if source_kind not in {"local_fixture", "supplied_evaluation"}:
        raise ValueError("source kind must be explicit")
    summary = summarize(records, planned, complete)
    return {"bundle_version": "0.1", "source_format": source_format, "source_kind": source_kind,
            "created_at": now(), "source": source, "policy_snapshot_id": policy, "target_revision": revision,
            "records": records, "summary": summary, "statistical_scope": "descriptive_only",
            "limits": ["Results describe supplied scenarios and scorer definitions, not production failure rates or a BR class.",
                       "A pass means complete declared scores with no reported violation, not independent conformance verification.",
                       "Scorer outputs and provenance require audit; signing and independent anchoring are not performed.",
                       "No confidence interval or population generalisation is claimed for this selected scenario set."]}
