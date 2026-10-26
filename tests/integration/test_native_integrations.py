"""Required optional-runtime tests: missing Inspect/OPA/ACS assets are errors, not skips."""
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from inspect_ai.log import read_eval_log, write_eval_log

from tools.acs_trace_evidence import read_trace, trace_assets
from tools.evidence_common import digest, write_evidence
from tools.fetch_acs_trace_assets import CACHE
from tools.inspect_evidence import export_log
from tools.opa_comparison import comparison
from tools.run_inspect_demo import run_demo
from tools.validate_json_schema import ROOT_DIR


class NativeIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory()
        cls.root = Path(cls.workspace.name)
        cls.log_path = run_demo(cls.root / "logs")

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def export_modified(self, transform, native_json=False, **kwargs):
        log = read_eval_log(str(self.log_path))
        transform(log)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ("modified.json" if native_json else "modified.eval")
            if native_json:
                path.write_text(log.model_dump_json())
            else:
                write_eval_log(log, path, format="eval")
            return export_log(path, **kwargs)

    def test_pinned_upstream_trace_sample(self):
        mapping, manifest = trace_assets()
        result = read_trace([CACHE / "sample.jsonl"], mapping)
        result["mapping_sha256"] = manifest["files"]["otel-mapping.json"]["sha256"]
        self.assertEqual(len(result["records"]), 6)
        self.assertEqual(result["failure_pair_count"], 3)
        self.assertEqual(result["analysis_status"], "findings")
        self.assertTrue(all(r["enforcement_status"] == "not_verified" for r in result["records"]))
        late = next(r for r in result["records"] if r["verdicts"] == ["allow"] and r["failures"])
        self.assertFalse(late["decision_usable_as_reported"])
        write_evidence(result, "acs-trace-evidence.schema.json", self.root / "native-trace.json")

    def test_real_opa_comparison(self):
        result = comparison()
        self.assertEqual(result["source_kind"], "local_fixture")
        for mode, violations in (("unmediated", 6), ("schema_only", 6), ("opa_enforced", 0)):
            rows = [r for r in result["records"] if r["mode"] == mode]
            self.assertEqual(len(rows), 8)
            self.assertEqual(sum(r["boundary_violation"] for r in rows), violations)
            self.assertFalse(any(r["error"] for r in rows))
        write_evidence(result, "evaluation-evidence.schema.json", self.root / "opa.json")

    def test_native_eval_export_has_separate_scores_and_no_model_usage(self):
        result = export_log(self.log_path)
        self.assertEqual(result["source_format"], "Inspect")
        self.assertEqual(result["summary"]["record_count"], 8)
        self.assertEqual(result["summary"]["task_successes"], 8)
        self.assertEqual(result["summary"]["violation_records"], 0)
        self.assertEqual(result["summary"]["evaluation_status"], "pass")
        self.assertEqual(result["source_kind"], "local_fixture")
        self.assertTrue(all(not s.model_usage for s in read_eval_log(str(self.log_path)).samples))
        write_evidence(result, "evaluation-evidence.schema.json", self.root / "inspect.json")

    def test_native_json_log_export(self):
        path = self.root / "inspect-log.json"
        write_eval_log(read_eval_log(str(self.log_path)), path, format="json")
        self.assertEqual(export_log(path)["summary"]["evaluation_status"], "pass")

    def test_missing_score_is_unknown_not_success(self):
        def modify(log):
            log.samples[0].scores.pop("boundary_violation")
        result = self.export_modified(modify)
        self.assertEqual(result["summary"]["evaluation_status"], "inconclusive")
        self.assertEqual(result["summary"]["unknown_or_error_records"], 1)

    def test_cancelled_and_invalidated_logs_cannot_pass(self):
        for field, value in (("status", "cancelled"), ("invalidated", True)):
            result = self.export_modified(lambda log: setattr(log, field, value))
            self.assertEqual(result["summary"]["evaluation_status"], "inconclusive")

    def test_truncated_log_cannot_pass(self):
        result = self.export_modified(lambda log: log.samples.pop())
        self.assertEqual(result["summary"]["evaluation_status"], "inconclusive")
        self.assertEqual(result["summary"]["planned_samples"], 8)

    def test_missing_planned_denominator_is_inconclusive(self):
        result = self.export_modified(lambda log: setattr(log, "results", None))
        self.assertEqual(result["summary"]["evaluation_status"], "inconclusive")
        self.assertIsNone(result["summary"]["planned_samples"])

    def test_policy_error_score_metadata_is_not_hidden(self):
        def modify(log):
            log.samples[0].scores["task_success"].metadata = {"brf_error": True}
        result = self.export_modified(modify)
        self.assertTrue(result["records"][0]["error"])
        self.assertEqual(result["summary"]["evaluation_status"], "inconclusive")

    def test_string_scores_need_explicit_mapping_for_each_scorer(self):
        def modify(log):
            for sample in log.samples:
                sample.scores["task_success"].value = "C"
                sample.scores["boundary_violation"].value = "I"
        self.assertEqual(self.export_modified(modify)["summary"]["evaluation_status"], "inconclusive")
        result = self.export_modified(modify, task_labels=("C", "I"), violation_labels=("C", "I"))
        self.assertEqual(result["summary"]["evaluation_status"], "pass")

    def test_duplicate_sample_epoch_and_conflicting_provenance_are_rejected(self):
        with self.assertRaises(ValueError):
            # The .eval writer coalesces duplicate IDs; JSON can represent this invalid input.
            self.export_modified(lambda log: log.samples.append(copy.deepcopy(log.samples[0])), native_json=True)
        with self.assertRaises(ValueError):
            export_log(self.log_path, policy="not-the-recorded-policy")

    def test_cli_does_not_overwrite_input_or_existing_output(self):
        before = digest(self.log_path.read_bytes())
        command = [sys.executable, str(ROOT_DIR / "tools/inspect_evidence.py"), str(self.log_path), "--output"]
        result = subprocess.run(command + [str(self.log_path), "--overwrite"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(digest(self.log_path.read_bytes()), before)
        output = self.root / "existing-output.json"
        output.write_text("preserve me")
        result = subprocess.run(command + [str(output)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output.read_text(), "preserve me")


if __name__ == "__main__":
    unittest.main()
