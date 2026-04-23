# Blast Radius Framework — Conformance Specification

*Machine-readable artefacts that make the framework adoptable, not just readable.*

**Spec version:** 0.1
**Date:** 2026-04-23
**For framework version:** 0.5

---

## Why this directory exists

`framework.md` describes the rating framework in prose. This is the spec. An auditor, deployer, underwriter, or regulator working against this directory can:

- Validate a BR profile against a JSON Schema (`br-profile.schema.json`)
- Validate a BRF component card against a JSON Schema (`component-card.schema.json`)
- Run a defined conformance test per architectural invariant (`invariant-conformance-tests.md`)
- Produce a signed, anchored, third-party-verifiable attestation (`attestation-format.md`)
- Compare against two worked examples (`examples/`)

The spec is intentionally minimal. It specifies forms, not implementations. Reference implementations will arrive as separate repositories once the form is stable.

---

## Contents

| File | Purpose | Status |
|---|---|---|
| `br-profile.schema.json` | JSON Schema (draft 2020-12) for a complete BR profile — the data shape a deployer produces. | v0.1 — shape complete; open for field-level review |
| `component-card.schema.json` | JSON Schema (draft 2020-12) for BRF component cards covering models, datasets/corpora, tools/integrations, dependencies, and evidence/anchor mechanisms. | v0.1 — initial component-documentation layer |
| `invariant-conformance-tests.md` | Per-invariant empirical test specifications. Each test has an ID, procedure, pass criterion, and BR-class applicability. | v0.1 — 7 invariants × 3-4 tests each |
| `attestation-format.md` | Signed + anchored attestation format. Canonical serialisation (JCS), signature algorithms, anchor types, verification procedure. | v0.1 — algorithms, procedures, skew tolerances |
| `component-card-format.md` | Companion note explaining how component cards relate to BR profiles and attestations. | v0.1 |
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

### As an auditor verifying a BR rating

1. Retrieve the attestation.
2. Validate against `br-profile.schema.json`.
3. Run the verification procedure in `attestation-format.md §4`.
4. For at least one test per invariant, re-run the test and confirm the result.
5. Recompute the ordinal class and cardinal score; confirm agreement with declared values.
6. Issue a findings report with any failures documented per step.

### As a specialist underwriter pricing a BR rating

1. Retrieve the attestation.
2. Verify per the auditor procedure.
3. Extract `aggregation.cardinal_score.B_hat` and `sigma_B` as the actuarial point estimate and uncertainty.
4. Map `K` sub-tag to the relevant regulatory regime for pricing the severity σ.
5. Apply your own actuarial priors on frequency λ per composition topology (§7.2).
6. Quote.

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

**Composition is first-class.** The `composition` object and its `topology` field are required. You cannot claim a BR rating without naming how your components compose; you cannot name a composition without it forcing the mathematics per `framework.md §7.2`.

**Component documentation is linkable.** Component cards provide a structured documentation layer for the models, datasets, tools, dependencies, and evidence mechanisms that sit underneath a BR profile. They do not replace the profile; they make it easier to audit.

**Open-world is marked, not hidden.** The `components[].worldview` field is required. Any open-world component forces BR-4 minimum per `framework.md §4.0`. Deployers cannot claim BR-2 or BR-3 with open-world substrate regardless of how they paint other axes.

**Cardinal score is optional but increasingly demanded.** BR-1 through BR-3 attestations may omit `cardinal_score`. BR-4+ insurability claims require it. Without the cardinal score, specialist underwriters have no υ variable to price; they will either decline to quote or apply a conservative default.

**Anchoring is non-optional above BR-4.** A signed attestation without an independent anchor is a self-assertion. An underwriter or regulator accepting one is accepting risk they cannot independently verify.

---

## What this spec does not yet cover

- **Third-party certification.** A deployer signs their own attestation here. A stronger form (an independent auditor counter-signing) is a v0.2 item.
- **Revocation.** Once an attestation is published, there is no specified mechanism to revoke it before `attestation_expiry`. A CRL- or OCSP-like mechanism is a v0.2 item.
- **Reference test harness.** The test procedures are prose. A language-agnostic test harness that reads a runner manifest and produces signed results is a candidate for a separate companion repository.
- **Automated questionnaire → profile conversion.** `framework.md §17` is a prose questionnaire; converting a filled questionnaire into a valid profile is useful tooling and v0.2.
- **Batch attestation semantics.** When a deployer publishes many attestations, they may batch under a single anchor. Merkle inclusion semantics are standard but not yet specified here.

All of the above are tracked in `framework.md §19` open questions and will arrive as separate commits once the v0.1 form has had real-world use.

---

## Versioning

Spec versions track framework versions. Spec v0.1 is the machine-readable companion to framework v0.5; spec v0.2 will accompany framework v0.6 or a material additions to the spec itself.

The JSON Schema's `$id` includes the schema filename without a version in the URL, but the `schema_version` field inside a profile identifies the schema version the profile conforms to. This permits evolution without URL churn.

---

## Contributing

Field-level review is especially welcome on `br-profile.schema.json`. Implementations will surface ambiguities and missing fields; issues and pull requests are the right place for them.

Corrections to `invariant-conformance-tests.md` (procedure improvements, edge cases, missing tests) are welcomed. Test IDs are stable; new tests add new IDs.

Additions to `examples/` showing real (or realistic) profiles from different verticals (clinical, financial, operational, research) help the spec mature. Examples should use fictional organisations and illustrative values.
