#!/usr/bin/env python3
"""Loopback JWT credential-boundary fixture; not an OAuth authorization server."""
import argparse
import hashlib
import hmac
import json
import re
import sqlite3
import threading
from pathlib import Path
from time import time_ns

try:
    from .credential_tokens import CredentialError, credential_id, load_public, verify_token
    from .fixture_ledger import Handler, Ledger
    from .validate_json_schema import decode_json
except ImportError:
    from credential_tokens import CredentialError, credential_id, load_public, verify_token
    from fixture_ledger import Handler, Ledger
    from validate_json_schema import decode_json


class CredentialLedger(Ledger):
    def __init__(self, database, admin, public_key, mode):
        self.public_key = load_public(public_key)
        super().__init__(database, admin, mode, handler=CredentialHandler)
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE tenants (tenant TEXT PRIMARY KEY, active INTEGER, budget INTEGER, spent INTEGER);
                INSERT INTO tenants VALUES ('alpha',1,3,0), ('beta',1,3,0);
                CREATE TABLE revocation_status (available INTEGER);
                INSERT INTO revocation_status VALUES (1);
                CREATE TABLE revoked_credentials (credential_id TEXT PRIMARY KEY);
                CREATE TABLE credential_receipts (seq INTEGER PRIMARY KEY, tenant TEXT, principal TEXT,
                    client_id TEXT, operation_id TEXT, amount INTEGER, payload_hash TEXT,
                    credential_id TEXT, committed_ns INTEGER,
                    UNIQUE(tenant, principal, client_id, operation_id));
            """)

    def authorize(self, db, token, tenant):
        claims = verify_token(token, self.public_key, tenant)
        if not db.execute("SELECT available FROM revocation_status").fetchone()[0]:
            raise CredentialError("revocation_state_unavailable", 503)
        if db.execute("SELECT 1 FROM revoked_credentials WHERE credential_id=?", (credential_id(claims),)).fetchone():
            raise CredentialError("revoked_credential")
        grant = db.execute("SELECT active FROM tenants WHERE tenant=?", (tenant,)).fetchone()
        if not grant or not grant[0]:
            raise CredentialError("resource_grant_unavailable", 403)
        return claims


class CredentialHandler(Handler):
    def bearer(self):
        values = self.headers.get_all("Authorization", [])
        if len(values) != 1 or not values[0].startswith("Bearer "):
            raise CredentialError("invalid_authorization_header")
        return values[0][7:]

    def admin(self):
        provided = self.bearer().encode("utf-8")
        if not hmac.compare_digest(provided, self.server.token.encode("ascii")):
            raise CredentialError("control_plane_credential_required")

    def do_GET(self):
        try:
            self.admin()
            if self.path != "/state":
                return self.respond(404, {"error": "unknown_endpoint"})
            with self.server.lock:
                waiting = dict(self.server.waiting)
            self.respond(200, {"waiting": waiting})
        except CredentialError as exc:
            self.respond(exc.status, {"error": exc.reason})

    def do_POST(self):
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 8192:
                raise ValueError("invalid_request_size")
            body = decode_json(self.rfile.read(size).decode("utf-8"))
            if not isinstance(body, dict):
                raise ValueError("object_required")
            if self.path in ("/revoke", "/availability", "/release"):
                self.admin()
                return self.control(body)
            match = re.fullmatch(r"/tenants/(alpha|beta)/increment", self.path)
            if not match:
                return self.respond(404, {"error": "unknown_endpoint"})
            self.commit_for_tenant(match[1], body, self.bearer())
        except CredentialError as exc:
            self.respond(exc.status, {"error": exc.reason})
        except (ValueError, TypeError, KeyError, TimeoutError, RecursionError) as exc:
            self.respond(400, {"error": str(exc)})
        except sqlite3.Error:
            self.respond(503, {"error": "ledger_unavailable"})

    def control(self, body):
        if self.path == "/release":
            gate = body.get("gate")
            if not isinstance(gate, str) or not 0 < len(gate) <= 100:
                raise ValueError("invalid_gate")
            with self.server.lock:
                self.server.gates.setdefault(gate, threading.Event()).set()
            return self.respond(200, {"released": True})
        with self.server.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if self.path == "/revoke":
                identifier = body.get("credential_id")
                if not isinstance(identifier, str) or not re.fullmatch(r"[0-9a-f]{64}", identifier):
                    raise ValueError("invalid_credential_identifier")
                db.execute("INSERT OR IGNORE INTO revoked_credentials VALUES (?)", (identifier,))
            else:
                available = body.get("available")
                if type(available) is not bool:
                    raise ValueError("boolean_availability_required")
                db.execute("UPDATE revocation_status SET available=?", (int(available),))
            db.commit()
        self.respond(200, {"acknowledged": True})

    def commit_for_tenant(self, tenant, body, token):
        if set(body) - {"operation_id", "amount", "wait_before", "wait_after"}:
            raise ValueError("unsupported_request_field")
        operation, amount = body.get("operation_id"), body.get("amount")
        if not isinstance(operation, str) or not 0 < len(operation) <= 100:
            raise ValueError("invalid_operation_id")
        if type(amount) is not int or not 0 < amount <= 3:
            raise ValueError("invalid_amount")
        for key in ("wait_before", "wait_after"):
            if key in body and (not isinstance(body[key], str) or not 0 < len(body[key]) <= 100):
                raise ValueError("invalid_gate")
        with self.server.connect() as db:
            db.execute("BEGIN")
            claims = self.server.authorize(db, token, tenant)
        self.server.wait(body.get("wait_before"), "before_commit", operation)
        with self.server.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if self.server.mode == "commit_recheck":
                claims = self.server.authorize(db, token, tenant)
            principal, client = claims["sub"], claims["client_id"]
            identity = (tenant, principal, client, operation)
            payload_hash = hashlib.sha256(json.dumps([*identity[:3], amount], separators=(",", ":")).encode()).hexdigest()
            prior = db.execute("SELECT seq, amount, payload_hash, committed_ns FROM credential_receipts "
                               "WHERE tenant=? AND principal=? AND client_id=? AND operation_id=?", identity).fetchone()
            if prior:
                seq, _prior_amount, prior_hash, committed_ns = prior
                if prior_hash != payload_hash:
                    return self.respond(409, {"error": "idempotency_payload_conflict"})
                replayed = True
            else:
                budget, spent = db.execute("SELECT budget,spent FROM tenants WHERE tenant=?", (tenant,)).fetchone()
                if spent + amount > budget:
                    raise CredentialError("tenant_budget_exhausted", 403)
                committed_ns = time_ns()
                row = db.execute("INSERT INTO credential_receipts(tenant,principal,client_id,operation_id,amount,payload_hash,credential_id,committed_ns) "
                                 "VALUES (?,?,?,?,?,?,?,?)", (*identity, amount, payload_hash, credential_id(claims), committed_ns))
                db.execute("UPDATE tenants SET spent=spent+? WHERE tenant=?", (amount, tenant))
                seq, replayed = row.lastrowid, False
            db.commit()
        self.server.wait(body.get("wait_after"), "after_commit", operation)
        self.respond(200, {"seq": seq, "tenant": tenant, "principal": principal, "client_id": client,
                           "operation_id": operation, "amount": amount, "committed_ns": committed_ns, "replayed": replayed})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--token-file", type=Path, required=True, help="control-plane secret, never an agent access token")
    parser.add_argument("--issuer-public-key", type=Path, required=True)
    parser.add_argument("--mode", choices=("commit_recheck", "admission_only"), default="commit_recheck")
    args = parser.parse_args()
    token = args.token_file.read_text().strip()
    if len(token) < 32 or not token.isascii():
        parser.error("invalid fixture admin credential")
    args.database.touch(mode=0o600, exist_ok=False)
    server = CredentialLedger(args.database, token, args.issuer_public_key.read_bytes(), args.mode)
    print(f"http://127.0.0.1:{server.server_port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
