# External Market and Project Review

**Reviewed:** 2026-10-26
**Repository baseline:** `f526690` (2026-04-30); public `main` matched this commit when checked.
**Status:** Research review and proposed update backlog. Existing framework rules and ratings have not been revised by this note.

## Assessment

BRF's six axes remain a useful way to describe the operational exposure of an agent deployment. Recent work gives us more concrete controls and evidence formats to map onto those axes. It also challenges several absolute claims in the April text.

The most useful next release would combine narrower, better-supported claims with one working evidence integration. More overview documents alone will not close the implementation gaps.

This review covers public primary sources for agent identity, protocols, runtime enforcement, evaluations, insurance, and EU legislation. It distinguishes work published since April from relevant work that already existed but was missing from our earlier assessment. Product descriptions establish what providers claim to offer; they do not establish independent effectiveness or coverage for a particular deployment.

## 1. Findings Requiring Attention

### P1: Insurance conclusions exceed the available evidence

[`framework.md`](../framework.md) sections 5.3 and 14 describe systems failing I1/I2 as structurally unpriceable. The [chatty-card executive summary](../reports/chatty-card-a2a/chatty-card-a2a-exec-summary.md) goes further and says matching deployments cannot obtain specialist cover. A BR classification cannot establish an insurer's decision or policy coverage.

AIUC announced insured ElevenLabs voice agents in February 2026, before our original assessment. HSB announced AI liability cover in March. Armilla now explicitly describes agent mistakes, and Munich Re describes aiSure distribution through Mosaic. These are different products, with different triggers and underwriting approaches. Their public descriptions do not establish that the insured systems meet BRF's determinism requirements. [AIUC announcement](https://aiuc.com/updates/elevenlabs-secures-first-of-its-kind-ai-agent-insurance), [HSB announcement](https://www.munichre.com/hsb/en/press-and-publications/press-releases/2026/2026-03-18-introducing-ai-liability-insurance-for-small-businesses.html), [Armilla](https://www.armilla.ai/), [Munich Re](https://www.munichre.com/en/solutions/for-industry-clients/insure-ai.item-42c4fe9ea6b591f569548792d2c96201.html).

**Recommended change:** distinguish architectural exposure, evidence readiness, and actual insurance outcomes. Record the insurer, product, insured scope, jurisdiction, exclusions, limits, and review date when coverage is known. Use "coverage not established" where it is unknown. Retain BR-5 as a BRF risk class without making it a market-wide insurance verdict.

The proposed Kalman score also needs a qualification. Uncertainty in a weighted compliance index is not automatically uncertainty in an insured loss distribution. The repo itself lists weights, observation noise, and process noise as uncalibrated. Treat the score as experimental until validation connects it to measured outcomes; an asserted identity with actuarial uncertainty does not supply that validation.

### P1: Protocol names are being used as substitutes for deployment evidence

