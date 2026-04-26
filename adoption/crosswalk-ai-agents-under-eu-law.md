# Repo-Set Crosswalk to *AI Agents Under EU Law*

*Research-to-research translation note from the Lane2 open repository set into the April 7, 2026 working paper **AI Agents Under EU Law**.*

**Status:** Initial crosswalk  
**Date:** 2026-04-26  
**Primary comparison target:** *AI Agents Under EU Law* (working paper, April 7, 2026)  
**Companion materials:** [crosswalk-eu-ai-act.md](./crosswalk-eu-ai-act.md), [Governance Failure Patterns](https://github.com/kevin-biot/governance-failure-patterns)

---

## 1. Purpose

This note answers a practical question:

> What is the relationship between the public Lane2 repository set and the working paper *AI Agents Under EU Law*?

Short answer:

- the paper is a **legal-technical research diagnosis** of what agent providers,
  deployers, and regulators now need
- the Lane2 repository set is **open technical and governance scaffolding**
  that makes much of that needed shape concrete

They are not the same kind of artifact. The paper diagnoses the governance and
standardisation gap. The repositories offer candidate structures that can help
close it.

---

## 2. Non-equivalence note

This crosswalk is **not** a claim that:

- the repositories are law
- the repositories are harmonised standards
- the repositories are Commission guidance
- the repositories are conformity assessment artifacts in themselves
- the working paper endorses the repository set

The correct relationship is:

- the paper identifies the regulatory, engineering, and standards gap
- the repositories contribute reusable control shapes, failure taxonomies,
  evidence forms, and conformance scaffolds that can help institutions close it

---

## 3. What the paper does

At a high level, *AI Agents Under EU Law* makes eight moves that matter for
technical governance:

1. it shifts attention from model labels to **external actions, data flows,
   connected systems, and affected persons**
2. it treats **runtime drift, traceability, oversight, and access control** as
   load-bearing compliance questions
3. it argues that multi-instrument compliance is the baseline: AI Act, GDPR,
   CRA, Data Act, NIS2, sector rules, and more
4. it identifies the incomplete state of standards and guidance for agentic AI
5. it pressures both deployers and regulators to ask what a governed agent
   runtime actually looks like

The paper is therefore not just a classification exercise. It is a structural
challenge to the current state of implementation guidance.

---

## 4. What the repository set does

The Lane2 open repository set contributes three distinct layers:

1. **Blast Radius Framework (BRF)** — rates operational blast surface and
   attestation shape for deployed agentic systems
2. **Governance Failure Patterns (GFP)** — names recurring governance weakness
   classes, anti-patterns, and repair paths
3. **The surrounding open specifications and pack work** — especially
   `obo-standard`, `pact-public`, and related public materials — provide
   bounded-intent, delegated-authority, and evidence-shape scaffolding

Taken together, these repositories do not merely say “agentic AI is risky.”
They propose reusable structures for:

- rating risk propagation
- diagnosing weak governance claims
- naming control failures
- structuring evidence
- shaping conformance questions
- reducing ambiguity for standards and policy actors

In that sense, the repository set functions as a **candidate reference-architecture scaffold** for a governance layer that the paper shows is still under-specified institutionally.

---

## 5. High-level mapping

| Working-paper concern | Closest repository response | What the repositories add | Current maturity |
|---|---|---|---|
| External actions, not model taxonomy, determine regulatory trigger | BRF `A–R–C–V–K–O`; GFP `F010 Risk-Profile Omission`; bounded-intent and tool-scoped design across the public stack | A concrete vocabulary for operational surface, not just legal category | Published research scaffold |
| Execution-layer control matters more than prompt-layer caution | GFP `F007 Runtime Governance Substitution`, `AP007 Policy PDF, Runtime Nothing`, `AP012 MCP Direct-to-LLM Tool Coupling`; BRF invariants | A named negative reference for governance that does not bind runtime behavior | Published research scaffold |
| Human oversight must be specific, proportionate, and credible | BRF reversibility, consequence, observability, trajectory, class-promotion logic; GFP `AP009 Human Oversight as Ceremony` | A way to ask whether oversight is structurally meaningful rather than ceremonially present | Published research scaffold; runtime rendering depends on implementation |
| Runtime drift and post-deployment change are compliance-critical | BRF observability + trajectory review; GFP `F002 Absorbed Drift and Baseline Laundering`, `F009 Validation-Lifecycle Break` | A public grammar for drift, baseline corruption, and stale validation | Published research scaffold |
| Multi-instrument compliance needs a real technical map | BRF EU AI Act crosswalk and `K` consequence framing; GFP risk-profile and accountability patterns | A bridge from legal obligations to operational profile and evidence shape | Partial; still not a full adjacent-law ontology |
| General-purpose open platforms create a structural classification dilemma | BRF worldview gate, composition classes, invariant floors; GFP `AP010 Capability Discovery as Attack Surface`, `AP015 Framework Without Risk Profile` | A hard architectural distinction between bounded and open-world systems | Published research scaffold |
| Standards and guidance are incomplete for agentic AI | BRF profiles, component cards, attestations, and crosswalks; GFP failure classes, anti-pattern tests, repair patterns | Reusable public starting artifacts for standards, guidance, common specifications, and assessors | Published and open |
| Regulators and deployers need evidence, not slogans | BRF signed-attestation and report shape; GFP conformance tests and evidence discipline | A verifier-friendly evidence grammar rather than governance marketing language | Published research scaffold |

---

## 6. Where the repositories are ahead of the paper

Relative to the paper, the repository set is ahead in five ways:

1. **Named failure classes**
   The paper identifies governance problems. GFP names recurring failure forms
   such as runtime-governance substitution, validation-lifecycle break, and
   risk-profile omission.

2. **Operational blast-surface vocabulary**
   BRF gives a compact architecture-first way to speak about authority, reach,
   coupling, reversibility, consequence, and observability.

3. **Negative reference discipline**
   The anti-pattern catalogues make it easier to say not only what good
   governance looks like, but what false or performative governance looks like.

4. **Attestation and machine-readable shape**
   BRF and GFP both move beyond prose by providing profile forms, tests, and
   reusable reporting structures.

5. **Open public-interest packaging**
   The repository set is deliberately reusable by deployers, standards actors,
   auditors, and public institutions without requiring access to a proprietary
   engagement.

---

## 7. Where the paper correctly identifies remaining gaps

The paper also highlights limits that the public repository set does not remove
by itself:

1. **A rating framework is not a runtime**
   BRF and GFP do not by themselves enforce tool-layer authority, oversight, or
   evidence capture. They need a runtime substrate or institutional uptake.

2. **Adjacent-law crosswalk depth remains incomplete**
   A full operational map across GDPR, CRA, Data Act, NIS2, sector regimes, and
   national overlays still requires more detailed surface modeling.

3. **Human oversight remains easy to overstate**
   Even with BRF and GFP, actual runtime enforcement of proportionate oversight
   remains an implementation question.

4. **Conformity practice still needs institutional form**
   Standards bodies, the Commission, sandbox operators, and assessors still
   need to turn public scaffolds into official methods.

The repositories reduce ambiguity. They do not eliminate the need for formal
institutional work.

---

## 8. Why this matters for standards and guidance

The paper implies that Europe still lacks enough concrete, public, reusable
technical structure for agentic governance. The repository set is useful
because it shortens that path.

It offers material that can be reused as input to:

- harmonised standards work
- Commission guidance
- common specifications
- AI regulatory sandbox methods
- conformity assessment and audit practice
- deployer internal control design

This is the practical public-interest proposition:

> less repeated abstract discussion, more concrete starting structure

---

## 9. Bottom line

The cleanest relationship is:

> *AI Agents Under EU Law* diagnoses the governance and standardisation problem. The Lane2 open repository set provides candidate control shapes, failure taxonomies, evidence forms, and conformance scaffolds that can help institutions build the missing operational layer.

The strongest careful claim is not that the repositories are already the
official answer. It is that they are an **open candidate scaffold for the
reference-architecture layer the paper shows is still missing**.
