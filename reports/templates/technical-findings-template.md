# Technical Findings Template — Tier 2

*Detailed architectural assessment for the architecture team and auditors.*

**Template version:** 1.0
**For framework version:** v0.5.1 or later
**Licence:** CC-BY-4.0
**Companion templates:** [`executive-summary-template.md`](./executive-summary-template.md) (Tier 1), [`adr-backlog-template.md`](./adr-backlog-template.md) (Tier 3)

---

## Purpose and audience

Tier 2 is the detailed assessment an architecture lead, senior engineer, or independent auditor consumes. It links to the machine-readable profile ([`br-profile.schema.json`](../../spec/br-profile.schema.json)) and cites specific framework sections. Length is whatever the system requires — depth over brevity.

Tier 2 is authoritative on factual claims; Tier 1 (executive summary) summarises Tier 2 in plain English; Tier 3 (ADR backlog) derives its remediation items from Tier 2's §9 gaps.

**Replace all `[SQUARE_BRACKET_PLACEHOLDERS]`** with your values.

---

# [SYSTEM_NAME] — Blast Radius Technical Findings

**Date of assessment:** [YYYY-MM-DD]
**Framework version:** [e.g. v0.5.1]
**Machine-readable profile:** `[SYSTEM_NAME]-profile.json` (conformant to [`br-profile.schema.json`](../../spec/br-profile.schema.json))
**Assessor:** [name / organisation]

## 1. System under assessment

**Scope statement:** *[What system is being rated, at what boundary, for what deployment context. Example: "The integrated Lane2 governance platform as deployed for a regulated-review workflow in the financial-services sector, inclusive of DOP + aARP + SAPP evidence-anchoring layer + PACT pack."]*

**Components rated:**
- **[COMPONENT_1_NAME]** — [brief description]
- **[COMPONENT_2_NAME]** — [brief description]
- **…**

**Composition topology** (per framework §7.2): *[T1 sub-additive / T2 super-additive / T3 multiplicative / T4 exponential-reducing / mixed / single-component]*

**Principal population** (per framework §4.2 R-axis sub-component): *[single_user / single_team / single_org / multi_tenant_small / multi_tenant_large / public]* — estimated count [N]

## 2. Pre-rating classifier (framework §4.0)

For each component, worldview is:

| Component | Worldview | Evidence |
|---|---|---|
| [COMPONENT_1] | closed-world | *[Evidence: ontology-bounded inputs; typed inter-component interfaces; scope structurally enforced]* |
| [COMPONENT_2] | closed-world | *[…]* |

If *any* component is open-world, state: "Open-world component present. System effective BR floor is BR-4 per §4.0 regardless of per-axis scores." Skip to §7 aggregation.

## 3. Per-component ratings

For each component:

### [COMPONENT_NAME]

**Tuple:** A[X]–R[X]–C[X]–V[X]–K[X]–O[X]

| Axis | Tier | Justification |
|---|---|---|
| A (Authority) | [A0-A4] | *[one-sentence justification referencing evidence]* |
| R (Reach) | [R1-R4] | *[...]* |
| C (Coupling) | [C1, C2, C3, C4a, C4b] | *[...]* |
| V (Reversibility) | [V1-V4] | *[...]* with recovery horizon *[value]* |
| K (Consequence) | [K1, K2, K3-F/L/P, K4-S/R/F] | *[...]* |
| O (Observability) | [O0-O4] | *[...]* |

**Modifiers:**
- δ_adv: *[0 / +1 / +2]* — *[one line on adversarial analysis status]*
- τ: *[stable / expanding / drifting]* — last review [DATE], cadence *[value]*

[Repeat for each component.]

## 4. Composition

**Topology:** *[T1/T2/T3/T4/mixed — per §7.2]*

**Component edges:**
| From | To | Interface type | Notes |
|---|---|---|---|
| [COMP_1] | [COMP_2] | typed | *[e.g. capability request]* |
| … | | | |

**If T4 claimed, independence attestation** (per schema `composition.t4_independence_attestation`): [Yes/No on each: different model families; different providers; different prompt derivations; uncorrelated failure history; evidence reference]

## 5. Invariant attestations (framework §9)

