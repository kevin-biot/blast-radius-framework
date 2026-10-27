#!/usr/bin/env python3
"""Separate stdlib/OpenSSL verifier for the bounded BRF DSSE evidence profile.

No imports from the signer or its Python crypto library. Checks cryptographic
integrity and subject/predicate binding, not full evidence-schema semantics.
"""
import argparse
import base64
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MEDIA = "application/vnd.in-toto+json"
PREDICATE = "https://github.com/kevin-biot/blast-radius-framework/blob/main/spec/predicates/evidence-v1.md"
SCHEMAS = {"acs_trace": "acs-trace-evidence.schema.json", "evaluation": "evaluation-evidence.schema.json",
           "execution": "execution-evidence.schema.json", "inventory_links": "inventory-links.schema.json"}


def read(path, limit):
    with Path(path).open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("input exceeds verifier limit")
    return data


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject(_value):
    raise ValueError("non-JSON numeric value")


def finite(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("non-finite JSON number")
    return number


def parse(raw):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=reject, parse_float=finite)


def decode(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9+/_-]*={0,2}", value):
        raise ValueError("malformed base64")
    return base64.b64decode(value + "=" * (-len(value) % 4), altchars=b"-_", validate=True)


def verify(envelope_path, evidence_path, public_key_path, openssl="openssl"):
    executable = shutil.which(openssl)
    if not executable:
        raise ValueError("OpenSSL 3+ is required; select it with --openssl")
    version = subprocess.run([executable, "version"], capture_output=True, text=True, check=True, timeout=10).stdout
    match = re.match(r"OpenSSL (\d+)\.", version)
    if not match or int(match[1]) < 3:
        raise ValueError("OpenSSL 3+ required (LibreSSL is not supported)")
    envelope = parse(read(envelope_path, 40_000_000))
    kind, signatures = envelope["payloadType"], envelope["signatures"]
    if not isinstance(kind, str) or not isinstance(signatures, list) or not 1 <= len(signatures) <= 32:
        raise ValueError("malformed DSSE envelope")
    if any(not isinstance(item, dict) or not isinstance(item.get("keyid", ""), str) for item in signatures):
        raise ValueError("malformed DSSE signature entry")
    body = decode(envelope["payload"])
    signature_bytes = [decode(item["sig"]) for item in signatures]
    kind_bytes = kind.encode("utf-8")
    authenticated = b"DSSEv1 " + str(len(kind_bytes)).encode("ascii") + b" " + kind_bytes
    authenticated += b" " + str(len(body)).encode("ascii") + b" " + body
    # Snapshot the caller-selected key; never follow a payload key, URL or keyid.
    key = read(public_key_path, 16_384)
    with tempfile.TemporaryDirectory(prefix="brf-openssl-") as tmp:
        directory = Path(tmp)
        trusted = directory / "trusted.pem"
        trusted.write_bytes(key)
        der = subprocess.run([executable, "pkey", "-pubin", "-in", str(trusted), "-pubout", "-outform", "DER"],
                             capture_output=True, check=True, timeout=10).stdout
        if len(der) != 44 or der[:12] != bytes.fromhex("302a300506032b6570032100"):
            raise ValueError("only an Ed25519 SubjectPublicKeyInfo is supported")
        message = directory / "pae.bin"
        signature = directory / "signature.bin"
        message.write_bytes(authenticated)
        accepted = False
        for value in signature_bytes:
            signature.write_bytes(value)
            result = subprocess.run([executable, "pkeyutl", "-verify", "-pubin", "-inkey", str(trusted),
                "-rawin", "-in", str(message), "-sigfile", str(signature)], capture_output=True, timeout=15)
            if result.returncode == 0:
                accepted = True
                break
    if not accepted:
        raise ValueError("no signature verifies against the supplied public key")
    if kind != MEDIA:
        raise ValueError("unsupported authenticated media type")
    statement = parse(body)
    if statement.get("_type") != "https://in-toto.io/Statement/v1" or statement.get("predicateType") != PREDICATE:
        raise ValueError("unsupported statement or predicate type")
    subjects = statement["subject"]
    if not isinstance(subjects, list) or len(subjects) != 1:
        raise ValueError("single-subject profile required")
    evidence = read(evidence_path, 8_000_000)
    if subjects[0]["digest"]["sha256"] != hashlib.sha256(evidence).hexdigest():
        raise ValueError("subject digest mismatch")
    predicate = statement["predicate"]
    if (predicate["evidence_schema"] != SCHEMAS[predicate["evidence_type"]]
        or predicate["verification_scope"] != "signature_and_subject_integrity_only"
        or predicate["signing_context"] not in {"caller_supplied_key", "ephemeral_demo_key"}
        or json.dumps(predicate["evidence"], sort_keys=True, allow_nan=False) != json.dumps(parse(evidence), sort_keys=True, allow_nan=False)):
        raise ValueError("evidence predicate/subject binding mismatch")
    return hashlib.sha256(der).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--envelope", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--public-key", type=Path, required=True)
    parser.add_argument("--openssl", default="openssl")
    args = parser.parse_args()
    try:
        fingerprint = verify(args.envelope, args.evidence, args.public_key, args.openssl)
        print(f"VERIFIED with OpenSSL: signature and subject binding; trusted key SHA-256 {fingerprint}; evidence truth/authority NOT verified")
        return 0
    except Exception as exc:
        print(f"NOT VERIFIED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
