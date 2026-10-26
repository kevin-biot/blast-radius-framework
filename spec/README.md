# Blast Radius Framework — Conformance Specification

*Machine-readable artefacts that make the framework adoptable, not just readable.*

**Spec version:** 0.1.1 (backward-compatible schema additions; explicit signing profile for new attestations)
**Date:** 2026-10-26
**For framework version:** 0.5

---

## Why this directory exists

`framework.md` describes the rating framework in prose. This is the spec. An auditor, deployer, underwriter, or regulator working against this directory can:

- Validate a BR profile against a JSON Schema (`br-profile.schema.json`)
- Validate a BRF component card against a JSON Schema (`component-card.schema.json`)
- Run a defined conformance test per architectural invariant (`invariant-conformance-tests.md`)
- Produce a signed, anchored, third-party-verifiable attestation (`attestation-format.md`)
- Compare against two worked examples (`examples/`)

The spec defines forms and test procedures. The [local utilities](../tools/README.md) provide validation, canonical-payload helpers and an ACS-shaped fixture, not a production enforcement runtime or general conformance harness.

---

## Contents

| File | Purpose | Status |
|---|---|---|
| `br-profile.schema.json` | JSON Schema (draft 2020-12) for BR profiles, with explicit new signing profile and PS256 option. | v0.1.1; legacy examples retained |
| `component-card.schema.json` | JSON Schema for five card types with optional structured authority context. | v0.1.1; older cards remain valid |
| `invariant-conformance-tests.md` | Per-invariant empirical test specifications. Each test has an ID, procedure, pass criterion, and BR-class applicability. | v0.1 — 7 invariants × 3-4 tests each |
| `attestation-format.md` | Signed + anchored attestation format with explicit BRF-JCS-0.1.1 signature input. | v0.1.1; legacy input construction must be declared |
| `component-card-format.md` | Profile linking plus separate organisational-mandate and technical-delegation context. | v0.1.1; additive fields |
| `acs-evidence.schema.json` | Observed decision/dispatch bundle for the version-pinned ACS adapter. | Local fixture tested; not ACS certification |
| `examples/example-component-card-tool-legal-db.json` | Worked example of a tool/integration component card linked to the closed-world BR-2 example profile. | Worked example |
| `examples/example-profile-closed-world-br2.json` | A worked example of a closed-world BR-2 profile (legal citation review assistant). All invariants hold; cardinal score computed. | Worked example |
| `examples/example-profile-open-world-br4.json` | A worked example of an open-world BR-4 profile (three-agent NL-coupled research assistant). Invariants mostly fail; cardinal score null. | Worked example showing how failure looks |

---

## How to use

### As a deployer claiming a BR rating

1. Read `framework.md` to understand the six axes, seven invariants, and composition rule.
2. Run the relevant tests from `invariant-conformance-tests.md` against your system. Record the results.
3. Populate a profile using `br-profile.schema.json`. Validate the JSON against the schema.
4. Sign and anchor the profile per `attestation-format.md`.
5. Publish the attestation at a stable URI; include it in vendor questionnaires, RFP responses, insurance submissions, and regulatory filings.

### Local validation utility

Run from the repository root:

```sh
bash tools/install-jsonschema-local.sh
python3 tools/validate_json_schema.py --check-repository
```

This checks schema/format validity and declared reference/semantic rules, including component-card profile links. It does not verify freshness, complete BR arithmetic, signatures, anchors or runtime behaviour. See [tool commands and limits](../tools/README.md) for individual validation, ACS setup and tests. Local dependencies and upstream schema caches stay in ignored `.tools/`.

### As an auditor verifying a BR rating

1. Retrieve the attestation.
2. Validate against `br-profile.schema.json`.
3. Run the verification procedure in `attestation-format.md §4`.
4. For at least one test per invariant, re-run the test and confirm the result.
5. Independently recompute the ordinal class. If an experimental cardinal score is claimed, obtain its normalization, observations, estimator state and calibration; it cannot be reconstructed from tier labels alone.
6. Issue a findings report with any failures documented per step.

