# Law as Pattern

*A manifesto for the governance of agentic AI systems.*

**Version:** 0.1
**Date:** 2026-04-21

---

## I. Where we are

**1.** Agentic AI changed what software does. It no longer only generates outputs; it acts on external systems, modifies state, delegates to peers, composes with third parties, and produces consequences. Errors are not wrong answers anymore. They are wrong actions.

**2.** Governance did not change with it. Accuracy benchmarks, prompt design, and model-level guardrails remain in place. None of them captures system-level impact. The industry knows this. The industry looks away.

**3.** Insurers know it too. They stay silent for three structural reasons:

- **Aggregation fear.** If one insurer publishes a scoring model and it is wrong, they are solely exposed. If every insurer uses the same model, systemic risk concentrates and regulators arrive. So each major carrier builds bespoke and keeps it proprietary. Munich Re's aiSure math is not public; AIUC-1 publishes criteria but not the loss distribution.
- **Missing actuarial substrate.** Casualty Actuarial Society, Institute of Actuaries UK, International Actuarial Association have no working groups on agentic-AI-specific loss distributions. The frequency/severity/uncertainty (λ/σ/υ) data does not exist yet because the deployments producing it are new and non-stationary. Munich Re has maybe 18 months of meaningful aiSure claims history.
- **Competitive moat logic.** A better AI scoring model *is* the product. Open-sourcing the schema is giving the moat away. Insurance has no PEPPOL, no SPDX, no SWIFT equivalent for AI disclosure because nobody is incentive-compatible for building it.

**4.** Regulators draft prose. Prose cannot be verified, cannot be composed, cannot be priced. The EU AI Act Article 15 says "robust" where it could have said "passes conformance test suite X". That was a choice, not a necessity.

## II. How we got here

**5.** Legal drafting tradition prizes ambiguity. Ambiguity lets courts adapt interpretation across cases the drafter did not foresee. Pattern — machine-readable, unambiguous, composable — is incompatible with judicial discretion as currently constituted.

**6.** Civil-law systems do this worse than common-law because they rely on legislative precision rather than case-law evolution. When the legislature is vague, civil-law practitioners have less ability to repair the gap.

**7.** Big Tech lobbying actively prefers prose. Prose is negotiable in court; pattern is not. The trilogue choices that produced Article 15 were lobbied into that shape. Article 12 logging was narrowed similarly. The patterns that existed in draft form did not survive.

**8.** The EU knows how to do pattern when it wants to. Three precedents:

- **eIDAS** — Levels of Assurance (Low / Substantial / High) with conformance tests, trust lists, machine-verifiable assertions. Digital identity as a composable pattern.
- **PSD2 Strong Customer Authentication** — the RTS spells out the mechanism, composable requirements (two-factor, dynamic linking, exemption conditions), and conformance tests. Banks implement against the pattern, not a lawyer's opinion.
- **Basel III risk-weighted capital** — banks compute RWA from a specification, not prose. Regulators audit against the spec.

**9.** So the AI Act's prose form is not fate. It is choice. And to the old critique that Brussels cannot do 27-member coordination: the AI Office is being set up with 27 national competent authorities, each interpreting "robustness" locally. It will fragment exactly as Single European Sky fragmented. Five years from now there will be a harmonisation proposal because the interpretations diverged.

## III. What pattern means

**10.** Pattern, as used here, means the union of:

- An **ontology** naming what is being rated
- **Executable properties** that can be verified at runtime, not asserted in prose
- A **compositional algebra** specifying how rated components combine
- A **disclosure schema** that makes claims machine-readable
- **Measurement mechanics** that quantify uncertainty, not eliminate it

A rule is a pattern when two independent auditors applying it to the same system produce the same score. Prose rules fail this test routinely. Pattern rules pass it by construction.

**11.** Pattern already exists in neighbouring domains:

- **IFRS / IAS** — accounting as pattern. Financial statements are machine-comparable because the pattern is shared.
- **SPDX / OSI license taxonomy** — intellectual-property licensing as pattern.
- **IATA TCR / airport slot allocation** — travel law already substantially machine-coded.
- **Basel III** — financial regulation as pattern (for capital; less so for conduct).
- **eIDAS** — digital identity assurance as pattern.
- **SWIFT ISO 20022** — payments as pattern.

