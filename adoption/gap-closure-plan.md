# Gap Closure Plan

*Task list for the six BRF adoption gaps made more visible by the OECD Catalogue of Tools & Metrics for Trustworthy AI.*

**Source:** [`../oecd-catalogue-assessment.md`](../oecd-catalogue-assessment.md) §6
**Status:** Initial execution pass
**Date:** 2026-04-23

---

## 1. Purpose

This plan turns the six gaps named in the OECD assessment into explicit work items. The objective is not to change the framework's core theory. The objective is to make BRF:

- easier to evidence
- easier to implement
- easier to translate into adjacent governance language
- easier to discover by readers who start from the OECD ecosystem rather than this repository

---

## 2. Task list

| Order | Gap | Deliverable in this repo | Status in this pass |
|---|---|---|---|
| 1 | Missing evidence adapters | [`external-tools-mapping.md`](./external-tools-mapping.md) | completed |
| 2 | Missing reference harness | [`benchmark-harness-design.md`](./benchmark-harness-design.md) | completed |
| 3 | Missing questionnaire-to-profile tooling | [`questionnaire-profile-conversion.md`](./questionnaire-profile-conversion.md) | completed |
| 4 | Missing component-card layer | [`component-cards.md`](./component-cards.md) | completed |
| 5 | Missing public crosswalks | [`crosswalks-roadmap.md`](./crosswalks-roadmap.md) | completed |
| 6 | Missing OECD-ecosystem visibility | [`oecd-visibility-plan.md`](./oecd-visibility-plan.md) | completed |

This pass produces the missing design-and-translation artefacts. It does **not** implement the companion repos or crosswalk documents themselves. It defines the shape they should take so implementation can proceed without re-deriving scope.

---

## 3. Worked one by one

### 3.1 Gap 1 — missing evidence adapters

Problem:
- adjacent tools exist
- BRF lacked a public map showing how their outputs support BRF claims

Action:
- produce [`external-tools-mapping.md`](./external-tools-mapping.md)

Exit condition for this pass:
- a deployer can look up a tool and see which BRF axis, invariant, or modifier it can support
- admissibility limits are stated so evidence is not over-claimed

### 3.2 Gap 2 — missing reference harness

Problem:
- the spec names tests but does not yet define the reference harness shape

Action:
- produce [`benchmark-harness-design.md`](./benchmark-harness-design.md)

Exit condition for this pass:
- a future companion repo can be started from a clear architecture, result-bundle format, and execution model

### 3.3 Gap 3 — missing questionnaire-to-profile tooling

Problem:
- BRF has a prose questionnaire and a machine-readable schema, but no bridge between them

Action:
- produce [`questionnaire-profile-conversion.md`](./questionnaire-profile-conversion.md)

Exit condition for this pass:
- a future converter can be built without ambiguity about inputs, outputs, warnings, or unresolved evidence handling

### 3.4 Gap 4 — missing component-card layer

Problem:
- BRF is strong on whole-system profiles but light on component-level documentation patterns

Action:
- produce [`component-cards.md`](./component-cards.md)

Exit condition for this pass:
- component-card types and minimum fields are defined tightly enough to guide implementation

### 3.5 Gap 5 — missing public crosswalks

Problem:
- readers need BRF translated into regimes they already know

Action:
- produce [`crosswalks-roadmap.md`](./crosswalks-roadmap.md)

Exit condition for this pass:
- priority order, source artefacts, and output shapes are defined for the first crosswalk publications

### 3.6 Gap 6 — missing OECD-ecosystem visibility

Problem:
- BRF is useful to OECD-catalogue users, but currently invisible in that discovery surface

Action:
- produce [`oecd-visibility-plan.md`](./oecd-visibility-plan.md)

Exit condition for this pass:
- the submission posture, metadata, dependencies, and sequencing are defined

---

## 4. Next implementation sequence

This is the recommended build order after this planning pass:

1. Implement the evidence-adapter annex as living guidance and extend it as tools change.
2. Stand up the benchmark-harness companion repo.
3. Stand up questionnaire-to-profile conversion tooling.
4. Publish the component-card format.
5. Publish the first crosswalk, starting with NIST AI RMF.
6. Submit BRF to the OECD catalogue and then submit a worked example.

That order is intentional:

- evidence adapters make the framework easier to use immediately
- the harness and converter make it easier to generate attestable artefacts
- component cards make evidence packets cleaner
- crosswalks and OECD visibility make the framework easier to buy, audit, and discover
