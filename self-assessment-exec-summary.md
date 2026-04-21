# Lane2 Self-Assessment — Executive Summary

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

BR-4 is the right rating for what we do. A stack in this consequence domain that rated BR-2 would be lying; a stack that rated BR-5 without demotion paths would be uninsurable. BR-4 with Invariants 1–7 held, composition topology T1 sub-additive, and no material anti-patterns without demotion paths is the **Consolidation Zone** (framework §14 Quadrant IV).

**Evidence anchors are demonstrable, not just claimed.** The OBO public reference implementation at [`obo-standard/examples/integrations/a2a/`](https://github.com/kevin-biot/obo-standard/tree/main/examples/integrations/a2a) ships a runnable end-to-end OBO + A2A composition with Ed25519 keys, a live public DNS trust anchor (`_obo-key.lane2.ai`), and Merkle evidence. Third parties can verify the DNS anchor with `dig` and run the composition themselves. A companion negative control at `examples/integrations/a2a-multi-hop/` deliberately ships the NL-coupled agent-agent-agent architecture the framework rejects; it is the measurable substrate against which the DOP-side Sentinel experiments demonstrate that typed topologies read zero drift where NL-coupled topologies read positive. The framework's T1-vs-T2 composition-class claim is empirically grounded, not theoretical.

---

## 2. What this means for the business

Three concrete impacts, decreasing order of material consequence:

### 2.1 Insurability posture is defensible but not yet priceable

Lane2's architecture satisfies the specialist-underwriter minimum criteria (Munich Re aiSure, AIUC, Armilla/Lloyd's) at the structural level: reproducible decision trails, immutable evidence retention via SAPP, policy-snapshot coherence, bounded blast radius, fail-closed execution. This places Lane2 in the **coverable-with-conditions** category rather than the Verisk-2026-excluded category. However, the cardinal score B̂(t|t) ± σ_B(t) is not yet numerically produced because the Kalman extension implementation is at Phase 0 (theoretical). Underwriters will price conservatively against the ordinal BR-4 rating until Phase 1 lands and σ_B becomes numerically available.

**Business consequence:** pre-launch, the commercial case is "we are architecturally pricing-friendly BR-4, expected to move toward numerically priceable BR-4 within [PoC window]". Post-Phase-1, Lane2 becomes a reference data-point specialist underwriters can calibrate against.

### 2.2 Regulatory posture is architectural — cross-border included

EU AI Act Articles 12 (logging), 15 (robustness), 19 (retention), 26(6) (authority access), 72/73 (post-market monitoring) are supported architecturally via the SAPP evidence-anchoring layer and the PACT pack compliance framework. Inside a single EU-jurisdiction deployment, the architecture meets or exceeds the minimum evidence profile.

Cross-border jurisdictional enforcement within Lane2-governed deployments is also architectural — via the composition of **aARP** (inter-jurisdictional matrix routing with provable lawful-route validation), **RTGF** (unified policy-driven fabric synchronising jurisdictional policy across components — "lawful by design"), and **Shared Ontology** (jurisdiction, consent, regulatory boundaries as machine-readable rules). This is Lane2's core I5 mechanism.

Where Lane2 composes with a non-Lane2 counterparty, the general framework §7.1 composition rule applies (as it does for every invariant): the counterparty's architecture is rated separately, and composition with a non-conformant counterparty is either declined or rated accordingly. This is a property of cross-org composition in general, not a specific I5 gap.

For the sub-case of cross-organisational free-roaming agents without a shared authorisation server, the **OBO open standard** (`kevin-biot/obo-standard`) is available as a convenience interop pattern — a deployment option when a Lane2-stack deployer needs to compose with that specific class of agent. OBO is not Lane2's core I5 mechanism; its absence in the broader industry does not reduce Lane2's own architectural I5 enforcement.

**Business consequence:** Regulated deployments, including cross-border, are architecturally defensible today within Lane2-governed scope. Ecosystem adoption of OBO is a commercial accelerator for specific deployer use cases (free-roaming agents crossing non-Lane2 systems); it is not a blocker to Lane2's own regulatory posture.

### 2.3 The integrated stack is pre-launch — three anti-pattern demotion paths are partial

At the public-observable level, three Part A anti-patterns (context stuffing, autonomy-slider fatigue, prompt-injection-as-feature) and three Part B anti-patterns (prompt storage governance, authentication freshness, retention/authority-export) are `exhibited_with_demotion_path`. The demotion paths exist; they are not fully implemented at public-observable level. These are **architectural-maturity items, not design flaws**. A pre-launch platform's architecture can be sound without every control being at full architectural-enforcement maturity.

**Business consequence:** these items are the PoC agenda. Each PoC engagement advances one or more of the demotion paths. By the end of a handful of PoC validations, the exhibited-with-demotion-path items move to not-exhibited.

