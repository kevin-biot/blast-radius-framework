import copy
import json
import tempfile
import unittest
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from tools.acs_trace_evidence import attributes, read_trace

SESSION = str(uuid5(NAMESPACE_URL, "brf-trace-test-session"))
REQUEST = str(uuid5(NAMESPACE_URL, "brf-trace-test-request"))
MAPPING = {"properties": {
    "step_to_span": {"default": {name: {"span_name": name} for name in ("gen_ai.tool.call", "gen_ai.tool.result", "acs.session")}},
    "decision_failure_event": {"properties": {"attribute_values": {"default": {
        "acs.failure.class": ["timeout", "unreachable", "handshake_failure", "other"],
        "acs.failure.posture": ["fail_open", "fail_closed"], "acs.failure.reported_by": ["guardian", "observed_agent"]}}}}
}}


def attr(key, value):
    encoded = {"arrayValue": {"values": [{"stringValue": v} for v in value]}} if isinstance(value, list) else {"stringValue": value}
    return {"key": key, "value": encoded}


def span(index=1, session=SESSION, request=REQUEST, name="gen_ai.tool.call", verdict="allow", failure=None):
    events = []
    if verdict is not None:
        events.append({"name": "acs.decision", "attributes": [attr("acs.decision", verdict)]})
    if failure:
        events.append({"name": "acs.decision.failure", "attributes": [attr("acs.failure." + k, v) for k, v in failure.items()]})
    return {"traceId": f"{index:032x}", "spanId": f"{index:016x}", "name": name,
            "attributes": [attr("acs.session.id", session), attr("acs.request_id", request)], "events": events}


class TraceEvidenceTests(unittest.TestCase):
    def analyze(self, *spans):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.jsonl"
            path.write_text(json.dumps({"resourceSpans": [{"scopeSpans": [{"spans": list(spans)}]}]}))
            return read_trace([path], MAPPING)

    def test_verdict_does_not_prove_enforcement(self):
        record = self.analyze(span(verdict="deny"))["records"][0]
        self.assertTrue(record["decision_usable_as_reported"])
        self.assertEqual(record["enforcement_status"], "not_verified")

    def test_host_failure_invalidates_guardian_verdict_across_trace_ids(self):
        failure = {"class": "timeout", "posture": "fail_closed", "reported_by": "observed_agent"}
        result = self.analyze(span(), span(2, verdict=None, failure=failure))
        self.assertEqual(len(result["records"]), 1)
        self.assertFalse(result["records"][0]["decision_usable_as_reported"])
        self.assertEqual(result["failure_pair_count"], 1)

    def test_failure_pairs_are_not_double_counted(self):
        failure = {"class": "timeout", "posture": "fail_open", "reported_by": "guardian"}
        first = span(failure=failure)
        second = span(2, verdict=None, failure=dict(failure, reported_by="observed_agent"))
        result = self.analyze(first, second)
        self.assertEqual(result["failure_pair_count"], 1)
        self.assertEqual(result["analysis_status"], "findings")

    def test_same_request_id_in_other_session_is_not_joined(self):
        other = str(uuid5(NAMESPACE_URL, "other-session"))
        failure = {"class": "timeout", "posture": "fail_closed", "reported_by": "observed_agent"}
        result = self.analyze(span(), span(2, session=other, verdict=None, failure=failure))
        first = next(r for r in result["records"] if r["session_id"] == SESSION)
        self.assertTrue(first["decision_usable_as_reported"])

    def test_handshake_failure_invalidates_the_session_not_other_sessions(self):
        failure = {"class": "handshake_failure", "posture": "fail_closed", "reported_by": "observed_agent"}
        handshake = span(2, request=str(uuid5(NAMESPACE_URL, "handshake")), name="acs.session", verdict=None, failure=failure)
        result = self.analyze(span(), handshake)
        self.assertTrue(all(not r["decision_usable_as_reported"] for r in result["records"]))

    def test_result_join_uses_request_reference_and_session(self):
        result_span = span(2, request=str(uuid5(NAMESPACE_URL, "result")), name="gen_ai.tool.result")
        result_span["attributes"] += [attr("acs.request_id_ref", REQUEST), attr("gen_ai.tool.name", "ledger.increment"), attr("acs.exit_status", "success")]
        records = self.analyze(span(), result_span)["records"]
        first = next(r for r in records if r["request_id"] == REQUEST)
        self.assertEqual(first["reported_tool_results"][0]["exit_status"], "success")
        self.assertEqual(first["enforcement_status"], "not_verified")
        orphan = self.analyze(result_span)["records"][0]
        self.assertIn(REQUEST, orphan["tool_result_request_refs"])
        self.assertTrue(orphan["findings"])

    def test_conflicting_verdicts_and_chain_hashes_are_findings(self):
        first, second = span(), span(2, verdict="deny")
        first["events"][0]["attributes"].append(attr("acs.chain_hash", "first"))
        second["events"][0]["attributes"].append(attr("acs.chain_hash", "second"))
        result = self.analyze(first, second)
        self.assertEqual(result["analysis_status"], "findings")
        self.assertFalse(result["records"][0]["decision_usable_as_reported"])

    def test_duplicate_attributes_and_conflicting_exports_are_rejected(self):
        with self.assertRaises(ValueError):
            attributes([attr("same", "a"), attr("same", "b")])
        second = copy.deepcopy(span())
        second["events"][0]["attributes"][0] = attr("acs.decision", "deny")
        with self.assertRaises(ValueError):
            self.analyze(span(), second)

    def test_duplicate_identical_exports_are_deduplicated(self):
        self.assertEqual(len(self.analyze(span(), span())["records"]), 1)

    def test_misaligned_policy_arrays_are_rejected(self):
        item = span()
        item["events"][0]["attributes"] += [attr("acs.policy.ids", ["p"]), attr("acs.policy.versions", []), attr("acs.policy.rule_ids", ["r"])]
        with self.assertRaises(ValueError):
            self.analyze(item)

    def test_dropped_telemetry_prevents_positive_eligibility(self):
        item = span()
        item["droppedEventsCount"] = 1
        self.assertFalse(self.analyze(item)["records"][0]["decision_usable_as_reported"])

    def test_unknown_span_cannot_hide_a_matching_failure(self):
        failure = {"class": "timeout", "posture": "fail_closed", "reported_by": "observed_agent"}
        result = self.analyze(span(), span(2, name="unknown.host.span", verdict=None, failure=failure))
        self.assertEqual(result["failure_pair_count"], 1)
        self.assertFalse(result["records"][0]["decision_usable_as_reported"])


if __name__ == "__main__":
    unittest.main()
