# From Tool Access to Blast Radius

*A classification framework for governing agentic AI systems*

**Version:** 0.5
**Status:** Research note, open for comment
**Date:** 2026-04-21
**Prior versions:** v0.1 (initial draft); v0.2 (aggregation rule, composition rule, §14 security-ops mapping); v0.3 (cardinal-score synthesis, seven architectural invariants, insurability as economic gate, compositional-enforcement pattern); v0.4 (pre-rating closed/open-world classifier, composition classes with sub-additive / super-additive / multiplicative / redundant mathematics, Invariant 7 as composition gate); v0.5 (Kalman extension — cardinal score becomes a filtered estimate B̂(t|t) ± σ_B(t); tiered evidence confidence maps to measurement noise R; σ_B(t) is the direct actuarial uncertainty υ output).

---

## 0. Reading guide

This framework is one of a set of documents in this repository:

1. **This document** (`framework.md`) — the rating framework. Six axes, three modifiers, seven invariants, composition rule, ordinal + cardinal aggregation.
2. **[manifesto.md](./manifesto.md)** — the argument for why the framework must exist: insurer silence, regulator prose, pattern precedents.
3. **[antipatterns.md](./antipatterns.md)** — negative reference: 26 named anti-patterns that inflate blast radius and commonly ship as "progress".
4. **[insurability.md](./insurability.md)** — economic/actuarial companion: why insurability cuts faster than regulation, λ/σ/υ mapping.
5. **[ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)** — credits to Gagne's multi-agent drift corpus (the empirical catalyst), prior published work, and intellectual background.

Read (1) for rating, (2) for the argument, (3) for diligence, (4) for market access, (5) for attribution.

---

## Abstract

Tool-enabled large language models have shifted AI systems from bounded reasoning to real-world action. Evaluation practice has not kept pace: accuracy benchmarks and model-level guardrails do not capture system-level impact. This note proposes a six-axis framework — authority, reach, coupling, reversibility, consequence, observability — with three modifiers, an ordinal aggregation rule, a cardinal *Expected Compliance Risk* score extended to all six axes, an explicit composition rule for multi-vendor stacks, and seven architectural invariants that must hold for any BR class claim to be genuine.

The central claim, from architecture, regulation, and actuarial science converging: **system architecture, not model capability, determines operational risk**. Blast radius must be designed, not discovered. Systems that cannot populate the framework's tuple cannot be priced by specialist underwriters (Munich Re aiSure, AIUC, Armilla via Lloyd's), cannot meet EU AI Act Article 12 / 15 obligations, and should not be deployed in regulated sectors regardless of their model-layer evaluation scores.

