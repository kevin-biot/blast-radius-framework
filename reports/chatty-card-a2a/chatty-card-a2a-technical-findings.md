# Chatty-Card A2A — BRF Technical Findings

*Independent rating of a market-default architectural pattern, anchored to measured per-event harm rates from a 1275-conversation transactional workflow experiment.*

**Date of assessment:** 2026-04-29
**Framework version:** v0.5.1
**Template version:** 1.0
**Machine-readable profile:** [`chatty-card-a2a-profile.json`](./chatty-card-a2a-profile.json) (conformant to `spec/br-profile.schema.json`)
**Assessor:** Blast Radius Framework authors, applying the framework to an external pattern (not a self-attestation)
**Companion documents:**
- [`chatty-card-a2a-exec-summary.md`](./chatty-card-a2a-exec-summary.md) — Tier 1 executive summary
- [`chatty-card-a2a-adr-backlog.md`](./chatty-card-a2a-adr-backlog.md) — Tier 3 remediation backlog (for any deployer of this pattern)

---

## 0. Honesty posture

This is a **pattern rating**, not a deployment rating. The system under assessment is not a single product or vendor's stack; it is the architectural pattern that the agentic-AI market currently treats as the default for A2A multi-agent integration. We refer to it as **"chatty-card A2A"**:

