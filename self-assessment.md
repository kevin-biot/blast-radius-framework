# Lane2 Self-Assessment against the Blast Radius Framework

*Eating our own sauce. Honest rating of the integrated Lane2 stack at the public-observable level.*

**Date of assessment:** 2026-04-21
**Framework version:** v0.5.1
**Template version:** 1.0
**Machine-readable profile:** [`self-assessment.json`](./self-assessment.json) (conformant to `spec/br-profile.schema.json`)
**Assessor:** Lane2 (self-attestation)
**Accountable executive:** Kevin Brown, Founder, Lane2

**Companion documents:**
- [`self-assessment-exec-summary.md`](./self-assessment-exec-summary.md) — Tier 1 executive summary
- [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md) — Tier 3 ADR remediation backlog

---

## 0. Honesty posture

This is a self-assessment at the **public-observable level**, using only information already disclosed in public repositories, public drafts, and the LinkedIn-level product descriptions. Some invariants are enforced more strongly at the internal-instrumented level than this document can attest to; where that is the case, the attestation records the weaker public-observable claim and flags the stronger internal-instrumented claim as private.

A self-assessment that came out perfectly clean would indicate the assessment was not applied honestly. This assessment surfaces **four named gaps** (§9) which seed the ADR backlog in [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md).

IP boundaries are per [`SCOPE.md` §3](./SCOPE.md). Where a public attestation would require disclosing an out-of-scope item (specific code paths, cryptographic parameters, customer names, internal ADR numbers, Kalman R_K calibration values, adversarial threat-model details beyond framework §15), the attestation records the enforcement mode and status at the granularity the public evidence supports, and notes that stronger internal evidence exists.

Where this self-assessment and the framework text disagree, the framework text is authoritative. Where this self-assessment and the machine-readable profile `self-assessment.json` disagree, the JSON is authoritative (the narrative here is a readable gloss on the profile).

---

## 1. System under assessment

**Scope statement:** the integrated Lane2 governance platform as deployed for a canonical **regulated operational workflow** in a high-consequence vertical — representative of the Consolidation Zone (framework §14) target market. The specific reference deployment is a PACT-pack-based regulated-review workflow with cross-organisational evidence anchoring, typical of the legal-citation-review, wallet-conformance, or clinical-triage archetypes.

**Components rated:**

