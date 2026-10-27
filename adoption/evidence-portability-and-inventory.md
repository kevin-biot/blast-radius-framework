# Evidence Portability and Component Inventory

**Date:** 2026-10-27
**Package:** Tooling v0.5.14; framework definitions 0.5.11 and profile spec 0.1.1 unchanged

This implements the remaining two tasks from the [live-boundary work list](./live-boundary-experiments.md). It makes evidence easier to exchange and supporting components easier to find. It does not promote an inventory into a runtime boundary or a signature into an organizational mandate.

The subsequent [v0.5.15 credential-boundary experiment](./credential-boundary-tests.md) adds issuer/audience/tenant/scope/expiry/revocation tests. Its execution-companion 0.1.1 bundle remains exportable through the existing DSSE `execution` predicate; source observations and external authority are still not verified by signing.

## Task List

| Task | Acceptance Criteria | Implemented and Tested | Still Outside Scope |
|---|---|---|---|
| 4. DSSE/in-toto evidence | Package a real evidence bundle, bind original bytes, verify an asymmetric signature through a separate path and reject tampering | Ed25519 DSSE export; one-subject in-toto Statement v1 with custom BRF predicate; explicit trusted-key verification; separate stdlib/OpenSSL CLI; negative tests; ephemeral-key demo | Trusted signer identity, HSM integration, key discovery/rotation/revocation, threshold trust, timestamps, anchors, evidence truth and native BR-profile signature verification |
| 5. CycloneDX links | Validate a real-format BOM, explicitly map entries to valid cards/profiles, retain gaps and reject bad references | Full pinned 1.7 schema with all external schema references cached offline; explicit sidecar links; exact versions and file digests; visible unmapped/unaddressable entries; negative tests | Runtime reach, permission grants, corporate authority, deployed identity, inventory completeness, CycloneDX signature verification and a BR classification |

## Evidence Packaging

`tools/dsse_evidence.py` packages the four supported companion bundle types: native ACS trace analysis, evaluation evidence, execution evidence and inventory links. It validates the supplied file before packaging. The custom [predicate specification](../spec/predicates/evidence-v1.md) preserves the bundle contents and binds the original file's exact bytes by SHA-256. Reformatting the subject file invalidates that binding. Unknown or inconclusive native observations remain unknown or inconclusive after signing.

