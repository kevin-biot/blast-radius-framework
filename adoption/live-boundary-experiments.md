# Live Boundary and Asynchronous Effect Experiments

**Date:** 2026-10-26
**Scope:** Repository/tooling v0.5.13; framework definitions 0.5.11 and spec 0.1.1 unchanged

These experiments distinguish a policy verdict, host dispatch, a durable tool commit and a residual effect. They use fixed proposals, no LLM generation, no paid API, no production credentials and no external network destination during execution. They demonstrate mechanisms and counterexamples, not deployment safety, population failure rates, a BR rating or organisational authority.

## Approved Task List

| Order | Acceptance Criteria | Result |
|---|---|---|
| 1 | Publish the native readers, OPA example and CI; verify hosted execution | Completed as [v0.5.12](https://github.com/kevin-biot/blast-radius-framework/tree/v0.5.12), commit `fed02782ba0969c3919125d5995e635069e67519`; [Linux/Python 3.12 CI passed](https://github.com/kevin-biot/blast-radius-framework/actions/runs/40345335934) |
| 2 | Run the pinned real Guardian and upstream shim; retain allow, deny, outage and bypass decisions with separate tool receipts | Implemented and run locally: eight cases, two failure-posture configurations; raw wire/audit/trace captures retained per run |
| 3 | Test retries, concurrent budget consumption, revocation before/during execution and committed residuals | Implemented and run locally: eleven cases, real HTTP concurrency, explicit race barriers and read-only durable-receipt observation |
| 4 | Export optional in-toto/DSSE evidence and demonstrate asymmetric verification independently | Implemented in v0.5.14: Ed25519 wrapper, explicit trusted-key verification and separate stdlib/OpenSSL command; original native bundles remain unsigned |
| 5 | Link CycloneDX inventory entries to component cards without inferring runtime reach | Implemented in v0.5.14: full pinned offline 1.7 schema, explicit exact-version card/profile mappings and visible gaps |

Steps 2 and 3 are repeatable local integration experiments. Their presence in CI configuration does not by itself establish a successful hosted run, independent reproduction or production coverage.

The [2026-10-27 portability and inventory follow-up](./evidence-portability-and-inventory.md) records completion criteria, verification limits and reproduction for tasks 4 and 5 separately from the original v0.5.13 test record.

**Hosted verification:** [run 40348621393 passed](https://github.com/kevin-biot/blast-radius-framework/actions/runs/40348621393) at implementation commit `22803bc836e57ace3117a782b9b9adafd0c91da9` on Ubuntu 24.04 / Python 3.12. Its logs confirm 44 base tests, 20 native integration tests, eight live cases and eleven asynchronous cases. This is a second platform under the same project-controlled workflow, not independent assessment. Subsequent successful runs retain a fixture-only evidence artifact for 14 days; download may require GitHub sign-in. Only allowlisted JSON/JSONL evidence and fake-input wire captures are uploaded, not credentials, SQLite databases, dependency trees or arbitrary application logs.

**Local verification:** on 2026-10-26, `bash tools/check-alignment-local.sh` passed 44 base tests and 20 native integration tests on macOS arm64 / Python 3.14.3. All nineteen new experiment cases matched their predeclared outcomes. Four existing profiles, one component card and all five generated evidence bundles validated. Python compilation, shell syntax and workflow YAML checks passed; relative-link checking found no new broken links (five historical changelog references predate this package). The unrelated DAREB note was not changed or staged.

## Live ACS: Eight Cases

The actual [ACS v0.1.4 reference Guardian](https://github.com/GenAI-Security-Project/agent-control-standard/tree/834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8/reference-implementations/agt) and its shipped Claude Code hook execute at commit `834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8`, using Bun 1.3.11 and the frozen upstream dependency lock. The Guardian evaluates its bundled AGT policy; BRF does not substitute the earlier fixture policy.

The harness invokes the upstream hook directly, not Claude Code or OpenCode themselves. It presents `Bash` proposals that exercise AGT's stock command-pattern rule. **No proposed shell command is executed.** Instead, the BRF fixture host dispatches a real HTTP tool that increments a private SQLite ledger and returns a receipt. Command text, including the inert deny probe `echo rm -rf /`, remains data. This tests Guardian/shim-to-tool dispatch integration, not Bash sandboxing or end-to-end agent-client conformance.

| Case In Each Configuration | Upstream Hook Result | Observed Tool Commit |
|---|---|---|
| Ordinary allowed proposal | allow | 1 unit |
| Pattern-denied proposal, host honors decision | deny | 0 units |
| Same denied proposal, host deliberately ignores hook | deny | 1 unit; negative-control boundary violation |
| Guardian stopped after a successful handshake, same cached session | default configuration: allow; explicit `ACS_ON_DECISION_FAILURE=deny`: deny | default: 1 unit; explicit deny: 0 units |

All eight expected outcomes matched locally. Three cases had deliberately observed boundary violations: both bypass controls and the default-posture outage. **An experiment passing means those expected unsafe outcomes were detected, not that every mode is safe.**

The outage uses the previously negotiated posture, not a fabricated response or replacement Guardian. Both upstream audit records identify transport failure and a negotiated proceed/block outcome. The upstream audit-to-OTLP converter produces host failure spans, which are read together with Guardian traces. Online hook decisions are checked against actual wire responses; case records retain request/session IDs and durable receipt IDs, amounts, payload digests and commit timestamps. Capture digests bind the retained wire/audit/trace files locally.

Every trace-analysis record still says `enforcement_status: not_verified`. Tool receipts are separate evidence, not a reason to upgrade a self-reported span. The reference does not supply tool-result request references in these hook payloads, so result-correlation findings remain visible rather than being guessed away.

## Asynchronous Effects: Eleven Cases

The separate Python tool process binds only to loopback. It uses a random fixture bearer credential, a fresh owner-only database, integer amounts, idempotency keys bound to payload hashes, and a three-unit grant budget. The harness reads committed receipts through a separate read-only SQLite connection. This is separate-process observation on the **same machine**, not an independent assessor or authenticated external witness.

| Test | Observed Result |
|---|---|
| Sequential retry with one idempotency key | One commit; retry returns the original receipt |
| Commit succeeds but HTTP response is dropped, then retry | Receipt exists before retry; one total commit; retry reports replay |
| Reuse key with a different amount | Conflict rejected; original one-unit commit remains |
| Two concurrent requests with the same key and payload | Both requests reach the pause point; one commit and one replay |
| Two concurrent two-unit requests; atomic grant/budget check and commit | One succeeds, one is denied; two units committed, within budget |
| Same workload; deliberately stale check-before-commit control | Both succeed; four units exceed the three-unit budget |
| Revoke queued work before tool dispatch | No commit |
| Revoke while request is paused before commit; atomic recheck | No commit |
| Same race; deliberately stale-check control | One post-revocation commit; boundary violation detected |
| Revoke after commit but before response | Existing one-unit effect remains and its response arrives; new work is denied |
| Direct request without fixture credential | Unauthorized; no commit |

All eleven expected outcomes matched locally, including two deliberate violations. Pause/release barriers establish ordering; no race conclusion depends on a lucky sleep. The unsafe control snapshots its grant and budget before the barrier. The atomic mode serializes idempotency, grant/budget checks, receipt creation and budget consumption in one SQLite transaction.

Idempotency is local to this service/database and bound to amount plus inert command text. A receipt proves this ledger's recorded mutation, not an email delivery, financial settlement or every downstream effect. Retrying with a new key can create another effect. Revocation governs future commits in the atomic mode; it does not roll back prior commits. The residual is reported explicitly and is not mislabeled as a new post-revocation violation.

## Reproduce

Follow [local runtime installation](../tools/README.md), then choose fresh run directories:

```sh
python3 tools/install_acs_runtime.py
python3 tools/run_acs_live.py --run-dir .tools/acs-live-example
python3 tools/run_async_boundary.py --run-dir .tools/async-boundary-example
python3 tools/validate_json_schema.py spec/execution-evidence.schema.json .tools/acs-live-example/evidence.json .tools/async-boundary-example/evidence.json
bash tools/check-alignment-local.sh
```

The installer supports macOS arm64 and Linux x86_64, verifies an embedded Bun release-archive SHA-256, pins the ACS Git commit, refuses a changed tracked checkout, and installs frozen dependencies with lifecycle scripts disabled. It installs no global runtime. Dependency binaries are still executable third-party code; review them before use. The local installation digest is not an independently trusted signature or supply-chain attestation.

The runners require a new directory and never reset an existing ledger. Exit 0 means every predeclared experimental outcome matched, including unsafe controls; exit 1 means an outcome mismatch; exit 2 means an operational/dependency/input failure. Schema validation checks structure and declared formats, not the truth or authenticity of observations. Evidence remains unsigned. Runtime artifacts stay under ignored `.tools/`; raw logs and identifiers need review before sharing. Temporary bearer-token files are removed on ordinary shutdown, not guaranteed cleanup after a crash.

## Remaining Gaps

The fixture has one local grant, not production identities, tenant isolation, audience-bound credentials, business delegation or a corporate approval system. Its control-plane credential is deliberately available to the harness, including bypass controls. It is not an RBAC or hostile-host security demonstration. The upstream wire remains unauthenticated. Nothing here infers external authority from a runtime permission.

Distributed accounting, clock skew and expiry, process-crash recovery, partitions, real cancellation/compensation, long-running external effects, model-driven attacks, canonical A2A/MCP clients and independent reproduction remain open. These tests exercise local transactional mechanisms; they do not revise I1, other invariants, the open-world floor or existing profiles. Optional evidence packaging and inventory linking are now implemented separately in v0.5.14; neither closes these runtime research gaps.
