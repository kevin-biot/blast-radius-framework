# Insurability and Blast Radius

*Mapping the actuarial requirements for agentic AI onto the classification framework*

**Version:** 0.1
**Status:** Research companion — maps prior published work (Kevin Brown, 2025) onto the blast-radius framework
**Date:** 2026-04-21
**Companions:**
- [framework.md](./framework.md) (rating framework, v0.5)
- [manifesto.md](./manifesto.md) (the argument)
- [antipatterns.md](./antipatterns.md) (negative reference)
- [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md) (credits)

---

## 1. Why this note exists

The blast-radius framework was written from the architecture side: what axes to rate, what "done right" looks like, what anti-patterns shipping as "progress" do to the rating. A separate body of work — published in 2025 by the same author on insurability of nondeterministic AI — approaches the same problem from the **actuarial side**: what do insurers need in order to price AI deployments, what are they currently excluding, and what architectural properties close the gap.

The two bodies of work are **independent derivations of the same requirements**. This note makes the mapping explicit so that:

1. The framework gains an economic / market-access frame it currently lacks.
2. The insurance piece gains a formal rating vocabulary (A–R–C–V–K–O) it did not have when written.
3. The combined framing answers a question neither alone does: *what is the minimum architectural shape that is both defensibly rateable and commercially insurable?*

The answer appears to be the same shape, from both directions.

## 2. The actuarial gap (from the 2025 piece)

Traditional insurance pricing needs three variables:

- **Frequency (λ)** — how often failures occur
- **Severity (σ)** — damage distribution per failure
- **Uncertainty (υ)** — confidence in λ and σ estimates

Nondeterministic AI breaks all three. Model updates change λ overnight; a single defect produces correlated losses across every deployment (unbounded σ); no stable history exists to establish υ. Munich Re's researchers concluded that traditional actuarial frameworks do not apply.

