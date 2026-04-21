# Blast Radius Report Template

*Three-tier report format for applying the Blast Radius Framework to a deployed or proposed agentic AI system.*

**For framework version:** v0.5.1 or later
**Template version:** 1.0
**Last updated:** 2026-04-21
**Licence:** CC-BY-4.0 (same as the framework)

---

## How to use this template

This template turns a Blast Radius rating into three audiences' worth of output from one engagement:

- **Tier 1 — Executive summary** for decision-making managers who need the business consequence in plain English
- **Tier 2 — Technical findings** for the architecture team doing the detailed rating
- **Tier 3 — ADR remediation backlog** for the architecture team's follow-up work on surfaced gaps

A complete Blast Radius report consists of three files (or three clearly-marked sections of one file):

```
{system-name}-exec-summary.md           — Tier 1, 1–2 pages, non-technical
{system-name}-technical-findings.md     — Tier 2, detailed, schema-linked
{system-name}-adr-backlog.md            — Tier 3, prioritised ADR candidates
```

Plus the machine-readable profile `{system-name}-profile.json` conforming to [`spec/br-profile.schema.json`](./spec/br-profile.schema.json).

Each tier is self-contained. A reader can consume any one without reading the others. Cross-references between tiers are preferred over restating content.

**Replace all `[SQUARE_BRACKET_PLACEHOLDERS]` with your values.** Placeholders are also tagged with a short note about what goes there. Remove the notes in the final report.

---

## Tier 1 — Executive Summary Template

*Target length: 1–2 pages. Target reader: accountable executive, board member, procurement head, risk officer, specialist underwriter. No framework jargon without a plain-English gloss.*

---

### [SYSTEM_NAME] — Blast Radius Report, Executive Summary

**Date of assessment:** [YYYY-MM-DD]
**Framework version:** [e.g. v0.5.1]
**Assessor:** [name / organisation]
**Accountable executive:** [name, role]

### 1. Headline

**[SYSTEM_NAME]** is rated **Blast Radius class [BR-1 | BR-2 | BR-3 | BR-4 | BR-5]** against framework version [VERSION].

In plain English: *[one sentence explaining what that class means for this system — e.g., "This is a systemic system: failures can affect multiple tenants, some decisions are hard to reverse, and the consequence domain is regulated. Governance requires architectural guarantees, not only process controls."]*

### 2. What this means for the business

Three concrete impacts, in decreasing order of material consequence:

