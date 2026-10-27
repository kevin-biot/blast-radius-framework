#!/usr/bin/env python3
"""Measure signed-credential admission/commit checks against a durable tool."""
import argparse
import base64
import json
import os
import secrets
import sqlite3
import subprocess
import sys
import time
import hmac
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization

try:
    from .credential_tokens import AUDIENCE, ISSUER, FixtureIssuer, credential_id, load_public
    from .evidence_common import digest, now, write_evidence
    from .execution_fixture import ROOT, Tool, artifact_paths, artifacts, bundle, case, first_line
    from .validate_json_schema import decode_json, load_json, make_validator, structural_errors
except ImportError:
    from credential_tokens import AUDIENCE, ISSUER, FixtureIssuer, credential_id, load_public
    from evidence_common import digest, now, write_evidence
    from execution_fixture import ROOT, Tool, artifact_paths, artifacts, bundle, case, first_line
    from validate_json_schema import decode_json, load_json, make_validator, structural_errors


class CredentialTool(Tool):
    def __init__(self, directory, public_key, mode="commit_recheck"):
        self.directory, self.mode = Path(directory), mode
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        self.database, self.token = self.directory / "ledger.sqlite", secrets.token_urlsafe(32)
        token_file, key_file = self.directory / "token", self.directory / "issuer-public.pem"
        for path, data in ((token_file, self.token.encode()), (key_file, public_key)):
            with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
                stream.write(data)
        self.stderr = (self.directory / "service.stderr").open("w")
        self.process = subprocess.Popen([sys.executable, str(ROOT / "tools/credential_ledger.py"),
            "--database", str(self.database), "--token-file", str(token_file), "--issuer-public-key", str(key_file),
            "--mode", mode], stdout=subprocess.PIPE, stderr=self.stderr, text=True)
        try:
            self.url = first_line(self.process)
            if not self.url.startswith("http://127.0.0.1:"):
                raise ValueError("unexpected credential fixture address")
        except BaseException:
            self.close()
            raise

    def observe_details(self):
        with closing(sqlite3.connect(self.database.as_uri() + "?mode=ro", uri=True)) as db:
            db.row_factory = sqlite3.Row
            db.execute("BEGIN")
            receipts = [dict(row) for row in db.execute("SELECT * FROM credential_receipts ORDER BY seq")]
            balances = [{**dict(row), "active": bool(row["active"])} for row in db.execute("SELECT * FROM tenants ORDER BY tenant")]
        observation = {"receipts": [{key: row[key] for key in ("seq", "operation_id", "amount", "payload_hash", "committed_ns")} for row in receipts],
                       "active": all(row["active"] for row in balances), "budget": sum(row["budget"] for row in balances),
                       "spent": sum(row["spent"] for row in balances)}
        return observation, receipts, balances

    def observe(self):
        return self.observe_details()[0]