**12.** None of these covers agentic AI. The gap is structural, not a temporary oversight.

**13.** The intellectual apparatus has been ready for decades. Legal knowledge engineering (Prakken, Sartor, Sergot) dates to the 1990s. Computational law languages (Catala, DAML, Blawx) exist. Rules as Code programmes (OECD, NSW, Canada, France) are operational. The use case finally arrived. The supply has been waiting.

## IV. What this framework is

**14.** The [Blast Radius Framework](./framework.md) is a sketch. It is not a finished specification. It is offered as a starting shape, to be refined by adoption, critique, and empirical evidence.

**15.** Its pieces map to the pattern definition in thesis 10:

- **Six axes** (Authority, Reach, Coupling, Reversibility, Consequence, Observability) — the ontology
- **Seven invariants** (deterministic execution, evidence binding, policy snapshot coherence, bounded blast radius, jurisdictional awareness, fail-closed execution control, bounded coupling) — the executable properties
- **Four composition topologies** (sub-additive, super-additive, multiplicative, exponential-reducing) — the compositional algebra
- **Vendor questionnaire** (framework.md §18) — the disclosure schema
- **Kalman-extended cardinal score** `B̂(t|t) ± σ_B(t)` — the measurement mechanics

**16.** It is licensed CC-BY-4.0. A pattern that cannot be freely adopted, redistributed, and built upon is not a pattern. It is a product. The framework must be a pattern.

**17.** It will be wrong in places. The v0.5 open questions list is at `framework.md §19`. Corrections, extensions, and counter-examples are explicitly invited. The framework evolves from evidence and critique, not from committee.

## V. What we ask

**18.** **Of specialist insurers:** publish the loss distributions. The moat is not the math; the moat is the data, and the data will compound faster if shared than if hoarded. A shared disclosure schema is a public good that rewards whoever builds it into their pricing fastest.

**19.** **Of regulators:** compose with existing patterns. eIDAS, PSD2, Basel, IFRS are precedents. The AI Office can adopt and extend rather than re-drafting prose that 27 authorities will interpret 27 ways. Harmonisation by composition is cheaper than harmonisation by litigation.

**20.** **Of standards bodies (ISO, IEC, NIST, ETSI):** adopt and refine. This is what you exist for. The framework is licensed openly for exactly that purpose.

**21.** **Of deployers:** demand the disclosure. The vendor questionnaire in `framework.md §18` is copy-paste ready for RFP clauses. A vendor that will not answer has rated the provision as "too revealing" which is itself a rating.

**22.** **Of architects:** build to the seven invariants. The market is about to reward systems that can produce evidence for Invariants 1–2 because they are the prerequisite for insurability. Governance is no longer the cost centre; it is the pricing input.

**23.** **Of contributors:** open an issue. Propose a section rewrite. Challenge the mathematics. Cite missing precedents. The framework belongs to whoever improves it.

## VI. Closing

**24.** The day is here. Tool-enabled AI is deployed in production in regulated sectors now. The regulatory patchwork is forming now. The insurance exclusions take effect through commercial contracts now (Verisk 2026). The precedents that will govern the next decade are being set now.

**25.** Architecture is the executable form of governance, of regulatory compliance, and of insurability. These are not three problems. They are one problem with three audiences. If blast radius is not designed, it is not controlled, not priced, and not deployable in regulated sectors.

**26.** Law must be machine code as pattern. Not because patterns are elegant, but because prose has failed the test of the moment. Agentic AI moves faster than judicial interpretation; it composes more densely than process-shaped management systems; it aggregates losses across deployments in ways no case-by-case adjudication can keep pace with.

**27.** The alternative to pattern is not "governance as we know it". The alternative is *uncovered, unpriced, unverifiable, and quietly banned from the sectors that matter most*. That is the actual default of the current trajectory. It is already happening.

**28.** We can do better. The pattern apparatus exists. The framework here is one attempt. Build better ones. But build.

---

*The Blast Radius Framework is maintained at [github.com/kevin-biot/blast-radius-framework](https://github.com/kevin-biot/blast-radius-framework). This manifesto is CC-BY-4.0. Signatures, endorsements, disagreements, and fork-and-improve contributions are all welcome by the same open terms as the framework itself.*