1. **[Regulatory / insurability / operational headline #1].** *[One or two sentences. Example: "Under the EU AI Act Article 12 logging obligations, evidence retention must be tamper-evident and externally anchored. Our current implementation uses application logs, which do not satisfy the requirement. A regulator audit today would find us non-compliant on this specific clause."]*
2. **[Headline #2].** *[Example: "Specialist underwriters (Munich Re aiSure, AIUC, Armilla/Lloyd's) require reproducible decision trails and policy-snapshot coherence as a minimum pricing input. The current system does not produce these. The commercial consequence is that deployments in the target regulated sector will either be excluded from coverage under Verisk 2026 terms, or priced with a conservative risk loading that makes the business case marginal."]*
3. **[Headline #3].** *[Example: "Operational risk: one legacy integration accepts natural-language input from a counterparty system, which breaks the framework's bounded-coupling invariant on that hop and promotes the entire corridor one class higher than the rest of the architecture would indicate. Closing this single interface moves the system from BR-5 to BR-4."]*

### 3. Top three remediation priorities

| # | Remediation | Effort | Estimated cost | Tier class change |
|---|---|---|---|---|
| 1 | *[e.g. "Replace application logs with externally-anchored Merkle-proof evidence"]* | *[weeks / months / quarters]* | *[band]* | *[moves from BR-X to BR-Y on this axis]* |
| 2 | *[…]* | | | |
| 3 | *[…]* | | | |

Detailed remediation backlog in the Tier 3 document (`[SYSTEM_NAME]-adr-backlog.md`).

### 4. Insurability posture

- **Current position under specialist-underwriter criteria (as of [DATE]):** *[Coverable / coverable with conditions / not coverable]*
- **Position under Verisk 2026 commercial insurance AI exclusions:** *[Covered / excluded / uncertain]*
- **Gap to Consolidation Zone (framework §14 Quadrant IV — BR-2/BR-3 with Invariants 1–7 intact):** *[List the 2–3 invariants or axis tiers that block]*

*[If the system is commercially uninsurable, state it explicitly. This is a board-level fact.]*

### 5. Recommendation

Choose one:

- [ ] **Proceed as-is.** The rating is acceptable for the stated deployment context. No material remediation required.
- [ ] **Proceed with parallel remediation.** The rating is acceptable for current operation; Tier 3 backlog to be executed in parallel to reduce residual BR over [timeframe].
- [ ] **Pause and remediate before proceeding.** The current rating does not meet the stated deployment context's requirements (regulatory / insurability / operational). Remediation must complete before production deployment / continued operation.
- [ ] **Redesign.** Required BR class cannot be reached from the current architecture without fundamental redesign of [specific component / composition topology / evidence chain]. Recommend pause and architectural restart.

**Justification:** *[One paragraph explaining which option and why]*

### 6. Sign-off

I have reviewed this Executive Summary. The rating and remediation path stated above represent my understanding of the system's current Blast Radius posture and the actions required to maintain or improve it.

**Signed:** ___________________________ *(name, role, date)*

**Witnessed:** ___________________________ *(assessor, date)*

---

*End of Tier 1. Detailed technical findings follow in `[SYSTEM_NAME]-technical-findings.md` (or the narrative self-assessment document). Remediation backlog in `[SYSTEM_NAME]-adr-backlog.md`.*

---

## Tier 2 — Technical Findings Template

*Target length: as detailed as needed. Target reader: architecture lead, senior engineer, auditor. Links to the machine-readable profile and to specific framework sections.*

---

### [SYSTEM_NAME] — Blast Radius Technical Findings

**Date of assessment:** [YYYY-MM-DD]
**Framework version:** [e.g. v0.5.1]
**Machine-readable profile:** `[SYSTEM_NAME]-profile.json` (conformant to `spec/br-profile.schema.json`)
**Assessor:** [name / organisation]

### 1. System under assessment

**Scope statement:** *[What system is being rated, at what boundary, for what deployment context. Example: "The integrated Lane2 governance platform as deployed for a regulated-review workflow in the financial-services sector, inclusive of DOP + aARP + SAPP evidence-anchoring layer + PACT pack."]*

**Components rated:**
- **[COMPONENT_1_NAME]** — [brief description]
- **[COMPONENT_2_NAME]** — [brief description]
- **…**

**Composition topology** (per framework §7.2): *[T1 sub-additive / T2 super-additive / T3 multiplicative / T4 exponential-reducing / mixed / single-component]*

**Principal population** (per framework §4.2 R-axis sub-component): *[single_user / single_team / single_org / multi_tenant_small / multi_tenant_large / public]* — estimated count [N]

### 2. Pre-rating classifier (framework §4.0)

For each component, worldview is:

| Component | Worldview | Evidence |
|---|---|---|
| [COMPONENT_1] | closed-world | *[Evidence: ontology-bounded inputs; typed inter-component interfaces; scope structurally enforced]* |
| [COMPONENT_2] | closed-world | *[…]* |

If *any* component is open-world, state: "Open-world component present. System effective BR floor is BR-4 per §4.0 regardless of per-axis scores." Skip to §7 aggregation.

### 3. Per-component ratings

For each component:

#### [COMPONENT_NAME]

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

### 4. Composition

**Topology:** *[T1/T2/T3/T4/mixed — per §7.2]*

**Component edges:**
| From | To | Interface type | Notes |
|---|---|---|---|
| [COMP_1] | [COMP_2] | typed | *[e.g. aARP capability request]* |
| … | | | |

**If T4 claimed, independence attestation** (per schema `composition.t4_independence_attestation`): [Yes/No on each: different model families; different providers; different prompt derivations; uncorrelated failure history; evidence reference]

### 5. Invariant attestations (framework §9)

| # | Invariant | Status | Enforcement mode | Evidence summary |
|---|---|---|---|---|
| I1 | Deterministic execution | [holds/partially/doesn't/n/a] | [architectural/structural/procedural/documentary] | *[brief]* |
| I2 | Evidence binding | […] | […] | *[...]* |
| I3 | Policy snapshot coherence | […] | […] | *[...]* |
| I4 | Bounded blast radius | […] | […] | *[...]* |
| I5 | Jurisdictional awareness | […] | […] | *[...]* |
| I6 | Fail-closed execution control | […] | […] | *[...]* |
| I7 | Bounded coupling | […] | […] | *[...]* |

**Conformance test results** (per `spec/invariant-conformance-tests.md` — list results per test ID run): 
- *[I1-T1: pass | partial | fail | not_run — evidence URI]*
- *[...]*

### 6. Anti-pattern attestations

Each of the 26 anti-patterns in [`antipatterns.md`](./antipatterns.md) receives one of:
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

### 7. Aggregation

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

**Cardinal score** (if Kalman Phase 1+ implemented): **B̂(t|t) = [VALUE] ± [σ_B(t)]**
- Weight vector: *[w_a, w_r, w_c, w_v, w_k, w_o]*
- Kalman phase: *[0/1/2/3]*
- Evidence-tier → R_K mapping reference: *[URI or "internal"]*

If cardinal score is not computable (Invariants 1 or 2 do not hold): state "Cardinal score not produced — Invariant [1/2] prerequisite not met; system is ordinal-rateable but not underwriter-priceable until prerequisite closed."

### 8. Residual vs inherent

- **Inherent BR** (absent mitigating controls): BR-[X]
- **Residual BR** (with controls operating as designed): BR-[Y]
- **Controls narrowing the gap:**
  - *[control 1]*
  - *[control 2]*

### 9. Gaps and open items

Honest enumeration of gaps surfaced by this assessment. These seed the Tier 3 ADR backlog.

- **Gap #1:** *[description]*. Impact: *[axis/invariant/anti-pattern affected]*. Surfaced via: *[test ID / review observation / external evidence]*.
- **Gap #2:** *[...]*
- **Gap #3:** *[...]*

If fewer than one gap surfaces, the assessment has not been applied honestly and should be re-run.

### 10. Evidence references

- Machine-readable profile: `[SYSTEM_NAME]-profile.json`
- Conformance test results: *[URI or directory]*
- Signed attestation: *[signature file + anchor reference]* (required at BR-3+)
- Prior assessments: *[list with dates]*

### 11. Assessor attestation

Assessor attests that the rating above reflects honest application of framework v[VERSION] against the system as observed on [DATE], within the IP and scope boundaries stated in §1. Residual uncertainty is reflected in σ_B(t) where computable and in §9 gaps otherwise.

**Signed:** ___________________________ *(assessor, date)*

---

*End of Tier 2. Remediation backlog follows in `[SYSTEM_NAME]-adr-backlog.md`.*

---

## Tier 3 — ADR Remediation Backlog Template

*Target length: one row per ADR candidate. Target reader: architecture team authoring the follow-up ADRs. Prioritised and bounded.*

---

### [SYSTEM_NAME] — Blast Radius ADR Remediation Backlog

**Date:** [YYYY-MM-DD]
**Derived from assessment:** `[SYSTEM_NAME]-technical-findings.md` (or the narrative assessment)
**Framework version:** [e.g. v0.5.1]

### Scope note

Items below are **ADR candidates**, not prescribed ADRs. The deployer's architecture team authors the actual ADRs in their own register, makes local decisions about scope and approach, and owns the implementation. This backlog surfaces gaps and proposes the *shape* of an ADR that would close each gap; it does not dictate the solution.

Priority column uses impact × feasibility:
- **P0** — blocks the stated deployment context (e.g. current rating disqualifies production)
- **P1** — material class-change potential within one quarter
- **P2** — material class-change potential within one year
- **P3** — hygiene; improves σ_B(t) or residual-vs-inherent gap but does not change ordinal class

### Backlog

| Priority | Proposed ADR title | Scope summary | Dependencies | Effort band | Class impact |
|---|---|---|---|---|---|
| P[0-3] | *[proposed ADR title — imperative form, e.g. "Replace application-log evidence with externally-anchored Merkle-proof evidence"]* | *[one-paragraph scope — what the ADR would decide, not how]* | *[other ADRs / infrastructure / vendors this depends on]* | *[days / weeks / months / quarters]* | *[axis/invariant/anti-pattern affected; class delta if implemented]* |
| … | | | | | |

### Cross-references

Each row should link to:

- **Framework sections** that motivate the gap (e.g. §9 Invariant 2, antipatterns.md B1)
- **Test IDs** (if any) that failed or partially-failed in conformance testing
- **Profile fields** in `[SYSTEM_NAME]-profile.json` that would change once the ADR is implemented

### Dependency graph

*[Optional: sketch the dependency order among backlog items. ADR candidates that unblock other work should be sequenced first. Items with circular dependencies should be decomposed.]*

### Out of scope for this backlog

- *[Items discussed during assessment but deemed outside the remediation mandate — e.g. "Changes to the PACT pack ontology are governed by a separate standards process and are not ADR candidates here"]*
- *[Other exclusions]*

### Review and ownership

Backlog owner: *[name, role]*
Review cadence: *[monthly / per-release / per-incident]*
Re-assessment trigger: *[when this backlog is consumed in full, re-run the full framework assessment; expected date [DATE]]*

---

*End of Tier 3. End of report.*

---

## Template notes

**What the three tiers do not cover:**

- **Runbooks.** Operational runbooks for incident response, kill-switch exercise, rollback drills are separate artefacts referenced from but not produced by this template.
- **Contractual language.** Procurement contract clauses (SLA, liability allocation, regulatory warranties) derived from the rating are separate deliverables.
- **Attestation signing.** Producing the signed + anchored attestation per `spec/attestation-format.md` is a separate step that consumes the `[SYSTEM_NAME]-profile.json`.
- **Third-party review.** Independent auditor review of a Lane2 self-assessment, or any assessment, is a separate engagement. This template supports self-attestation at default scope.

**Versioning this template:**

Template is versioned independently of framework. Current: 1.0. Minor updates (wording, added examples) will be 1.x; additions to tier structure or acceptance criteria will be 2.x. External reports produced from this template should state both template version and framework version.

**Licence reminder:**

This template is CC-BY-4.0 (same as the framework). Derivative works are welcome with attribution. Commercial use including fee-for-assessment engagements is permitted. If you produce assessments using this template and want to be cited as a practitioner, open an issue on the repository.