def run(directory):
    if jwt.__version__ != "2.15.1":
        raise ValueError("Install the pinned PyJWT 2.15.1 integration runtime")
    directory = Path(directory).resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    issuer = FixtureIssuer()
    public = issuer.public_bytes()
    (directory / "issuer-public.pem").write_bytes(public)
    paths = artifact_paths(("credential_tokens.py", "credential_ledger.py", "run_credential_boundary.py", "integration-requirements.txt"))
    paths += [ROOT / "spec/credential-context.schema.json"]
    before, cases, contexts = artifacts(paths), [], []

    def record(name, tool, expected, results, expected_statuses, ids=(), checks=None, violation=False, residual=0):
        observation, receipts, balances = tool.observe_details()
        row = case(name, expected, observation, violation=violation, residual=residual)
        row["checks"] = {"http_statuses_match": [status for status, _ in results] == expected_statuses, **(checks or {})}
        row["expectation_met"] &= all(row["checks"].values())
        cases.append(row)
        contexts.append({"case_id": name, "mode": tool.mode, "http_statuses": [s for s, _ in results],
                         "error_reasons": [body["error"] for _, body in results if "error" in body],
                         "credential_ids_sha256": sorted(set(ids)), "tenant_balances": balances, "receipts": receipts})

    instant = int(time.time())
    scenarios = [
        ("valid_credential", {}, None, 200),
        ("wrong_signing_key", {}, "wrong_key", 401),
        ("tampered_signed_claims", {}, "tampered", 401),
        ("wrong_issuer", {"iss": "https://other.example.invalid"}, None, 401),
        ("wrong_audience", {"aud": "urn:brf:other-tool"}, None, 401),
        ("wrong_tenant", {"brf_tenant": "beta"}, None, 403),
        ("missing_scope", {"scope": "ledger:read"}, None, 403),
        ("expired_credential", {"iat": instant - 60, "nbf": instant - 60, "exp": instant - 10}, None, 401),
        ("not_yet_valid", {"nbf": instant + 60}, None, 401),
        ("missing_required_claim", {}, "missing_claim", 401),
        ("id_token_type_rejected", {}, "wrong_type", 401),
        ("symmetric_algorithm_rejected", {}, "wrong_algorithm", 401),
        ("unsecured_token_rejected", {}, "unsecured", 401),
        ("key_discovery_header_rejected", {}, "jku", 401),
        ("key_id_is_not_trust", {}, "kid", 200),
        ("boolean_expiry_rejected", {"exp": True}, None, 401),
        ("excessive_credential_lifetime", {"exp": instant + 600}, None, 401),
        ("revoked_before_dispatch", {}, "revoked", 401),
        ("revocation_state_unavailable", {}, "unavailable", 503),
        ("admin_secret_not_access_token", {}, "admin", 401),
    ]
    for name, overrides, injection, expected_status in scenarios:
        token, claims = issuer.issue(**overrides)
        identifier = credential_id(claims)
        with CredentialTool(directory / name, public) as tool:
            if injection == "wrong_key":
                token, claims = FixtureIssuer().issue()
                identifier = credential_id(claims)
            elif injection == "tampered":
                parts = token.split(".")
                parts[1] = base64.urlsafe_b64encode(json.dumps({**claims, "sub": "forged-subject"}).encode()).decode().rstrip("=")
                token = ".".join(parts)
            elif injection == "missing_claim":
                claims.pop("client_id")
                token = jwt.encode(claims, issuer.key, algorithm="EdDSA", headers={"typ": "at+jwt"})
            elif injection in ("wrong_type", "jku", "kid"):
                header = {"typ": "JWT"} if injection == "wrong_type" else {"typ": "at+jwt", injection: "https://example.invalid/not-fetched"}
                token = jwt.encode(claims, issuer.key, algorithm="EdDSA", headers=header)
            elif injection == "wrong_algorithm":
                token = jwt.encode(claims, "fixture-only-symmetric-secret-not-a-trust-anchor", algorithm="HS256", headers={"typ": "at+jwt"})
            elif injection == "unsecured":
                token = jwt.encode(claims, key=None, algorithm="none", headers={"typ": "at+jwt"})
            elif injection == "revoked":
                tool.call("/revoke", {"credential_id": identifier})
            elif injection == "unavailable":
                tool.call("/availability", {"available": False})
            elif injection == "admin":
                token = tool.token
            result = tool.call("/tenants/alpha/increment", {"operation_id": "probe", "amount": 1}, token=token)
            record(name, tool, int(expected_status == 200), [result], [expected_status], [] if injection == "admin" else [identifier])

    for dimension in ("tenant", "principal", "client"):
        name = "idempotency_namespace_" + dimension
        first, first_claims = issuer.issue()
        second, second_claims = issuer.issue(**({"brf_tenant": "beta"} if dimension == "tenant" else {"sub": "fixture-agent-other"} if dimension == "principal" else {"client_id": "fixture-client-other"}))
        with CredentialTool(directory / name, public) as tool:
            results = [tool.call("/tenants/alpha/increment", {"operation_id": "same", "amount": 1}, token=first),
                       tool.call(f"/tenants/{second_claims['brf_tenant']}/increment", {"operation_id": "same", "amount": 1}, token=second)]
            record(name, tool, 2, results, [200, 200], [credential_id(first_claims), credential_id(second_claims)],
                   {"distinct_receipts": results[0][1].get("seq") != results[1][1].get("seq")})

    for name in ("retry_requires_current_credential", "revocation_binds_issuer_jti_not_encoding", "agent_cannot_use_admin_control"):
        token, claims = issuer.issue()
        identifier = credential_id(claims)
        with CredentialTool(directory / name, public) as tool:
            body = {"operation_id": "same", "amount": 1}
            if name == "agent_cannot_use_admin_control":
                results = [tool.call("/revoke", {"credential_id": identifier}, token=token)]
                record(name, tool, 0, results, [401], [identifier])
                continue
            results = [tool.call("/tenants/alpha/increment", body, token=token)] if name == "retry_requires_current_credential" else []
            tool.call("/revoke", {"credential_id": identifier})
            if name == "revocation_binds_issuer_jti_not_encoding":
                token = jwt.encode(claims, issuer.key, algorithm="EdDSA", headers={"typ": "at+jwt", "kid": "changed-hint"})
            results.append(tool.call("/tenants/alpha/increment", body, token=token))
            record(name, tool, int(name == "retry_requires_current_credential"), results,
                   [200, 401] if name == "retry_requires_current_credential" else [401], [identifier])

    for injection in ("revoked", "expired", "unavailable"):
        for mode in ("commit_recheck", "admission_only"):
            name = "inflight_" + injection + "_" + mode
            with CredentialTool(directory / name, public, mode) as tool, ThreadPoolExecutor(max_workers=1) as pool:
                token, claims = issuer.issue(**({"exp": int(time.time()) + 3} if injection == "expired" else {}))
                identifier = credential_id(claims)
                future = pool.submit(tool.call, "/tenants/alpha/increment", {"operation_id": "inflight", "amount": 1, "wait_before": "commit"}, token)
                tool.wait_for(1)
                if injection == "revoked":
                    tool.call("/revoke", {"credential_id": identifier})
                elif injection == "unavailable":
                    tool.call("/availability", {"available": False})
                else:
                    deadline = time.monotonic() + 6
                    while time.time() < claims["exp"]:
                        if time.monotonic() >= deadline:
                            raise TimeoutError("wall clock did not reach fixture expiry within the bounded wait")
                        time.sleep(0.02)
                tool.call("/release", {"gate": "commit"})
                result = future.result(timeout=8)
                unsafe = mode == "admission_only"
                record(name, tool, int(unsafe), [result], [200 if unsafe else 503 if injection == "unavailable" else 401], [identifier], violation=unsafe)

    token, claims = issuer.issue()
    identifier = credential_id(claims)
    with CredentialTool(directory / "already-committed", public) as tool, ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(tool.call, "/tenants/alpha/increment", {"operation_id": "committed", "amount": 1, "wait_after": "response"}, token)
        tool.wait_for(1, "after_commit")
        effect_seen = tool.observe()["spent"] == 1
        tool.call("/revoke", {"credential_id": identifier})
        tool.call("/release", {"gate": "response"})
        results = [future.result(timeout=8), tool.call("/tenants/alpha/increment", {"operation_id": "later", "amount": 1}, token=token)]
        record("revocation_cannot_undo_commit", tool, 1, results, [200, 401], [identifier], {"effect_preceded_revocation": effect_seen}, residual=1)
    with CredentialTool(directory / "bearer-reuse", public) as tool:
        token, claims = issuer.issue()
        results = [tool.call("/tenants/alpha/increment", {"operation_id": f"reuse-{i}", "amount": 1}, token=token) for i in range(4)]
        record("bearer_reuse_is_not_prevented_but_budget_is_bounded", tool, 3, results, [200, 200, 200, 403], [credential_id(claims)])

    context = {"schema_version": "0.1.0", "generated_at": now(), "issuer": ISSUER, "audience": AUDIENCE,
               "trusted_key_sha256": digest(issuer.key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)),
               "library": {"name": "PyJWT", "version": jwt.__version__}, "mandate_status": "not_established",
               "observation_scope": "same_machine_fixture", "records": contexts,
               "limits": ["Fixture-issued bearer credentials and verified claims are not corporate/legal authority or a verified real-world actor.",
                          "Loopback local state, no OAuth/OIDC server, distributed revocation, TLS, holder binding or hostile-host protection.",
                          "Admission-only modes are deliberate unsafe controls; passing expectations is not a safety verdict."]}
    write_evidence(context, "credential-context.schema.json", directory / "credential-context.json")
    result = bundle("credential_boundary", cases, before, paths)
    result["schema_version"] = "0.1.1"
    result["captures"] = [{"path": path.name, "sha256": digest(path.read_bytes())} for path in
                          (directory / "credential-context.json", directory / "issuer-public.pem")]
    return result


