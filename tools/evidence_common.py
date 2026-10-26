"""Shared evidence-file handling; no implicit signatures or runtime claims."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from .validate_json_schema import ROOT_DIR, load_json, make_validator, structural_errors
except ImportError:
    from validate_json_schema import ROOT_DIR, load_json, make_validator, structural_errors


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_evidence(bundle, schema_name, output, overwrite=False):
    errors = structural_errors(make_validator(load_json(ROOT_DIR / "spec" / schema_name)), bundle)
    if errors:
        raise ValueError("; ".join(errors))
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, delete=False) as stream:
            temp = Path(stream.name)
            json.dump(bundle, stream, indent=2, allow_nan=False)
            stream.write("\n")
        if overwrite:
            os.replace(temp, output)
        else:
            os.link(temp, output)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)
