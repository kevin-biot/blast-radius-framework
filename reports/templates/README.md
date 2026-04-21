# Report Templates

*Three reusable report templates, one per tier, for applying the Blast Radius Framework to any system.*

**Template version:** 1.0
**For framework version:** v0.5.1 or later
**Licence:** CC-BY-4.0

---

## The three tiers

| Template | Tier | Audience | Length target |
|---|---|---|---|
| [`executive-summary-template.md`](./executive-summary-template.md) | 1 | Accountable executive, board, procurement, risk officer, specialist underwriter | 1–2 pages, non-technical |
| [`technical-findings-template.md`](./technical-findings-template.md) | 2 | Architecture lead, senior engineer, auditor | As detailed as the system requires |
| [`adr-backlog-template.md`](./adr-backlog-template.md) | 3 | Architecture team's remediation work | One row per ADR candidate, prioritised |

Each tier is self-contained. A reader can consume any one without reading the others. A complete Blast Radius report uses all three plus a machine-readable profile conformant to [`../../spec/br-profile.schema.json`](../../spec/br-profile.schema.json).

## How to use

1. Pick the template for the tier you need
2. Replace all `[SQUARE_BRACKET_PLACEHOLDERS]` with your values
3. Remove the placeholder-note text (the *italic* guidance inside placeholders)
4. Cross-reference across tiers using relative links consistent with your report's location
5. Validate your machine-readable profile against the schema
6. Sign + anchor the attestation per [`../../spec/attestation-format.md`](../../spec/attestation-format.md) if at BR-3+

## What these templates are not

- **Not runbooks.** Operational runbooks for incident response, kill-switch exercise, rollback drills are separate artefacts that a Tier 2 / Tier 3 document can reference but does not produce.
- **Not contractual language.** Procurement contract clauses (SLA, liability allocation, regulatory warranties) derived from the rating are separate deliverables.
- **Not attestation signing.** The signed + anchored attestation per [`../../spec/attestation-format.md`](../../spec/attestation-format.md) is a separate step that consumes the machine-readable profile.
- **Not third-party review.** Independent auditor review of a self-assessment is a separate engagement. These templates support self-attestation at default scope.

## Design principles

- **Forms, not implementations.** The templates prescribe what a report looks like. How you produce one is your choice: your CI, your attestation service, your HSM, your pack registry.
- **Honesty is machine-checkable at the profile level.** The Tier 2 findings map onto the JSON Schema profile; the profile validates; corrections require version bumps with change-log entries.
- **Composition is first-class.** Tier 2 §4 (composition topology) and §7 (aggregation with interaction overrides) are both required. You cannot claim a BR rating without naming how your components compose.
- **Open-world is marked, not hidden.** Tier 2 §2 (worldview classifier) makes worldview explicit per component. Any open-world component forces BR-4 minimum per [`../../framework.md §4.0`](../../framework.md).
- **Force function is the authoring method.** See [`../../authoring-notes.md`](../../authoring-notes.md). A self-assessment produced by AI alone is not a self-assessment.

## Worked example

The first worked application of these templates is [`../lane2/`](../lane2/) — Lane2's own self-assessment. Readers producing their own reports should skim lane2/ for calibration of what "populated" looks like, specifically for how the tiers compose.

## Versioning

Templates are versioned independently of the framework. Current: 1.0. Minor updates (wording, added examples) will be 1.x; additions to tier structure or acceptance criteria will be 2.x. External reports produced from these templates should state both template version and framework version in their headers.
