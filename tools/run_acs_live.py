#!/usr/bin/env python3
"""Execute the pinned upstream Guardian/shim against a separate durable tool."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from .acs_trace_evidence import read_trace, trace_assets
    from .evidence_common import digest, write_evidence
    from .execution_fixture import Tool, artifact_paths, artifacts, bundle, case, first_line, stop
    from .install_acs_runtime import AGT, BUN, BUN_VERSION, CHECKOUT, COMMIT, ROOT
except ImportError:
    from acs_trace_evidence import read_trace, trace_assets
    from evidence_common import digest, write_evidence
    from execution_fixture import Tool, artifact_paths, artifacts, bundle, case, first_line, stop
    from install_acs_runtime import AGT, BUN, BUN_VERSION, CHECKOUT, COMMIT, ROOT


def verify_runtime():
    if not BUN.is_file() or not AGT.is_dir():
        raise ValueError("Run python3 tools/install_acs_runtime.py first")
    for args, expected in [([str(BUN), "--version"], BUN_VERSION),
                           (["git", "rev-parse", "HEAD"], COMMIT),
                           (["git", "status", "--porcelain", "--untracked-files=no"], "")]:
        result = subprocess.run(args, cwd=CHECKOUT, capture_output=True, text=True, check=True, timeout=15)
        if result.stdout.strip() != expected:
            raise ValueError(f"Runtime pin/cleanliness check failed: {args}")


class Guardian:
    def __init__(self, directory, posture):
        self.directory = directory
        directory.mkdir(mode=0o700)
        self.env = {key: value for key, value in os.environ.items()
                    if key in {"PATH", "HOME", "SYSTEMROOT", "TMPDIR"}}
        self.env.update(NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost",
                        ACS_GUARDIAN_PORT="0", ACS_GUARDIAN_HOST="127.0.0.1",
                        ACS_ENVELOPE_LOG=str(directory / "envelopes.jsonl"),
                        ACS_SESSION_CONTEXT_LOG=str(directory / "session-context.jsonl"),
                        ACS_OTEL_FILE=str(directory / "trace.jsonl"),
                        ACS_SESSION_DIR=str(directory / "sessions"),
                        ACS_AUDIT_LOG=str(directory / "audit.jsonl"))
        if posture == "deny":
            self.env["ACS_ON_DECISION_FAILURE"] = "deny"
        self.stderr = (directory / "guardian.stderr").open("w")
        self.process = subprocess.Popen([str(BUN), "run", "packages/guardian/src/main.ts"], cwd=AGT,
            env=self.env, stdout=subprocess.PIPE, stderr=self.stderr, text=True)
        line = first_line(self.process)
        prefix = "Guardian listening at http://localhost:"
        if not line.startswith(prefix):
            self.close()
            raise RuntimeError(f"Unexpected Guardian startup: {line}; inspect guardian.stderr")
        self.env["ACS_GUARDIAN_URL"] = line.removeprefix("Guardian listening at ").replace("localhost", "127.0.0.1")
        self.session = "brf-live-" + posture

    def hook(self, command, result=None):
        payload = {"session_id": self.session, "hook_event_name": "PreToolUse" if result is None else "PostToolUse",
                   "tool_name": "Bash", "tool_input": {"command": command}}
        if result is not None:
            payload["tool_response"] = {"stdout": json.dumps(result)}
        output = subprocess.run([str(BUN), "run", "hosts/claude-code/acs-hook.ts"], cwd=AGT,
            env=self.env, input=json.dumps(payload), capture_output=True, text=True, timeout=20)
        if output.returncode != 0:
            raise RuntimeError(f"Upstream hook failed ({output.returncode}): {output.stderr[:1000]}")
        return json.loads(output.stdout)

    def close(self):
        try:
            stop(self.process)
        finally:
            self.stderr.close()
            if self.process.stdout:
                self.process.stdout.close()

    def last_request(self, command, decision):
        rows = [json.loads(line) for line in (self.directory / "envelopes.jsonl").read_text().splitlines()]
        request = next(row for row in reversed(rows) if row["direction"] == "request" and row["method"] == "steps/toolCallRequest")
        response = next(row for row in rows if row["direction"] == "response" and row["rpc_id"] == request["rpc_id"])
        params = request["envelope"]["params"]
        if params["payload"]["raw_command"] != command or response["envelope"]["result"]["decision"] != decision:
            raise ValueError("Hook/wire observation mismatch")
        self.wire_session = params["metadata"]["session_id"]
        return {"acs_request_id": params["request_id"], "acs_session_id": self.wire_session}


def run(directory):
    verify_runtime()
    directory = Path(directory).resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    paths = artifact_paths(("run_acs_live.py", "install_acs_runtime.py", "acs_trace_evidence.py"))
    paths += [AGT / name for name in ("bun.lock", "policy/manifest.yaml", "policy/lib/data.json")]
    before, cases = artifacts(paths), []
    for posture in ("default", "deny"):
        guardian = Guardian(directory / posture, posture)
        try:
            with Tool(directory / (posture + "-tool")) as tool:
                for name, command, bypass, expected_decision, expected in [
                    ("allow", "echo brf-safe", False, "allow", 1),
                    ("deny", "echo rm -rf /", False, "deny", 0),
                    ("deny_bypass_control", "echo rm -rf /", True, "deny", 1),
                ]:
                    operation = posture + "-" + name
                    output = guardian.hook(command)
                    decision = output.get("hookSpecificOutput", {}).get("permissionDecision")
                    if decision != expected_decision:
                        raise ValueError(f"Unexpected upstream decision for {operation}: {output}")
                    correlation = guardian.last_request(command, decision)
                    if decision == "allow" or bypass:
                        status, receipt = tool.call("/commit", {"operation_id": operation, "amount": 1, "command": command})
                        if status != 200:
                            raise ValueError(f"Tool did not commit expected effect: {status} {receipt}")
                        guardian.hook(command, receipt)
                    observation = tool.observe()
                    observation["receipts"] = [r for r in observation["receipts"] if r["operation_id"] == operation]
                    cases.append(case(operation, expected, observation, decision, violation=bypass))
                    cases[-1].update(correlation)
                # Same session and cached handshake; only the real Guardian stops.
                guardian.close()
                operation = posture + "-outage"
                output = guardian.hook("echo rm -rf /")
                decision = output.get("hookSpecificOutput", {}).get("permissionDecision")
                expected_decision = "allow" if posture == "default" else "deny"
                if decision != expected_decision:
                    raise ValueError(f"Outage posture mismatch: {output}")
                if decision == "allow":
                    if tool.call("/commit", {"operation_id": operation, "amount": 1})[0] != 200:
                        raise ValueError("fail-open effect did not commit")
                observation = tool.observe()
                observation["receipts"] = [r for r in observation["receipts"] if r["operation_id"] == operation]
                cases.append(case(operation, int(posture == "default"), observation, decision,
                                  violation=posture == "default"))
                audit = [json.loads(line) for line in (guardian.directory / "audit.jsonl").read_text().splitlines()]
                if not audit:
                    raise ValueError("No upstream outage audit record")
                entry = audit[-1]
                if (entry.get("posture") != ("proceed" if posture == "default" else "deny")
                    or entry.get("posture_source") != "negotiated"
                    or entry.get("outcome") != ("proceeded" if posture == "default" else "blocked")
                    or entry.get("failure", {}).get("kind") != "transport"):
                    raise ValueError("Unexpected upstream outage audit semantics")
                cases[-1].update(acs_request_id=entry["rpc_id"], acs_session_id=guardian.wire_session)
                subprocess.run([str(BUN), "run", "packages/guardian/src/audit-to-otlp.ts",
                    str(guardian.directory / "audit.jsonl"), str(guardian.directory / "host-trace.jsonl")],
                    cwd=AGT, env=guardian.env, check=True, capture_output=True, text=True, timeout=20)
        finally:
            guardian.close()
    # These remain trace-only analyses, kept separate from the receipt evidence.
    mapping, manifest = trace_assets()
    for posture in ("default", "deny"):
        trace = read_trace([directory / posture / name for name in ("trace.jsonl", "host-trace.jsonl")], mapping)
        trace["mapping_sha256"] = manifest["files"]["otel-mapping.json"]["sha256"]
        write_evidence(trace, "acs-trace-evidence.schema.json", directory / posture / "trace-analysis.json")
    verify_runtime()
    result = bundle("acs_live", cases, before, paths, {"repository": "GenAI-Security-Project/agent-control-standard",
                    "commit": COMMIT, "release": "v0.1.4", "bun": BUN_VERSION})
    result["captures"] = [{"path": str(path.relative_to(directory)), "sha256": digest(path.read_bytes())}
        for posture in ("default", "deny") for name in ("envelopes.jsonl", "audit.jsonl", "trace.jsonl", "host-trace.jsonl")
        for path in [directory / posture / name]]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True, help="new directory for private runtime artifacts")
    args = parser.parse_args()
    try:
        result = run(args.run_dir)
        write_evidence(result, "execution-evidence.schema.json", args.run_dir / "evidence.json")
        print(f"{len(result['cases'])} cases; expectations met: {result['expectations_met']}; "
              f"observed violation cases: {result['boundary_violation_cases']}")
        return 0 if result["expectations_met"] else 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
