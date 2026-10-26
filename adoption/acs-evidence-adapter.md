# ACS Control and Evidence Adapter

**Status:** Implemented local fixture and transcript exporter; live interoperability not run
**Reviewed:** 2026-10-26

**Unreleased extension:** the [native ACS OTLP reader](./alignment-implementation.md) can now ingest the pinned upstream synthetic trace sample and correlate its decision/failure events. It does not replace the transcript adapter below, execute the Guardian or establish actual enforcement.

## Pinned Surface

The adapter uses [ACS v0.1.4](https://github.com/GenAI-Security-Project/agent-control-standard/releases/tag/v0.1.4), commit `834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8`, whose wire/schema version is 0.1.0. It supports the `steps/toolCallRequest` hook and final dispositions. Other hooks and full `modify`, `ask` and `defer` workflows are not implemented. The fixture pauses those dispositions; only `allow` can dispatch.

The [OWASP introduction](https://genai.owasp.org/resource/agent-control-standard-acs/) describes the standard. Neither that announcement nor schema-valid messages establish that a deployment is fail-closed. The [reference README checked in the review](https://github.com/GenAI-Security-Project/agent-control-standard/blob/4cf23d4cce832e522ffab69e7dd8d7209ec11a9a/README.md) discloses fail-open and authentication limitations. We have not executed that Guardian here.

## Evidence Map

| Captured evidence | BRF relevance | Limit |
|---|---|---|
| Tool name and proposed arguments | A: intended action envelope | Not a tested ceiling or proof of reachable tools |
| Policy reference/version | I3: declared policy binding | Matching a string is not cryptographic verification of a policy snapshot |
| Allow/deny plus actual dispatch observation | I6: default-deny investigation | Not full I6-T1 token cases or I6-T2 cryptographic verification |
| Missing response plus observed blocked dispatch | I6: outage behaviour | Does not test all timeout, crash or retry paths |
| Request/session IDs and input digest | O: correlation and input provenance | Not trace completeness, independent timestamping or tamper-proof observation |
| Target revision and source kind | Reproduction scope | Supplied labels require independent corroboration |

Every record keeps the decision and the actual outcome separate. Execution after a denial or outage fails the consistency check. An allowed tool that executes and returns failure is not a denial bypass; its failure remains visible as an outcome. An unused allow is inconclusive for the execution test, not a denial bypass. Missing policy-version references produce an inconclusive result. Invalid payloads and mismatched correlations are rejected.

`evaluation_status: pass` means consistency **only for supplied events**, not a BR class, token verification result, statistically estimated failure rate or ACS certification. Outcomes are supplied observations; a malicious or incomplete observer can lie. Preserve and independently inspect the source transcript identified by `input_sha256`.

## Run It

Use the exact install, fetch, fixture, export and validation commands in [`../tools/README.md`](../tools/README.md). Output follows [`../spec/acs-evidence.schema.json`](../spec/acs-evidence.schema.json). The demo has no external state mutation and does not contact the upstream Guardian.

Next integration acceptance criteria: run the pinned upstream implementation under a recorded configuration; observe the protected tool independently; exercise allow, denial, outage and bypass paths; retain request/response and external receipts; test cross-tenant isolation, revocation and retries. Report fail-open behaviour rather than silently replacing it with the local fixture's semantics.

## Telemetry and Evaluation Bridge

The following is a **mapping design**, not a shipped OpenTelemetry exporter or native Inspect/AgentDojo reader. Pin an upstream telemetry convention revision before selecting concrete attribute names from the [GenAI conventions repository](https://github.com/open-telemetry/semantic-conventions-genai).

| BRF logical field | Telemetry/evaluation input to retain | Additional binding needed |
|---|---|---|
| Request/session identity | Tool span ID, trace ID and evaluation sample ID | A declared mapping across retries and asynchronous work; do not assume session ID equals trace ID |
| Proposed action | Tool and redacted arguments or canonical digest | Tenant, audience, scopes, policy version and declared exposure budget |
| Decision and execution | Policy disposition, tool attempt and external receipt | Distinguish denied attempt, dispatch, commit and compensation |
| Outcome | Task success and separately committed violation | Scenario ground truth and independent observer |
| Reproduction | Model, scaffold, dataset, seed, configuration and target revisions | Captured exogenous inputs; a seed alone is not replay evidence |
| Aggregate result | Trials, denominators and uncertainty | Predeclared failure definition, confidence method and scope limits |

Do not export secrets or raw prompts by default. Minimise sensitive content and declare retention and access controls. Ordinary spans are not signed attestations. A native evaluation exporter must demonstrate a repeatable scenario and separately schema-validate its output before R09 can close.