### As an underwriter reviewing a BR packet

1. Verify the attestation and inspect its actual deployment scope and unresolved findings.
2. Obtain product-specific exposure, incident, loss and control-test evidence.
3. Treat any cardinal score/covariance as experimental; require calibration before considering it as an input to a loss model.
4. Determine appetite, wording, limits and price separately. BR class and signatures do not establish coverage.

### As a regulator assessing a deployment

1. Retrieve the attestation.
2. Verify signature and anchor.
3. Read invariants and test results.
4. Confirm the `K` sub-tag matches your regulatory mandate.
5. Request re-runs of any test the attestation claims passed.

---

## Design principles

**Forms, not implementations.** The spec prescribes what an attestation looks like. How you produce one is your choice: your CI, your attestation service, your HSM. Multiple implementations are expected and welcomed.

**Honesty is machine-checkable.** A deployer filling out this schema honestly has no advantage over one filling it out dishonestly *unless* the attestation is verified against actual system behaviour. The test specifications in `invariant-conformance-tests.md` are what make self-attestation verifiable.

**Composition is first-class.** The `composition` object and its `topology` field are required. You cannot claim a BR rating without naming how your components compose; the mathematical models in `framework.md §7.2` require explicit independence, containment and exposure assumptions.

**Component documentation is linkable.** Component cards provide a structured documentation layer for the models, datasets, tools, dependencies, and evidence mechanisms that sit underneath a BR profile. They do not replace the profile; they make it easier to audit.

**Open-world is marked, not hidden.** The `components[].worldview` field is required. Any open-world component forces BR-4 minimum per `framework.md §4.0`. Deployers cannot claim BR-2 or BR-3 with open-world substrate regardless of how they paint other axes.

**Cardinal scores are experimental and optional.** Require normalization, calibration and reproducible estimator inputs for a numerical claim. BR class and index covariance do not establish coverage, underwriting acceptance or a premium. See the [claims policy](../adoption/claims-and-evidence.md).

**Independent anchors support integrity, not truth.** BRF requires anchoring for BR-4+ attestations. Check the anchor and trust model independently; neither signatures nor anchors prove the asserted behaviour.

---

## What this spec does not yet cover

- **Third-party certification.** A deployer signs their own attestation here. A stronger form (an independent auditor counter-signing) is a v0.2 item.
- **Revocation.** Once an attestation is published, there is no specified mechanism to revoke it before `attestation_expiry`. A CRL- or OCSP-like mechanism is a v0.2 item.
- **Reference test harness.** The test procedures are prose. A language-agnostic test harness that reads a runner manifest and produces signed results is a candidate for a separate companion repository.
- **Automated questionnaire → profile conversion.** `framework.md §17` is a prose questionnaire; converting a filled questionnaire into a valid profile is useful tooling and v0.2.
- **Batch attestation semantics.** When a deployer publishes many attestations, they may batch under a single anchor. Merkle inclusion semantics are standard but not yet specified here.

These are open work, not promised delivery or evidence of real-world adoption. See the [update worklist](../adoption/update-worklist-2026-10.md).

---

## Versioning

Spec 0.1.1 accompanies framework 0.5.11 and is included in the repository tag `v0.5.11`. Additive fields retain legacy 0.1 profiles; new JSON signatures use the explicit 0.1.1 payload profile. Historical examples are not re-signed by schema validation. Normative I1/worldview changes are reserved for a versioned revision.

The JSON Schema's `$id` includes the schema filename without a version in the URL, but the `schema_version` field inside a profile identifies the schema version the profile conforms to. This permits evolution without URL churn.

---

## Contributing

Field-level review is especially welcome on `br-profile.schema.json`. Implementations will surface ambiguities and missing fields; issues and pull requests are the right place for them.

Corrections to `invariant-conformance-tests.md` (procedure improvements, edge cases, missing tests) are welcomed. Test IDs are stable; new tests add new IDs.

Additions to `examples/` showing real (or realistic) profiles from different verticals (clinical, financial, operational, research) help the spec mature. Examples should use fictional organisations and illustrative values.
