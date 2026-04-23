# BRF Crosswalk to ISO/IEC 42001

*Translation note from the Blast Radius Framework into ISO/IEC 42001's AI management system frame.*

**Status:** Initial crosswalk
**Date:** 2026-04-23
**Primary sources:** [ISO/IEC 42001 official standard page](https://www.iso.org/standard/42001), [ISO 42001 explained](https://committee.iso.org/es/sites/isoorg/home/insights-news/resources/iso-42001-explained-what-it-is.html), [ISO AI management systems overview](https://www.iso.org/artificial-intelligence/ai-management-systems)

---

## 1. Purpose

This note answers the parallel question to the NIST crosswalk:

> If an organisation is working toward ISO/IEC 42001, where does BRF fit?

Short answer:

- **ISO/IEC 42001** is an organization-level management system standard for establishing, implementing, maintaining, and continually improving an AI management system
- **BRF** is a deployed-system classifier and attestation frame for operational blast radius

They are complementary, not interchangeable.

---

## 2. What ISO/IEC 42001 is

Per the official ISO material, ISO/IEC 42001:2023:

- specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS)
- is designed for organizations that develop, provide, or use AI-based products or services
- is built around a **Plan-Do-Check-Act** methodology
- is intended to help organizations manage AI-related risks and opportunities across the organization

The official ISO explainer also presents the standard at a high level as covering:

- leadership and organizational context
- AI policy and objectives
- risk management for AI systems
- data governance and system lifecycle controls
- transparency and information provision
- performance evaluation and monitoring
- continual improvement

That is a management-system scope, not a system-rating scope.

---

## 3. Non-equivalence note

This crosswalk is **not** a claim that:

- a BR profile is an ISO/IEC 42001 certification
- ISO/IEC 42001 automatically yields a BR class
- BRF can replace an AI management system

The correct relationship is:

- ISO/IEC 42001 gives the organization-wide governance and continuous-improvement frame
- BRF gives the system-level operational classification and evidence shape for a specific deployed agentic system

---

## 4. High-level mapping

| BRF element | Closest ISO/IEC 42001 area | Relationship | What BRF adds |
|---|---|---|---|
| `A–R–C–V–K–O` tuple | risk management; system lifecycle controls; transparency; monitoring | Gives a structured description of operational impact in deployment context | A compact deployable-system rating rather than organization-wide management-system requirements |
| Closed-world vs open-world gate | context; risk management; responsible use | Sharpens how system architecture changes governance credibility | Hard architectural boundary and BR-floor consequence |
| Composition topology (`T1`-`T4`) | system lifecycle controls; risk management | Makes inter-component structure explicit | Formal topology classes and composition math |
| Seven architectural invariants | governance; controls; monitoring; continual improvement | Correspond to what a mature AIMS should make possible | Concrete structural properties required for a credible BR claim |
| Anti-pattern catalogue | risk management; continual improvement | Helps identify governance failures embodied in architecture | Named negative reference set tied to blast-radius expansion |
| Signed and anchored attestation | transparency; information provision; performance evaluation | Strengthens evidence presentation and third-party reviewability | A verifier-friendly attestation form rather than a generic management artifact |
| Component cards | data governance; system lifecycle controls; transparency | Document the moving parts under a rated system | Structured component-level disclosure linked to the BR profile |

---

## 5. Mapping by ISO/IEC 42001 concern area

### 5.1 Leadership and organizational context

ISO's public explainer highlights leadership, organizational context, policy, objectives, roles, and responsibilities.

BRF aligns here through:

- deployer identity and accountable executive fields in the profile
- explicit rating context and deployment context
- named ownership of evidence and attestation posture
- role-based reports and decision artefacts in `reports/`

BRF adds:

- a requirement to disclose the rated system's actual blast-radius posture
- a distinction between nominal governance and structurally enforced governance

ISO asks whether leadership and governance are in place. BRF asks what system architecture those governance arrangements are actually governing.

### 5.2 AI policy, objectives, and risk management

ISO's public material emphasizes risk management for AI systems and balancing innovation with governance.

BRF aligns here through:

- the six-axis tuple
- modifiers for attack accessibility, trajectory, and residual-vs-inherent posture
- consequence tagging
- anti-pattern attestation

BRF adds:

- an ordinal class
- a cardinal score with uncertainty
- explicit class-promotion logic when dangerous combinations appear

ISO provides the management-system expectation that risk be managed. BRF provides a tighter operational way to describe the risk of a particular system instance.

### 5.3 Data governance and system lifecycle controls

ISO's public explainer names data governance and system lifecycle controls explicitly.

BRF aligns here through:

- policy snapshot coherence
- evidence binding
- component cards for models, corpora, tools, dependencies, and evidence anchors
- change-management triggers and re-attestation rules

BRF adds:

- profile-linked component documentation
- attestation-ready evidence references
- composition-aware system disclosure

This is one of the strongest fit areas: ISO says these controls should exist; BRF gives a shape for proving what they mean for blast radius.

### 5.4 Transparency and information provision

ISO's public material names transparency, accountability, and information provision as core concerns.

BRF aligns here through:

- profile publication
- executive summary, technical findings, and ADR backlog formats
- anti-pattern disclosure
- component cards
- signed and anchored attestation

BRF adds:

- a procurement-grade vendor questionnaire
- a machine-readable profile schema
- a concrete evidence-verification path

### 5.5 Performance evaluation, monitoring, and continual improvement

ISO's public material highlights performance evaluation, monitoring, and continual improvement under the management-system model and the PDCA cycle.

BRF aligns here through:

- invariant conformance tests
- observability tiers
- trajectory review
- re-attestation triggers
- remediation backlog structure

BRF adds:

- system-specific pass/fail evidence tied to invariants
- a direct link between weak observability and promoted effective blast radius
- a clearer bridge from audit findings to remediation backlog

---

## 6. Where BRF is stronger or more specific

Relative to the public ISO/IEC 42001 material, BRF is more specific in five places:

1. **System-level architecture classification**
2. **Composition and coupling**
3. **Hard structural invariants**
4. **Verifier-friendly attestation**
5. **Insurability and uncertainty output**

---

## 7. Where ISO/IEC 42001 is broader

ISO/IEC 42001 is broader in at least four ways:

1. **Organization-wide governance**
2. **Management-system operation across the AI lifecycle**
3. **PDCA-driven continual improvement**
4. **Certification ecosystem**

ISO's official explainer is also explicit that certification is voluntary and performed by independent certification bodies rather than ISO itself.

---

## 8. Practical use

The most useful pattern is:

1. use ISO/IEC 42001 to build the organization's AI management system
2. use BRF to classify and evidence individual deployed agentic systems within that system
3. use BRF reports, profiles, component cards, and attestations as system-specific evidence packets inside the broader ISO-style management system

This keeps the division of labor clean:

- **ISO/IEC 42001** governs the organization's AI management system
- **BRF** governs the rated system's operational blast-radius disclosure and evidence posture

---

## 9. Source-limit note

This crosswalk intentionally stays at the official-summary level because the full ISO/IEC 42001 standard text is not publicly open access.

That means:

- the mapping here is reliable at the management-system-concern level
- it is **not** a clause-by-clause certification guide

If a clause-level crosswalk is needed later, it should be produced against licensed access to the full standard text.

---

## 10. Bottom line

If you are using ISO/IEC 42001, BRF should be read as:

- a **system-specific operational classification and evidence layer**
- not an alternative management system
- not a substitute for certification

The cleanest statement is:

> ISO/IEC 42001 gives the organizational AI management system. BRF gives the blast-radius classification and attestation form for specific deployed agentic systems inside that system.
