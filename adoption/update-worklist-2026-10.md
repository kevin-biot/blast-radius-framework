# October Update Worklist

**Date:** 2026-10-26
**Source:** [external review](./external-review-2026-10.md), R01-R12
**Release baseline:** framework 0.5.11 and spec 0.1.1, published together under tag `v0.5.11`

This records implementation status, not only documents delivered. Existing ordinal profiles and test IDs retain their historical versions. No independent assessor, insurer or standards body has endorsed this pass.

| Order | Item | This pass | Remaining exit condition |
|---|---|---|---|
| 1 | R01: claims audit | Publication-baseline corrections applied to framework, notation, insurance companion, summaries and templates; historical material explicitly qualified | Independent review of claims and source sufficiency; no coverage finding claimed |
| 2 | R02: EU crosswalk | Amended baseline, role/article evidence map, high-risk dates and Article 26(6) correction published | Deployment-specific legal review and full operative redline; source-access limit disclosed |
| 3 | R03: protocols | A1/A3/A8 rewritten around actual deployment enforcement, with current sources | No protocol-wide certification or live deployment test |
| 4 | R04: validation and signing ambiguity | Local format/schema/reference/semantic checks, corrected card link/I6 mappings, explicit signing bytes and negative tests | Asymmetric signature/anchor interoperability and complete rating arithmetic not implemented |
| 5 | R05: I1 boundary revision | [Versioned test proposal](./execution-boundary-research.md) separates model variability, replay and policy determinism; seed-only proof withdrawn | Implement and independently run the revised boundary suite; version normative I1 changes |
| 6 | R06: worldview/composition | Incorrect probability statements qualified; conservative floor retained; counterexample programme defined | Run paired comparisons, publish assumptions/data and decide any normative change |
| 7 | R07: ACS | [Pinned schema adapter and local allow/deny/outage fixture](./acs-evidence-adapter.md) implemented and tested | Live upstream Guardian interoperability, independent tool observer and production bypass tests |
| 8 | R08: delegation cards | Optional structured mandate, identity, audience, scope, expiry, revocation and policy fields; example and negative validation tests | No live issuer, mandate validation or credential enforcement claimed |
| 9 | R09: evaluations/telemetry | Logical mapping and output requirements documented in ACS note | Native Inspect/AgentDojo importer, pinned OTel instrumentation and one reproducible scenario still open |
| 10 | R10: indirect effects | Explicit asynchronous/cumulative-effect test matrix proposed | Execute against a real boundary with external receipts and measured latency/exposure |
| 11 | R11: adoption/release ledger | Guidance, local implementation, tested integration and external adoption separated; indexes/changelog updated for tag `v0.5.11` | Future revisions must keep release metadata aligned; external adoption remains unverified |
| 12 | R12: OECD/independent assessment | Existing [visibility plan](./oecd-visibility-plan.md) retained | No submission sent, listing verified or independent reproduction completed |

## Reproduce This Pass

Use [`../tools/README.md`](../tools/README.md): install local dependencies, fetch pinned ACS schemas, run unit tests and repository validation, then run the demo/export/schema check. Dependency installation and schema retrieval need network access; subsequent checks are offline. The generated source kind is `local_fixture`, never `captured_acs`.

The tests validate the utilities and synthetic host, not measured failure rates of deployed agents. The unrelated untracked DAREB note is outside this change set. Historical assessment JSON files are not re-signed or re-rated.

Verification on 2026-10-26: 25 unit tests passed; four historical/example profiles and one component card passed repository validation; the allow/deny/outage fixture exported a schema-valid bundle with only the allowed action executed. Negative CLI cases returned nonzero and retained failed/inconclusive bundles. Shell syntax and whitespace checks passed; no new broken relative file links were found across the changed Markdown files. These results do not close the live or independent tests above.

## Next Execution Order

Finish R05/R06 comparative scenarios before changing classification rules. Then run R07 against the pinned upstream implementation, add the R09 native exporter and execute R10's async/isolation suite. Use the reproducible packet for independent assessment before seeking OECD listing or implying external adoption.
