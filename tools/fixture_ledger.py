#!/usr/bin/env python3
"""Loopback-only effect sink for boundary experiments, not a production service."""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import socket
import sqlite3
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from time import time_ns


class Ledger(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, database, token, mode, handler=None):
        super().__init__(("127.0.0.1", 0), handler or Handler)
        self.database, self.token, self.mode = database, token, mode
        self.lock = threading.Lock()
        self.gates, self.waiting = {}, {}
        with self.connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE grant_state (active INTEGER, budget INTEGER, spent INTEGER);
                INSERT INTO grant_state VALUES (1, 3, 0);
                CREATE TABLE receipts (seq INTEGER PRIMARY KEY, operation_id TEXT UNIQUE,
                    amount INTEGER, payload_hash TEXT, committed_ns INTEGER);
            """)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.database, timeout=5)
        try:
            with db:
                yield db
        finally:
            db.close()

    def wait(self, name, phase, operation):
        if not name:
            return
        with self.lock:
            event = self.gates.setdefault(name, threading.Event())
            request = operation + ":" + str(threading.get_ident())
            self.waiting[request] = {"gate": name, "phase": phase}
        try:
            if not event.wait(10):
                raise TimeoutError("fixture gate was not released within ten seconds")
        finally:
            with self.lock:
                self.waiting.pop(request, None)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def respond(self, status, value):
        data = json.dumps(value, allow_nan=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def authorized(self):
        if not hmac.compare_digest(self.headers.get("Authorization", ""), "Bearer " + self.server.token):
            self.respond(401, {"error": "fixture token required"})
            return False
        return True

    def do_GET(self):
        if not self.authorized():
            return
        if self.path != "/state":
            return self.respond(404, {"error": "unknown endpoint"})
        with self.server.connect() as db:
            active, budget, spent = db.execute("SELECT * FROM grant_state").fetchone()
        with self.server.lock:
            waiting = dict(self.server.waiting)
        self.respond(200, {"active": bool(active), "budget": budget, "spent": spent, "waiting": waiting})

    def do_POST(self):
        if not self.authorized():
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 8192:
                raise ValueError("invalid request size")
            body = json.loads(self.rfile.read(size))
            if not isinstance(body, dict):
                raise ValueError("expected object")
            if self.path == "/revoke":
                with self.server.connect() as db:
                    db.execute("UPDATE grant_state SET active=0")
                return self.respond(200, {"revoked": True})
            if self.path == "/release":
                name = body.get("gate")
                if not isinstance(name, str) or not name:
                    raise ValueError("gate must be a nonempty string")
                with self.server.lock:
                    self.server.gates.setdefault(name, threading.Event()).set()
                return self.respond(200, {"released": name})
            if self.path != "/commit":
                return self.respond(404, {"error": "unknown endpoint"})
            self.commit(body)
        except (ValueError, KeyError, TypeError, TimeoutError) as exc:
            self.respond(400, {"error": str(exc)})
        except sqlite3.Error:
            self.respond(503, {"error": "ledger unavailable; no success asserted"})

    def commit(self, body):
        operation, amount = body.get("operation_id"), body.get("amount")
        command = body.get("command", "fixture increment")
        if not isinstance(operation, str) or not 0 < len(operation) <= 100:
            raise ValueError("invalid operation_id")
        if type(amount) is not int or not 0 < amount <= 3 or not isinstance(command, str):
            raise ValueError("invalid amount or command")
        for key in ("wait_before", "wait_after"):
            if key in body and (not isinstance(body[key], str) or len(body[key]) > 100):
                raise ValueError("invalid gate")
        payload_hash = hashlib.sha256(json.dumps([amount, command], separators=(",", ":")).encode()).hexdigest()
        # The unsafe control deliberately snapshots authority before the gate.
        with self.server.connect() as db:
            active, budget, spent = db.execute("SELECT * FROM grant_state").fetchone()
        stale_permit = active and spent + amount <= budget
        self.server.wait(body.get("wait_before"), "before_commit", operation)
        with self.server.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            prior = db.execute("SELECT seq, payload_hash, committed_ns FROM receipts WHERE operation_id=?", (operation,)).fetchone()
            if prior:
                seq, prior_hash, committed_ns = prior
                if prior_hash != payload_hash:
                    return self.respond(409, {"error": "idempotency key conflicts with prior payload"})
                receipt = {"seq": seq, "operation_id": operation, "amount": amount, "committed_ns": committed_ns, "replayed": True}
            else:
                active, budget, spent = db.execute("SELECT * FROM grant_state").fetchone()
                permit = active and spent + amount <= budget if self.server.mode == "atomic" else stale_permit
                if not permit:
                    return self.respond(403, {"error": "revoked or aggregate budget exhausted"})
                committed_ns = time_ns()
                row = db.execute("INSERT INTO receipts(operation_id, amount, payload_hash, committed_ns) VALUES (?, ?, ?, ?)",
                                 (operation, amount, payload_hash, committed_ns))
                db.execute("UPDATE grant_state SET spent=spent+?", (amount,))
                receipt = {"seq": row.lastrowid, "operation_id": operation, "amount": amount, "committed_ns": committed_ns, "replayed": False}
            db.commit()
        self.server.wait(body.get("wait_after"), "after_commit", operation)
        if body.get("drop_response"):
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            return
        self.respond(200, receipt)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--mode", choices=("atomic", "check_then_commit"), default="atomic")
    args = parser.parse_args()
    if args.database.exists():
        parser.error("database must be new; existing evidence is never reset")
    token = args.token_file.read_text().strip()
    if len(token) < 32:
        parser.error("fixture token too short")
    args.database.touch(mode=0o600, exist_ok=False)
    server = Ledger(args.database, token, args.mode)
    print(f"http://127.0.0.1:{server.server_port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
