import copy
import hashlib
import unittest

from tools.attestation_payload import (PAYLOAD_PROFILE, anchor_bytes, hmac_signature,
                                       signing_bytes, verify_hmac)


class AttestationTests(unittest.TestCase):
    def setUp(self):
        self.payload = {"profile_id": "test-only", "signature": {
            "algorithm": "HMAC-SHA256", "signer_id": "test-key", "signature_value": "",
            "payload_profile": PAYLOAD_PROFILE, "signed_payload_canonical_form": "JCS-RFC8785",
            "signed_at": "2026-10-26T10:00:00Z"}}
        self.key = b"public-test-key-never-use-in-production"

    def test_canonical_input_and_known_signature_vector(self):
        expected = b'{"profile_id":"test-only","signature":{"algorithm":"HMAC-SHA256","payload_profile":"BRF-JCS-0.1.1","signature_value":"","signed_at":"2026-10-26T10:00:00Z","signed_payload_canonical_form":"JCS-RFC8785","signer_id":"test-key"}}'
        self.assertEqual(signing_bytes(self.payload), expected)
        self.payload["signature"]["signature_value"] = hmac_signature(self.payload, self.key)
        self.assertEqual(self.payload["signature"]["signature_value"], "NwdGG129HWU65miMmLW/Q/M6aLvZHp/nR1xLZ7R37x8=")
        self.assertTrue(verify_hmac(self.payload, self.key))
        self.assertFalse(verify_hmac(self.payload, b"wrong-key"))

    def test_metadata_and_content_tampering_fail(self):
        self.payload["signature"]["signature_value"] = hmac_signature(self.payload, self.key)
        for field in ("signer_id", "signed_at"):
            changed = copy.deepcopy(self.payload)
            changed["signature"][field] += "tampered"
            self.assertFalse(verify_hmac(changed, self.key))
        self.payload["profile_id"] = "tampered"
        self.assertFalse(verify_hmac(self.payload, self.key))

    def test_anchor_is_excluded_but_signature_is_in_anchor_commitment(self):
        before = signing_bytes(self.payload)
        self.payload["anchor"] = {"anchor_commitment": "not-real"}
        self.assertEqual(before, signing_bytes(self.payload))
        first_hash = hashlib.sha256(anchor_bytes(self.payload)).digest()
        self.payload["signature"]["signature_value"] = hmac_signature(self.payload, self.key)
        self.assertNotEqual(first_hash, hashlib.sha256(anchor_bytes(self.payload)).digest())

    def test_ambiguous_legacy_payload_is_not_guessed(self):
        self.payload["signature"].pop("payload_profile")
        with self.assertRaises(ValueError):
            signing_bytes(self.payload)


if __name__ == "__main__":
    unittest.main()
