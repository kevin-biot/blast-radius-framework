#!/usr/bin/env python3
"""Export fixture evidence with an ephemeral demo key; verify via two paths."""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from .cyclonedx_inventory import build_links
    from .dsse_evidence import crypto, read_limited, seal, verify
    from .evidence_common import write_evidence
    from .validate_json_schema import ROOT_DIR
except ImportError:
    from cyclonedx_inventory import build_links
    from dsse_evidence import crypto, read_limited, seal, verify
    from evidence_common import write_evidence
    from validate_json_schema import ROOT_DIR


def new_file(path, data):
    with os.fdopen(os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600), "wb") as stream:
        stream.write(data)


def run(evidence, directory, openssl="openssl"):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, mode=0o700, exist_ok=False)
    serialization, private_type, *_ = crypto()
    key = private_type.generate()
    public = directory / "demo-public.pem"
    new_file(public, key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    subject = directory / "evidence.json"
    new_file(subject, read_limited(evidence))
    inventory = build_links(ROOT_DIR / "examples/cyclonedx/bom.json", ROOT_DIR / "examples/cyclonedx/card-map.json",
                            [ROOT_DIR / "spec/examples/example-component-card-tool-legal-db.json"],
                            [ROOT_DIR / "spec/examples/example-profile-closed-world-br2.json"])
    write_evidence(inventory, "inventory-links.schema.json", directory / "inventory-links.json")
    with tempfile.TemporaryDirectory(prefix="private-key-", dir=directory) as private_dir:
        private = Path(private_dir) / "key.pem"
        new_file(private, key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        for name, kind in (("evidence", "execution"), ("inventory-links", "inventory_links")):
            artifact, envelope = directory / (name + ".json"), directory / (name + ".dsse.json")
            write_evidence(seal(artifact, kind, private, signing_context="ephemeral_demo_key"), "dsse-envelope.schema.json", envelope)
            verify(envelope, artifact, public)
            subprocess.run([sys.executable, "-I", str(ROOT_DIR / "tools/verify_dsse_openssl.py"),
                "--envelope", str(envelope), "--evidence", str(artifact), "--public-key", str(public),
                "--openssl", openssl], check=True, timeout=30)
    print("Two envelopes verified via Python and separate OpenSSL path; ephemeral demo private key removed. No organisational identity/authority is attested.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True, help="local fixture execution-evidence bundle")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--openssl", default=os.environ.get("BRF_OPENSSL", "openssl"))
    args = parser.parse_args()
    try:
        run(args.evidence, args.run_dir, args.openssl)
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
