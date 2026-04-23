# Crosswalks Roadmap

*Publishing plan for translating BRF into adjacent governance and assurance regimes.*

**Gap addressed:** missing public crosswalks
**Status:** roadmap
**Date:** 2026-04-23

---

## 1. Why crosswalks matter

BRF is strongest when read on its own terms. Many buyers, auditors, and regulators do not start there.

They start from:

- NIST AI RMF
- ISO/IEC 42001
- the EU AI Act
- specialist-underwriter published criteria

Crosswalks are therefore not optional packaging work. They are translation infrastructure.

---

## 2. Priority order

### 2.1 First crosswalk — NIST AI RMF

Why first:

- widely recognised
- process-shaped rather than architecture-shaped
- useful for showing exactly what BRF adds rather than duplicates

Target output:

- matrix from BRF axes / invariants / modifiers into RMF functions and categories
- short note on where BRF is narrower, stricter, or simply orthogonal

Status:

- initial delivery now published in [`crosswalk-nist-ai-rmf.md`](./crosswalk-nist-ai-rmf.md)

### 2.2 Second crosswalk — ISO/IEC 42001

Why second:

- many organisations need management-system alignment for purchasing and assurance

Target output:

- mapping from BRF evidence expectations into ISO 42001 control and management-system language

Status:

- initial delivery now published in [`crosswalk-iso-42001.md`](./crosswalk-iso-42001.md)

### 2.3 Third crosswalk — EU AI Act

Why third:

- directly relevant to European deployers
- BRF already positions itself against Articles 12, 15, 19, 26(6), and 72

Target output:

- mapping from BR class, `K` sub-tag, invariants, and attestation evidence into likely obligations and evidence requests

Status:

- initial delivery now published in [`crosswalk-eu-ai-act.md`](./crosswalk-eu-ai-act.md)

### 2.4 Fourth crosswalk — specialist underwriters

Why fourth:

- highly valuable commercially
- best done after the three broader public-regime crosswalks are published

Target output:

- mapping from BRF evidence and invariants into published criteria from Munich Re aiSure, AIUC-1, and Armilla / Lloyd's style requirements

Status:

- initial delivery now published in [`crosswalk-specialist-underwriters.md`](./crosswalk-specialist-underwriters.md)

---

## 3. Common output shape

Every crosswalk should contain:

1. **scope statement**
2. **mapping table**
3. **non-equivalence note**
4. **what BRF adds**
5. **what BRF does not attempt to replace**

Without the non-equivalence note, crosswalks get misread as substitution claims.

---

## 4. Recommended source material

For every crosswalk, use:

- [`../framework.md`](../framework.md)
- [`../NOTATION.md`](../NOTATION.md)
- [`../insurability.md`](../insurability.md)
- [`../spec/README.md`](../spec/README.md)
- [`../spec/attestation-format.md`](../spec/attestation-format.md)
- [`../reports/lane2/`](../reports/lane2/) as the worked example layer

That ensures the crosswalks connect theory, notation, machine-readable form, and reporting artefacts.

---

## 5. First concrete deliverables

Suggested deliverable sequence:

1. `crosswalk-nist-ai-rmf.md` — completed in this directory
2. `crosswalk-iso-42001.md` — completed in this directory
3. `crosswalk-eu-ai-act.md` — completed in this directory
4. `crosswalk-specialist-underwriters.md` — completed in this directory

Each should be publishable as a standalone note.

---

## 6. Why this closes the gap

The gap was not the lack of adjacent frameworks. The gap was the lack of a public translation layer from BRF into those frameworks.

This roadmap closes that by defining:

- which crosswalk to do first
- what each crosswalk should contain
- how to avoid substitution confusion
