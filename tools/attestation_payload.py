"""BRF-JCS-0.1.1 payload construction; HMAC test/reference support only."""
from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".tools/jsonschema-lib"))
try:
    import rfc8785
except ImportError as exc:
    raise SystemExit("Run `bash tools/install-jsonschema-local.sh` first.") from exc

PAYLOAD_PROFILE = "BRF-JCS-0.1.1"


def signing_bytes(attestation):
    payload = copy.deepcopy(attestation)
    signature = payload["signature"]
    if signature.get("payload_profile") != PAYLOAD_PROFILE:
        raise ValueError("ambiguous or unsupported signature payload profile")
    if signature.get("signed_payload_canonical_form") != "JCS-RFC8785":
        raise ValueError("only JCS-RFC8785 is implemented")
    if not signature.get("signed_at"):
        raise ValueError("signed_at is required")
    payload.pop("anchor", None)
    signature["signature_value"] = ""
    return rfc8785.dumps(payload)


def anchor_bytes(attestation):
    payload = copy.deepcopy(attestation)
    payload.pop("anchor", None)
    return rfc8785.dumps(payload)


def hmac_signature(attestation, key):
    if attestation["signature"]["algorithm"] != "HMAC-SHA256":
        raise ValueError("reference helper only supports HMAC-SHA256")
    return base64.b64encode(hmac.new(key, signing_bytes(attestation), hashlib.sha256).digest()).decode("ascii")


def verify_hmac(attestation, key):
    return hmac.compare_digest(hmac_signature(attestation, key), attestation["signature"]["signature_value"])
