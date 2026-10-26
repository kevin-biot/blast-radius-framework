# Local BRF Utilities

Run from the repository root with Python 3.10+ and pip. Tested locally with Python 3.14.3 on 2026-10-26. No production agent runtime or general conformance runner is included.

## Install and Validate

```sh
bash tools/install-jsonschema-local.sh
python3 tools/validate_json_schema.py --check-repository
```

The installer puts dependencies under ignored `.tools/jsonschema-lib`. Direct dependencies are pinned in `requirements.txt`; transitive dependencies are not a fully locked environment. Installation needs network access. Normal validation is offline: unknown remote schema references fail rather than being fetched.

The repository check covers example and report profiles, component cards and their profile links. Individual checks can supply a profile catalogue:

```sh
python3 tools/validate_json_schema.py spec/component-card.schema.json spec/examples/example-component-card-tool-legal-db.json --profile spec/examples/example-profile-closed-world-br2.json
```

Checks include schema validity, supported formats, duplicate JSON keys, non-finite numbers, component/edge references, the retained open-world floor, expiry ordering and invariant/test-ID prefixes. They do **not** establish freshness, full BR arithmetic, execution conformance, signatures, anchors, coverage or legal compliance. Old examples remain illustrative, not newly signed attestations.

## ACS-Shaped Local Fixture

```sh
python3 tools/fetch_acs_schemas.py
python3 tools/demo_acs.py --output .tools/acs-demo/transcript.json
python3 tools/acs_evidence.py .tools/acs-demo/transcript.json --output .tools/acs-demo/evidence.json
python3 tools/validate_json_schema.py spec/acs-evidence.schema.json .tools/acs-demo/evidence.json
python3 -m unittest discover -s tests -v
```

Schema retrieval needs network access and downloads JSON, not executable upstream code. The cache pins ACS release v0.1.4's commit `834f3f0d51e7bbbd9a68ff682bec89f97ddd72d8`; its wire/schema version is **0.1.0**. The manifest records local file hashes; it is not an independently signed supply-chain attestation. Subsequent fixture/export/test runs use that offline cache. Missing cache files are errors, not skipped tests.

The fixture is an in-process policy function plus an in-memory ledger. It exercises allow, deny and policy-service outage; only the allowed increment reaches the ledger. It does not run the upstream Guardian, call a live policy service or prove production mediation. See the [adapter scope and evidence map](../adoption/acs-evidence-adapter.md).

The exporter accepts a transcript object with `source_kind`, `policy_snapshot_id`, `target_revision` and an `events` array. Each event contains the upstream-shaped `request`, `response` (or null) and an `observation` with boolean `executed`, `outcome` (`succeeded`, `failed` or `blocked`), and `policy_service_error` when a response is absent. The fixture generates an example. For real captures, record the actual observer and production revision; an asserted `captured_acs` label does not authenticate the source.

Exporter exit codes: 0 means all supplied records were dispatch-consistent and policy-version-bound where a response existed; 1 means failed/inconclusive records; 2 means invalid input, missing dependencies/cache or an operational error. Results are written for exit 0 or 1. A pass does not mean every required scenario was supplied or the full I6 invariant holds.

## Canonical Payload Helper

`attestation_payload.py` constructs the signature and anchor input bytes specified by `BRF-JCS-0.1.1`. Tests include a fixed canonical-byte/HMAC vector, tampering and the anchor exclusion rule. HMAC helpers are reference/test support only; they do not implement asymmetric verification, key trust, independent witnessing or anchor resolution. Never reuse the public test key.

## Reproduction Limits

Unit tests test these utilities, not an external deployment. The post-release [alignment pass](../adoption/alignment-implementation.md) adds the native ACS/Inspect readers and real local OPA example below. AgentDojo, OCSF ingestion, live Guardian interoperability, production asynchronous-effect tests and independent assessment remain open.

## Optional Native Integrations (Unreleased)

These require Python 3.11+. The OPA installer supports macOS arm64/x86_64 and Linux aarch64/x86_64. No Docker daemon or model API key is needed.

