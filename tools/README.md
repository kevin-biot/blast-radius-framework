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

Unit tests test these utilities, not an external deployment. The published [alignment pass](../adoption/alignment-implementation.md) adds native ACS/Inspect readers and the real local OPA example below. The [live boundary experiments](../adoption/live-boundary-experiments.md) add real Guardian/shim processes and durable local race tests. AgentDojo, OCSF ingestion, full agent-client interoperability, production asynchronous-effect tests and independent assessment remain open.

## Optional Native Integrations

These require Python 3.11+. The OPA installer supports macOS arm64/x86_64 and Linux aarch64/x86_64. No Docker daemon or model API key is needed.

```sh
bash tools/install-jsonschema-local.sh
bash tools/install-integrations-local.sh
python3 tools/install_opa_local.py
python3 tools/install_acs_runtime.py
python3 tools/fetch_acs_schemas.py
python3 tools/fetch_acs_trace_assets.py
python3 tools/fetch_cyclonedx_schemas.py
bash tools/check-alignment-local.sh
```

The optional venv pins Inspect 0.3.283. OPA 1.21.4 is downloaded from its official release and checked against an embedded platform-specific SHA-256. Downloaded code/data stay under ignored `.tools/`; Inspect may also use its normal application-data trace/cache directory. Python direct dependencies are pinned, not the full transitive graph. Installation/fetch needs network; checks use local data and a mock model, with no external model calls.

