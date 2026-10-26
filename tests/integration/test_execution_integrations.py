"""Real subprocess/tool integration; dependency failures must never become skips."""
import tempfile
import unittest
from pathlib import Path

from tools.evidence_common import write_evidence
from tools.execution_fixture import Tool
from tools.run_acs_live import run as run_acs
from tools.run_async_boundary import run as run_async
from tools.validate_json_schema import load_json


class ExecutionIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory()
        cls.root = Path(cls.workspace.name)
        try:
            cls.acs = run_acs(cls.root / "acs")
            cls.asynchronous = run_async(cls.root / "async")
        except BaseException:
            cls.workspace.cleanup()
            raise
        cls.live_cases = {row["case_id"]: row for row in cls.acs["cases"]}
        cls.async_cases = {row["case_id"]: row for row in cls.asynchronous["cases"]}

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def test_all_expected_outcomes_and_evidence_schemas(self):
        for name, result in (("acs", self.acs), ("async", self.asynchronous)):
            self.assertTrue(result["expectations_met"])
            self.assertEqual(len(result["cases"]), 8 if name == "acs" else 11)
            self.assertEqual(result["boundary_violation_cases"], 3 if name == "acs" else 2)
            write_evidence(result, "execution-evidence.schema.json", self.root / (name + "-evidence.json"))

    def test_live_allow_deny_and_bypass_have_real_receipts(self):
        for posture in ("default", "deny"):
            for scenario, amount in (("allow", 1), ("deny", 0), ("deny_bypass_control", 1)):
                row = self.live_cases[posture + "-" + scenario]
                self.assertEqual(row["observed_committed_amount"], amount)
                self.assertEqual(row["boundary_violation"], scenario == "deny_bypass_control")
                self.assertTrue(row["acs_request_id"])
            self.assertNotEqual(self.live_cases[posture + "-deny"]["acs_request_id"],
                                self.live_cases[posture + "-deny_bypass_control"]["acs_request_id"])

    def test_live_outage_preserves_default_and_explicit_postures(self):
        self.assertEqual(self.live_cases["default-outage"]["observed_committed_amount"], 1)
        self.assertEqual(self.live_cases["deny-outage"]["observed_committed_amount"], 0)
        for posture in ("default", "deny"):
            trace = load_json(self.root / "acs" / posture / "trace-analysis.json")
            self.assertTrue(all(r["enforcement_status"] == "not_verified" for r in trace["records"]))
            outage = next(r for r in trace["records"] if r["request_id"] == self.live_cases[posture + "-outage"]["acs_request_id"])
            self.assertTrue(outage["failures"])
            self.assertFalse(outage["decision_usable_as_reported"])

    def test_retry_and_idempotency_have_one_committed_effect(self):
        for name in ("sequential_retry", "retry_after_lost_response", "conflicting_idempotency_payload", "concurrent_same_key"):
            row = self.async_cases[name]
            self.assertEqual(len(row["receipts"]), 1)
            self.assertEqual(row["observed_committed_amount"], 1)
            self.assertTrue(all(row["checks"].values()))

    def test_atomic_budget_and_stale_check_negative_control(self):
        self.assertEqual(self.async_cases["aggregate_budget_atomic"]["spent"], 2)
        stale = self.async_cases["aggregate_budget_check_then_commit"]
        self.assertEqual(stale["spent"], 4)
        self.assertGreater(stale["spent"], stale["budget"])
        self.assertTrue(stale["boundary_violation"])

    def test_revocation_checks_and_irreversible_residual(self):
        for name in ("revoked_before_dispatch", "revoked_inflight_atomic"):
            self.assertEqual(self.async_cases[name]["observed_committed_amount"], 0)
        self.assertTrue(self.async_cases["revoked_inflight_check_then_commit"]["boundary_violation"])
        row = self.async_cases["revocation_does_not_undo_committed_effect"]
        self.assertEqual(row["residual_amount"], 1)
        self.assertFalse(row["active"])
        self.assertFalse(row["boundary_violation"])

    def test_auth_input_validation_and_missing_evidence_are_not_success(self):
        with Tool(self.root / "validation-tool") as tool:
            for amount in (True, -1, 0, 4, "1"):
                self.assertEqual(tool.call("/commit", {"operation_id": "bad", "amount": amount})[0], 400)
            self.assertEqual(tool.call("/commit", {"operation_id": "bad", "amount": 1}, token="wrong")[0], 401)
            self.assertEqual(tool.observe()["receipts"], [])
            tool.database.unlink()
            with self.assertRaises(Exception):
                tool.observe()

    def test_fresh_run_and_output_guards(self):
        for runner, directory in ((run_acs, self.root / "acs"), (run_async, self.root / "async")):
            with self.assertRaises(FileExistsError):
                runner(directory)
        target = self.root / "no-clobber.json"
        write_evidence(self.acs, "execution-evidence.schema.json", target)
        with self.assertRaises(FileExistsError):
            write_evidence(self.asynchronous, "execution-evidence.schema.json", target)


if __name__ == "__main__":
    unittest.main()