```sh
bash tools/install-jsonschema-local.sh
bash tools/install-integrations-local.sh
python3 tools/install_opa_local.py
python3 tools/fetch_acs_schemas.py
python3 tools/fetch_acs_trace_assets.py
bash tools/check-alignment-local.sh
```

The optional venv pins Inspect 0.3.283. OPA 1.21.4 is downloaded from its official release and checked against an embedded platform-specific SHA-256. Downloaded code/data stay under ignored `.tools/`; Inspect may also use its normal application-data trace/cache directory. Python direct dependencies are pinned, not the full transitive graph. Installation/fetch needs network; checks use local data and a mock model, with no external model calls.

The check runner executes unit tests and the separate native integration suite, validates repository artifacts and retains fresh evidence under `.tools/alignment-check.*`. Missing optional dependencies are errors, not skipped passes. The added GitHub workflow runs the same commands; its presence is not proof of a successful hosted run.

### Native ACS OTLP

```sh
python3 tools/acs_trace_evidence.py .tools/acs-trace-v0.1.4/sample.jsonl --output .tools/native-acs-evidence.json
```

Pass multiple JSON/JSONL files containing OTLP `ExportTraceServiceRequest.resourceSpans` to join host and Guardian streams. Correlation uses session/request pairs, not trace IDs; tool-result references are session-scoped. Failure events override decision eligibility. Unknown span names carrying ACS decisions/failures are retained as findings. Every record leaves enforcement `not_verified`.

The pinned upstream sample is synthetic and intentionally has findings, so the command writes a schema-valid bundle and returns **1**. Consistent analysis returns 0; invalid input/cache or operational failure returns 2. None means enforcement verified. Output uses `spec/acs-trace-evidence.schema.json`; full ACS-Trace/OTLP conformance and OCSF import are not implemented. Cached manifest hashes are not independent signed attestations.

### Native Inspect Logs

```sh
.tools/integration-env/bin/python tools/run_inspect_demo.py --log-dir .tools/inspect-example-logs --output .tools/inspect-example.json
.tools/integration-env/bin/python tools/inspect_evidence.py PATH_TO_LOG.eval --output .tools/imported-inspect.json --policy-snapshot-id POLICY_ID --target-revision TARGET_REVISION
```

The first command generates a real Inspect `.eval` log for the OPA fixture without LLM generation. The second reads an existing `.eval` or JSON log through Inspect's API. Policy/revision flags can be omitted if declared in `eval.metadata.brf`; disagreements are errors. A missing source kind becomes `supplied_evaluation`, not independently captured production evidence.

Scorers default to `task_success` and `boundary_violation`; select others with `--task-score` and `--violation-score`. Booleans/numeric 0 or 1 are interpreted automatically. String scores require explicit mappings, for example `--task-positive C --task-negative I --violation-positive C --violation-negative I`. The positive violation label must actually mean a violation occurred, not generic correctness. Missing/unsupported scores remain null. Selected scorer `metadata.brf_error: true` marks an error. Cancelled, incomplete, limited or invalidated runs cannot silently pass.

Output uses `spec/evaluation-evidence.schema.json`. Exit 0 means complete boundary scores with no reported violation, not universal safety or task success; 1 means a violation or inconclusive evidence; 2 means input/operational error. Messages, prompts, arbitrary headers and credentials are not copied. Identifiers and selected metadata still need publication/privacy review.

### OPA Comparison

```sh
python3 tools/opa_comparison.py --output .tools/opa-comparison.json
```

Actual Rego queries cover eight fixed cases in `unmediated`, `schema_only` and `opa_enforced` modes. Unsafe baselines make the combined bundle a deliberate finding (exit **1**), while the OPA-gated mode is checked separately by integration tests. `schema_only` is not canonical A2A/MCP. See [the worked example](../examples/opa-boundary/README.md) for exact counts and scope.

New exporters refuse existing output unless `--overwrite` is supplied. ACS/Inspect exporters reject replacing their input even with that flag; the OPA comparison protects its policy, fixture, runner and binary. Unknown planned sample counts remain inconclusive. Evidence is created owner-only, never appended or automatically signed. See the [alignment implementation note](../adoption/alignment-implementation.md) for result interpretation and remaining live/independent tests.
