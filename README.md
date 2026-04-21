# Blast Radius Framework

*A classification framework for governing agentic AI systems.*

Tool-enabled large language models have shifted AI systems from bounded reasoning to real-world action. Evaluation practice has not kept pace: accuracy benchmarks and model-level guardrails do not capture system-level impact. This repository proposes a framework that does.

## The framework in one paragraph

Six axes (**A**uthority, **R**each, **C**oupling, **V** reversibility, **K** consequence, **O**bservability) with three modifiers (attack-accessibility, trajectory, residual-vs-inherent), five blast-radius classes (BR-1 through BR-5), an ordinal aggregation rule with explicit interaction overrides, a cardinal score `B̂(t|t) ± σ_B(t)` (Kalman-extended from DOP-162 Expected Compliance Risk), a composition rule for multi-vendor stacks with four named topology classes (sub-additive / super-additive / multiplicative / exponential-reducing), and seven architectural invariants that a BR profile must satisfy to be genuine rather than nominal. The central claim: system architecture, not model capability, determines operational risk — a claim that holds from engineering, regulatory, and actuarial directions simultaneously.

## The four documents

1. **[framework.md](./framework.md)** — the rating framework itself (current version: v0.5). Start here.
2. **[antipatterns.md](./antipatterns.md)** — 26 named anti-patterns that inflate blast radius and currently ship as "progress". Use for vendor diligence.
3. **[insurability.md](./insurability.md)** — actuarial companion mapping the framework onto specialist underwriter requirements (Munich Re aiSure, AIUC-1, Armilla/Lloyd's) and the λ/σ/υ variables their pricing needs.
4. **[DOP reference implementation audit](https://github.com/kevin-biot/DOP/blob/main/docs/research/governance/dop-repo-shape-as-br-reference.md)** — in a separate repository, a worked audit of the DOP framework against the specification here, including honest gap list.

## Reading guide by role

| If you are a… | Read |
|---|---|
| Architect / engineering lead | `framework.md` §§4–9 (axes, aggregation, invariants); `antipatterns.md` for self-assessment |
| CISO / security function | `framework.md` §13 (security-ops mapping); `antipatterns.md` Part B (evidence-chain anti-patterns) |
| Risk / compliance / audit | `framework.md` §§5, 10, 18 (aggregation, governance, vendor questionnaire); `insurability.md` |
| Procurement / purchasing | `framework.md` §18 (vendor questionnaire); `antipatterns.md` entire |
| Board / executive | `framework.md` abstract + §18 central claim + §14 insurability |
| Insurer / underwriter | `framework.md` §§5, 9, 14; `insurability.md` entire |
| Regulator | `framework.md` §§4, 9, 10, 13, 14; `insurability.md` §4 Quadrant mapping |

## Status

- **Current version:** v0.5 (2026-04-21)
- **Maturity:** research draft; open for comment
- **Stability:** major-version increments preserve section numbering; minor revisions may refine equations and add open questions
- **Not yet shipped:** machine-readable schema for the vendor questionnaire, conformance test specifications per invariant, axis-scoring rubric, reference attestation format. These are the v0.6+ work.

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
