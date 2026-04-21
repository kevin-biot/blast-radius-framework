# About Lane2 and this repository

*A living statement. Updates when the business changes.*

**Last updated:** 2026-04-21
**Version:** 0.1
**Homepage:** [lane2.ai](https://lane2.ai)

---

## 1. Who we are

Lane2 is a small AI infrastructure startup, currently pre-launch. We build governance, safety, and evidence primitives that let other teams deploy AI applications into regulated verticals — legal review, clinical assessment, financial operations, digital-identity and wallet conformance, and adjacent domains where the cost of an unbounded action is measured in fines, harm, or loss of trust.

We are deliberately product-as-infrastructure. We do not build vertical agents, we do not compete for clinical-AI or legal-AI market share, and we do not operate the deployed systems our customers ship. The verticals own their domain expertise; what they lack is production-grade governance infrastructure that can satisfy a regulator, a specialist underwriter, or a post-incident audit. That is what we sell.

This positioning is not neutrality. It is a bet that the governance layer is a distinct category of infrastructure — the way cloud control planes became distinct from compute, identity became distinct from applications, and financial risk frameworks became distinct from trading desks. Agentic AI is in the same arc. Lane2 is a player in the governance-layer category.

## 2. What this repository is

The [Blast Radius Framework](./framework.md) is the distilled *shapes* of what we learned building production-grade AI governance infrastructure. Six axes, three modifiers, seven invariants, four composition topologies, a cardinal score, a vendor questionnaire, a machine-readable conformance spec. These are not trade secrets. The code that implements them is; the shapes are not.

We are releasing these shapes under **CC-BY-4.0** because a classification framework that cannot be freely adopted, redistributed, and built upon is not a standard. It is a product. We want this to be a standard. Others — competitors, complementors, standards bodies, regulators, specialist underwriters — are invited to adopt, critique, and extend.

The repository does not include working code (yet). The `spec/` directory includes a JSON Schema, per-invariant test specifications, and worked example profiles — enough for someone to implement against. Reference implementations, when they arrive, will arrive in separate repositories with appropriate licensing.

## 3. Why a target, not a manual

The framework is deliberately sharp-edged. A deployer who applies §4.0 (worldview classifier) plus §9 (seven invariants) plus the anti-pattern catalogue to their current agentic stack may find the stack comes out rated BR-4 or BR-5 — or unrateable by construction. That is the framework doing its job.

If the framework reads as "you have been building bad architecture", the honest question is whether it is right. Often it is. Most agentic-AI stacks shipping in production today satisfy one or two of the seven invariants and leave the others as documentary claims. Most use at least three of the fifteen architectural anti-patterns. Most cannot supply the evidence that a specialist underwriter needs to price the deployment, which means they are commercially uninsurable in the sectors their go-to-market narrative is aimed at.

Better to discover this at redesign time, when the cost is architectural rework, than to discover it via an incident, a regulator letter, a Verisk 2026-style commercial insurance exclusion, or an EU AI Act Article 26 authority request that the system cannot answer. The framework is offered in that spirit: a mirror held up honestly, not a sales pitch with decorative criticism attached.

## 4. What is open, what is private, what is available

**Open** — released under CC-BY-4.0 in this repository. Use without contacting us.

- `framework.md` — the rating framework (v0.5)
- `manifesto.md` — *Law as Pattern*, the argument
- `antipatterns.md` — 26 named anti-patterns
- `insurability.md` — actuarial companion
- `spec/` — JSON Schema, conformance tests, attestation format, worked examples
- `ACKNOWLEDGEMENTS.md` — credits to Jason Gagne's Sentinel programme and other sources

**Private** — Lane2 commercial IP. **Available for pre-launch validation PoC engagements.**

- **DOP** — our governance platform. The reference implementation from which the framework's architectural primitives (action-class taxonomy, capability-routing broker, ontology-as-firewall composition, Kalman-based compliance state estimation, and the Expected Compliance Risk formalism) are generalised.
- **SAPP** (Settlement Anchor Protocol Platform) — our externally-anchored evidence engine. The reference design behind Invariant 2 (evidence binding) and §15 (compositional enforcement) in the framework. Provides tamper-evident Merkle-proof commitments with independent signing keys, evidence scoring, liability allocation, and EU AI Act minimum-evidence-profile conformance out of the box.
- **PACT packs** — our domain-specific governance packs. One reference pack (legal-citation-review) is public in a sibling repository; other packs (clinical, financial, wallet/identity) are private.

**You do not need DOP, SAPP, or any PACT pack to use the framework.** The framework is deliberately tool-agnostic. Any conformant implementation of the patterns described is acceptable; our private components are one set of implementations, not the only ones possible.

We are pre-launch as of this writing. Commercial terms are being defined; in the meantime, **all our work is available for validation PoC engagements**: architecture review against the framework, deployer-level conformance assessment, proof-of-concept deployments of DOP or SAPP in a customer environment, and joint work with vertical-agent teams or specialist underwriters on calibrating the framework to a specific domain. Contact via [lane2.ai](https://lane2.ai).

## 5. Historical genesis — why we rejected direct-LLM-tool coupling

Roughly a year before Jason Gagne's Sentinel corpus was published, we reviewed the emerging agentic-AI integration patterns and made a specific architectural rejection. The patterns we declined to adopt:

- **Agent-to-agent natural-language coupling** as a composition primitive (the pattern that later appeared in A2A, CrewAI defaults, AutoGen defaults, LangGraph defaults)
- **Direct LLM-tool coupling** as the integration substrate — i.e. making every enterprise API tool-callable and letting the LLM choose freely. MCP-the-protocol is neutral; the MCP-ecosystem-as-integration-default was the specific pattern we rejected, along with the adjacent pattern of function-calling-as-primary-control-surface.
- **Persona prompts as a security boundary** — "you are a helpful assistant that never does X"

The patterns we adopted instead:

- **Narrow closed-world agents** with declared scope enforced structurally
- **Capability-routing via a broker** (the pattern the framework calls AARP) — peers exchange typed capability requests, not natural language
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

- **v0.1, 2026-04-21** — Initial positioning. Pre-launch. DOP and SAPP named as private IP available for PoC engagement. Historical genesis of the integration-pattern rejection documented.

This document is a *living statement* and will be updated as Lane2's commercial terms, product offerings, and position in the market evolve. Consult the current `README.md` for commercial terms in force at the time you are reading.
