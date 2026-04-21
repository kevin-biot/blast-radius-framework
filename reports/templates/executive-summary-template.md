# Executive Summary Template — Tier 1

*Non-technical summary for decision-making managers.*

**Template version:** 1.0
**For framework version:** v0.5.1 or later
**Licence:** CC-BY-4.0
**Companion templates:** [`technical-findings-template.md`](./technical-findings-template.md) (Tier 2), [`adr-backlog-template.md`](./adr-backlog-template.md) (Tier 3)

---

## Purpose and audience

Tier 1 is the **one-to-two-page** document a board member, accountable executive, procurement head, risk officer, or specialist underwriter reads *first*. It must produce a clear BR class, the business consequences, the remediation priorities, and the insurability posture — in plain English, without framework jargon that forces the reader to consult [`NOTATION.md`](../../NOTATION.md) mid-read.

A reader who cannot state the BR class, top-3 impacts, and top-3 remediations in plain English after one read of this tier has a template that failed its job. That is the pass criterion.

**Replace all `[SQUARE_BRACKET_PLACEHOLDERS]`** with your values. Placeholders carry a short note about what goes there; remove the notes in the final report.

---

# [SYSTEM_NAME] — Blast Radius Report, Executive Summary

**Date of assessment:** [YYYY-MM-DD]
**Framework version:** [e.g. v0.5.1]
**Assessor:** [name / organisation]
**Accountable executive:** [name, role]

## 1. Headline

**[SYSTEM_NAME]** is rated **Blast Radius class [BR-1 | BR-2 | BR-3 | BR-4 | BR-5]** against framework version [VERSION].

In plain English: *[one sentence explaining what that class means for this system — e.g., "This is a systemic system: failures can affect multiple tenants, some decisions are hard to reverse, and the consequence domain is regulated. Governance requires architectural guarantees, not only process controls."]*

## 2. What this means for the business

Three concrete impacts, in decreasing order of material consequence:

1. **[Regulatory / insurability / operational headline #1].** *[One or two sentences. Example: "Under the EU AI Act Article 12 logging obligations, evidence retention must be tamper-evident and externally anchored. Our current implementation uses application logs, which do not satisfy the requirement. A regulator audit today would find us non-compliant on this specific clause."]*
2. **[Headline #2].** *[Example: "Specialist underwriters (Munich Re aiSure, AIUC, Armilla/Lloyd's) require reproducible decision trails and policy-snapshot coherence as a minimum pricing input. The current system does not produce these. The commercial consequence is that deployments in the target regulated sector will either be excluded from coverage under Verisk 2026 terms, or priced with a conservative risk loading that makes the business case marginal."]*
3. **[Headline #3].** *[Example: "Operational risk: one legacy integration accepts natural-language input from a counterparty system, which breaks the framework's bounded-coupling invariant on that hop and promotes the entire corridor one class higher than the rest of the architecture would indicate. Closing this single interface moves the system from BR-5 to BR-4."]*

## 3. Top three remediation priorities

| # | Remediation | Effort | Estimated cost | Tier class change |
|---|---|---|---|---|
| 1 | *[e.g. "Replace application logs with externally-anchored Merkle-proof evidence"]* | *[weeks / months / quarters]* | *[band]* | *[moves from BR-X to BR-Y on this axis]* |
| 2 | *[…]* | | | |
| 3 | *[…]* | | | |

Detailed remediation backlog in [`[SYSTEM_NAME]-adr-backlog.md`](./[SYSTEM_NAME]-adr-backlog.md) (Tier 3 document).

## 4. Insurability posture

- **Current position under specialist-underwriter criteria (as of [DATE]):** *[Coverable / coverable with conditions / not coverable]*
- **Position under Verisk 2026 commercial insurance AI exclusions:** *[Covered / excluded / uncertain]*
- **Gap to Consolidation Zone** (framework §14 Quadrant IV — BR-2/BR-3 with Invariants 1–7 intact)**:** *[List the 2–3 invariants or axis tiers that block. Or state that the current BR class is the minimum achievable for the consequence domain, in which case the Consolidation Zone is reached at the current rating rather than requiring further compression.]*

*[If the system is commercially uninsurable, state it explicitly. This is a board-level fact.]*

## 5. Recommendation

Choose one:

- [ ] **Proceed as-is.** The rating is acceptable for the stated deployment context. No material remediation required.
- [ ] **Proceed with parallel remediation.** The rating is acceptable for current operation; Tier 3 backlog to be executed in parallel to reduce residual BR over [timeframe].
- [ ] **Pause and remediate before proceeding.** The current rating does not meet the stated deployment context's requirements (regulatory / insurability / operational). Remediation must complete before production deployment / continued operation.
- [ ] **Redesign.** Required BR class cannot be reached from the current architecture without fundamental redesign of [specific component / composition topology / evidence chain]. Recommend pause and architectural restart.

**Justification:** *[One paragraph explaining which option and why]*

## 6. Sign-off

I have reviewed this Executive Summary. The rating and remediation path stated above represent my understanding of the system's current Blast Radius posture and the actions required to maintain or improve it.

**Signed:** ___________________________ *(name, role, date)*

**Witnessed:** ___________________________ *(assessor, date)*

---

*End of Tier 1. Detailed technical findings in [`technical-findings-template.md`](./technical-findings-template.md) (or the narrative assessment document). Remediation backlog in [`adr-backlog-template.md`](./adr-backlog-template.md).*

## Worked example

A filled Tier 1 executive summary, produced by Lane2 applying the framework to its own integrated stack, lives at [`../lane2/self-assessment-exec-summary.md`](../lane2/self-assessment-exec-summary.md). Read it alongside this template if you want a concrete example of what "populated" looks like.
