# Changelog

All notable changes to the Blast Radius Framework will be documented here. The framework is versioned `vX.Y` with minor revisions preserving section numbering where possible. Patch versions (`vX.Y.Z`) indicate clarifications, worked examples, and extraction of reference content without adding or changing substantive definitions.

## framework v0.5.2 — 2026-04-21

**Artefacts added (no definition changes)** — executes the plan in [`SCOPE.md`](./SCOPE.md):

- **[`report-template.md`](./report-template.md)** — reusable three-tier report format (executive summary / technical findings / ADR remediation backlog). Template version 1.0. Designed for third-party deployer reuse without Lane2-specific assumptions.
- **[`self-assessment.md`](./self-assessment.md)** — Lane2's own self-assessment against framework v0.5.1. Closed-world T1 sub-additive composition of DOP + aARP + SAPP evidence-anchoring layer + PACT pack for a canonical regulated-operational-workflow deployment. Final rating **BR-4** (residual; inherent BR-5 compressed by architectural controls). Surfaces four named gaps: cross-border I5 is structural not architectural; Kalman Phase 1 not yet implemented (σ_B theoretical); τ cadence nominal pending operational trajectory record; principal-population accounting not instrumented in evidence schema.
- **[`self-assessment.json`](./self-assessment.json)** — machine-readable profile conformant to `spec/br-profile.schema.json`. Per-component tiers, composition topology, all seven invariant attestations, all 26 anti-pattern attestations, aggregation with interaction-overrides fired.
- **[`self-assessment-exec-summary.md`](./self-assessment-exec-summary.md)** — Tier 1 executive summary for decision-making managers. Non-technical. Three business impacts, three remediation priorities, insurability posture, recommendation, sign-off.
- **[`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md)** — Tier 3 remediation backlog. 12 ADR candidates, prioritised P0–P3, with dependencies and cross-references.
- **[`SCOPE.md`](./SCOPE.md)** — planning artefact written before execution to keep the work against a written plan.

**Honesty posture of the self-assessment:** published with four named gaps and six anti-patterns marked `exhibited_with_demotion_path`. A self-assessment that came out perfectly clean would indicate the assessment was not applied honestly. The framework's own authors apply the framework to themselves and find maturity items; those items become the remediation backlog rather than being papered over.

No change to framework definitions, axis enums, class definitions, composition topologies, invariants, anti-patterns, or the schema. v0.5.2 is strictly additive artefacts.



**Three additions in response to external review** (the changes external readers would need before adopting):

- **§5.5 Two worked examples** added. Clinical oncology triage advisor (A2–R3–C3–V3–K4-S–O4, closed-world, Invariants 1–7 hold, final BR-4) and cross-border instant-payment corridor agent (A3–R4–C4a–V4–K4-R–O4, closed-world apart from one legacy NL interface, rule 1 promotes to BR-5). Both examples show high BR classes arising honestly from high-consequence domains — closed-world architecture is necessary but not sufficient for low BR. The payments example specifically demonstrates how a single legacy NL interface in an otherwise typed chain promotes the entire corridor one BR class via Invariant 7 (bounded coupling) partial failure.
- **§12 observability gap strengthened**. Previously read as a closing insight; now makes explicit that observability is the axis that makes BR-4 and BR-5 *rateable at all*. Without O ≥ 3, a BR-4 profile is an unverified claim; without O = 4, a BR-5 claim is structurally un-auditable. The Kalman extension's σ_B(t) → υ identification depends on O operationally. Invariants 1–5 are verifiable only at O ≥ 2 and architecturally enforceable only at O = 4.
- **NOTATION.md added as standalone lookup document.** Previously §21 (notation appendix) was embedded in framework.md. Extracted to a dedicated file covering tier enums, modifiers, classes, composition topologies, interaction overrides, cardinal score formulas, Kalman variables, composition-math variables, collision summary, invariants summary, and anti-pattern IDs. Framework §21 is now a short pointer. A reader doing reference lookup no longer has to navigate a 600-line document.

No change to axis definitions, invariant list, composition topologies, interaction overrides, or schema. v0.5.1 is strictly additive / clarifying / reorganising.



## spec v0.1 — 2026-04-21

**Machine-readable conformance artefacts.** New `spec/` directory. Principal additions:

- **`spec/br-profile.schema.json`** — JSON Schema (Draft 2020-12) for a complete BR profile. Required fields for system identification, per-component ratings (worldview, axes A–R–C–V–K–O, modifiers), composition topology (T1–T4), per-invariant attestation with conformance test results, ordinal aggregation with interaction-override list, optional Kalman-extended cardinal score, anti-pattern attestations, signature and external anchor.
- **`spec/invariant-conformance-tests.md`** — empirical test specifications per invariant. Twenty-three tests across Invariants 1–7, each with stable test ID (I1-T1 through I7-T3), procedure, pass criterion, implied enforcement mode, and BR-class applicability. Results are recorded in profiles under `invariants.I{n}.conformance_test_results`.
- **`spec/attestation-format.md`** — signed + anchored attestation format. Canonical serialisation via JCS (RFC 8785), Ed25519 recommended default, acceptable anchor types (SAPP, OpenTimestamps, RFC 3161 TSA, custom Merkle), anchor-to-signature skew tolerance by BR class (BR-3 24h, BR-4 1h, BR-5 5min), six-step verification procedure.
- **`spec/examples/example-profile-closed-world-br2.json`** — worked example: legal citation review assistant, all seven invariants holding, cardinal score computed with σ_B.
- **`spec/examples/example-profile-open-world-br4.json`** — worked example: three-agent NL-coupled research assistant; Invariants 1, 3, 4, 7 fail; open-world floor fires BR-4; cardinal score omitted (Invariants 1–2 failed, cannot produce σ_B).
- **`spec/README.md`** — orientation with per-role usage guide (deployer, auditor, underwriter, regulator).

Both example profiles validate against the schema (verified with `jsonschema` Draft 2020-12 validator). Schema and tests complete for v0.5 of the framework; axis-scoring rubric and third-party certification form remain v0.6+.

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
