"""Pinned full-schema validation and explicit inventory-link integrity tests."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.cyclonedx_inventory import build_links, cyclonedx_validator
from tools.evidence_common import digest, write_evidence
from tools.fetch_cyclonedx_schemas import CACHE
from tools.validate_json_schema import ROOT_DIR, load_json, structural_errors

FIXTURE = ROOT_DIR / "examples/cyclonedx/bom.json"
MAPPING = ROOT_DIR / "examples/cyclonedx/card-map.json"
CARD = ROOT_DIR / "spec/examples/example-component-card-tool-legal-db.json"
PROFILE = ROOT_DIR / "spec/examples/example-profile-closed-world-br2.json"


class CycloneDxInventoryTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.root = Path(self.workspace.name)
        self.addCleanup(self.workspace.cleanup)

    def run_modified(self, bom_change=lambda _b: None, map_change=lambda _m: None, card_change=lambda _c: None, profiles=True):
        bom, mapping, card = load_json(FIXTURE), load_json(MAPPING), load_json(CARD)
        bom_change(bom)
        map_change(mapping)
        card_change(card)
        paths = [self.root / name for name in ("bom.json", "map.json", "card.json")]
        for path, value in zip(paths, (bom, mapping, card)):
            path.write_text(json.dumps(value))
        return build_links(paths[0], paths[1], [paths[2]], [PROFILE] if profiles else [])

    def test_fixture_preserves_gaps_and_binds_cards_and_profiles(self):
        result = build_links(FIXTURE, MAPPING, [CARD], [PROFILE])
        self.assertEqual(len(result["inventory"]), 4)
        self.assertEqual([x["link_status"] for x in result["inventory"]].count("unmapped"), 2)
        self.assertEqual([x["link_status"] for x in result["inventory"]].count("not_addressable"), 1)
        linked = next(x for x in result["inventory"] if x["bom_ref"] == "legal-db")
        self.assertEqual(linked["card_links"][0]["card_sha256"], digest(CARD.read_bytes()))
        self.assertEqual(linked["card_links"][0]["profile_bindings"][0]["sha256"], digest(PROFILE.read_bytes()))
        self.assertEqual(result["runtime_reach"], "not_established")
        self.assertEqual(result["authority"], "not_established")
        write_evidence(result, "inventory-links.schema.json", self.root / "links.json")

    def test_full_schema_checks_spdx_not_only_top_level_fields(self):
        with self.assertRaises(ValueError):
            self.run_modified(lambda b: b["components"][0]["licenses"][0]["license"].update(id="not-an-SPDX-license"))
        with self.assertRaises(ValueError):
            self.run_modified(lambda b: b["services"][0].update(endpoints=[True]))

    def test_unsupported_bom_version_is_not_silently_converted(self):
        with self.assertRaises(ValueError):
            self.run_modified(lambda b: b.update(specVersion="1.6"))

    def test_duplicate_and_dangling_references_are_rejected(self):
        with self.assertRaises(ValueError):
            self.run_modified(lambda b: b["components"][0].update({"bom-ref": "legal-db"}))
        with self.assertRaises(ValueError):
            self.run_modified(lambda b: b["dependencies"][0]["dependsOn"].append("missing"))
        with self.assertRaises(ValueError):
            self.run_modified(lambda b: b["dependencies"].append({"ref": "parser"}))

    def test_external_bom_links_are_reported_without_fetching(self):
        ref = "urn:cdx:5a7344f9-790f-453d-834a-c794b5f964a6/1#external"
        with patch("urllib.request.urlopen", side_effect=AssertionError("must stay offline")) as network:
            result = self.run_modified(lambda b: b["dependencies"][0]["dependsOn"].append(ref))
            network.assert_not_called()
        self.assertEqual(result["external_refs_not_resolved"], [ref])

    def test_missing_dependencies_are_not_replaced_by_an_empty_graph(self):
        result = self.run_modified(lambda b: b.pop("dependencies"))
        self.assertEqual(result["declared_dependencies"], [])
        self.assertEqual(result["dependency_graph_declaration"], "not_supplied")
        self.assertTrue(all(x["dependency_declaration"] != "listed" for x in result["inventory"]))
        self.assertTrue(any("unknown" in limit for limit in result["limits"]))
        self.assertEqual(len(result["inventory"]), 4)

    def test_unknown_or_duplicate_explicit_mappings_are_errors(self):
        for change in (lambda m: m["links"][0].update(bom_ref="missing"),
                       lambda m: m["links"][0].update(card_id="missing"),
                       lambda m: m["links"].append(copy.deepcopy(m["links"][0]))):
            with self.assertRaises(ValueError):
                self.run_modified(map_change=change)

    def test_version_mismatch_and_missing_versions_are_errors(self):
        for change in (lambda b: b["services"][0].update(version="2.0"), lambda b: b["services"][0].pop("version")):
            with self.assertRaises(ValueError):
                self.run_modified(bom_change=change)

    def test_invalid_cards_and_unresolved_profiles_are_errors(self):
        with self.assertRaises(ValueError):
            self.run_modified(card_change=lambda c: c["details"].pop("auth_model"))
        with self.assertRaises(ValueError):
            self.run_modified(profiles=False)
        with self.assertRaises(ValueError):
            build_links(FIXTURE, MAPPING, [CARD, CARD], [PROFILE])

    def test_inventory_only_mode_does_not_guess_a_matching_name(self):
        result = self.run_modified(map_change=lambda m: m.update(links=[]))
        self.assertFalse(any(row["card_links"] for row in result["inventory"]))
        self.assertEqual(result["unused_card_ids"], ["tool-legal-citation-db-v1"])

    def test_changed_cache_and_remote_schema_refs_fail_offline(self):
        cache = self.root / "cache"
        shutil.copytree(CACHE, cache)
        path = cache / "bom-1.7.schema.json"
        schema = load_json(path)
        schema["allOf"] = [{"$ref": "https://example.org/not-allowed.schema.json"}]
        path.write_text(json.dumps(schema))
        with self.assertRaises(ValueError):
            cyclonedx_validator(cache)
        manifest = load_json(cache / "manifest.json")
        manifest["files"][path.name]["sha256"] = digest(path.read_bytes())
        (cache / "manifest.json").write_text(json.dumps(manifest))
        with patch("urllib.request.urlopen", side_effect=AssertionError("no remote schema lookup")) as network:
            validator = cyclonedx_validator(cache)
            with self.assertRaises(Exception):
                structural_errors(validator, load_json(FIXTURE))
            network.assert_not_called()

    def test_duplicate_json_and_no_clobber_output(self):
        bom = self.root / "duplicate.json"
        bom.write_text('{"bomFormat":"CycloneDX","bomFormat":"CycloneDX"}')
        with self.assertRaises(ValueError):
            build_links(bom, MAPPING, [CARD], [PROFILE])
        output = self.root / "output.json"
        result = build_links(FIXTURE, MAPPING, [CARD], [PROFILE])
        write_evidence(result, "inventory-links.schema.json", output)
        with self.assertRaises(FileExistsError):
            write_evidence(result, "inventory-links.schema.json", output)


if __name__ == "__main__":
    unittest.main()
