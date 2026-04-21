# Blast Radius Framework

*A classification framework for governing agentic AI systems.*

Tool-enabled large language models have shifted AI systems from bounded reasoning to real-world action. Evaluation practice has not kept pace: accuracy benchmarks and model-level guardrails do not capture system-level impact. This repository proposes a framework that does.

Published by **[Lane2](https://lane2.ai)** — a small AI infrastructure startup, pre-launch. The framework is licensed under CC-BY-4.0 and usable without engagement.

Lane2 publishes four open repositories solving distinct industry gaps:

- this one (blast-radius-framework) — rating agentic AI for operational impact
- [obo-standard](https://github.com/kevin-biot/obo-standard) — OBO minimum evidence standard for cross-organisational agentic transactions with no shared authorisation server (DNS-anchored, composes with OAuth/WIMSE/SPIFFE/W3C VCs/A2A/AGNTCY)
- [pact-public](https://github.com/kevin-biot/pact-public) — PACT specification bundle: closed-world bounded-intent ontology packs for regulated agent execution
- [Euro-Cloud-Substrate](https://github.com/kevin-biot/Euro-Cloud-Substrate) — ECS minimum contracts for EU cloud providers to export verifier-friendly evidence ("if you cannot export verifier-friendly evidence, you do not have sovereignty — you have hosting")

Our integrated commercial product suite — DOP (Deterministic Orchestration Pipeline), aARP (Autonomous Agent Routing Protocol), SAPP (Secure Agent Payment Protocol), CaaS (Context-as-a-Service), RTGF (Reference Token Generation Framework), and the Shared Ontology — is available for validation PoC engagements during pre-launch. See [about.md](./about.md) for full positioning, how the four open repos compose, and the OBO↔aARP relationship.

## The framework in one paragraph

Six axes (**A**uthority, **R**each, **C**oupling, **V** reversibility, **K** consequence, **O**bservability) with three modifiers (attack-accessibility, trajectory, residual-vs-inherent), five blast-radius classes (BR-1 through BR-5), an ordinal aggregation rule with explicit interaction overrides, a cardinal Kalman-extended Expected Compliance Risk score `B̂(t|t) ± σ_B(t)`, a composition rule for multi-vendor stacks with four named topology classes (sub-additive / super-additive / multiplicative / exponential-reducing), and seven architectural invariants that a BR profile must satisfy to be genuine rather than nominal. The central claim: system architecture, not model capability, determines operational risk — a claim that holds from engineering, regulatory, and actuarial directions simultaneously.

## The documents

1. **[framework.md](./framework.md)** — the rating framework itself (current version: v0.5.1). Start here for the specification.
2. **[NOTATION.md](./NOTATION.md)** — standalone lookup reference: every symbol, every tier enum, every class definition, every interaction override, every invariant, every anti-pattern ID. Use this when building or auditing. Authoritative over the embedded framework.md §21 pointer.
3. **[manifesto.md](./manifesto.md)** — *Law as Pattern*. The argument for why a framework like this must exist.
4. **[about.md](./about.md)** — who we are (Lane2, pre-launch), what is open and what is private (DOP, aARP, SAPP, CaaS, RTGF, Shared Ontology, PACT packs — available for PoC engagement), and the historical genesis of why we rejected direct-LLM-tool coupling. Covers how the four open Lane2 repositories compose and the OBO↔aARP relationship.
5. **[antipatterns.md](./antipatterns.md)** — 26 named anti-patterns that inflate blast radius and currently ship as "progress". Use for vendor diligence.
6. **[insurability.md](./insurability.md)** — actuarial companion mapping the framework onto specialist underwriter requirements (Munich Re aiSure, AIUC-1, Armilla/Lloyd's) and the λ/σ/υ variables their pricing needs.
7. **[spec/](./spec/)** — machine-readable conformance artefacts: JSON Schema for BR profiles, per-invariant test specifications, signed-attestation format, worked example profiles (closed-world BR-2 and open-world BR-4).
8. **[ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)** — credits to Jason Gagne's Sentinel programme (the empirical catalyst for Invariant 7 and the C4a phase-transition claims), prior published insurability work, and the broader intellectual background (Rules as Code, legal knowledge engineering, eIDAS / PSD2 / Basel precedents).

## Reading guide by role

| If you are a… | Read |
|---|---|
| Architect / engineering lead | `framework.md` §§4–9 (axes, aggregation, invariants); `antipatterns.md` for self-assessment |
| CISO / security function | `framework.md` §13 (security-ops mapping); `antipatterns.md` Part B (evidence-chain anti-patterns) |
| Risk / compliance / audit | `framework.md` §§5, 10, 18 (aggregation, governance, vendor questionnaire); `insurability.md` |
| Procurement / purchasing | `framework.md` §18 (vendor questionnaire); `antipatterns.md` entire |
| Board / executive | `framework.md` abstract + §18 central claim + §14 insurability |
| Insurer / underwriter | `framework.md` §§5, 9, 14; `insurability.md` entire |
| Regulator | `framework.md` §§4, 9, 10, 13, 14; `insurability.md` §4 Quadrant mapping; `manifesto.md` §§8–9 on composition with eIDAS / PSD2 / Basel |
| Anyone asking "why does this exist?" | `manifesto.md` — the argument, read standalone |
| Anyone asking "who are you and what do you sell?" | `about.md` — Lane2 positioning, private IP, how to engage for PoC |
| Anyone asking "who did the empirical work?" | `ACKNOWLEDGEMENTS.md` — Jason Gagne's **Sentinel** programme at PreneurialWorks is the empirical catalyst. Repo: [github.com/jasongagne-git/sentinel](https://github.com/jasongagne-git/sentinel). Cite Gagne 2026 (DOI [10.5281/zenodo.19477188](https://doi.org/10.5281/zenodo.19477188) preprint; [10.5281/zenodo.19476723](https://doi.org/10.5281/zenodo.19476723) dataset) whenever using Invariant 7 or the C4a claims |

## Status

- **Current version:** v0.5.1 (2026-04-21)
- **Maturity:** research draft; open for comment
- **Stability:** major-version increments preserve section numbering; minor revisions may refine equations and add open questions; patch versions (v0.5.1, v0.5.2, …) clarify and reorganise without changing definitions.
- **Spec v0.1 has shipped** as of 2026-04-21 — see [spec/](./spec/). Includes JSON Schema for BR profiles, per-invariant conformance tests, signed-attestation format, and two worked example profiles (closed-world BR-2; open-world BR-4). Axis-scoring rubric and third-party certification format remain v0.6+ work.
- **Tags:** `v0.5` (initial public release, 2026-04-21 initial commit), `v0.5.1` (this release — notation extracted to [NOTATION.md](./NOTATION.md), §5.5 worked examples added, §12 observability strengthened). External citations should use explicit version tags — e.g. `framework.md v0.5.1 §5.1` — rather than tracking `main`.

## Versioning policy

The framework is versioned `vX.Y` with history preserved in [CHANGELOG.md](./CHANGELOG.md). Stable section numbers are a priority — citations like `framework.md §5.4 Kalman extension` should remain valid across minor revisions. A major version increment signals a section renumbering or a removed concept; in that case the CHANGELOG will document migration.

## Contributing

Issues and discussion welcome. The framework evolves from empirical evidence (Sentinel-class datasets, specialist underwriter published criteria, real deployer audits) and from critique. Both are invited.

Open questions live at the tail of `framework.md §19`. Proposals to close any of them are particularly welcome.

## Citation

> Brown, K. (2026). *Blast Radius Framework: A classification framework for governing agentic AI systems*. Version 0.5. https://github.com/kevin-biot/blast-radius-framework

## Licence

The text of this repository is licensed under [Creative Commons Attribution 4.0 International (CC-BY-4.0)](./LICENSE). You may copy, redistribute, and build upon the material for any purpose, including commercially, under the terms of that licence.

Any code, schemas, or conformance test suites added in future versions will be released under Apache 2.0 alongside the text.

## Related work

- **OECD Rules as Code** programme
- **eIDAS** (Levels of Assurance with conformance tests) as a precedent for pattern-based EU regulation
- **Basel III risk-weighted capital** as a precedent for pattern-based financial regulation
- **MITRE ATLAS** (adversarial ML threat landscape) — attack-shaped, complements this framework's impact-shaped approach
- **OWASP LLM Top 10** — threat-shaped, complements
- **NIST AI RMF** — process-shaped, complements
- **ISO/IEC 42001** — management-system-shaped, complements
- **EU AI Act** (Regulation 2024/1689) — category-shaped, complements

The framework here occupies the gap none of the above cover: *operational blast radius as a rateable, priceable, composable property of the deployed system*.