def check_packet(directory):
    directory = Path(directory).resolve()
    snapshots = {}
    for name, limit in (("evidence.json", 8_000_000), ("credential-context.json", 8_000_000), ("issuer-public.pem", 16_384)):
        path = directory / name
        if path.is_symlink():
            raise ValueError("packet files must not be symbolic links")
        with path.open("rb") as stream:
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise ValueError("packet file exceeds size limit")
        snapshots[name] = raw
    result, context = [decode_json(snapshots[name].decode("utf-8")) for name in ("evidence.json", "credential-context.json")]
    for instance, schema in ((result, "execution-evidence.schema.json"), (context, "credential-context.schema.json")):
        errors = structural_errors(make_validator(load_json(ROOT / "spec" / schema)), instance)
        if errors:
            raise ValueError("; ".join(errors))
    if result["kind"] != "credential_boundary" or result["schema_version"] != "0.1.1":
        raise ValueError("not a credential execution packet")
    captures = result.get("captures", [])
    names = [item["path"] for item in captures]
    if len(names) != 2 or set(names) != {"credential-context.json", "issuer-public.pem"}:
        raise ValueError("unexpected capture set; paths are never followed outside the explicit packet")
    for item in captures:
        if not hmac.compare_digest(item["sha256"], digest(snapshots[item["path"]])):
            raise ValueError("capture digest mismatch")
    key = load_public(snapshots["issuer-public.pem"])
    fingerprint = digest(key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo))
    if not hmac.compare_digest(fingerprint, context["trusted_key_sha256"]):
        raise ValueError("issuer public-key binding mismatch")
    if context["issuer"] != ISSUER or context["audience"] != AUDIENCE or context["library"]["version"] != "2.15.1":
        raise ValueError("fixture verifier configuration mismatch")
    rows = {row["case_id"]: row for row in context["records"]}
    if len(rows) != len(context["records"]) or len({c["case_id"] for c in result["cases"]}) != len(result["cases"]):
        raise ValueError("duplicate case identity")
    if set(rows) != {c["case_id"] for c in result["cases"]}:
        raise ValueError("execution/context cases do not match")
    for item in result["cases"]:
        row = rows[item["case_id"]]
        receipts = [{key: receipt[key] for key in ("seq", "operation_id", "amount", "payload_hash", "committed_ns")} for receipt in row["receipts"]]
        if receipts != item["receipts"] or len({r["seq"] for r in receipts}) != len(receipts):
            raise ValueError("receipt projection or sequence mismatch")
        balances = row["tenant_balances"]
        if len(balances) != 2 or {b["tenant"] for b in balances} != {"alpha", "beta"}:
            raise ValueError("invalid tenant balance set")
        for balance in balances:
            if balance["spent"] != sum(r["amount"] for r in row["receipts"] if r["tenant"] == balance["tenant"]):
                raise ValueError("per-tenant receipt accounting mismatch")
            if balance["spent"] > balance["budget"]:
                raise ValueError("tenant budget exceeded")
        amount = sum(r["amount"] for r in receipts)
        if (item["observed_committed_amount"] != amount or item["spent"] != amount
            or item["budget"] != sum(b["budget"] for b in balances) or item["active"] != all(b["active"] for b in balances)
            or item["residual_amount"] > amount):
            raise ValueError("execution receipt accounting mismatch")
        expected = amount == item["expected_committed_amount"] and all(item.get("checks", {}).values())
        if item["expectation_met"] != expected:
            raise ValueError("inconsistent case expectation summary")
    if (result["expectations_met"] != all(c["expectation_met"] for c in result["cases"])
        or result["boundary_violation_cases"] != sum(c["boundary_violation"] for c in result["cases"])):
        raise ValueError("inconsistent aggregate summary")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true", help="validate an existing packet's schemas, hashes and internal accounting, not observation truth")
    args = parser.parse_args()
    try:
        if not args.check_only:
            result = run(args.run_dir)
            write_evidence(result, "execution-evidence.schema.json", args.run_dir / "evidence.json")
        result = check_packet(args.run_dir)
        print(f"{len(result['cases'])} credential cases; expectations met: {result['expectations_met']}; "
              f"deliberate violation cases: {result['boundary_violation_cases']}; external mandate NOT established")
        return 0 if result["expectations_met"] else 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
