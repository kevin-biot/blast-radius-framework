#!/usr/bin/env python3
"""Offline structural validation and explicit BRF reference/semantic checks."""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / ".tools" / "jsonschema-lib"))

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
    from referencing import Registry
    from referencing.exceptions import NoSuchResource
except ImportError as exc:
    raise SystemExit("Run `bash tools/install-jsonschema-local.sh` first.") from exc


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-JSON numeric constant: {value}")


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"non-finite numeric value: {value}")
    return number


def decode_json(text):
    return json.loads(text,
                      object_pairs_hook=unique_object, parse_constant=reject_constant, parse_float=finite_float)


def load_json(path: Path):
    return decode_json(path.read_text(encoding="utf-8"))


def offline_resource(uri):
    raise NoSuchResource(ref=uri)


def make_validator(schema, registry=None):
    if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("schema must declare JSON Schema draft 2020-12")
    Draft202012Validator.check_schema(schema)
    checker = FormatChecker()
    if not {"date", "date-time", "uuid", "uri"} <= checker.checkers.keys():
        raise ValueError("format dependencies missing; rerun the local installer")
    return Draft202012Validator(schema, format_checker=checker,
                               registry=registry if registry is not None else Registry(retrieve=offline_resource))


def structural_errors(validator, instance):
    errors = []
    for error in validator.iter_errors(instance):
        path = "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in error.absolute_path)
        errors.append(f"{path}: {error.message}")
    return sorted(errors)


def semantic_errors(instance, profiles=None):
    errors = []
    if not isinstance(instance, dict):
        return errors
    if "profile_id" in instance:
        components = instance.get("components", [])
        ids = [component["component_id"] for component in components]
        if len(set(ids)) != len(ids):
            errors.append("components: duplicate component_id")
        for edge in instance.get("composition", {}).get("edges", []):
            for end in ("from", "to"):
                if edge[end] not in ids:
                    errors.append(f"composition.edges: unknown component {edge[end]!r}")
        if any(c.get("worldview") == "open-world" for c in components):
            if instance["aggregation"]["ordinal_class"] in {"BR-1", "BR-2", "BR-3"}:
                errors.append("aggregation: violates the published v0.5 open-world BR-4 floor")
        expiry = instance.get("attestation_expiry")
        if expiry and datetime.fromisoformat(expiry.replace("Z", "+00:00")) <= datetime.fromisoformat(instance["attestation_date"].replace("Z", "+00:00")):
            errors.append("attestation_expiry: must follow attestation_date")
        for invariant, claim in instance.get("invariants", {}).items():
            for test in claim.get("conformance_test_results", []):
                if not test["test_id"].startswith(invariant + "-T"):
                    errors.append(f"{invariant}: mismatched test ID {test['test_id']}")
    if "card_type" in instance and profiles is not None:
        for profile_id in instance["related_profile_ids"]:
            if profile_id not in profiles:
                errors.append(f"related_profile_ids: unknown profile {profile_id!r}")
    return errors


def validate_instance(schema_path, instance_path, profiles=None):
    validator = make_validator(load_json(schema_path))
    instance = load_json(instance_path)
    errors = structural_errors(validator, instance)
    if not errors:
        errors = semantic_errors(instance, profiles)
    print(f"{'FAIL' if errors else 'OK  '} {instance_path}")
    for error in errors:
        print(f"  - {error}")
    if not errors and isinstance(instance, dict) and "card_type" in instance and profiles is None:
        print("  NOTE: profile references not checked; supply --profile or --check-repository")
    return int(bool(errors))


def repository_files():
    profiles = sorted((ROOT_DIR / "spec/examples").glob("example-profile-*.json"))
    profiles += sorted((ROOT_DIR / "reports").rglob("*.json"))
    cards = sorted((ROOT_DIR / "spec/examples").glob("example-component-card-*.json"))
    return profiles, cards


def profile_catalog(paths):
    catalog = {}
    for path in paths:
        instance = load_json(path)
        profile_id = instance["profile_id"]
        if profile_id in catalog:
            raise ValueError(f"duplicate profile_id: {profile_id}")
        catalog[profile_id] = path
    return catalog


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", nargs="?")
    parser.add_argument("instances", nargs="*")
    parser.add_argument("--profile", action="append", default=[], type=Path,
                        help="Profile file to resolve component-card links; repeat as needed")
    parser.add_argument("--check-repository", action="store_true")
    args = parser.parse_args(argv)
    if args.check_repository and (args.schema or args.instances or args.profile):
        parser.error("--check-repository cannot be combined with individual files")
    if not args.check_repository and (not args.schema or not args.instances):
        parser.error("supply SCHEMA INSTANCE... or --check-repository")
    try:
        failed = 0
        if args.check_repository:
            profiles, cards = repository_files()
            catalog = profile_catalog(profiles)
            for path in profiles:
                failed |= validate_instance(ROOT_DIR / "spec/br-profile.schema.json", path)
            for path in cards:
                failed |= validate_instance(ROOT_DIR / "spec/component-card.schema.json", path, catalog)
        else:
            catalog = profile_catalog(args.profile) if args.profile else None
            for path in args.instances:
                failed |= validate_instance(Path(args.schema), Path(path), catalog)
        print("Checked structure, supported formats and declared semantic/reference rules; signatures, anchors and BR arithmetic are not verified.")
        return failed
    except (OSError, ValueError, SchemaError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR: validation could not complete: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
