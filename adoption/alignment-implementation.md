# Project Alignment Implementation

**Status:** Repository/tooling release v0.5.12; framework v0.5.11 and spec 0.1.1 unchanged
**Date:** 2026-10-26

The first package implements native ACS trace ingestion, a native Inspect log exporter and an OPA-backed fixed-proposal comparison. These are interoperability and mechanism tests, not a certification programme or new agent failure-rate study.

**Follow-up:** [live boundary experiments](./live-boundary-experiments.md) in tooling v0.5.13 execute the real pinned Guardian/shim and add durable asynchronous effect tests. The original v0.5.12 verification record below remains historical; the follow-up records its own scope and results.

**2026-10-27 follow-up:** tooling v0.5.14 implements [DSSE/in-toto portability and CycloneDX linking](./evidence-portability-and-inventory.md). These are optional companion formats, not new BR ratings or a key-trust service.

## Task List and Results

| Order | Work | Implemented and run | Still open |
|---|---|---|---|
| 1 | Native ACS ingestion | OTLP/JSON and JSONL reader; pinned mapping/sample; joins by session + request, result references, failure precedence and conflict checks; separate v0.5.13 live local experiment | Production Guardian deployment, OCSF reader, authenticated independent observation and complete ACS-Trace conformance |
| 2 | Native Inspect exporter | Pinned Inspect 0.3.283 API reads both `.eval` and JSON; separate task/violation scores; missing scores, cancelled/truncated/invalidated runs remain inconclusive | AgentDojo importer, model-driven adversarial workload and independently audited scorers |
| 3 | Non-Lane2 policy example | Digest-pinned OPA 1.21.4 executed real Rego decisions; same eight fixed scenarios in three modes; Inspect produced a real log with no LLM generation; separate v0.5.13 local async race tests | Full canonical A2A/MCP comparison, distributed external effects and independent reproduction |
| 4 | Repeatable verification | One-command local checks; CI workflow with commit-pinned actions and read-only permissions; v0.5.12 hosted Linux run passed | Follow-up hosted runs checked separately; transitive Python dependencies are not fully locked |
| 5 | Standard evidence packaging | v0.5.14 Ed25519 DSSE export; explicit trusted-key verifier and separate stdlib/OpenSSL path; ephemeral-key demo and negative tests | Native BR-profile asymmetric verification, trusted signer lifecycle, timestamps/anchors and independent assessment |
| 6 | Component inventory interoperability | v0.5.14 full pinned CycloneDX 1.7 schema validation and explicit card/profile linking; gaps preserved | Deployed identity, inventory completeness, other formats/versions and actual runtime reach |
| 7 | Identity and threat coverage | Existing delegation cards and test proposals retained | Live credential revocation/audience tests and selected OWASP scenario mappings |

## ACS: What the Reader Actually Establishes

