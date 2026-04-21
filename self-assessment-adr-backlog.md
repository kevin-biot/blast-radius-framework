# Lane2 Self-Assessment — ADR Remediation Backlog

**Date:** 2026-04-21
**Derived from:** [`self-assessment.md`](./self-assessment.md) §9 (gaps) + §6 (anti-pattern attestations marked `exhibited_with_demotion_path`)
**Framework version:** v0.5.1

---

## Scope note

Items below are **ADR candidates**. Lane2's internal architecture team will author actual ADRs (DOP-N, SAPP-N, PACT-N, etc.) in the private ADR register. This backlog surfaces the gaps and proposes the *shape* of an ADR that would close each; it does not dictate the solution.

**Priority legend:**

- **P0** — blocks the stated deployment context
- **P1** — material class-change or residual-gap-closure potential within one quarter
- **P2** — material potential within one year
- **P3** — hygiene; improves σ_B(t) or residual-vs-inherent gap but does not change ordinal class

## Backlog

| # | Priority | Proposed ADR title | Scope summary | Dependencies | Effort band | Class / invariant impact |
|---|---|---|---|---|---|---|
| 1 | **P1** | **Kalman Phase 1 implementation on a pilot compliance metric** | Implement the scalar Kalman filter from framework.md §5.4 against a single compliance metric in a pilot deployment. Produce B̂(t\|t) and σ_B(t) numerically. Calibrate the evidence-tier → R_K mapping against the pilot's observed tier distribution. | A pilot deployment (any PoC engagement); a declared compliance metric (candidate: compliance-decision ratio). | months (pilot-dependent) | Closes Gap-1. Moves Lane2 from ordinal-rateable BR-4 to numerically priceable BR-4; unlocks specialist-underwriter pricing workflow. No ordinal class change. |
| 2 | **P1** | **Principal-population accounting in the evidence schema** | Add `principal_count` and `principal_set_id` to per-action evidence records. Instrument the pipeline to enumerate or estimate affected principals per action. Aggregate per session and per PoC deployment. | DOP evidence-contract schema version bump; coordination with SAPP envelope format. | weeks | Closes Gap-3. Gives framework §4.2 R-axis sub-component (population exposure) its numerical dimension. No ordinal class change; materially improves σ_B(t) granularity on R. |
| 3 | **P1** | **First authority-export drill in a PoC deployment** | Exercise the authority-export path from spec/attestation-format.md end-to-end: sample of sealed attestations → export → independent verifier recomputes hashes and verifies anchor → produces an audit report. First drill run during a PoC; result becomes calibration artefact. | A PoC deployment with real sealed attestations. | weeks | Closes B10 `exhibited_with_demotion_path` → `not_exhibited`. No ordinal class change; closes one anti-pattern with demotion path. |
| 4 | **P2** | **First OBO-conformant cross-border composition (standards-track)** | Compose a Lane2 deployment with a willing OBO-conformant counterparty (standards-track partner or pilot). Exercise the DNS-anchored credential + evidence-envelope round-trip. Produce a signed composed attestation per spec. **Note: reframed from a P1 I5-gap-closure item to a P2 standards-track interop item after the v1.1 self-assessment correction.** Lane2's I5 is architectural within its own deployments (aARP + RTGF + Shared Ontology); OBO adoption elsewhere does not close a Lane2 gap — it enables a specific deployer use case (free-roaming agent interop) that some customers will value. | Counterparty willing to pilot OBO; published OBO-conformant evidence on both sides. | quarter | Commercial: proves OBO interop for deployers in the free-roaming-agent class. Does not change Lane2's BR class. Advances OBO as an industry standard. |
| 5 | **P2** | **Trajectory (τ) cadence formalisation** | Define the review cadence for τ per deployment class (pilot / pre-production / production). Record the first three trajectory reviews after a PoC goes into continuous operation. | At least one continuous-operation deployment (months of data). | months | Closes Gap-2. Moves τ attestation from nominal-stable-for-pre-launch to evidence-stable. No ordinal class change; material for the framework's trajectory modifier. |
| 6 | **P2** | **Typed context slots — full structural separation** | Replace the remaining concatenation of tool outputs into LLM context with typed context slots per antipatterns.md A10 demotion. Each slot tagged with trust level; runtime detection of role-escape strings. | Current context-stuffing paths enumerated; migration plan per pipeline stage. | quarter | Closes A10 `exhibited_with_demotion_path` → `not_exhibited`. No ordinal class change; closes one anti-pattern. |
| 7 | **P2** | **Approval-quality metrics and forced re-approval cadence** | Instrument approval gates with median-review-time, diff-of-approved-vs-declined, time-since-last-decline metrics. Implement forced re-approval of standing patterns at a configurable cadence (weekly / monthly / quarterly per action class). | Existing approval gate instrumentation extended. | weeks | Closes A14 `exhibited_with_demotion_path` → `not_exhibited`. No ordinal class change. |
| 8 | **P2** | **Structural prompt-retention enforcement** | Upgrade B3 from `exhibited_with_demotion_path` (template policy shipped) to architectural enforcement: retention classes declared in PACT pack become runtime invariants, with prompt-lifecycle enforcement at the DOP storage layer and architectural support for GDPR Art. 17 erasure. | PACT pack retention-class schema; DOP storage-layer integration. | quarter | Closes B3 `exhibited_with_demotion_path` → `not_exhibited`. No ordinal class change. |
| 9 | **P2** | **Presence-binding enforcement as PACT pack conformance requirement** | Make presence-binding level (fresh_live / recent_live / cached_auth / device_unlock_only / none) a mandatory per-action-class field in PACT pack conformance. Packs declaring an action class above A1 must also declare a presence-binding floor; deployments failing to meet the floor fail closed. | PACT pack conformance spec update; deployer auth-integration documentation. | quarter | Closes B5 `exhibited_with_demotion_path` → `not_exhibited` (or at least structural → architectural on I6 composition). No ordinal class change. |
| 10 | **P2** | **Prompt-injection structural separation on tool outputs** | Full structural separation of tool outputs from LLM reasoning surface per antipatterns.md A15 demotion. Typed output channel; quote + sanitise at protocol boundary; runtime role-escape detection. | Pipeline refactor across tool-call and evidence-contract layers. | quarter | Closes A15 `exhibited_with_demotion_path` → `not_exhibited`. Strengthens I4 and I7 architectural claims. |
| 11 | **P3** | **O4 public-observable claim** | Publish enough of the runtime invariant-checking logic (or its specification) that an external auditor can verify the framework-complete O4 claim at the public-observable level rather than only at internal-instrumented level. This is primarily a documentation and specification effort; the mechanisms exist. | Internal ADRs for each invariant's runtime-check mechanism; public-facing spec document derived from them. | quarter | Upgrades O axis from O3 (public) to O4 (public) in several components, enabling the O4 demotion rule in §5.1 where V≤2 and all invariants hold. Potential residual class impact when combined with V ≤ 2 deployments. |
| 12 | **P3** | **Third-party auditor certification scheme** | Define and publish the third-party audit format for a Lane2 self-assessment being counter-signed by an independent auditor. This is downstream of framework v0.6+ work on the certification scheme. | Framework v0.6+ certification-scheme ADR; candidate auditor partners identified. | year+ | Moves Lane2 self-assessment from self-attested to third-party-attested. Enables stronger regulatory and underwriter posture. |

