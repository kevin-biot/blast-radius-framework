# BRF Crosswalk to Specialist-Underwriter Criteria

*Translation note from the Blast Radius Framework into the public due-diligence and assurance criteria used in the specialist AI-insurance market.*

**Status:** Initial crosswalk
**Date:** 2026-04-23
**Primary sources:** [Munich Re aiSure whitepaper and FAQ](https://www.munichre.com/en/solutions/for-industry-clients/insure-ai/ai-whitepaper.hsb.html), [Armilla insurance and warranty pages](https://www.armilla.ai/ai-insurance), [Armilla product launch materials](https://www.armilla.ai/resources/chaucer-and-armilla-launch-new-ai-liability-insurance-product), [AIUC-1 certification materials](https://www.aiuc-1.com/aiuc-1-certification), [AIUC-1 certificate explainer](https://aiuc-1.com/learn/certificate)

---

## 1. Purpose

This note answers a market-facing question:

> If an organisation wants to be insurable in the specialist AI-insurance market, where does BRF fit?

Short answer:

- the specialist market does not ask only whether a system is legally compliant
- it asks whether the system can be **understood, measured, monitored, and bounded** well enough to support underwriting and coverage terms

BRF fits as the architecture-and-evidence layer that makes those questions easier to answer.

---

## 2. Source-limit note

This crosswalk uses **publicly stated** insurer and assurance criteria, not private underwriting manuals or policy wordings.

That means:

- the mapping is reliable at the public due-diligence and assurance level
- it is **not** a guarantee of underwriting appetite, premium, or policy terms
- it is **not** a substitute for broker, insurer, or legal advice

This matters because much of the decisive underwriting detail is not public.

---

## 3. What the public specialist-market sources say

### 3.1 Munich Re aiSure

Munich Re's public aiSure material describes:

- insurance for AI performance and reliability risk
- technical due diligence before coverage
- focus on model development pipelines, drift, monitoring, historical performance, and risk estimation
- pricing and coverage that depend on quality, reliability, and performance stability

### 3.2 Armilla

Armilla's public material describes:

- affirmative AI liability coverage and performance warranties
- third-party validation of performance, fairness, and robustness
- coverage for underperformance, hallucinations, drift, and other deviations from expected AI behavior
- ongoing monitoring and AI risk analytics

Armilla also states publicly that it operates as a Lloyd’s coverholder and that some offerings are backed by named insurance partners.

### 3.3 AIUC-1

AIUC-1's public material describes:

- scoped certification for AI agents
- evidence collection across technical, operational, and legal controls
- technical testing for hallucinations, unsafe tool calls, and adversarial attacks
- recurring retesting and annual re-audit
- outputs including a certificate, audit report, and evaluation results

AIUC-1 is not itself a policy. It is an assurance layer that is clearly relevant to insurability and enterprise trust.

---

## 4. Non-equivalence note

This crosswalk is **not** a claim that:

- a BR profile guarantees coverage
- a BR class determines premium
- a BR attestation replaces underwriting or certification

The correct relationship is:

- specialist underwriters and assurance bodies ask for evidence of reliability, controls, monitoring, and bounded risk
- BRF gives a structured way to disclose and evidence those properties at the deployed-system level

---

## 5. High-level mapping

| Public specialist-market criterion | Closest BRF element | Relationship | What BRF adds |
|---|---|---|---|
| reproducible decision trails | Invariant 1; `O`; attestation format | Strong fit | A formal system-level place to record replayability and trace quality |
| monitoring and drift control | `O`; `tau`; benchmark harness; post-change re-attestation | Strong fit | A consistent vocabulary for observability maturity and trajectory |
| performance stability | worldview, coupling, invariants, cardinal uncertainty | Strong fit | A way to connect system architecture to uncertainty rather than only point metrics |
| bounded failure propagation | `R`, `C`, `V`; bounded blast-radius invariant | Strong fit | Explicit composition and propagation framing |
| fairness / robustness / security testing | anti-patterns, `delta_adv`, benchmark harness, component cards | Partial fit | Connects test outputs to deployment architecture and blast radius |
| scoped assurance and evidence pack | reports, component cards, signed / anchored attestation | Strong fit | A machine-readable and verifier-friendly evidence package |
| recurring reassessment | trajectory review, re-attestation triggers | Strong fit | Explicit triggers for material change and renewed evaluation |

---

## 6. Mapping by source family

### 6.1 Munich Re aiSure

Munich Re's public aiSure material emphasizes technical due diligence, historical performance data, drift, monitoring, and quantitative risk estimation.

BRF aligns here through:

- `O` and observability evidence
- trajectory review
- invariant conformance tests
- cardinal score and uncertainty
- component cards for models, tools, and dependencies

BRF adds:

- a stronger architecture-first explanation of why reliability and stability differ across system designs
- explicit coupling and reach treatment
- attestation-ready disclosure form

The public aiSure material is especially compatible with BRF's Kalman extension and evidence-quality frame, because both care about uncertainty rather than just point performance.

### 6.2 Armilla

Armilla's public material emphasizes third-party validation of performance, fairness, robustness, and warranty/liability coverage for AI underperformance, hallucinations, drift, and related harms.

BRF aligns here through:

- `K`, especially consequence tagging
- `delta_adv`
- anti-pattern catalogue
- benchmark-harness design
- component cards

BRF adds:

- a system-level blast-radius vocabulary for how far those harms can propagate
- clearer authority, reach, coupling, and reversibility disclosure
- a more explicit architecture-and-evidence packet for deployers and brokers

Armilla's public framing is especially compatible with BRF where the central concern is not abstract safety posture but real deployment loss scenarios.

### 6.3 AIUC-1

AIUC-1's public material emphasizes technical testing, operational controls, legal policies, recurring evaluation, scoped certification, and enterprise-risk concerns such as data leaks, jailbreaks, and reliability failures.

BRF aligns here through:

- anti-pattern attestation
- `delta_adv`
- invariant conformance tests
- component cards
- re-attestation and trajectory review

BRF adds:

- explicit composition disclosure
- blast-radius class and propagation framing
- closer integration with deployer and underwriter evidence packets

AIUC-1 is particularly relevant to BRF because it operationalizes many assurance expectations around AI agents but does not itself provide a blast-radius classifier.

---

## 7. Where BRF is stronger or more specific

Relative to the public specialist-market material, BRF is more specific in six places:

1. **Open-world / closed-world distinction**
2. **Composition and coupling**
3. **Operational reversibility**
4. **System-level blast-radius class**
5. **Attestation shape**
6. **Consistent role-based report set**

---

## 8. Where specialist-market material is broader or different

The public specialist-market material is broader or different in five places:

1. **Coverage structure and insurance economics**
2. **Actual underwriting appetite**
3. **Liability and warranty triggers**
4. **Fairness / robustness / performance testing detail**
5. **Ongoing market-specific monitoring expectations**

That is expected. BRF is not an insurance product. It is a classifier and evidence discipline.

---

## 9. Practical use

The most useful pattern is:

1. use BRF to produce a system-specific architecture and evidence packet
2. attach benchmark outputs, component cards, and attestation artefacts
3. use that packet in discussions with brokers, underwriters, enterprise buyers, and assurance schemes like AIUC-1

This is the clean division of labor:

- specialist insurers and assurance bodies decide how to test, quote, certify, or cover
- BRF helps the deployer present a cleaner, more structurally meaningful disclosure package

---

## 10. Bottom line

If you are trying to be insurable in the specialist AI market, BRF should be read as:

- a **pre-underwriting architecture and evidence discipline**
- not a coverage guarantee
- not a substitute for certification or underwriting

The cleanest statement is:

> Specialist insurers and assurance bodies ask whether AI risk is measurable, bounded, and monitorable. BRF helps the deployer show those properties in a system-specific, architecture-first form.
