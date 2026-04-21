# Notation and Quick Reference

*Standalone lookup document. Every symbol, every tier, every class definition, in one place.*

**For framework version:** v0.5.1
**Last updated:** 2026-04-21

---

This document is a reference sheet. If you're looking up *"what's BR-3 again?"* or *"what's the difference between C4a and C4b?"*, start here. For the argument and prose, see [framework.md](./framework.md). For the machine-readable form, see [spec/br-profile.schema.json](./spec/br-profile.schema.json).

---

## 1. Pre-rating classifier

Each component of a system is classified once, before the tuple is assigned.

| Class | Definition | Consequence |
|---|---|---|
| **Closed-world** | Inputs normalised to controlled vocabulary before reaching agent context; ontology defines what can exist; inter-component interfaces typed (structured capability requests, not NL); scope declared and structurally enforced | Can claim Invariants 1–7 and reach BR-2 or BR-3 with full evidence |
| **Open-world** | Any NL can reach agent context; NL or free-form prompt between components; scope is persona prompt not structural bound; context window is the trust boundary | Cannot claim Invariant 7 (bounded coupling); forces BR-4 minimum regardless of per-axis scores |

**Rule:** any open-world component promotes system effective BR to BR-4 minimum.

---

## 2. Rating axes and tiers

System profile: **A–R–C–V–K–O**.

### A — Authority

| Tier | Meaning |
|---|---|
| **A0** | Observe only |
| **A1** | Recommend only |
| **A2** | Draft actions (human approval required before execution) |
| **A3** | Execute bounded actions (pre-approved classes, parameter limits) |
| **A4** | Execute open-ended actions (tool access without structural bounds) |

### R — Reach

| Tier | Meaning |
|---|---|
| **R1** | Single system, single tenant |
| **R2** | Multiple internal systems, single organisation |
| **R3** | Cross-functional enterprise systems, multi-tenant |
| **R4** | External or regulated domains, public-facing, or affecting third parties |

### C — Coupling

| Tier | Meaning |
|---|---|
| **C1** | Isolated agent, no tools |
| **C2** | Agent plus tools, no peer agents |
| **C3** | Workflow or chain, typed interfaces, bounded state |
| **C4a** | Multi-agent with NL-coupled peers, no shared state |
| **C4b** | Multi-agent with shared state or recursive composition |

The C4a / C4b split is material. Stateless NL-coupling (C4a) is still dangerous because failures correlate through the shared LLM substrate even without shared application state.

### V — Reversibility

Each tier carries an explicit recovery horizon.

| Tier | Meaning |
|---|---|
| **V1** | Fully reversible, horizon ≤ minutes (idempotent, local state) |
| **V2** | Reversible with effort, horizon ≤ hours (compensating transactions, manual rollback) |
| **V3** | Partially reversible, horizon ≤ days (data restoration, customer communication) |
| **V4** | Practically irreversible, horizon > days or requires external cooperation |

### K — Consequence

K decomposes into sub-tags matching regulatory regimes.

| Tier | Meaning |
|---|---|
| **K1** | Minor inconvenience |
| **K2** | Operational disruption |
| **K3-F** | Material financial impact |
| **K3-L** | Material legal / contractual impact |
| **K3-P** | Material privacy impact (GDPR, CCPA, data-subject rights) |
| **K4-S** | High-consequence safety (physical, clinical, psychological) |
| **K4-R** | High-consequence regulated / systemic (financial stability, public infrastructure, sanctions) |
| **K4-F** | High-consequence fundamental rights (EU AI Act Annex III, equality, due process) |

### O — Observability

| Tier | Meaning |
|---|---|
| **O0** | No runtime observability |
| **O1** | Coarse telemetry (success/failure, latency) |
| **O2** | Action-level logs, replayable traces, manual review |
| **O3** | Real-time anomaly and drift detection, auditable decisions, evidence preserved |
| **O4** | Real-time detection plus architectural invariants checkable at runtime |

**Observability is a first-class axis AND the cross-cutting verifiability surface for Invariants 1–5.** O ≥ 2 is the minimum for any invariant claim to be auditable; O = 4 is what separates architectural enforcement from architectural assertion.

---

## 3. Modifiers

### δ_adv — Attack-accessibility

| Value | Meaning |
|---|---|
| **0** | Adversarial escalation path analysed and closed (threat model documented) |
| **+1** | Known escalation paths with mitigations but residual risk |
| **+2** | Unanalysed or open adversarial surface |

