import unittest

from tools.evaluation_evidence import summarize
from tools.inspect_evidence import binary_score
from tools.opa_comparison import FIXTURE, load_json, run_case


class EvaluationEvidenceTests(unittest.TestCase):
    def record(self, task=True, violation=False, error=False):
        return {"task_success": task, "boundary_violation": violation, "error": error}

    def test_missing_scores_errors_and_incomplete_samples_are_inconclusive(self):
        for records, planned, complete in (([self.record(violation=None)], 1, True),
                                           ([self.record(error=True)], 1, True),
                                           ([self.record()], 2, True), ([self.record()], 1, False)):
            self.assertEqual(summarize(records, planned, complete)["evaluation_status"], "inconclusive")

    def test_violation_is_not_hidden_by_unknown_scores(self):
        self.assertEqual(summarize([self.record(violation=True), self.record(task=None)], 2, False)["evaluation_status"], "fail")

    def test_task_success_is_separate_from_boundary_violation(self):
        summary = summarize([self.record(task=False)], 1, True)
        self.assertEqual(summary["task_successes"], 0)
        self.assertEqual(summary["evaluation_status"], "pass")

    def test_unknown_planned_denominator_cannot_establish_completion(self):
        self.assertEqual(summarize([self.record()], None, True)["evaluation_status"], "inconclusive")

    def test_string_scores_require_explicit_mapping(self):
        for value in ("C", "I", "true", "1", 0.5, None, {}, []):
            self.assertIsNone(binary_score(value))
        self.assertTrue(binary_score("C", "C", "I"))
        self.assertFalse(binary_score("I", "C", "I"))
        self.assertIsNone(binary_score("unknown", "C", "I"))

    def test_opa_failure_denies_instead_of_dispatching(self):
        workload = load_json(FIXTURE / "scenarios.json")
        result = run_case("opa_enforced", workload["scenarios"][0], workload["context"], opa=FIXTURE / "missing-binary")
        self.assertEqual(result["receipts"], [])
        self.assertTrue(result["error"])
        self.assertFalse(result["boundary_violation"])

    def test_shape_validation_does_not_claim_semantic_containment(self):
        workload = load_json(FIXTURE / "scenarios.json")
        cross_tenant = workload["scenarios"][1]
        self.assertTrue(run_case("schema_only", cross_tenant, workload["context"])["boundary_violation"])


if __name__ == "__main__":
    unittest.main()
