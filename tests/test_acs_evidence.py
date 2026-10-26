import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.acs_evidence import acs_validators, export_bundle
from tools.demo_acs import demo, guardian, host, request
from tools.validate_json_schema import ROOT_DIR, load_json, make_validator, structural_errors


class AcsEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Missing upstream cache is an error, never an implicit skipped conformance run.
        cls.validators = acs_validators()

    def export(self, transcript):
        return export_bundle(transcript, self.validators, "0" * 64)

    def test_allow_deny_and_outage_have_observed_outcomes(self):
        bundle = self.export(demo())
        self.assertEqual(bundle["evaluation_status"], "pass")
        self.assertEqual([r["executed"] for r in bundle["records"]], [True, False, False])
        self.assertFalse(structural_errors(make_validator(load_json(ROOT_DIR / "spec/acs-evidence.schema.json")), bundle))

    def test_denial_bypass_is_reported_as_failure(self):
        transcript = demo()
        transcript["events"][1]["observation"] = {"executed": True, "outcome": "succeeded"}
        bundle = self.export(transcript)
        self.assertEqual(bundle["evaluation_status"], "fail")
        self.assertIn("not completion", bundle["brf_evidence_relevance"][0])

    def test_allowed_tool_failure_is_not_a_denial_bypass(self):
        transcript = demo()
        transcript["events"][0]["observation"]["outcome"] = "failed"
        self.assertEqual(self.export(transcript)["evaluation_status"], "pass")

    def test_unused_permission_is_inconclusive_not_a_denial_bypass(self):
        transcript = demo()
        transcript["events"][0]["observation"] = {"executed": False, "outcome": "blocked"}
        self.assertEqual(self.export(transcript)["evaluation_status"], "inconclusive")

    def test_cli_writes_nonpassing_bundles_and_returns_nonzero(self):
        for missing_policy in (False, True):
            transcript = demo()
            if missing_policy:
                transcript["events"][0]["response"]["result"].pop("policy_references")
            else:
                transcript["events"][1]["observation"] = {"executed": True, "outcome": "succeeded"}
            with tempfile.TemporaryDirectory() as tmp:
                source, output = Path(tmp) / "transcript.json", Path(tmp) / "bundle.json"
                source.write_text(json.dumps(transcript))
                run = subprocess.run([sys.executable, str(ROOT_DIR / "tools/acs_evidence.py"),
                                      str(source), "--output", str(output)], capture_output=True, text=True)
                self.assertEqual(run.returncode, 1, run.stderr)
                bundle = load_json(output)
                self.assertEqual(bundle["evaluation_status"], "inconclusive" if missing_policy else "fail")
                self.assertFalse(structural_errors(make_validator(load_json(ROOT_DIR / "spec/acs-evidence.schema.json")), bundle))

    def test_bad_policy_response_cannot_dispatch(self):
        for field, value in (("request_id", "wrong"), ("acs_version", "0.2.0"), ("policy_references", [])):
            def bad_service(req):
                response = guardian(req)
                response["result"][field] = value
                return response
            ledger = []
            with self.assertRaises(ValueError):
                host(request("invalid-response", 2), bad_service, ledger)
            self.assertEqual(ledger, [])

    def test_mismatched_response_and_duplicate_requests_are_rejected(self):
        transcript = demo()
        transcript["events"][0]["response"]["id"] = "wrong-request"
        with self.assertRaises(ValueError):
            self.export(transcript)
        transcript = demo()
        transcript["events"].append(copy.deepcopy(transcript["events"][0]))
        with self.assertRaises(ValueError):
            self.export(transcript)

    def test_missing_policy_reference_is_inconclusive(self):
        transcript = demo()
        transcript["events"][0]["response"]["result"].pop("policy_references")
        self.assertEqual(self.export(transcript)["evaluation_status"], "inconclusive")

    def test_acs_payload_invalid_argument_is_rejected(self):
        transcript = demo()
        transcript["events"][0]["request"]["params"]["payload"]["arguments"]["amount"] = 2
        with self.assertRaises(ValueError):
            self.export(transcript)

    def test_timeout_does_not_execute(self):
        def timeout(_):
            raise TimeoutError("fixture timeout")
        ledger = []
        event = host(request("timeout", 2), timeout, ledger)
        self.assertEqual(ledger, [])
        self.assertFalse(event["observation"]["executed"])


if __name__ == "__main__":
    unittest.main()
