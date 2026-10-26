# Lane2 Self-Assessment — Executive Summary


**Review correction, 2026-10-26:** This is an April assessment, not a current re-attestation. Its numeric profile and measured observations are retained. Statements that the architecture guarantees coverage, avoids exclusions, cannot obtain insurance, or necessarily forecloses lawful deployment are withdrawn. **Coverage not established.** See [current claims policy](../../adoption/claims-and-evidence.md) and [current EU crosswalk](../../adoption/crosswalk-eu-ai-act.md). The historical JSON profile is not re-signed or re-rated by this correction.

**System:** Lane2 integrated governance platform (reference regulated-operational-workflow deployment)
**Date of assessment:** 2026-04-21
**Framework version:** v0.5.1
**Assessor:** Lane2 (self-attestation)
**Accountable executive:** Kevin Brown, Founder, Lane2

**Companion documents:** [`self-assessment.md`](./self-assessment.md) (technical findings), [`self-assessment.json`](./self-assessment.json) (machine-readable profile), [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md) (remediation backlog).

---

## 1. Headline

The Lane2 stack — when deployed for a canonical regulated operational workflow (e.g. legal-citation-review, wallet-conformance, clinical-triage archetypes) — is rated **BR-4 (Systemic)**.

**In plain English:** this is a high-consequence system by design. The domains Lane2 targets (regulated review, cross-border payments, clinical triage) carry inherent consequence that puts any well-designed system into BR-4 — the framework rates the domain honestly, not the architecture's aesthetic. Our architecture compresses an **inherent BR-5** (what the consequence domain alone would imply without controls) down to a **residual BR-4** by enforcing all seven architectural invariants — six at full architectural-enforcement maturity and one (observability O4) partially at the public-observable level pending publication of the runtime invariant-checking specification.

The April BR-4 rating describes the assessed configuration under the framework then in force. It is not an insurer decision or a current independent confirmation of the controls.