Effective class = base class + δ_adv.

### τ — Trajectory

| Value | Meaning |
|---|---|
| **stable** | No class change in review period; controls track configuration |
| **expanding** | Tool or reach additions accepted; class recomputed and uprated |
| **drifting** | Observed behaviour suggests movement not reflected in configuration |

BR-3+ systems require a documented trajectory review cadence.

### Residual vs inherent

Report both. Inherent BR = class in the absence of mitigating controls. Residual BR = class with controls operating as designed. Audit narrows the gap.

---

## 4. Blast-radius classes

| Class | Name | Typical profile |
|---|---|---|
| **BR-1** | Contained | Low authority, limited reach, fully reversible, observable. Summarisation, analytics, read-only assistants. |
| **BR-2** | Managed | Limited execution, controlled scope, human oversight, action-level logs. Drafting systems, decision support. |
| **BR-3** | Expansive | Write capability, multi-system reach, partial autonomy, real-time observability required. Operational automation agents. |
| **BR-4** | Systemic | High coupling, high reach, limited reversibility, high consequence. Requires architectural guarantees in addition to runtime controls. Multi-agent decision systems, compliance pipelines, enterprise operational agents. |
| **BR-5** | Intolerable without formal governance | High consequence combined with high coupling or low reversibility. Requires pre-deployment architectural proof, formal assurance, regulatory alignment, insurability evidence. Safety-critical, clinical, or regulated autonomous systems. |

---

## 5. Composition topologies

Before applying the §7.1 pairwise composition rule, identify the topology. Each has distinct compound-risk mathematics.

| Topology | Regime | Compound failure math | Compound BR |
|---|---|---|---|
| **T1 sub-additive** | Closed-world narrow fail-closed chain | P(fail) ≈ 1 − ∏(1 − Rᵢ) — union bound, ≈ Σ Rᵢ for small Rᵢ | BR ≤ max(BRᵢ) — bounded by typed boundary |
| **T2 super-additive** | Open-world NL-coupled chain | P(fail) > additive — failures correlate via shared substrate (ρ > 0) | BR > max(BRᵢ); diverges with chain length n |
| **T3 multiplicative** | Defence-in-depth (attack resistance, not failure propagation) | P(bypass compound) = ∏ P_bypass,ᵢ | Small when each P_bypass,ᵢ small |
| **T4 exponential-reducing** | Parallel redundancy with genuine independence (voting with quorum k) | P(joint failure) = P(≥ k fail) — binomial tail, exponentially small in n | Small when components genuinely independent |

**T2-in-disguise test:** most claimed T4 voting ensembles are actually T2 because same-model-family evaluators share substrate and correlate on failure. Require evidence of independence (different families, different providers, different prompt derivations, uncorrelated failure history) before granting T4 treatment.

---

## 6. Interaction overrides (non-linearity)

Applied on top of the base ordinal aggregation (max over axes).

| Rule | Trigger | Effect |
|---|---|---|
| 1 | C4a or C4b + V ≥ 3 | Promote one class |
| 2 | A ≥ 3 + K4 | Minimum BR-4 (floor, not promotion) |
| 3 | R4 + O ≤ 1 | Promote one class |
| 4 | Invariant 7 absent (partial) | Promote one class — applies only to closed-world systems; pure open-world hits BR-4 floor via §4.0 |
| Pre-rating | Open-world component present | BR-4 minimum regardless of other axes |

### Observability modifier

- O0 or O1 on any BR-3+ system → promote one class
- O4 with architectural invariants at runtime → may demote one class *only if* V ≤ 2 *and* §9 invariants all hold

---

## 7. Cardinal score (v0.3 + v0.5 Kalman extension)

### v0.3 point estimate

**B(t) = w_a·A + w_r·R + w_c·C + w_v·(1−V) + w_k·K + w_o·(1−O)**

where each axis tier is normalised to [0, 1] and **w = [w_a, w_r, w_c, w_v, w_k, w_o]** is the per-domain weight vector.

### v0.5 Kalman-filtered

**B̂(t|t) = wᵀ · x̂(t|t)** with uncertainty **σ_B(t) = √(wᵀ · P(t|t) · w)**

Rated output: **B̂(t|t) ± σ_B(t)**, where x̂(t|t) is the Kalman-filtered state estimate and P(t|t) is the filter covariance.

### Actuarial identification

