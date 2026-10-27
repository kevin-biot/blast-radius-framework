"""Live signed-JWT resource boundary, local revocation and effect observations."""
import base64
import json
import tempfile
import shutil
import time
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPConnection
from unittest.mock import patch
from urllib.parse import urlsplit

import jwt

from tools.credential_tokens import CredentialError, FixtureIssuer, verify_token
from tools.dsse_evidence import seal, verify
from tools.evidence_common import digest, write_evidence
from tools.run_credential_boundary import CredentialTool, check_packet, run
from tools.validate_json_schema import ROOT_DIR, load_json, make_validator, structural_errors
from cryptography.hazmat.primitives import serialization


class CredentialBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory()
        cls.root = Path(cls.workspace.name)
        try:
            cls.result = run(cls.root / "credential-run")
            cls.context = load_json(cls.root / "credential-run/credential-context.json")
        except BaseException:
            cls.workspace.cleanup()
            raise
        cls.cases = {row["case_id"]: row for row in cls.result["cases"]}
        cls.records = {row["case_id"]: row for row in cls.context["records"]}

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def test_all_cases_schema_versions_and_bound_capture_hashes(self):
        self.assertEqual(len(self.result["cases"]), 34)
        self.assertEqual(len(self.context["records"]), 34)
        self.assertTrue(self.result["expectations_met"])
        self.assertEqual(self.result["boundary_violation_cases"], 3)
        self.assertEqual(self.result["schema_version"], "0.1.1")
        write_evidence(self.result, "execution-evidence.schema.json", self.root / "execution.json")
        write_evidence(self.result, "execution-evidence.schema.json", self.root / "credential-run/evidence.json")
        self.assertTrue(check_packet(self.root / "credential-run")["expectations_met"])
        self.assertFalse(structural_errors(make_validator(load_json(ROOT_DIR / "spec/credential-context.schema.json")), self.context))
        for capture in self.result["captures"]:
            self.assertEqual(capture["sha256"], digest((self.root / "credential-run" / capture["path"]).read_bytes()))
        older_label = {**self.result, "schema_version": "0.1.0"}
        self.assertTrue(structural_errors(make_validator(load_json(ROOT_DIR / "spec/execution-evidence.schema.json")), older_label))

    def test_signature_issuer_audience_tenant_scope_and_expiry_denials(self):
        for name, reason in (("wrong_signing_key", "invalid_credential"), ("tampered_signed_claims", "invalid_credential"),
                             ("wrong_issuer", "wrong_issuer"), ("wrong_audience", "wrong_audience"),
                             ("wrong_tenant", "wrong_tenant"), ("missing_scope", "insufficient_scope"),
                             ("expired_credential", "expired_credential"), ("not_yet_valid", "credential_not_yet_valid")):
            with self.subTest(case=name):
                self.assertEqual(self.cases[name]["observed_committed_amount"], 0)
                self.assertEqual(self.records[name]["error_reasons"], [reason])
                self.assertTrue(all(row["spent"] == 0 for row in self.records[name]["tenant_balances"]))

    def test_algorithm_type_missing_claim_and_lifetime_controls(self):
        for name in ("missing_required_claim", "id_token_type_rejected", "symmetric_algorithm_rejected",
                     "unsecured_token_rejected", "boolean_expiry_rejected", "excessive_credential_lifetime"):
            self.assertEqual(self.records[name]["http_statuses"], [401])
            self.assertEqual(self.cases[name]["receipts"], [])

    def test_key_hints_are_not_key_discovery(self):
        self.assertEqual(self.cases["key_id_is_not_trust"]["observed_committed_amount"], 1)
        self.assertEqual(self.cases["key_discovery_header_rejected"]["observed_committed_amount"], 0)
        issuer = FixtureIssuer()
        token, claims = issuer.issue()
        token = jwt.encode(claims, issuer.key, algorithm="EdDSA", headers={"typ": "at+jwt", "jku": "https://example.invalid/key"})
        with patch("urllib.request.urlopen", side_effect=AssertionError("no key fetch")) as network:
            with self.assertRaises(CredentialError):
                verify_token(token, issuer.key.public_key(), "alpha")
            network.assert_not_called()

    def test_revocation_and_unavailability_are_fail_closed(self):
        for name, status in (("revoked_before_dispatch", 401), ("revocation_state_unavailable", 503),
                             ("revocation_binds_issuer_jti_not_encoding", 401)):
            self.assertEqual(self.records[name]["http_statuses"], [status])
            self.assertEqual(self.cases[name]["observed_committed_amount"], 0)
        self.assertEqual(self.records["retry_requires_current_credential"]["http_statuses"], [200, 401])
        self.assertEqual(len(self.cases["retry_requires_current_credential"]["receipts"]), 1)

    def test_idempotency_is_scoped_to_tenant_principal_and_client(self):
        for dimension, field in (("tenant", "tenant"), ("principal", "principal"), ("client", "client_id")):
            record = self.records["idempotency_namespace_" + dimension]
            self.assertEqual(record["http_statuses"], [200, 200])
            self.assertEqual(len({row[field] for row in record["receipts"]}), 2)
            self.assertEqual(len({row["seq"] for row in record["receipts"]}), 2)

    def test_inflight_rechecks_and_unsafe_admission_controls(self):
        for fault in ("revoked", "expired", "unavailable"):
            strict, stale = self.cases["inflight_" + fault + "_commit_recheck"], self.cases["inflight_" + fault + "_admission_only"]
            self.assertEqual(strict["observed_committed_amount"], 0)
            self.assertFalse(strict["boundary_violation"])
            self.assertEqual(stale["observed_committed_amount"], 1)
            self.assertTrue(stale["boundary_violation"])
            if fault == "expired":
                self.assertEqual(self.records["inflight_expired_commit_recheck"]["error_reasons"], ["expired_credential"])

    def test_committed_residual_and_bearer_reuse_are_not_hidden(self):
        residual = self.cases["revocation_cannot_undo_commit"]
        self.assertEqual(residual["residual_amount"], 1)
        self.assertFalse(residual["boundary_violation"])
        name = "bearer_reuse_is_not_prevented_but_budget_is_bounded"
        self.assertEqual(self.cases[name]["observed_committed_amount"], 3)
        self.assertFalse(self.cases[name]["boundary_violation"])
        alpha = next(row for row in self.records[name]["tenant_balances"] if row["tenant"] == "alpha")
        self.assertEqual(alpha["spent"], alpha["budget"])
        self.assertEqual(self.records[name]["http_statuses"], [200, 200, 200, 403])

    def test_data_and_control_plane_credentials_are_not_interchangeable(self):
        for name in ("admin_secret_not_access_token", "agent_cannot_use_admin_control"):
            self.assertEqual(self.records[name]["http_statuses"], [401])
            self.assertEqual(self.cases[name]["receipts"], [])

    def test_duplicate_jwt_json_and_ambiguous_claim_types_fail(self):
        issuer = FixtureIssuer()
        token, claims = issuer.issue()
        header = base64.urlsafe_b64encode(b'{"alg":"EdDSA","typ":"at+jwt"}').rstrip(b"=")
        payload = json.dumps(claims).encode()[:-1] + b',"aud":"urn:brf:fixture:credential-ledger"}'
        payload = base64.urlsafe_b64encode(payload).rstrip(b"=")
        message = header + b"." + payload
        duplicate = (message + b"." + base64.urlsafe_b64encode(issuer.key.sign(message)).rstrip(b"=")).decode()
        with self.assertRaises(CredentialError):
            verify_token(duplicate, issuer.key.public_key(), "alpha")
        nested = base64.urlsafe_b64encode(b'{"nested":' + b'[' * 1200 + b'0' + b']' * 1200 + b'}').rstrip(b"=")
        message = header + b"." + nested
        deeply_nested = (message + b"." + base64.urlsafe_b64encode(issuer.key.sign(message)).rstrip(b"=")).decode()
        with self.assertRaises(CredentialError):
            verify_token(deeply_nested, issuer.key.public_key(), "alpha")
        for updates in ({"exp": True}, {"exp": str(int(time.time()) + 60)}, {"aud": [claims["aud"]]},
                        {"scope": ["ledger:increment"]}, {"scope": "ledger:increment\nledger:other"}):
            forged = jwt.encode({**claims, **updates}, issuer.key, algorithm="EdDSA", headers={"typ": "at+jwt"})
            with self.assertRaises(CredentialError):
                verify_token(forged, issuer.key.public_key(), "alpha")

    def test_request_fields_retry_conflicts_and_agent_state_access(self):
        issuer = FixtureIssuer()
        token, _ = issuer.issue()
        with CredentialTool(self.root / "request-checks", issuer.public_bytes()) as tool:
            route, body = "/tenants/alpha/increment", {"operation_id": "same", "amount": 1}
            self.assertEqual(tool.call(route, {**body, "tenant": "beta"}, token=token)[0], 400)
            first, retry = tool.call(route, body, token=token), tool.call(route, body, token=token)
            self.assertEqual(first[1]["seq"], retry[1]["seq"])
            self.assertTrue(retry[1]["replayed"])
            self.assertEqual(tool.call(route, {**body, "amount": 2}, token=token)[0], 409)
            self.assertEqual(tool.call("/state", token=token)[0], 401)
            address = urlsplit(tool.url)
            connection = HTTPConnection(address.hostname, address.port, timeout=10)
            try:
                raw = json.dumps({"operation_id": "duplicate-header", "amount": 1}).encode()
                connection.putrequest("POST", route)
                connection.putheader("Authorization", "Bearer " + token)
                connection.putheader("Authorization", "Bearer " + token)
                connection.putheader("Content-Length", str(len(raw)))
                connection.endheaders(raw)
                response = connection.getresponse()
                self.assertEqual(response.status, 401)
                response.read()
            finally:
                connection.close()
            self.assertEqual(tool.observe()["spent"], 1)

    def test_concurrent_principals_share_one_atomic_tenant_budget(self):
        issuer = FixtureIssuer()
        tokens = [issuer.issue(sub="fixture-agent-" + str(i))[0] for i in range(2)]
        with CredentialTool(self.root / "concurrent-budget", issuer.public_bytes()) as tool, ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(tool.call, "/tenants/alpha/increment", {"operation_id": "parallel", "amount": 2,
                       "wait_before": "both"}, token) for token in tokens]
            tool.wait_for(2)
            tool.call("/release", {"gate": "both"})
            results = [future.result(timeout=8) for future in futures]
            self.assertEqual(sorted(status for status, _ in results), [200, 403])
            observation, receipts, balances = tool.observe_details()
            self.assertEqual(observation["spent"], 2)
            self.assertEqual(len(receipts), 1)
            self.assertEqual(next(row["spent"] for row in balances if row["tenant"] == "beta"), 0)

    def test_no_private_keys_or_bearer_tokens_in_exported_captures(self):
        text = json.dumps(self.result) + json.dumps(self.context)
        self.assertNotIn("PRIVATE KEY", text)
        self.assertNotIn("Bearer ", text)
        self.assertNotIn("eyJ", text)
        self.assertEqual(self.context["mandate_status"], "not_established")
        self.assertFalse(list((self.root / "credential-run").rglob("token")))
        self.assertFalse(list((self.root / "credential-run").rglob("*private*")))

    def test_new_execution_bundle_remains_portable_without_predicate_change(self):
        issuer = FixtureIssuer()
        private, public = self.root / "demo-private.pem", self.root / "demo-public.pem"
        private.write_bytes(issuer.key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        public.write_bytes(issuer.public_bytes())
        try:
            source = self.root / "credential-execution.json"
            write_evidence(self.result, "execution-evidence.schema.json", source)
            envelope = self.root / "credential.dsse.json"
            write_evidence(seal(source, "execution", private, signing_context="ephemeral_demo_key"), "dsse-envelope.schema.json", envelope)
            checked = verify(envelope, source, public)
            self.assertTrue(checked["signature_verified"])
            self.assertFalse(checked["authority_verified"])
        finally:
            private.unlink(missing_ok=True)

    def test_packet_tampering_and_accounting_mismatches_are_rejected(self):
        directory = self.root / "tampered-packet"
        directory.mkdir()
        for name in ("evidence.json", "credential-context.json", "issuer-public.pem"):
            if name == "evidence.json":
                write_evidence(self.result, "execution-evidence.schema.json", directory / name)
            else:
                shutil.copyfile(self.root / "credential-run" / name, directory / name)
        context_path = directory / "credential-context.json"
        context = load_json(context_path)
        context["records"][0]["tenant_balances"][0]["spent"] += 1
        context_path.write_text(json.dumps(context))
        with self.assertRaises(ValueError):
            check_packet(directory)
        result = load_json(directory / "evidence.json")
        next(c for c in result["captures"] if c["path"] == context_path.name)["sha256"] = digest(context_path.read_bytes())
        (directory / "evidence.json").write_text(json.dumps(result))
        with self.assertRaises(ValueError):
            check_packet(directory)
        result["captures"][0]["path"] = "../not-followed"
        (directory / "evidence.json").write_text(json.dumps(result))
        with self.assertRaises(ValueError):
            check_packet(directory)
        context_path.write_bytes((self.root / "credential-run/credential-context.json").read_bytes())
        (directory / "evidence.json").write_text(json.dumps(self.result))
        self.assertTrue(check_packet(directory)["expectations_met"])
        key = directory / "issuer-public.pem"
        key.unlink()
        key.symlink_to(self.root / "credential-run/issuer-public.pem")
        with self.assertRaises(ValueError):
            check_packet(directory)


if __name__ == "__main__":
    unittest.main()
