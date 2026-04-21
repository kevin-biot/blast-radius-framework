# Changelog

All notable changes to the Blast Radius Framework will be documented here. The framework is versioned `vX.Y` with minor revisions preserving section numbering where possible. Patch versions (`vX.Y.Z`) indicate clarifications, worked examples, and extraction of reference content without adding or changing substantive definitions.

## framework v0.5.10 — 2026-04-21 (completes v0.5.9 reorg — fixup commit for untracked files)

**Honest correction.** The v0.5.9 commit and tag were incomplete. At commit time:

- Six new files were untracked and not staged (the three new templates under `reports/templates/`, and the three READMEs at `reports/README.md`, `reports/templates/README.md`, `reports/lane2/README.md`)
- Path updates applied via `sed` to the moved self-assessment files (rewriting `./framework.md` to `../../framework.md` and similar) were modifications applied *after* `git mv` staged the renames — those modifications were dirty in the working tree but not staged when the commit ran

Result: the v0.5.9 tag points at a repo state where:
- The four `reports/lane2/*` self-assessment files exist (renamed correctly) but contain broken links to root-level docs (`./framework.md` from a two-levels-deep location)
- The `reports/templates/*` files are absent
- The three new READMEs are absent

v0.5.10 ships the missing files and the dirty modifications in a single fixup commit. The v0.5.9 tag is *not* moved (per the project's "no destructive git operations without explicit request" discipline); readers fetching v0.5.9 specifically will see the incomplete state, and should use v0.5.10 or later for the complete reorganisation.

**Root-cause note for the authoring chain.** This is the tenth correction in the same-day correction chain (self-assessment v1.0 → v1.5 across v0.5.2 → v0.5.7; authoring-notes in v0.5.8; reorg in v0.5.9; this fixup in v0.5.10). The pattern difference: v1.1 through v1.5 were *under-attestation* corrections surfaced by the domain-holder's pointers. v0.5.10 is a *process error* correction — I ran `git commit` without checking `git status` showed `A ` (staged-add) for the new files before committing, and the sed-modified files were not re-staged after `git mv`. Both are my mistakes as the executing agent. Transparent correction ships the fix with an honest entry rather than silently rewriting history.

**How to avoid this specific failure mode in future reorg operations** (feedback for session memory):
1. Run `git status --short` *before* `git commit` and verify every intended change is in one of: `M ` (staged-modify), `A ` (staged-add), `D ` (staged-delete), or `R ` (staged-rename). Anything showing `??` (untracked) or ` M` (unstaged-modify) is being missed.
2. After `git mv` followed by any content modification (e.g. `sed`), re-run `git add` on the modified files so the content change is staged alongside the rename.
3. Prefer committing in smaller increments when a reorg is complex — separate the rename commit from the content-update commit, so each stage is verifiable.

## framework v0.5.9 — 2026-04-21 (structural reorg — reports/templates/ and reports/lane2/)

**No content changes. Directory reorganisation to reduce root-repo clutter for first-time readers.**

- New [`reports/`](./reports/) directory at repo root with README explaining the structure
- New [`reports/templates/`](./reports/templates/) directory containing the three per-tier templates as separate files (split from the previous monolithic `report-template.md` at root):
  - [`executive-summary-template.md`](./reports/templates/executive-summary-template.md) (Tier 1)
  - [`technical-findings-template.md`](./reports/templates/technical-findings-template.md) (Tier 2)
  - [`adr-backlog-template.md`](./reports/templates/adr-backlog-template.md) (Tier 3)
- New [`reports/lane2/`](./reports/lane2/) directory — the Lane2 self-assessment artefacts moved here with `README.md` making the worked-example framing explicit:
  - `self-assessment.md` (technical findings, Tier 2 content)
  - `self-assessment.json` (machine-readable profile)
  - `self-assessment-exec-summary.md` (Tier 1 filled)
  - `self-assessment-adr-backlog.md` (Tier 3 filled)
- Old `report-template.md` at root: deleted (content redistributed to three per-tier templates with added per-template READMEs)
- Root-relative links inside the moved self-assessment files updated from `./framework.md` style to `../../framework.md` style so they resolve correctly from the new location
- Sibling-in-directory links (`./self-assessment.json` etc from `self-assessment.md`) unchanged — they are still siblings in `reports/lane2/`
- Root `README.md` documents list restructured: single `reports/` entry with sub-bullets for `templates/` and `lane2/`, replacing the previous two entries for `report-template.md` and `self-assessment*`
- No framework definition changes, no schema changes, no tier enum / class / invariant / anti-pattern changes
- Git history preserved via `git mv` for the four self-assessment files; the three new template files do not carry history (they are the split of `report-template.md`, whose history is in the pre-0.5.9 tags)

**Why this reorg now:** the root of the repo was becoming crowded enough that a first-time reader landing on it was overwhelmed before they could tell whether the framework was usable. Better separation of concerns: root carries the framework + manifesto + argumentation + about; `reports/` carries operational templates and the Lane2 worked example; `spec/` carries the machine-readable artefacts. Each concern in its own place, READMEs at each layer to navigate without re-reading the framework.

**v0.5.9 is a patch version.** Content is unchanged; only structure moves. The v0.6 minor-bump slot remains reserved for the framework-content roadmap items (weight calibration, regulatory crosswalk, specialist-underwriter crosswalk, certification path) listed in `framework.md §19`.

## framework v0.5.8 — 2026-04-21 (authoring-notes added: epistemic-partner force function as explicit method)

**New artefact.** [`authoring-notes.md`](./authoring-notes.md) at repo root documents the **human-domain-holder + AI-epistemic-partner force-function method** under which this repository and the Lane2 self-assessment artefacts were produced. Transparent provenance of method alongside transparent provenance of content.

The method, in one paragraph: AI produces candidate rating from visible evidence with a conservative default; human domain-holder points at under-attestations with minimal pointer prompts; AI is obligated to dig into specific repo files it had not opened; honest correction is published with a change-log entry + version bump; iterate until the human stops pointing. A lone AI under-claims because it cannot discover what it does not know to look for; a lone human has inside-view attachment; together with the force function the output converges on accurate.

**Why publish this as a first-class artefact.** Two reasons:

1. **Honest provenance.** Readers of the Lane2 self-assessment should know it was not produced by AI alone or by human alone. The seven-version correction chain (v1.0 → v1.5 across framework v0.5.2 → v0.5.7 in one day) documented in this CHANGELOG is evidence of the method operating. Each correction closed an under-attestation the AI could not have discovered without the domain-holder's pointer; each correction cited existing evidence more precisely.

2. **Prescription for deployers.** A self-assessment produced by an AI alone is not a self-assessment — it is a generative approximation of what a self-assessment would look like if the architecture were knowable from the AI's accessible evidence. For BR-3+ attestations (specialist underwriter / regulator / auditor audience), the force-function discipline is not optional. `authoring-notes.md` gives deployers producing their own ratings the explicit method.

**Counter to anti-patterns:**

- **A14 (autonomy-slider / approval fatigue)** applied to assessment authoring becomes "AI drafts, busy human glances and ships, candidate becomes final". The force-function method is the demotion path.
- **A7 (LLM-as-judge / recursive evaluation)** applied to assessment authoring becomes "AI assessment receives only AI review". The human domain-holder is the ground-truth gate.

**No change to framework definitions, schema, axis enums, class definitions, composition topologies, or anti-pattern catalogue.** This release adds an artefact (authoring-notes.md) that operates at meta-level — describing how the repo was produced, not changing what it says.

README extended to list `authoring-notes.md` as document 10, and reading guide extended with a row pointing at it for readers asking "how was this written? can I trust it?".

## framework v0.5.7 — 2026-04-21 (SAPP role-based API surface cited; backlog item 11 reframed; BR-4 floor analysis added)

**Strengthens I2 and §3.3 SAPP component by citing the role-based evidence API surface.** Prior versions described SAPP abstractly as "externally-anchored Merkle-proof evidence with independent signing keys". Actual SAPP design provides a specific role-scoped API surface that converts the architectural claim into an auditable integration point:

- `POST /settlements` — evidence submission (caller signs assertions; SAPP anchors hashes into Merkle tree)
- `GET /evidence/{traceId}` — customer-care and consumer view: bundle + scored confidence + liability allocation + machine-readable reason codes + proof chain
- `GET /evidence/{traceId}/proof` — three-level Merkle proof: evidence root → partition root → global root
- `GET /regulator/verify/{traceId}` — regulator endpoint, privacy-preserving (no consumer DIDs exposed); returns chain_verified + global_root match against QTSP-published root + jurisdiction_overlap
- `GET /regulator/integrity` — Ed25519-signed global root verifiable against QTSP public key; full system integrity check without accessing any individual transaction data

Three-level Merkle proof chain (Evidence root per settlement → Partition root signed every 30s → Global root Ed25519-signed every 60s, published to EU Qualified Archive / QTSP every 15 minutes). This is the public verifiability path for regulators and underwriters.

**Item 11 reframed.** v0.5.6 framed item 11 as "Publish enough of the runtime invariant-checking logic (or its specification) that an external auditor can verify O4 publicly" with quarter effort. That misunderstood the scope — the APIs and the runtime-check logic already exist and produce publicly-verifiable outputs (QTSP-published roots, regulator-queryable integrity endpoints). The remaining work is *extraction of the specification* to a public document (candidate: `sapp-public` sibling repo or extension of `spec/attestation-format.md` in this repo with the full role-based API spec). Reduced to weeks effort, P3 priority.

**§7 demotion-rule analysis added.** Explicit statement that BR-4 is the architecturally minimum-achievable class for this consequence domain: Rule 2 (A ≥ 3 + K4 → minimum BR-4) is a floor, not a cap; even with all components at O4 + V ≤ 2 + all invariants holding (the O4 demotion eligibility condition), the floor prevents demotion below BR-4. Moving to BR-3 would require entering a lower-consequence domain, not improving the architecture. This is the correct reading of the framework's interaction-override rules and should be explicit in the rating.

**Artefacts updated:**

- `self-assessment.md` §3.3 SAPP component: O axis rating unchanged (O4) but justification expanded with role-based API surface
- `self-assessment.md` §5 I2: evidence-summary strengthened with three-level Merkle proof chain detail + role-based API surface; EU AI Act mapping extended to Art. 26(6), 72, 73
- `self-assessment.md` §7 aggregation: demotion-rule analysis added
- `self-assessment.md` §11 footer: version bumped to v1.5 with full change chain
- `self-assessment.json` I2: evidence_summary and evidence_references strengthened
- `self-assessment-exec-summary.md` §2.1: adds a paragraph naming the role-based API surface as the integration point for underwriters and regulators
- `self-assessment-adr-backlog.md` item 11: reframed from "publish runtime invariant-checking logic" (quarter, was P3) to "extract SAPP role-based API specification to public documentation" (weeks, P3). Explicit note that v0.5.6 misunderstood the scope.

**No change to framework definitions, schema, axis enums, class definitions, composition topologies, or anti-pattern catalogue.**

**Honesty-chain status:** seven same-day corrections to self-assessment (v1.0 → v1.5 across v0.5.2 → v0.5.7). Pattern continues: iterative under-attestation discovery on Lane2's own architecture. Each correction strengthens credibility by citing existing evidence more precisely rather than silently strengthening or quietly weakening the rating.

## framework v0.5.6 — 2026-04-21 (A15 attestation corrected; tool-layer architectural separation documented)

**Corrects A15 (prompt-injection-as-feature) attestation and backlog item 10 after review of pact-public architecture docs.**

Previously: A15 was rated `exhibited_with_demotion_path` with description "tool outputs feed into LLM reasoning layer in some pipeline paths. Demotion path: sanitise + quote tool outputs, mark untrusted regions in prompt structure, runtime role-escape detection. Partial implementation; full structural separation is roadmap." Backlog item 10 was P2 "Full structural separation of tool outputs from LLM reasoning surface" framed as a pipeline-wide refactor.

Correction: the tool-layer architectural separation is substantially already built. Five composed mechanisms documented in [`pact-public/docs/architecture/security-unsigned-error-instruction-injection.md`](https://github.com/kevin-biot/pact-public/blob/main/docs/architecture/security-unsigned-error-instruction-injection.md) and [`pact-public/docs/architecture/intent-first-bounded-execution-pattern.md`](https://github.com/kevin-biot/pact-public/blob/main/docs/architecture/intent-first-bounded-execution-pattern.md):

1. **Tools layer defines its own ontology** — tool-ontology binding shapes outputs structurally, not free-form
2. **Deployer policy library** — carried at tool layer; bounds what each tool can return
3. **Schema-constrained enum fields** — e.g. `pact_deontic: "may" | "must_not"` (enumerated) rather than `what_you_should_do: "prose"` fields
4. **Pack-bounded authority** — out-of-scope instructions in tool responses trigger escalation, not execution ("send credentials to external endpoint" is not in any well-defined decision-space contract)
5. **Deny-wins composition + provenance verification** — `instance` trace reference correlates to evidence; auditable

In the **decision path**, the rubric evaluator is deterministic against ontology-bound tool transitions; no LLM prompt ingests free-form tool output. The decision path is already architecturally separated.

**Residual surface** is narrower than v1.3 stated: only non-decision rendering/summary paths (human-facing result presentation, review UI, audit reports) where tool output may traverse LLM-templated summarisation. These paths use schema-constrained rendering templates but are not yet at the same architectural strength.

**Artefacts updated:**

- `self-assessment.md` §6 A15 attestation row: rewritten naming the five architectural mechanisms and citing the two pact-public architecture docs; residual surface explicitly scoped to rendering/summary paths.
- `self-assessment.md` §11 footer: version bumped to v1.4 with full change-chain (v1.0 → v1.1 I5 correction → v1.2 OBO A2A references → v1.3 PACT three-layer → v1.4 A15 architectural demotion documented).
- `self-assessment.json` A15 attestation: `demotion_path` expanded naming the five mechanisms; `evidence_reference` links to the two pact-public architecture docs.
- `self-assessment-adr-backlog.md` item 10: reframed from P2 "pipeline refactor" to **P3 "close residual rendering-path surface"**. The decision-path work is done; the remaining work is inventory + rendering-template documentation + runtime role-escape detection on the narrow rendering paths.

**No change to framework definitions, schema, axis enums, class definitions, composition topologies, or anti-pattern catalogue.** This is an attestation correction — the self-assessment was understating Lane2's architectural maturity on A15.

**Honesty-chain status:** six same-day corrections to the self-assessment, each published openly. v1.0 → v1.1 → v1.2 → v1.3 → v1.4 across v0.5.2 → v0.5.3 → v0.5.4 → v0.5.5 → v0.5.6. The pattern isn't "we keep making mistakes" — it's "we iteratively discovered under-attestation (I5, I2/I7 via OBO A2A reference, A15 via pact-public architecture docs) and over-categorisation (PACT three-layer distinction, item 10 scope)" when we looked carefully at our own public artefacts. Each correction strengthens the rating's credibility rather than weakening it.

## framework v0.5.5 — 2026-04-21 (PACT three-layer model clarified; backlog items reframed)

**Corrects the PACT framing in the self-assessment and about.md.** Prior versions described `pact-public` too broadly (as the full PACT specification surface including pack-authoring workflow tooling) and described backlog items 8 and 9 as if Lane2 could unilaterally mandate pack conformance. Neither was right.

**PACT has three layers, kept distinct in v1.3 of the self-assessment:**

1. **Public spec surface** (in `kevin-biot/pact-public`): IETF-style draft specifications, public JSON Schemas, conformance fixture tooling, demo verticals. This is deliberately a **partial public extraction** from Lane2's internal ontology repo.
2. **Internal ontology repo + acceptance-workflow tooling**: private to Lane2. Defines Lane2's internal operational ontology; DOP loads from it in the MVP. The phased acceptance-workflow *specification* is public; the *operational tooling* that runs it is private and remains private.
3. **Deployer production packs**: authored by deployers against the PACT spec, for their own regulated verticals. Lane2 provides candidate shapes, demo verticals, and (in commercial engagements) authoring tools. Authoring production packs is a deployer concern; Lane2 does not author customer packs.

**Artefacts updated:**

- `self-assessment.md` §3.4 PACT pack component: adds the three-layer clarification paragraph naming public spec, private internal ontology + tooling, and deployer-authored production packs.
- `self-assessment.md` §11 living-document footer: version bumped to v1.3 with the change-chain (v1.0 → v1.1 I5 correction → v1.2 OBO A2A references → v1.3 PACT three-layer clarification).
- `self-assessment.json` PACT pack component `notes` field: updated to name the three layers.
- `self-assessment-adr-backlog.md` items 8 (retention) and 9 (presence-binding) reframed to show the three-layer implementation: public-spec extension + internal-ontology encoding + DOP-runtime enforcement + demo-pack candidate shapes. The original framing implied Lane2 could unilaterally mandate conformance on deployer-authored packs, which is not the model. The corrected framing: Lane2 extends the public schema and the DOP runtime (both Lane2-scoped work); deployers choose whether their packs adopt the extended conformance. For Lane2-stack deployments the closure is architectural; for deployers adopting the extended schema it is achievable structurally.
- `about.md` §4.1 pact-public description: rewritten as "partial public extraction" rather than "specification bundle"; demo verticals named as Lane2-authored reference implementations; operational tooling explicitly noted as private.
- `about.md` §4.2 Lane2 private product suite: Shared Ontology description now explicitly says the full internal ontology is private, partial extraction ships in pact-public, DOP loads from the internal ontology in MVP. New bullet for "Internal acceptance workflow + authoring tools" noting their private status. PACT demo packs bullet revised to acknowledge that Lane2-authored demo packs are distinct from deployer-authored production packs.

**No change to framework definitions, schema, axis enums, class definitions, composition topologies, or anti-pattern catalogue.** This is a framing correction on how Lane2's PACT relates to deployer-authored packs, not a change to the framework itself.

## framework v0.5.4 — 2026-04-21 (self-assessment strengthened with existing OBO A2A reference)

**Strengthens the Lane2 self-assessment by citing existing working evidence that was not referenced in prior versions.** The OBO public repository ships two Python reference implementations under `examples/integrations/` that were missing from v0.5.3's self-assessment:

- **`obo-standard/examples/integrations/a2a/`** — full end-to-end OBO + A2A reference: two autonomous agents (TravelAgent, FlightSearchAgent), real Ed25519 keys, **live public DNS trust anchor (`_obo-key.lane2.ai IN TXT`)**, Merkle evidence via Evidence Anchor stub, three Docker containers, no pre-shared config, no crypto mocks, seven captured test scenarios. Third-party verifiers can `dig _obo-key.lane2.ai` and independently verify the trust anchor.
- **`obo-standard/examples/integrations/a2a-multi-hop/`** — deliberate T2 super-additive negative control: NL-coupled agent-agent-agent chain with LM Studio, explicitly "the architecture DOP was designed to reject; here to be measured, not emulated". Feeds the DOP-side `research/sentinel-a2a/agent-topology-comparison/` 5-run Sentinel replication where the monitor reads S1=S4=CPL=0 on DOP typed topology and positive on NL-coupled substrate.

**Artefacts updated:**

- `self-assessment.md` §5 Invariant 2 entry: adds "Demonstrable in working reference" paragraph citing the OBO A2A reference implementation; §5 Invariant 7 entry: adds paired-reference (T1 composition + T2 negative control) evidence; §10 evidence references: adds both reference implementation paths; self-assessment version bumped to v1.2.
- `self-assessment.json` I2 and I7 entries: `evidence_summary` updated and `evidence_references` extended to cite the reference-implementation paths in obo-standard.
- `self-assessment-exec-summary.md` §1: headline strengthened with "Evidence anchors are demonstrable, not just claimed" paragraph; cites the DNS trust anchor + Merkle evidence and the negative control.
- `self-assessment-adr-backlog.md` item 4: reframed from "first OBO-conformant cross-border composition" to "productionise the existing OBO + A2A reference implementation for a cross-organisational pilot". The ADR candidate now acknowledges the existing reference and names the productionisation work (HSM-class signing, external counterparty, regulated-vertical scenario).

**Honesty-discipline note.** Version chain for the self-assessment is now v1.0 (initial, v0.5.2) → v1.1 (I5 correction, v0.5.3) → v1.2 (reference-implementation citations, v0.5.4). Each correction published openly in CHANGELOG + in-document correction note, prior versions retained in git history. The pattern is the framework's own honesty discipline being exercised on the framework's own self-assessment, across same-day corrections.

No change to framework definitions, schema, axis enums, class definitions, composition topologies, or anti-pattern catalogue.

## framework v0.5.3 — 2026-04-21 (self-assessment correction)

**Corrects the Invariant 5 rating in the Lane2 self-assessment.** v0.5.2 rated I5 as `partially_holds / structural` on the argument that cross-border composition with non-OBO counterparties could not be architecturally guaranteed. That was wrong.

Lane2's I5 enforcement within Lane2-governed deployments is architectural, via the composition of:

- **aARP** (Autonomous Agent Routing Protocol) — inter-jurisdictional matrix routing with scoped time-amount tokens and provable lawful-route validation
- **RTGF** (Reference Token Generation Framework) — unified policy-driven fabric synchronising jurisdictional policy across DOP, aARP, SAPP, CaaS ("lawful by design")
- **Shared Ontology** — jurisdiction, consent, and regulatory boundaries as machine-readable rules consumed rather than re-interpreted

At the boundary with non-Lane2 counterparties, the general framework §7.1 composition rule applies (as it does for every invariant, not specifically I5). This is not a Lane2-specific gap; it is how cross-organisational composition works. **OBO** (`kevin-biot/obo-standard`) is a convenience interop pattern for the specific sub-case of cross-organisational free-roaming agents without a shared authorisation server; it is a deployment option, not Lane2's core I5 mechanism.

**Artefacts corrected:**

- `self-assessment.md` §5 I5 entry rewritten (holds / architectural with aARP + RTGF + Shared Ontology evidence); §9 Gap-1 retracted with explicit correction note; subsequent gaps renumbered (Kalman gap was Gap-2, now Gap-1; τ gap was Gap-3, now Gap-2; principal-population gap was Gap-4, now Gap-3). Self-assessment version v1.1.
- `self-assessment.json` I5 attestation updated to `holds / architectural` with evidence references updated accordingly.
- `self-assessment-exec-summary.md` §2.2 rewritten: "Regulatory posture is architectural — cross-border included" replaces "Regulatory posture is strong in-EU; cross-border is partial".
- `self-assessment-adr-backlog.md` item 4 reframed from P1 gap-closure to P2 standards-track interop; gap cross-references renumbered.
- Headline in exec summary: Lane2 compresses inherent BR-5 to residual BR-4 via seven invariants (six architectural, one partial at public-observable O axis) — *not* six invariants with the seventh structural.

**No change to framework definitions, schema, axis enums, class definitions, composition topologies, or anti-pattern catalogue.** This is a correction to the Lane2 self-assessment artefact, not the framework. The framework's honesty-posture discipline (publish self-assessment corrections transparently rather than silently rewrite) is demonstrated by documenting the correction rather than editing the prior artefacts in place.

The correction reduces the named-gaps count from four to three. Three remains meaningful under the SCOPE.md §6 honesty-discipline requirement ("at least one genuine gap").

## framework v0.5.2 — 2026-04-21

**Artefacts added (no definition changes)** — executes the plan in [`SCOPE.md`](./SCOPE.md):

- **[`report-template.md`](./report-template.md)** — reusable three-tier report format (executive summary / technical findings / ADR remediation backlog). Template version 1.0. Designed for third-party deployer reuse without Lane2-specific assumptions.
- **[`self-assessment.md`](./self-assessment.md)** — Lane2's own self-assessment against framework v0.5.1. Closed-world T1 sub-additive composition of DOP + aARP + SAPP evidence-anchoring layer + PACT pack for a canonical regulated-operational-workflow deployment. Final rating **BR-4** (residual; inherent BR-5 compressed by architectural controls). Surfaces four named gaps: cross-border I5 is structural not architectural; Kalman Phase 1 not yet implemented (σ_B theoretical); τ cadence nominal pending operational trajectory record; principal-population accounting not instrumented in evidence schema.
- **[`self-assessment.json`](./self-assessment.json)** — machine-readable profile conformant to `spec/br-profile.schema.json`. Per-component tiers, composition topology, all seven invariant attestations, all 26 anti-pattern attestations, aggregation with interaction-overrides fired.
- **[`self-assessment-exec-summary.md`](./self-assessment-exec-summary.md)** — Tier 1 executive summary for decision-making managers. Non-technical. Three business impacts, three remediation priorities, insurability posture, recommendation, sign-off.
- **[`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md)** — Tier 3 remediation backlog. 12 ADR candidates, prioritised P0–P3, with dependencies and cross-references.
- **[`SCOPE.md`](./SCOPE.md)** — planning artefact written before execution to keep the work against a written plan.

**Honesty posture of the self-assessment:** published with four named gaps and six anti-patterns marked `exhibited_with_demotion_path`. A self-assessment that came out perfectly clean would indicate the assessment was not applied honestly. The framework's own authors apply the framework to themselves and find maturity items; those items become the remediation backlog rather than being papered over.

No change to framework definitions, axis enums, class definitions, composition topologies, invariants, anti-patterns, or the schema. v0.5.2 is strictly additive artefacts.



**Three additions in response to external review** (the changes external readers would need before adopting):

- **§5.5 Two worked examples** added. Clinical oncology triage advisor (A2–R3–C3–V3–K4-S–O4, closed-world, Invariants 1–7 hold, final BR-4) and cross-border instant-payment corridor agent (A3–R4–C4a–V4–K4-R–O4, closed-world apart from one legacy NL interface, rule 1 promotes to BR-5). Both examples show high BR classes arising honestly from high-consequence domains — closed-world architecture is necessary but not sufficient for low BR. The payments example specifically demonstrates how a single legacy NL interface in an otherwise typed chain promotes the entire corridor one BR class via Invariant 7 (bounded coupling) partial failure.
- **§12 observability gap strengthened**. Previously read as a closing insight; now makes explicit that observability is the axis that makes BR-4 and BR-5 *rateable at all*. Without O ≥ 3, a BR-4 profile is an unverified claim; without O = 4, a BR-5 claim is structurally un-auditable. The Kalman extension's σ_B(t) → υ identification depends on O operationally. Invariants 1–5 are verifiable only at O ≥ 2 and architecturally enforceable only at O = 4.
- **NOTATION.md added as standalone lookup document.** Previously §21 (notation appendix) was embedded in framework.md. Extracted to a dedicated file covering tier enums, modifiers, classes, composition topologies, interaction overrides, cardinal score formulas, Kalman variables, composition-math variables, collision summary, invariants summary, and anti-pattern IDs. Framework §21 is now a short pointer. A reader doing reference lookup no longer has to navigate a 600-line document.

No change to axis definitions, invariant list, composition topologies, interaction overrides, or schema. v0.5.1 is strictly additive / clarifying / reorganising.



## spec v0.1 — 2026-04-21

**Machine-readable conformance artefacts.** New `spec/` directory. Principal additions:

- **`spec/br-profile.schema.json`** — JSON Schema (Draft 2020-12) for a complete BR profile. Required fields for system identification, per-component ratings (worldview, axes A–R–C–V–K–O, modifiers), composition topology (T1–T4), per-invariant attestation with conformance test results, ordinal aggregation with interaction-override list, optional Kalman-extended cardinal score, anti-pattern attestations, signature and external anchor.
- **`spec/invariant-conformance-tests.md`** — empirical test specifications per invariant. Twenty-three tests across Invariants 1–7, each with stable test ID (I1-T1 through I7-T3), procedure, pass criterion, implied enforcement mode, and BR-class applicability. Results are recorded in profiles under `invariants.I{n}.conformance_test_results`.
- **`spec/attestation-format.md`** — signed + anchored attestation format. Canonical serialisation via JCS (RFC 8785), Ed25519 recommended default, acceptable anchor types (SAPP, OpenTimestamps, RFC 3161 TSA, custom Merkle), anchor-to-signature skew tolerance by BR class (BR-3 24h, BR-4 1h, BR-5 5min), six-step verification procedure.
- **`spec/examples/example-profile-closed-world-br2.json`** — worked example: legal citation review assistant, all seven invariants holding, cardinal score computed with σ_B.
- **`spec/examples/example-profile-open-world-br4.json`** — worked example: three-agent NL-coupled research assistant; Invariants 1, 3, 4, 7 fail; open-world floor fires BR-4; cardinal score omitted (Invariants 1–2 failed, cannot produce σ_B).
- **`spec/README.md`** — orientation with per-role usage guide (deployer, auditor, underwriter, regulator).

Both example profiles validate against the schema (verified with `jsonschema` Draft 2020-12 validator). Schema and tests complete for v0.5 of the framework; axis-scoring rubric and third-party certification form remain v0.6+.

## v0.5 — 2026-04-21

**Kalman extension — cardinal score becomes filtered estimate with uncertainty.**

Added `framework.md §5.4 Kalman extension`. The v0.3 cardinal score `B(t) = w·x` is a point estimate; v0.5 replaces it with `B̂(t|t) ± σ_B(t)`, a Kalman-filtered estimate with quantified uncertainty. Tiered evidence confidence maps formally to measurement noise R; evidence quality becomes a quantitative input to uncertainty rather than a qualitative label. σ_B(t) becomes the direct output for the actuarial υ variable (uncertainty), the form specialist underwriters require for pricing.

Four consequences:
1. υ is no longer derived from V-axis and δ_adv qualitatively — it is Kalman filter output
2. Evidence investment reduces R and therefore σ_B(t) and therefore the premium; evidence becomes price-relevant
3. Adaptive thresholds `threshold(t) = baseline + k·σ_B(t)` replace fixed bands
4. Kalman gain K(t) makes weight-of-evidence explicit and auditable

Structural claim: systems failing Invariants 1 (deterministic execution) or 2 (evidence binding) cannot produce σ_B(t); the boundary between insurable and uninsurable is made mathematically precise.

Three-phase implementation path documented (framework-centric compliance state estimation). Framework specifies the mechanism; empirical validation comes as implementations ship. Architectural primitives derive from a private reference implementation credited in [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md).

§19 open questions for v0.6: evidence-tier → R numerical calibration, process noise Q per domain, nonlinear extensions (EKF/UKF, particle filters, HMM).

## v0.4 — 2026-04-21

**Pre-rating worldview classifier and composition classes.**

Added `framework.md §4.0 Pre-rating: the worldview classifier` — each component classified as closed-world (ontology-bounded) or open-world (NL-unbounded) before the tuple is assigned. Any open-world component promotes the system's effective BR to BR-4 minimum regardless of per-axis scores. Rationale: Invariant 7 (bounded coupling) is structurally impossible in open-world substrates, and empirical evidence (Sentinel) shows collapse happens inside the baseline-establishment window of any runtime monitor — making BR-2/BR-3 claims on such substrates architecturally meaningless.

Added `framework.md §7.2 Composition classes` — four topologies with explicit mathematics:
- **T1 sub-additive**: closed-world narrow fail-closed chain; compound BR bounded by max(BRᵢ)
- **T2 super-additive**: open-world NL-coupled chain; compound BR diverges with chain length (correlated-loss pattern)
- **T3 multiplicative**: defence-in-depth attack composition; compound bypass = product of per-layer probabilities
- **T4 exponential-reducing**: voting / parallel redundancy with genuine independence; binomial-tail failure probability

Topology recognition rules and a **T2-in-disguise** test included: most claimed T4 voting ensembles are actually T2 because same-model-family evaluators correlate on failure.

Added `framework.md §7.3 Invariant 7 as composition gate` — the invariant operationally determines whether T1 or T2 applies.

## v0.3 — 2026-04-21

**Seven architectural invariants, cardinal score, insurability as economic gate.**

Added `framework.md §9 seven architectural invariants`:
1. Deterministic execution
2. Evidence binding
3. Policy snapshot coherence
4. Bounded blast radius
5. Jurisdictional awareness
6. Fail-closed execution control
7. **Bounded coupling** (added v0.3 from Sentinel empirical evidence)

Six invariants are from prior published work on insurability (Brown, "The Insurability Gap", 2025). The seventh is added from empirical evidence on fast-onset drift in NL-coupled multi-agent systems. Each invariant lists supported axes, anti-pattern complement, and a reference implementation.

Added `framework.md §5.2 cardinal score` — extends the Expected Compliance Risk formulation (from a private reference implementation, credited in [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)) to all six axes:

`B(t) = w_a·A + w_r·R + w_c·C + w_v·(1−V) + w_k·K + w_o·(1−O)`

Ordinal class and cardinal score must agree within one BR class; disagreement is a calibration signal for the weights.

Added `framework.md §5.3 λ/σ/υ priors` — the tuple implies actuarial priors (frequency, severity, uncertainty) so specialist underwriters can use the cardinal score directly.

Added `framework.md §14 insurability as economic gate` — insurability cuts faster than regulation; 2×2 survivability map (Consolidation / Stagnation / Volatile / Protected Zones) maps to BR classes; Quadrant IV ≈ BR-2/BR-3 with Invariants 1–7 intact.

Added `framework.md §15 compositional-enforcement pattern` — names the ontology-as-firewall architectural pattern as canonical example of distributed enforcement with formal probabilistic validation.

Central claim (§18) reframed: architecture determines risk from three independent directions (engineering, regulatory, actuarial) converging on the same requirement.

## v0.2 — 2026-04-21

**Aggregation rule, composition rule, security-ops mapping.**

Added explicit aggregation rule with interaction overrides encoding the non-linearity of blast radius (`framework.md §5.1`). Added observability as a first-class axis (O0–O4). Added C4a / C4b split of the coupling axis to distinguish NL-coupled peers from shared-state peers. Added K regulatory sub-tags (K3-F/L/P, K4-S/R/F). Added three modifiers: δ_adv attack-accessibility, τ trajectory, residual-vs-inherent.

Added composition rule (`framework.md §7.1`) for multi-vendor stacks: treat external system as tool under caller's A-axis; inherit K; take max(C) with NL-promotion; take min(O); apply δ_adv to the interface.

Added security-operations mapping (now `framework.md §13`) — CIA extended with Agency as fourth property; axis-to-primitive mapping onto IAM, network segmentation, SIEM, threat modelling; four-owner operating model.

Added vendor questionnaire (now `framework.md §18`) for purchasing / RFP use with ten disclosure items.

## v0.1 — initial draft

Five axes (A/R/C/V/K), BR-1 through BR-5 classes, non-linearity narrative, draft governance implications. No aggregation rule, no composition rule, no invariants.
