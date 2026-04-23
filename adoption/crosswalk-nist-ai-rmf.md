# BRF Crosswalk to NIST AI RMF

*First translation note from the Blast Radius Framework into the NIST Artificial Intelligence Risk Management Framework.*

**Status:** Initial crosswalk
**Date:** 2026-04-23
**Primary sources:** [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1), [AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/), [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook), [NIST AI 600-1 Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)

---

## 1. Purpose

This note answers a practical question:

> If an organisation already works in NIST AI RMF terms, where does BRF fit?

Short answer:

- **NIST AI RMF** is a voluntary, process-oriented AI risk management framework organised around **Govern, Map, Measure, and Manage**
- **BRF** is an architecture-first system classifier focused on operational blast radius, attestation shape, and insurability-relevant evidence

They are complementary, not interchangeable.

---

## 2. What NIST AI RMF says at a high level

Per NIST AI RMF 1.0 and the AI RMF Core:

- the Core is composed of four functions: **Govern, Map, Measure, Manage**
- **Govern** is cross-cutting and is intended to be infused throughout the other three functions
- the functions are not a checklist and not necessarily an ordered series of steps
- risk management is continuous across the AI lifecycle

The official playbook and related AIRC material make the framework more actionable, but the center of gravity remains process, organizational culture, and lifecycle risk management.

This matters because BRF is not trying to replace that layer. BRF adds a stricter answer to a narrower question:

> How far can this deployed system's unintended impact propagate, under what architecture, with what evidence shape?

---

## 3. Non-equivalence note

This crosswalk is **not** a claim that:

- a BR class satisfies the NIST AI RMF
- the NIST AI RMF yields a BR class
- one framework can be substituted for the other

The correct relationship is:

- NIST AI RMF gives the broader risk-management operating frame
- BRF gives a deployable-system blast-radius classifier and attestation form inside that frame

---

## 4. High-level mapping

| BRF element | Closest NIST AI RMF function(s) | Relationship | What BRF adds |
|---|---|---|---|
| `A–R–C–V–K–O` tuple | Map, Measure, Manage | Maps and measures operational characteristics relevant to deployment context | A compact, rateable system tuple rather than broad process outcomes |
| Closed-world vs open-world pre-rating gate | Map | Fits NIST's emphasis on context, scope, and intended use | A hard architectural boundary with BR-floor implications |
| Composition topology (`T1`-`T4`) | Map, Measure | Relates to system context, interaction, and emergent risk | Explicit composition mathematics and topology classes |
| Interaction overrides | Measure, Manage | Formalize how combined conditions raise effective risk | Operational class-promotion rules rather than narrative escalation |
| Seven architectural invariants | Govern, Measure, Manage | Correspond to governance, testing, monitoring, and control expectations | Concrete structural properties required for a credible BR claim |
| Anti-pattern catalogue | Map, Measure | Helps identify known risk-expanding designs | Named negative reference catalogue tied directly to blast-radius damage |
| Signed and anchored attestation | Govern, Measure, Manage | Aligns with documentation, monitoring, and evidence practices | A verifiable attestation form for auditors, underwriters, and regulators |
| Kalman-extended `B̂(t|t) ± σ_B(t)` | Measure, Manage | Resonates with measurement, monitoring, and risk response | Explicit uncertainty output shaped for insurability and comparative rating |

---

## 5. Mapping by NIST function

### 5.1 Govern

NIST says Govern is the cross-cutting function that cultivates risk culture, aligns policies and procedures, and connects technical design to organizational values.

BRF aligns here through:

- accountable executive naming in the profile and attestation
- invariant enforcement mode disclosure
- anti-pattern attestation
- change-management triggers
- policy-snapshot coherence and evidence-binding requirements

BRF adds something NIST does not try to standardize:

- a fixed attestation form
- a required naming of worldview and composition
- an explicit distinction between architectural, structural, procedural, and documentary enforcement

### 5.2 Map

NIST Map is about context, intended use, impacts, stakeholders, and deployment setting. The Playbook notes that narrow-scope systems are easier to map, measure, and manage, and that open-ended public LLM systems are harder because of deployment variability.

BRF maps this into:

- worldview classification
- authority and reach tiers
- coupling regime
- principal population
- consequence sub-tag
- external dependency composition

BRF is stricter here than NIST because it turns context into:

- hard class floors
- topology classes
- explicit promoted classes when certain combinations appear

### 5.3 Measure

NIST Measure says appropriate methods and metrics should be selected for the most significant risks, that unmeasured risks should be documented, and that production behavior should be monitored.

BRF aligns here through:

- invariant conformance tests
- action and replay evidence
- observability tiers
- attack-accessibility analysis
- trajectory review
- residual-vs-inherent separation

BRF adds:

- a defined output shape for the measurement results
- formal class aggregation
- attestation-ready evidence references
- a direct uncertainty term `sigma_B`

### 5.4 Manage

NIST Manage covers risk responses, monitoring, incident handling, post-deployment TEVV, recovery, and change management.

BRF aligns here through:

- reversibility tiering
- kill-switch and rollback disclosure
- class recomputation triggers
- trajectory cadence
- observability evidence
- dependency re-attestation and attestation expiry

BRF adds:

- an explicit blast-radius framing for recovery horizons
- minimum class promotions when observability or reversibility is weak
- a tighter connection between architecture and risk-response credibility

---

## 6. Where BRF is stronger or more specific

BRF is more specific than NIST AI RMF in six places:

1. **Architecture-first classification**
2. **Open-world / closed-world distinction**
3. **Composition**
4. **Structural invariants**
5. **Attestation**
6. **Insurability**

---

## 7. Where NIST AI RMF is broader

NIST is broader than BRF in four places:

1. **Organization-wide risk culture**
2. **Stakeholder and affected-community engagement**
3. **General socio-technical risk management beyond a single attested system**
4. **Playbook-style action guidance across many AI use contexts**

---

## 8. Practical use

The most useful operational pattern is:

1. run organisational AI governance in NIST AI RMF terms
2. use BRF for deployed-system rating, evidence, and procurement-grade disclosure
3. attach BRF profiles, reports, and attestations as the system-specific evidence packet within the broader NIST-style risk-management programme

---

## 9. Note on the Generative AI Profile

As of April 23, 2026, the current official NIST Generative AI Profile is [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1), published July 26, 2024 and updated April 8, 2026 on the NIST publication page.

It is useful to read alongside this crosswalk because it sharpens the NIST treatment of generative-AI-specific risks. It still does not replace BRF's:

- worldview gate
- composition model
- structural invariant discipline
- attestation shape

It is a complement, not a substitute.

---

## 10. Bottom line

If you already use NIST AI RMF, BRF should be read as:

- a **system-specific architectural rating and attestation layer**
- not a rival enterprise governance framework
- not a duplicate checklist

The cleanest statement is:

> NIST AI RMF gives the risk-management operating system. BRF gives the blast-radius rating and attestation form for deployed agentic systems inside that operating system.
