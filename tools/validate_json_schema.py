#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
LOCAL_LIB = ROOT_DIR / ".tools" / "jsonschema-lib"
if LOCAL_LIB.exists():
    sys.path.insert(0, str(LOCAL_LIB))

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "jsonschema is not installed locally. Run `./tools/install-jsonschema-local.sh` first."
    ) from exc


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_instance(schema_path: Path, instance_path: Path) -> int:
    schema = load_json(schema_path)
    instance = load_json(instance_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path))

    if not errors:
        print(f"OK  {instance_path} against {schema_path}")
        return 0

    print(f"FAIL {instance_path} against {schema_path}")
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        print(f"  - {location}: {error.message}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate one or more JSON instances against a JSON Schema."
    )
    parser.add_argument("schema", help="Path to the schema JSON file")
    parser.add_argument("instances", nargs="+", help="Path(s) to JSON instance file(s)")
    args = parser.parse_args()

    schema_path = Path(args.schema).resolve()
    instance_paths = [Path(item).resolve() for item in args.instances]

    if not schema_path.exists():
        raise SystemExit(f"Schema not found: {schema_path}")

    exit_code = 0
    for instance_path in instance_paths:
        if not instance_path.exists():
            print(f"FAIL {instance_path} against {schema_path}")
            print("  - <root>: instance file not found")
            exit_code = 1
            continue
        exit_code |= validate_instance(schema_path, instance_path)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