- **Frequency (λ)** — C-axis and O-axis dominate (fast-onset drift in C4a + O≤2)
- **Severity (σ)** — K-axis and R-axis dominate (K4 with R≥3 produces correlated loss)
- **Uncertainty (υ)** — ≡ σ_B(t) under the v0.5 Kalman extension

---

## 8. Kalman state-space variables (§5.4)

Disambiguated with subscript `_K` to avoid collision with rating axes.

| Symbol | Meaning |
|---|---|
| **x(t)** | Latent compliance state vector |
| **x̂(t\|t−1)** | A priori state estimate |
| **x̂(t\|t)** | A posteriori state estimate |
| **P(t\|t−1)** / **P(t\|t)** | A priori / a posteriori covariance of x̂ |
| **y(t)** | Observation vector (rubric evaluations, tool-call outcomes, evidence submissions) |
| **A_K** | State-transition matrix. *Not* the Authority axis. |
| **H**, **Hᵀ** | Observation matrix and its transpose |
| **Q** | Process-noise covariance — prior on state shift between observations |
| **R_K** | Measurement-noise covariance. *Not* the Reach axis. Calibrated from evidence tiers: forensic → low R_K; minimal → high R_K. |
| **K_K(t)** | Kalman gain. *Not* the Consequence axis. Weight applied to new observations. |
| **I** | Identity matrix |

---

## 9. Composition-math variables (§7.2)

| Symbol | Meaning |
|---|---|
| **Rᵢ** | Per-component failure probability. *Not the Reach axis.* |
| **BRᵢ** | Per-component blast radius class |
| **n** | Chain length |
| **P_bypass,ᵢ** | Per-layer attack bypass probability (T3) |
| **ρ** | Correlation coefficient between component failures (T2) |
| **k** (composition) | Quorum threshold in T4 voting |
| **∏**, **Σ**, **max** | Product, sum, max over components i = 1..n |

---

## 10. Notational collisions (summary)

Three letters are overloaded. Context disambiguates; where ambiguity is catastrophic the subscripted forms are used even inline.

| Letter | As rating axis | As Kalman matrix |
|---|---|---|
| **A** | Authority axis | A_K — state-transition matrix |
| **R** | Reach axis | R_K — measurement-noise covariance |
| **K** | Consequence axis | K_K — Kalman gain |

Outside §5.4 and this document's §8, unqualified `A`, `R`, `K` always mean the rating axes.

---

## 11. Architectural invariants (summary of §9)

| # | Invariant | One-line verifier |
|---|---|---|
| **I1** | Deterministic execution | Re-run produces identical evidence hashes |
| **I2** | Evidence binding | Tamper-evident, externally anchored, independently signed |
| **I3** | Policy snapshot coherence | Every decision carries `policy_snapshot_id` |
| **I4** | Bounded blast radius | Cross-tenant isolation tested; action-class ceiling enforced |
| **I5** | Jurisdictional awareness | Regulatory tier unoverridable; conflicts fail closed + escalate |
| **I6** | Fail-closed execution control | Default DENY; cryptographic token verification blocks execution |
| **I7** | Bounded coupling | No NL peer coupling; typed interfaces across component edges |

---

## 12. Anti-pattern IDs (summary of [antipatterns.md](./antipatterns.md))

**Part A — architectural (15 patterns):** A1 A2A · A2 API-agent-ready · A3 MCP ecosystem · A4 agent marketplaces · A5 auto-tool-gen from OpenAPI · A6 CrewAI/AutoGen persona+NL default · A7 LLM-as-judge · A8 OAuth-as-agent-identity · A9 ungoverned vector memory · A10 context stuffing · A11 computer use · A12 deep research · A13 BYOA/shadow agents · A14 autonomy-slider approval fatigue · A15 prompt-injection-as-feature

**Part B — evidence-chain (11 patterns):** B1 logs-as-evidence · B2 post-hoc logging vs runtime controls · B3 prompt storage without governance · B4 no delegation chain · B5 no authentication freshness · B6 unsigned/self-signed-only · B7 no explainability source mapping · B8 mutable at rest · B9 no replay · B10 no retention/authority-export · B11 critical-action fail-open

---

## Versioning

- This document tracks `framework.md` versions.
- Current: aligned with framework v0.5.1.
- Changes to tier enums, class definitions, or invariant names produce a new framework version and a corresponding update here.
- Symbol collisions, if introduced, are added to §10 with explicit disambiguation rules.

Citation: cite `framework.md` at a specific version (e.g. "framework.md v0.5.1 §5.1") for all references to definitions. This document is a lookup mirror, not an independent source of truth.
