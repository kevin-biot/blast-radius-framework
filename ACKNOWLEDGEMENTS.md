# Acknowledgements

This framework synthesises ideas and evidence from several sources. Specific credits below; general intellectual debts to the Rules as Code programme, eIDAS / PSD2 / Basel as pattern-based regulatory precedents, and the broader legal-knowledge-engineering tradition are stated in [manifesto.md](./manifesto.md) §§11–13.

## The empirical catalyst — Jason Gagne's Sentinel programme

The seventh invariant (*bounded coupling*) and the C4a phase-transition claims in the framework rest directly on Jason Gagne's **Sentinel** programme at **PreneurialWorks** — an empirical multi-agent drift measurement platform. Sentinel comprises 79 experiments, 36,000+ agent messages, and 76,000+ probes run on distributed Jetson Orin Nano hardware. Findings include vocabulary collapse of 23–43%, sentiment collapse of 12–60%, probe-message divergence of 5–50×, and — critically — that in-context monitoring itself pollutes measurement by a factor of 3–6×.

Every Sentinel finding is mechanism-dependent on **conversational coupling** between agents. That is precisely the substrate pattern the framework's Invariant 7 (bounded coupling) rules out and the §4.0 worldview classifier gates on. Sentinel is therefore the framework's empirical falsification surface: if NL-coupled substrates did not exhibit the measured phase transitions, Invariant 7 and the T2 super-additive composition class would be unmotivated. They are instead measured, reproducible, and time-indexed.

Without Sentinel's corpus, the framework would still have the architectural claim that NL-coupled agent chains are dangerous. With it, the framework can say *measurably, reproducibly, at specific turn-counts under specific workload shapes*. That is the difference between a position and an empirical argument.

### Primary citations

Gagne, J. (2026). *Behavioral Drift in Multi-Agent LLM Systems: Emergent Failure Modes, Cascade Dynamics, and Measurement Challenges.* Preprint. DOI: [10.5281/zenodo.19477188](https://doi.org/10.5281/zenodo.19477188).

Gagne, J. (2026). *Sentinel — code and dataset.* DOI: [10.5281/zenodo.19476723](https://doi.org/10.5281/zenodo.19476723). Canonical dataset.

Gagne, J. (2026). *The Behavioral Sufficiency Problem: Why AI Governance Frameworks, Modeled on Human Regulatory Theory, Cannot Operate Without the Cultural and Social Infrastructure That Co-Evolved Alongside Human Law.* SSRN Preprint. Governance-theoretic argument complementing the empirics.

Repository: [github.com/jasongagne-git/sentinel](https://github.com/jasongagne-git/sentinel)

All three works should be read by anyone implementing against the framework. Cite Gagne 2026 (Behavioral Drift) whenever invoking Invariant 7, the C4a phase-transition claims, or the T2 super-additive composition class.

### Scope note

Sentinel is explicitly *not* a pre-deployment certification framework or a production monitoring platform — Gagne frames it as a controlled laboratory. Its findings are about one specific coupling pattern (conversational NL coupling); they do not test typed-capability-routing architectures, shared-weights latent coupling, or ontology-vocabulary attractors. When citing Sentinel as evidence, preserve the scope: it is evidence about NL-coupled multi-agent systems, not about multi-agent systems in general.

## Private reference implementation

A proprietary governance platform (not publicly available) provided the majority of the architectural primitives the framework generalises:

- The compositional ontology-as-firewall pattern (`framework.md §15`) and its formal Bayesian validation
- The cardinal Expected Compliance Risk formalism that the Kalman extension in `framework.md §5.4` generalises
- The session-execution attestation pattern, capability-routing broker pattern, and action-class taxonomy cited throughout
- The EU AI Act minimum evidence profile (referenced in `framework.md §5.4` via the evidence-tier → R mapping)

The framework here distils those primitives into a form that can be adopted, critiqued, and extended by practitioners without access to the private implementation. References to "an internal reference implementation" in the framework text point to this work. Specific architectural decision records (ADRs), code paths, and implementation details remain private.

## Prior published work — insurability framing

The six-invariant synthesis in `framework.md §9` (Invariants 1–6) derives from:

Brown, K. (2025). *The Insurability Gap: Why Nondeterministic AI Is Structurally Uninsurable, and What Changes When Architecture Produces Evidence Invariants.* Essay, privately circulated and selectively published.

The framework's v0.5 work adds Invariant 7 (bounded coupling) from Gagne-era empirical evidence post-dating the 2025 essay, and extends the ordinal rating into a cardinal score with Kalman-filtered uncertainty. See [insurability.md](./insurability.md) for the detailed mapping.

## General intellectual background

- **Rules as Code** — OECD, NSW government, Canada, France — as the framing for *law as pattern*
- **eIDAS** — Levels of Assurance with conformance tests — as the precedent for pattern-based EU regulation the AI Act should have followed
- **Basel III** — risk-weighted capital computed from specification — as the precedent for pattern-based financial regulation
- **IFRS / IAS, SPDX / OSI, SWIFT ISO 20022, IATA TCR** — as precedents for composable pattern in accounting, IP, payments, travel
- **Legal knowledge engineering** — Prakken, Sartor, Sergot (1990s onwards) — as the supply-side of *law as machine code* that has existed for decades
- **Catala, DAML, Blawx** — as live computational-law languages demonstrating feasibility
- **MITRE ATLAS, OWASP LLM Top 10, NIST AI RMF, ISO/IEC 42001** — as neighbouring, non-overlapping frameworks that this work complements rather than replaces

## Contributions

The framework belongs to whoever improves it. Contributors and their contributions will be credited in this file with each merged change. Open an issue at the repository to propose corrections, extensions, or empirical counter-evidence.