[`antipatterns.md`](../antipatterns.md) A1 says A2A peers grant execution to any reachable caller and force reach upward. The actual A2A specification describes server authentication and authorization, structured data, signed cards, and authenticated extended cards. Our April chatty-card report already acknowledges this distinction, but the main catalogue has not caught up. [A2A specification, sections 4, 7, 8 and 13](https://a2a-protocol.org/latest/specification/).

MCP's checked authorization page resolves to the **2026-07-28** specification. It describes resource-server roles, resource metadata, scopes, and audience controls; its security guidance addresses confused deputies, token passthrough, SSRF, and local server compromise. Authorization is optional overall, with transport-specific guidance. Adoption of the protocol therefore establishes neither safety nor the absence of controls. [MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [MCP security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices).

**Recommended change:** name the failure mechanism: unrestricted credentials, unmediated delegation, untrusted output controlling execution, missing tenant checks, or undisclosed dependencies. Assess the deployed authorization and execution path. A public discovery document exposes information; that fact alone does not establish execution authority.

For versioned reviews, retain the protocol revision and implementation commit. The A2A `latest` URL is a moving reference and should be pinned when an assessment is issued.

### P1: Model behaviour, execution bounds, and audit reconstruction need separate treatment

The README's claim that architecture determines operational risk independently of model capability is too broad. Architecture establishes reachable effects and containment, while model behaviour influences which actions are attempted and how often controls are challenged. Anthropic's September incident assessment reports both evaluation-environment misconfiguration and model-dependent behaviour. It supports testing both layers. [Anthropic assessment, 2026-09-09, corrected 2026-09-10](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents).

I1-T2 also requires a pinned sampling seed and requires replay to fail when that seed is removed. A deterministic policy engine can remain reproducible without an LLM seed. Conversely, a seed does not guarantee model reproducibility across environments. PyTorch documents platform and release limits even with identical seeds. [Current test](../spec/invariant-conformance-tests.md), [PyTorch reproducibility guidance](https://docs.pytorch.org/docs/2.14/notes/randomness.html).

**Recommended change:** distinguish model resampling, replay of captured observations, deterministic policy decisions, and reconstruction of external side effects. Test the safety-critical execution boundary using fixed policy and recorded model/tool results. Test model variability separately with repeated trials. Canonical hashing establishes stable encoding; it does not establish deterministic behaviour or that a recorded event happened.

### P1: The worldview gate and composition mathematics need a validation programme

[`framework.md`](../framework.md) sections 4.0 and 7 currently turn any natural-language input into an unconditional BR-4 floor and a T2 classification. This conflates the reasoning input with the authority of that input over external actions. An agent can read arbitrary prose while an independent tool gateway enforces a finite action set, tenant boundaries, budgets, and network destinations.

That architecture still needs adversarial testing. It is nevertheless a counterexample candidate the framework must be able to examine. A typed JSON envelope can also carry arbitrary instructions, so checking the wire format alone is insufficient.

The local [chatty-card report](../reports/chatty-card-a2a/chatty-card-a2a-technical-findings.md) and the checked [companion case study](https://github.com/kevin-biot/governance-failure-patterns/tree/main/case-studies/chatty-card-a2a-substrate-harm) describe a particular transactional apparatus; the canonical-protocol comparison remains pending in the public case study. Its raw research artefacts are described as private. Those boundaries limit independent reproduction and generalisation.

**Recommended change:** compare unrestricted prose delegation with the same workload behind independently enforced execution limits. Specify the loss metric, exposure period, shared dependencies, and assumptions behind each composition equation. In particular, max-bounded aggregate loss, products of bypass probabilities, and voting reductions require different assumptions. Keep existing floors labelled as conservative BRF policy until counterexample tests and calibration justify revisions.

### P2: Adoption completion and validation claims need correction

[`gap-closure-plan.md`](./gap-closure-plan.md) marks all six gaps completed while the reference harness and converter are design notes and OECD visibility is a plan. Component cards and initial crosswalks do exist. No public submission or deployed adapter was verified in this review.

The current validator passed both example profiles, both assessment profiles, and the example component card. Two additional checks exposed gaps:

- The example card references `example-closed-world-br2`, while the actual profile ID is `example-br2-closed-world-001`.
- An in-memory card with `last_reviewed_at: "not-a-date"` still passed the current validator, which does not enable a format checker.

There are also substantive spec inconsistencies: the EU crosswalk and evidence mapping call I6 observability/replay, while I6 is **fail-closed execution control**. The attestation document labels `RS256` as RSA-PSS and gives differing treatments of `signature_value` when signing and verifying. These need correction before claiming interoperable attestation verification.

**Recommended change:** track guidance delivered, implementation delivered, tested integration, and external adoption separately. Add schema self-validation, supported format checks, cross-document references, semantic checks, and negative fixtures. Cryptographic verification and independent review remain additional steps.

## 2. External Work to Connect To

| Project or market | What was verified | Useful BRF update |
|---|---|---|
| OWASP Agent Control Standard (ACS) | September announcement; release `v0.1.4` published 2026-10-16; schemas, hooks, and a reference implementation | Map enforceable dispositions and failure behaviour into A, O, I3 and I6; add an ACS evidence adapter |
| NIST agent initiative and NCCoE identity work | February initiative; September comment-summary announcement and planned DevSecOps implementation use case | Extend the NIST crosswalk beyond AI RMF to agent identity and authorization evidence |
| IETF WIMSE AIMS | `draft-ietf-wimse-aims-00`, dated 2026-09-15, an active WG Internet-Draft | Add delegation, credential lifetime, revocation, and cross-service correlation to component cards |
| MCP and A2A | Published security and authorization mechanisms, with deployment-specific enforcement | Replace protocol-wide conclusions with versioned control assessments |
| OpenTelemetry GenAI conventions | Conventions cover GenAI and MCP; the former agent-spans page now redirects readers to a dedicated repository | Map trace/session/tool identifiers to BR evidence; retain policy and integrity checks beyond ordinary telemetry |
| Inspect and AgentDojo | Inspect supports agent tasks, sandboxes and logs; AgentDojo supplies an extensible adversarial environment | Implement a thin BRF result exporter using existing evaluation infrastructure |
| OECD OpenEnv entry | Entry remains available and describes environment APIs and agent evaluations | Retain it as discovery material; verify implementation capabilities and versions at the upstream project |
| Specialist insurance | Distinct agent liability, model performance, and assurance-backed offerings | Record actual product scope and underwriting evidence without inferring cover from a BR class |
| EU AI Act implementation | July amending Regulation and current Commission implementation material | Refresh the legal crosswalk's version, applicability dates and role-specific evidence mapping |

### ACS is the closest practical integration

ACS now occupies part of the runtime-control territory our April positioning treated as largely uncovered. It defines pre-action decisions, observability, and inventory interfaces. Its release is an implementation opportunity and an adjacent standard to assess. [OWASP announcement](https://genai.owasp.org/resource/agent-control-standard-acs/), [release v0.1.4](https://github.com/GenAI-Security-Project/agent-control-standard/releases/tag/v0.1.4).

The checked README at commit `4cf23d4cce832e522ffab69e7dd8d7209ec11a9a` explicitly reports a fail-open default, missing wire authentication in its reference Guardian, and limited live hook coverage. These are the authors' disclosures, not findings from running that implementation here. They show why a standard's specification and a particular deployment need separate BRF evidence. [Pinned ACS README](https://github.com/GenAI-Security-Project/agent-control-standard/blob/4cf23d4cce832e522ffab69e7dd8d7209ec11a9a/README.md).

A useful first integration would record the proposed action, policy revision, decision, actual tool outcome, and failure disposition. Exercise an allowed call, a denied call, and an unreachable policy service. Verify that a denial actually prevents execution and that alternative execution paths cannot bypass the hook. Emit an evidence bundle; keep any preliminary rating separate from unrun tests.

### Identity standards sharpen the authority distinction

NIST's programme has progressed beyond its original consultation. The September announcement identifies DevSecOps as its first implementation use case; this is ongoing standards work rather than evidence of a completed universal agent standard. [NIST September update](https://www.nist.gov/news-events/news/2026/09/comments-software-and-agentic-ai-identity-concept-paper).

WIMSE AIMS composes existing identity and OAuth mechanisms and discusses authorization context, revocation signals, and audit correlation. It remains a draft. Its acronym means Agent Identity Management System, distinct from the AI management system terminology in ISO/IEC 42001. [AIMS draft-00](https://datatracker.ietf.org/doc/html/draft-ietf-wimse-aims-00).

BRF should record three separate facts: the organisational mandate supplied by its issuer; the technical delegation accepted by services; and the action limits actually enforced. Runtime verification can establish bindings, scope, expiry, and enforcement outcomes under stated trust assumptions. It cannot independently establish the legal validity of a corporate mandate.

### Reuse the evaluation and telemetry infrastructure

Inspect already provides agent evaluation building blocks and sandbox support. AgentDojo predates our April work and offers tasks, attacks, and defences for tool-using agents. Its absence from the earlier mapping was a coverage gap, rather than a recent market change. OpenEnv remains useful for environments. [Inspect](https://inspect.aisi.org.uk/), [Inspect sandboxing](https://inspect.aisi.org.uk/sandboxing.html), [AgentDojo paper record](https://www.research-collection.ethz.ch/items/21acec58-727b-46a8-9570-3ec6815ac9f1), [OECD OpenEnv entry](https://oecd.ai/en/catalogue/tools/openenv).

Prefer BRF scenarios, acceptance criteria, and result exports on those tools over building another general evaluation engine. Retain both task success and harmful-action outcomes, trial counts, model and scaffold versions, policy snapshots, and confidence intervals. Benchmark scores describe their tested conditions; they cannot certify an untested production boundary.

OpenTelemetry's GenAI material has moved to a dedicated conventions repository. A BRF adapter should pin its upstream version and extend traces with policy and evidence bindings. An ordinary span is not an independent attestation. Minimise captured sensitive content and specify retention. [Conventions repository](https://github.com/open-telemetry/semantic-conventions-genai).

### The EU legal snapshot needs updating

The April crosswalk cites the original 2024 Regulation. The published Digital Omnibus amendment, Regulation (EU) 2026/1744, changes the implementation timetable. Current Commission material gives **2 December 2027** for the relevant Annex III high-risk rules and **2 August 2028** for the relevant Annex I product rules. These are specific high-risk dates; other provisions have different application dates. [Amending Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601744), [Commission enforcement timeline](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act).

Refresh each affected article against the amended text and record legal role, use category, applicable provision, date, and evidence needed. Keep BR class and legal classification distinct. The Commission pages and indexed Official Journal text were readable during this review; direct EUR-Lex opens encountered an anti-bot page, so an operative article-by-article redline remains a follow-up task.

## 3. Proposed Update Backlog

**Execution update:** this table preserves the review's original recommendations. Implementation and outstanding exit conditions are now tracked in the [October update worklist](./update-worklist-2026-10.md); the findings above describe the pre-update snapshot, not the repaired validator.

All items below are **open recommendations**. Completing this review does not complete them.

| ID | Priority | Task | Completion evidence |
|---|---|---|---|
| R01 | P0 | Audit insurer, legal, and quantitative claims across framework, companions, and assessments | Each material claim is sourced, qualified, or identified as a hypothesis; assessment corrections are recorded |
| R02 | P0 | Refresh the EU crosswalk against the amended Act | Role/article/date matrix with amendment provenance; affected assessment statements reviewed |
| R03 | P0 | Correct A1/A3/A8 protocol descriptions and deployment assumptions | Current protocol references plus contrasting constrained and unconstrained deployment examples |
| R04 | P0 | Repair validator, card links, I6 mappings, and attestation ambiguity | Invalid formats and dangling links fail; test vectors verify one unambiguous signing procedure |
| R05 | P1 | Revise I1 around the declared execution boundary | Separate captured replay, policy determinism, model variability and side-effect reconstruction tests |
| R06 | P1 | Evaluate the worldview gate and composition equations | A documented counterexample suite; assumptions and calibration data for each mathematical claim |
| R07 | P1 | Publish an ACS control/evidence mapping and run a small adapter | Version-pinned allow/deny/outage runs with actual outcomes and unresolved claims visible |
| R08 | P1 | Extend component cards for identity and delegation | Principal/agent bindings, audience, scope, expiry, revocation and policy references in examples |
| R09 | P1 | Add Inspect/AgentDojo results and an OpenTelemetry mapping | One repeatable scenario and schema-valid result bundle with provenance and statistical limits |
| R10 | P1 | Test asynchronous and indirect effects | Cancellation/revocation latency, in-flight calls, retries, idempotency, budgets, memory, egress and shared-resource effects |
| R11 | P2 | Reconcile the adoption ledger and public release state | Plans and implementations have separate statuses; framework/spec revisions and review dates agree |
| R12 | P2 | Prepare an OECD submission and an independent assessment exercise | Submission receipt or listing, plus independently reproduced results and disclosed disagreements |

Suggested sequence: R01-R04 establish a credible publication baseline. R05-R06 are framework-version work because they affect definitions and ratings. R07-R10 provide useful implementation evidence, with revised definitions recorded explicitly where needed. R11-R12 make progress and adoption visible.

For R10, use the existing six axes first. Memory and connector supply chains affect C and O; delegated credentials affect A and R; data exfiltration affects V and K even through read-only tools. A seventh axis should need evidence of a dimension the existing model cannot express.

## 4. Verification and Limits of This Review

The existing local validator accepted four profiles and one component card. Its schema-only success did not detect the broken card/profile relationship or invalid date described above. No external runtime, insurer underwriting process, or production deployment was executed or independently audited.

The untracked DAREB comparison note was left untouched. This review does not adopt its earlier characterisation of DAREB as a runtime-risk claim: the supplied DAREB text describes a case-level evidential test, so any comparison should respect that stated scope.

There is no evidence here that the six axes need replacing. The case for updating the surrounding claims, tests, integrations, and adoption status is considerably stronger. A practical next milestone is a small, independently repeatable BRF assessment over an existing control implementation.
