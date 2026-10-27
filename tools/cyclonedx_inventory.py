#!/usr/bin/env python3
"""Validate a pinned CycloneDX 1.7 BOM and explicitly link BRF cards offline."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from .evidence_common import digest, now, write_evidence
    from .fetch_cyclonedx_schemas import CACHE, COMMIT, FILES
    from .validate_json_schema import ROOT_DIR, decode_json, load_json, make_validator, offline_resource, semantic_errors, structural_errors
except ImportError:
    from evidence_common import digest, now, write_evidence
    from fetch_cyclonedx_schemas import CACHE, COMMIT, FILES
    from validate_json_schema import ROOT_DIR, decode_json, load_json, make_validator, offline_resource, semantic_errors, structural_errors

from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry, Resource


def cyclonedx_validator(cache=CACHE):
    manifest = load_json(cache / "manifest.json")
    if manifest.get("commit") != COMMIT or manifest.get("spec_version") != "1.7":
        raise ValueError("wrong CycloneDX schema cache pin")
    resources, schemas = [], {}
    for name in FILES:
        raw = (cache / name).read_bytes()
        if digest(raw) != manifest["files"][name]["sha256"]:
            raise ValueError(f"CycloneDX schema cache digest mismatch: {name}")
        schema = decode_json(raw.decode("utf-8"))
        if schema.get("$schema") != "http://json-schema.org/draft-07/schema#":
            raise ValueError("unexpected upstream schema dialect")
        expected_id = "http://cyclonedx.org/schema/" + name
        if schema.get("$id") != expected_id:
            raise ValueError("unexpected upstream schema identifier")
        Draft7Validator.check_schema(schema)
        resource = Resource.from_contents(schema)
        resources.extend([(expected_id, resource), (expected_id.replace("http:", "https:"), resource)])
        schemas[name] = schema
    registry = Registry(retrieve=offline_resource).with_resources(resources)
    return Draft7Validator(schemas["bom-1.7.schema.json"], registry=registry, format_checker=FormatChecker())


def records(bom):
    def descend(items, kind):
        for item in items:
            yield kind, item
            yield from descend(item.get("components" if kind == "component" else "services", []), kind)
    root = bom.get("metadata", {}).get("component")
    if root:
        yield from descend([root], "component")
    yield from descend(bom.get("components", []), "component")
    yield from descend(bom.get("services", []), "service")


def all_refs(value):
    if isinstance(value, dict):
        if "bom-ref" in value:
            yield value["bom-ref"]
        for child in value.values():
            yield from all_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_refs(child)


def build_links(bom_path, mapping_path, card_paths=(), profile_paths=()):
    snapshots, sources = {}, []

    def read(path, role):
        path = Path(path).resolve()
        with path.open("rb") as stream:
            raw = stream.read(8_000_001)
        if len(raw) > 8_000_000:
            raise ValueError("inventory input exceeds size limit")
        if path in snapshots:
            raise ValueError("same source file supplied more than once")
        snapshots[path] = raw
        sources.append({"role": role, "name": path.name, "sha256": digest(raw)})
        return decode_json(raw.decode("utf-8")), digest(raw)

    def validate(value, schema_name):
        errors = structural_errors(make_validator(load_json(ROOT_DIR / "spec" / schema_name)), value)
        if errors:
            raise ValueError("; ".join(errors))

    bom, _ = read(bom_path, "bom")
    if bom.get("bomFormat") != "CycloneDX" or bom.get("specVersion") != "1.7":
        raise ValueError("only CycloneDX JSON specVersion 1.7 is supported; no silent conversion")
    errors = structural_errors(cyclonedx_validator(), bom)
    if errors:
        raise ValueError("; ".join(errors))
    refs = list(all_refs(bom))
    if len(refs) != len(set(refs)):
        raise ValueError("duplicate bom-ref anywhere in the BOM")
    if any(ref.startswith("urn:cdx:") for ref in refs):
        raise ValueError("this bridge requires local bom-ref values distinct from BOM-Link URNs")
    entries = list(records(bom))
    targets = {item["bom-ref"]: item for _, item in entries if "bom-ref" in item}
    dependencies, external, seen_dependencies = [], set(), set()
    for dependency in bom.get("dependencies", []):
        if dependency["ref"] in seen_dependencies:
            raise ValueError("duplicate dependency declaration")
        seen_dependencies.add(dependency["ref"])
        row = {"ref": dependency["ref"], "depends_on": dependency.get("dependsOn", []), "provides": dependency.get("provides", [])}
        for ref in [row["ref"], *row["depends_on"], *row["provides"]]:
            if ref not in targets:
                if re.fullmatch(r"urn:cdx:[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}/[1-9][0-9]*(?:#.+)?", ref):
                    external.add(ref)
                else:
                    raise ValueError(f"dangling local inventory dependency: {ref}")
        dependencies.append(row)
    profiles = {}
    for path in profile_paths:
        profile, sha = read(path, "profile")
        validate(profile, "br-profile.schema.json")
        errors = semantic_errors(profile)
        if errors:
            raise ValueError("; ".join(errors))
        profile_id = profile["profile_id"]
        if profile_id in profiles:
            raise ValueError("duplicate profile_id")
        profiles[profile_id] = sha
    cards = {}
    for path in card_paths:
        card, sha = read(path, "card")
        validate(card, "component-card.schema.json")
        errors = semantic_errors(card, profiles)
        if errors:
            raise ValueError("; ".join(errors))
        if card["card_id"] in cards:
            raise ValueError("duplicate card_id")
        cards[card["card_id"]] = (card, sha)
    mapping, _ = read(mapping_path, "mapping")
    validate(mapping, "inventory-map.schema.json")
    links, used = {}, set()
    for link in mapping["links"]:
        ref, card_id = link["bom_ref"], link["card_id"]
        if ref not in targets or card_id not in cards:
            raise ValueError("mapping contains an unknown local bom-ref or card_id")
        card, sha = cards[card_id]
        version = targets[ref].get("version")
        if not isinstance(version, str) or not version.strip() or version != card["version"]:
            raise ValueError("explicit card link requires an exact, present component/service version")
        links.setdefault(ref, []).append({"card_id": card_id, "card_sha256": sha,
            "profile_bindings": [{"profile_id": profile_id, "sha256": profiles[profile_id]} for profile_id in card["related_profile_ids"]]})
        used.add(card_id)
    inventory = []
    for kind, item in entries:
        ref = item.get("bom-ref")
        inventory.append({"kind": kind, "bom_ref": ref, "name": item["name"], "version": item.get("version"),
            "purl": item.get("purl"), "link_status": "not_addressable" if ref is None else "declared_unverified" if ref in links else "unmapped",
            "dependency_declaration": "not_addressable" if ref is None else "listed" if ref in seen_dependencies else "not_listed",
            "card_links": links.get(ref, [])})
    if any(path.read_bytes() != raw for path, raw in snapshots.items()):
        raise ValueError("source changed during inventory linking")
    return {"schema_version": "0.1.0", "generated_at": now(), "source_format": "CycloneDX-JSON", "spec_version": "1.7",
        "schema_commit": COMMIT, "sources": sources, "inventory": inventory,
        "dependency_graph_declaration": "supplied" if "dependencies" in bom else "not_supplied", "declared_dependencies": dependencies,
        "external_refs_not_resolved": sorted(external), "unused_card_ids": sorted(set(cards) - used),
        "runtime_reach": "not_established", "authority": "not_established",
        "limits": ["Inventory and explicit card links are unverified declarations, not authenticated identity or deployed revision proof.",
                   "Dependency/provides declarations are not BRF composition edges, runtime reachability, permissions or corporate authority.",
                   "Unmapped/unaddressable entries remain visible; missing dependency declarations are unknown, not dependency-free.",
                   "External BOM-Links are not fetched. CycloneDX signatures and inventory completeness are not verified."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bom", type=Path)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--card", type=Path, action="append", default=[])
    parser.add_argument("--profile", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_links(args.bom, args.mapping, args.card, args.profile)
        write_evidence(result, "inventory-links.schema.json", args.output)
        linked = sum(row["link_status"] == "declared_unverified" for row in result["inventory"])
        print(f"VALIDATED: {len(result['inventory'])} inventory entries, {linked} explicitly linked; runtime reach/authority NOT established")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}; fetch schemas with python3 tools/fetch_cyclonedx_schemas.py", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
