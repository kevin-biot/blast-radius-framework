# Scope of Work — Lane2 Self-Assessment and Reusable Report Template

**Status:** Executed (v0.5.2 through v0.5.7); subsequently reorganised in v0.5.9.
**Date opened:** 2026-04-21
**Framework version target at time of writing:** v0.5.2 (patch — adds artefacts, changes no definitions)
**Actual execution:** v0.5.2 (initial publication) → v0.5.7 (seven same-day corrections under the force-function method); structural reorganisation in v0.5.9.

**Post-execution note (v0.5.9 reorganisation).** This document describes the plan as written, with file locations that matched the initial execution in v0.5.2. In v0.5.9 the artefacts were reorganised to reduce root-repo clutter:

- `report-template.md` at root → split into three per-tier templates at [`reports/templates/`](./reports/templates/)
- `self-assessment.md` at root → [`reports/lane2/self-assessment.md`](./reports/lane2/self-assessment.md)
- `self-assessment.json` at root → [`reports/lane2/self-assessment.json`](./reports/lane2/self-assessment.json)
- `self-assessment-exec-summary.md` at root → [`reports/lane2/self-assessment-exec-summary.md`](./reports/lane2/self-assessment-exec-summary.md)
- `self-assessment-adr-backlog.md` at root → [`reports/lane2/self-assessment-adr-backlog.md`](./reports/lane2/self-assessment-adr-backlog.md)

The body of this document is retained as historical record of the plan; when reading file paths mentioned below, apply the above redirection.

---

---

## 1. Motivation

Three reasons to do this now, in one wave:

1. **Framework credibility test.** Applying the framework to Lane2's own stack is the proof-of-the-pudding. A rating apparatus that its authors will not apply to themselves is a sales tool, not a standard. Publishing a self-rating with honest gaps is the stronger signal than publishing one that is all green.
2. **Reusable artefact for deployers.** A three-tier report template (executive summary / technical findings / ADR remediation backlog) fills a gap the framework currently has: the rating is rateable, but the *communication* from architecture team to executive is ad-hoc. Templating this makes the framework usable inside organisations without Lane2 running the engagement.
3. **Competitive signal.** A published Lane2 rating sets expectations. Competitors who produce equivalent self-ratings demonstrate architectural depth; competitors who cannot are on the back foot. Under Verisk 2026 commercial insurance exclusions and EU AI Act Article 26 authority requests, *not having a rating* becomes its own signal within 18 months.

---

## 2. Deliverables

### D1 — Reusable three-tier report template

**File:** `report-template.md` at repo root.

**Contents:** single file with three delimited sections:

- **Tier 1 — Executive summary (1–2 pages).** Non-technical. For decision-making managers. Must cover: current BR class in plain English; top-3 business impacts (regulatory / insurability / operational); top-3 remediation priorities with effort band and investment estimate; insurability posture (current + Verisk 2026); go / continue-with-remediation / redesign recommendation; accountable-executive sign-off line.
- **Tier 2 — Technical findings (detailed).** For architecture team. Schema-conformant profile plus narrative on every non-trivial tier assignment, per-invariant test results with evidence, every interaction-override that fired with trigger explanation, cardinal score with weight disclosure, comparison to class thresholds.
- **Tier 3 — ADR remediation backlog.** For architecture team's follow-up. For each material gap: proposed ADR title, scope summary, dependencies, effort band, priority (impact × feasibility). Explicit note that these are *ADR candidates*, not prescriptions.

**Acceptance criteria:**
- Usable by a third-party deployer without Lane2-specific assumptions
- Each tier is self-contained (a reader can pick up any one without reading the others)
- Tier 1 contains no acronyms or framework jargon requiring the reader to consult NOTATION.md
- Tier 3 items reference framework sections for traceability

**Effort:** ~1 day.

### D2 — Lane2 self-assessment (technical content)

**Files:**
- `self-assessment.md` — narrative rating with honest findings, at repo root
- `self-assessment.json` — machine-readable profile conformant to `spec/br-profile.schema.json`

**Scope:** rating the integrated Lane2 stack (DOP + aARP + SAPP + CaaS + RTGF + Shared Ontology) at the **public-observable level**. Treat each Lane2 product as a component; declare composition topology; attest invariants; attest anti-patterns; compute aggregation; produce cardinal score if defensibly computable.

**Acceptance criteria:**
- `self-assessment.json` validates against `spec/br-profile.schema.json`
- Every invariant attested with an enforcement mode (`architectural` / `structural` / `procedural` / `documentary`) and a status (`holds` / `partially_holds` / `does_not_hold` / `not_applicable`)
- Every anti-pattern attested (`not_exhibited` / `exhibited_with_demotion_path` / `exhibited_without_demotion_path` / `not_applicable`)
- Every fired interaction override (§5.1) documented with trigger
- Residual-vs-inherent gap documented with named control types
- IP boundaries respected per §3 below
- At least one genuine gap surfaced and named — a self-assessment that comes out perfectly clean does not exist and should be reconsidered before publication

**Effort:** ~2 days.

### D3 — Template applied to Lane2 self-assessment

**Files:**
- `self-assessment-exec-summary.md` — Tier 1 content for Lane2's rating
- `self-assessment-adr-backlog.md` — Tier 3 content for Lane2's rating

