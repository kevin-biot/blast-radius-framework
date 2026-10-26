import tempfile
import unittest
from pathlib import Path

from tools.validate_json_schema import (ROOT_DIR, load_json, make_validator,
                                       semantic_errors, structural_errors)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.schema = load_json(ROOT_DIR / "spec/component-card.schema.json")
        self.card = load_json(ROOT_DIR / "spec/examples/example-component-card-tool-legal-db.json")
        self.profile = load_json(ROOT_DIR / "spec/examples/example-profile-closed-world-br2.json")

    def test_bad_date_and_missing_type_specific_fields(self):
        self.card["last_reviewed_at"] = "2026-02-30"
        self.card["details"].pop("auth_model")
        errors = structural_errors(make_validator(self.schema), self.card)
        self.assertTrue(any("date" in err for err in errors))
        self.assertTrue(any("auth_model" in err for err in errors))

    def test_bad_schema_is_rejected(self):
        self.schema["type"] = "not-a-json-schema-type"
        with self.assertRaises(Exception):
            make_validator(self.schema)

    def test_delegation_requires_external_evidence_for_a_referenced_mandate(self):
        self.assertEqual(structural_errors(make_validator(self.schema), self.card), [])
        self.card["authority_context"]["mandate_source"]["status"] = "reference_provided"
        self.assertTrue(structural_errors(make_validator(self.schema), self.card))

    def test_revocation_claim_requires_time_and_evidence(self):
        self.card["authority_context"]["revocation_check"]["status"] = "active_at_check"
        self.assertTrue(structural_errors(make_validator(self.schema), self.card))

    def test_new_signed_profile_requires_explicit_payload_construction(self):
        schema = load_json(ROOT_DIR / "spec/br-profile.schema.json")
        self.profile["schema_version"] = "0.1.1"
        self.profile["signature"] = {"algorithm": "HMAC-SHA256", "signer_id": "test-only",
                                     "signature_value": "", "signed_payload_canonical_form": "JCS-RFC8785"}
        self.assertTrue(structural_errors(make_validator(schema), self.profile))
        self.profile["signature"].update(payload_profile="BRF-JCS-0.1.1", signed_at="2026-10-26T10:00:00Z")
        self.assertEqual(structural_errors(make_validator(schema), self.profile), [])

    def test_dangling_card_link_is_rejected(self):
        self.assertEqual(semantic_errors(self.card, {self.profile["profile_id"]: True}), [])
        self.assertTrue(semantic_errors(self.card, {}))

    def test_unknown_component_edge_is_rejected(self):
        self.profile["composition"]["edges"] = [{"from": "missing", "to": "citation-verifier", "interface_type": "typed"}]
        self.assertTrue(semantic_errors(self.profile))

    def test_legacy_floor_is_preserved(self):
        self.profile["components"][0]["worldview"] = "open-world"
        self.assertTrue(semantic_errors(self.profile))

    def test_mixed_json_paths_do_not_crash_error_sort(self):
        schema = {"$schema": self.schema["$schema"], "type": "object", "additionalProperties": {"type": "integer"}}
        self.assertEqual(len(structural_errors(make_validator(schema), {"a": [], "b": "bad"})), 2)

    def test_remote_reference_is_never_fetched(self):
        schema = {"$schema": self.schema["$schema"], "$ref": "https://example.invalid/schema.json"}
        with self.assertRaises(Exception):
            structural_errors(make_validator(schema), {})

    def test_duplicate_keys_and_non_json_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            for text in ('{"x": 1, "x": 2}', '{"x": NaN}', '{"x": 1e999}'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    load_json(path)


if __name__ == "__main__":
    unittest.main()
