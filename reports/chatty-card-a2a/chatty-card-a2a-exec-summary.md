# Chatty-Card A2A — Executive Summary

**Pattern under assessment:** chatty-card A2A — agent cards consulted by an LLM-prose broker, free-text inter-agent briefings, no typed handoff, no state-machine routing, no domain-gate refusals at tool boundaries
**Date of assessment:** 2026-04-29
**Framework version:** v0.5.1
**Assessor:** Blast Radius Framework authors, applying the framework to an external pattern (not a self-attestation)

**Companion documents:** [`chatty-card-a2a-technical-findings.md`](./chatty-card-a2a-technical-findings.md) (Tier 2 detailed), [`chatty-card-a2a-profile.json`](./chatty-card-a2a-profile.json) (machine-readable profile), [`chatty-card-a2a-adr-backlog.md`](./chatty-card-a2a-adr-backlog.md) (Tier 3 remediation backlog for deployers).

---

## 1. Headline

The chatty-card A2A pattern, as deployed today for transactional workflows, is rated **BR-5 (Catastrophic / Uninsurable as deployed)**.

**In plain English:** the pattern's failure profile sits in the framework's uninsurable region. Five of seven architectural invariants fail or are inapplicable; two fail definitively (deterministic execution, bounded coupling). Because Invariant 1 (deterministic execution) fails, the framework's Kalman uncertainty extension is **structurally inapplicable** — the cardinal score B̂(t|t) ± σ_B(t) cannot be produced. The pattern retains an ordinal BR-5 rating but cannot quantify υ and is structurally unpriceable. This is the architectural boundary between insurable and uninsurable, made precise.

This rating is **not** an indictment of A2A-the-specification or MCP-the-specification. Both specifications support typed primitives — A2A's `Task` / `TaskStatus` / `Artifact` / `Part.data` payloads, MCP's `inputSchema` / `outputSchema` / structured tool results — that would catch most of the failure modes measured here. The chatty-card variant does not use them canonically. The pattern under assessment is the **sloppy market default**, not the specifications themselves.

The empirical anchor is a 1275-conversation controlled experiment (5 random seeds × 255 customers) on a four-agent transactional booking workflow, with cross-family replication on a different model. The full case study is at [`governance-failure-patterns/case-studies/chatty-card-a2a-substrate-harm/`](https://github.com/kevin-biot/governance-failure-patterns/tree/main/case-studies/chatty-card-a2a-substrate-harm).

A v2 canonical-A2A+MCP-per-spec rig has been forked from the same apparatus to measure how much of the fault profile survives strict spec discipline. That measurement is pending and will refine this rating.

## 2. What this means for a buyer or deployer

Three concrete impacts, decreasing order of material consequence:

### 2.1 Insurability posture is *not defensible* as currently deployed

The pattern fails Invariant 1 (deterministic execution) because the broker's routing, briefing content, and tool-argument distribution are LLM-stochastic on identical inputs. Without Invariant 1, measurement noise R_K and process noise Q cannot be separated by the Kalman filter; σ_B(t) cannot be calibrated; the system is structurally unpriceable. Specialist underwriters (Munich Re aiSure, AIUC, Armilla / Lloyd's) have no surface to price against because the architecture cannot produce reproducible decision trails.

Verisk's 2026 commercial general-liability exclusions name AI agent loss as an excluded peril for non-conforming architectures. Chatty-card A2A on a transactional workflow falls inside the excluded category structurally, not because of any specific implementation defect.

**Business consequence:** a chatty-card-A2A deployment cannot obtain priced cover against AI agent loss in the 2026 specialist-underwriter market without first changing architecture. The rating is portable: any deployer using this pattern inherits BR-5 until they re-architect.

### 2.2 Regulatory posture is materially weak

EU AI Act Article 25(4) and the recent academic synthesis on agentic systems under EU law (Nannini et al. 2026) both point at the same architectural property: high-risk systems with untraceable behavioral drift cannot be lawfully placed on the EU market. The chatty-card pattern produces drift inside the baseline-establishment window of any monitor a deployer can install — the failure leads any feasible detector. Logs exist, but they tell you about events after they harmed the ledger, not before they happened.

