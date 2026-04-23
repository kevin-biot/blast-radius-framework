# BRF Crosswalk to the EU AI Act

*Translation note from the Blast Radius Framework into Regulation (EU) 2024/1689.*

**Status:** Initial crosswalk
**Date:** 2026-04-23
**Primary sources:** [Regulation (EU) 2024/1689 official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), with emphasis on Articles 12, 13, 15, 26, 27, and 72

---

## 1. Purpose

This note answers a practical question:

> If an organisation is reading the EU AI Act, where does BRF fit?

Short answer:

- the **EU AI Act** is a binding legal framework that imposes obligations on providers, deployers, importers, distributors, and others depending on system category and role
- **BRF** is an architecture-first operational classifier and attestation frame for deployed agentic systems

They are complementary, not interchangeable.

---

## 2. What the EU AI Act does

As of **April 23, 2026**, the current official legal source is [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) on EUR-Lex.

For BRF purposes, the most relevant parts are the provisions that require:

- record-keeping and traceability for high-risk systems in **Article 12**
- transparency and provider information to deployers in **Article 13**
- accuracy, robustness, and cybersecurity in **Article 15**
- deployer obligations in **Article 26**
- fundamental-rights impact assessments for certain deployers in **Article 27**
- post-market monitoring by providers in **Article 72**

The Act is legal-category-shaped. BRF is operational-blast-radius-shaped.

---

## 3. Non-equivalence note

This crosswalk is **not** a claim that:

- a BR class satisfies the EU AI Act
- an AI Act classification yields a BR class
- BRF can replace legal advice, conformity assessment, or statutory obligations

The correct relationship is:

- the **EU AI Act** defines the legal obligations
- **BRF** helps an organisation describe, evidence, and pressure-test whether the system architecture can actually support those obligations in operation

---

## 4. High-level mapping

| BRF element | Closest EU AI Act area | Relationship | What BRF adds |
|---|---|---|---|
| `A–R–C–V–K–O` tuple | high-risk obligations, deployer obligations, post-market monitoring | Makes the deployed system's operational profile explicit | A compact rating vocabulary for propagation, reversibility, and observability |
| Closed-world vs open-world gate | risk posture, robustness, human oversight credibility | Sharpens whether the substrate can plausibly support the legal controls claimed | A hard architectural floor for open-world systems |
| Composition topology (`T1`-`T4`) | system context, provider/deployer information, post-market monitoring | Makes multi-component interaction explicit | Named topology classes and compounding logic |
| Seven architectural invariants | Articles 12, 13, 15, 26, 72 especially | Correspond to whether legal obligations are structurally supportable | Concrete architectural properties rather than only procedural statements |
| Anti-pattern catalogue | legal-compliance failure modes embodied in design | Helps identify where nominal compliance is likely to collapse in operation | Named negative reference tied to blast-radius expansion |
| Signed and anchored attestation | evidence for auditors, authorities, customers, and underwriters | Strengthens verification posture | A verifier-friendly evidence form beyond minimum legal narrative |
| Reports + component cards | transparency, instructions for use, audit support | Improve explainability and evidence packaging | Role-specific reporting and linkable component disclosures |

---

## 5. Mapping by article cluster

### 5.1 Article 12 — record-keeping

Article 12 requires high-risk AI systems to technically allow the automatic recording of events over the system lifetime, and makes logging relevant to traceability, post-market monitoring, and monitoring operation by deployers.

BRF aligns here through:

- `O` as a first-class axis
- Invariant 2 (evidence binding)
- Invariant 6 (observability / replay in the framework’s usage)
- signed and anchored attestations
- evidence and anchor component cards

BRF adds:

- a distinction between coarse telemetry and replayable, audit-admissible traces
- class consequences when observability is weak
- a path from trace quality to priceable uncertainty

The Act says logging must exist. BRF says weak logging and non-replayable evidence change the effective blast radius and credibility of the claim.

### 5.2 Article 13 — transparency and information to deployers

Article 13 requires high-risk AI systems to be accompanied by instructions for use and information that lets deployers use the system appropriately, including capabilities, limitations, expected accuracy characteristics, foreseeable circumstances affecting performance, and human-oversight needs.

BRF aligns here through:

- the six-axis tuple
- component cards
- the vendor questionnaire in `framework.md §17`
- the technical findings and executive summary report layers

BRF adds:

- a machine-readable profile form
- explicit composition disclosure
- anti-pattern disclosure
- a way to make “capabilities and limitations” operational rather than marketing-shaped

