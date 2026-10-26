#!/usr/bin/env python3
"""Cache immutable ACS trace mapping and upstream sample; no code is executed."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

try:
    from .fetch_acs_schemas import COMMIT
except ImportError:
    from fetch_acs_schemas import COMMIT

CACHE = Path(__file__).resolve().parent.parent / ".tools/acs-trace-v0.1.4"
FILES = {
    "otel-mapping.json": "specification/v0.1.0/trace/otel-mapping.json",
    "sample.jsonl": "reference-implementations/agt/samples/trace/acs-trace-sample.jsonl",
    "LICENSE": "LICENSE",
}


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = {"upstream_commit": COMMIT, "files": {}}
    for name, path in FILES.items():
        url = f"https://raw.githubusercontent.com/GenAI-Security-Project/agent-control-standard/{COMMIT}/{path}"
        with urlopen(url, timeout=30) as response:
            raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("trace asset exceeds size limit")
        (CACHE / name).write_bytes(raw)
        manifest["files"][name] = {"sha256": hashlib.sha256(raw).hexdigest(), "source": url}
    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Cached pinned ACS trace mapping and synthetic upstream sample: {CACHE}")


if __name__ == "__main__":
    main()