## Dependency graph (summary)

- ADR candidates **1 and 2** unlock **11** (O4 claim depends partly on Kalman Phase 1 for the v0.5 uncertainty surface)
- ADR candidate **3** unlocks **12** (authority-export drill is precondition for third-party certification scheme)
- ADR candidate **4** is standards-track commercial; independent of other items; not gap-closing for Lane2 (reframed after v1.1 correction)
- ADR candidates **5–10** are largely parallelisable; any of them can proceed once resourced
- ADR candidate **12** is downstream of framework v0.6+ and not actionable at v0.5.1

## Cross-references

- Framework sections motivating these items: §4.2 R-axis (items 2), §5.4 Kalman extension (items 1, 11), §7.1 composition rule (item 4), §9 Invariants 1–7 (items throughout), §14 insurability (items 1, 3, 12)
- Anti-patterns closed or advanced: A10 (item 6), A14 (item 7), A15 (item 10), B3 (item 8), B5 (item 9), B10 (item 3)
- Gaps in self-assessment.md §9 (post-v1.1 renumbering): Gap-1 Kalman (item 1), Gap-2 τ cadence (item 5), Gap-3 principal-population (item 2). (Item 4 OBO-composition was previously tied to a now-retracted "Gap-1 cross-border I5 structural" claim; see self-assessment.md §9 correction note.)
- Profile fields affected: `aggregation.cardinal_score` (items 1), `system.principal_population` and per-action population (item 2), `anti_patterns` many items, `signature` + `anchor` (item 3), `invariants.I5.enforcement_mode` (item 4)

## Out of scope for this backlog

- **Framework evolution.** Changes to axis definitions, invariant list, composition topologies, or interaction overrides are framework-version work (v0.6+), not ADR candidates for Lane2's reference stack.
- **New product development.** Adding a new Lane2 component (e.g. a monitoring dashboard, a compliance report generator) is product roadmap work, not remediation.
- **Customer-specific customisation.** Per-customer pack authoring, per-customer weight calibration, and per-customer retention configuration are deployer engineering work, not Lane2 ADRs.
- **Non-framework regulatory programme work.** Pursuit of specific certifications (ISO 42001, SOC 2 for AI, future EU AI Act conformity assessment) is business-operations work that consumes this backlog's outputs but is not itself ADR-shaped here.

## Review and ownership

**Backlog owner:** Kevin Brown / Lane2 engineering (pre-launch scale)
**Review cadence:** monthly while pre-launch; per-PoC-engagement once PoC cadence begins
**Re-assessment trigger:** when this backlog is consumed to the P1 level in full (items 1–4 closed), re-run the full framework self-assessment and produce a new `self-assessment-v0.X.md` with updated attestations.

**First re-assessment trigger date (estimate):** within six months of first PoC engagement beginning, subject to the commercial pipeline.

---

*End of Tier 3 remediation backlog. Start of self-assessment at [`self-assessment.md`](./self-assessment.md); summary at [`self-assessment-exec-summary.md`](./self-assessment-exec-summary.md); profile at [`self-assessment.json`](./self-assessment.json).*
