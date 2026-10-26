"""Process lifecycle and read-only receipt observation for local experiments."""
from __future__ import annotations

import json
import os
import queue
import secrets
import sqlite3
import subprocess
import sys
import threading
import time
from contextlib import closing
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

try:
    from .evidence_common import digest, now
except ImportError:
    from evidence_common import digest, now

ROOT = Path(__file__).resolve().parent.parent
OPENER = build_opener(ProxyHandler({}))


def stop(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    if process.returncode not in (0, -15):
        raise RuntimeError(f"fixture subprocess exited {process.returncode}")


def first_line(process, timeout=15):
    result = queue.Queue()
    threading.Thread(target=lambda: result.put(process.stdout.readline()), daemon=True).start()
    try:
        line = result.get(timeout=timeout).strip()
        if not line:
            raise RuntimeError("fixture subprocess ended before reporting readiness")
        return line
    except BaseException:
        stop(process)
        raise


class Tool:
    def __init__(self, directory, mode="atomic"):
        self.directory = Path(directory)
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        self.database = self.directory / "ledger.sqlite"
        self.token = secrets.token_urlsafe(32)
        token_file = self.directory / "token"
        with token_file.open("x") as stream:
            os.chmod(token_file, 0o600)
            stream.write(self.token)
        self.stderr = (self.directory / "service.stderr").open("w")
        self.process = subprocess.Popen([sys.executable, str(ROOT / "tools/fixture_ledger.py"),
            "--database", str(self.database), "--token-file", str(token_file), "--mode", mode],
            stdout=subprocess.PIPE, stderr=self.stderr, text=True)
        self.url = first_line(self.process)
        if not self.url.startswith("http://127.0.0.1:"):
            self.close()
            raise RuntimeError("unexpected fixture service address")

    def call(self, path, body=None, token=None):
        request = Request(self.url + path, data=json.dumps(body).encode() if body is not None else None,
                          headers={"Authorization": "Bearer " + (self.token if token is None else token),
                                   "Content-Type": "application/json"})
        try:
            with OPENER.open(request, timeout=15) as response:
                return response.status, json.load(response)
        except HTTPError as exc:
            with closing(exc):
                return exc.code, json.load(exc)

    def observe(self):
        # A separate connection reads committed records, not HTTP verdicts.
        with closing(sqlite3.connect(self.database.as_uri() + "?mode=ro", uri=True)) as db:
            db.execute("BEGIN")
            receipts = [{"seq": row[0], "operation_id": row[1], "amount": row[2],
                         "payload_hash": row[3], "committed_ns": row[4]}
                        for row in db.execute("SELECT * FROM receipts ORDER BY seq")]
            active, budget, spent = db.execute("SELECT * FROM grant_state").fetchone()
        return {"receipts": receipts, "active": bool(active), "budget": budget, "spent": spent}

    def wait_for(self, count, phase="before_commit"):
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            status, state = self.call("/state")
            if status == 200 and sum(x["phase"] == phase for x in state["waiting"].values()) == count:
                return
            time.sleep(0.01)
        raise TimeoutError(f"did not observe {count} requests at {phase}")

    def close(self):
        try:
            stop(self.process)
        finally:
            self.stderr.close()
            if self.process.stdout:
                self.process.stdout.close()
            (self.directory / "token").unlink(missing_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


def artifact_paths(extra=()):
    return [ROOT / "tools" / name for name in ("fixture_ledger.py", "execution_fixture.py", "evidence_common.py",
            "validate_json_schema.py", *extra)] + [ROOT / "spec/execution-evidence.schema.json"]


def artifacts(paths):
    return [{"path": str(path.relative_to(ROOT)), "sha256": digest(path.read_bytes())} for path in paths]


def bundle(kind, cases, before, paths, upstream=None):
    if before != artifacts(paths):
        raise ValueError("experiment source changed during execution")
    return {"schema_version": "0.1.0", "kind": kind, "generated_at": now(),
            "scope": "local_fixed_proposal_mechanism_test", "observer": "same_machine_read_only_sqlite",
            "authority_scope": "fixture_runtime_grants_only", "signed": False,
            "upstream": upstream, "artifacts": before, "cases": cases,
            "expectations_met": all(case["expectation_met"] for case in cases),
            "boundary_violation_cases": sum(case["boundary_violation"] for case in cases)}


def case(name, expected, observation, decision="not_applicable", violation=False, residual=0):
    observed = sum(row["amount"] for row in observation["receipts"])
    return {"case_id": name, "decision": decision, "expected_committed_amount": expected,
            "observed_committed_amount": observed, "expectation_met": observed == expected,
            "boundary_violation": bool(violation and observed), "residual_amount": min(residual, observed), **observation}