- **DOP** (Deterministic Orchestration Pipeline) — the execution substrate. Runs the pipeline: intake → phrase normalisation → NFM mapping → template selection → rubric evaluation → tool execution → evidence sealing.
- **aARP** (Autonomous Agent Routing Protocol) — cross-domain capability routing. Where the workflow requires capability the local DOP instance does not hold, aARP routes the request to a peer with provable lawful-route validation.
- **SAPP evidence-anchoring layer** (Secure Agent Payment Protocol — evidence subsystem) — externally-anchored Merkle-proof commitments of the evidence produced by DOP and aARP.
- **PACT pack** (Pack-based Agentic Contract for Trust, domain pack) — the closed-world ontology slice that bounds what concepts can exist in this deployment. In public form for some verticals ([pact-public](https://github.com/kevin-biot/pact-public)); private for others.

**Components referenced but not per-component rated in this reference deployment:**

- **CaaS** (Context-as-a-Service) — deployed only for edge telecom / IoT contexts; not present in the canonical regulated-review workflow.
- **RTGF** (Reference Token Generation Framework) — the integration fabric; rated implicitly through the composition topology rather than as its own tuple.
- **Shared Ontology** — the formal semantic model underlying PACT packs; rated via the PACT pack component.

**Composition topology** (per framework §7.2): **T1 sub-additive** — closed-world narrow fail-closed chain. Inter-component interfaces are typed (aARP capability requests, PACT pack ontology references, SAPP evidence submissions). No NL peer coupling.

**Principal population:** `single_org` to `multi_tenant_small` depending on deployer; representative count 10²–10⁴ principals per deployment.

## 2. Pre-rating classifier (framework §4.0)

| Component | Worldview | Evidence (public-observable) |
|---|---|---|
| DOP | closed-world | Inputs normalised to PACT pack's controlled vocabulary before reaching agent context; unresolved inputs route to clarification (not generative interpretation). Scope declared structurally per domain. |
| aARP | closed-world | Typed capability requests between peers; no NL between agents. Scope bounded by capability grants in the routing broker. |
| SAPP evidence layer | closed-world | Evidence submissions are structured per the envelope schema; no NL interpretation. |
| PACT pack | closed-world | The point of the pack: signed, time-bounded ontology slice; only concepts declared in the pack can exist. |

All components closed-world. Pre-rating gate does not force BR-4 floor.

## 3. Per-component ratings

### 3.1 DOP

**Tuple: A3–R3–C2–V2–K4-R–O3**

| Axis | Tier | Justification |
|---|---|---|
| A | **A3** | Bounded execution within declared action-class ceiling; Class D structurally unreachable |
| R | **R3** | Within a single deployer organisation: enterprise multi-tenant across the deployer's business units |
| C | **C2** | Agent + tools. No peer agents at this layer (aARP mediates peer interactions) |
| V | **V2** | Canary + rollback scripts for pipeline changes; pipeline itself does not act on external state during execution (that is the tool layer's responsibility, rated per tool) |
| K | **K4-R** | Representative worst-case: regulated sector deployment. For lower-consequence verticals (K3-L legal, K3-F financial), tier is K3-* and aggregation reduces accordingly. |
| O | **O3** | Real-time dual-gaze drift monitoring (inward rubric drift + outward workload drift). O4 claim (architectural invariants checkable at runtime) is supported for some invariants — policy-snapshot hash verification, action-class dispatcher refusal, STA-equivalent verification — but the framework-complete O4 claim (every invariant checkable at runtime) is stronger at the internal-instrumented level than the public evidence supports. Recorded as O3 here. |

**Modifiers:**
- δ_adv = **+1** — threat model public in framework §15 (compositional enforcement via ontology-as-firewall with Bayesian validation). Residual risk named explicitly in the threat model: ontology poisoning, normalisation oracle, LLM hallucination. Mitigations documented; residual risk not zero.
- τ = **stable** — pre-launch; no production drift observed; trajectory review cadence to be formalised per PoC engagement. This is a genuine immaturity, not a defect — a pre-launch system cannot have an operational trajectory record.

### 3.2 aARP

**Tuple: A3–R4–C3–V2–K4-R–O3**

| Axis | Tier | Justification |
|---|---|---|
| A | **A3** | Executes routing — the routing itself is an action with consequence (wrong route = evidence chain breaks) |
| R | **R4** | Cross-organisational, cross-jurisdictional by design; affects third parties |
| C | **C3** | Typed workflow chain — capability requests are structured, not NL |
| V | **V2** | Routing decisions revisable before execution commits; the routed action may be less reversible (its V is rated at the called component) |
| K | **K4-R** | Regulated/systemic at the routing layer: a wrong lawful-route validation has regulatory and contractual consequences |
| O | **O3** | Routing decisions produce evidence; O4 at internal-instrumented level, O3 at public |

**Modifiers:**
- δ_adv = **+1** — routing attack surface (capability enumeration, routing poisoning) analysed; countermeasures structural. Residual risk in inter-jurisdictional matrix under adversarial corridor owners.
- τ = **stable** (pre-launch qualification per DOP above)

### 3.3 SAPP evidence-anchoring layer

**Tuple: A2–R4–C2–V1–K4-R–O4**

| Axis | Tier | Justification |
|---|---|---|
| A | **A2** | The evidence layer drafts commitments; the *actions* committed are performed elsewhere (payment systems, DOP, aARP). From the evidence layer's perspective, its outputs are signed attestations, not executions. |
| R | **R4** | Commitments are externally verifiable, cross-organisational |
| C | **C2** | Evidence service + Merkle proof anchor. No peer agents. |
| V | **V1** | Evidence commitments are append-only and immediate; an incorrect commitment cannot be retracted but can be superseded with a signed correction within minutes |
| K | **K4-R** | The evidence *is* the regulatory artefact for payments, so errors at this layer are K4-R. |
| O | **O4** | Tamper-evident by construction; externally verifiable without contacting Lane2 infrastructure; architectural invariants (Merkle inclusion, signature chain) checkable at runtime by any verifier. SAPP provides a **role-based evidence API surface** (per Lane2's private SAPP specification, demonstrable under PoC): `POST /settlements` (evidence submission), `GET /evidence/{traceId}` (customer-care/consumer view with bundle + confidence + liability + reason codes + proof), `GET /evidence/{traceId}/proof` (three-level Merkle proof: evidence root → partition root → global root), `GET /regulator/verify/{traceId}` (regulator endpoint, privacy-preserving — no consumer DIDs exposed; returns chain_verified + global_root match against QTSP + jurisdiction_overlap), `GET /regulator/integrity` (Ed25519-signed global root verifiable against QTSP public key). Global root published to EU Qualified Archive / QTSP on a 15-minute checkpoint cycle. Regulators can verify full system integrity without accessing any transaction data. |

**Modifiers:**
- δ_adv = **0** — threat model: anchor key compromise (mitigated by key hierarchy + rotation + HSM-class storage per attestation-format.md §2), signature replay (mitigated by envelope nonce + time window), Merkle-root substitution (mitigated by the append-only anchor semantics). Attack surface analysed and closed at the anchor-layer boundary.
- τ = **stable**

### 3.4 PACT pack (reference deployment)

**Tuple: A1–R3–C1–V1–K3-L–O3**

*Note: PACT packs are configuration artefacts, not agents. They do not act; they bound what other components can act on. The "authority" attribution here reflects that a pack can — via its ontology definition — cause downstream components to accept or refuse inputs, which is an A1-equivalent influence on outcomes.*

**Three-layer distinction (clarified in v1.3 — see §11 change log).** PACT has three distinct layers that this self-assessment keeps separate:

1. **PACT specification surface** — in [`kevin-biot/pact-public`](https://github.com/kevin-biot/pact-public). IETF-style drafts (pack conformance, authoring workflow, governance, certification/trust-mark, operational profile), public JSON Schemas (pack descriptor, intent mappings, entity patterns, manifest, promotion gate result), conformance fixture tooling, demo verticals. This is deliberately a **partial public extraction** from Lane2's internal ontology repo.
2. **Internal ontology repo + acceptance tooling** — private to Lane2. Defines Lane2's internal operational ontology; DOP loads from it in the MVP. The phased acceptance workflow *tooling* is never passed into public work (the workflow *specification* is public; the operational tools that run it are private).
3. **Deployer production packs** — authored by deployers against the PACT spec, for their own regulated verticals. Lane2 provides candidate shapes, demo verticals, and (in commercial engagements) authoring tools. Authoring production packs is explicitly a deployer concern; Lane2 does not author customer packs.

In this self-assessment's reference deployment, "the PACT pack" is a deployer-authored production pack consuming the public PACT spec, loaded by DOP from the private internal ontology backing store. The rating above is at the component boundary — the pack as loaded into DOP — rather than rating the public spec artefacts or the internal ontology repo as separate components.

| Axis | Tier | Justification |
|---|---|---|
| A | **A1** | Recommends (via ontology membership) what can and cannot reach templates; no direct execution |
| R | **R3** | Loaded across all components in the deployment |
| C | **C1** | Isolated configuration artefact |
| V | **V1** | Packs are versioned; corrections ship as new versions |
| K | **K3-L** | Bad pack ontology is a legal/contractual problem (wrong scope, wrong authority); at K3-L for a legal review pack, at K4-S for clinical, etc. Representative K3-L here. |
| O | **O3** | Pack loading is logged; pack contents are public for the legal-review reference pack; conformance tests exist (per `pact-public`) |

## 4. Composition

**Topology:** **T1 sub-additive** (closed-world narrow fail-closed chain).

**Component edges:**

| From | To | Interface type | Notes |
|---|---|---|---|
| DOP | PACT pack | typed (pack loading via manifest; ontology queries via structured API) | Pack is a configuration artefact; this is not a peer call |
| DOP | aARP | typed (capability request: scoped time-amount token) | No NL |
| aARP | aARP peer (remote) | typed (routing protocol) | DNS-anchored, per OBO-style verification |
| DOP | SAPP evidence layer | typed (evidence submission schema) | Sealed Merkle commitment returned |
| SAPP | external anchor | typed (Merkle inclusion) | Cryptographic, not linguistic |

**Compound math applying T1:**

- **P(chain failure) ≈ 1 − ∏(1 − Rᵢ)** — union bound; for small per-component failure probability, ≈ Σ Rᵢ
- **BR(compound | failure) ≤ max(BRᵢ)** — the typed boundary stops propagation

Inside the DOP component there is also a **T3 multiplicative defence-in-depth** composition (the 8-layer ontology-as-firewall described in framework §15). T3 applies to *attack resistance* against an IPI adversary, not to failure propagation between components. Both topologies coexist and reinforce each other.

No T2 super-additive substrate anywhere. No T4 voting composition (Lane2's architecture does not rely on LLM ensembles for decision-making; the LLM layer is one input to a deterministic rubric-evaluation pipeline, not a voting participant).

## 5. Invariant attestations

### I1 — Deterministic execution

- **Status:** holds
- **Enforcement mode:** architectural
- **Evidence summary:** DOP is the Deterministic Orchestration Pipeline — reproducibility is a design property. Canonical evidence-contract hashing over full input + policy snapshot + outputs; LLM sampling pinned where used; CI-verifiable re-run reproducibility at the internal-instrumented level.
- **Public test:** re-running the same input against the same PACT pack and the same policy snapshot produces an identical contract hash. This is the product's name-level promise.
- **Caveat:** the public-observable attestation is structural (the design is reproducible); the architectural attestation (every call site verified in code, CI-integrated determinism tests) is at the internal-instrumented level.

### I2 — Evidence binding

- **Status:** holds
- **Enforcement mode:** architectural
- **Evidence summary:** SAPP evidence layer produces externally-anchored Merkle-proof commitments with independent signing keys. Every decision output is bound to a policy snapshot hash + an evidence envelope. Tamper-evident at rest (append-only anchor); tamper-evident in transit (signed envelope). Three-level Merkle proof chain: Evidence root (per-settlement) → Partition root (append-only audit tree, signed every 30s) → Global root (root-of-roots, Ed25519 signed every 60s, published to EU Qualified Archive / QTSP every 15 minutes).
- **Demonstrable in working reference:** the OBO repo's `examples/integrations/a2a/` ships a runnable end-to-end OBO + A2A reference implementation with Ed25519 keys, a live public DNS trust anchor (`_obo-key.lane2.ai IN TXT "v=obo1 ed25519=…"`), and Merkle evidence via an Evidence Anchor stub. Three Docker containers; no pre-shared config; no crypto mocks; seven captured test scenarios. A third-party verifier can `dig _obo-key.lane2.ai` and independently verify the DNS trust anchor without contacting Lane2 infrastructure.
- **Role-based evidence API surface:** SAPP exposes role-scoped verification APIs (per Lane2 private specification, demonstrable under PoC): customer-care and consumer views via `GET /evidence/{traceId}` (bundle + scored confidence + liability allocation + machine-readable reason codes + proof); proof retrieval via `GET /evidence/{traceId}/proof` (three-level Merkle); regulator endpoints `GET /regulator/verify/{traceId}` and `GET /regulator/integrity` (privacy-preserving — no consumer DIDs; returns chain_verified + global_root match against QTSP + jurisdiction_overlap). A regulator can verify full system integrity without accessing any individual transaction data. Extraction of this API specification to a public sibling document is the subject of backlog item 11.
- **EU AI Act mapping:** Art. 12 (automatic logging), Art. 15 (robustness integrity), Art. 19 (retention), Art. 26(6) (authority access) supported architecturally via the role-based API surface; Art. 72/73 (post-market monitoring/incident) supported via the integrity endpoints + machine-readable reason codes.

### I3 — Policy snapshot coherence

- **Status:** holds
- **Enforcement mode:** architectural
- **Evidence summary:** Every evidence record carries `policy_snapshot_id` binding the decision to a specific policy epoch. Policy snapshots are versioned and hash-verified at retrieval. Rubric bindings in PACT packs are version-locked to pack release.
- **Public evidence:** PACT pack conformance drafts include versioning and snapshot semantics; DOP ADRs on policy-snapshot binding are the (private) internal counterpart.

### I4 — Bounded blast radius

- **Status:** holds
- **Enforcement mode:** architectural
- **Evidence summary:** Action-class ceiling enforced at DOP dispatcher (Class D structurally unreachable); tool-ontology binding limits each tool's invocable shape; PACT pack scopes what can reach the dispatcher in the first place.
- **Public evidence:** framework §9 Invariant 4 and §15 compositional enforcement pattern describe the mechanism; DOP ADRs are the internal counterpart.

### I5 — Jurisdictional awareness

- **Status:** holds
- **Enforcement mode:** architectural
- **Evidence summary:** jurisdictional enforcement within Lane2-governed deployments is architectural via the composition of three mechanisms: (1) **aARP** Autonomous Agent Routing Protocol carries inter-jurisdictional matrix routing with provable lawful-route validation; scoped time-amount tokens encode jurisdictional constraints. (2) **RTGF** Reference Token Generation Framework synchronises jurisdictional policy across DOP, aARP, SAPP, CaaS — "lawful by design" is its positioning property, not a marketing phrase. (3) **Shared Ontology** encodes jurisdiction, consent, and regulatory boundaries as machine-readable rules that all Lane2 components consume rather than re-interpret. On top of that stack sits a policy hierarchy with unoverridable regulatory tier, jurisdictional conflict resolution that fails closed and escalates.
- **Composition boundary note:** at the boundary with non-Lane2 counterparties, the general §7.1 composition rule applies (the counterparty's architecture is rated separately; if the counterparty cannot produce an equivalent attestation, the composition must be rated accordingly or declined). This is the same composition rule that applies to every invariant — it is not a gap specific to I5. For the specific sub-case of cross-organisational free-roaming agents that need to cross into counterparty systems without a shared authorisation server, the **OBO open standard** (`kevin-biot/obo-standard`) is a convenience interop pattern available as a deployment option; OBO is not Lane2's core I5 mechanism, and the absence of OBO adoption elsewhere in the industry does not reduce Lane2's own architectural enforcement of I5.

### I6 — Fail-closed execution control

- **Status:** holds
- **Enforcement mode:** architectural
- **Evidence summary:** Dual policy enforcement points with default DENY; action-class taxonomy with Class D structurally prohibited; critical-action fail-closed on evidence-write failure (a commit without a sealed evidence record is structurally impossible). Session-execution attestation blocks tool execution on missing or invalid tokens.
- **Public evidence:** framework §9 Invariant 6 describes the pattern; DOP's action-class dispatcher is the internal counterpart.

### I7 — Bounded coupling

- **Status:** holds
- **Enforcement mode:** architectural
- **Evidence summary:** No agent-to-agent NL coupling anywhere in the composition. aARP routes typed capability requests; PACT pack bounds what concepts can exist; SAPP envelopes are structured. Composition topology is T1 by construction.
- **Demonstrable via composed reference and negative control:** the OBO repo ships *both* a T1 composition (OBO + A2A with typed task payloads — `examples/integrations/a2a/`) *and* a T2 super-additive negative control (`examples/integrations/a2a-multi-hop/` with NL-coupled agent-agent-agent chain feeding LM Studio). The negative control is explicitly labelled "the architecture DOP was designed to reject; here to be measured, not emulated". This pair of references is empirical substrate for the framework's T1-vs-T2 composition-class distinction: DOP-side Sentinel replication on typed topology reads S1=S4=CPL=0 across 300 windows × 5 RNG seeds, vs the NL-coupled substrate as positive measurement.
- **Public evidence:** framework §4.0 worldview classifier, §7.2 T1 definition, §9 Invariant 7. Lane2 about.md §5 historical genesis documents the a priori rejection of NL-coupling as a composition primitive. OBO repo `examples/integrations/a2a/` is the working demonstration; `examples/integrations/a2a-multi-hop/` is the negative control.

## 6. Anti-pattern attestations

**Part A — architectural (15 patterns):**

| ID | Pattern | Status | Notes |
|---|---|---|---|
| A1 | A2A public capability discovery | not_exhibited | aARP is per-principal authenticated; no public AgentCard surface |
| A2 | API-agent-ready / API-first | not_exhibited | Action-class taxonomy with per-tool ceiling; no auto-exposure of write APIs |
| A3 | MCP server ecosystem without composition rule | not_exhibited | MCP not used as integration default; where used externally, composition rule (framework §7.1) applies |
| A4 | Agent marketplaces | not_exhibited | No marketplace distribution |
| A5 | Auto-tool-generation from OpenAPI | not_exhibited | Tool onboarding is explicit per-tool with declared ceiling |
| A6 | CrewAI / AutoGen / LangGraph default (persona + NL) | not_exhibited | No persona prompts as security boundary; no NL peer coupling |
| A7 | LLM-as-judge / recursive evaluation | not_exhibited | Rubric evaluation is deterministic per PACT pack; no LLM-as-judge loops |
| A8 | OAuth-as-agent-identity | not_exhibited | aARP uses scoped time-amount tokens distinct from user OAuth; agent principal is separate from user principal |
| A9 | Ungoverned vector memory | not_exhibited | PACT pack is the primary retrieval surface; no free-form vector store with write-back on interactions |
| A10 | Context stuffing | exhibited_with_demotion_path | Some tool outputs are concatenated to LLM context in the current pipeline design. Demotion path: typed context slots with per-slot trust level (framework antipatterns.md A10 demotion). Partial implementation at public-observable level; full typed-slot architecture is roadmap. |
| A11 | Computer use | not_exhibited | No browser or OS-level agents in the Lane2 suite |
| A12 | Deep research | not_exhibited | Retrieval is scoped to PACT pack corpora, not open web |
| A13 | BYOA into corporate data | not_exhibited | Lane2 does not expose BYOA; customers' own BYOA practices are out of scope for this self-assessment |
| A14 | Autonomy sliders / approval fatigue | exhibited_with_demotion_path | Any system with human approval gates (A2/A3 action classes) is subject to reflexive-approval decay. Demotion path: approval-quality metrics (median review time, diff-of-approved-vs-declined), periodic forced re-approval of standing patterns. Partial at public-observable level. |
| A15 | Prompt-injection-as-feature | exhibited_with_demotion_path | Architecturally demoted at the decision path via five composed mechanisms documented in [`pact-public/docs/architecture/security-unsigned-error-instruction-injection.md`](https://github.com/kevin-biot/pact-public/blob/main/docs/architecture/security-unsigned-error-instruction-injection.md) and [`pact-public/docs/architecture/intent-first-bounded-execution-pattern.md`](https://github.com/kevin-biot/pact-public/blob/main/docs/architecture/intent-first-bounded-execution-pattern.md): (1) tools layer defines its own ontology (tool-ontology binding); (2) tools carry the deployer policy library that bounds what they can return; (3) schema-constrained enum fields (e.g. `pact_deontic: "may" | "must_not"`) replace prose instruction fields; (4) pack-bounded authority — out-of-scope instructions in tool responses trigger escalation, not execution; (5) deny-wins composition + provenance verification (`instance` trace) across multiple tool responses. In the decision path the rubric evaluator is deterministic against ontology-bound tool transitions; no LLM prompt ingests free-form tool output. **Residual surface** is in non-decision rendering/summary paths (human-facing result presentation, review UI) where tool output may traverse LLM-templated summarisation; these paths use schema-constrained rendering templates but are not yet at the same architectural strength as the decision path. Characterisation: exhibited in specific rendering paths; architecturally demoted in the decision path. |

**Part B — evidence-chain (11 patterns):**

| ID | Pattern | Status | Notes |
|---|---|---|---|
| B1 | Application logs as "evidence" | not_exhibited | SAPP evidence layer with external anchor; not mutable at rest |
| B2 | Post-hoc logging vs runtime controls | not_exhibited | DOP enforces at runtime; logs are evidence of the enforcement, not the enforcement itself |
| B3 | Prompt storage without governance | exhibited_with_demotion_path | Retention policy framework exists (Shared Ontology + PACT pack declares retention classes); per-deployment implementation is deployer responsibility, with template policy shipped. Gap: the *template* policy is structural; the *enforced* policy is deployer-configured and Lane2 cannot architecturally guarantee across deployments. |
| B4 | No delegation chain | not_exhibited | aARP tokens carry subject, scope, delegation hash, expiry, tool allowlist |
| B5 | No authentication freshness | exhibited_with_demotion_path | Presence-binding levels defined in the ontology (fresh_live, recent_live, cached_auth, device_unlock_only, none); freshness enforcement depends on the deployer's auth integration. Structural at the pattern level; architectural requires the deployer's auth stack to honour the levels. |
| B6 | Unsigned / self-signed-only evidence | not_exhibited | Independent anchor (SAPP) with its own signing keys |
| B7 | No explainability source mapping | not_exhibited | PROV-O provenance per framework §9 Invariant 3 pattern; explain-statement API surfaces source mapping on demand |
| B8 | Mutable at rest | not_exhibited | Append-only anchor; hash-chain per stage |
| B9 | No replay capability | not_exhibited | Deterministic execution + policy-snapshot binding + sealed evidence = replay is constructive |
| B10 | No retention / authority-export | exhibited_with_demotion_path | Retention policy template shipped; per-deployment enforcement is deployer configuration. Authority-export path defined in the attestation format; first-deployer exercises still outstanding. Gap: no exercised authority-export drill at the Lane2 stack level yet (pre-launch). |
| B11 | Critical-action fail-open | not_exhibited | Fail-closed on evidence-write failure; fail-closed on STA-verify failure; fail-closed on anchor-write failure for Class B/C actions |

## 7. Aggregation

**Base class** (max over axes across components): **BR-4** (driven by K4-R in DOP, aARP, SAPP).

**Interaction overrides (per §5.1):**

| Rule | Triggered? | Effect |
|---|---|---|
| 1 — C4a/b + V≥3 | No | No C4a/b present; N/A |
| 2 — A≥3 + K4 | **Yes** | Sets minimum BR-4. Already at BR-4, no uplift. |
| 3 — R4 + O≤1 | No | R4 present (aARP, SAPP) but O is O3/O4, not O≤1 |
| 4 — Invariant 7 absent (partial) | No | I7 holds architecturally |
| Pre-rating open-world | No | All components closed-world |
| O0/O1 on BR-3+ | No | O is O3/O4 |
| O4 demotion (requires V≤2 + all invariants hold) | **Partial** | Only SAPP component has O4; V across components is V1/V2; Invariant 5 only partially holds, blocking the demotion eligibility. **Demotion not granted.** |

**Final ordinal class: BR-4.**

**BR-4 is the architecturally minimum-achievable class for this consequence domain.** The §5.1 O4 demotion rule requires V ≤ 2 across all components and all §9 invariants holding. Max V across components = V2 (V1 for SAPP evidence and PACT pack, V2 for DOP and aARP — the ≤ 2 requirement is met at the component max). Invariants 1–7 all hold (per §5). If the composed-system O rating were uniformly O4 (it is at SAPP; DOP/aARP components seal to SAPP for external verifiability), the demotion rule would be eligible to fire. **But Rule 2 (A ≥ 3 + K4 → minimum BR-4) is a floor, not a cap**: the floor cannot be demoted below. For this K4-R consequence domain with A3 execution authority, BR-4 is therefore the minimum achievable class — moving to BR-3 would require entering a lower-consequence domain, not improving the architecture.

**Cardinal score:** Kalman extension implementation is Phase 0 (theoretical) in the Lane2 reference implementation at public-observable level; Phase 1 (scalar Kalman on a single deployer metric) is under way internally. **Cardinal score is not produced in this self-assessment** — σ_B(t) is a theoretical construct until Phase 1 lands. This is a named gap (§9 Gap-1).

Point-estimate reference computation (illustrative, without Kalman filtering):

With weights representative for a regulated operational workflow — `w = [w_a=0.15, w_r=0.15, w_c=0.15, w_v=0.10, w_k=0.25, w_o=0.20]` — and axis tiers normalised to [0, 1], the point cardinal B(t) ≈ 0.62 (illustrative only; weight calibration is framework v0.6 open question #1, not canonical).

## 8. Residual vs inherent

- **Inherent BR** (absent mitigating controls): **BR-5** — K4-R consequence domain alone drives inherent exposure to BR-5 before any architectural control is applied. This is the "without the architecture, what would this system be?" baseline.
- **Residual BR** (with Lane2 architectural controls operating): **BR-4** — the architecture compresses the inherent BR-5 back to BR-4 by making Invariants 1, 2, 3, 4, 6, 7 architectural and Invariant 5 structural.
- **Gap-closing controls between inherent BR-5 and residual BR-4:**
  - Closed-world worldview across all components (§4.0 — pre-rating gate held)
  - T1 sub-additive composition (§7.2 — failures bounded to max per-component BR)
  - Action-class taxonomy with Class D structurally unreachable (I4, I6)
  - Externally-anchored Merkle-proof evidence with independent signing keys (I2)
  - Policy-snapshot binding (I3)
  - Deterministic execution enabling replay (I1)

## 9. Gaps surfaced by this assessment

Three named gaps. Each seeds an ADR candidate in [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md).

*v1.1 correction note: an earlier v1.0 of this assessment (published same day) listed four gaps including a "Gap-1: cross-border I5 structural" item. On review, that item conflated Lane2's own architectural jurisdictional enforcement (which holds, via aARP + RTGF + Shared Ontology) with the general §7.1 composition-rule observation that a counterparty's own architecture is rated separately. The general composition-rule observation applies to every invariant, not specifically to I5, and is not a Lane2-specific gap. Gap-1 has been removed; gap numbering has been re-sequenced so remaining gaps are now Gap-1 (Kalman), Gap-2 (τ), Gap-3 (principal-population).*

### Gap-1 — Kalman extension (σ_B(t)) is theoretical

Framework §5.4 v0.5 Kalman extension is specified; implementation in the Lane2 reference stack is Phase 0 (not yet scalar Phase 1 on a deployer metric). σ_B(t) cannot be produced for this self-assessment. The consequence: cardinal score is not computed; actuarial υ variable is not numerically expressible; specialist underwriters will price with a conservative default where σ_B would otherwise give them a tighter figure. Remediation: implement Phase 1 scalar Kalman on a selected deployer metric (the obvious candidate is the compliance-decision ratio in a pilot deployment).

### Gap-2 — Trajectory review cadence is nominal (pre-launch)

The τ modifier is recorded as `stable` for every component, but the evidence is "no production drift observed" in a pre-launch system. A genuine stable classification requires an operational trajectory record. Remediation: formalise τ cadence per PoC engagement; after first PoC completion, re-run the assessment with actual trajectory evidence.

### Gap-3 — Principal-population accounting is not explicitly tracked

Framework §4.2 R-axis sub-component (population exposure: how many principals a single action can affect) is not instrumented as a first-class field in the current Lane2 pipeline evidence schema. The `self-assessment.json` profile has `system.principal_population` populated at the system level; per-action population exposure is not enumerable. Remediation: add principal-population count to each evidence record where the action has a non-empty principal set, so aggregation over a session can surface per-session population exposure.

Three Part A anti-patterns (A10 context stuffing, A14 autonomy-slider fatigue, A15 prompt-injection-as-feature) are listed as `exhibited_with_demotion_path` — all three have demotion paths in progress but not fully implemented at the public-observable level. These are architectural-maturity items rather than design flaws; the demotion paths are real and the framework allows them to be exhibited with a declared path.

Two Part B anti-patterns (B3 prompt storage governance, B5 authentication freshness, B10 retention/authority-export) are `exhibited_with_demotion_path` for the same reason — the patterns are at structural enforcement level at the Lane2 stack, and architectural enforcement requires deployer-side integration or further implementation.

## 10. Evidence references

- Machine-readable profile: [`self-assessment.json`](./self-assessment.json)
- Framework version: [`framework.md v0.5.1`](./framework.md) (commit `d80db51`)
- Lane2 positioning: [`about.md v0.3`](./about.md)
- Public product descriptions: Kevin Brown, LinkedIn (as of 2026-04-21)
- Open Lane2 repositories: [kevin-biot/pact-public](https://github.com/kevin-biot/pact-public), [kevin-biot/obo-standard](https://github.com/kevin-biot/obo-standard), [kevin-biot/Euro-Cloud-Substrate](https://github.com/kevin-biot/Euro-Cloud-Substrate)
- Working reference implementation: [obo-standard/examples/integrations/a2a/](https://github.com/kevin-biot/obo-standard/tree/main/examples/integrations/a2a) (OBO + A2A composed, runnable end-to-end; live DNS trust anchor; Merkle evidence anchor; seven captured test scenarios)
- Negative control for T2 super-additive composition: [obo-standard/examples/integrations/a2a-multi-hop/](https://github.com/kevin-biot/obo-standard/tree/main/examples/integrations/a2a-multi-hop) (deliberately NL-coupled agent-agent-agent chain; feeds DOP-side Sentinel replication at `research/sentinel-a2a/agent-topology-comparison/`)
- This assessment produces **no signed attestation** at publication time. A signed attestation per [`spec/attestation-format.md`](./spec/attestation-format.md) is an ADR candidate in the backlog. (The OBO A2A reference implementation does produce signed evidence envelopes + anchor JWS proofs in its captures; those are demonstrable but are demo-grade, not a production attestation signed by Lane2 as a legal entity.)

## 11. Assessor attestation

The assessor (Lane2, self-attesting via Kevin Brown) attests that the rating above reflects honest application of framework v0.5.1 against the Lane2 stack as publicly disclosed on 2026-04-21, within the IP and scope boundaries stated in [`SCOPE.md §3`](./SCOPE.md). Stronger internal evidence exists for several invariants; where that is the case, the assessment records the weaker public-observable claim and flags the stronger internal-instrumented claim as private.

Residual uncertainty is not expressed as σ_B(t) because Kalman Phase 1 is not implemented (Gap-1); residual uncertainty is captured qualitatively in §9 gaps and in the `exhibited_with_demotion_path` attestations of §6.

This self-assessment is a **living document** tied to a framework version. When framework v0.6+ ships, or when any of Gap-1 through Gap-3 closes, this assessment is re-run. Self-assessment version: **v1.5** (2026-04-21; strengthens I2 and §3.3 SAPP component by citing the role-based evidence API surface — customer/consumer views via `GET /evidence/{traceId}`, regulator endpoints `GET /regulator/verify/{traceId}` + `GET /regulator/integrity` privacy-preserving and QTSP-verifiable, three-level Merkle proof chain with 15-minute QTSP publication cycle — all per Lane2 private SAPP specification, demonstrable under PoC. Adds §7 demotion-rule analysis: BR-4 is the architecturally minimum-achievable class for this consequence domain because Rule 2 floor prevents demotion below BR-4. Backlog item 11 reframed as SAPP API specification extraction — the APIs exist; extraction to public doc is administrative.). Prior: v1.4 (A15 architectural demotion at decision path), v1.3 (PACT three-layer), v1.2 (OBO A2A references), v1.1 (I5 correction), v1.0 (initial publication in framework v0.5.2).

**Signed** (attestation): Kevin Brown, Founder, Lane2 — 2026-04-21
**Signed** (drafting assessor): Lane2 self-attestation with AI-assisted framework application; sign-off is Kevin Brown's as principal.

---

*End of technical findings. Executive summary at [`self-assessment-exec-summary.md`](./self-assessment-exec-summary.md). Remediation backlog at [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md).*