The reader pins release [v0.1.4](https://github.com/GenAI-Security-Project/agent-control-standard/releases/tag/v0.1.4), commit `834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8`. Its schema version remains 0.1.0, so a schema-version label alone does not identify these trace rules. The [pinned trace specification](https://github.com/GenAI-Security-Project/agent-control-standard/blob/834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8/docs/spec/trace/events.md) defines the session/request join and failure precedence.

A failure reported by either stream makes the pair's decision ineligible as a usable decision. Absence of a failure does not prove enforcement. Every output record therefore says `enforcement_status: not_verified`, even when a tool-result event reports success. Service names, policy versions and chain hashes are untrusted claims. Conflicting verdicts/hashes, dropped telemetry and orphan result references are findings; they are not silently discarded. Duplicate identical span exports are deduplicated; conflicting exports with the same trace/span identity are rejected. Handshake failure invalidates decision eligibility throughout the reported session.

The upstream committed sample is synthetic. It produced six request pairs, three reported failure pairs and fail-open findings. No upstream Guardian was executed by ingesting that file. The sample's original Apache 2.0 licence is cached alongside it. Unknown span names are counted as ignored; the reader is not a general OTLP or full ACS-Trace validator.

## Inspect: Score Semantics Are Explicit

The exporter uses Inspect's [native log API](https://inspect.aisi.org.uk/eval-logs.html), not a guessed log format. Its two declared scorers are `task_success` and `boundary_violation` by default. Boolean and numeric 0/1 values are accepted; string labels require separate explicit positive/negative mappings for each scorer. A generic correctness score cannot silently become containment evidence.

The source log digest, producer/model, task version, declared policy/revision, selected generation settings, sample IDs/types and epochs are retained. Duplicate sample/epoch identities are rejected when present in the decoded log. Inspect's `.eval` writer can coalesce duplicate identities before storage; an importer cannot recover observations omitted by a producer. Source-log integrity and observer/scorer completeness still need independent review.

Missing scores, sample errors/limits, explicit scorer `metadata.brf_error`, cancellation, invalidation, unknown planned sample counts and a mismatch between planned and observed samples prevent a pass. A known violation remains a failure even if other samples are unknown. Task success is counted separately: a complete run with failed tasks but no scored boundary violation can have a boundary-evaluation pass. This is not an assertion of task usefulness. No prompts, tool arguments, credentials or arbitrary generation headers are copied into the exported bundle; identifiers and selected metadata still require a privacy review before publication.

## OPA: Fixed Proposals, Not an Agent Benchmark

OPA is a separate policy decision point; our fixture host enforces its boolean response before mutating an in-memory ledger. This follows the distinction in OPA's [agent-tool-calling guidance](https://www.openpolicyagent.org/docs/agent-tool-calling). Undefined/malformed responses, process errors and timeouts do not authorize dispatch. The proposed principal and grants are fictional technical inputs, not proof of a corporate mandate.

The [worked example](../examples/opa-boundary/README.md) compares `unmediated`, `schema_only` and `opa_enforced`. **`schema_only` is not a canonical A2A/MCP implementation.** The selected proposals and ledger expectations are hand-authored, with no LLM sampling. The results establish only that the implemented policy/host combination handles these cases. They neither quantify production risk nor falsify the retained worldview floor. Budget tests are sequential; they do not establish race-free distributed accounting.

## Reproduction and Limits

Use the [local utility instructions](../tools/README.md) to install optional runtimes and fetch pinned assets, then run `bash tools/check-alignment-local.sh`. The check runner preserves new evidence in a unique ignored directory and expects nonzero finding exits from the upstream ACS sample and the intentionally unsafe comparison baselines. Missing dependencies cause errors, not skipped integration passes.

Network access is needed for installation and pinned data retrieval. The v0.5.12 checks use local OPA, local files and Inspect's mock model; they make no external model calls. Inspect may use its normal application-data trace/cache directory in addition to the chosen log directory. The local run used macOS arm64 / Python 3.14.3; [the published v0.5.12 workflow passed on Linux / Python 3.12](https://github.com/kevin-biot/blast-radius-framework/actions/runs/40345335934). The v0.5.13 checks also start isolated loopback Guardian and tool processes.

No independent assessment, full agent-client ACS integration, insurance outcome, legal compliance decision or revised BR rating is claimed. The next research step remains a preregistered model-driven comparison with actual protocol implementations and an external observer.

## Verification Record

On 2026-10-26, `bash tools/check-alignment-local.sh` passed 44 unit tests and 12 native integration tests. The check also validated four existing profiles, one component card and all three generated evidence bundles. The pinned ACS synthetic sample produced six request pairs and three reported failure pairs; all enforcement states remained unverified. OPA matched all eight fixture expectations with zero declared violation cases; the two negative-control modes each had six violation cases. Inspect produced and re-imported a native `.eval` log with eight scored samples and no model generation.

Python compilation, shell syntax, changed/new-file whitespace and new relative-link checks passed. The workflow YAML parsed with read-only permissions and commit-pinned actions. Publication was followed by successful hosted run `40345335934`, then tag v0.5.12. This packages the tools without changing classifications. The unrelated DAREB note was not modified.
