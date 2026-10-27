#!/usr/bin/env python3
"""Optional Ed25519 DSSE packaging; never infer trust from an embedded key ID."""
from __future__ import annotations

import argparse
import base64
import re
import sys
from pathlib import Path

try:
    from .evidence_common import digest, now, write_evidence
    from .validate_json_schema import ROOT_DIR, decode_json, load_json, make_validator, structural_errors
except ImportError:
    from evidence_common import digest, now, write_evidence
    from validate_json_schema import ROOT_DIR, decode_json, load_json, make_validator, structural_errors

MEDIA_TYPE = "application/vnd.in-toto+json"
STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "https://github.com/kevin-biot/blast-radius-framework/blob/main/spec/predicates/evidence-v1.md"
SCHEMAS = {"acs_trace": "acs-trace-evidence.schema.json", "evaluation": "evaluation-evidence.schema.json",
           "execution": "execution-evidence.schema.json", "inventory_links": "inventory-links.schema.json"}
MAX_EVIDENCE = 8_000_000


class VerificationError(ValueError):
    pass


def crypto():
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    except ImportError as exc:
        raise ValueError("Run bash tools/install-integrations-local.sh and use .tools/integration-env/bin/python") from exc
    return serialization, Ed25519PrivateKey, Ed25519PublicKey, InvalidSignature


def read_limited(path, limit=MAX_EVIDENCE):
    with Path(path).open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("input exceeds size limit")
    return data


def validate(value, schema):
    errors = structural_errors(make_validator(load_json(ROOT_DIR / "spec" / schema)), value)
    if errors:
        raise ValueError("; ".join(errors))


def pae(payload_type, body):
    kind = payload_type.encode("utf-8")
    return b"DSSEv1 " + str(len(kind)).encode() + b" " + kind + b" " + str(len(body)).encode() + b" " + body


def unbase64(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9+/_-]*={0,2}", value):
        raise ValueError("invalid base64 encoding")
    return base64.b64decode(value + "=" * (-len(value) % 4), altchars=b"-_", validate=True)


def key_fingerprint(key):
    serialization, *_ = crypto()
    return digest(key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo))


def seal(evidence_path, evidence_type, private_key_path, signing_context="caller_supplied_key"):
    import json
    serialization, private_type, *_ = crypto()
    raw = read_limited(evidence_path)
    evidence = decode_json(raw.decode("utf-8"))
    validate(evidence, SCHEMAS[evidence_type])
    private = serialization.load_pem_private_key(read_limited(private_key_path, 16_384), password=None)
    if not isinstance(private, private_type):
        raise ValueError("only Ed25519 private keys are supported")
    statement = {"_type": STATEMENT_TYPE,
                 "subject": [{"name": Path(evidence_path).name, "digest": {"sha256": digest(raw)}}],
                 "predicateType": PREDICATE_TYPE,
                 "predicate": {"evidence_type": evidence_type, "evidence_schema": SCHEMAS[evidence_type],
                     "issued_at": now(), "verification_scope": "signature_and_subject_integrity_only",
                     "signing_context": signing_context, "evidence": evidence}}
    validate(statement, "evidence-statement.schema.json")
    body = json.dumps(statement, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return {"payloadType": MEDIA_TYPE, "payload": base64.b64encode(body).decode("ascii"),
            "signatures": [{"keyid": "sha256:" + key_fingerprint(private.public_key()),
                            "sig": base64.b64encode(private.sign(pae(MEDIA_TYPE, body))).decode("ascii")}]}


def decode_envelope(raw):
    envelope = decode_json(raw.decode("utf-8"))
    validate(envelope, "dsse-envelope.schema.json")
    body = unbase64(envelope["payload"])
    signatures = [unbase64(item["sig"]) for item in envelope["signatures"]]
    return envelope["payloadType"], body, signatures


def verify(envelope_path, evidence_path, public_key_path):
    import json
    serialization, _, public_type, invalid_signature = crypto()
    kind, body, signatures = decode_envelope(read_limited(envelope_path, 40_000_000))
    key = serialization.load_pem_public_key(read_limited(public_key_path, 16_384))
    if not isinstance(key, public_type):
        raise ValueError("only Ed25519 trusted public keys are supported")
    verified = False
    for signature in signatures:
        try:
            key.verify(signature, pae(kind, body))
            verified = True
            break
        except invalid_signature:
            continue
    if not verified:
        raise VerificationError("no signature verifies against the supplied trusted public key")
    if kind != MEDIA_TYPE:
        raise VerificationError("unsupported authenticated payload type")
    # Parse exactly the bytes verified above, never a second envelope read.
    statement = decode_json(body.decode("utf-8"))
    validate(statement, "evidence-statement.schema.json")
    predicate = statement["predicate"]
    expected_schema = SCHEMAS[predicate["evidence_type"]]
    if predicate["evidence_schema"] != expected_schema:
        raise VerificationError("evidence type/schema binding mismatch")
    raw = read_limited(evidence_path)
    if statement["subject"][0]["digest"]["sha256"] != digest(raw):
        raise VerificationError("supplied subject bytes do not match the signed digest")
    evidence = decode_json(raw.decode("utf-8"))
    validate(evidence, expected_schema)
    validate(predicate["evidence"], expected_schema)
    if json.dumps(evidence, sort_keys=True, allow_nan=False) != json.dumps(predicate["evidence"], sort_keys=True, allow_nan=False):
        raise VerificationError("signed predicate differs from the supplied evidence")
    return {"signature_verified": True, "subject_digest_verified": True,
            "trusted_key_sha256": key_fingerprint(key), "evidence_claims_verified": False,
            "authority_verified": False, "statement": statement}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export")
    export.add_argument("--evidence", type=Path, required=True)
    export.add_argument("--evidence-type", choices=SCHEMAS, required=True)
    export.add_argument("--private-key", type=Path, required=True, help="caller-managed unencrypted Ed25519 PEM; not a key-management service")
    export.add_argument("--output", type=Path, required=True)
    check = sub.add_parser("verify")
    check.add_argument("--envelope", type=Path, required=True)
    check.add_argument("--evidence", type=Path, required=True)
    check.add_argument("--public-key", type=Path, required=True, help="trusted PEM selected out of band, not from the envelope")
    args = parser.parse_args()
    try:
        if args.command == "export":
            write_evidence(seal(args.evidence, args.evidence_type, args.private_key), "dsse-envelope.schema.json", args.output)
            print("EXPORTED: DSSE Ed25519 envelope; not a trusted identity or BR certification")
        else:
            result = verify(args.envelope, args.evidence, args.public_key)
            print(f"VERIFIED: signature and supplied subject bytes; trusted key SHA-256 {result['trusted_key_sha256']}; claims/authority NOT verified")
        return 0
    except VerificationError as exc:
        print(f"NOT VERIFIED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
