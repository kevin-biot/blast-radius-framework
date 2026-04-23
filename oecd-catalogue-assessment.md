# OECD Catalogue Assessment

*What the OECD Catalogue of Tools & Metrics for Trustworthy AI adds to the Blast Radius Framework, what it does not add, and what work it suggests next.*

**Status:** Working note for repo readers
**Date:** 2026-04-23
**Scope:** [OECD Catalogue of Tools & Metrics for Trustworthy AI](https://oecd.ai/en/catalogue/overview/), with emphasis on the [metrics catalogue](https://oecd.ai/en/catalogue/metrics)

---

## 1. Why this note exists

Readers of this repository will reasonably ask:

1. "Does the OECD catalogue already solve this problem?"
2. "If not, does it expose a miss in the Blast Radius Framework?"
3. "Which OECD-linked tools are actually useful to someone trying to apply BRF in practice?"

This note answers those questions directly so readers do not need to know the OECD catalogue in advance.

Short answer:

- **No, the OECD catalogue does not replace BRF.**
- **Yes, it highlights useful supporting tools and some packaging/tooling gaps around BRF.**
- **The main gap is not the core theory. The main gap is the surrounding evidence-and-adoption tooling.**

---

## 2. Detailed task list

This assessment was produced against the following task list:

1. Define what the OECD catalogue is and is not.
2. Compare the OECD catalogue's metrics layer to BRF's rating layer.
3. Identify OECD-listed tools that a BRF deployer, auditor, or underwriter could actually use.
4. Separate genuine BRF gaps from adjacent-but-non-overlapping OECD material.
5. Convert the result into a practical action list for this repository and its companion repos.

Tasks 1 through 4 are completed in this note. Task 5 is completed as the prioritised roadmap in §7.

---

## 3. What the OECD catalogue is

The OECD catalogue is a **discovery and comparison surface** for trustworthy-AI tools, metrics, and use cases. It is broad by design.

Per the OECD catalogue overview and FAQ:

- the catalogue is a "one-stop-shop" for tools and metrics related to trustworthy AI
- it covers **technical**, **procedural**, and **educational** tools
- the metrics side is mainly a library of **technical formulas and methodologies** for measuring fairness, privacy, robustness, safety, security, transparency, and related properties
- submissions are open; the OECD Secretariat reviews entries for quality and taxonomy fit, but inclusion is **not an OECD endorsement**

That means the catalogue is useful as:

- a map of the surrounding ecosystem
- a place to find candidate supporting tools
- a way to see which adjacent governance practices already have public artefacts

It is **not**:

- a single coherent rating framework for deployed agentic systems
- an audit standard by itself
- an actuarial rating system
- a substitute for architecture-specific operational classification

---

## 4. What the OECD catalogue changes for BRF

### 4.1 What it does **not** change

The catalogue does **not** overturn BRF's core claim.

BRF's core position is that operational risk in agentic systems is driven by **architecture and composition**, not by model-quality metrics alone. The OECD metrics catalogue is mostly a library of formulas such as accuracy, AUC, privacy leakage counts, anonymity-set measures, and adversarial success measures. Those are useful, but they do not classify:

- bounded versus unbounded authority
- propagation through composed systems
- coupling regimes
- recovery horizons
- principal-population consequence
- insurability posture
- attested multi-vendor composition

Those are exactly the dimensions BRF was built to rate.

### 4.2 What it **does** change

The OECD catalogue makes three things clearer:

1. **There is already a public ecosystem of supporting tools.**
   BRF should point to these where they help generate evidence, documentation, or test artefacts.

2. **BRF currently has stronger theory than surrounding tooling.**
   The repo already admits this in the spec and open questions: reference harness, questionnaire-to-profile conversion, certification path, and crosswalks remain open. See [spec/README.md](./spec/README.md) and the v0.6 open questions in [framework.md](./framework.md).

3. **Readers need a bridge.**
   Many readers will not know the OECD work; many OECD catalogue users will not know BRF. A comparison note and tool-mapping layer make both more useful.

---

## 5. OECD material that is genuinely useful for BRF users

Not every OECD-listed entry matters for BRF. The useful ones are the ones that can produce evidence, documentation, or operational test artefacts that feed a BR profile or attestation.

### 5.1 High-value supporting tools

| Tool | OECD type | Why it matters for BRF | Recommended BRF use |
|---|---|---|---|
| [OpenEnv](https://oecd.ai/en/catalogue/tools/openenv) | Technical | Evaluates agents against real systems rather than toy benchmarks; surfaces failures in tool selection, argument formation, permissions, partial observability, and recovery | Use as a pattern for a BRF benchmark harness and for reproducible invariant/axis evidence in realistic agent workflows |
| [PyRIT](https://oecd.ai/en/catalogue/tools/pyrit) | Technical | Automates red-teaming for hallucination, misuse, privacy harms, and prompt injection | Feed `delta_adv` evidence, attack-surface testing, and change-regression testing |
| [garak](https://oecd.ai/en/catalogue/tools/garak%2C-llm-vulnerability-scanner) | Technical | Structured adversarial probing across jailbreaks, leakage, prompt injection, misinformation, and other failure modes | Use as a standard evidence generator for attack accessibility and prompt-surface claims |
| [Model Cards](https://oecd.ai/en/catalogue/tools/model-cards) | Procedural / educational | Standardised model documentation already familiar to many readers | Use as a template reference for BRF model-component cards inside larger system attestations |
| [Microsoft Datasheets for Datasets](https://oecd.ai/en/catalogue/tools/microsoft-datasheets-for-datasets) | Procedural | Standard dataset documentation for provenance, assumptions, and intended use | Use as a reference shape for dataset and corpus disclosures attached to BRF profiles |
| [IBM Factsheets for AI Governance](https://oecd.ai/en/catalogue/tools/ibm-factsheets-for-ai-governance) | Technical | Lifecycle and lineage tracking for model assets | Useful pattern for BRF evidence packets and component inventory views |
| [Judgment Assurance](https://oecd.ai/en/catalogue/tools/judgment-assurance) | Procedural | Stronger treatment of oversight maturity and reconstructible human judgment | Complement BRF's human-oversight and approval-fatigue treatment; useful for board/audit audiences |
| [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://oecd.ai/en/catalogue/tools/artificial-intelligence-risk-management-framework-ai-rmf-10) | Procedural | Widely known process-oriented governance frame | Primary candidate for a formal BRF crosswalk |

### 5.2 Useful but bounded tools

These are useful only in a constrained way:

| Tool | Why bounded |
|---|---|
| [AI Inherent Risk Scale (AIIRS)](https://oecd.ai/en/catalogue/tools/ai-inherent-risk-scale-aiirs) | Strong upstream triage for human-directed GenAI tasks, but explicitly not an agentic-system framework |
| Individual OECD metrics on privacy, fairness, or robustness | Useful as component-level evidence, but not a system-level blast-radius classifier |

### 5.3 What the metrics catalogue is good for

The metrics catalogue is most useful to BRF when treated as a **supporting evidence menu**:

- privacy-related metrics can support claims under `K3-P` or related data-governance concerns
- robustness and adversarial metrics can support `delta_adv` evidence
- anomaly-detection and drift-related metrics can support parts of `O` and `tau`
- task or model performance metrics can support narrow component documentation

What it should **not** be used for is replacing BRF's system-level class calculation.

---

## 6. Real gaps in BRF that the OECD catalogue makes more visible

The OECD catalogue does not expose a miss in BRF's central theory. It exposes misses in the **supporting adoption layer**.

### 6.1 Missing evidence adapters

BRF has the profile schema, invariant tests, and attestation format. What it does not yet have is a simple public mapping that says:

- "PyRIT output can support these BRF claims"
- "garak output can support these claims"
- "Model Cards and Datasheets can attach here"
- "OpenEnv-style environments can generate these benchmark artefacts"

This is a packaging miss, not a framework-definition miss.

### 6.2 Missing reference harness

The spec is explicit that it defines forms rather than implementations, and that a reference test harness has not yet shipped. See [spec/README.md](./spec/README.md). OECD entries like OpenEnv make that absence more obvious because they show what a public evaluation harness looks like in adjacent work.

### 6.3 Missing questionnaire-to-profile tooling

BRF already has a vendor questionnaire in [framework.md](./framework.md) and a profile schema in [spec/br-profile.schema.json](./spec/br-profile.schema.json). The missing bridge is the converter that takes structured answers and emits a valid profile draft with open items flagged.

### 6.4 Missing component-card layer

BRF is strong at the **system profile** level. OECD-listed documentation artefacts are stronger at the **component documentation** level. There is room for a BRF-native card format covering:

- model component
- dataset / retrieval corpus
- tool / integration
- external dependency
- evidence / anchor / attestation keying

### 6.5 Missing public crosswalks

The repo already names this as open work in [framework.md](./framework.md), but the OECD catalogue increases the practical importance:

- BRF to NIST AI RMF
- BRF to ISO/IEC 42001
- BRF to EU AI Act obligations
- BRF to specialist-underwriter evidence expectations

Without those crosswalks, BRF remains stronger for people already persuaded by the architecture-first frame than for buyers who need translation into existing governance language.

### 6.6 Missing visibility inside the OECD ecosystem

If the OECD catalogue is where many practitioners first look for trustworthy-AI tools, then BRF itself should probably be discoverable there as:

- a procedural rating framework
- a governance / audit tool
- a machine-readable attestation format with worked examples

This is not a theoretical gap. It is a distribution gap.

---

## 7. Prioritised action list

The list below is the practical output of this assessment.

### P0 — immediate, highest leverage

1. **Publish this OECD assessment note.**
   Done in this file. Purpose: stop the repeated "does OECD already cover this?" question before it starts.

2. **Add an external-tools mapping annex.**
   New artefact to produce next:
   - external tool
   - evidence type produced
   - BRF axis / invariant / modifier supported
   - admissibility caveats

3. **Make OECD context visible from the README.**
   Readers unfamiliar with the OECD work should find this note from the front page.

### P1 — next companion artefacts

4. **Build a BRF benchmark and test harness companion repo.**
   Suggested shape:
   - OpenEnv-style environment abstraction for realistic agent workflows
   - runner manifest per invariant and per archetype
   - signed result bundle output suitable for BR attestation attachment

5. **Build questionnaire-to-profile conversion tooling.**
   Input:
   - structured answers to `framework.md §17`
   Output:
   - draft `br-profile.schema.json` payload
   - unresolved evidence requests
   - warnings where answers are inconsistent

6. **Define BRF component cards.**
   Minimum card types:
   - model card
   - dataset / corpus card
   - tool / integration card
   - dependency attestation card

### P2 — translation and market adoption

7. **Publish regulatory and assurance crosswalks.**
   Priority order:
   - NIST AI RMF
   - ISO/IEC 42001
   - EU AI Act
   - specialist-underwriter published criteria

8. **Publish benchmark archetype profiles.**
   The repo already names this as open work. Candidate archetypes:
   - customer-support copilot
   - code assistant
   - RAG workflow
   - research agent
   - clinical triage assistant
   - payments / financial operations agent

9. **Publish evidence-tier calibration guidance.**
   Even before full numeric `R` calibration ships, readers need a usable directional guide for what counts as minimal, moderate, and forensic evidence in BRF terms.

### P3 — ecosystem visibility

10. **Submit BRF to the OECD catalogue.**
    Candidate submission shape:
    - procedural tool / rating framework
    - governance and compliance
    - risk management
    - audit / attestation

11. **Submit a BRF worked example as an OECD use case.**
    The Lane2 self-assessment is the obvious first candidate once positioning is final.

---

## 8. Bottom line

The OECD catalogue is useful to BRF in exactly the right way:

- not as a replacement
- not as a refutation
- but as a source of **supporting tools, documentation patterns, and ecosystem visibility**

The correct interpretation is:

- **BRF remains the architecture-first system-level classifier**
- **OECD supplies adjacent tools and public reference points**
- **the work now is to bridge them**

If BRF wants to be maximally useful to deployers, auditors, underwriters, and regulators, the next step is not to weaken the framework into a generic trustworthiness catalogue. The next step is to make BRF better at **absorbing evidence produced by the surrounding tool ecosystem** and better at **showing up where that ecosystem already gathers**.