The implementation follows [DSSE protocol 1.0.2](https://github.com/secure-systems-lab/dsse/blob/b531b787bb3e5f0c3e1c19cee84da1c5d569b061/protocol.md) and [in-toto Statement v1](https://github.com/in-toto/attestation/blob/df02077bf97218a8860a5c534eff1f1381f56984/spec/v1/statement.md), pinned to attestation release v1.2.0. It uses Ed25519 via pinned `cryptography` 50.0.2. The signature covers the original serialized payload and its media type through DSSE pre-authentication encoding; it is **not** a JCS signature. The existing BRF-JCS-0.1.1 format and HMAC payload helper are unchanged.

Verification requires a public key explicitly selected by the caller. An envelope's `keyid`, embedded key, URL or other hint never selects a trusted key. Standard/URL-safe and padded/unpadded base64 are accepted; duplicate JSON keys and malformed encodings are rejected. The bounded reader accepts up to 32 signature entries but implements only one valid signature against one supplied key, not multi-key threshold authorization. It verifies bytes before parsing the statement and never re-reads the envelope to obtain the payload.

The separate `tools/verify_dsse_openssl.py` uses only Python's standard library and an OpenSSL 3+ CLI. It imports neither the signer nor Python `cryptography`. It independently constructs the pre-authentication bytes and checks the signature and subject/predicate binding. Full companion-schema validation belongs to the primary verifier and the check runner; the OpenSSL path is not a replacement for that step. Both paths can share underlying OpenSSL cryptography, and both run under the same user's machine. This is an independently executable verification path, **not independent assessment or necessarily an independently developed cryptographic primitive**. See the [OpenSSL operation](https://docs.openssl.org/3.6/man1/openssl-pkeyutl/) and [Ed25519 API](https://cryptography.io/en/50.0.2/hazmat/primitives/asymmetric/ed25519/) documentation.

The demo generates an ephemeral Ed25519 key, labels its signed statements `ephemeral_demo_key`, verifies both an execution bundle and an inventory-link bundle, and removes its temporary private-key directory on ordinary success or exception. It retains the public key for reproducing verification. A public key supplied alongside a self-signed demo is not evidence of BRF's institutional signing identity. A successful check says nothing about the signer's authorization, freshness, observation completeness, legal authority, insurance outcome or production safety.

## CycloneDX Bridge

The bridge pins [CycloneDX schema release 1.7.2](https://github.com/CycloneDX/specification/tree/349314a9d7671d7d2ca5b711a725f49a73979da6), commit `349314a9d7671d7d2ca5b711a725f49a73979da6`, whose BOM `specVersion` is **1.7**. It supports JSON 1.7 only; it does not silently upgrade older BOMs or parse XML. The fetcher caches the BOM schema, SPDX schema, JSF schema, cryptography definitions and license. Subsequent validation is offline; unknown remote schema references fail instead of being fetched. Local manifest hashes detect changed cached files, not malicious replacement of both cache and manifest or an independently signed supply chain.

The projection includes the metadata root component and top-level/nested components and services. It does not flatten pedigree, formulation or model datasets into claimed deployed components. Full input schema validation still applies to those other sections. Local dependency references outside this projected inventory are rejected rather than silently resolved into runtime components. External BOM-Links in the dependency graph are listed but never fetched. Other external references remain in the source BOM and are not independently resolved.

Explicit sidecar entries map a local `bom-ref` to a supplied `card_id`. Each mapped entry must have an exact, nonempty version matching the card. Cards and profiles are schema-validated, profile IDs resolve locally, and file digests bind the particular inputs. This binds document revisions, not the identity or actual deployment of a named component. Name similarity, purls and declared dependency edges do not automatically create links or BRF composition edges.

The fictional [worked example](../examples/cyclonedx/README.md) contains four entries. One service maps to the existing fictional legal-database card and its historical closed-world profile; two entries remain unmapped and one lacks a `bom-ref`. Missing dependency declarations remain distinguishable from supplied declarations, and unlisted entities are not treated as dependency-free. No card, profile rating or authority context is synthesized from inventory.

## Reproduction

After installing the existing local validation/integration runtimes and pinned ACS/OPA assets, add:

```sh
python3 tools/fetch_cyclonedx_schemas.py
bash tools/check-alignment-local.sh
```

The full runner creates fresh live/async evidence, performs the portability demo, validates its output schemas and retains artifacts under a new ignored `.tools/alignment-check.*` directory. Its successful CI run also uploads an explicit fixture-only allowlist for 14 days: existing captures plus copied subject evidence, two DSSE envelopes, inventory links and the **demo public key only**. No private-key path, production key, bearer token, database or dependency tree is selected. Review identifiers and metadata before sharing non-fixture captures.

The [utility instructions](../tools/README.md) include standalone importer, exporter and both verifier commands. Inventory success means schema/link checks completed, not runtime coverage. Signature success means integrity against the caller-selected key and supplied subject bytes, not evidence truth. Unsupported inputs and operational failures never become skipped passing tests.

## Change Control

**Local verification, 2026-10-27:** `bash tools/check-alignment-local.sh` passed 44 base tests and 45 integration tests (89 total) on macOS arm64 / Python 3.14.3, including 13 DSSE/CLI/demo checks and 12 CycloneDX checks. Both demo envelopes verified through Python and the separate OpenSSL 3.6.5 path. Existing live/async outcomes and profile/card validation remained unchanged. All generated output schemas validated. Python compilation, shell syntax and workflow YAML checks passed; the fixture allowlist selected exactly 20 files and no private-key path. Relative-link checks found no new broken links; five historical changelog references predate this package.

The package is additive tooling with a new custom predicate and companion schemas. Existing framework definitions, class floors, profiles, native attestation signatures and component cards are unchanged. The unrelated DAREB note is neither edited nor staged. Hosted verification is recorded after publication, separately from local results.