The check runner executes unit tests and the separate native integration suite, validates repository artifacts and retains fresh evidence under `.tools/alignment-check.*`. Missing optional dependencies are errors, not skipped passes. The v0.5.12 [hosted baseline passed](https://github.com/kevin-biot/blast-radius-framework/actions/runs/40345335934); later workflow changes require their own successful run.

The expanded live/async implementation also [passed hosted CI](https://github.com/kevin-biot/blast-radius-framework/actions/runs/40348621393). Subsequent successful workflow runs retain the five evidence bundles and allowlisted fake-input ACS wire/audit/trace captures for 14 days. The artifact is linked from the workflow run and may require GitHub sign-in to download. Token files, databases and dependency directories are not selected; these uploads are not signed BRF attestations.

### Live Guardian and Asynchronous Effects

```sh
python3 tools/install_acs_runtime.py
python3 tools/run_acs_live.py --run-dir .tools/acs-live-example
python3 tools/run_async_boundary.py --run-dir .tools/async-boundary-example
python3 tools/validate_json_schema.py spec/execution-evidence.schema.json .tools/acs-live-example/evidence.json .tools/async-boundary-example/evidence.json
```

The installer supports macOS arm64 and Linux x86_64. It checks a pinned Bun 1.3.11 archive digest, installs only under `.tools/`, checks out ACS v0.1.4's exact commit and runs its frozen install with lifecycle scripts disabled. It refuses a changed tracked upstream checkout; it never resets user changes. The cached binary digest detects ordinary local replacement, not malicious modification of both binary and local manifest. Third-party native code still executes.

The live runner executes the actual Guardian and shipped hook but not the Claude Code application. A separate HTTP tool durably increments a private ledger; shell proposals are inert strings, never executed commands. Eight cases preserve the default fail-open posture and compare explicit fail-closed, honored denial and deliberate denial bypass. Upstream wire IDs, converted host failure spans and raw-capture digests are retained. The async runner adds eleven receipt-backed retry/budget/revocation cases with atomic enforcement and deliberately stale-check controls. See the [complete task/results note](../adoption/live-boundary-experiments.md).

Both runners require a **new** run directory. Exit 0 means experimental expectations matched, including unsafe negative controls, not a safety pass; 1 means a mismatch; 2 means an operational error. They bind only to loopback and use fresh fixture credentials, no production/model APIs. Observation is same-machine read-only SQLite, not an independent witness. Bundles are unsigned and cannot establish corporate authority, full protocol conformance or a production BR class. Token files are removed on ordinary shutdown; review retained raw artifacts before sharing.

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

The ACS/Inspect/OPA exporters refuse existing output unless `--overwrite` is supplied. ACS/Inspect exporters reject replacing their input even with that flag; the OPA comparison protects its policy, fixture, runner and binary. Unknown planned sample counts remain inconclusive. Their evidence is created owner-only, never appended or automatically signed. Optional DSSE packaging is a separate operation below. See the [alignment implementation note](../adoption/alignment-implementation.md) for result interpretation and remaining live/independent tests.

## DSSE and CycloneDX Companions

Tooling v0.5.14 adds the remaining [portability and inventory tasks](../adoption/evidence-portability-and-inventory.md). Install the integration runtime (including pinned `cryptography` 50.0.2), fetch the pinned CycloneDX schemas, and ensure `openssl` is OpenSSL 3+ rather than LibreSSL. Set `BRF_OPENSSL` to its executable path when necessary. The full check runner produces and verifies two ephemeral-demo-key envelopes; it retains only the public key and removes the temporary private-key directory on ordinary success or exception.

For an existing evidence file and caller-managed unencrypted Ed25519 PEM key:

```sh
.tools/integration-env/bin/python tools/dsse_evidence.py export --evidence EVIDENCE.json --evidence-type execution --private-key SIGNING_KEY.pem --output .tools/evidence.dsse.json
.tools/integration-env/bin/python tools/dsse_evidence.py verify --envelope .tools/evidence.dsse.json --evidence EVIDENCE.json --public-key TRUSTED_PUBLIC_KEY.pem
python3 tools/verify_dsse_openssl.py --envelope .tools/evidence.dsse.json --evidence EVIDENCE.json --public-key TRUSTED_PUBLIC_KEY.pem --openssl openssl
```

Supported evidence types are `acs_trace`, `evaluation`, `execution` and `inventory_links`. This utility is not a production key-management/HSM service; do not put real signing keys in the repository. The signer binds the original subject bytes and nested evidence contents. The public key must be trusted out of band: an envelope's key ID or embedded URL never establishes trust. Primary verify exits 0 for signature/subject integrity, 1 for signature or binding failure, 2 for malformed/unsupported input or operational failure. The separate OpenSSL command returns 1 for any failure and checks integrity/binding, not the complete companion schema. Neither command establishes claim truth, current authorization, key revocation, a trusted timestamp or a BR rating. New DSSE exports always refuse existing output paths.

Validate and link a CycloneDX 1.7 inventory:

```sh
python3 tools/fetch_cyclonedx_schemas.py
python3 tools/cyclonedx_inventory.py examples/cyclonedx/bom.json --mapping examples/cyclonedx/card-map.json --card spec/examples/example-component-card-tool-legal-db.json --profile spec/examples/example-profile-closed-world-br2.json --output .tools/cyclonedx-links.json
python3 tools/validate_json_schema.py spec/inventory-links.schema.json .tools/cyclonedx-links.json
```

The bridge uses the complete official JSON schema set pinned to release 1.7.2, validates offline, refuses unknown remote references and never fetches BOM-Links or endpoints. It projects metadata/top-level/nested components and services, requires reviewed explicit links and exact versions, and resolves each linked card's profile IDs. Other versions/XML are rejected, not converted. Missing dependency declarations, unmapped entries and entries without `bom-ref` remain explicit. The [fictional example](../examples/cyclonedx/README.md) yields four entries and one card link. Exit 0 means inventory/link checks completed, not completeness or reach; errors return 2. Existing output files are never overwritten. File digests and declared links are not identity, permissions or corporate authority.

Successful hosted checks retain the existing fixture artifact plus copied subject evidence, two DSSE envelopes, inventory links and `demo-public.pem` for 14 days. The allowlist does not include private keys. The demo public key is for reproduction only and is not a BRF institutional identity. Original native bundles retain their unsigned/unverified markers even when wrapped in DSSE.

## Signed Credential Boundary

Tooling v0.5.15 adds a separate loopback JWT-protected tool and local issuer fixture, using pinned PyJWT 2.15.1 and Ed25519 keys. It tests issuer, audience, tenant, scope, type/algorithm, expiry, local revocation, scoped idempotency and control-plane separation. See the [34-case task/results guide and OWASP mapping](../adoption/credential-boundary-tests.md). This does not add authentication to the upstream ACS Guardian or implement an external identity provider.

```sh
bash tools/install-integrations-local.sh
.tools/integration-env/bin/python tools/run_credential_boundary.py --run-dir .tools/credential-example
.tools/integration-env/bin/python tools/run_credential_boundary.py --run-dir .tools/credential-example --check-only
python3 tools/validate_json_schema.py spec/execution-evidence.schema.json .tools/credential-example/evidence.json
python3 tools/validate_json_schema.py spec/credential-context.schema.json .tools/credential-example/credential-context.json
```

Run mode requires a new directory. Check-only mode starts no service and checks bounded file snapshots, capture/key bindings, schemas, receipt correlation and internal accounting; it rejects arbitrary capture paths and symbolic-link files. Neither mode authenticates the observer or establishes external authority. Exit 0 means all predeclared experimental outcomes matched, including unsafe controls; 1 means an experimental mismatch; 2 means invalid input or operational failure.

Credential execution uses companion format 0.1.1; existing ACS/async 0.1.0 bundles remain valid, and profile spec 0.1.1 is unchanged. The execution bundle hash-binds its context/public-key captures and can use the existing DSSE `execution` exporter. DSSE verification does not automatically resolve capture files; validate the explicit packet separately. The standard projection totals both tenants, while the context retains the per-tenant/principal/client receipt identities. Resource-grant `active` is not token validity.

The full check runner executes these tests and retains `credential-boundary/evidence.json`, `credential-context.json` and `issuer-public.pem` through the explicit CI allowlist. No JWT or private signing key is written to those exports; fixture-admin secret files are removed on ordinary shutdown. The local issuer is an in-memory test signer, not a company trust anchor. Bearer reuse, real identity proof, holder binding, provider federation, distributed revocation and corporate/legal mandate are not solved by these checks.
