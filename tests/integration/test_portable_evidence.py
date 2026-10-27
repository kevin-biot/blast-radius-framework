"""DSSE signature/binding tests, including a separate stdlib/OpenSSL path."""
import base64
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from tools.dsse_evidence import MEDIA_TYPE, VerificationError, pae, seal, verify
from tools.evidence_common import write_evidence
from tools.execution_fixture import ROOT
from tools.run_portability_demo import run as run_demo


def fixture():
    return {"schema_version": "0.1.0", "kind": "async_boundary", "generated_at": "2026-10-27T10:00:00Z",
        "scope": "local_fixed_proposal_mechanism_test", "observer": "same_machine_read_only_sqlite",
        "authority_scope": "fixture_runtime_grants_only", "signed": False, "upstream": None,
        "artifacts": [{"path": "fictional-tool", "sha256": "a" * 64}], "expectations_met": True,
        "boundary_violation_cases": 0, "cases": [{"case_id": "fixture", "decision": "not_applicable",
            "expected_committed_amount": 1, "observed_committed_amount": 1, "expectation_met": True,
            "boundary_violation": False, "residual_amount": 0, "active": True, "budget": 3, "spent": 1,
            "receipts": [{"seq": 1, "operation_id": "example", "amount": 1, "payload_hash": "b" * 64,
                          "committed_ns": 1793100000000000001}]}]}


class PortableEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.root = Path(self.workspace.name)
        self.addCleanup(self.workspace.cleanup)
        self.key = Ed25519PrivateKey.generate()
        self.private, self.public = self.root / "private.pem", self.root / "public.pem"
        self.private.write_bytes(self.key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        self.public.write_bytes(self.key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
        self.evidence = self.root / "evidence.json"
        write_evidence(fixture(), "execution-evidence.schema.json", self.evidence)
        self.envelope = seal(self.evidence, "execution", self.private)
        self.path = self.root / "envelope.json"

    def save(self):
        self.path.write_text(json.dumps(self.envelope))

    def openssl(self, success=True, evidence=None, public=None):
        self.save()
        result = subprocess.run([sys.executable, "-I", str(ROOT / "tools/verify_dsse_openssl.py"),
            "--envelope", str(self.path), "--evidence", str(evidence or self.evidence),
            "--public-key", str(public or self.public), "--openssl", os.environ.get("BRF_OPENSSL", "openssl")],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)

    def resign(self, transform, media=MEDIA_TYPE):
        statement = json.loads(base64.b64decode(self.envelope["payload"]))
        transform(statement)
        raw = json.dumps(statement, separators=(",", ":")).encode()
        self.envelope = {"payloadType": media, "payload": base64.b64encode(raw).decode(),
                         "signatures": [{"sig": base64.b64encode(self.key.sign(pae(media, raw))).decode()}]}
        self.save()

    def test_pae_known_vector_and_utf8_byte_lengths(self):
        self.assertEqual(pae("http://example.com/HelloWorld", b"hello world"),
                         b"DSSEv1 29 http://example.com/HelloWorld 11 hello world")
        self.assertEqual(pae("\u00e9", b"\x00\xff"), b"DSSEv1 2 \xc3\xa9 2 \x00\xff")

    def test_native_and_independent_openssl_verification(self):
        self.save()
        result = verify(self.path, self.evidence, self.public)
        self.assertTrue(result["signature_verified"])
        self.assertFalse(result["evidence_claims_verified"])
        self.assertFalse(result["authority_verified"])
        self.assertEqual(result["statement"]["predicate"]["evidence"]["cases"][0]["receipts"][0]["committed_ns"], 1793100000000000001)
        self.openssl()

    def test_tampered_signature_and_payload_are_rejected(self):
        for field in ("payload", "sig"):
            with self.subTest(field=field):
                original = copy.deepcopy(self.envelope)
                target = self.envelope if field == "payload" else self.envelope["signatures"][0]
                data = bytearray(base64.b64decode(target[field]))
                data[-1] ^= 1
                target[field] = base64.b64encode(data).decode()
                self.save()
                with self.assertRaises(VerificationError):
                    verify(self.path, self.evidence, self.public)
                self.openssl(False)
                self.envelope = original

    def test_wrong_key_and_subject_bytes_are_rejected(self):
        other = self.root / "other.pem"
        other.write_bytes(Ed25519PrivateKey.generate().public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
        self.save()
        with self.assertRaises(VerificationError):
            verify(self.path, self.evidence, other)
        self.openssl(False, public=other)
        changed = self.root / "changed.json"
        changed.write_bytes(self.evidence.read_bytes() + b" ")
        with self.assertRaises(VerificationError):
            verify(self.path, changed, self.public)
        self.openssl(False, evidence=changed)

    def test_keyid_and_unknown_envelope_fields_do_not_confer_trust(self):
        self.envelope["signatures"][0]["keyid"] = "untrusted:changed-hint"
        self.envelope["signatures"][0]["futureField"] = "ignored"
        self.envelope["publicKey"] = "https://example.org/do-not-fetch.pem"
        self.save()
        verify(self.path, self.evidence, self.public)
        self.openssl()

    def test_urlsafe_unpadded_encoding_and_additional_signatures(self):
        for target, field in ((self.envelope, "payload"), (self.envelope["signatures"][0], "sig")):
            target[field] = base64.urlsafe_b64encode(base64.b64decode(target[field])).decode().rstrip("=")
        self.envelope["signatures"].insert(0, {"sig": base64.b64encode(b"x" * 64).decode()})
        self.save()
        verify(self.path, self.evidence, self.public)
        self.openssl()

    def test_authenticated_type_and_predicate_bindings_are_required(self):
        original = copy.deepcopy(self.envelope)
        for transform, media in [(lambda s: None, "application/json"),
                                 (lambda s: s.update(predicateType="https://example.org/wrong"), MEDIA_TYPE),
                                 (lambda s: s["predicate"].update(evidence_schema="wrong.json"), MEDIA_TYPE),
                                 (lambda s: s["predicate"]["evidence"]["cases"][0].update(spent=True), MEDIA_TYPE)]:
            self.envelope = copy.deepcopy(original)
            self.resign(transform, media)
            with self.assertRaises(ValueError):
                verify(self.path, self.evidence, self.public)
            self.openssl(False)

    def test_malformed_encodings_duplicate_keys_and_empty_signatures_fail(self):
        for raw in (b'{"payload":"x","payload":"y"}',
                    json.dumps({**self.envelope, "signatures": []}).encode(),
                    json.dumps({**self.envelope, "payload": "invalid!"}).encode()):
            self.path.write_bytes(raw)
            with self.assertRaises(ValueError):
                verify(self.path, self.evidence, self.public)

    def test_wrong_key_algorithm_is_not_guessed(self):
        self.public.write_bytes(rsa.generate_private_key(public_exponent=65537, key_size=2048).public_key().public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
        self.save()
        with self.assertRaises(ValueError):
            verify(self.path, self.evidence, self.public)
        self.openssl(False)

    def test_invalid_source_and_existing_output_are_not_silently_signed(self):
        self.evidence.write_text('{"not": "execution evidence"}')
        with self.assertRaises(ValueError):
            seal(self.evidence, "execution", self.private)
        self.save()
        with self.assertRaises(FileExistsError):
            write_evidence(self.envelope, "dsse-envelope.schema.json", self.path)

    def test_demo_verifies_both_artifacts_and_removes_private_key(self):
        directory = self.root / "demo"
        run_demo(self.evidence, directory, os.environ.get("BRF_OPENSSL", "openssl"))
        self.assertEqual({p.name for p in directory.iterdir()},
                         {"evidence.json", "evidence.dsse.json", "inventory-links.json", "inventory-links.dsse.json", "demo-public.pem"})
        for name in ("evidence", "inventory-links"):
            result = verify(directory / (name + ".dsse.json"), directory / (name + ".json"), directory / "demo-public.pem")
            self.assertEqual(result["statement"]["predicate"]["signing_context"], "ephemeral_demo_key")

    def test_demo_failure_also_removes_private_key(self):
        directory = self.root / "failed-demo"
        with patch("tools.run_portability_demo.subprocess.run", side_effect=OSError("OpenSSL unavailable")):
            with self.assertRaises(OSError):
                run_demo(self.evidence, directory)
        self.assertFalse(list(directory.glob("private-key-*")))

    def test_cli_exit_codes_and_no_clobber(self):
        output = self.root / "cli-envelope.json"
        cli = [sys.executable, str(ROOT / "tools/dsse_evidence.py")]
        export = [*cli, "export", "--evidence", str(self.evidence), "--evidence-type", "execution",
                  "--private-key", str(self.private), "--output", str(output)]
        self.assertEqual(subprocess.run(export, capture_output=True, timeout=15).returncode, 0)
        original = output.read_bytes()
        self.assertEqual(subprocess.run(export, capture_output=True, timeout=15).returncode, 2)
        self.assertEqual(output.read_bytes(), original)
        check = [*cli, "verify", "--envelope", str(output), "--evidence", str(self.evidence), "--public-key", str(self.public)]
        self.assertEqual(subprocess.run(check, capture_output=True, timeout=15).returncode, 0)
        self.evidence.write_bytes(self.evidence.read_bytes() + b" ")
        self.assertEqual(subprocess.run(check, capture_output=True, timeout=15).returncode, 1)
        output.write_text('{"payload":"invalid!"}')
        self.assertEqual(subprocess.run(check, capture_output=True, timeout=15).returncode, 2)


if __name__ == "__main__":
    unittest.main()