---

## 3. Top three remediation priorities

From [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md):

| # | Remediation | Effort | Class impact |
|---|---|---|---|
| 1 | **Kalman Phase 1 implementation** — scalar Kalman on a pilot-deployment compliance metric, producing σ_B(t) numerically. Unlocks cardinal score for underwriters; closes Gap-2. | months (pilot-dependent) | Moves Lane2 from "ordinal-rateable BR-4" to "numerically priceable BR-4"; enables specialist underwriter quoting. |
| 2 | **Principal-population accounting** — instrument per-action principal-count in the evidence schema; closes Gap-4. Gives the R-axis sub-component its population dimension. | weeks | No ordinal class change; materially improves residual-vs-inherent gap and σ_B granularity. |
| 3 | **First authority-export drill and first OBO-conformant composition** — exercise the B10 authority-export path end-to-end in a PoC; exercise cross-border OBO composition with a willing counterparty. Closes B10 exhibited-with-demotion-path and moves Gap-1 toward architectural. | quarter | Moves two `exhibited_with_demotion_path` anti-patterns to `not_exhibited`; advances I5 toward architectural. |

Detailed backlog with P0/P1/P2/P3 priority, dependencies, and full ADR candidate list in [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md).

---

## 4. Insurability posture (detailed)

| Question | Answer |
|---|---|
| Coverable today by specialist underwriters (Munich Re aiSure, AIUC, Armilla/Lloyd's)? | **Yes, with conditions.** Structural alignment on all six insurability invariants; cardinal score not yet numerically available so pricing will be conservative. |
| Coverable under Verisk 2026 commercial insurance AI exclusions? | **Yes, not excluded.** The exclusion framework targets nondeterministic, unevidenced, uncontained systems. Lane2's profile does not match the excluded category. |
| Gap to Consolidation Zone (framework §14 Quadrant IV — BR-2/BR-3 with Invariants 1–7 intact)? | Lane2 is already in Quadrant IV at BR-4. Quadrant IV is defined as architectural-invariants-enforced with market-access-maintained; the BR-4 within the Consolidation Zone is the *appropriate* rating for the consequence domain, not a gap from BR-2/BR-3. Moving below BR-4 would require operating in a lower-consequence domain — not a remediation, a business-scope change. |
| Is the cardinal score B̂(t|t) ± σ_B(t) produced? | **No (Gap-2).** Kalman extension implementation is Phase 0 (theoretical). Remediation #1 above closes this. |

---

## 5. Recommendation

- [ ] Proceed as-is. *(Not selected — Gap-2 materially affects underwriter pricing.)*
- [x] **Proceed with parallel remediation.** The current BR-4 rating is appropriate for the deployment context (regulated operational workflows). The architecture meets the structural requirements; the three top-priority remediations execute in parallel with PoC engagement. Lane2 is commercially deployable now; the remediations improve underwriter pricing and close partial-holdings on specific invariants.
- [ ] Pause and remediate before proceeding.
- [ ] Redesign.

**Justification.** The BR-4 rating is an honest rating of the domain we target; Lane2's architectural compression from inherent BR-5 to residual BR-4 is what the framework says good closed-world T1 architecture should achieve. The remediation priorities are maturity items, not design flaws — they do not block commercial deployment. PoC engagements are the mechanism by which the remediations land; commercial deployment and remediation are not in tension, they are complementary phases of the same pre-launch-to-launch transition.

A stack in the target consequence domains that rated BR-2 or BR-3 would be under-rating its own consequence domain and would not be credible to a regulator or underwriter. A stack that rated BR-5 without demotion paths would be commercially uninsurable. BR-4 with Invariants 1–7 held or partially-held is the rating that says *we know what we are building, we know what it costs to govern it, and we have done the architectural work*.

---

## 6. Sign-off

I have reviewed this Executive Summary and the underlying technical findings in [`self-assessment.md`](./self-assessment.md). The rating and remediation path stated above represent my understanding of the Lane2 stack's current Blast Radius posture and the actions required to maintain and improve it through pre-launch into commercial deployment.

The self-assessment is published openly as a worked example of the framework applied honestly to its own authors' work. Readers are invited to critique, corroborate, or counter-evidence any claim made here; pull requests and issues on the [blast-radius-framework repository](https://github.com/kevin-biot/blast-radius-framework) are the right channel.

**Signed:** Kevin Brown, Founder, Lane2 — 2026-04-21

**Witnessed:** Self-attestation (no third-party auditor at this date). Independent auditor review is a v0.6+ framework item and will apply to a future revision of this assessment when the third-party certification form ships.

---

*End of Tier 1 Executive Summary. Detailed technical findings in [`self-assessment.md`](./self-assessment.md). ADR remediation backlog in [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md).*
