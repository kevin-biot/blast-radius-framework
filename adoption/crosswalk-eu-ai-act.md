# BRF Crosswalk to the EU AI Act

*Architecture-and-evidence mapping, not a legal classification or compliance opinion.*

**Status:** Reviewed translation; deployment-specific legal review still required
**Reviewed:** 2026-10-26; supersedes the 2026-04-23 crosswalk
**Legal baseline:** Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744

## 1. Sources and application dates

Use the [Official Journal amendment, Article 1(40)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1744) together with the [27 July 2026 consolidated text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R1689-20260727). Consolidation is a documentary aid, not a replacement for the legal acts. The amendment entered into force on 27 July 2026.

Amended Article 113(c) schedules Chapter III, Sections 1-3, except Article 6(5), for **2 December 2027** for Article 6(2)/Annex III systems and **2 August 2028** for Article 6(1)/Annex I systems. It is not a blanket postponement of the Act. The [Commission implementation timeline](https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline) distinguishes provisions already applicable, including transparency rules from 2 August 2026, and transitions for existing systems.

Record the legal role, intended purpose, classification rationale, applicable article and application/transition date for each deployment. Check Article 2 scope, Article 111 transitions, Article 113 and sector legislation rather than assigning one date to the whole evidence packet. **Article 72 is in Chapter IX**, not the Chapter III sections postponed by Article 113(c); obtain a role- and system-specific interpretation of its application rather than copying the dates above.

Source-access limit: this review checked official indexed passages, amendment provisions and Commission guidance. Direct EUR-Lex retrieval intermittently returned an anti-bot page. This is not a certified full-text redline or exhaustive check of every amended provision.

## 2. Role and evidence crosswalk

The legal-subject column below is a short orientation to the [Act's provisions](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=OJ%3AL_202401689), read with the amendment. The BRF mapping and missing-evidence columns are our assessment, not EU endorsement.

| Article / legal subject | BRF evidence that can help | What BRF does not establish |
|---|---|---|
| 9: high-risk risk management | Threat model, inherent/residual profile, failure and abuse tests | Complete lifecycle risk management or acceptable residual risk |
| 12: automatic logging capability | O-axis evidence; I2/I3 event and policy binding | Required log coverage, retention or access controls simply by signing a profile |
| 13: provider information and instructions | Component cards, capabilities, limits, tested configuration | Complete instructions for use or their accuracy |
| 14: human oversight | Approval bypass, intervention latency and stop-path tests | Oversight staff competence, organisational authority or effective staffing |
| 15: accuracy, robustness and cybersecurity | Containment, adversarial and deployment-specific outcome tests | Model quality, cybersecurity or lifecycle compliance from a BR class |
| 19: provider log retention | Retention configuration, retrieval and deletion tests | That logs are actually retained under the provider's control |
| 26: deployer duties | Observed use constraints, oversight paths, log retrieval | Organisational compliance or a valid mandate to act |
| 27: FRIA for specified deployers/use cases | Affected populations, consequence pathways and mitigation evidence | The statutory assessment, consultation or notification |
| 72: provider post-market monitoring | Versioned incidents, changes, trajectory reviews and re-attestation triggers | A complete monitoring system or continuous compliance |

Article 19(1) and [Article 26(6)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R1689-20260727) concern provider and deployer logs respectively: under their control, an appropriate period of at least six months, subject to other applicable law. **Article 26(6) is not a generic authority-access provision.** Article 12 is the system's logging capability, not a substitute retention policy.

Amended Article 72(3) retains a documented monitoring plan and calls for Commission guidance including a template by 2 September 2027. Do not describe the former harmonised-template mandate as the current requirement. See [amendment Article 1(30)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1744).

## 3. Runtime and external authority are different evidence

A runtime can demonstrate that a presented identity, delegated scope, policy version and action request passed a particular technical check. It cannot establish that a company validly appointed the principal, that a person had a legal mandate, or that a business policy correctly interprets the law. Record those external sources and their accountable owners separately.

In particular, **I6 means fail-closed execution control**, not drift detection or a legal-authority check. A denial trace supports a tested execution boundary. It does not prove every route to the protected tool is mediated or that the organisation was entitled to grant the permission.

## 4. Minimum deployment packet

1. Legal-role and applicability record, owned by the organisation's responsible legal/compliance function.
2. Versioned deployment graph, BR tuple, worldview declaration and explicit rating assumptions.
3. Test evidence for reachable effects, denied actions, outages, oversight intervention, revocation, retries and rollback.
4. Logging/retention/access evidence with policy IDs and affected-data limits.
5. Component cards and signed profile, with independent verification of signatures and anchors where claimed.
6. Unresolved findings, monitoring owner, review date and material-change triggers.

A low BR class, a narrow runtime permission or a valid signature does not establish legal compliance. A high BR class does not itself prohibit deployment. Insurance coverage is a separate contract-specific decision under the [claims and evidence policy](./claims-and-evidence.md).
