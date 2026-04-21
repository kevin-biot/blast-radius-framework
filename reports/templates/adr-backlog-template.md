# ADR Remediation Backlog Template — Tier 3

*Prioritised list of ADR candidates for the architecture team's follow-up work.*

**Template version:** 1.0
**For framework version:** v0.5.1 or later
**Licence:** CC-BY-4.0
**Companion templates:** [`executive-summary-template.md`](./executive-summary-template.md) (Tier 1), [`technical-findings-template.md`](./technical-findings-template.md) (Tier 2)

---

## Purpose and audience

Tier 3 is consumed by the architecture team doing remediation. It lists **ADR candidates** — proposed shapes for architectural decision records the deployer's team will author — derived from the §9 gaps in the Tier 2 technical findings.

Crucially: Tier 3 items are *candidates*, not prescriptions. The deployer authors the actual ADRs in their own register, makes local decisions about scope and approach, and owns the implementation. This backlog surfaces *what is wrong and proposes the shape of the ADR that would close it*; it does not dictate the solution.

**Replace all `[SQUARE_BRACKET_PLACEHOLDERS]`** with your values.

---

# [SYSTEM_NAME] — Blast Radius ADR Remediation Backlog

**Date:** [YYYY-MM-DD]
**Derived from assessment:** [`[SYSTEM_NAME]-technical-findings.md`](./) (or the narrative Tier 2 document)
**Framework version:** [e.g. v0.5.1]

## Scope note

Items below are **ADR candidates**, not prescribed ADRs. The deployer's architecture team authors the actual ADRs in their own register, makes local decisions about scope and approach, and owns the implementation. This backlog surfaces gaps and proposes the *shape* of an ADR that would close each gap; it does not dictate the solution.

**Priority legend:**

- **P0** — blocks the stated deployment context (e.g. current rating disqualifies production)
- **P1** — material class-change potential within one quarter
- **P2** — material class-change potential within one year, or material residual-gap-closure
- **P3** — hygiene; improves σ_B(t) or residual-vs-inherent gap but does not change ordinal class

## Backlog

| # | Priority | Proposed ADR title | Scope summary | Dependencies | Effort band | Class / invariant impact |
|---|---|---|---|---|---|---|
| 1 | P[0-3] | *[proposed ADR title — imperative form, e.g. "Replace application-log evidence with externally-anchored Merkle-proof evidence"]* | *[one-paragraph scope — what the ADR would decide, not how]* | *[other ADRs / infrastructure / vendors this depends on]* | *[days / weeks / months / quarters]* | *[axis/invariant/anti-pattern affected; class delta if implemented]* |
| … | | | | | | |

## Cross-references

Each row should link to:

- **Framework sections** that motivate the gap (e.g. [`framework.md §9 Invariant 2`](../../framework.md), [`antipatterns.md B1`](../../antipatterns.md))
- **Test IDs** (if any) that failed or partially-failed in conformance testing (from [`spec/invariant-conformance-tests.md`](../../spec/invariant-conformance-tests.md))
- **Profile fields** in `[SYSTEM_NAME]-profile.json` that would change once the ADR is implemented

## Dependency graph

*[Optional: sketch the dependency order among backlog items. ADR candidates that unblock other work should be sequenced first. Items with circular dependencies should be decomposed.]*

## Out of scope for this backlog

- *[Items discussed during assessment but deemed outside the remediation mandate — e.g. "Changes to the ontology are governed by a separate standards process and are not ADR candidates here"]*
- *[Other exclusions]*

## Review and ownership

**Backlog owner:** *[name, role]*
**Review cadence:** *[monthly / per-release / per-incident]*
**Re-assessment trigger:** *[when this backlog is consumed in full, re-run the full framework assessment; expected date [DATE]]*

---

*End of Tier 3. End of report.*

## Worked example

A filled Tier 3 backlog, produced by Lane2 applying the framework to its own integrated stack, lives at [`../lane2/self-assessment-adr-backlog.md`](../lane2/self-assessment-adr-backlog.md). It contains 12 ADR candidates across P0–P3 with dependency graph and cross-references.
