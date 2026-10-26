#!/usr/bin/env python3
"""Cache the ACS schemas used by the adapter from an immutable upstream commit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
COMMIT = "834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8"  # ACS release v0.1.4
BASE = "https://genai-security-project.github.io/agent-control-standard/schema/v0.1.0/"
RAW = f"https://raw.githubusercontent.com/GenAI-Security-Project/agent-control-standard/{COMMIT}/specification/v0.1.0/"
CACHE = ROOT / ".tools/acs-v0.1.4"


def references(value):
    if isinstance(value, dict):
        if "$ref" in value:
            yield value["$ref"]
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def main():
    pending = ["request-envelope.json", "response-envelope.json",
               "hooks/tool-call-request.json", "hooks/tool-call-result.json"]
    files = {}
    while pending:
        path = pending.pop()
        if path in files:
            continue
        uri = urljoin(BASE, path)
        if not uri.startswith(BASE) or ".." in PurePosixPath(path).parts:
            raise ValueError("schema reference escapes the pinned ACS source")
        with urlopen(RAW + path, timeout=20) as response:
            raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("upstream schema exceeds size limit")
        schema = json.loads(raw)
        if schema["$id"] != uri:
            raise ValueError(f"unexpected schema ID in {path}")
        target = CACHE / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        files[path] = hashlib.sha256(raw).hexdigest()
        for ref in references(schema):
            resolved = urljoin(uri, ref).split("#")[0]
            if not resolved.startswith(BASE):
                raise ValueError(f"external schema reference is not allowed: {resolved}")
            pending.append(resolved[len(BASE):])
    # Publish the manifest last; an interrupted download is not a complete cache.
    manifest = {"upstream_commit": COMMIT, "upstream_release": "v0.1.4",
                "schema_base": BASE, "files": files}
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Cached {len(files)} pinned ACS schemas in {CACHE}")


if __name__ == "__main__":
    main()