**Evidence anchors are demonstrable, not just claimed.** The OBO public reference implementation at [`obo-standard/examples/integrations/a2a/`](https://github.com/kevin-biot/obo-standard/tree/main/examples/integrations/a2a) ships a runnable end-to-end OBO + A2A composition with Ed25519 keys, a live public DNS trust anchor (`_obo-key.lane2.ai`), and Merkle evidence. Third parties can verify the DNS anchor with `dig` and run the composition themselves. A companion negative control at `examples/integrations/a2a-multi-hop/` deliberately ships the NL-coupled agent-agent-agent architecture the framework rejects; it is the measurable substrate against which the DOP-side Sentinel experiments demonstrate that typed topologies read zero drift where NL-coupled topologies read positive. The framework's T1-vs-T2 composition-class claim is empirically grounded, not theoretical.

---

## 2. What this means for the business

Three concrete impacts, decreasing order of material consequence:

### 2.1 Insurability posture is defensible but not yet priceable

**Current correction:** the April architecture describes controls relevant to underwriting due diligence. No insurer acceptance, bound policy or exclusion analysis is established by this self-assessment.

SAPP specifically provides **role-based evidence APIs** that are the shape underwriters and regulators can consume without bespoke integration: customer-care and consumer verification via `GET /evidence/{traceId}` with scored bundles and machine-readable reason codes; regulator verification via `GET /regulator/verify/{traceId}` and `GET /regulator/integrity` with privacy-preserving, QTSP-anchored responses. Three-level Merkle proof chain published to EU Qualified Archive on 15-minute cycles. This is the integration surface that converts "we have anchored evidence" from an architectural claim into a verifiable API an auditor can hit.

The cardinal score was not produced in April. Implementing the experimental filter would still require independent calibration and loss-model validation; it would not establish an insurer's appetite or price.

**Business consequence:** present the architecture and unresolved findings to prospective reviewers without a claim of coverage, preferential premium or underwriting acceptance.

### 2.2 Regulatory posture is architectural — cross-border included

The architecture may supply evidence relevant to Articles 12, 15, 19, 26 and 72/73. Article 26(6) concerns deployer log retention, not authority access. This assessment does not establish legal applicability or compliance; use the [reviewed crosswalk](../../adoption/crosswalk-eu-ai-act.md).

Cross-border jurisdictional enforcement within Lane2-governed deployments is also architectural — via the composition of **aARP** (inter-jurisdictional matrix routing with provable lawful-route validation), **RTGF** (unified policy-driven fabric synchronising jurisdictional policy across components — "lawful by design"), and **Shared Ontology** (jurisdiction, consent, regulatory boundaries as machine-readable rules). This is Lane2's core I5 mechanism.

Where Lane2 composes with a non-Lane2 counterparty, the general framework §7.1 composition rule applies (as it does for every invariant): the counterparty's architecture is rated separately, and composition with a non-conformant counterparty is either declined or rated accordingly. This is a property of cross-org composition in general, not a specific I5 gap.

For the sub-case of cross-organisational free-roaming agents without a shared authorisation server, the **OBO open standard** (`kevin-biot/obo-standard`) is available as a convenience interop pattern — a deployment option when a Lane2-stack deployer needs to compose with that specific class of agent. OBO is not Lane2's core I5 mechanism; its absence in the broader industry does not reduce Lane2's own architectural I5 enforcement.

**Business consequence:** cross-border deployment needs legal-role, jurisdiction, organisational-mandate and runtime-boundary review. An architecture description or interoperability standard is not a legal clearance.

### 2.3 The integrated stack is pre-launch — three anti-pattern demotion paths are partial

At the public-observable level, three Part A anti-patterns (context stuffing, autonomy-slider fatigue, prompt-injection-as-feature) and three Part B anti-patterns (prompt storage governance, authentication freshness, retention/authority-export) are `exhibited_with_demotion_path`. The demotion paths exist; they are not fully implemented at public-observable level. These are **architectural-maturity items, not design flaws**. A pre-launch platform's architecture can be sound without every control being at full architectural-enforcement maturity.

**Business consequence:** these items are the PoC agenda. Each PoC engagement advances one or more of the demotion paths. By the end of a handful of PoC validations, the exhibited-with-demotion-path items move to not-exhibited.

---

## 3. Top three remediation priorities

From [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md):

| # | Remediation | Effort | Class impact |
|---|---|---|---|
| 1 | **Kalman Phase 1 implementation** — scalar Kalman on a pilot-deployment compliance metric, producing σ_B(t) numerically. Produces an experimental index only after calibration; closes the implementation portion of Gap-2. | months (pilot-dependent) | Does not change the ordinal rating or establish insurer acceptance. |
| 2 | **Principal-population accounting** — instrument per-action principal-count in the evidence schema; closes Gap-4. Gives the R-axis sub-component its population dimension. | weeks | No ordinal class change; materially improves residual-vs-inherent gap and σ_B granularity. |
| 3 | **First authority-export drill and first OBO-conformant composition** — exercise the B10 authority-export path end-to-end in a PoC; exercise cross-border OBO composition with a willing counterparty. Closes B10 exhibited-with-demotion-path and moves Gap-1 toward architectural. | quarter | Moves two `exhibited_with_demotion_path` anti-patterns to `not_exhibited`; advances I5 toward architectural. |

Detailed backlog with P0/P1/P2/P3 priority, dependencies, and full ADR candidate list in [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md).

---

## 4. Insurability posture (detailed)

| Question | Answer |
|---|---|
| Coverable today by specialist underwriters (Munich Re aiSure, AIUC, Armilla/Lloyd's)? | **Not established.** An insurer must assess the actual proposal and policy terms. |
| Coverable under Verisk 2026 commercial insurance AI exclusions? | **Not established.** No applicable policy wording and endorsement analysis is supplied here. |
| Gap to Consolidation Zone (framework §14 Quadrant IV — BR-2/BR-3 with Invariants 1–7 intact)? | Lane2 is already in Quadrant IV at BR-4. Quadrant IV is defined as architectural-invariants-enforced with market-access-maintained; the BR-4 within the Consolidation Zone is the *appropriate* rating for the consequence domain, not a gap from BR-2/BR-3. Moving below BR-4 would require operating in a lower-consequence domain — not a remediation, a business-scope change. |
| Is the cardinal score B̂(t|t) ± σ_B(t) produced? | **No (Gap-2).** Kalman extension implementation is Phase 0 (theoretical). Remediation #1 above closes this. |

---

## 5. Recommendation

- [ ] Proceed as-is. *(Not selected — Gap-2 materially affects underwriter pricing.)*
- [x] **Proceed with parallel remediation.** The current BR-4 rating is appropriate for the deployment context (regulated operational workflows). The architecture meets the structural requirements; the three top-priority remediations execute in parallel with PoC engagement. This is the historical April selection, not a current deployment authorisation or pricing finding.
- [ ] Pause and remediate before proceeding.
- [ ] Redesign.

**Current correction:** the April recommendation is historical and is not renewed by this document edit. Validate the deployed configuration, unresolved controls, legal obligations and contractual requirements before a commercial decision.

The retained BR-4 rating is not a declaration that other systems in these domains must receive the same rating. Assess each deployment's actual authority, scope, coupling and evidence.

---

## 6. Sign-off

I have reviewed this Executive Summary and the underlying technical findings in [`self-assessment.md`](./self-assessment.md). The rating and remediation path stated above represent my understanding of the Lane2 stack's current Blast Radius posture and the actions required to maintain and improve it through pre-launch into commercial deployment.

The self-assessment is published openly as a worked example of the framework applied honestly to its own authors' work. Readers are invited to critique, corroborate, or counter-evidence any claim made here; pull requests and issues on the [blast-radius-framework repository](https://github.com/kevin-biot/blast-radius-framework) are the right channel.

**Signed:** Kevin Brown, Founder, Lane2 — 2026-04-21

**Witnessed:** Self-attestation (no third-party auditor at this date). Independent auditor review is a v0.6+ framework item and will apply to a future revision of this assessment when the third-party certification form ships.

---

*End of Tier 1 Executive Summary. Detailed technical findings in [`self-assessment.md`](./self-assessment.md). ADR remediation backlog in [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md).*