| # | Invariant | Status | Enforcement mode | Evidence summary |
|---|---|---|---|---|
| I1 | Deterministic execution | [holds/partially/doesn't/n/a] | [architectural/structural/procedural/documentary] | *[brief]* |
| I2 | Evidence binding | […] | […] | *[...]* |
| I3 | Policy snapshot coherence | […] | […] | *[...]* |
| I4 | Bounded blast radius | […] | […] | *[...]* |
| I5 | Jurisdictional awareness | […] | […] | *[...]* |
| I6 | Fail-closed execution control | […] | […] | *[...]* |
| I7 | Bounded coupling | […] | […] | *[...]* |

**Conformance test results** (per [`spec/invariant-conformance-tests.md`](../../spec/invariant-conformance-tests.md) — list results per test ID run):
- *[I1-T1: pass | partial | fail | not_run — evidence URI]*
- *[...]*

## 6. Anti-pattern attestations

Each of the 26 anti-patterns in [`antipatterns.md`](../../antipatterns.md) receives one of:
- `not_exhibited`
- `exhibited_with_demotion_path` (with the path described)
- `exhibited_without_demotion_path`
- `not_applicable`

| ID | Pattern | Status | Demotion path / evidence |
|---|---|---|---|
| A1 | A2A public capability discovery | […] | *[...]* |
| A2 | API-agent-ready / API-first tool exposure | […] | *[...]* |
| … (all 15 Part A) | | | |
| B1 | Application logs as "evidence" | […] | *[...]* |
| … (all 11 Part B) | | | |

## 7. Aggregation

**Base class** (max over axes): BR-[X]

**Interaction overrides** (per §5.1):
| Rule | Triggered? | Effect |
|---|---|---|
| 1 — C4a/b + V≥3 | [yes/no] | *[result]* |
| 2 — A≥3 + K4 (minimum BR-4 floor) | [yes/no] | *[result]* |
| 3 — R4 + O≤1 | [yes/no] | *[result]* |
| 4 — Invariant 7 absent (partial) | [yes/no] | *[result]* |
| Pre-rating open-world component present | [yes/no] | *[result]* |
| O0/O1 on BR-3+ | [yes/no] | *[result]* |
| O4 demotion (requires V≤2 + all invariants hold) | [yes/no] | *[result]* |

**Final ordinal class:** BR-[X]

**Floor analysis:** *[if rule 2 fires (A≥3 + K4), state explicitly that BR-4 is a floor not a cap; even if O4 demotion were eligible, the floor prevents demotion below BR-4 for this consequence domain]*

**Cardinal score** (if Kalman Phase 1+ implemented): **B̂(t|t) = [VALUE] ± [σ_B(t)]**
- Weight vector: *[w_a, w_r, w_c, w_v, w_k, w_o]*
- Kalman phase: *[0/1/2/3]*
- Evidence-tier → R_K mapping reference: *[URI or "internal"]*

If cardinal score is not computable (Invariants 1 or 2 do not hold): state "Cardinal score not produced — Invariant [1/2] prerequisite not met; system is ordinal-rateable but not underwriter-priceable until prerequisite closed."

## 8. Residual vs inherent

- **Inherent BR** (absent mitigating controls): BR-[X]
- **Residual BR** (with controls operating as designed): BR-[Y]
- **Controls narrowing the gap:**
  - *[control 1]*
  - *[control 2]*

## 9. Gaps and open items

Honest enumeration of gaps surfaced by this assessment. These seed the Tier 3 ADR backlog.

- **Gap #1:** *[description]*. Impact: *[axis/invariant/anti-pattern affected]*. Surfaced via: *[test ID / review observation / external evidence]*.
- **Gap #2:** *[...]*
- **Gap #3:** *[...]*

If fewer than one gap surfaces, the assessment has not been applied honestly and should be re-run. See [`../../authoring-notes.md`](../../authoring-notes.md) on the force-function method.

## 10. Evidence references

- Machine-readable profile: `[SYSTEM_NAME]-profile.json`
- Conformance test results: *[URI or directory]*
- Signed attestation: *[signature file + anchor reference]* (required at BR-3+)
- Prior assessments: *[list with dates]*

## 11. Assessor attestation

Assessor attests that the rating above reflects honest application of framework v[VERSION] against the system as observed on [DATE], within the IP and scope boundaries stated in §1. Residual uncertainty is reflected in σ_B(t) where computable and in §9 gaps otherwise.

**Signed:** ___________________________ *(assessor, date)*

---

*End of Tier 2. Executive summary in [`executive-summary-template.md`](./executive-summary-template.md). Remediation backlog in [`adr-backlog-template.md`](./adr-backlog-template.md).*

## Worked example

A filled Tier 2 technical assessment, produced by Lane2 applying the framework to its own integrated stack, lives at [`../lane2/self-assessment.md`](../lane2/self-assessment.md) with machine-readable profile at [`../lane2/self-assessment.json`](../lane2/self-assessment.json). The lane2/ example has been revised seven times under the force-function method (see [`../../authoring-notes.md`](../../authoring-notes.md) and [`../../CHANGELOG.md`](../../CHANGELOG.md) v0.5.2 through v0.5.7 entries).
