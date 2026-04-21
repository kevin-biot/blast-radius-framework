# Reports

*Reusable report templates and worked examples of the Blast Radius Framework applied to real (or realistic) systems.*

This directory has two things:

1. **[`templates/`](./templates/)** — three reusable report templates, one per tier, for producing a Blast Radius report against any deployed or proposed agentic system
2. **Per-system subdirectories** — one per rated system, each containing a completed assessment using the templates. Currently:
   - **[`lane2/`](./lane2/)** — Lane2 applying the framework to its own integrated governance platform (the framework's authors rating their own stack honestly)

---

## How reports compose

A complete Blast Radius report is a set of three files plus a machine-readable profile:

```
{system-name}-exec-summary.md           — Tier 1, 1–2 pages, non-technical
{system-name}-technical-findings.md     — Tier 2, detailed, schema-linked
                                          (or .md with "self-assessment.md"
                                          style naming when the deployer
                                          self-attests)
{system-name}-adr-backlog.md            — Tier 3, prioritised ADR candidates
{system-name}-profile.json              — conformant to spec/br-profile.schema.json
```

The three tiers are produced from the three templates in [`templates/`](./templates/). The profile is produced against [`../spec/br-profile.schema.json`](../spec/br-profile.schema.json).

Each tier is self-contained. A reader can consume any one without reading the others. Cross-references between tiers are preferred over restating content. Tier 1 is the board/executive/underwriter summary; Tier 2 is the architecture team's detailed assessment; Tier 3 is the remediation backlog derived from Tier 2's gaps.

## How to produce your own report

1. Read [`../framework.md`](../framework.md) (the rating framework specification, v0.5.1 or later) and [`../NOTATION.md`](../NOTATION.md) (quick reference).
2. Read [`../authoring-notes.md`](../authoring-notes.md) — the method under which credible reports are produced (human-domain-holder + AI-epistemic-partner with a force function). A self-assessment by an AI alone is not a self-assessment.
3. Open [`templates/`](./templates/) and read the three template files.
4. Read [`lane2/`](./lane2/) as a worked example to calibrate what "populated" looks like.
5. Create a directory under `reports/` for your system (e.g. `reports/your-system-name/`). Populate the three tier files plus the profile by replacing `[SQUARE_BRACKET_PLACEHOLDERS]` in the templates with your values.
6. Validate your profile against [`../spec/br-profile.schema.json`](../spec/br-profile.schema.json) before publishing.
7. Sign and anchor per [`../spec/attestation-format.md`](../spec/attestation-format.md). Required for BR-3+; recommended always.

## Contributing worked examples

Worked examples from deployers applying the framework to their own systems are explicitly welcome in this directory. Open a pull request adding your subdirectory. Rules:

- Use fictional organisation names unless you have explicit sign-off to publish under real names
- Respect your own IP boundaries (redact internal paths, keys, customer names)
- Apply the force-function method documented in [`../authoring-notes.md`](../authoring-notes.md) — a candidate rating produced by AI alone is not acceptable as a contributed example
- Include the change-log of corrections if the assessment went through revisions
- Cite the framework version you rated against