Specialist underwriters (Munich Re aiSure, AIUC, Armilla via Lloyd's) are not refusing to cover AI — they are demanding specific architectural properties that make actuarial modelling possible:

- **Reproducible decision trails.** Reconstruct how and why a decision was reached.
- **Immutable evidence retention.** Tamper-evident, survives adversarial scrutiny.
- **Policy coherence over time.** Decisions provably evaluated against the policy in effect at execution time.
- **Blast-radius containment.** Failures isolated, not cascading across tenants.
- **Jurisdictional and operational boundaries.** Respected by design.

A system that cannot supply this data cannot be priced, and therefore cannot be covered. The gap is architectural, not procedural.

## 3. The six invariants (from the 2025 piece) mapped to the framework

The piece names six invariants that survive the correction. Each maps directly to the framework axes, the Expected Compliance Risk formulation (framework.md §5.2), or the anti-pattern catalogue.

### Invariant 1 — Deterministic execution

*"For identical inputs under identical policy snapshots, the system must produce identical outputs."*

| Framework element | Mapping |
|---|---|
| v0.2 §11 "observability gap" | Replay requires determinism; without it O4 is unreachable |
| Anti-pattern catalogue B9 "no replay capability" | Direct complement |
| Reference implementation pattern | Deterministic canonical contract hashing over the full evidence tuple, reproducible at audit time |
| Demotion path | Non-deterministic systems cannot pass MEP-03 — unrateable above BR-2 for regulated deployment |

### Invariant 2 — Evidence binding

*"Every decision must produce immutable policy state, execution context, and outputs."*

| Framework element | Mapping |
|---|---|
| v0.2 §4.6 O axis | O2 requires action-level logs with replay; O3+ requires tamper-evidence |
| Anti-pattern catalogue B1, B6, B8 | Logs-as-evidence, unsigned evidence, mutable at rest — all direct anti-patterns |
| Reference implementation pattern | Externally-anchored Merkle-proof evidence with independent signing keys (e.g. Lane2's SAPP — Secure Agent Payment Protocol — evidence-anchoring layer) |
| SAPP specifically | External anchor, independent signing keys, three-level Merkle proofs, evidence scoring |

### Invariant 3 — Policy snapshot coherence

*"The system must maintain versioned policy states and bind each execution to a specific policy epoch."*

| Framework element | Mapping |
|---|---|
| v0.2 §14.3 (security ops) "a coupling constraint that is not enforced structurally cannot be monitored" | Policy snapshots are the structural binding |
| Anti-pattern catalogue B7 "no explainability source mapping" | Source mapping requires policy-snapshot binding |
| Reference implementation pattern | `policy_snapshot_id` linkage tuple in every evidence record; policy-snapshot hash bound cryptographically to the decision; external rubric loading with version binding |

### Invariant 4 — Bounded blast radius

*"Failures in one component, tenant, or execution cannot propagate unboundedly."*

| Framework element | Mapping |
|---|---|
| v0.2 §4 entire framework | Blast radius *is* the property; tuple quantifies it |
| Cardinal formulation | `B(t) = w_d·D + w_r·R + w_v·(1−V) + w_c·C` — the Expected Compliance Risk operational formula; v0.5 extends to all six axes (framework.md §5.2) |
| Anti-pattern catalogue A1–A7, A9, A11–A13 | Each breaks the bound in a specific architectural way |
| Reference implementation pattern | aARP-style (Autonomous Agent Routing Protocol) narrow closed-world routing; Action Classes A/B/C/D with D structurally unreachable; tool-ontology binding limits reach per tool; R-axis principal-population accounting |

### Invariant 5 — Jurisdictional awareness

*"The system must understand and enforce jurisdictional constraints on data flow, decision authority, and regulatory requirements."*

| Framework element | Mapping |
|---|---|
| v0.2 §4.5 K-axis sub-tags (K3-F/L/P, K4-S/R/F) | Regulatory mapping primitive |
| v0.2 §5.1 interaction override rule 3 (R4 + O≤1 → promote) | External reach without observability cannot be governed |
| Reference implementation pattern | Policy hierarchy with fixed precedence and unoverridable regulatory tier; jurisdictional conflict resolution that fails closed; DNS-anchored on-behalf-of verification for cross-border corridor admission |
| Gap in current DOP audit | K regulatory crosswalk sub-tags not present in domain labels; follow-up ADR candidate #8 |

### Invariant 6 — Fail-closed execution control

*"The system must deny execution by default. When evidence is insufficient, the system stops."*

| Framework element | Mapping |
|---|---|
| v0.2 §4.1 A-axis Action Classes | A0–A2 default; A3+ requires explicit authority grant |
| Anti-pattern catalogue B11 "critical action fail-open" | Direct complement |
| Reference implementation pattern | Dual policy enforcement points with default DENY; action-classification with prohibited class structurally unreachable; critical-action fail-closed policy; session-execution attestation blocking tool execution on missing or invalid tokens |
| Architectural invariant | Class D prohibited not by policy but by not being permissible in any declared mode — the strongest form of fail-closed |

## 4. The two-axis survivability map mapped to BR classes

The 2025 piece offers a 2×2 (architectural invariant enforcement × market access under constraint) with four quadrants. The mapping to BR classes:

| Quadrant | 2025 name | BR-class mapping | Framework rationale |
|---|---|---|---|
| IV — High governance / High survivability | **Consolidation Zone** | Runs at BR-2 or BR-3 *with insurability* | All seven invariants met; passes an externally-anchored Merkle-proof minimum evidence profile; passes framework.md §18 vendor questionnaire; anti-pattern catalogue clean |
| III — High governance / Low survivability | **Stagnation Zone** | Nominal BR-2/BR-3 but effective BR-4 | Documentary controls masquerading as architectural; post-hoc logging (B2), unsigned evidence (B6), no replay (B9). The anti-pattern catalogue's Part B is precisely this quadrant's failure mode |
| I — Low governance / Low survivability | **Volatile Zone** | Unrateable; treated as BR-4 minimum | Agent marketplaces (A4), CrewAI default (A6), MCP-without-composition (A3), A2A (A1) — the VC-funded agent-ecosystem cluster |
| II — Low governance / High survivability | **Protected Zone** | BR-1 or BR-2 by virtue of not being exposed | Research-only, non-commercial, no liability-bearing deployment |

The useful inversion: **Consolidation Zone ≈ BR-2/BR-3 with invariants intact**. A system can be rated BR-3 and still be in the Stagnation Zone if its evidence chain is post-hoc or its determinism is absent. The v0.2 framework and the insurability frame together catch this — v0.2 alone does not, because it rates snapshot properties, not the combined architectural-plus-evidence package.

## 5. Why insurability is a stronger economic gate than regulation

The 2025 piece makes a point the framework should absorb: **insurability cuts faster than regulation**.

- Regulation moves on multi-year cycles; insurers reprice annually or more.
- Regulation sets minimum acceptable standards; insurers set pricing that determines whether deployment is economically viable.
- A system can be regulatorily compliant and commercially uninsurable — at which point it cannot be deployed in regulated sectors regardless of what the regulation permits.
- Verisk's 2026 AI exclusions (referenced in the 2025 piece) take effect through commercial insurance contracts, not through regulatory enforcement.

**Implication for the framework.** BR-4 and BR-5 governance requirements should include *insurability evidence*, not only regulatory evidence. A system that cannot produce the λ/σ/υ data specialist underwriters demand is operationally unrateable at BR-4+, regardless of its EU AI Act posture.

### Suggested §9 addition (v0.3 framework)

For BR-4 and BR-5 controls, append:

> **Insurability evidence.** Deployer must produce: reproducible decision trails, immutable evidence retention per an externally-anchored Merkle-proof minimum profile, policy snapshot coherence, documented blast-radius containment with quantified bounds, jurisdictional enforcement record. Absence of any constitutes an uninsurable profile and disqualifies the BR-4/5 claim regardless of other controls.

## 6. Where the framework and the 2025 piece disagree — and why it's productive

The two pieces mostly agree. Three places they differ productively:

### 6.1 Axis count

The 2025 piece lists six invariants. v0.2 lists six axes (A/R/C/V/K/O) plus three modifiers. The invariants and axes overlap but don't align 1:1 — because the invariants are *architectural properties* and the axes are *blast-radius dimensions*. The mapping in §3 above makes the correspondence explicit: each invariant is an *enforcement mechanism* for one or more axes.

This is a feature, not a bug. Rating needs dimensions; architecture needs invariants. Conflating them is what produces governance theatre.

### 6.2 Observability

The 2025 piece does not name observability as an invariant explicitly. It assumes it follows from deterministic execution + evidence binding + replay. v0.2 elevates O to first-class status because *unobservable systems fail audit even when deterministic and evidenced*.

**Framework position:** v0.2 is correct to elevate O; the 2025 piece should be read as implying it within Invariants 1+2+5. v0.3 should cite this explicitly so no reader infers observability is optional.

### 6.3 Coupling

The 2025 piece does not call out coupling (C-axis) explicitly. The blast-radius framework treats C as the dominant non-linearity source (v0.2 §5 interaction override 1: C4a/C4b + V≥3 promotes one class).

**Framework position:** C is the axis with the most empirical evidence (Gagne's multi-agent drift corpus, see [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md); replication against it shows fast-onset drift). The 2025 piece was written before that evidence was collected. v0.3 adds coupling as a seventh invariant: *"bounded coupling"* — agent-to-agent and workflow-chain interactions must be typed and bounded, not NL-coupled.

## 7. The combined picture

Putting the framework, the DOP reference, the anti-pattern catalogue, and the insurability frame together:

1. **What to rate** — v0.2 six axes + modifiers, aggregation rule, composition rule.
2. **What "done right" looks like** — DOP reference implementation (Action Classes enforced, policy hierarchy, ontology-via-composition firewall with Bayesian validation, SAPP-anchored evidence, dual-gaze observability).
3. **What you're probably rating too generously** — anti-pattern catalogue's 15 architectural + 11 evidence-chain patterns.
4. **Why it matters economically** — insurability is the market gate; uninsurable systems cannot be deployed in regulated sectors; architecture is what closes the λ/σ/υ gap.

A vendor claiming BR-3+ should be required to answer the §13 questionnaire *and* demonstrate the six invariants *and* have no Part A or Part B anti-patterns active without documented demotion paths. A system that passes all three tests is genuinely in the Consolidation Zone.

## 8. Open questions for v0.3

1. **Merge the ECR formulation with the six invariants.** The Expected Compliance Risk formula quantifies blast radius; the invariants define what makes a system ECR-computable in the first place. v0.3 shows the dependency chain.
2. **Cite specialist underwriter requirements directly.** Munich Re aiSure, AIUC-1, Armilla/Lloyd's have published criteria. v0.3 should crosswalk each specialist's published requirements to framework axes, so a deployer can align assurance effort.
3. **λ/σ/υ as quantitative extension.** v0.2 §15 open question #1 asks for a cardinal score. The Expected Compliance Risk formulation provides one. The insurability frame provides the *variables the cardinal score needs to populate* (frequency, severity, uncertainty). The synthesis is the v0.3 quantitative aggregation: given a BR profile, what does it imply for λ, σ, υ?
4. **Coupling as seventh invariant.** As noted §6.3.
5. **Compositional insurability.** If system X is insurable and system Y is insurable, is X ∘ Y insurable? The composition rule in v0.2 §7 answers this architecturally; the insurability extension is what δ_adv and compound λ look like under composition.

---

## 9. Central claim

**The architectural requirements for insurability and the architectural requirements for governed blast radius are the same requirements, derived from different directions.** The framework that answers one answers the other. Deployers who organise their architecture around the six invariants are simultaneously rating-defensible, regulator-aligned, and commercially insurable. Deployers who treat governance as policy layered on top of nondeterministic agentic substrates are in the Stagnation Zone regardless of how many committees they convene.

Both routes end at the same conclusion: **architecture is the executable form of governance, and also the executable form of insurability, and also the executable form of regulatory compliance**. These are not three problems. They are one problem with three audiences.
