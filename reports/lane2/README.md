# Lane2 Self-Assessment

*The Blast Radius Framework applied to the Lane2 integrated governance platform, by its authors.*

**Rated system:** Lane2 integrated governance platform (reference regulated-operational-workflow deployment)
**Final ordinal class:** BR-4 (Systemic)
**Framework version:** v0.5.1
**Assessment version:** v1.5 (after seven corrections — see [`../../CHANGELOG.md`](../../CHANGELOG.md) v0.5.2 through v0.5.7 entries)
**Date:** 2026-04-21

---

## What this directory contains

The Lane2 self-assessment is a complete worked application of the three report templates in [`../templates/`](../templates/):

| File | Tier | What it is |
|---|---|---|
| [`self-assessment-exec-summary.md`](./self-assessment-exec-summary.md) | 1 | 1–2-page executive summary for board, executive, procurement, underwriter audience. Plain English. Start here if you want the headline. |
| [`self-assessment.md`](./self-assessment.md) | 2 | Detailed technical findings. Component-by-component rating (DOP, aARP, SAPP, PACT pack), composition topology, all seven invariants, all 26 anti-patterns, aggregation with interaction overrides, residual-vs-inherent gap analysis. Start here if you want the architecture-level detail. |
| [`self-assessment-adr-backlog.md`](./self-assessment-adr-backlog.md) | 3 | Twelve ADR candidates prioritised P0–P3 with dependencies, effort bands, and cross-references. Start here if you want to see the remediation roadmap. |
| [`self-assessment.json`](./self-assessment.json) | Profile | Machine-readable BR profile, validates against [`../../spec/br-profile.schema.json`](../../spec/br-profile.schema.json). Start here if you want the data surface an auditor or underwriter consumes. |

## Why this self-assessment is published

Three reasons:

1. **The framework's credibility test.** A rating apparatus whose authors will not apply it to themselves is a sales tool, not a standard. Lane2 is published with honest gaps as the evidence that the framework is genuinely applicable to production systems.

2. **Worked template example.** Readers producing their own Blast Radius reports using the templates in [`../templates/`](../templates/) need a concrete example of what populated tier files look like. This is that example.

3. **Competitive signal.** A Lane2 rating published honestly — BR-4 with three named gaps, six anti-patterns marked `exhibited_with_demotion_path`, seven same-day corrections to the attestation — sets the bar for what a credible self-assessment looks like. Competitors who will not produce an equivalent rating are visibly absent.

## Headline findings

- **Final ordinal class: BR-4.** The architecturally minimum-achievable class for the K4-R consequence domain under Rule 2 (A≥3 + K4 → minimum BR-4 floor).
- **Inherent BR-5 → Residual BR-4** via architectural controls: six of seven invariants architectural; composition topology T1 sub-additive; all 26 anti-patterns either `not_exhibited` (20) or `exhibited_with_demotion_path` (6 — architectural-maturity items, not design flaws).
- **Three named gaps:** Kalman Phase 1 (cardinal score theoretical pending implementation); τ trajectory cadence (pre-launch — no operational record yet); principal-population accounting (not instrumented in evidence schema).
- **Evidence anchors are demonstrable, not just claimed.** OBO + A2A reference implementation at [`kevin-biot/obo-standard/examples/integrations/a2a/`](https://github.com/kevin-biot/obo-standard/tree/main/examples/integrations/a2a) with live public DNS trust anchor (`_obo-key.lane2.ai`) third parties can verify. SAPP role-based API surface (customer / regulator / integrity endpoints) demonstrable under PoC.
- **Insurability posture:** coverable with conditions under specialist-underwriter criteria (Munich Re aiSure, AIUC, Armilla/Lloyd's); not excluded under Verisk 2026 commercial insurance AI exclusions; cardinal score `B̂(t|t) ± σ_B(t)` not yet numerical pending Kalman Phase 1.

## Correction chain — the force-function method operating on this assessment

This self-assessment went through **seven versions in one calendar day** (v1.0 through v1.5) across framework releases v0.5.2 through v0.5.7. Each version closed an under-attestation the AI could not have discovered alone. Each correction cites existing evidence more precisely. No correction retracted an accurate claim. See [`../../authoring-notes.md`](../../authoring-notes.md) for the authoring method (human-domain-holder + AI epistemic partner with a force function) and [`../../CHANGELOG.md`](../../CHANGELOG.md) for the full correction chain.

Summary of what the force function surfaced:

- **v1.1 (v0.5.3):** I5 upgraded from `partially_holds / structural` to `holds / architectural` after aARP + RTGF + Shared Ontology were recognised as core jurisdictional mechanism (OBO is convenience interop for a specific deployer class, not Lane2's core I5)
- **v1.2 (v0.5.4):** I2 and I7 strengthened by citing the existing OBO + A2A reference implementation — Ed25519 keys, live DNS trust anchor, Merkle evidence, seven captured scenarios
- **v1.3 (v0.5.5):** PACT three-layer distinction clarified (public spec extraction / private internal ontology + tooling / deployer-authored production packs); backlog items 8 and 9 reframed because Lane2 cannot unilaterally mandate pack conformance on deployer-authored packs
- **v1.4 (v0.5.6):** A15 attestation corrected — decision-path architectural separation is substantially built via tool-ontology binding + deployer policy library + schema-constrained enum fields + pack-bounded authority + deny-wins composition + provenance; residual surface narrower than prior versions stated (rendering/summary paths only); backlog item 10 reduced P2 → P3
- **v1.5 (v0.5.7):** SAPP role-based API surface cited (POST /settlements, GET /evidence/{traceId}, /regulator/verify, /regulator/integrity with QTSP-anchored global root); backlog item 11 reframed from "publish runtime-check logic" to "extract API spec to public doc"; §7 BR-4 floor analysis added

## How to cite this assessment

> Brown, K. (2026). *Lane2 Self-Assessment against the Blast Radius Framework, v1.5.* In: Blast Radius Framework v0.5.7. github.com/kevin-biot/blast-radius-framework/reports/lane2/. CC-BY-4.0.
