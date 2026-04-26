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

## Public-interest reuse potential

This repository is published openly as public-interest scaffolding, not as a
private gatekept method. The aim is to reduce months of repeated abstract
discussion by giving deployers, regulators, standards bodies, auditors, and
conformity actors a concrete starting shape they can adopt, challenge, refine,
and formalise.

In particular, the material here is intended to be reusable as input to:

- harmonised standards work
- European Commission guidance
- common specifications where standards are delayed or incomplete
- AI regulatory sandbox methods and exit-report structure
- conformity assessment and audit practice
- deployer internal control and evidence design

The repository does **not** claim to be a harmonised standard, Commission
guidance, or a conformity assessment artifact in itself. It is an open
candidate scaffold for the technical and governance shapes those official
artifacts will need.

This repository works especially well when read together with
[Governance Failure Patterns](https://github.com/kevin-biot/governance-failure-patterns),
which names the recurring governance weaknesses that a blast-radius rating
should detect, demote, or force into explicit remediation.

## The documents

1. **[framework.md](./framework.md)** — the rating framework itself (current version: v0.5.1). Start here for the specification.
2. **[NOTATION.md](./NOTATION.md)** — standalone lookup reference: every symbol, every tier enum, every class definition, every interaction override, every invariant, every anti-pattern ID. Use this when building or auditing. Authoritative over the embedded framework.md §21 pointer.
3. **[manifesto.md](./manifesto.md)** — *Law as Pattern*. The argument for why a framework like this must exist.
4. **[about.md](./about.md)** — who we are (Lane2, pre-launch), what is open and what is private (DOP, aARP, SAPP, CaaS, RTGF, Shared Ontology, PACT packs — available for PoC engagement), and the historical genesis of why we rejected direct-LLM-tool coupling. Covers how the four open Lane2 repositories compose and the OBO↔aARP relationship.
5. **[antipatterns.md](./antipatterns.md)** — 26 named anti-patterns that inflate blast radius and currently ship as "progress". Use for vendor diligence.
6. **[insurability.md](./insurability.md)** — actuarial companion mapping the framework onto specialist underwriter requirements (Munich Re aiSure, AIUC-1, Armilla/Lloyd's) and the λ/σ/υ variables their pricing needs.
7. **[spec/](./spec/)** — machine-readable conformance artefacts: JSON Schema for BR profiles, JSON Schema for component cards, per-invariant test specifications, signed-attestation format, and worked example profiles (closed-world BR-2 and open-world BR-4).
8. **[adoption/](./adoption/)** — companion artefacts for operationalising and distributing the framework: gap-closure task list, external-tools mapping annex, benchmark-harness design, questionnaire-to-profile conversion design, component-card format, published NIST AI RMF crosswalk, published ISO/IEC 42001 crosswalk, published EU AI Act crosswalk, published *AI Agents Under EU Law* research crosswalk, published specialist-underwriter crosswalk, crosswalk roadmap, and OECD visibility plan.
9. **[reports/](./reports/)** — report templates and worked examples:
   - [`reports/templates/`](./reports/templates/) — three reusable templates (Tier 1 executive summary, Tier 2 technical findings, Tier 3 ADR backlog) for applying the framework to any system
   - [`reports/lane2/`](./reports/lane2/) — Lane2 applying the framework to its own integrated stack as the worked example. Seven-version correction chain documented; three named gaps published honestly
10. **[oecd-catalogue-assessment.md](./oecd-catalogue-assessment.md)** — comparison note for readers asking whether the OECD Catalogue of Tools & Metrics for Trustworthy AI already covers this problem. Separates what the OECD catalogue does, what it does not do, which OECD-linked tools are genuinely useful to BRF adopters, and which BRF roadmap items it makes more urgent.
11. **[authoring-notes.md](./authoring-notes.md)** — transparent provenance of method: how this repo and the self-assessment artefacts were produced under a human-domain-holder + AI-epistemic-partner force-function pattern. Prescription for deployers applying the framework to their own systems. Counter to A14 (approval fatigue) and A7 (LLM-as-judge) applied to assessment authoring.
12. **[ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)** — credits to Jason Gagne's Sentinel programme (the empirical catalyst for Invariant 7 and the C4a phase-transition claims), prior published insurability work, and the broader intellectual background (Rules as Code, legal knowledge engineering, eIDAS / PSD2 / Basel precedents).

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
| Anyone asking "does OECD already cover this?" | `oecd-catalogue-assessment.md` — direct comparison with the OECD Catalogue of Tools & Metrics for Trustworthy AI, plus supporting-tool map and action list |
| Anyone asking "what are the missing adoption pieces and how do we close them?" | `adoption/` — the gap-closure workstream: evidence adapters, harness design, converter design, component cards, four published crosswalks, and OECD visibility plan |
| Anyone asking "how does this relate to NIST AI RMF?" | `adoption/crosswalk-nist-ai-rmf.md` — first crosswalk showing how BRF fits inside NIST's Govern / Map / Measure / Manage structure without claiming equivalence |
| Anyone asking "how does this relate to ISO/IEC 42001?" | `adoption/crosswalk-iso-42001.md` — second crosswalk showing how BRF fits inside an AI management system standard without claiming certification or substitution |
| Anyone asking "how does this relate to the EU AI Act?" | `adoption/crosswalk-eu-ai-act.md` — third crosswalk showing how BRF supports architecture-and-evidence disclosure for legal obligations without substituting for law or conformity assessment |
| Anyone asking "how does this relate to AI Agents Under EU Law?" | `adoption/crosswalk-ai-agents-under-eu-law.md` — research-to-research note showing how the Lane2 open repository set contributes candidate control shapes, failure taxonomies, evidence forms, and conformance scaffolds for the gap the working paper identifies |
| Anyone asking "how does this relate to insurance or specialist underwriters?" | `adoption/crosswalk-specialist-underwriters.md` — fourth crosswalk showing how BRF maps into public due-diligence and assurance criteria in the specialist AI-insurance market |
| Anyone asking "who did the empirical work?" | `ACKNOWLEDGEMENTS.md` — Jason Gagne's **Sentinel** programme at PreneurialWorks is the empirical catalyst. Repo: [github.com/jasongagne-git/sentinel](https://github.com/jasongagne-git/sentinel). Cite Gagne 2026 (DOI [10.5281/zenodo.19477188](https://doi.org/10.5281/zenodo.19477188) preprint; [10.5281/zenodo.19476723](https://doi.org/10.5281/zenodo.19476723) dataset) whenever using Invariant 7 or the C4a claims |
| Anyone asking "how was this written? can I trust it?" | `authoring-notes.md` — the human-domain-holder + AI-epistemic-partner force-function method; seven-version self-assessment correction chain as evidence the method operates; prescription for deployers producing their own ratings |

## Status

- **Current version:** v0.5.10 (2026-04-21) — completes the v0.5.9 structural reorg (v0.5.9 shipped with six untracked files and unstaged sed modifications). Templates under [`reports/templates/`](./reports/templates/); Lane2 self-assessment artefacts under [`reports/lane2/`](./reports/lane2/) with all links now resolving correctly. See CHANGELOG for the process-error note. No framework definition changes.
- **Maturity:** research draft; open for comment
- **Stability:** major-version increments preserve section numbering; minor revisions may refine equations and add open questions; patch versions (v0.5.1, v0.5.2, …) clarify and reorganise without changing definitions.
- **Spec v0.1 has shipped** as of 2026-04-23 — see [spec/](./spec/). Includes JSON Schema for BR profiles, JSON Schema for component cards, per-invariant conformance tests, signed-attestation format, and two worked example profiles (closed-world BR-2; open-world BR-4). Axis-scoring rubric and third-party certification format remain v0.6+ work.
- **Tags:** `v0.5` (initial public release), `v0.5.1` (notation extracted, worked examples added, observability strengthened), `v0.5.2` (report template, Lane2 self-assessment, worked template application), `v0.5.3` (self-assessment I5 correction), `v0.5.4` (OBO A2A reference implementation evidence added), `v0.5.5` (PACT three-layer model clarified; backlog items 8 and 9 reframed), `v0.5.6` (A15 tool-layer architectural separation documented), `v0.5.7` (SAPP role-based API surface cited; backlog item 11 reframed; BR-4 floor analysis), `v0.5.8` (authoring-notes.md — epistemic-partner force-function method documented), `v0.5.9` (structural reorg — incomplete; see v0.5.10), `v0.5.10` (completes v0.5.9 reorg — fixup commit for untracked files). External citations should use explicit version tags — e.g. `framework.md v0.5.1 §5.1` — rather than tracking `main`. Do not use `v0.5.9` — use `v0.5.10` or later for the complete reorg.

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
- **OECD Catalogue of Tools & Metrics for Trustworthy AI** — broad discovery surface for technical, procedural, and educational tools; useful as adjacent ecosystem and evidence-source map, not a substitute for an architecture-first blast-radius rating. See [`oecd-catalogue-assessment.md`](./oecd-catalogue-assessment.md)
- **eIDAS** (Levels of Assurance with conformance tests) as a precedent for pattern-based EU regulation
- **Basel III risk-weighted capital** as a precedent for pattern-based financial regulation
- **MITRE ATLAS** (adversarial ML threat landscape) — attack-shaped, complements this framework's impact-shaped approach
- **OWASP LLM Top 10** — threat-shaped, complements
- **NIST AI RMF** — process-shaped, complements
- **ISO/IEC 42001** — management-system-shaped, complements
- **EU AI Act** (Regulation 2024/1689) — category-shaped, complements

The framework here occupies the gap none of the above cover: *operational blast radius as a rateable, priceable, composable property of the deployed system*.

## Companion repository

This repository is a companion to
[Governance Failure Patterns](https://github.com/kevin-biot/governance-failure-patterns).

The relationship is:

- **Blast Radius Framework** rates the operational blast surface of a deployed
  system and provides an attestation form.
- **Governance Failure Patterns** names recurring governance failure classes,
  anti-patterns, and tightening patterns that help explain why systems may be
  weakly controlled, misleadingly governed, or difficult to audit.

The two repositories are adjacent but not interchangeable:

- BRF is the rating and attestation layer
- GFP is the diagnosis and remediation-pattern layer
