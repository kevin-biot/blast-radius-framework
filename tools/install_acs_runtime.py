#!/usr/bin/env python3
"""Install a pinned, isolated upstream Guardian and Bun under .tools."""
from __future__ import annotations

import hashlib
import io
import os
import platform
import subprocess
import zipfile
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
COMMIT = "834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8"
BUN_VERSION = "1.3.11"
ASSETS = {
    ("Darwin", "arm64"): ("bun-darwin-aarch64", "6f5a3467ed9caec4795bf78cd476507d9f870c7d57b86c945fcb338126772ffc"),
    ("Linux", "x86_64"): ("bun-linux-x64", "8611ba935af886f05a6f38740a15160326c15e5d5d07adef966130b4493607ed"),
}
BUN = ROOT / ".tools/bin/bun"
CHECKOUT = ROOT / ".tools/acs-runtime"
AGT = CHECKOUT / "reference-implementations/agt"


def run(*args, cwd=ROOT, **kwargs):
    return subprocess.run(args, cwd=cwd, check=True, text=True, **kwargs)


def main():
    key = (platform.system(), platform.machine())
    if key not in ASSETS:
        raise SystemExit(f"Unsupported platform for pinned Bun: {key}")
    asset, digest = ASSETS[key]
    # A separately retained binary digest detects local replacement on later runs.
    manifest = BUN.with_name("bun.sha256")
    if BUN.exists():
        if not manifest.exists() or hashlib.sha256(BUN.read_bytes()).hexdigest() != manifest.read_text().strip():
            raise SystemExit("Existing Bun has no matching local installation digest")
        if run(str(BUN), "--version", capture_output=True).stdout.strip() != BUN_VERSION:
            raise SystemExit("Existing Bun version differs from the pin")
    else:
        url = f"https://github.com/oven-sh/bun/releases/download/bun-v{BUN_VERSION}/{asset}.zip"
        with urlopen(url, timeout=120) as response:
            data = response.read(100_000_001)
        if len(data) > 100_000_000 or hashlib.sha256(data).hexdigest() != digest:
            raise SystemExit("Bun archive size/digest mismatch")
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            binary = archive.read(f"{asset}/bun")
        BUN.parent.mkdir(parents=True, exist_ok=True)
        with BUN.open("xb") as output:
            output.write(binary)
        BUN.chmod(0o755)
        manifest.write_text(hashlib.sha256(binary).hexdigest() + "\n")
    if not CHECKOUT.exists():
        run("git", "init", str(CHECKOUT))
        run("git", "remote", "add", "origin", "https://github.com/GenAI-Security-Project/agent-control-standard.git", cwd=CHECKOUT)
        run("git", "fetch", "--depth=1", "origin", COMMIT, cwd=CHECKOUT)
        run("git", "checkout", "--detach", "FETCH_HEAD", cwd=CHECKOUT)
    if run("git", "rev-parse", "HEAD", cwd=CHECKOUT, capture_output=True).stdout.strip() != COMMIT:
        raise SystemExit("Existing ACS checkout differs from the pin; refusing to reset it")
    if run("git", "status", "--porcelain", "--untracked-files=no", cwd=CHECKOUT, capture_output=True).stdout.strip():
        raise SystemExit("ACS tracked files have local changes; refusing installation")
    env = dict(os.environ, BUN_INSTALL_CACHE_DIR=str(ROOT / ".tools/bun-cache"))
    run(str(BUN), "install", "--frozen-lockfile", "--ignore-scripts", cwd=AGT, env=env)
    print(f"Installed Bun {BUN_VERSION} and ACS {COMMIT}; dependency lifecycle scripts disabled")


if __name__ == "__main__":
    main()
