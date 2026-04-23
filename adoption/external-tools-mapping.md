# External Tools Mapping

*Evidence adapters for using adjacent tools and metrics in support of a Blast Radius Framework profile or attestation.*

**Purpose:** turn "interesting adjacent tool" into "usable BRF evidence with stated limits"
**Status:** initial mapping
**Date:** 2026-04-23

---

## 1. How to use this annex

This annex answers a narrow question:

> If I have output from an external tool or metric family, what BRF claim can it support?

It does **not** mean:

- the tool determines the BR class
- the tool replaces invariant testing
- the tool can be cited without review

Every mapping below must be read with the same discipline:

1. identify the exact BRF claim being supported
2. identify whether the tool output is direct evidence or only a supporting signal
3. identify what additional attested evidence is still required

---

## 2. Admissibility scale

This annex uses four evidence roles:

| Role | Meaning |
|---|---|
| **Primary** | Can directly support a BRF claim if run and retained under controlled conditions |
| **Supporting** | Useful evidence, but not enough on its own |
| **Triage** | Helps decide where to investigate, but not suitable as attestation evidence by itself |
| **Context only** | Useful for narrative explanation or packaging, not for claim support |

---

## 3. Tool-to-BRF mapping

| Tool / family | Typical output | BRF area supported | Evidence role | What it can support | What it cannot support alone |
|---|---|---|---|---|---|
| [OpenEnv](https://oecd.ai/en/catalogue/tools/openenv) | task runs against realistic agent environments; success/failure traces; tool-call behavior under constraints | `A`, `R`, `V`, `O`; Invariants 1, 4, 6, 7; `tau` | Primary / Supporting | action-class ceiling checks; recovery behavior; trace completeness; coupling behavior in realistic workflows | whole-system BR class; actuarial calibration; attestation signature / anchor claims |
| [PyRIT](https://oecd.ai/en/catalogue/tools/pyrit) | automated red-team prompts, attack attempts, policy failure traces | `delta_adv`; parts of `K`, `O`; anti-pattern confirmation | Supporting | prompt-injection exposure; data exfiltration attempts; misuse susceptibility; regression tracking after control changes | bounded-coupling proof; reversibility proof; jurisdictional claims |
| [garak](https://oecd.ai/en/catalogue/tools/garak%2C-llm-vulnerability-scanner) | vulnerability scan outputs across jailbreak, leakage, hallucination, prompt-injection families | `delta_adv`; anti-patterns A10, A12, A15; parts of `O` | Supporting | attack-surface characterisation and comparison over time | any architectural invariant on its own; evidence binding; deterministic execution |
| Model Cards | structured model documentation | component-card layer; parts of `A`, `K`, `delta_adv` | Supporting | model identity, intended use, limitations, known failure modes, update cadence | system topology; composition mathematics; runtime evidence claims |
| Datasheets for Datasets | dataset provenance, collection, consent, limitations | `K3-P`; `K4-F`; jurisdictional and data-governance narratives | Supporting | dataset provenance and deletion constraints; population scope; corpus assumptions | runtime tenant isolation; action ceilings; evidence integrity |
| IBM Factsheets / similar governance factsheets | asset lineage, versioning, governance metadata | `O`; Invariants 2 and 3; change-management narratives | Supporting | version lineage, policy-snapshot explanation, accountability metadata | independent anchor proof; hash-chain verification |
| NIST AI RMF artefacts | risk register, control narratives, process evidence | translation layer; governance crosswalk | Context only / Supporting | board and audit translation of BRF findings into a known process frame | BRF class computation; invariant satisfaction |
| AIIRS | inherent-risk triage score or class | upstream intake and scoping | Triage | deciding whether a human-directed GenAI use case needs BRF follow-on analysis | agentic blast-radius rating |
| Privacy metrics families | leakage counts, anonymisation statistics, re-identification risk | `K3-P`; `delta_adv` | Supporting | magnitude and nature of privacy exposure in a component or corpus | whole-system consequence class without population and topology context |
| Fairness metrics families | disparity measures, error-rate differences | `K4-F`; parts of `K3-L` | Supporting | differential-impact concerns where the system affects people | operational propagation, reversibility, or composition |
| Robustness metrics families | adversarial success rates, perturbation sensitivity | `delta_adv`; parts of `O` and `tau` | Supporting | comparative hardening claims and change regression | bounded authority or external reach claims |
| Drift / anomaly metrics | divergence measures, alert frequencies, baseline deviations | `O`; `tau`; parts of Invariant 6 | Supporting | real-time monitoring maturity and stability trend | architectural enforcement claims without runtime boundary checks |

---

## 4. Mapping by BRF claim type

### 4.1 Axis support

| BRF axis / modifier | Best adjacent evidence families | Notes |
|---|---|---|
| `A` authority | OpenEnv scenario runs; tool / integration cards | Requires declared tool ceilings and policy enforcement evidence, not just test outcomes |
| `R` reach | OpenEnv environment topology; dependency cards; system inventory | Reach claims must still be tied to actual systems and principal populations |
| `C` coupling | OpenEnv multi-component runs; architecture diagrams; dependency cards | No external scanner can substitute for naming the actual coupling regime |
| `V` reversibility | OpenEnv rollback scenarios; replay logs; exercised rollback evidence | Reversibility claims require exercised recovery, not stated plans alone |
| `K` consequence | population and domain analysis; privacy/fairness metrics; regulatory mapping | Metrics can inform severity, but domain context still sets consequence tier |
| `O` observability | drift metrics; factsheets; trace bundles; evidence-layer design | O4 claims still require runtime-checkable invariant boundaries |
| `delta_adv` | PyRIT; garak; robustness metrics | Good supporting evidence, but only inside a defined threat model |
| `tau` | drift metrics; repeated benchmark runs; release-over-release regression tracking | Best treated as longitudinal evidence, not single-run snapshots |

### 4.2 Invariant support

| Invariant | Adjacent tools that can help | Still required beyond the tool |
|---|---|---|
| I1 deterministic execution | controlled benchmark reruns; replay harnesses | canonical serialisation, fixed policy snapshot, reproducibility checks in your own system |
| I2 evidence binding | governance factsheets can document lineage | cryptographic signatures, hash chains, and external anchors remain mandatory |
| I3 policy snapshot coherence | factsheets, version registries, config lineage systems | immutable snapshot IDs and retrieval proof in the system under audit |
| I4 bounded blast radius | OpenEnv fault-injection and tenant-isolation runs | actual architectural containment boundaries |
| I5 jurisdictional / policy boundary integrity | dataset cards, dependency cards, policy metadata | enforceable routing and boundary controls, not just declarations |
| I6 observability and replay | benchmark traces, drift metrics, event logs | preserved, replayable, audit-admissible traces |
| I7 bounded coupling | OpenEnv multi-agent scenarios | typed interfaces and closed-world constraints; no external tool can rescue open-world NL coupling |

### 4.3 Anti-pattern support

Some adjacent tools are especially useful for evidencing or falsifying anti-pattern claims:

| Anti-pattern area | Helpful tools |
|---|---|
| prompt injection and untrusted tool-output flow | PyRIT, garak |
| long-context abuse and deep-research drift | garak, drift metrics, repeated benchmark runs |
| ungoverned memory and data contamination | dataset cards, lineage factsheets, deletion verification evidence |
| autonomy slider / approval fatigue | oversight-quality analytics, decision-review metrics, Judgment Assurance-style methods |
| marketplace / plugin / MCP sprawl | dependency cards, asset inventory, reach inventory, attested source metadata |

---

## 5. Minimum evidence packet pattern

When an external tool is used to support a BRF claim, the evidence packet should include:

1. tool identity and version
2. run date and operator
3. target system version and policy snapshot
4. scenario or metric definition
5. raw outputs or verifiable result bundle
6. interpretation statement tying the output to a specific BRF claim
7. limits statement saying what the tool output does **not** prove

Without items 6 and 7, external evidence is easily over-claimed.

---

## 6. Recommended first integrations

If BRF adopts only a few adjacent tools first, the highest-value sequence is:

1. **OpenEnv-style benchmark environments** for realistic workflow evidence
2. **PyRIT and garak** for `delta_adv` and prompt-surface evidence
3. **Model Cards / Datasheets / dependency cards** for component-documentation discipline

This sequence matches the practical needs of BRF adopters:

- generate evidence
- test adversarial surfaces
- document the components being rated

---

## 7. Bottom line

The correct relationship is:

- adjacent tools generate evidence
- BRF interprets that evidence in system-architecture terms
- the attestation records the claim and its verification form

The tool does not become the framework. The framework becomes easier to use because the tool has a clearly defined place inside it.
