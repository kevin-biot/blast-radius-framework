#!/usr/bin/env python3
"""Cache the complete pinned CycloneDX 1.7 JSON schema reference set."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

COMMIT = "349314a9d7671d7d2ca5b711a725f49a73979da6"
RELEASE = "1.7.2"
CACHE = Path(__file__).resolve().parent.parent / ".tools/cyclonedx-1.7.2"
FILES = ("bom-1.7.schema.json", "spdx.schema.json", "jsf-0.82.schema.json", "cryptography-defs.schema.json")


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = {"commit": COMMIT, "release": RELEASE, "spec_version": "1.7", "files": {}}
    for name in (*FILES, "LICENSE"):
        path = "schema/" + name if name != "LICENSE" else name
        url = f"https://raw.githubusercontent.com/CycloneDX/specification/{COMMIT}/{path}"
        with urlopen(url, timeout=30) as response:
            data = response.read(4_000_001)
        if len(data) > 4_000_000:
            raise ValueError("schema asset exceeds size limit")
        (CACHE / name).write_bytes(data)
        manifest["files"][name] = {"sha256": hashlib.sha256(data).hexdigest(), "source": url}
    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Cached CycloneDX spec 1.7 / schema release {RELEASE} at {COMMIT}: {CACHE}")


if __name__ == "__main__":
    main()
