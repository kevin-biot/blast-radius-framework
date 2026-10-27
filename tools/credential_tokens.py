"""Bounded JWT access-token checks for a local fixture, not an identity provider."""
import base64
import hashlib
import json
import re
import time
from uuid import uuid4

try:
    from .validate_json_schema import decode_json
except ImportError:
    from validate_json_schema import decode_json

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

ISSUER = "https://issuer.example.invalid/brf-fixture"
AUDIENCE = "urn:brf:fixture:credential-ledger"
SCOPE = "ledger:increment"
MAX_LIFETIME = 300
REQUIRED = ("iss", "sub", "aud", "exp", "iat", "nbf", "jti", "client_id", "brf_tenant", "scope")


class CredentialError(ValueError):
    def __init__(self, reason, status=401):
        self.reason, self.status = reason, status
        super().__init__(reason)


def credential_id(claims):
    return hashlib.sha256(json.dumps([claims["iss"], claims["jti"]], separators=(",", ":")).encode()).hexdigest()


def load_public(data):
    key = serialization.load_pem_public_key(data)
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError("fixture requires a caller-pinned Ed25519 issuer key")
    return key


def verify_token(token, key, tenant):
    try:
        if not isinstance(token, str) or len(token) > 8192:
            raise CredentialError("invalid_credential")
        parts = token.split(".")
        if len(parts) != 3 or any(not re.fullmatch(r"[A-Za-z0-9_-]+", part) for part in parts):
            raise CredentialError("invalid_credential")
        # Reject ambiguous JSON before the library parses it; no decision is
        # authorized from these unverified previews.
        header, preview = [decode_json(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)).decode("utf-8")) for part in parts[:2]]
        if not isinstance(header, dict) or not isinstance(preview, dict):
            raise CredentialError("invalid_credential")
        if header.get("alg") != "EdDSA" or header.get("typ") != "at+jwt":
            raise CredentialError("unsupported_token_type_or_algorithm")
        if any(name in header for name in ("jku", "x5u", "jwk", "x5c", "crit", "b64")):
            raise CredentialError("unsupported_key_or_critical_header")
        if not isinstance(header.get("kid", ""), str):
            raise CredentialError("invalid_credential")
        for name in REQUIRED:
            value = preview.get(name)
            if name in ("exp", "iat", "nbf"):
                if type(value) is not int:
                    raise CredentialError("invalid_claim_type")
            elif not isinstance(value, str) or not value.strip() or len(value) > 256:
                raise CredentialError("invalid_claim_type")
        if not preview["iat"] <= preview["nbf"] < preview["exp"]:
            raise CredentialError("invalid_time_order")
        if preview["exp"] - preview["iat"] > MAX_LIFETIME:
            raise CredentialError("credential_lifetime_exceeds_policy")
        claims = jwt.decode(token, key, algorithms=["EdDSA"], issuer=ISSUER, audience=AUDIENCE, leeway=0,
                            options={"require": list(REQUIRED), "strict_aud": True, "verify_signature": True,
                                     "verify_iss": True, "verify_aud": True, "verify_iat": True,
                                     "verify_exp": True, "verify_nbf": True})
        if claims["brf_tenant"] != tenant:
            raise CredentialError("wrong_tenant", 403)
        if not re.fullmatch(r"[\x21\x23-\x5b\x5d-\x7e]+(?: [\x21\x23-\x5b\x5d-\x7e]+)*", claims["scope"]):
            raise CredentialError("invalid_scope_encoding")
        if SCOPE not in claims["scope"].split(" "):
            raise CredentialError("insufficient_scope", 403)
        return claims
    except CredentialError:
        raise
    except jwt.ExpiredSignatureError as exc:
        raise CredentialError("expired_credential") from exc
    except jwt.ImmatureSignatureError as exc:
        raise CredentialError("credential_not_yet_valid") from exc
    except jwt.InvalidAudienceError as exc:
        raise CredentialError("wrong_audience") from exc
    except jwt.InvalidIssuerError as exc:
        raise CredentialError("wrong_issuer") from exc
    except (jwt.InvalidTokenError, ValueError, TypeError, UnicodeError, RecursionError) as exc:
        raise CredentialError("invalid_credential") from exc


class FixtureIssuer:
    """In-memory test signer; its private key is never sent to the tool process."""
    def __init__(self):
        self.key = Ed25519PrivateKey.generate()

    def public_bytes(self):
        return self.key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

    def issue(self, **overrides):
        instant = int(time.time())
        claims = {"iss": ISSUER, "aud": AUDIENCE, "sub": "fixture-agent-alpha", "client_id": "fixture-client",
                  "iat": instant, "nbf": instant, "exp": instant + MAX_LIFETIME, "jti": str(uuid4()),
                  "brf_tenant": "alpha", "scope": SCOPE}
        claims.update(overrides)
        return jwt.encode(claims, self.key, algorithm="EdDSA", headers={"typ": "at+jwt"}), claims
