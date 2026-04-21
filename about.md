# About Lane2 and this repository

*A living statement. Updates when the business changes.*

**Last updated:** 2026-04-21
**Version:** 0.3
**Homepage:** [lane2.ai](https://lane2.ai)

---

## 1. Who we are

Lane2 is a small AI infrastructure startup, currently pre-launch. We build governance, safety, and evidence primitives that let other teams deploy AI applications into regulated verticals — legal review, clinical assessment, financial operations, digital-identity and wallet conformance, and adjacent domains where the cost of an unbounded action is measured in fines, harm, or loss of trust.

We are deliberately product-as-infrastructure. We do not build vertical agents, we do not compete for clinical-AI or legal-AI market share, and we do not operate the deployed systems our customers ship. The verticals own their domain expertise; what they lack is production-grade governance infrastructure that can satisfy a regulator, a specialist underwriter, or a post-incident audit. That is what we sell.

This positioning is not neutrality. It is a bet that the governance layer is a distinct category of infrastructure — the way cloud control planes became distinct from compute, identity became distinct from applications, and financial risk frameworks became distinct from trading desks. Agentic AI is in the same arc. Lane2 is a player in the governance-layer category.

## 2. What this repository is

The [Blast Radius Framework](./framework.md) is one of four open artefacts Lane2 publishes as part of a deliberate dual-mode strategy: **open the shapes that should be standards, keep the integrated product that makes them deployable**. The other open artefacts are the narrow ontology ([obo-standard](https://github.com/kevin-biot/obo-standard)), PACT pack patterns ([pact-public](https://github.com/kevin-biot/pact-public)), and European cloud substrate work ([Euro-Cloud-Substrate](https://github.com/kevin-biot/Euro-Cloud-Substrate)). See §4 for the full map.

The framework specifically contains the distilled *shapes* of what we learned building production-grade AI governance infrastructure. Six axes, three modifiers, seven invariants, four composition topologies, a cardinal score, a vendor questionnaire, a machine-readable conformance spec. These are not trade secrets. The code that implements them is; the shapes are not.

We are releasing these shapes under **CC-BY-4.0** because a classification framework that cannot be freely adopted, redistributed, and built upon is not a standard. It is a product. We want this to be a standard. Others — competitors, complementors, standards bodies, regulators, specialist underwriters — are invited to adopt, critique, and extend.

The repository does not include working code (yet). The `spec/` directory includes a JSON Schema, per-invariant test specifications, and worked example profiles — enough for someone to implement against. Reference implementations, when they arrive, will arrive in separate repositories with appropriate licensing.

## 3. Why a target, not a manual

The framework is deliberately sharp-edged. A deployer who applies §4.0 (worldview classifier) plus §9 (seven invariants) plus the anti-pattern catalogue to their current agentic stack may find the stack comes out rated BR-4 or BR-5 — or unrateable by construction. That is the framework doing its job.

If the framework reads as "you have been building bad architecture", the honest question is whether it is right. Often it is. Most agentic-AI stacks shipping in production today satisfy one or two of the seven invariants and leave the others as documentary claims. Most use at least three of the fifteen architectural anti-patterns. Most cannot supply the evidence that a specialist underwriter needs to price the deployment, which means they are commercially uninsurable in the sectors their go-to-market narrative is aimed at.

Better to discover this at redesign time, when the cost is architectural rework, than to discover it via an incident, a regulator letter, a Verisk 2026-style commercial insurance exclusion, or an EU AI Act Article 26 authority request that the system cannot answer. The framework is offered in that spirit: a mirror held up honestly, not a sales pitch with decorative criticism attached.

## 4. What is open, what is private, what is available

Lane2 operates a dual-mode strategy: **open the shapes that should be standards, keep the integrated product that makes them deployable**. Both sides are available for engagement — the open work for free adoption under CC-BY-4.0, the commercial product for pre-launch validation PoC engagements.

### 4.1 Open — public repositories under CC-BY-4.0

The four open repositories are not a single project split into pieces. They are four *distinct* contributions, each solving a different industry gap, each composable with the others.

| Repository | What it is |
|---|---|
| [kevin-biot/blast-radius-framework](https://github.com/kevin-biot/blast-radius-framework) *(this repo)* | **Blast Radius classification framework** — how to rate agentic AI systems for operational impact. Six axes, seven invariants, four composition topologies, machine-readable conformance spec. Answers *"what would we score you if a specialist underwriter asked?"* |
| [kevin-biot/obo-standard](https://github.com/kevin-biot/obo-standard) | **OBO (On Behalf Of) minimum evidence standard** for agentic transactions crossing organisational and jurisdictional boundaries *without a shared authorisation server*. DNS-anchored trust (DKIM pattern). Two JSON artefacts: Credential (pre-transaction, "who authorised what scope") + Evidence Envelope (post-transaction, "what actually happened, sealed"). Draft: `draft-obo-agentic-evidence-envelope-01`. Composes with OAuth / WIMSE / SPIFFE / W3C VCs / A2A / AGNTCY — fills the cross-org accountability gap they leave rather than competing with them. Answers *"how does a Ryanair back-office prove in court what a travel-planning agent it never met did on a customer's behalf?"* |
| [kevin-biot/pact-public](https://github.com/kevin-biot/pact-public) | **PACT (Pack-based Agentic Contract for Trust)** specification bundle — the **partial public extraction** of Lane2's internal ontology work. IETF-style draft specifications (pack conformance, authoring/approval workflow, operational ontology profile, certification + trust-mark, open-standard transition, closed-world rationale, open-pack spec, manifesto); public JSON Schemas (pack-descriptor, intent-mappings, entity-patterns, bundle-manifest, promotion-gate-result, convergence-fixtures); conformance fixture tooling; demo verticals (authored by Lane2 as reference implementations). The extraction is deliberately partial — Lane2's internal ontology repo and the operational tooling that runs the authoring/acceptance workflow are private and remain so. Authoring production packs for specific regulated verticals is a deployer concern; Lane2 publishes the spec + schemas + demo verticals + candidate shapes. Answers *"how do we keep agents bounded to a declared intent scope when regulators ask?"* |
| [kevin-biot/Euro-Cloud-Substrate](https://github.com/kevin-biot/Euro-Cloud-Substrate) | **Euro Cloud Substrate (ECS)** — portable, governable, European cloud substrate specification. Minimal shared contracts European providers can implement to export verifier-friendly evidence. Evidence profiles, golden bundles, reference adapters (k8s-admission, ML-inference-sidecar, object-storage-proxy), RFP guide, pilot pack. Its position: *"if you cannot export verifier-friendly evidence, you do not have sovereignty — you have hosting."* Answers *"what is the minimum contract that makes EU-jurisdiction AI deployment substrate actually sovereign, not cosmetically sovereign?"* |

**How the four compose.** The framework here (blast-radius) is the rating surface. OBO is the cross-organisational accountability layer agents carry when they cross trust boundaries. PACT is the closed-world intent scope each agent operates inside. ECS is the jurisdiction-aware substrate underneath. A deployer can adopt any subset — the dependency graph is explicit but loose.

**On OBO and aARP.** OBO and Lane2's aARP (§4.2) are not competitors; they solve adjacent problems. **OBO** is for free-roaming agents crossing organisational boundaries with no shared authorisation server — DNS-anchored evidence that any counterparty can verify offline. **aARP** is for intent discovery and routing *within* Lane2-governed deployments — scoped capability requests across domains with provable lawful-route validation. Lane2 can use and does compose with OBO (it is an open standard we contribute to); we prefer aARP as the ground-truth mechanism for agents to find and pass intent because it gives the integrator typed-protocol guarantees that OBO's envelope-form does not. Put differently: OBO is the evidence a free-roaming agent leaves behind; aARP is the typed channel a governed agent routes through. Both are valid; which one to use depends on whether the integrator can define the intent space structurally or must accept arbitrary agents arriving from outside.

Use all four freely. No contact required. Cite per the README citation block of the relevant repo.

### 4.2 Private — Lane2 commercial IP, available for pre-launch PoC validation engagements

The integrated Lane2 platform binds the open shapes into a deployable product. Five components plus a formal ontology:

- **DOP (Deterministic Orchestration Pipeline)** — the foundation for reproducible AI operations. Every process runs under deterministic control, producing identical outcomes for identical inputs, backed by cryptographic evidence contracts and fail-closed quality gates. The reference implementation from which the framework's architectural primitives — action-class taxonomy, ontology-as-firewall composition, Kalman-based compliance state estimation, Expected Compliance Risk formalism — are generalised.

- **aARP (Autonomous Agent Routing Protocol)** — extends deterministic orchestration across domains and jurisdictions. Scoped time-amount tokens and inter-jurisdictional matrix routing let autonomous systems collaborate securely with provable lawful-route validation. The framework references aARP-style routing as the canonical pattern for bounded coupling (Invariant 7) and Composition class T1 sub-additive chains (§7.2).

- **SAPP (Secure Agent Payment Protocol)** — the compliant financial layer. Enables automated, cross-organisational payments with cryptographically verified regulatory adherence and dynamic, threshold-based liability allocation. The framework references SAPP's evidence-anchoring layer specifically — externally-anchored Merkle-proof commitments with independent signing keys — as the reference design for Invariant 2 (evidence binding) and §15 (compositional enforcement).

- **CaaS (Context-as-a-Service)** — the real-time contextual intelligence substrate. Operates at telecom and IoT edges, transforming raw sensor and network data into cryptographically signed context evidence powering lawful orchestration, routing, and compliance. Relevant to framework axes O (observability) and R (reach) in edge-deployed scenarios.

- **RTGF (Reference Token Generation Framework)** — integrates DOP / aARP / SAPP / CaaS into a unified policy-driven fabric, synchronising evidence, routing, compliance, and context in real time. The operating layer for AI, automation, and payments that is *lawful by design*.

- **Shared Ontology** — the formal semantic model binding all of the above. Standardised capability verbs, evidence classes, policy concepts (jurisdiction / consent / regulatory boundaries as machine-readable rules), inter-domain links (DOP / aARP / SAPP / CaaS). The full internal ontology repository is private to Lane2; a partial public extraction ships in [pact-public](https://github.com/kevin-biot/pact-public) as the PACT specification surface. DOP loads from the internal ontology in the MVP.

- **Internal acceptance workflow + authoring tools** — Lane2 operates a phased acceptance workflow for ontology-pack promotion (the *specification* of which is published in the pact-public drafts; the *operational tooling* is private and will remain private). Candidate pack shapes and authoring tools are made available to commercial engagement customers; they are not open-source artefacts.

- **PACT demo packs** — beyond the reference verticals in pact-public (public), Lane2 maintains additional demo packs internally for domains where public extraction has not yet been prepared. Production packs for deployer-specific regulated verticals are authored by the deployer (sometimes with Lane2 commercial support) using pact-public schemas as the shape contract; Lane2 does not author customer production packs.

### 4.3 You do not need our products to use the framework

The framework is deliberately tool-agnostic. Any conformant implementation of the patterns described is acceptable; Lane2's components are one set of implementations, not the only ones possible. A deployer can:

- Adopt the framework and build a conformant implementation themselves (the spec in `/spec/` is enough to do this)
- Adopt the framework and compose with third-party vendors that claim conformance
- Engage Lane2 for a PoC of DOP / aARP / SAPP / CaaS / RTGF against a specific deployment context

All three paths are explicitly supported.

### 4.4 Pre-launch engagement

We are pre-launch as of this writing. Commercial terms are being defined; in the meantime, **all our work is available for validation PoC engagements**, including:

- Architecture review of a customer system against the framework
- Deployer-level conformance assessment producing a signed BR attestation
- Proof-of-concept deployments of DOP, aARP, SAPP, CaaS, or RTGF in a customer environment
- Joint calibration with vertical-agent teams or specialist underwriters on weight vectors, evidence-tier-to-R_K calibration, or domain-specific actuarial priors
- Standards-body engagement on the open artefacts (framework, ontology, substrate)

Contact via [lane2.ai](https://lane2.ai).

## 5. Historical genesis — why we rejected direct-LLM-tool coupling

Roughly a year before Jason Gagne's Sentinel corpus was published, we reviewed the emerging agentic-AI integration patterns and made a specific architectural rejection. The patterns we declined to adopt:

- **Agent-to-agent natural-language coupling** as a composition primitive (the pattern that later appeared in A2A, CrewAI defaults, AutoGen defaults, LangGraph defaults)
- **Direct LLM-tool coupling** as the integration substrate — i.e. making every enterprise API tool-callable and letting the LLM choose freely. MCP-the-protocol is neutral; the MCP-ecosystem-as-integration-default was the specific pattern we rejected, along with the adjacent pattern of function-calling-as-primary-control-surface.
- **Persona prompts as a security boundary** — "you are a helpful assistant that never does X"

The patterns we adopted instead:

- **Narrow closed-world agents** with declared scope enforced structurally
- **Capability-routing via a broker** — peers exchange typed capability requests, not natural language. This pattern is the product we call aARP (Autonomous Agent Routing Protocol, §4.2).
- **Phrase normalisation plus ontology firewall** as the trust substrate — unresolved inputs are rejected, not generatively interpreted
- **Action-class taxonomy** with the prohibited class structurally unreachable rather than policy-forbidden

The rejection was *a priori*, on control-theory grounds: natural-language-coupled multi-agent substrates have unbounded input gain and cannot satisfy the composition bounds required for input-to-state stability. We could not prove at that point that the rejected patterns would fail under load; we could show that the chosen patterns were bounded and that the rejected patterns were not. That asymmetry was sufficient to commit.

A year later, Gagne's Sentinel empirical work made the failure mode of the rejected patterns measurable: vocabulary collapse 23–43%, sentiment collapse 12–60%, probe-message divergence 5–50×, and in-context monitoring itself polluting measurement by a factor of 3–6× in the NL-coupled regime. The framework's Invariant 7 (bounded coupling), the §4.0 worldview classifier, and the T2 super-additive composition class in §7.2 are the generalised form of the rejection the platform made a priori.

This is not a claim that we saw everything. Sentinel measures one specific coupling pattern — conversational NL coupling between peers. Other patterns that the framework warns against (shared-weights latent coupling, ontology-vocabulary attractors, emergent asymmetries in typed protocols under load) remain untested empirically. The framework is honest about that. So are we.

## 6. How to engage

Three tiers, in increasing intensity:

1. **Use the framework.** Free, CC-BY-4.0, no contact needed. Cite per the citation block in the README.
2. **Contribute.** File an issue on GitHub for corrections, extensions, missing anti-patterns, empirical counter-evidence, or new examples. Contributors are credited per `ACKNOWLEDGEMENTS.md`.
3. **Validate with a PoC.** Architecture review, conformance assessment against the framework, PoC deployment of DOP or SAPP, or joint calibration work on weights / R-values / actuarial priors. All of this is available during pre-launch. Contact via [lane2.ai](https://lane2.ai).

---

## Change log for this statement

- **v0.3, 2026-04-21** — Corrected the descriptions of the four open repositories. v0.2 described obo-standard as "narrow ontology as open standard" and pact-public as "PACT pack reference implementations"; both were wrong. Correct: obo-standard is the OBO (On Behalf Of) minimum evidence standard for cross-organisational agentic transactions without shared authorisation servers, DNS-anchored and composable with OAuth/WIMSE/SPIFFE/W3C VCs/A2A/AGNTCY; pact-public is the PACT specification bundle — governance invariants, pack conformance, authoring workflow, certification/trust-mark — with closed-world bounded-intent packs as the alternative to classical open-world ontologies at runtime; Euro-Cloud-Substrate (ECS) is a sovereignty specification: minimum contracts for EU cloud providers to export verifier-friendly evidence. Added a paragraph clarifying how the four open repos compose, and a paragraph on the OBO↔aARP relationship (OBO for free-roaming cross-org agents, aARP for typed-protocol intent routing within Lane2-governed deployments; they compose rather than compete).
- **v0.2, 2026-04-21** — Expanded §4 to cover the full Lane2 product suite (DOP, aARP, SAPP, CaaS, RTGF, Shared Ontology) with correct public expansions per the founder's canonical product descriptions: DOP = Deterministic Orchestration Pipeline, aARP = Autonomous Agent Routing Protocol, SAPP = Secure Agent Payment Protocol. Added §4.1 open-repository listing (blast-radius-framework, obo-standard, pact-public, Euro-Cloud-Substrate). Reframed as "knowledge sharing while competing commercially as an infra startup". Prior v0.1 referred to SAPP as "Settlement Anchor Protocol Platform" (an internal working name); the public-facing product is SAPP = Secure Agent Payment Protocol, and the framework references specifically its evidence-anchoring layer.
- **v0.1, 2026-04-21** — Initial positioning. Pre-launch. DOP and SAPP named as private IP available for PoC engagement. Historical genesis of the integration-pattern rejection documented.

This document is a *living statement* and will be updated as Lane2's commercial terms, product offerings, and position in the market evolve. Consult the current `README.md` for commercial terms in force at the time you are reading.