- agent capabilities advertised through agent cards consulted by an LLM-prose broker
- inter-agent messaging over free-text natural-language briefings (not typed `Task` / `Artifact` / structured `Part.data` payloads, even though A2A's specification supports those)
- routing decided by LLM prose over agent-card descriptions, not by a deterministic state machine
- domain tools exposed directly to the language model with descriptive `inputSchema` parameters but without domain-gate refusals on unmet preconditions
- retrieval-augmented generation (RAG) of customer / domain context injected unfiltered into broker briefings

A deployer using this pattern can attach this report to their own deployment by inheriting the pattern-level rating and adjusting per-deployment R, K, and δ_adv. The pattern itself produces a BR floor that the deployment cannot exit without changing the architecture.

The empirical anchor for this rating is a controlled experiment: D.5 substrate-harm at tag `d5-v1.1`, commit `817c68d9`, 5 random seeds × 255 customers = 1275 conversations on a four-agent booking workflow (intake → broker → seat assignment + meal assignment), `mistralai/ministral-3-3b` as broker and sub-agents, LM Studio temperature 0, harm metrics H1–H5 logged per call to a tamper-evident audit substrate. **Cross-family replication** on a 20-customer smoke with `ibm/granite-4-h-tiny` (Q8) confirmed the failure profile is robust to model swap within a quality band.

This rating supersedes any reading that interprets v1's measurements as an indictment of A2A-the-specification. They are not. A2A's specification supports `Task`, `TaskStatus`, `Artifact`, structured `Part.data`, and MCP's specification supports `inputSchema`, `outputSchema`, structured tool results, and domain validators. **Used canonically per spec, both protocols would catch most of the failure modes measured here.** The chatty-card variant does not use them canonically. A v2 canonical-A2A+MCP-per-spec rig has been forked from the same apparatus to measure how much of the fault profile survives strict spec discipline; that result is forthcoming and will refine this rating.

---

## 1. System under assessment

**Scope statement:** the chatty-card A2A pattern as deployed for a representative transactional workflow — single user-facing intent (booking a flight seat with dietary meal accommodation) routed across four agents via NL briefings, with one externally-affecting consequential action (the `assign_meal` and `reserve` tool calls that mutate a shared booking ledger).

**Components rated:**

- **CustomerIntake agent** — receives the user's request, produces an NL "understanding" + "brief" for downstream agents
- **Broker agent** — reads agent-card prose; chooses next specialist by LLM-prose decision; composes NL briefings for specialists; injects unfiltered retrieved RAG chunks into briefings
- **SeatAgent specialist** — receives broker briefing; calls `check_availability` and `reserve` tools; returns NL summary of action taken
- **MealAgent specialist** — receives broker briefing; calls `check_meal_availability` and `assign_meal` tools; returns NL summary of action taken

The **shared substrate** between these components is natural-language messaging only. The **shared ledger** (plane booking SQLite database) is consulted by tools but not consulted by the broker for routing decisions; the broker's routing authority lives in its own narrative state.

**Composition topology** (per framework §7.2): **T2 super-additive — open-world chain with NL-coupled interfaces between every consecutive pair**. Invariant 7 (bounded coupling) fails on three of three inter-agent edges. Compound BR diverges with chain length.

**Principal population:** the canonical deployment is `multi_tenant_small` to `public` (consumer-facing booking systems serve the public; internal enterprise booking systems sit at multi-tenant). For BR aggregation we adopt R4 (`multi_tenant_large` / sectoral) as the representative case for a deployed booking system; the rating moves to R5 for public-facing consumer deployments and back to R3 for single-org workflows.

## 2. Pre-rating classifier (framework §4.0)

| Component | Worldview | Evidence (public-observable / measured) |
|---|---|---|
| CustomerIntake | open-world | Free-text user-request narrative consumed and re-rendered as free-text "understanding" / "brief". No controlled vocabulary; no normalisation; no out-of-scope detection. |
| Broker | open-world | Agent-card consultation is NL prose. Routing decision is an LLM completion. Briefings are free-form. RAG injection is unfiltered. The broker is the load-bearing NL coupling node. |
| SeatAgent | open-world (input) / closed-world (tool boundary) | Receives free-text briefing as input. Tool calls themselves are typed (OpenAI tool-calling format) but the *decision* to call any tool, and the *arguments* passed, are LLM-determined from NL input. |
| MealAgent | open-world (input) / closed-world (tool boundary) | Same as SeatAgent. |

**Pre-rating outcome:** any open-world component anywhere in the composition forces BR-4 floor regardless of per-axis aggregation. Three of four components are open-world end-to-end; the remaining two are open-world on input. **Floor: BR-4.** Per-axis aggregation will determine whether the rating sits at BR-4 or above.

## 3. Per-component ratings

The four agents share an architecture and produce a closely-coupled failure profile. Rather than rate each separately and aggregate, we rate the load-bearing **Broker** component (the NL coupling node) and treat the others as inheriting the broker's posture. This compresses the report and reflects the empirical observation that the broker is where the substrate damage concentrates.

### 3.1 Broker (load-bearing component)

**Tuple: A4–R4–C4–V1–K4-R–O1**

| Axis | Tier | Justification |
|---|---|---|
| A | **A4** | Broker delegates consequential action (assigning a meal to a wrong customer is a financial, dietary-safety, and regulatory event) on the basis of its own narrative state, without external authorisation. The 31% broker-fabrication rate on premature-meal events (cousin Q1 attribution, seed 42, n=84) is direct evidence that the broker exercises action authority it does not possess. |
| R | **R4** | Representative case is sectoral / multi-tenant transactional workflow (booking systems, customer-service orchestration, financial onboarding flows). Public-facing consumer deployments would rate R5; single-org pilots would rate R3. |
| C | **C4** | NL peer coupling on every inter-agent edge. The S4 architectural-coupling metric measured at 0.203 ± 0.001 across 5 seeds (architectural fixed-point on the substrate). Adjacent T2 fan-out experiment ([a2a-coupling-findings](https://github.com/kevin-biot/a2a-coupling-findings)) measured S4 = 0.366 between sibling specialists with no direct channel — coupling propagates through implicit vocabulary inheritance. |
| V | **V1** | No canary, no rollback. Faults commit to the booking ledger before detection: 60% of smoke customers had a meal call attempted on a phantom seat (no reserved seat in the ledger at call time); the call commits before any review. |
| K | **K4-R** | Representative worst-case: regulated booking domain (financial services compliance, ADA accessibility, dietary-safety duty-of-care). Lower-consequence verticals (booking a non-regulated consumer service) would rate K3-L. |
| O | **O1** | Drift detection on the NL substrate would need to lead the substrate's own faults. Phase B Sentinel re-analysis ([a2a-coupling-findings](https://github.com/kevin-biot/a2a-coupling-findings)) showed 20 of 23 experiments cross G5 yellow inside the baseline-establishment window — a Nyquist-style physical constraint. Logs exist but tell you about events after they harmed the ledger. |

**Modifiers:**

- **δ_adv = +1**. The pattern is adversary-permissive by construction: any user-influenced narrative (intake), any retrieved RAG chunk (whose customer-id provenance is not enforced), and any agent-card description is operational input to the broker's routing and briefing. Threat model is not formally produced for the pattern, but the substrate's permeability is measured: 35% cross-customer contamination on smoke (other-customer preferences surface in active-customer briefings).
- **τ = deteriorating**. The pattern's failure rate compounds with chain length and population scale. Multiple AIID and OECD-catalogued incidents on chatty-agent deployments evidence the trajectory at industry scale; the framework's §14 quadrant diagnosis places this pattern in the divergent zone.

### 3.2 Inheritance to other components

**CustomerIntake**: A1 (no consequential action on its own), R inherited, C4 (output is NL into the broker substrate), V N/A, K inherited, O1.

**SeatAgent / MealAgent**: A3 to A4 depending on the tool. `reserve` is A3 (mutates a per-customer cell of a multi-tenant ledger). `assign_meal` is A4 because the empirical fault rate shows it can mutate the wrong cell (cross-customer or no-cell-at-all). C4 on input; tool boundary itself is C2.

The system's effective rating is dominated by the broker's tuple and by the open-world classifier's BR-4 floor.

## 4. Aggregation and class

### 4.1 Pre-rating gate
Open-world components present → **BR floor = 4** (framework §4.0).

### 4.2 Per-axis aggregation (framework §5.1)

Reading off the broker tuple A4–R4–C4–V1–K4-R–O1, framework Rule 1 (highest-tier-axis dominance for the BR class):

- A4 → suggests BR-4
- R4 → suggests BR-4
- C4 → suggests BR-4 (and Invariant 7 fails — see §5)
- V1 → no rollback discipline → no demotion
- K4 → BR-4
- O1 → no observability discipline → no demotion + Invariant 7 absent → **promote one class** per Rule 4

**Effective class before composition: BR-5.**

### 4.3 Composition (framework §7.2 + §7.3)

Topology is T2 (NL-coupled chain). Invariant 7 fails at every interface. Rule 6 (insurability composition): if any component fails Invariant 1 or 2, the composed system is unpriceable regardless of the other components' rating. Invariant 1 fails on the broker (see §5); the composition is unpriceable.

**Compound class: BR-5 (Catastrophic / Uninsurable as deployed).**

### 4.4 Cardinal score (framework §5.2 / §5.4)

**The Kalman uncertainty extension is structurally inapplicable to this pattern.** Invariant 1 fails (same input does not produce same observation: routing varies, briefings vary, tool argument distributions vary). Measurement noise R_K cannot be separated from compliance drift Q. σ_B(t) cannot be estimated. The pattern retains an ordinal BR-5 rating but **cannot quantify υ and is structurally unpriceable** — the architectural boundary between insurable and uninsurable made precise (framework §5.4).

This is the same boundary lane2 navigates from the other side: lane2's Invariant 1 holds (DOP determinism), so its σ_B(t) is producible in principle (Kalman Phase 0 → Phase 1 work, lane2 ADR backlog item 1). For chatty-card A2A, σ_B(t) is *structurally* unproducible. The two stacks sit on opposite sides of the priceability boundary.

## 5. Architectural invariant attestation (framework §9)

| Invariant | Status | Evidence |
|---|---|---|
| **I1 Deterministic execution** | **FAILED** | Same seed + same code → same numerics statistically (4.0% ± 0.33% across 5 seeds), but per-customer routing, briefing content, and tool arguments are LLM-stochastic. Identical inputs do not produce identical observations. |
| **I2 Evidence binding** | partial | Audit substrate logs every tool call with validation result, customer-id-for, customer-id-about, and pre/post state. Strong at the tool boundary. **Weak at the inter-agent boundary**: NL briefings are logged but not signed, not bound to a typed contract, not consultable by downstream agents as authoritative state. |
| **I3 Policy snapshot coherence** | not assessed | The pattern as measured does not carry an explicit policy layer; this invariant doesn't apply at the pattern's level of abstraction. Deployers adding policy would need to attest separately. |
| **I4 Bounded blast radius** | **FAILED** | 35% cross-customer contamination on smoke; reservations and meal assignments commit to the ledger when no rollback exists. The blast radius of any single fault touches the wrong customer's cell with measurable probability. |
| **I5 Jurisdictional awareness** | not assessed | Pattern-level abstraction; deployer responsibility. |
| **I6 Fail-closed execution control** | **FAILED** | `assign_meal` is callable when the workflow ledger has no `seat_id` for the customer (60% of smoke). The tool boundary does not refuse on unmet precondition; the broker does not refuse to route. The pattern fails open. |
| **I7 Bounded coupling** | **FAILED** | NL on every inter-agent edge. T2 super-additive composition mathematics apply. Adjacent T2 fan-out experiment showed S4 = 0.366 between agents with no direct channel — coupling propagates structurally, not just observably. |

**Five of seven invariants fail or are inapplicable; two fail definitively (I1, I7) and these are the gatekeepers for insurability and for closed-world status. The pattern is structurally outside the insurable region.**

## 6. Anti-pattern attestation

The chatty-card A2A pattern exhibits the following entries from the [`governance-failure-patterns` catalogue](https://github.com/kevin-biot/governance-failure-patterns):

| Anti-pattern | Status | Demotion path within pattern? |
|---|---|---|
| `AP006` Natural-Language Peer Coupling | **exhibited_no_demotion_path** | The pattern's defining property; demoting requires changing the architecture |
| `AP010` Capability Discovery as Attack Surface | exhibited_with_demotion_path | A static state-machine over typed capabilities (canonical A2A) demotes this; available in v2 |
| `AP012` MCP Direct-to-LLM Tool Coupling | exhibited_with_demotion_path | Domain gates at the MCP boundary (canonical MCP) demote this; available in v2 |
| `AP018` Closed-World Tool Schema Example Anchoring | exhibited_with_demotion_path | Abstract format descriptions or runtime-generated examples demote; surfaced and partially demonstrated by the schema-fix smoke |

`AP006` is the structural one. The pattern cannot be demoted without ceasing to be the pattern. `AP010` and `AP012` have demotion paths that the canonical-spec variant (v2 forthcoming) is designed to exercise. `AP018` is new to the catalogue and was discovered by this experiment's apparatus-discipline pass.

The companion case study in [`governance-failure-patterns/case-studies/chatty-card-a2a-substrate-harm/`](https://github.com/kevin-biot/governance-failure-patterns/tree/main/case-studies/chatty-card-a2a-substrate-harm) covers the per-event empirical signatures of these anti-patterns at greater detail.

## 7. Empirical evidence summary

| Measurement | Value | Source |
|---|---|---|
| Full success rate (5 seeds × 255 customers) | 4.0% ± 0.33% | `data/full_arm_a/{42,137,271,314,1729}/audit.sqlite` at tag d5-v1.1 |
| Premature-meal events on smoke | 12 / 20 (60%) | RT-1.5 smoke baseline |
| Cross-customer contamination on smoke | 35% | H2 metric, schema-fix smoke |
| Ground-truth violation rate (where measurable) | 50% | H4 metric, schema-fix smoke |
| Schema-anchor concentration (`'14A'`) | 19 / 22 reserve attempts | Granite + Mistral baseline smokes |
| S4 architectural-coupling metric | 0.203 ± 0.001 | Sentinel post-hoc, 5 seeds |
| Token ceiling on survivor-narrative length | ~6144 chars / ~1536 tokens | Cousin token-ceiling analysis, seed 42 |
| Active-predator survival rate | 0% (P1, P2, P3, P4, P5, P6, P7, P9) | Q3 survivor analysis |
| Passive-predator survival rate | 17% (P8, P10) | Q3 survivor analysis |

Cross-family replication: IBM Granite 4 7B Q8 produced 19/22 reserve attempts on seat 14A on the same 20-customer prefix, confirming model-invariance of the failure profile.

## 8. Threat model summary (δ_adv basis)

The pattern is **adversary-permissive** by construction. A short threat-model checklist:

- **Customer-side narrative injection**: any customer-supplied free text becomes operational context for downstream routing and briefing. No normalisation; no controlled vocabulary; no out-of-scope detection. Empirical: 35% cross-customer contamination demonstrates the substrate's permeability without any deliberate adversary.
- **RAG poisoning**: retrieved chunks are injected unfiltered into broker briefings. A poisoned preference-store entry becomes operational input to the next conversation that retrieves it. The pattern as measured already shows passive contamination at 35%; an active adversary would amplify this.
- **Schema-anchor exploitation**: an attacker who can influence tool-schema descriptions (supply chain, MCP-server side) can drive downstream argument distributions toward chosen values. AP018 evidence: 86% concentration on a single seat from one schema example.
- **Capability-discovery enumeration**: agent cards are world-readable in the typical chatty-card deployment; capability enumeration is a default first step for anyone attacking the architecture. AP010.

The pattern's δ_adv = +1 reflects that these surfaces are present and the substrate cannot defend them structurally. A specific deployment may add compensating controls (rate limits, narrative input filtering, RAG provenance enforcement) and reduce δ_adv at the deployment level; the pattern itself does not.

## 9. Gaps surfaced by this assessment

| # | Gap | Owner of remediation | Maps to ADR-backlog item |
|---|---|---|---|
| 1 | The pattern fails Invariant 1 structurally; σ_B(t) is unproducible. | Anyone deploying this pattern who needs an actuarially priceable risk profile. | Backlog #1: move to canonical A2A+MCP per spec. |
| 2 | Invariant 6 (fail-closed) is not enforceable at the LLM tool boundary in this pattern. | Tool-schema designer, MCP-server designer. | Backlog #2: add domain-gate refusal at the MCP `outputSchema` and at the broker. |
| 3 | Invariant 7 (bounded coupling) fails on every inter-agent edge. | Architecture choice; the pattern itself. | Backlog #3: replace NL briefings with typed `Task` / `Artifact` / `Part.data`. Substrate replacement (canonical A2A, then DOP/AARP, in falsification order). |
| 4 | AP018 schema-anchor effect is undetected by typical apparatus reviews. | Tool-schema designer, BRF rating reviewer. | Backlog #4: include schema-text review in BR rating; add to GFP `evidence/notes/`. |

The four backlog items above are detailed in [`chatty-card-a2a-adr-backlog.md`](./chatty-card-a2a-adr-backlog.md).

## 10. Re-attestation conditions

This pattern rating expires when any of:

- the canonical A2A+MCP-per-spec variant (v2 D.5) is measured and the result requires re-rating
- the typed-intent / DOP-AARP variant (v3 D.5, conditional on v2 residuals) is measured and the result requires re-rating
- a vendor implementation publishes a self-attestation following this template that diverges from the pattern-level assumptions (e.g., a vendor stack that ships canonical-spec discipline by default)
- AIID, OECD, or specialist-underwriter records report a chatty-card-A2A incident profile that diverges from this case's measurements

Until then, the rating stands at **BR-5 (Catastrophic / Uninsurable as deployed pattern)**.

---

*This rating is offered as a public service by the Blast Radius Framework authors. It does not name any specific vendor product. Vendors deploying canonical A2A+MCP per spec are explicitly out of scope for this rating; vendors deploying the chatty-card variant are within scope and inherit the rating until they self-attest otherwise.*
