# Component Card Format

*Machine-readable documentation cards for the components that sit underneath a Blast Radius Framework profile or attestation.*

**Spec version:** 0.1.1
**Date:** 2026-10-26
**For framework version:** 0.5

---

## Why this file exists

`br-profile.schema.json` describes the **rated system**.

`component-card.schema.json` describes the **parts that make that system easier to audit**:

- model components
- datasets and retrieval corpora
- tools and integrations
- external dependencies
- evidence and anchor mechanisms

The objective is to fill the documentation layer between high-level BR profiles and raw evidence artefacts.

---

## Files

| File | Purpose | Status |
|---|---|---|
| `component-card.schema.json` | JSON Schema for a single component card. Supports five card types: model, dataset/corpus, tool/integration, dependency attestation, and evidence/anchor. | v0.1 |
| `examples/example-component-card-tool-legal-db.json` | Worked example of a tool/integration component card linked to the closed-world BR-2 example profile. | Worked example |

---

## How to use

### As a deployer

1. Produce one component card per material component that affects authority, reach, coupling, reversibility, consequence, observability, or evidence verification.
2. Link the card to the relevant BR profile via `related_profile_ids`.
3. Preserve evidence references in `evidence_refs` so auditors can follow from card to artefact.
4. Keep the card updated when the component or its risk posture changes.

### As an auditor or underwriter

1. Read the BR profile first.
2. Retrieve the component cards for any model, tool, dependency, or evidence mechanism that materially affects the rating.
3. Confirm that the component-card claims align with the profile, attestation, and observed evidence.

### Profile linking guidance

The minimum linking pattern is:

1. the profile names the rated system and its components
2. the component card lists the relevant `related_profile_ids`
3. reports or attestations point to the card where a reviewer needs component-level detail

An initial example card is included at [`examples/example-component-card-tool-legal-db.json`](./examples/example-component-card-tool-legal-db.json). It links to the closed-world BR-2 worked example via `related_profile_ids: ["example-br2-closed-world-001"]`.

---

## Authority and Delegation Context

The optional `authority_context` object separates externally supplied mandate evidence from technical delegation. It records `mandate_source` and its accountable owner, `principal_id`, `agent_id`, `audience`, `delegated_scopes`, `expires_at`, `policy_snapshot_id`, `revocation_check`, optional parent-delegation evidence and explicit limits.

A supplied mandate reference is not proof of its legal validity. A successful revocation check must include a timestamp and evidence reference; it is not a promise of continuing validity. Admission must still enforce current scope, expiry, revocation and policy at the execution boundary. Do not put bearer tokens or secrets in cards.

The fictional legal-database example deliberately declares `mandate_source.status: not_established` and `revocation_check.status: not_checked`. It grants nothing. Its profile link resolves to the existing example; the example is not a current re-attestation.

These fields align with questions raised by [NIST's agent identity work](https://www.nist.gov/news-events/news/2026/09/comments-software-and-agentic-ai-identity-concept-paper) and [WIMSE AIMS draft-00](https://datatracker.ietf.org/doc/html/draft-ietf-wimse-aims-00). They do not claim conformance to either. AIMS here means Agent Identity Management System, not the ISO/IEC 42001 management system.

## Design principles

**System-aware, not generic.** These cards are not a replacement for Model Cards or Datasheets for Datasets. They are BRF-shaped documentation forms that connect components to system-level blast-radius claims.

**Minimal but linkable.** The schema captures the minimum structured fields needed to reference cards from profiles, reports, and attestations. Richer prose can live in Markdown or external documentation as long as the structured card remains stable.

**Card types are intentionally narrow.** The five initial types match the minimum set needed for BRF adopters:

- `model`
- `dataset_corpus`
- `tool_integration`
- `dependency_attestation`
- `evidence_anchor`

---

## What the schema does not do

- It does not compute BR classes.
- It does not substitute for the profile schema.
- It does not provide cryptographic attestation on its own.
- It does not replace domain-specific documentation standards.

It makes those things easier to connect and verify.

---

## Recommended first use

The highest-value first cards are:

1. one tool/integration card for each write-capable tool
2. one dependency-attestation card for each external vendor dependency
3. one evidence/anchor card for the evidence-verification path

That sequence captures the components most likely to change blast radius or attestation credibility.

## Validation

Use the repo-local validator after installing it once:

1. `./tools/install-jsonschema-local.sh`
2. `python3 ./tools/validate_json_schema.py --check-repository`

This resolves card/profile IDs as well as checking structure and supported formats. Runtime expiry, revocation, evidence truth and legal authority are not verified. The runtime is local under ignored `.tools/`; see [utility limits](../tools/README.md).
