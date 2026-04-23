# Adoption Workstream

*Companion artefacts that make the Blast Radius Framework easier to apply, evidence, translate, and distribute.*

This directory exists to close the **supporting adoption gaps** identified in [`../oecd-catalogue-assessment.md`](../oecd-catalogue-assessment.md) §6.

The framework and spec already define:

- the rating model
- the profile shape
- the invariant tests
- the attestation form

What this directory adds is the operational layer around those forms:

- which external tools can generate usable BRF evidence
- what a future benchmark harness should look like
- how a vendor questionnaire can be turned into a draft BR profile
- what BRF component cards should contain
- how to translate BRF into adjacent governance regimes
- how BRF should show up in the OECD ecosystem

## Files

1. [`gap-closure-plan.md`](./gap-closure-plan.md) — the task list and execution order for the six gaps surfaced by the OECD assessment.
2. [`external-tools-mapping.md`](./external-tools-mapping.md) — evidence-adapter annex mapping adjacent tools and metrics into BRF claims.
3. [`benchmark-harness-design.md`](./benchmark-harness-design.md) — design note for a BRF benchmark and invariant-test companion repo.
4. [`questionnaire-profile-conversion.md`](./questionnaire-profile-conversion.md) — design note for converting the vendor questionnaire into a valid draft BR profile.
5. [`component-cards.md`](./component-cards.md) — proposed BRF-native card formats for models, datasets, tools, dependencies, and evidence anchors.
6. [`crosswalk-nist-ai-rmf.md`](./crosswalk-nist-ai-rmf.md) — first published crosswalk, translating BRF into NIST AI RMF terms.
7. [`crosswalk-iso-42001.md`](./crosswalk-iso-42001.md) — second published crosswalk, translating BRF into ISO/IEC 42001 management-system terms.
8. [`crosswalk-eu-ai-act.md`](./crosswalk-eu-ai-act.md) — third published crosswalk, translating BRF into EU AI Act obligations and evidence posture.
9. [`crosswalk-specialist-underwriters.md`](./crosswalk-specialist-underwriters.md) — fourth published crosswalk, translating BRF into public specialist-market underwriting and assurance criteria.
10. [`crosswalks-roadmap.md`](./crosswalks-roadmap.md) — completed-sequence note plus any future expansion of the crosswalk set.
11. [`oecd-visibility-plan.md`](./oecd-visibility-plan.md) — plan for making BRF discoverable inside the OECD catalogue ecosystem.

## How to use this directory

1. Read [`gap-closure-plan.md`](./gap-closure-plan.md) first.
2. Use [`external-tools-mapping.md`](./external-tools-mapping.md) when deciding whether evidence from an adjacent tool can support a BR profile or attestation.
3. Use the design notes and the component-card schema in [`../spec/`](../spec/) when building companion repositories or implementation work.
4. Read the four published crosswalks — [`crosswalk-nist-ai-rmf.md`](./crosswalk-nist-ai-rmf.md), [`crosswalk-iso-42001.md`](./crosswalk-iso-42001.md), [`crosswalk-eu-ai-act.md`](./crosswalk-eu-ai-act.md), and [`crosswalk-specialist-underwriters.md`](./crosswalk-specialist-underwriters.md) — then use [`crosswalks-roadmap.md`](./crosswalks-roadmap.md) for any future expansion.
5. Use [`oecd-visibility-plan.md`](./oecd-visibility-plan.md) for market-facing packaging work.

These artefacts are intentionally practical. They do not change framework definitions. They make the framework easier to operationalise.
