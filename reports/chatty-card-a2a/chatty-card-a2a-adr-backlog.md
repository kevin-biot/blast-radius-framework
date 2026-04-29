# Chatty-Card A2A — ADR Remediation Backlog

**Date:** 2026-04-29
**Derived from:** [`chatty-card-a2a-technical-findings.md`](./chatty-card-a2a-technical-findings.md) §9 (gaps) + §6 (anti-pattern attestations)
**Framework version:** v0.5.1

---

## Scope note

Items below are **ADR candidates for any deployer of the chatty-card A2A pattern**, not for a single owning organisation. The Lane2 self-assessment ADR backlog ([`../lane2/self-assessment-adr-backlog.md`](../lane2/self-assessment-adr-backlog.md)) targets a single-owner architecture; this backlog targets *the pattern itself* and is intended as a starting point for any deployer carrying the BR-5 rating.

A deployer adopting any of these ADR candidates should produce their own profile against `spec/br-profile.schema.json` after the change lands; the rating is portable and re-attestation is required on material architecture change.

**Priority legend:**

- **P0** — required to exit BR-5 / uninsurable / unpriceable status
- **P1** — required to bring per-event harm rates below current measurements
- **P2** — required to demote named anti-patterns
- **P3** — hygiene; reduces δ_adv or sharpens observability without changing class

## Backlog