(Tier 2 content lives in `self-assessment.md` itself; no separate file needed.)

**Acceptance criteria:**
- `self-assessment-exec-summary.md` is readable in under 10 minutes by a non-technical reader and produces a clear BR class, top-3 impacts, and top-3 remediations
- `self-assessment-adr-backlog.md` lists ADR candidates ordered by priority with effort bands
- The three artefacts (technical + exec + backlog) cross-reference consistently

**Effort:** ~1 day on top of D2.

---

## 3. IP boundaries

The public-observable level is deliberately narrower than the internal-instrumented level. A self-assessment at the public-observable level establishes the shape of Lane2's rating without exposing implementation.

### In scope to disclose

- Per-component tier values (A, R, C, V, K, O) for DOP, aARP, SAPP, CaaS, RTGF, Shared Ontology
- Composition topology with edge types (typed / NL / shared-state / voting-quorum)
- Invariant attestations at component granularity with enforcement mode
- Anti-pattern attestations across the 26-pattern catalogue
- Residual-vs-inherent gap list with named control *types* (not specific internal controls)
- Cardinal score if the weights and the implementation phase are defensible at the public level
- Remediation plan at architectural-intent level

### Out of scope — do not disclose in this round

- Source file paths, function signatures, class names, module structures
- Cryptographic parameter values (key sizes, curves, HSM vendor)
- Threat-model details beyond framework §15 public description
- Customer names, deployment sizes, sector splits, pilot counts
- Roadmap claims or dates beyond "pre-launch"
- Kalman R_K calibration numbers (leave as "calibrated internally")
- Internal ADR identifiers (refer to general patterns, not ADR numbers)
- Specific Sentinel-replication data or raw telemetry

### Default rule

When unsure, err toward exclusion. Adding detail later is cheap; retracting public disclosure is expensive.

---

## 4. Sequencing

1. **D1 (template)** — first, because D2 and D3 fill the shape it defines. Building the template during the Lane2 engagement risks producing a Lane2-shaped template rather than a reusable one.
2. **D2 (self-assessment technical content)** — after D1. Produces the schema-conformant profile that feeds D3's Tier 1 summary and Tier 3 backlog.
3. **D3 (template applied)** — after D2. Executive summary and ADR backlog filled from the technical findings.

All three ship in one commit wave on a single branch; tagged `v0.5.2` at the commit that completes D3.

---

## 5. What this round explicitly does *not* include

- AI-epistemic-reviewer product scoping — separate effort, informed by what this round surfaces
- Customer engagements — not until the self-assessment and template are stable
- Third-party certification scheme — v0.6+ framework work
- Retroactive commitments to remediation timelines for gaps surfaced in D2
- Any change to framework.md, NOTATION.md, schema, or the anti-pattern catalogue — this round is artefacts, not definitions

---

## 6. Review process

- **Author:** single author drafts each artefact
- **Self-review:** pass for IP-boundary adherence against §3 before each commit
- **Pre-merge review:** confirm no outputs of D2/D3 expose items in the out-of-scope list
- **Honesty check:** explicit review question on D2 — "does this surface any genuine gap?" A negative answer means D2 needs another pass.
- **Publication:** commit wave on main branch; tag `v0.5.2`; no staged rollout (the artefacts are either ready or not)

---

## 7. Success criteria — judged post-publication

- **D1 usable by a third-party deployer:** another deployer can fill in the template for their own system without Lane2-specific assumptions
- **D2 credible as a self-assessment:** surfaces at least one genuine gap that motivates a later internal ADR
- **D3 usable as board-level communication:** a non-technical reader can state the BR class, top-3 impacts, and top-3 remediations in plain English after one read of the exec summary

If any of these three fails post-publication, the round is a calibration data point and v0.5.3 adjusts.

---

## 8. Version impact

| Artefact | Change |
|---|---|
| `framework.md` | no change — v0.5.1 remains |
| `NOTATION.md` | no change |
| `spec/br-profile.schema.json` | no change |
| `CHANGELOG.md` | new `framework v0.5.2` entry documenting the three additions |
| `README.md` | reading guide extended to name the new artefacts |
| `about.md` | possibly reference the self-assessment from the "pre-launch / PoC" framing |
| Git tag | `v0.5.2` at the commit that completes D3 |

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Self-assessment surfaces an uncomfortable finding | Ship with honest commentary; this is the point of the exercise |
| IP over-disclosure | Out-of-scope list in §3; final review pass before merge; default-to-exclusion rule |
| Template ends up Lane2-specific | D1 written abstractly first, *then* applied in D3; not written during D2 |
| Timeline expands | Each deliverable has bounded scope; if one balloons, cut scope rather than push date |
| Rating comes out different than marketing assumes | Publish as-is; do not retroactively adjust to save face. The published rating is the authoritative one. |
| Competitors weaponise the honest gaps | Accept this — the alternative is dishonest marketing, which is worse. Self-critical honest assessment beats selective green-washing in every evaluation regime that matters (underwriter, regulator, sophisticated buyer) |

---

## 10. Go-ahead

This document captures the plan. On approval, execution begins with **D1 (template)**. Estimated total time to published `v0.5.2` tag: 4 working days from start.

Sign-off: Kevin Brown (Lane2 founder) — confirmation that the scope above is agreed and the IP boundaries in §3 are adequate.