Article 13 is one of the cleanest fit points for BRF because BRF is already designed as a disclosure discipline.

### 5.3 Article 15 — accuracy, robustness, and cybersecurity

Article 15 requires high-risk AI systems to achieve an appropriate level of accuracy, robustness, and cybersecurity and perform consistently on those dimensions through their lifecycle. It also points toward benchmarks and measurement methodologies.

BRF aligns here through:

- the worldview gate
- the coupling axis
- `delta_adv`
- trajectory review
- invariant conformance tests
- benchmark-harness design work in `adoption/`

BRF adds:

- a stronger architectural treatment of why some substrates are harder to govern
- class promotions when dangerous combinations appear
- a clearer way to represent operational containment rather than only model performance

The AI Act speaks in robustness language. BRF sharpens that into architecture, coupling, and propagation language.

### 5.4 Article 26 — deployer obligations

Article 26 includes deployer obligations such as using systems in accordance with instructions, ensuring relevant human oversight, keeping logs under deployer control where applicable, and cooperating with competent authorities. The public EUR-Lex text also captures the obligation for certain deployers to inform natural persons when Annex III high-risk systems make or assist decisions about them.

BRF aligns here through:

- authority and reversibility tiering
- kill-switch and rollback disclosure
- observability evidence
- role-based reports
- component cards for tools and dependencies

BRF adds:

- a tighter way to express whether human oversight is structurally meaningful
- explicit treatment of practical reversibility
- anti-pattern handling for approval fatigue and nominal oversight

The legal obligation is deployer behavior. BRF helps determine whether the system architecture makes those deployer obligations realistic.

### 5.5 Article 27 — fundamental-rights impact assessment

Article 27 requires certain deployers to perform a fundamental-rights impact assessment before deploying particular high-risk systems. The official text requires the assessment to consider the use context, the affected categories of persons, likely harms, human oversight, and risk-mitigation measures.

BRF aligns here through:

- `K` sub-tags, especially `K4-F`
- principal-population framing
- residual-vs-inherent separation
- report templates
- anti-pattern catalogue

BRF adds:

- a compact way to tie rights-impact concerns to authority, reach, coupling, and reversibility
- a cleaner evidence packet for procurement, audit, and board review

Article 27 is where BRF can be especially helpful as an internal preparation layer, even though it is not itself the statutory FRIA.

### 5.6 Article 72 — post-market monitoring

Article 72 requires providers of high-risk systems to establish and document a post-market monitoring system that actively and systematically collects, documents, and analyses relevant data over the system lifetime to evaluate continuous compliance.

BRF aligns here through:

- trajectory review
- re-attestation triggers
- benchmark-harness design
- component-card updates
- cardinal-score uncertainty updates

BRF adds:

- a direct link between monitoring quality and rating credibility
- a way to express how architecture affects post-market monitoring difficulty
- a disciplined trigger model for re-rating after material change

The legal requirement is monitoring. BRF adds a system-specific way to say what the monitoring is trying to preserve.

---

## 6. Where BRF is stronger or more specific

Relative to the EU AI Act, BRF is more specific in six places:

1. **Architecture-first classification**
2. **Open-world / closed-world distinction**
3. **Composition and coupling**
4. **Structural invariants**
5. **Operational reversibility**
6. **Verifier-friendly attestation**

---

## 7. Where the EU AI Act is broader or different

The EU AI Act is broader or simply different in five places:

1. **It is binding law, not a voluntary framework**
2. **It allocates obligations by legal role**
3. **It classifies by legal risk category and use case, not by operational blast radius**
4. **It includes conformity-assessment and enforcement machinery**
5. **It reaches beyond system architecture into statutory duties, registration, and authority access**

---

## 8. Practical use

The most useful pattern is:

1. determine the system's legal category and role obligations under the EU AI Act
2. use BRF to classify the deployed system's operational blast radius and evidence posture
3. use BRF reports, profiles, component cards, and attestations as the architecture-and-evidence packet supporting legal compliance work

That division of labor is clean:

- the **EU AI Act** says what the law requires
- **BRF** helps determine whether the deployed architecture can actually produce the evidence and containment posture those obligations presuppose

---

## 9. Bottom line

If you are reading the EU AI Act, BRF should be read as:

- a **system-specific architectural evidence layer**
- not a substitute for legal classification
- not a substitute for conformity assessment

The cleanest statement is:

> The EU AI Act sets the legal obligations. BRF helps disclose and test whether the deployed system architecture can actually sustain them in operation.