| # | Priority | Proposed ADR title | Scope summary | Dependencies | Effort band | Class / invariant impact |
|---|---|---|---|---|---|---|
| 1 | **P0** | **Replace LLM-prose broker routing with state-machine routing over the operational ledger** | The broker's routing decision (which specialist next, which Task to dispatch) becomes deterministic over the booking ledger / shared state. The LLM is invoked only to compose briefing prose for specialists, never to decide whether or in what order to call them. SeatAgent runs only while `assignment_for(customer_id).seat_id is None`; MealAgent runs only after `seat_reserved=true` is asserted. | A2A spec compliance: `Task`, `TaskStatus`, `Artifact` primitives. The deployer's existing operational ledger as routing-authority surface. | quarter | Closes Invariant 1 failure (deterministic execution). Without this, σ_B(t) is unproducible and the deployment cannot exit unpriceable status. Without this, no other backlog item can demote BR-5. |
| 2 | **P0** | **Add MCP-side domain-gate refusals on consequential tools** | Every consequential MCP tool (`reserve`, `assign_meal`, equivalents in the deployer's domain) gets an `outputSchema` failure mode that refuses the call when the precondition is not met (no upstream Artifact, no required ledger state). The refusal is **structural** — the tool implementation itself returns a typed failure, not a narrative apology. Defense in depth: the broker also state-machine-checks before dispatching, but the tool boundary is the load-bearing refusal point. | MCP spec compliance: `outputSchema`, structured tool results. Domain-gate logic per tool. | quarter | Closes Invariant 6 failure (fail-closed execution control). Eliminates the 60% premature-action rate measured on the chatty-card baseline. AP012 demoted from `exhibited_no_demotion_path` toward `exhibited_with_demotion_path → not_exhibited`. |
| 3 | **P0** | **Replace inter-agent NL briefings with typed `Task` / `Artifact` / `Part.data` payloads** | Operational state between agents lives in typed JSON `Part.data` payloads attached to A2A `Task` instances. NL `Message` parts may be present for human-readable context but **are not consulted by downstream agents as authoritative state**. SeatAgent returns a typed `SeatReservation` Artifact; MealAgent reads it from the Task, not from the broker's narrative. | A2A spec compliance: `Task`, `Artifact`, `Part.data`. Typed Artifact JSON schemas for the deployer's domain (`SeatReservation`, `MealAssignment`, equivalents). | quarter | Closes Invariant 7 failure (bounded coupling). Moves composition class from T2 super-additive to T1 sub-additive. AP006 *partially* demoted — NL still present in briefings, but operational gates are typed. **This is the load-bearing change for exiting BR-5**; without it the pattern remains in the uninsurable region regardless of items 1 and 2. |
| 4 | **P1** | **Per-customer scoping on RAG retrieval** | Retrieval-augmented generation queries against the preference store / context store filter results to `metadata.customer_id == active_customer_id` and **fail closed** when scoping leaves fewer than the threshold for useful retrieval (deployer-set; suggested ≥ 2 chunks). No silent fallback to unfiltered retrieval. | The RAG layer's metadata schema. Filter logic at retrieve-time. | weeks | Eliminates the 35% cross-customer contamination rate at the RAG-layer source. Strengthens Invariant 4 (bounded blast radius). Does not on its own demote BR-5 if items 1–3 are not in place; with them, it is the closing item that brings cross-customer contamination toward 0%. |
| 5 | **P1** | **Tool-schema example anchoring audit (AP018 closure)** | Audit every tool / MCP function `description` field for concrete example values inside NL prose (`"e.g. '14A' or '32H'"`). Replace with abstract format guidance (`"row+letter format per spec"`). Where examples must appear, generate them dynamically per call from runtime state, or rotate across an enumerated set. Add a tool-boundary monitor: if argument distribution concentrates on the schema-example value disproportionately, log + flag. | Inventory of all tool / MCP descriptions. Build / review pipeline check on schema text changes. | weeks | Demotes AP018 from `exhibited_with_demotion_path` toward `not_exhibited`. Does not on its own demote BR class. **Material for δ_adv**: removes a supply-chain attack surface where schema-text edits propagate as default-argument poisoning. |
| 6 | **P1** | **Conversational-substrate audit logging extended to inter-agent NL** | NL briefings between agents are logged with the same discipline as tool calls: timestamped, hashed, bound to `Task.task_id`, retrievable for forensic replay. **Even after the pattern moves to typed Artifacts**, any residual NL prose (briefings, summaries) needs forensic-tier evidence retention to satisfy Invariant 2 partial → full. | Audit substrate extension. Storage cost depends on NL-channel volume. | weeks | Strengthens Invariant 2 (evidence binding) from partial to full. Material for ISO 42001 / EU AI Act traceability claims. |
| 7 | **P2** | **Capability-discovery enumeration mitigation (AP010 closure)** | If agent cards are world-readable in the deployment, restrict discovery to authenticated principals with declared scope. Static state-machine routing (item 1) eliminates the *runtime* dependency on agent-card prose, but cards may still be enumerated for reconnaissance. Bind agent-card visibility to delegation scope. | Authentication layer for agent-card endpoints. Delegation scope per principal. | weeks | Demotes AP010 from `exhibited_with_demotion_path` toward `not_exhibited`. Reduces δ_adv. |
| 8 | **P2** | **Typed intent vs action-command semantics review** | Even with canonical A2A+MCP per spec (items 1–3), the broker still issues `Task`s as commands ("MealAgent: assign meal type X to seat Y"). A semantic alternative is capability-request / capability-response: broker asks "MealAgent: do you have capacity for meal type X for customer C with seat Y?"; MealAgent returns `available=true/false` + reservation token; broker commits the action separately. This is the AARP semantic shape. **Whether it adds material safety over canonical A2A+MCP is the v2 → v3 falsification question.** Land this ADR conditional on v2 leaving residuals. | v2 D.5 measurement (forthcoming). | quarter (post v2) | Conditional on v2 leaving residuals, this item closes the substrate-replacement gap. If v2 closes residuals to ~zero, this item is unnecessary. |
| 9 | **P3** | **Trajectory cadence formalisation for the deployment** | The pattern's τ modifier is rated `deteriorating` at the pattern level. A specific deployment can rate τ better with evidence: documented review cadence, drift measurement on the deployed substrate, response to incidents. | Continuous-operation deployment + months of operational evidence. | months | Material for σ_B(t) once items 1–3 are in place. |
| 10 | **P3** | **Third-party auditor counter-signature on the deployment's BR profile** | Once the deployment has executed items 1–3 and produced its own BR profile, seek third-party audit counter-signature. This is downstream of framework v0.6+ certification scheme work (lane2 backlog item 12). | Framework v0.6 certification scheme; auditor partner identification. | year+ | Moves the deployment from self-attested to third-party-attested. |

## Dependency graph (summary)

- ADR candidates **1, 2, 3 are P0 and mutually reinforcing**. The deployment cannot exit BR-5 without all three. Item 1 alone closes Invariant 1; item 3 alone closes Invariant 7; item 2 alone closes Invariant 6. The combined change is what produces the canonical-A2A+MCP-per-spec variant.
- ADR candidate **4 closes residual cross-customer contamination** once 1–3 are in place. On its own, against the chatty-card baseline, item 4 was previously planned as the v1 "Arm B" experiment; the schema-fix verdict reframed Arm B as one column of a four-arm decomposition rather than a standalone fix.
- ADR candidate **5 (AP018 closure) is independent** and reduces apparatus-confound risk on any future rating exercise. Land it alongside 1–3 to keep the rating's empirical claims clean.
- ADR candidates **6, 7, 9, 10** are post-1–3 hygiene that strengthen the deployment's evidence posture without changing class.
- ADR candidate **8 is gated on v2 D.5 measurement.** Do not land speculatively; the experimental result is what determines whether substrate replacement is required beyond canonical-spec discipline.

## What this backlog is *not*

It is not a complete remediation programme. A real deployer's backlog will have additional items specific to their domain: regulatory mappings (item 5 / 6 expand into ISO 42001 control IDs and EU AI Act Art. 15 / 17 / 19 evidence schedules), principal-population accounting (analogous to lane2 backlog item 2), and authority-export drills for any consequential-action class.

The eight items above are the **architectural** remediation surface. Procedural and regulatory items layer on top. The ordering reflects what the framework requires to demote class — not what a deployer's compliance team requires to satisfy any one regulatory regime.

## Why item 3 is the load-bearing P0

Two of the three P0 items can be implemented within the chatty-card pattern *as quality improvements* without changing the architecture:

- Item 1 (state-machine routing) replaces the LLM prose with deterministic logic — but the LLM still composes briefings, the broker still has narrative state, and downstream agents still consume NL.
- Item 2 (MCP domain gates) hardens the tool boundary — but the upstream NL substrate is unchanged.

Item 3 is the substrate change. It moves operational state out of the NL channel entirely and into typed `Part.data` payloads. Without item 3, items 1 and 2 are bandages on an open wound: the broker's narrative may converge on the wrong state through any of the AP006 / AP012 / AP018 mechanisms, and items 1 and 2 only catch *tool-call-time* incoherence, not *briefing-time* incoherence that propagates downstream.

This is why the rating is BR-5 and not BR-4: closure requires **all three** P0 items, not any subset.
