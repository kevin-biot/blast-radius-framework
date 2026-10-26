#!/usr/bin/env python3
"""Install a digest-pinned OPA binary under .tools; never install globally."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import tempfile
from pathlib import Path
from urllib.request import urlopen

VERSION = "1.21.4"
ASSETS = {
    ("Darwin", "arm64"): ("opa_darwin_arm64", "4c105208a9282f590385bccbe600875c011f0894ccf9431782dfe855e1f99aa6"),
    ("Darwin", "x86_64"): ("opa_darwin_amd64", "8802bd39bc14b58a705e6b3d4f4dd14f7f24ee657f0362c737338be243190c7e"),
    ("Linux", "x86_64"): ("opa_linux_amd64_static", "2ab571f367f293bb19523b76f92f1945bbf245003392c7f392903f95c2b9b630"),
    ("Linux", "aarch64"): ("opa_linux_arm64_static", "810aa96e44f1f852d044888cf830324e44eafd0f510345339011347ab4deaab1"),
}
TARGET = Path(__file__).resolve().parent.parent / ".tools/bin/opa"


def file_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    key = (platform.system(), platform.machine())
    if key not in ASSETS:
        raise SystemExit(f"Unsupported platform: {key}; install the pinned OPA version separately.")
    asset, digest = ASSETS[key]
    url = f"https://github.com/open-policy-agent/opa/releases/download/v{VERSION}/{asset}"
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    if TARGET.exists():
        if file_digest(TARGET) != digest:
            raise SystemExit("Existing local OPA does not match the pinned digest; refusing to replace it.")
    else:
        temp = None
        try:
            with tempfile.NamedTemporaryFile(dir=TARGET.parent, delete=False) as stream:
                temp = Path(stream.name)
                total = 0
                with urlopen(url, timeout=120) as response:
                    while chunk := response.read(1024 * 1024):
                        total += len(chunk)
                        if total > 150_000_000:
                            raise ValueError("OPA asset exceeds size limit")
                        stream.write(chunk)
            if file_digest(temp) != digest:
                raise ValueError("OPA download digest mismatch")
            temp.chmod(0o755)
            os.replace(temp, TARGET)
        finally:
            if temp is not None:
                temp.unlink(missing_ok=True)
    (TARGET.parent / "opa-manifest.json").write_text(json.dumps(
        {"version": VERSION, "asset": asset, "sha256": digest, "source": url}, indent=2) + "\n")
    print(f"Verified OPA {VERSION}: {TARGET}")


if __name__ == "__main__":
    main()