v0.3 integrated three advances: the seven-invariant synthesis (six from prior published insurability work; seventh — *bounded coupling* — from Gagne's multi-agent drift corpus on fast-onset drift, see [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)); the cardinal score (Expected Compliance Risk extended over all six axes); and the compositional-enforcement pattern, exemplified by ontology-as-firewall with Bayesian validation.

v0.4 added composition discipline: a pre-rating classifier separating **closed-world** (ontology-bounded) systems from **open-world** (NL-unbounded) systems, and four composition classes with explicit mathematics — sub-additive for bounded chains, super-additive for NL-coupled chains, multiplicative for defence-in-depth, exponential-reducing for voting redundancy. The framework now refuses to rate an open-world system below BR-4 regardless of per-axis scores, because Invariant 7 (bounded coupling) is structurally impossible in that substrate.

v0.5 adds the Kalman extension. The cardinal score B(t) is no longer a point estimate — it becomes a filtered estimate B̂(t|t) with uncertainty σ_B(t) that is directly usable by specialist underwriters as the actuarial υ variable. Tiered evidence-confidence ratings map formally to Kalman measurement noise R, turning evidence quality into a quantitative input to uncertainty rather than a qualitative label. Systems failing Invariants 1–2 cannot produce σ_B(t) and fall back to ordinal rating with no uncertainty quantification — a structural boundary between insurable and uninsurable that the framework now makes explicit.

---

## 1. The shift: from output to action

Function calling, tool APIs, and orchestration frameworks have changed what LLM-based systems do. They no longer just generate outputs; they act on external systems and modify state beyond their own boundary. Errors are no longer incorrect answers — they are incorrect actions with consequences.

Evaluation and governance practice has not kept pace. Accuracy benchmarks, prompt design, and model-level guardrails remain useful but do not capture system-level impact.

## 2. The missing concept

Three communities need a classification of operational agentic AI impact, and none currently has one:

- **Engineering.** Cloud systems have failure domains; finance has VaR and counterparty exposure; safety engineering has blast radius. Agentic AI has no equivalent tuple notation.
- **Regulation.** ISO/IEC 42001 is process-shaped; NIST AI RMF is prose; the EU AI Act classifies systems by risk *category* (unacceptable / high / limited / minimal) rather than operational blast radius; MITRE ATLAS and OWASP LLM Top 10 are attack-shaped; Anthropic RSP and OpenAI Preparedness are frontier-capability-shaped.
- **Actuarial.** Specialist insurers (Munich Re aiSure, AIUC, Armilla/Lloyd's) require data for pricing that nondeterministic systems cannot supply (stable frequency λ, bounded severity σ, quantifiable uncertainty υ). The 2025 insurability piece named the gap formally; the implication is that uninsurable systems are commercially foreclosed in regulated sectors regardless of regulatory compliance.

The three communities converge on the same requirement: a way to classify *how far unintended impact can propagate* from an autonomous or semi-autonomous action. This note names that classification.

## 3. Definition

**Blast radius (agentic systems):** the maximum scope of unintended impact a system can produce through autonomous or semi-autonomous action across connected systems, under a defined threat model, within a defined recovery horizon, with evidence sufficient to populate an actuarial model.

Four explicit parameters — scope, threat model, recovery horizon, evidence sufficiency — turn the concept from a rhetorical phrase into something that can be attested, audited, priced, and underwritten.

## 4. Classification: pre-rating classifier and six axes

### 4.0 Pre-rating: the worldview classifier

Before the six-axis tuple is assigned, each component of the system must be classified as either **closed-world** or **open-world**. This is not a rating adjustment; it is a *pre-rating gate* that determines which axes and which composition mathematics (§7.2) apply.

**Closed-world (ontology-bounded).** Inputs are normalised to a controlled vocabulary before entering agent context; an ontology defines which concepts can exist; inter-component interfaces are typed (structured capability requests, not NL); scope is declared per component and structurally enforced. Reference: DOP narrow closed-world agents with AARP routing, phrase normalisation, and the 8-layer ontology-as-firewall composition (§15). Closed-world systems can claim Invariants 1–7 and can reach BR-2/BR-3 with full evidence.

**Open-world (NL-unbounded).** Any natural-language content can reach agent context; inter-component interfaces are NL or free-form prompt; scope is declared as a persona prompt but not structurally enforced; context window is the trust boundary or absent entirely. Reference: A2A (AgentCards + NL peer calls), CrewAI / AutoGen / LangGraph default patterns, MCP server ecosystems without composition rule, LLM-as-judge recursion, any agent that consumes untrusted NL as context.

**Open-world systems cannot claim Invariant 7 (bounded coupling).** NL is by definition unbounded; bounded coupling is not a property that can be layered on after the fact. Therefore:

- Any component that is open-world promotes the system's effective BR to **BR-4 minimum regardless of per-axis scores**
- BR-2 and BR-3 claims require every component to be closed-world
- An open-world-to-closed-world interface counts as open-world for composition (§7.2)

**Why a pre-rating gate, not a modifier.** The empirical evidence from Gagne's multi-agent drift corpus[^1] is clear: collapse in open-world NL-coupled substrates happens inside the baseline-establishment window of any runtime monitor. BR-2/BR-3 would imply monitoring-based governance can contain the risk; the evidence says it cannot. Classifying worldview first prevents the common failure mode where a system is rated BR-3 on per-axis scoring while sitting architecturally in the regime where the ratings are meaningless.

With worldview set, a system is expressed as the tuple **A–R–C–V–K–O**.

### 4.1 Authority (A)

- **A0** Observe only
- **A1** Recommend only
- **A2** Draft actions (human approval required)
- **A3** Execute bounded actions (pre-approved classes, parameter limits)
- **A4** Execute open-ended actions (tool access without structural bounds)

Tool access is a grant of authority, not merely capability.

### 4.2 Reach (R)

- **R1** Single system, single tenant
- **R2** Multiple internal systems, single organisation
- **R3** Cross-functional enterprise systems, multi-tenant
- **R4** External or regulated domains, public-facing, or affecting third parties

Reach has two sub-components: *systems touched* (lateral propagation) and *principals affected* (population exposure). Both must be recorded.

### 4.3 Coupling (C)

- **C1** Isolated agent, no tools
- **C2** Agent plus tools, no peer agents
- **C3** Workflow or chain, typed interfaces, bounded state
- **C4a** Multi-agent with NL-coupled peers, no shared state
- **C4b** Multi-agent with shared state or recursive composition

The C4a / C4b split is material: empirical work on multi-agent drift (Gagne 2026[^1], replicated against the Sentinel corpus) shows phase transitions in the C4a regime within typical baseline-establishment windows. Stateless NL-coupling is not safe simply because no state is shared.

### 4.4 Reversibility (V)

Each tier carries an explicit recovery horizon.

- **V1** Fully reversible, horizon ≤ minutes (idempotent, local state)
- **V2** Reversible with effort, horizon ≤ hours (compensating transactions, manual rollback)
- **V3** Partially reversible, horizon ≤ days (data restoration, customer communication)
- **V4** Practically irreversible, horizon > days or requires external cooperation

### 4.5 Consequence (K)

K decomposes into sub-domains so evidence burden aligns with regulatory regime.

- **K1** Minor inconvenience
- **K2** Operational disruption
- **K3** Material impact — K3-F (financial), K3-L (legal/contractual), K3-P (privacy/GDPR)
- **K4** High-consequence — K4-S (safety/clinical), K4-R (regulated/systemic), K4-F (fundamental rights per EU AI Act Annex III)

### 4.6 Observability (O)

- **O0** No runtime observability
- **O1** Coarse telemetry (success/failure, latency)
- **O2** Action-level logs, replayable traces, manual review
- **O3** Real-time anomaly and drift detection, auditable decisions, evidence preserved
- **O4** Real-time detection plus **architectural invariants checkable at runtime** (capability boundaries, action-class enforcement, coupling constraints, ontology membership)

Observability is a first-class axis *and* a cross-cutting enabler: Invariants 1–5 (§9) are only *verifiable* if O ≥ 2 (replay), and O ≥ 4 is what separates architectural enforcement from architectural assertion.

## 5. Profile, aggregation, cardinal score

### 5.1 Ordinal aggregation

Base rule: BR class = max over A, R, C, V, K where each tier maps to a candidate class.

**Interaction overrides** (non-linearity made operational):

1. **C4a or C4b + V ≥ 3 → promote one class.** High coupling with irreversibility compounds non-linearly.
2. **A ≥ 3 + K4 → minimum BR-4.** Bounded execution in high-consequence domains never rates below BR-4.
3. **R4 + O ≤ 1 → promote one class.** External reach without observability cannot be governed by post-hoc review.
4. **Seventh invariant (§9) absent → promote one class.** Bounded coupling is not structurally present → effective BR up by one. (If the system contains an open-world component, §4.0 already sets the BR floor to 4; this rule applies only to closed-world systems where Invariant 7 is partially absent, e.g. mixed C4a interfaces within a nominally typed topology.)

**Observability modifier:**

- O0 or O1 on any BR-3+ system → promote one class
- O4 with architectural invariants at runtime → may demote one class *only if* V ≤ 2 and §9 invariants all hold.

### 5.2 Cardinal score — BR-ECR

An internal reference implementation defines Expected Compliance Risk as `B(t) = w_d·D + w_r·R + w_v·(1−V) + w_c·C`. v0.3 extends this to all six axes:

**B(t) = w_a·A + w_r·R + w_c·C + w_v·(1−V) + w_k·K + w_o·(1−O)**

where each axis tier is normalised to [0, 1] and weights are calibrated per deployment domain (clinical weights differ from payments weights differ from analytics weights). The ordinal BR class is a thresholding of B(t); the cardinal score is what specialist underwriters can use directly.

The cardinal score and the ordinal class must agree within one BR class; disagreement is a calibration signal for the weights.

### 5.3 λ / σ / υ priors implied by the tuple

The tuple implies actuarial priors:

- **Frequency (λ)** — C-axis and O-axis dominate. C4a + O≤2 systems have empirically fast-onset drift (Sentinel); expected incident frequency is structurally higher and unstable under model updates.
- **Severity (σ)** — K-axis and R-axis dominate. K4 with R≥3 produces correlated loss across the principal population.
- **Uncertainty (υ)** — under v0.4 this was derived from V-axis and δ_adv qualitatively. Under v0.5 (§5.4) it becomes the direct output of the Kalman-filtered cardinal estimate: υ ≡ σ_B(t).

The cardinal score feeds these priors directly when Invariants 1–2 (deterministic execution + evidence binding per §9) are present. Absent those invariants, no priors can be extracted and the system is structurally unpriceable.

### 5.4 Kalman extension — uncertainty-aware rating

The v0.3 cardinal score is a point estimate. Kalman filtering provides the operational mechanism to extend it to a filtered estimate with explicit uncertainty, producing the form underwriters actually need. The framework-centric architecture and Kalman-as-compliance-state-estimator approach derive from an internal reference implementation (credited in [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)); the specification below distils the mechanism into a portable form.

**State-space model.**

- Latent state x(t) = normalised six-axis tuple (the true compliance posture)
- Observation y(t) = rubric evaluations, tool-call outcomes, evidence submissions at time t
- **Measurement noise R** per tiered evidence confidence: forensic tier = low R (high trust), minimal tier = high R (low trust). Evidence tier becomes a *quantitative noise model*, not a qualitative label.
- **Process noise Q** = per-domain prior on how quickly compliance posture can shift between observations

**Filter equations:**

Predict: x̂(t|t−1) = A·x̂(t−1|t−1); P(t|t−1) = A·P(t−1|t−1)·Aᵀ + Q

Update: K(t) = P(t|t−1)·Hᵀ·(H·P(t|t−1)·Hᵀ + R)⁻¹; x̂(t|t) = x̂(t|t−1) + K(t)·(y(t) − H·x̂(t|t−1)); P(t|t) = (I − K(t)·H)·P(t|t−1)

**Cardinal score under the extension.**

- Filtered estimate: **B̂(t|t) = w·x̂(t|t)**
- Uncertainty: **σ_B(t) = √(wᵀ·P(t|t)·w)**
- Rated output: **B̂(t|t) ± σ_B(t)**, replacing the v0.3 point score

**What this changes:**

1. **υ becomes a direct Kalman output.** Specialist underwriters (Munich Re aiSure, AIUC, Armilla/Lloyd's) receive point estimate + quantified uncertainty — the minimum data their actuarial models need. The v0.4 framework produced υ qualitatively; v0.5 produces it numerically.
2. **Evidence tier has quantitative effect.** Moving a control from minimal-tier evidence to forensic-tier evidence *reduces σ_B(t)* by reducing R. Evidence investment becomes directly price-relevant, not merely compliance-relevant.
3. **Adaptive BR thresholds.** The §5.1 interaction overrides are ordinal; Kalman supports continuous adaptive thresholds: *threshold(t) = baseline + k · σ_B(t)*. High-noise sessions get looser thresholds; low-noise sessions get tighter ones. Alerts fire on *statistically significant* deviations, not on arbitrary fixed bands.
4. **Kalman gain K(t) makes weight-of-evidence explicit.** Each new observation's influence on the estimate is quantified by K(t), with forensic-grade evidence producing higher gain and minimal-grade producing lower. Auditors can trace why a particular evidence submission moved the rating by how much.

**Subsumption of prior truth-value models.** The NAL truth-value model (frequency f, confidence c, from Xu 2025 AIKR grounding) is a special case of Kalman with scalar state and no dynamics. The same relationship holds here: v0.3's ordinal aggregation is Kalman with infinite Q (no prior carried forward); v0.3's point cardinal score is Kalman at a single observation. v0.5 generalises both to the temporal-dynamic case.

**Dependencies on the invariants.**

The Kalman extension is only meaningful if Invariants 1–2 hold:

- Invariant 1 (deterministic execution) — the filter requires that identical inputs under identical policy snapshots produce identical observations. Without it, measurement noise R cannot be separated from genuine compliance drift.
- Invariant 2 (evidence binding) — R is meaningful only if evidence tiers are attested and tamper-evident. Unsigned evidence has unknown R.

A system failing Invariant 1 or 2 cannot produce σ_B(t). It retains an ordinal rating but **cannot quantify υ and is structurally unpriceable**. This is the architectural boundary between insurable and uninsurable made precise.

**Three-phase implementation path:**

- Phase 1 — scalar Kalman on a single deployer metric. Target: replace rolling-mean on a chosen compliance ratio with a Kalman-filtered ratio ± σ. Outputs the quantity ± σ(t) instead of a point estimate and separates measurement noise from genuine drift.
- Phase 2 — multivariate state vector (e.g. compliance-decision ratio, resolution-tier distribution, evidence-confidence mean). Full covariance P(t) captures correlations between drift signals.
- Phase 3 — per-session compliance trajectory. Per-session Kalman state maintained across tool-call sequence. *dB̂/dt* becomes the compliance trajectory signal.

**Research arc beyond v0.5.** Kalman is the optimal linear estimator. For nonlinear compliance dynamics, EKF or UKF apply. For non-Gaussian compliance distributions, particle filters are the general solution. Beyond that, HMM regime detection captures phase transitions. Framework versions after v0.5 will encode richer estimators as implementation experience accrues.

**Honesty note.** Implementations of the Kalman extension are under way in a private reference implementation; public deployer implementations at the time of v0.5 are limited. Until Phase 1 lands in a deployer's environment, σ_B(t) is a theoretical construct; claims of σ_B(t) without implementation are overstating.

## 6. Modifiers

### 6.1 Attack-accessibility (δ_adv)

- **δ_adv = 0** — adversarial escalation path analysed and closed
- **δ_adv = +1** — known paths with mitigations, residual risk
- **δ_adv = +2** — unanalysed or open adversarial surface

Effective class = base class + δ_adv.

### 6.2 Trajectory (τ)

- **τ = stable** — no class change in review period
- **τ = expanding** — accepted tool/reach additions; class recomputed
- **τ = drifting** — observed behaviour suggests movement not reflected in configuration

Drift is a state to be measured, not a failure mode to be discovered. BR-3+ requires a documented trajectory review cadence.

### 6.3 Residual vs inherent

Report both: **inherent BR** (absent mitigating controls) and **residual BR** (with controls operating). Audit is about narrowing the gap.

## 7. Composition

### 7.1 Pairwise composition rule

If System X invokes System Y (ungoverned or governed under a different framework):

1. Treat Y as an additional tool under X's A-axis
2. Inherit Y's K (consequence is a property of what the action touches)
3. Take max(C_X, C_Y); promote by one if the X–Y interface is NL rather than typed
4. Take min(O_X, O_Y) on the joint action path
5. Apply §6.1 δ_adv to the interface itself
6. **Insurability composition:** if either X or Y fails Invariant 1 or 2 (§9), the composed system is unpriceable regardless of the other component's rating. Insurability is not preserved under composition with uninsurable components.

Vendors that cannot supply a rating for their side of the interface cannot be composed into a rated system; the integrator must rate them or decline the composition.

### 7.2 Composition classes — four topologies, four mathematics

Before applying §7.1 pairwise, the composition *topology* must be identified. Four topologies appear in agentic systems, each with distinct compound-risk mathematics. Reading the topology wrong leads to the common error of rating a chain as if it behaves like voting, or vice versa.

Notation: Rᵢ is the per-component failure probability; BRᵢ is the per-component blast radius; n is chain length; P_bypass,ᵢ is the per-layer attack bypass probability.

**T1. Sub-additive — closed-world narrow fail-closed chain.**

Components are closed-world (§4.0), each fail-closed, connected by typed interfaces. One component's failure halts the chain; failure does not propagate into the next component's reasoning.

- **P(chain failure)** ≈ 1 − ∏(1 − Rᵢ) (union bound; approximately Σ Rᵢ for small Rᵢ)
- **BR(compound | failure)** ≤ max(BRᵢ) — blast radius is bounded by the worst component's individual BR because the typed boundary stops propagation
- **Expected compound BR** is bounded, not divergent with chain length

Reference: DOP multi-agent deployment with AARP routing. Each agent's ontology firewall halts on ambiguity; the next agent never sees NL output.

**T2. Super-additive — open-world NL-coupled chain.**

Components are open-world (§4.0), connected by NL. One agent's output becomes the next's context. Failures correlate through shared substrate: model-provider updates, drift synchronisation, context poisoning travel.

- **P(chain failure)** exceeds additive — failures are correlated with non-trivial ρ
- **BR(compound | failure)** > max(BRᵢ) — propagation is unbounded because NL carries the failure to the next component's reasoning surface
- **Expected compound BR diverges with n** — this is the reinsurance correlated-loss pattern named in the 2025 insurability piece

Reference: A2A peer chains, CrewAI/AutoGen default, LLM-as-judge recursion. Sentinel empirical evidence: collapse inside 15 turns for n ≥ 2.

**T3. Multiplicative — defence-in-depth attack composition.**

Distinct from T1/T2 because it concerns *attack bypass*, not *failure propagation*. Layers are in series for an attacker (must bypass each one); compound bypass probability is the product.

- **P(bypass compound)** = ∏ P_bypass,ᵢ (independent layers) or product with correlation term (realistic)
- Reference: a private reference implementation's Bayesian threat-model analysis over 8 layers of indirect-prompt-injection defence gives compound bypass ≈ 10⁻¹⁹ under the model's independence assumptions. Sobol sensitivity identifies the dominant-contributor layer for remediation priority. The analytical shape (Bayesian per-layer priors, Monte Carlo sampling of compound bypass, Sobol indices for residual risk concentration) is portable and is what this framework references; the specific number is illustrative, not canonical.
- **Important distinction:** T3 mathematics applies to *attack resistance* against an adversary trying to bypass controls, not to *failure propagation* from one component to another. Both T1 and T3 can coexist in the same system (T1 for failure propagation, T3 for attack bypass) and they reinforce each other.

**T4. Exponential-reducing — voting / parallel redundancy.**

Independent components evaluate the same decision; output requires quorum. Per-component failure is independent.

- **P(joint failure)** = P(≥ k fail) — binomial tail, exponentially small in n for fixed failure rate < k/n
- Reference: LLM ensemble voting with architectural independence (different models, different providers, different prompts). Rarely implemented correctly because "LLM-as-judge with the same model family" violates independence (and is actually T2 in disguise).

**Topology recognition rules:**

- If every component is closed-world and interfaces are typed → **T1 sub-additive**
- If any component is open-world, or any interface is NL → **T2 super-additive**
- Attack-resistance composition (architectural layers against an adversary) → **T3 multiplicative**
- Parallel independent evaluators with quorum → **T4 exponential-reducing**

Mixed topologies are common (e.g. a closed-world T1 chain with T3 defence-in-depth per component). Rate each sub-topology separately and combine per §7.1 pairwise.

**Recognising T2-in-disguise.** The most common misclassification is LLM-as-judge or same-model-family voting rated as T4 when it is actually T2: the "independent" evaluators share substrate and correlate on failure. The BR framework requires evidence of independence (different model families, different providers, different prompts, independently tuned thresholds) before granting T4 treatment.

### 7.3 Invariant 7 as composition gate

Invariant 7 (bounded coupling, §9) is the gate that separates T1 from T2. Closed-world substrate with typed interfaces satisfies Invariant 7 structurally; open-world substrate or NL interfaces do not. A composition can claim T1 sub-additive mathematics only if Invariant 7 holds across all interfaces. If it does not, the composition defaults to T2 super-additive, and compound BR diverges with chain length.

This is why the worldview classifier (§4.0) is a *pre-rating* gate: it determines which composition class applies, which determines whether the ordinal rating has arithmetic meaning.

## 8. Blast-radius classes

- **BR-1 Contained.** Low authority, limited reach, fully reversible, observable.
- **BR-2 Managed.** Limited execution, controlled scope, human oversight, action-level logs.
- **BR-3 Expansive.** Write capability, multi-system reach, partial autonomy, real-time observability required.
- **BR-4 Systemic.** High coupling, high reach, limited reversibility, high consequence. Requires architectural guarantees plus runtime controls.
- **BR-5 Intolerable without formal governance.** High consequence combined with high coupling or low reversibility. Requires pre-deployment architectural proof, formal assurance, regulatory alignment, insurability evidence.

## 9. The seven architectural invariants

A BR profile is *genuine* only if seven architectural invariants hold. These are not features to be added — they are design-time properties that enforcement is composed from. Six derive from the 2025 insurability piece; the seventh is added from Sentinel empirical evidence on fast-onset coupling drift.

Each invariant supports specific framework axes. A rating that cannot demonstrate the corresponding invariants is inherent-only, not residual.

### Invariant 1 — Deterministic execution

For identical inputs under identical policy snapshots, the system must produce identical outputs.

**Supports:** V (replay underpins rollback evidence), O (cannot audit what you cannot reproduce).
**Anti-pattern complement:** B9 (no replay capability).
**Reference implementation pattern:** deterministic canonical contract hashing over the full evidence tuple (inputs, policy snapshot, outputs, tool calls), with reproduction verified at audit time.

### Invariant 2 — Evidence binding

Every decision must produce immutable policy state, execution context, and outputs. Tamper-evident, audit-admissible.

**Supports:** O (evidence is the observable surface), K (regulatory evidence requirements).
**Anti-pattern complement:** B1 (logs-as-evidence), B6 (unsigned or self-signed-only), B8 (mutable at rest).
**Reference implementation pattern:** externally-anchored Merkle-proof evidence with independent signing keys (Ed25519/ES256/HMAC). SAPP (Settlement Anchor Protocol Platform) is one such design; the essential properties are that the anchor's signing keys are independent of the system under audit, and that evidence commitments are append-only and verifiable by third parties.

### Invariant 3 — Policy snapshot coherence

Versioned policy states; every execution bound to a specific policy epoch.

**Supports:** V (explainability of past decisions), K (regulatory traceability).
**Anti-pattern complement:** B7 (no explainability source mapping).
**Reference implementation pattern:** a `policy_snapshot_id` linkage tuple carried in every evidence record; policy-snapshot hash bound cryptographically to the decision; external rubric loading with version binding so versions are not spoofable.

### Invariant 4 — Bounded blast radius

Failures in one component, tenant, or execution cannot propagate unboundedly.

**Supports:** R (population exposure), K (correlated severity σ).
**Anti-pattern complement:** A1–A7, A11–A13 each break the bound in specific ways.
**Reference implementation pattern:** capability-routing broker (narrow closed-world); action-class taxonomy (advisory / constrained-proposal-with-attestation / bounded-execution-with-attestation / prohibited) with the prohibited class structurally unreachable; tool-ontology binding restricting invocation to ontology-declared shapes; ontology-as-firewall distributed enforcement (§15).

### Invariant 5 — Jurisdictional awareness

Jurisdictional constraints on data flow, decision authority, and regulatory requirements are enforced structurally.

**Supports:** K sub-tags (K3-P, K4-R, K4-F), R (cross-border reach).
**Anti-pattern complement:** A13 (BYOA into corp data).
**Reference implementation pattern:** policy hierarchy with fixed precedence (regulatory > corporate > manager > local > user), regulatory tier unoverridable; jurisdictional conflict resolution that fails closed and escalates; DNS-anchored on-behalf-of verification for cross-border admission.

### Invariant 6 — Fail-closed execution control

Deny by default. Execution requires explicit cryptographic verification of evidence sufficiency.

**Supports:** A (authority enforcement), V (fail-closed preserves reversibility at decision time).
**Anti-pattern complement:** B11 (critical action fail-open).
**Reference implementation pattern:** dual policy enforcement points (pre-pipeline and tool-level) with default DENY; action classification with prohibited class structurally unreachable; critical-action fail-closed policy (local or anchor write failure blocks the action); session-execution attestation tokens with cryptographic verification blocking tool execution on missing or invalid tokens.

### Invariant 7 — Bounded coupling (added v0.3)

Agent-to-agent and workflow interactions must be typed and bounded. NL-coupled peers (C4a) and shared-state/recursive peers (C4b) violate this unless mediated by typed protocol with fail-closed defaults.

**Why added.** Gagne's multi-agent drift corpus (Gagne 2026[^1]): in the C4a regime, governance-signal crossings occur at window ≤ 3 of 10 in 20 of 23 experiments under monitoring-apparatus replication — i.e. collapse happens inside the baseline-establishment window of any runtime monitor. Invariants 1–6 are insufficient if coupling is unbounded because monitoring races and loses.

**Supports:** C axis (directly), A (bounded coupling makes authority grants meaningful), O (monitoring is only useful if substrate is bounded).
**Anti-pattern complement:** A1 (A2A), A3 (MCP without composition), A6 (CrewAI/AutoGen default persona+NL), A7 (LLM-as-judge).
**Reference implementation pattern:** agent-agent NL communication rejected architecturally; capability routing via a broker with typed requests; NL between agents structurally prevented by the protocol shape, not by convention.
**Operational role in rating:** Invariant 7 is the gate between §7.2 composition topology T1 (sub-additive) and T2 (super-additive). It is enforced at two points: §4.0 worldview classifier (pre-rating — open-world components cannot claim it) and §7.2 composition class (post-component-rating — any NL interface downgrades to T2). A closed-world component chain with typed interfaces satisfies Invariant 7; any NL-interface break in the chain breaks the invariant and the composition mathematics with it.

### Cross-cutting: observability

O is a rating axis and simultaneously the *verifiability surface* for Invariants 1, 2, 3, 4, 5. O ≥ 2 is the minimum for any invariant claim to be auditable; O = 4 with architectural invariants checkable at runtime is what separates architectural enforcement from architectural assertion.

## 10. Governance implications

Controls must match the class. At BR-4 and BR-5, controls must include architectural requirements, regulatory requirements, *and* insurability requirements.

| Class | Minimum controls |
|-------|-------|
| BR-1 | Logging, clear ownership, deprecation path |
| BR-2 | Approval gates, audit trails, incident runbook, quarterly review |
| BR-3 | Tool scoping, containment, rate limits, real-time observability (O3+), documented kill switch, trajectory review |
| BR-4 | All BR-3 plus: Invariants 1–7 documented and verifiable; independent oversight; adversarial testing; O4 architectural invariants at runtime; coupling constraints enforced structurally; composition attestation for dependencies |
| BR-5 | All BR-4 plus: pre-deployment architectural proof; formal assurance documentation; regulatory alignment evidence; **insurability evidence** (reproducible decision trails, immutable evidence retention per an externally-anchored Merkle-proof minimum profile, policy snapshot coherence, documented blast-radius containment with quantified bounds, jurisdictional enforcement record); independent pre-deployment review; demonstrated reversibility plan |

Absence of insurability evidence at BR-5 is not a nice-to-have gap — it foreclosures commercial deployment in regulated sectors via specialist underwriters' exclusions (e.g. Verisk 2026 AI exclusions applied through commercial insurance contracts).

## 11. Non-linearity of risk

Blast radius is not additive. Moderate authority plus high coupling plus low reversibility can exceed the risk of high authority in an isolated system. §5.1 interaction overrides encode the primary non-linearities formally. Sobol sensitivity analysis applied to a per-layer defence-in-depth threat model is the equivalent quantitative demonstration within an architecture: residual risk concentrates in one layer non-uniformly, and remediation priority follows the index, not the nominal count of layers.

## 12. The observability gap

Agentic systems may pass monitoring checks, show stable metrics, and appear to improve — while system state has crossed failure thresholds. Blast radius can expand while the system appears healthy. Three practical consequences:

1. **Coarse telemetry is not observability.** O1 does not surface drift in the C-axis or emergent coupling in the R-axis.
2. **Post-hoc auditability is not runtime observability.** O2 supports incident review, not real-time intervention.
3. **O4 requires architectural invariants.** To observe that a capability boundary is still enforced, the boundary must be machine-checkable, not only documented.

Reframe: observability is not "can we investigate an incident" but "would we know, now, that the system is outside its rated profile".

## 13. Mapping to security operations

AI governance will be absorbed into security operations rather than run alongside them. Governance functions produce policy; security functions produce controls that run at 3am. Agentic AI needs the latter.

### 13.1 From CIA to CIA + Agency

Traditional information security guarantees confidentiality, integrity, availability. Agentic AI introduces a fourth property:

**Agency** — the ability of a system to take autonomous or semi-autonomous action on connected systems, bounded by its authority, reach, and coupling profile, under a defined threat model.

The A–R–C–V–K–O tuple is the operational vocabulary for agency, the way an ACL is the vocabulary for confidentiality.

### 13.2 Axis-to-primitive mapping

| Axis | Existing security primitive | Agentic extension |
|---|---|---|
| A Authority | IAM, least-privilege, capability tokens | Action-class enforcement at runtime |
| R Reach | Network segmentation, lateral-movement surface | Principal-population accounting |
| C Coupling | Trust zones, boundary enforcement | NL-coupling as distinct propagation mode (C4a) |
| V Reversibility | Backup, DR, RTO/RPO | Recovery horizon per action class |
| K Consequence | Data classification | *Action* classification with regulatory sub-tags |
| O Observability | SIEM, detection engineering | Architectural invariants checkable at runtime |
| δ_adv | Threat modelling, red team | Prompt injection, tool confusion as tier-promotion |

### 13.3 BR-4/5 architectural controls *are* security controls

At BR-4+, architecture *is* the preventive control surface. A capability boundary that is not machine-checkable at runtime is not a control; it is an assumption. A coupling constraint not enforced structurally cannot be monitored because monitoring loses the race. A kill switch that has not been exercised is a policy statement.

### 13.4 Four-owner operating model

- Security function owns δ_adv rating and attestation review
- Risk/governance owns K sub-tag mapping and regulatory crosswalk
- Architecture review owns §5 aggregation and §7 composition
- Operations owns τ cadence and kill-switch exercise

Four owners, one tuple. This vocabulary lets the teams share context without negotiating one per engagement.

## 14. Insurability as economic gate

Insurability cuts faster than regulation.

- Regulation moves on multi-year cycles; insurers reprice annually or faster.
- Regulation sets minimum acceptable standards; insurers set pricing that determines deployment viability.
- A system can be regulatorily compliant and commercially uninsurable — at which point it cannot be deployed in regulated sectors regardless of what the regulation permits.
- Verisk's 2026 AI exclusions take effect through commercial insurance contracts, not regulatory enforcement.

Specialist underwriters (Munich Re aiSure, AIUC with AIUC-1 certification, Armilla via Lloyd's) have already published criteria: reproducible decision trails, immutable evidence retention, policy coherence over time, blast-radius containment, jurisdictional boundaries. These are Invariants 1–6 by different names. A system that satisfies the seven invariants can be priced; one that cannot satisfy Invariants 1–2 is structurally unpriceable and should be treated as uninsurable.

The v0.5 Kalman extension (§5.4) makes this precise. Tiered evidence confidence maps to the Kalman measurement noise R, so the actuarial uncertainty σ_B(t) is a direct function of the evidence quality the system produces. This closes the actuarial circuit: invariants → evidence tiers → R → σ_B(t) → υ → premium. A deployer that invests in forensic-grade evidence reduces R and therefore reduces σ_B(t) and therefore reduces the υ component of the underwriter's price. Evidence investment becomes price-relevant, not just compliance-relevant — which is the economic mechanism that rewards architecture over policy.

The 2×2 survivability map (architectural invariant enforcement × market access under constraint) yields four quadrants. The useful mapping:

- **Quadrant IV Consolidation Zone ≈ BR-2/BR-3 with Invariants 1–7 intact** — the post-correction operating standard
- **Quadrant III Stagnation Zone** — nominal BR-2/3 but effective BR-4 because evidence is post-hoc or determinism absent
- **Quadrant I Volatile Zone** — unrateable by construction (agent marketplaces, CrewAI default, MCP-without-composition); treat as BR-4 minimum
- **Quadrant II Protected Zone** — low commercial exposure; research-only

This framework and the specialist-underwriter criteria are independent derivations of the same requirements from different directions.

## 15. Compositional enforcement — the ontology-as-firewall pattern

A pattern that appears repeatedly in genuinely architectural systems deserves naming: **enforcement by composition of typed boundaries rather than a single named gate**.

The canonical example is DOP's ontology-as-firewall:

- Normaliser strips control characters
- Dictionary mapper resolves phrases against SKOS ontology
- NFM facts bind intent to concept URI
- Template selector preconditions gate on concept URI + confidence
- Rubric evaluator runs Ed25519-sealed rules
- Evidence contract is tamper-evident and policy-snapshot bound
- Session-execution attestation verifies the call chain

No single stage is "the firewall". The ontology is the firewall — it determines what can exist at all. An attacker controlling raw input cannot invent a concept URI that doesn't exist. In one private reference implementation, compound bypass probability is quantified at ~10⁻¹⁹ via a Bayesian threat model with Beta-distributed per-layer priors, validated by Monte Carlo simulation and a CI-integrated synthetic attack harness (BPER — Bypass Prevention Efficacy Rate). The analytical method is portable; the specific figure is illustrative of what the method can produce for a well-designed composition.

**Why the pattern matters for rating.** An auditor searching for "an ontology firewall gate" and finding none will rate the control documentary. The correct procedure is to look for the *shape* of enforcement — is the property (ontology membership, typed boundary, action class) enforced across multiple stages such that bypassing one stage does not bypass the property?

The v0.1 of the DOP audit (now corrected) made this exact error. The lesson: when rating any system, check for compositional enforcement before calling a control documentary. Formal validation (Bayesian threat model, bypass harness, synthetic attack suite, Sobol sensitivity analysis) is the evidence that composition produces an architectural guarantee, not just defence in depth.

## 16. Self-assessment for architects

Applied to one's own system:

- Do we observe the C-axis *at runtime*, or only at architecture review?
- Is there a documented, exercised kill switch at the composition layer?
- When a new dependency is added, do we recompute the profile?
- If monitoring races and loses (τ = drifting with fast onset), is Invariant 7 enforced structurally?
- Can we produce evidence for Invariants 1–7 without hand-waving?
- Would a specialist underwriter find what they need in our evidence pack?

A framework that does not make its authors uncomfortable is too lenient.

## 17. Vendor questionnaire (purchasing / RFP)

1. **Profile.** State the A–R–C–V–K–O tuple for the product in the proposed deployment context. If multi-configuration, state the highest-class configuration supported.
2. **Aggregation.** State the resulting BR class using §5.1. Identify which interaction overrides fire. Report the §5.2 cardinal score B(t) with weights disclosed.
3. **Invariants.** For each of Invariants 1–7 (§9), describe how the property is enforced (architectural / structural / procedural / documentary) and cite the evidence that allows an auditor to verify.
4. **Modifiers.** δ_adv analysis and mitigations; τ cadence and last three outcomes; residual vs inherent separated by named controls.
5. **Composition.** External systems called; rated profile per dependency; insurability assumption for each.
6. **Architectural evidence (BR-3+).** Invariants enforced structurally on A and C axes, not monitored.
7. **Reversibility plan.** For V3/V4, rollback mechanism, recovery horizon, last successful rollback exercise.
8. **Kill switch.** Mechanism, authorised operators, activation time, last test.
9. **Observability evidence.** Sample of what an auditor would see in the first 24 hours of an incident.
10. **Change management.** Profile recomputation triggers.
11. **Insurability disclosure.** Which specialist underwriter has reviewed the profile; what evidence was supplied; outcome.
12. **Anti-pattern attestation.** Does the system exhibit any patterns from the anti-pattern catalogue? For each exhibited, describe the demotion path implemented.
13. **Attestation.** Accountable executive, date of last independent review.

A vendor that cannot produce this disclosure for a BR-3+ product has not rated its own system; treat residual BR as inherent BR, and inherent BR as unknown.

## 18. Central claim

The operational risk of agentic AI systems is determined by architecture, not model capability. This single claim is true from three independent directions:

- **Engineering.** Systems with bounded A–R–C–V–K–O tuples and Invariants 1–7 enforced exhibit quantifiable, attestable behaviour; systems without do not.
- **Regulatory.** EU AI Act Articles 12, 15, 19, 26(6), 72 require evidence that architecture must produce; policy layered on top cannot substitute.
- **Actuarial.** Specialist underwriters cannot price systems that fail Invariants 1–2; Consolidation Zone is BR-2/BR-3 with Invariants 1–7 intact.

The three communities arrive at the same requirement.

## 19. Open questions for v0.6

1. **Weight calibration.** The §5.2 cardinal score uses per-domain weights. A public calibration corpus (clinical, financial, operational) would let organisations align B̂(t|t) interpretation.
2. **Benchmarks.** Reference profiles for common archetypes (customer support, code assistant, clinical triage, RAG pipeline, multi-agent researcher).
3. **Regulatory crosswalk.** Direct mapping from BR class + K sub-tag to EU AI Act obligation, NIST RMF activity, ISO 42001 control.
4. **Specialist-underwriter crosswalk.** Explicit mapping from Invariants 1–7 and the §18 disclosure items to Munich Re aiSure, AIUC-1, Armilla/Lloyd's published criteria.
5. **Certification path.** Minimum viable attestation scheme for a vendor to claim a BR class. SOC-2-shaped third-party audit is the obvious model.
6. **Insurability composition — quantitative.** §7.1 rule 6 is architectural; §7.2 topologies give the qualitative shape; quantitative compound λ/σ/υ under each topology (particularly T2 with measured correlation ρ) still needs derivation. ISS-composition-with-bounded-gain is the mathematical backbone; translating ISS gain bounds to insurance-pricing language is the next step.
7. **Trajectory quantification.** τ is currently categorical (stable/expanding/drifting); with Phase 3 of the Kalman extension implemented, *dB̂/dt* becomes the continuous trajectory signal underwriters can price. Mapping dB̂/dt magnitudes to τ categories (and eventually replacing the categorical form) is the v0.6 path.
8. **T2 correlation estimation.** Super-additive composition (§7.2) requires an estimate of ρ between components sharing LLM substrate. Empirical ρ for common model-provider pairs is unstudied; Sentinel-style instrumentation could produce the first estimates.
9. **T4 independence attestation.** Voting ensembles are frequently claimed T4 but operate T2. A minimum-viable independence attestation (different model families, different providers, different prompt derivations, uncorrelated failure history on a shared benchmark) is the evidence a BR-4+ deployment should require before granting T4 treatment.
10. **Evidence-tier → R calibration (v0.5 Kalman extension).** Evidence-tier taxonomies are qualitative in current practice; the Kalman extension maps them to measurement noise R. The *numerical R values* per tier per domain are not yet published. Without these, σ_B(t) is only directionally meaningful. First-deployer Phase 1 implementations will produce the first empirical R estimates.
11. **Process noise Q per domain.** Q encodes prior belief about how fast compliance posture can shift between observations. Too small Q underestimates σ_B(t) (overconfident); too large Q makes the filter track noise. Domain-specific Q calibration is a prerequisite for cross-deployer comparability.
12. **Nonlinear extensions.** EKF / UKF for nonlinear dynamics; particle filters for non-Gaussian compliance distributions; HMM for regime detection. Each becomes a framework version as implementation experience accrues.

## 20. Conclusion

Tool-enabled AI is a transition from bounded reasoning to unbounded action across connected systems. Closing the classification gap requires more than a taxonomy: a tuple notation, ordinal + cardinal aggregation, explicit modifiers, a composition rule, seven architectural invariants that make ratings genuine, class-specific controls that include architectural *and* insurability evidence, and a compositional-enforcement pattern that can be audited without being mis-read as documentary.

v0.3 delivers these pieces. The minimum shape is disciplined: six axes, three modifiers, seven invariants, five classes, one questionnaire, one cardinal formula. Further refinement will come from applying it to real systems and converging the weight calibration with specialist-underwriter pricing.

---

**Architecture is the executable form of governance, of regulatory compliance, and of insurability. These are not three problems — they are one problem with three audiences. If blast radius is not designed, it is not controlled, not priced, and not deployable in regulated sectors.**

---

[^1]: Gagne, J. (2026). *Behavioral Drift in Multi-Agent LLM Systems: Emergent Failure Modes, Cascade Dynamics, and Measurement Challenges.* Preprint, DOI: [10.5281/zenodo.19477188](https://doi.org/10.5281/zenodo.19477188). Code + dataset: [10.5281/zenodo.19476723](https://doi.org/10.5281/zenodo.19476723). Repo: [github.com/jasongagne-git/sentinel](https://github.com/jasongagne-git/sentinel). The empirical basis for C4a phase transitions, fast-onset drift, and Invariant 7 (bounded coupling). See [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md) for full attribution.

[^2]: Monitor-vs-substrate analysis against Gagne's corpus: 20 of 23 experiments replicated show governance-signal crossings at window ≤ 3 of 10 under the monitoring-apparatus replication. Substrate property, not apparatus limitation.

[^3]: Private reference implementation — Bayesian Threat Model for Indirect Prompt Injection (Beta-distributed per-layer priors) combined with IPI Defence Validation (compound bypass ≈ 10⁻¹⁹ under the model's independence assumptions). The analytical method is portable; the figure is illustrative. Basis for the compositional-enforcement pattern (§15). Credited in [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md).

[^4]: Brown, K. (2025). *The Insurability Gap: Why Nondeterministic AI Is Structurally Uninsurable, and What Changes When Architecture Produces Evidence Invariants.* Prior published work; six invariants of §9 derive from this. v0.3 adds Invariant 7 (bounded coupling) from Gagne-era evidence post-dating the 2025 publication.

[^5]: Gagne, J. (2026). *The Behavioral Sufficiency Problem: Why AI Governance Frameworks, Modeled on Human Regulatory Theory, Cannot Operate Without the Cultural and Social Infrastructure That Co-Evolved Alongside Human Law.* SSRN Preprint. Governance-theoretic argument complementing the Behavioral Drift empirics.
