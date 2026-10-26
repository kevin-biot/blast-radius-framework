# Chatty-Card A2A — Executive Summary


**Review correction, 2026-10-26:** This is an April assessment, not a current re-attestation. Its numeric profile and measured observations are retained. Statements that the architecture guarantees coverage, avoids exclusions, cannot obtain insurance, or necessarily forecloses lawful deployment are withdrawn. **Coverage not established.** See [current claims policy](../../adoption/claims-and-evidence.md) and [current EU crosswalk](../../adoption/crosswalk-eu-ai-act.md). The historical JSON profile is not re-signed or re-rated by this correction.

**Pattern under assessment:** chatty-card A2A — agent cards consulted by an LLM-prose broker, free-text inter-agent briefings, no typed handoff, no state-machine routing, no domain-gate refusals at tool boundaries
**Date of assessment:** 2026-04-29
**Framework version:** v0.5.1
**Assessor:** Blast Radius Framework authors, applying the framework to an external pattern (not a self-attestation)

**Companion documents:** [`chatty-card-a2a-technical-findings.md`](./chatty-card-a2a-technical-findings.md) (Tier 2 detailed), [`chatty-card-a2a-profile.json`](./chatty-card-a2a-profile.json) (machine-readable profile), [`chatty-card-a2a-adr-backlog.md`](./chatty-card-a2a-adr-backlog.md) (Tier 3 remediation backlog for deployers).

---

## 1. Headline

The chatty-card A2A pattern, as deployed today for transactional workflows, is rated **BR-5 (Catastrophic under the April BRF classification)**.

**In plain English:** the April apparatus exposed serious workflow and containment failures. The retained BR-5 profile records that assessment, not a universal statement about A2A or insurance. No calibrated cardinal estimate, insurer decision or current re-test is supplied.

This rating is **not** an indictment of A2A-the-specification or MCP-the-specification. Both specifications support typed primitives — A2A's `Task` / `TaskStatus` / `Artifact` / `Part.data` payloads, MCP's `inputSchema` / `outputSchema` / structured tool results — that would catch most of the failure modes measured here. The chatty-card variant does not use them canonically. The pattern under assessment is the **specific prose-broker apparatus**, not the specifications themselves.

The empirical anchor is a 1275-conversation controlled experiment (5 random seeds × 255 customers) on a four-agent transactional booking workflow, with cross-family replication on a different model. The full case study is at [`governance-failure-patterns/case-studies/chatty-card-a2a-substrate-harm/`](https://github.com/kevin-biot/governance-failure-patterns/tree/main/case-studies/chatty-card-a2a-substrate-harm).

A v2 canonical-A2A+MCP-per-spec rig has been forked from the same apparatus to measure how much of the fault profile survives strict spec discipline. That measurement is pending and will refine this rating.

## 2. What this means for a buyer or deployer

Three concrete impacts, decreasing order of material consequence:

### 2.1 Insurability posture is *not defensible* as currently deployed

The April apparatus showed variable routing, briefings and tool arguments. That does not prove that all stochastic systems are statistically unmodellable or uninsurable. Boundary replay, calibration and the comparison with canonical protocol use remain open.

No applicable insurance policy wording or endorsement analysis is supplied. Previous categorical exclusion and specialist-market statements are withdrawn.

**Business consequence:** include the observed failures and scope in underwriting due diligence. Do not claim that this assessment establishes either eligibility for or exclusion from coverage.

### 2.2 Regulatory posture is materially weak

The measured failures are relevant to risk-management and robustness work. They are not a legal finding that every deployment of this pattern is prohibited. The apparatus does not prove that every feasible monitor is too late. Use the [reviewed EU crosswalk](../../adoption/crosswalk-eu-ai-act.md) for legal-role, article and timing checks.

The ISO/IEC 42001 and NIST AI RMF crosswalks are translation aids, not certification or conformity assessments.

**Business consequence:** determine legal applicability and test mitigations on the actual deployment before claiming compliance. Architecture changes are candidates for measurement, not a legal conclusion.

### 2.3 Per-event harm rates are high enough to drive customer-relations and reputational risk independent of insurance and regulation

On the measured workflow:
- 96% per-customer fault rate (specialist returns without committing the requested action)
- 35% cross-customer contamination (other-customer preferences leak into the active customer's briefing)
- 50% ground-truth violation rate where measurable (the wrong outcome is committed)
- 60% premature-action rate (downstream action attempted on a phantom upstream state)

The April report describes cross-seed and cross-family replication in its apparatus. Those observations do not establish architecture-only causation, general market prevalence or failure rates in other deployments.

**Business consequence:** reproduce the relevant failure cases and compare canonical protocol use, enforced boundaries, models and workflow changes before selecting remediation. Only the reported apparatus was measured.

## 3. Demotion path

Three live options for a deployer carrying this rating:

1. **Move to canonical A2A+MCP per spec.** Use `Task` / `TaskStatus` / `Artifact` / `Part.data` for the operational channel. Move RAG / preference-store retrieval into typed `DataPart` payloads. Add MCP `outputSchema` validators that refuse downstream calls when upstream artifacts are absent. Make broker routing a state machine over the ledger, not an LLM prose decision. **This may be sufficient** — pending the v2 canonical-rig measurement.
2. **Move to typed-intent substrate replacement** (DOP / AARP-style). Replace inter-agent NL with capability requests carrying typed payloads. Specialists respond with typed assertions. Whether this adds anything over option 1 is the open question v2/v3 is designed to answer empirically.
3. **Restrict the workflow to advisory action class only.** Where the consequential action surface can be removed (the LLM advises a human approver, no automated `assign_meal` equivalent), the BR rating drops because Authority A and Reversibility V change. Honest demotion path for use cases that don't need execution authority but adopted A2A for the orchestration aesthetic.

Without remediation and re-testing, the April BR-5 finding remains unresolved for that assessed configuration. Legal and insurance decisions require separate evidence.

## 4. What this rating is not

It is not:
- An attack on A2A as a protocol specification. The specification supports the canonical variant.
- An attack on MCP as a protocol specification. The specification supports domain gates and structured outputs.
- A claim that any specific vendor's product carries this rating. Vendors implementing canonical A2A+MCP per spec are explicitly out of scope.
- A claim that the failure profile generalises to non-transactional domains. Only transactional workflows with consequential action are measured.

It is:
- A reported measurement of a particular apparatus across two model families, not evidence of market prevalence.
- A starting hypothesis for containment and workflow remediation that requires comparative testing.
- A starting point a deployer can use to self-assess. If the deployer's architecture matches the pattern described, the rating inherits. If not, the deployer should produce their own profile against `spec/br-profile.schema.json`.

## 5. Re-attestation

This rating expires on any of: v2 canonical-A2A+MCP measurement landing, vendor self-attestations diverging from the pattern, or AIID / OECD / specialist-underwriter incident records diverging from the measured profile. See [`chatty-card-a2a-technical-findings.md`](./chatty-card-a2a-technical-findings.md) §10 for full re-attestation conditions.

---

*This rating is offered as a public service. The framework rates the pattern, not any specific vendor or product. The supporting case study and per-event evidence are public on the companion repository [`governance-failure-patterns`](https://github.com/kevin-biot/governance-failure-patterns).*
