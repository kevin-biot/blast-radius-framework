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

Unit tests test these utilities, not an external deployment. Inspect/AgentDojo importers, OpenTelemetry instrumentation, live ACS interoperability, production asynchronous-effect tests and independent assessment remain open in the [update worklist](../adoption/update-worklist-2026-10.md).