ISO 42001 and NIST AI RMF crosswalks (in [`adoption/`](../../adoption/)) place chatty-card A2A in the categories that require structural remediation, not procedural mitigation.

**Business consequence:** a deployer claiming AI Act high-risk compliance on this architecture is exposed to enforcement risk that procedural controls cannot close. Architecture change is the only remediation that lands the deployment in a defensible regulatory posture.

### 2.3 Per-event harm rates are high enough to drive customer-relations and reputational risk independent of insurance and regulation

On the measured workflow:
- 96% per-customer fault rate (specialist returns without committing the requested action)
- 35% cross-customer contamination (other-customer preferences leak into the active customer's briefing)
- 50% ground-truth violation rate where measurable (the wrong outcome is committed)
- 60% premature-action rate (downstream action attempted on a phantom upstream state)

These rates were stable across 5 random seeds and across two model families (Mistral 3B Q4 → Granite 4 7B Q8). They are properties of the architecture, not artefacts of any one model.

**Business consequence:** consumer-facing chatty-card A2A deployments produce a customer-experience failure profile that is visible to end users and not solvable by tuning, prompt engineering, or model upgrades. Architecture change is the only intervention that demonstrably moves the numbers.

## 3. Demotion path

Three live options for a deployer carrying this rating:

1. **Move to canonical A2A+MCP per spec.** Use `Task` / `TaskStatus` / `Artifact` / `Part.data` for the operational channel. Move RAG / preference-store retrieval into typed `DataPart` payloads. Add MCP `outputSchema` validators that refuse downstream calls when upstream artifacts are absent. Make broker routing a state machine over the ledger, not an LLM prose decision. **This may be sufficient** — pending the v2 canonical-rig measurement.
2. **Move to typed-intent substrate replacement** (DOP / AARP-style). Replace inter-agent NL with capability requests carrying typed payloads. Specialists respond with typed assertions. Whether this adds anything over option 1 is the open question v2/v3 is designed to answer empirically.
3. **Restrict the workflow to advisory action class only.** Where the consequential action surface can be removed (the LLM advises a human approver, no automated `assign_meal` equivalent), the BR rating drops because Authority A and Reversibility V change. Honest demotion path for use cases that don't need execution authority but adopted A2A for the orchestration aesthetic.

Doing nothing is also an option. The BR-5 rating, the insurability gap, and the regulatory exposure are public-domain consequences regardless.

## 4. What this rating is not

It is not:
- An attack on A2A as a protocol specification. The specification supports the canonical variant.
- An attack on MCP as a protocol specification. The specification supports domain gates and structured outputs.
- A claim that any specific vendor's product carries this rating. Vendors implementing canonical A2A+MCP per spec are explicitly out of scope.
- A claim that the failure profile generalises to non-transactional domains. Only transactional workflows with consequential action are measured.

It is:
- A measured claim about the **default** way A2A is deployed in 2026, with empirical numbers across two model families.
- A claim that procedural controls cannot demote this rating; architecture change is required.
- A starting point a deployer can use to self-assess. If the deployer's architecture matches the pattern described, the rating inherits. If not, the deployer should produce their own profile against `spec/br-profile.schema.json`.

## 5. Re-attestation

This rating expires on any of: v2 canonical-A2A+MCP measurement landing, vendor self-attestations diverging from the pattern, or AIID / OECD / specialist-underwriter incident records diverging from the measured profile. See [`chatty-card-a2a-technical-findings.md`](./chatty-card-a2a-technical-findings.md) §10 for full re-attestation conditions.

---

*This rating is offered as a public service. The framework rates the pattern, not any specific vendor or product. The supporting case study and per-event evidence are public on the companion repository [`governance-failure-patterns`](https://github.com/kevin-biot/governance-failure-patterns).*
