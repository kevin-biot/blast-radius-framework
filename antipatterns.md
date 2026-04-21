# Blast-Radius Anti-Pattern Catalogue

*A negative reference for the classification framework*

**Version:** 0.1
**Status:** Research draft
**Date:** 2026-04-21
**Companion to:**
- [framework.md](./framework.md) (rating framework, v0.5)
- [manifesto.md](./manifesto.md) (the argument)
- [insurability.md](./insurability.md) (actuarial companion)
- [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md) (credits — Gagne's multi-agent drift corpus, prior published work, private reference implementation)

---

## 1. Purpose

The framework names axes. The positive reference shows what architectural enforcement looks like. This catalogue is the negative reference: **named anti-patterns currently shipping as "progress" that expand blast radius by design.**

Most of these are vendor-promoted and marketed. A CISO, purchasing manager, or risk function reading a vendor pitch should be able to recognise the anti-pattern by name and compute the BR damage without re-derivation.

Two parts:

- **Part A — architectural anti-patterns** (A2A, MCP ecosystem, etc.) that expand A/R/C/V/K.
- **Part B — evidence-chain anti-patterns** that fail EU AI Act, GDPR, and general audit expectations regardless of how well the A/R/C/V/K axes are designed.

The catalogue deliberately crosses boundaries the industry keeps separate (architecture vs compliance vs security) because the underlying blast-radius test does not respect those boundaries.

## 2. How to read each entry

```
Name              — commonly used term
Mechanism         — how blast radius expands
Axis damage       — A/R/C/V/K/O deltas; δ_adv implication
Typical BR        — class produced when the pattern is adopted naively
Demotion path     — what architectural change brings it back to a defensible class
Regulatory risk   — EU AI Act, GDPR, sector-specific where applicable
```

All axis codes refer to the v0.2 framework: **A** authority, **R** reach, **C** coupling (with C4a NL-coupled peers / C4b shared-state), **V** reversibility, **K** consequence, **O** observability, **δ_adv** adversarial modifier.

---

## Part A — Architectural anti-patterns

### A1. A2A (agent-to-agent protocol with public capability discovery)

**Mechanism.** Agents publish AgentCards advertising their tools and capabilities to peers. Discovery is the design goal. NL is the interaction medium.

**Axis damage.** Maxes A (each peer grants execution authority to any caller that can reach it). Forces R3+ by construction. Creates **C4a as the default** (NL-coupled peers — the regime where Sentinel shows collapse inside 15 turns). AgentCard is a δ_adv enumeration surface; an attacker who discovers an AgentCard knows exactly what to prompt-inject for.

**Typical BR.** BR-4 before any specific tool is wired; BR-5 when composed with write-capable backends.

**Demotion path.** Typed, signed capability requests with broker mediation (aARP-style). Remove NL from the peer-to-peer channel. Make capability discovery authenticated and per-principal, not public.

**Regulatory risk.** EU AI Act Article 14 (human oversight) — AgentCard-discovered capabilities can be invoked without human confirmation; Article 15 (cybersecurity) — public capability discovery is a threat surface.

### A2. "API-agent-ready" / API-first tool exposure

**Mechanism.** Vendor sales narrative: expose every enterprise API endpoint as an LLM-callable tool. "More tools = more capable agent."

**Axis damage.** Maxes A (write APIs become A3/A4), maxes R (every system touched), zero C-axis review. Least-privilege is architecturally unreachable from this starting point because the pitch treats surface as feature.

**Typical BR.** BR-4 to BR-5 depending on write-API presence.

**Demotion path.** Action-class taxonomy with per-API ceiling; session-execution attestation gates on constrained-proposal and bounded-execution classes; mandatory parameter constraints. Refuse to onboard a tool without a declared ceiling.

**Regulatory risk.** EU AI Act Article 13 (transparency) — if users don't know which APIs the agent can hit, transparency obligation fails.

### A3. MCP server ecosystem without composition rule

**Mechanism.** Model Context Protocol itself is neutral. The *ecosystem* is the risk: each MCP server is a trust boundary nobody audits, "install this MCP server to give Claude Desktop access to X" pattern becomes the default integration.

**Axis damage.** A3/A4 trivially reached through any write-capable server. C-axis expands per server installed, composed ad-hoc. O collapses because MCP server internals are opaque. δ_adv unbounded — server authors could be anyone.

**Typical BR.** BR-3 per server; aggregate rapidly reaches BR-5 as servers compose.

**Demotion path.** Formal composition rule (v0.2 §7): each MCP server rated before install; δ_adv analysed; observability requirement on the server-side tool path. MCP servers from unrated sources refused by policy.

**Regulatory risk.** GDPR (data leaving governance boundary through ungoverned MCP server); EU AI Act Article 15 (supply chain integrity).

### A4. Agent marketplaces / plugin stores

**Mechanism.** Install agents from a store. GPT Store, plugin ecosystems. Supply chain trust is transitive: you trust the marketplace, which reviewed the agent. You inherit the marketplace's review quality.

**Axis damage.** Entire A/R/C/V/K/O profile inherited from the marketplace listing — which typically doesn't rate on these axes at all. δ_adv unbounded (malicious agents), and τ (trajectory) drifts with every update pushed by the agent author.

**Typical BR.** Unknown by construction. Operationally BR-3+; the honest rating is *unrateable*.

**Demotion path.** Treat the marketplace as an external composition (v0.2 §7); require the marketplace to publish A–R–C–V–K–O profiles per listing; refuse install of unrated listings.

**Regulatory risk.** EU AI Act provider vs deployer obligations — marketplace behaviour blurs who's the provider.

### A5. Auto-tool-generation from OpenAPI/GraphQL specs

**Mechanism.** Frameworks that read your OpenAPI/GraphQL schema and auto-emit a tool per endpoint. "Zero-config agent onboarding."

**Axis damage.** Every endpoint becomes a tool without per-tool review. A maxed. K sub-tag unset (no per-endpoint consequence analysis). δ_adv unanalysed per tool.

**Typical BR.** BR-3 to BR-4 depending on the API's write surface.

**Demotion path.** Mandatory per-tool allowlist; explicit ceiling per endpoint; param-constraint declaration before exposure.

**Regulatory risk.** EU AI Act Article 9 (risk management) — auto-generation short-circuits the per-risk assessment the Article expects.

### A6. CrewAI / AutoGen / LangGraph default pattern

**Mechanism.** Persona prompts ("You are a wise X agent") plus NL context exchange between peers. The mass-market tutorial default.

**Axis damage.** C4a by construction. No A-axis ceiling. R unbounded (agents can be given any tool). The phase transition Sentinel identifies in the C4a regime is reached within typical baseline-establishment windows (<15 turns).

**Typical BR.** BR-4 even with bounded tools; BR-5 with write tools. Collapse inside 15 turns makes runtime monitoring structurally incapable of catching it.

**Demotion path.** Replace NL peer coupling with typed routed requests (aARP-style); remove persona prompts as a security primitive; add action-class ceilings.

**Regulatory risk.** EU AI Act Article 15 (robustness) — Sentinel evidence says these systems are not robust under typical workload.

### A7. LLM-as-judge / recursive agent evaluation

**Mechanism.** One agent's output becomes the gate on another agent's action. Evaluator agents, critic agents, voting ensembles.

**Axis damage.** Evaluation loops can reach mutual-agreement drift without ground truth. Creates C4b (shared-state coupling through the evaluation artifact). V-axis degrades because bad decisions can be endorsed by a peer agent with the same biases.

**Typical BR.** BR-3 to BR-4, heavily dependent on whether evaluator is trusted.

**Demotion path.** Ground-truth gates (empirical checks, typed assertions) in addition to agent-evaluator; evaluator output logged as evidence but never as sole authority.

**Regulatory risk.** EU AI Act Article 14 (human oversight) — if the only reviewer is another LLM, the oversight is nominal.

### A8. OAuth-as-agent-identity (agent authenticates as user)

**Mechanism.** Agent acquires user's OAuth token; acts with user's full permissions. Principal is conflated.

**Axis damage.** A-axis escalation by identity aliasing: there's no separation between "user can do X" and "agent can do X on user's behalf". Authorisation ledger can't distinguish user intent from agent-initiated action.

**Typical BR.** BR-3; higher if user permissions are broad.

**Demotion path.** Delegated-identity model with explicit agent principal, recorded in every action's evidence. Session-execution attestation binds agent identity to session, not user identity; attestation tokens carry subject, tool allowlist, parameter constraints, policy snapshot, and expiry.

**Regulatory risk.** GDPR (data-subject rights don't know *who* processed data); EU AI Act Article 12 (logging must identify the actor).

### A9. Ungoverned vector memory / RAG-as-memory

**Mechanism.** Retrieval-augmented generation with write-back to vector stores. Prompts become data. Past interactions retrieved as context for new ones.

**Axis damage.** V-axis catastrophic: you cannot "unwrite" a vector reliably. One poisoned interaction contaminates future retrievals. O collapses because vector contents are not human-readable. Creates implicit C4b (shared state across sessions).

**Typical BR.** BR-3 even without other factors; BR-4 in multi-user shared-memory deployments.

**Demotion path.** Strict write-through provenance (every vector tagged with source + signature); retention policy with exercised deletion; separate reference corpus (immutable, curated) from interaction memory.

**Regulatory risk.** GDPR Article 17 (right to erasure) — if you cannot reliably delete vectors, you cannot honour the right; EU AI Act Article 10 (data governance).

### A10. Context stuffing / long-context abuse

**Mechanism.** Pack everything into the context window. System prompt, user input, tool outputs, retrieved data — all concatenated, trusting the LLM to sort it out.

**Axis damage.** O collapses — there is no observable boundary between trusted system prompt and untrusted user-supplied content. δ_adv maxed — prompt injection via any of the concatenated sources. τ degrades as context accumulates.

**Typical BR.** BR-3 per session; BR-4 when context persists across sessions.

**Demotion path.** Typed context slots with per-slot trust level; hard boundary between system and data; runtime detection of cross-boundary influence.

**Regulatory risk.** EU AI Act Article 15 (robustness against manipulation).

### A11. Computer use / browser agents

**Mechanism.** Agent given keyboard, mouse, or browser automation authority. Observes the screen and acts on it.

**Axis damage.** A4 by construction — agent can do anything a human operator can. R unbounded. V usually V3/V4 (clicks that hit "submit" are irreversible). δ_adv maximal — every on-screen element is a potential injection vector; agents can be tricked by screen content.

**Typical BR.** BR-5 without exceptional controls. BR-4 with whitelisted applications and screen-level content filtering.

**Demotion path.** Application whitelist, action-class ceiling, confirmation gate on all write operations, per-click evidence with signed screen capture.

**Regulatory risk.** EU AI Act Article 14 (human oversight) nearly unenforceable at speed; Article 15 (cybersecurity) — screen content is an attacker-controlled channel.

### A12. "Deep research" long-running agents

**Mechanism.** Agent browses the open web, reads pages, synthesises reports. Runtime measured in minutes or hours.

**Axis damage.** δ_adv is maximal and *cumulative* — every URL is an attacker-controlled prompt injection point. Context grows with runtime; trust erodes. V-axis complicated (agent may take actions based on poisoned context).

**Typical BR.** BR-3 when output is advisory-only; BR-4+ if agent can act on findings.

**Demotion path.** Whitelisted sources only; signed-retrieval evidence per page; hard cap on runtime; output strictly Class A (advisory) unless independently verified.

**Regulatory risk.** EU AI Act Article 15 (robustness) — open-web retrieval is adversarial input by default.

### A13. BYOA into corporate data / shadow agents

**Mechanism.** Employee connects personal Claude Desktop / ChatGPT to SharePoint, Gmail, internal wikis via MCP. Or dev team spins up an agent on a service account with broad credentials. IT often unaware.

**Axis damage.** Entire A/R/C/V/K profile is unknown because the deployment is undocumented. DLP-blind. No evidence trail. τ drifts without trajectory review.

**Typical BR.** Unrateable. Should be treated as BR-4 by default until rated, because the population affected is "all corporate data the credential can reach".

**Demotion path.** Agent asset inventory (like an IT CMDB but for agents); required profile disclosure before credential issue; DLP integration on agent egress paths.

**Regulatory risk.** GDPR (processor registry obligations); sector-specific (financial, healthcare) — undocumented agents almost certainly breach.

### A14. Autonomy sliders / approval fatigue

**Mechanism.** System designed with human-in-the-loop confirmation gate. Operator approves N routine actions; the (N+1)th approval becomes reflexive. Architectural V-axis is strong; *practical* V-axis decays over time.

**Axis damage.** τ (trajectory) finding. V-axis on paper unchanged; V-axis in practice degrades. This is exactly what the framework's trajectory modifier catches and most process-shaped governance misses.

**Typical BR.** Can degrade from BR-2 to effective BR-4 without a single architectural change.

**Demotion path.** Approval-quality metrics (median review time, diff-of-approved-vs-declined); periodic forced re-approval of standing patterns; independent sampled review.

**Regulatory risk.** EU AI Act Article 14 (human oversight must be *effective*, not nominal).

### A15. Prompt-injection-as-feature (tool output concatenated to next prompt)

**Mechanism.** By protocol, tool result text is concatenated into the next LLM prompt without framing or attestation. The channel is how tools work.

**Axis damage.** δ_adv built-in. Tool results from any source can contain injection payloads that escalate authority, redirect tools, or leak data.

**Typical BR.** BR-2 in read-only tool chains; BR-4 when any tool can return attacker-controlled text *and* write tools exist in the same session.

**Demotion path.** Sanitise / quote tool outputs at the protocol layer; mark tool-output regions as untrusted in the prompt structure; runtime detection of role-escape strings in tool outputs.

**Regulatory risk.** EU AI Act Article 15 (cybersecurity).

---

## Part B — Evidence-chain anti-patterns

These are the anti-patterns an EU AI Act auditor, a regulator, or a post-incident forensic examiner will find first. They are often present in systems that score acceptably on the architectural axes — which means an otherwise-well-designed system can still fail assurance if the evidence chain is wrong.

The positive reference for this section is **Lane2's SAPP (Secure Agent Payment Protocol)** as a design — specifically its evidence-anchoring layer, which provides externally-anchored Merkle-proof evidence with independent signing keys. See §4 at end.

### B1. Application logs as "evidence"

**Mechanism.** System writes what happened to structured logs (JSON, syslog, ELK, Splunk). Operators call this "the audit trail".

**Why it fails.** Logs are mutable at rest — a DBA, admin, or compromised pipeline can alter them. No cryptographic integrity. No external anchor. Not admissible as proof in disputes. No liability model.

**Axis damage.** O appears strong (lots of data); on audit, O is documentary because the data isn't tamper-evident.

**Demotion path.** Tamper-evident evidence contracts with hash-chain or Merkle backing; external anchor (e.g. SAPP); retention policy enforced at storage layer.

**Regulatory risk.** EU AI Act Article 12 (automatic logging must be *technically suitable* for post-market monitoring and integrity proof); Article 72 (incident analysis).

### B2. Post-hoc logging instead of runtime controls

**Mechanism.** The system *logs* that a violation occurred but did not *prevent* it. Governance is a forensic activity rather than an enforcement activity.

**Why it fails.** By the time the log is reviewed, the unsafe action has happened. In agentic systems with fast-onset drift (Gagne's multi-agent drift corpus shows collapse inside the baseline-establishment window, see [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)), post-hoc logging is structurally incapable of preventing harm. A log is not a control.

**Axis damage.** O non-zero but effective V collapses. The framework's §9 at BR-4+ requires *preventive* controls that are architectural, not only detective.

**Demotion path.** Runtime enforcement gates (action-class dispatcher, STA verification, ontology firewall — *actually enforced at runtime*) in addition to logging. At BR-3+, the log is evidence of the control firing, not the control itself.

**Regulatory risk.** EU AI Act Article 15 (robustness must be runtime-effective, not post-hoc observable).

### B3. Prompt storage without governance

**Mechanism.** System stores user prompts indefinitely. Often trained on, always retained, rarely auditable. May leak into model training, may leak to support tooling, may be retrieved by LLM-provider employees.

**Why it fails.** Prompts are user data and often contain PII, PHI, trade secrets, or client-confidential material. No retention policy, no erasure capability, no consent mapping.

**Axis damage.** K jumps because any breach surfaces user data. O appears strong (prompts stored) but is damaging, not protective. V-axis catastrophic for GDPR Article 17 right-to-erasure if prompts are used in training.

**Demotion path.** Explicit prompt-retention policy; per-principal retention window; documented training-use carveout; exercised deletion. For regulated deployments, process prompts in-region and record provenance of any cross-border flow.

**Regulatory risk.** GDPR Article 5 (storage limitation), Article 17 (erasure), Article 30 (records of processing); EU AI Act Article 10 (data governance); sector rules (HIPAA, PCI-DSS).

### B4. No delegation chain recorded

**Mechanism.** Agent acts. Evidence records *that the action happened* but not *who authorised the agent to take it, scoped how, for how long, derived from which policy snapshot*.

**Why it fails.** After the fact, it's impossible to say: was this action within the agent's grant? Was the grant in-date? Was the principal who issued the grant authorised to issue it? The delegation chain is the forensic backbone of agentic audit.

**Axis damage.** Post-incident, A-axis is un-reconstructable. Any claim about action authority becomes "the code allowed it" rather than "the principal authorised it".

**Demotion path.** Cryptographically signed delegation tokens (STA-style) carrying: subject, tool allowlist, param constraints, policy snapshot ID, expiry, delegation-chain hash. Every action's evidence cites the token that authorised it.

**Regulatory risk.** EU AI Act Article 12 (logging must identify the actor and basis); Article 14 (oversight requires traceability of authorisation); sector (SOX, GDPR accountability principle).

### B5. No authentication chain / missing principal

**Mechanism.** Evidence shows an agent acted but not which principal's identity was established when. Or identity was established once at session start and inherited thereafter.

**Why it fails.** In high-assurance operations, *freshness* of authentication matters. Was the operator physically present when the critical action was authorised, or was this an old cached auth? Can the authentication be tied to the specific action, not just the session?

**Axis damage.** A-axis reconstruction fails for any action late in a long session. Wallet-style and high-assurance operations specifically require freshness binding.

**Demotion path.** Presence-binding levels: *fresh_live* (nonce-bound biometric), *recent_live* (time-bounded biometric), *cached_auth*, *device_unlock_only*, *none*. Evidence records the level. Policy rejects critical actions at insufficient freshness. Schemes of this shape exist in private reference implementations; the level taxonomy is the portable part.

**Regulatory risk.** PSD2 SCA; eIDAS; EU AI Act Article 14 (oversight freshness); sector-specific high-assurance rules.

### B6. Unsigned or self-signed-by-vendor evidence

**Mechanism.** Evidence is recorded, maybe even hash-chained, but signed only by the vendor's own key — or not signed at all. "Trust us, we have a log."

**Why it fails.** In a dispute between deployer and vendor, vendor-signed-only evidence cannot be independently verified. In a regulator-vs-deployer proceeding, evidence from a system the deployer controls is weaker than evidence countersigned by an independent anchor.

**Axis damage.** O nominal; O effective is weak for adversarial reconstruction.

**Demotion path.** Independent anchor with its own signing key (SAPP-style), recording the evidence commitment in an append-only chain the vendor cannot rewrite. Deployer can verify against the anchor; regulator can verify against the anchor; vendor cannot unilaterally retract.

**Regulatory risk.** EU AI Act Article 12 integrity requirement; evidentiary admissibility in dispute.

### B7. No explainability source mapping

**Mechanism.** Agent produces a decision. Evidence records the output but not which inputs, policy rules, ontology concepts, or evidence entities the decision derived from.

**Why it fails.** Transparency obligations require the *reason* the system reached the decision, traceable to the source data. A confident output with no source trace is untestable, un-challengeable, and fails GDPR Article 22 right-to-explanation for automated decisions.

**Axis damage.** K compounds — a K3 regulated decision with no source mapping is unchallengeable, escalating effective consequence.

**Demotion path.** W3C PROV-O provenance: `prov:wasGeneratedBy`, `prov:wasAttributedTo`, `prov:wasDerivedFrom`. Provenance depth gated by confidence (low confidence → full graph). An explain-statement API exposes source mapping on demand.

**Regulatory risk.** EU AI Act Article 13 (transparency); GDPR Article 22 (automated decision-making); sector-specific explainability (FCRA, EU consumer credit).

### B8. Evidence mutable at rest

**Mechanism.** Evidence stored in normal application database. Admins, DBAs, or compromised pipelines can alter it. No cryptographic integrity at rest.

**Why it fails.** Log-as-evidence assumes infrastructure trust. For regulated actions the question is "can you prove the evidence you present wasn't edited". If not, it isn't evidence.

**Axis damage.** Counts as documentary O, not structural or architectural.

**Demotion path.** Hash-chain per pipeline stage; deterministic contract hashing (canonical and reproducible); external anchoring on an independent Merkle-proof layer; authority-export path that recomputes hashes and verifies them against the anchor.

**Regulatory risk.** EU AI Act Article 12 integrity; sector (SOX 404, SEC 17a-4).

### B9. No replay capability

**Mechanism.** System can show what was logged but cannot *re-execute* the decision path from stored evidence. Bugs, drift, or disputes cannot be reproduced.

**Why it fails.** Post-market monitoring (EU AI Act Article 72) and authority investigation (Article 26) both require the ability to reconstruct what the system did. Logs describing the event are insufficient if you cannot reproduce it.

**Axis damage.** V-axis forensic reconstruction fails.

**Demotion path.** Deterministic trace replay from evidence contracts; policy-snapshot binding so the exact policy in force at decision time is re-loadable; tool-execution transcripts preserved with input/output.

**Regulatory risk.** EU AI Act Article 72 / 73 (post-market monitoring + incident).

### B10. No retention policy or authority-export path

**Mechanism.** Evidence exists but either indefinitely retained (privacy / storage-limit violation) or deleted at operational convenience (audit violation). Or: evidence cannot be exported in a form the authority will accept.

**Why it fails.** Retention windows are regulation-specific (varies by sector); authority export formats are specified (e.g. EU AI Act Article 19 retention, Article 26(6) access). Operational-convenience retention is neither compliant nor defensible.

**Axis damage.** Regulatory K sub-tag escalation when audit dry-run fails.

**Demotion path.** Storage lifecycle >= required minimum (MEP-06); controlled deletion policy; replay/evidence export reproducible (MEP-07); audit dry-run drill (MEP validation runbook).

**Regulatory risk.** EU AI Act Articles 19 / 26(6); GDPR Article 5 storage limitation; sector-specific (varies).

### B11. Critical action fail-open

**Mechanism.** When evidence write fails (anchor down, signer unavailable, store full), the action proceeds anyway because "availability matters". The system silently degrades from evidenced to unevidenced operation.

**Why it fails.** The most dangerous actions are exactly the ones that end up with no evidence. The failure mode is undetectable at audit because everything looks normal.

**Axis damage.** Evidence chain breaks precisely at the points of highest consequence.

**Demotion path.** Critical-action fail-closed policy (MEP-08): local evidence write failure OR anchor write failure blocks the action at Class B/C. Class A (advisory) may proceed with degraded evidence but tagged as such.

**Regulatory risk.** EU AI Act Article 15 (cybersecurity) and Article 12 (logging integrity) combined.

---

## 3. Scoring rubric

A system exhibiting any of these anti-patterns has its effective BR rating adjusted. Suggested rule (ordinal; v0.3 to refine):

- **Each Part A anti-pattern present →** effective BR class +1 unless the pattern's demotion path is fully implemented
- **Each Part B anti-pattern present →** effective BR class +1 unless the evidence chain passes an externally-anchored Merkle-proof minimum evidence profile
- **A2A, API-first, CrewAI default, MCP-without-composition-rule** — each independently promotes to BR-4 minimum
- **Agent marketplace or BYOA without profile disclosure** — rated as *unrateable*; treat as BR-4

A composed system (multi-vendor, §7 of v0.2) takes the worst rating across components.

Anti-pattern findings should be listed by name in the vendor questionnaire §13 of the framework. "This system does not exhibit anti-pattern X" is a disclosure; absence of the disclosure is not absence of the anti-pattern.

---

## 4. The positive reference — SAPP model

The evidence-chain anti-patterns in Part B point collectively to a single architectural answer: **externally anchored, cryptographically signed, deterministically replayable, provenance-carrying evidence**. Lane2's SAPP (Secure Agent Payment Protocol) — specifically its evidence-anchoring layer — is the reference.

**Why SAPP is the shape to copy:**

1. **External anchor with independent keys.** Evidence commitments are signed by SAPP's keys, not only the system-under-audit's keys. Deployer cannot silently rewrite; vendor cannot silently retract.
2. **Three-level Merkle proofs.** Fast verification at any level; compact proofs for off-system verification.
3. **Domain-neutral.** SAPP does not care whether the operation is a bank transfer, an AI decision, a SIM swap, or an insurance claim. The evidence substrate is the same — which is why it can serve as a *standard* rather than a per-domain implementation.
4. **Evidence scoring.** 10 categories, 0–1.0. An evidence bundle isn't just present — it's *rated*. Low-scoring evidence triggers higher oversight per the Expected Compliance Risk / proportionate-oversight model (framework.md §5.2).
5. **Deterministic liability allocation.** The evidence model is built to answer "whose fault is this" deterministically, not just "what happened".
6. **EU AI Act mapping explicit.** The relevant articles (12 automatic logging, 15 robustness/cybersecurity, 19 retention, 26(6) authority access, 72 post-market monitoring, 73 incident reporting) map to specific minimum-profile controls that a SAPP-style evidence platform can satisfy mechanically. A deployer knows what passes.
7. **PROV-O provenance, depth-gated by confidence.** Cheap when confidence is high; full graph when oversight is flagged.
8. **Fail-closed on critical actions.** MEP-08 — the opposite of anti-pattern B11.

**Why the industry doesn't have this yet:**

Most vendors treat evidence as a logging feature. SAPP treats evidence as a *product* — an engine deliberately separated from the systems it witnesses. That separation is the whole point: the thing that signs the evidence cannot also be the thing that made the decision, or the evidence is self-attestation.

For the framework's purposes, the SAPP-shaped reference answers most of Part B in one architectural move. A vendor that wants to clear the Part B catalogue can point to "we use a SAPP-shaped evidence server" and audit becomes tractable.

---

## 5. Regulatory crosswalk (indicative)

| Anti-pattern family | Primary EU AI Act exposure | Other exposure |
|---|---|---|
| A1–A7 (architectural) | Art. 9 risk mgmt, 13 transparency, 14 oversight, 15 cybersecurity | NIS2, sector rules |
| A8 (identity collapse) | Art. 12 logging of actor | GDPR Art. 5, 22, 30 |
| A9–A10 (memory / context) | Art. 10 data governance, 15 robustness | GDPR Art. 5, 17 |
| A11–A12 (high-agency) | Art. 14 oversight, 15 robustness | Sector-specific |
| A13 (BYOA / shadow) | Art. 9, 12, 26 | GDPR Art. 30 processor registry |
| A14 (autonomy decay) | Art. 14 effective oversight | — |
| A15 (injection-as-feature) | Art. 15 cybersecurity | — |
| B1–B2 (logs not controls) | Art. 12, 15, 72, 73 | SOX 404, SEC 17a-4 |
| B3 (prompt storage) | Art. 10 | GDPR Art. 5, 17, 30, PCI, HIPAA |
| B4–B5 (delegation / auth) | Art. 12, 14 | PSD2 SCA, eIDAS |
| B6 (signing) | Art. 12 integrity | Evidentiary admissibility |
| B7 (explainability) | Art. 13 | GDPR Art. 22, FCRA |
| B8–B10 (mutability, replay, retention) | Art. 12, 19, 26(6), 72 | SOX 404 |
| B11 (fail-open) | Art. 12, 15 | — |

This is indicative, not legal advice. The crosswalk should be reviewed by a regulatory counsel familiar with the deployer's sector before being used in attestation.

---

## 6. How to use this catalogue

**Vendor diligence.** Add to the §13 questionnaire: "Does this system exhibit any of Part A anti-patterns A1–A15? Any of Part B B1–B11? If yes, describe the demotion path implemented." A vendor who can produce clean answers on all 26 has genuinely engineered for blast radius.

**Self-assessment.** Walk the catalogue against your own systems. Note which you rely on and which you've demoted. For each that you exhibit, list the concrete change that would close it.

**Procurement language.** RFP clauses can name the anti-patterns directly: "Vendor attests the system does not exhibit A2A-style public capability discovery; does not rely on auto-generated tool exposure; implements tamper-evident evidence with independent anchoring per an externally-anchored Merkle-proof minimum profile or better."

**Architectural review.** Use the catalogue as a checklist before promoting a system to BR-3+. Every item on the list that the system exhibits must have either a demotion path implemented or an explicit acceptance of the elevated BR class with compensating controls documented.

---

## 7. Open question for v0.2 of the catalogue

1. **Missing patterns.** This is v0.1 of the catalogue. Patterns not yet covered but likely to be added:
   - "Prompt caching as side-channel" (cache-timing attacks on LLM providers)
   - "Inference-server sharing / multi-tenant embedding leakage"
   - "Tool-result-as-training-signal" (tool outputs contaminating future model training)
   - "Agent supply chain: the agent you deployed last month is not the agent running today"
2. **Quantification.** Each pattern currently takes BR +1 as a flat modifier. Some patterns are strictly worse than others; a weighted rubric (paralleling the Expected Compliance Risk formulation in framework.md §5.2) would be more useful.
3. **Anti-pattern decay.** When a pattern's demotion path is partially implemented, what counts as "closed"? A partial-credit rubric would help auditors.

---

**If the framework tells you what to rate, and the reference tells you what "done right" looks like, this catalogue tells you what you are probably rating too generously. Industry defaults are pre-populated with these patterns; they are not absent by accident.**
