# Changelog

All notable changes to the Blast Radius Framework will be documented here. The framework is versioned `vX.Y` with minor revisions preserving section numbering where possible.

## v0.5 — 2026-04-21

**Kalman extension — cardinal score becomes filtered estimate with uncertainty.**

Added `framework.md §5.4 Kalman extension`. The v0.3 cardinal score `B(t) = w·x` is a point estimate; v0.5 replaces it with `B̂(t|t) ± σ_B(t)`, a Kalman-filtered estimate with quantified uncertainty. Tiered evidence confidence maps formally to measurement noise R; evidence quality becomes a quantitative input to uncertainty rather than a qualitative label. σ_B(t) becomes the direct output for the actuarial υ variable (uncertainty), the form specialist underwriters require for pricing.

Four consequences:
1. υ is no longer derived from V-axis and δ_adv qualitatively — it is Kalman filter output
2. Evidence investment reduces R and therefore σ_B(t) and therefore the premium; evidence becomes price-relevant
3. Adaptive thresholds `threshold(t) = baseline + k·σ_B(t)` replace fixed bands
4. Kalman gain K(t) makes weight-of-evidence explicit and auditable

Structural claim: systems failing Invariants 1 (deterministic execution) or 2 (evidence binding) cannot produce σ_B(t); the boundary between insurable and uninsurable is made mathematically precise.

Three-phase implementation path documented (framework-centric compliance state estimation). Framework specifies the mechanism; empirical validation comes as implementations ship. Architectural primitives derive from a private reference implementation credited in [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md).

§19 open questions for v0.6: evidence-tier → R numerical calibration, process noise Q per domain, nonlinear extensions (EKF/UKF, particle filters, HMM).

## v0.4 — 2026-04-21

**Pre-rating worldview classifier and composition classes.**

Added `framework.md §4.0 Pre-rating: the worldview classifier` — each component classified as closed-world (ontology-bounded) or open-world (NL-unbounded) before the tuple is assigned. Any open-world component promotes the system's effective BR to BR-4 minimum regardless of per-axis scores. Rationale: Invariant 7 (bounded coupling) is structurally impossible in open-world substrates, and empirical evidence (Sentinel) shows collapse happens inside the baseline-establishment window of any runtime monitor — making BR-2/BR-3 claims on such substrates architecturally meaningless.

Added `framework.md §7.2 Composition classes` — four topologies with explicit mathematics:
- **T1 sub-additive**: closed-world narrow fail-closed chain; compound BR bounded by max(BRᵢ)
- **T2 super-additive**: open-world NL-coupled chain; compound BR diverges with chain length (correlated-loss pattern)
- **T3 multiplicative**: defence-in-depth attack composition; compound bypass = product of per-layer probabilities
- **T4 exponential-reducing**: voting / parallel redundancy with genuine independence; binomial-tail failure probability

Topology recognition rules and a **T2-in-disguise** test included: most claimed T4 voting ensembles are actually T2 because same-model-family evaluators correlate on failure.

Added `framework.md §7.3 Invariant 7 as composition gate` — the invariant operationally determines whether T1 or T2 applies.

## v0.3 — 2026-04-21

**Seven architectural invariants, cardinal score, insurability as economic gate.**

Added `framework.md §9 seven architectural invariants`:
1. Deterministic execution
2. Evidence binding
3. Policy snapshot coherence
4. Bounded blast radius
5. Jurisdictional awareness
6. Fail-closed execution control
7. **Bounded coupling** (added v0.3 from Sentinel empirical evidence)

Six invariants are from prior published work on insurability (Brown, "The Insurability Gap", 2025). The seventh is added from empirical evidence on fast-onset drift in NL-coupled multi-agent systems. Each invariant lists supported axes, anti-pattern complement, and a reference implementation.

Added `framework.md §5.2 cardinal score` — extends the Expected Compliance Risk formulation (from a private reference implementation, credited in [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)) to all six axes:

`B(t) = w_a·A + w_r·R + w_c·C + w_v·(1−V) + w_k·K + w_o·(1−O)`

Ordinal class and cardinal score must agree within one BR class; disagreement is a calibration signal for the weights.

Added `framework.md §5.3 λ/σ/υ priors` — the tuple implies actuarial priors (frequency, severity, uncertainty) so specialist underwriters can use the cardinal score directly.

Added `framework.md §14 insurability as economic gate` — insurability cuts faster than regulation; 2×2 survivability map (Consolidation / Stagnation / Volatile / Protected Zones) maps to BR classes; Quadrant IV ≈ BR-2/BR-3 with Invariants 1–7 intact.

Added `framework.md §15 compositional-enforcement pattern` — names the ontology-as-firewall architectural pattern as canonical example of distributed enforcement with formal probabilistic validation.

Central claim (§18) reframed: architecture determines risk from three independent directions (engineering, regulatory, actuarial) converging on the same requirement.

## v0.2 — 2026-04-21

**Aggregation rule, composition rule, security-ops mapping.**

Added explicit aggregation rule with interaction overrides encoding the non-linearity of blast radius (`framework.md §5.1`). Added observability as a first-class axis (O0–O4). Added C4a / C4b split of the coupling axis to distinguish NL-coupled peers from shared-state peers. Added K regulatory sub-tags (K3-F/L/P, K4-S/R/F). Added three modifiers: δ_adv attack-accessibility, τ trajectory, residual-vs-inherent.

Added composition rule (`framework.md §7.1`) for multi-vendor stacks: treat external system as tool under caller's A-axis; inherit K; take max(C) with NL-promotion; take min(O); apply δ_adv to the interface.

Added security-operations mapping (now `framework.md §13`) — CIA extended with Agency as fourth property; axis-to-primitive mapping onto IAM, network segmentation, SIEM, threat modelling; four-owner operating model.

Added vendor questionnaire (now `framework.md §18`) for purchasing / RFP use with ten disclosure items.

## v0.1 — initial draft

Five axes (A/R/C/V/K), BR-1 through BR-5 classes, non-linearity narrative, draft governance implications. No aggregation rule, no composition rule, no invariants.
