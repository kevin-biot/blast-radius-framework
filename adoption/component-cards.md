# Component Cards

*Proposed BRF-native card formats for documenting the components that sit underneath a system-level BR profile.*

**Gap addressed:** missing component-card layer
**Status:** design note
**Date:** 2026-04-23

---

## 1. Why component cards exist

A BR profile describes the **system as rated**. Component cards describe the **parts that make that rating possible to audit**.

This fills the documentation layer between:

- narrative architecture description
- full system profile
- raw evidence artefacts

Component cards should make it easier to answer questions like:

- which model is this system actually using?
- which corpus or dataset can influence it?
- which tool can it call?
- which external dependency changes the system's reach or coupling?
- how is evidence for this component signed or anchored?

---

## 2. Card types

Minimum card set:

1. **Model card**
2. **Dataset / corpus card**
3. **Tool / integration card**
4. **Dependency attestation card**
5. **Evidence / anchor card**

Each card type should be linkable from a future BR profile or attestation bundle.

---

## 3. Common fields

Every card should include:

- `card_type`
- `card_id`
- `component_name`
- `version`
- `owner`
- `status`
- `last_reviewed_at`
- `related_profile_ids`
- `evidence_refs`
- `limits`

These common fields keep the card family consistent.

---

## 4. Per-card minimum fields

### 4.1 Model card

Minimum extras:

- provider
- model family and release
- execution role in the system
- allowed authority class
- known failure modes
- update cadence
- prompt / context boundary notes
- adversarial exposure notes

### 4.2 Dataset / corpus card

Minimum extras:

- source type
- provenance
- collection basis
- consent / licence basis
- deletion and retention semantics
- jurisdictions represented
- principal populations affected
- known bias or coverage limits

### 4.3 Tool / integration card

Minimum extras:

- tool identity
- target system touched
- read/write capability
- action-class ceiling
- parameter constraints
- auth model
- rollback semantics
- logging and replay support

### 4.4 Dependency attestation card

Minimum extras:

- external vendor or deployer
- dependency type
- worldview
- reach contribution
- coupling contribution
- upstream attestation reference
- expiry or review cadence

### 4.5 Evidence / anchor card

Minimum extras:

- evidence type
- signing method
- anchor type
- resolver / verifier details
- retention policy
- independent verification path

---

## 5. Relationship to existing documentation patterns

These cards should borrow the best habits from:

- Model Cards
- Datasheets for Datasets
- governance factsheets

But they should remain BRF-shaped:

- architecture and composition aware
- attestation aware
- operationally scoped

The objective is not to create another generic documentation family. The objective is to create the documentation layer BRF needs for deployers, auditors, and underwriters.

---

## 6. Suggested publication format

Phase 1 can be simple Markdown plus frontmatter. Example:

```yaml
card_type: tool
card_id: tool-sapp-regulator-api-v1
component_name: SAPP regulator verification API
version: 1.0
owner: Lane2
status: active
last_reviewed_at: 2026-04-23
related_profile_ids:
  - lane2-public-observable-v1
```

Then prose sections below the frontmatter.

An initial machine-readable schema now exists in [`../spec/component-card.schema.json`](../spec/component-card.schema.json), with the companion note in [`../spec/component-card-format.md`](../spec/component-card-format.md).

---

## 7. Why this closes the gap

The gap was the lack of a clean component-documentation layer between full BR profiles and raw evidence.

These card types close that by defining:

- what components need documenting
- what the minimum fields are
- how the cards connect to BR profiles and attestations

The schema and spec note in [`../spec/`](../spec/) make the first machine-readable version real rather than only proposed.
