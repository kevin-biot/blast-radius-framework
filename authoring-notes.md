# Authoring Notes

*How this repository — and specifically the Lane2 self-assessment artefacts — were produced. Transparent provenance of method, not just of content.*

**Last updated:** 2026-04-21

---

## The method: human domain-holder + AI epistemic partner, with a force function

This repository was produced by two roles operating in iteration:

- **Human domain-holder** (Kevin Brown, Lane2) — holds the architectural truth across the Lane2 stack and its public and private repositories; knows what exists, what is spec vs what is implemented, what the internal IP boundaries are.
- **AI epistemic partner** — reads public artefacts and the repos it is given access to, drafts candidate ratings and narratives from visible evidence, defaults to conservative attestation in absence of full-stack visibility.

Neither role alone produces an accurate architectural assessment. A lone AI under-claims because it cannot discover what it does not know to look for. A lone human domain-holder has inside-view attachment and may not see what an outside reader would need to see. The combination converges on accurate — but only if a specific force function is engaged.

## The force function

The pattern that produces credible output:

1. **AI produces candidate** from visible evidence.
2. **Human domain-holder anchors on under-attestations** with minimal pointer prompts — *"check X again"*, *"what about Y"*, *"have a closer look at Z"*. Not answers — pointers.
3. **AI digs into the repo code bases** on each pointer, opening files it had not opened, reading architecture docs and specifications. Depth-into-repo, not rephrase-from-memory.
4. **Honest correction published** with transparent change-log entry, version bump, prior versions retained in git. The correction trail *is* the credibility.
5. **Iterate** until the human domain-holder stops pointing at under-attestations.

## Evidence this pattern operated on this repository

The Lane2 [self-assessment](./reports/lane2/self-assessment.md) went through **seven versions in one calendar day** (v1.0 through v1.5) across framework releases v0.5.2 through v0.5.7. Each version closed an under-attestation the AI could not have discovered alone. See [CHANGELOG.md](./CHANGELOG.md) for the correction chain. Examples of what the force function surfaced:

- **I5** upgraded from `partially_holds / structural` to `holds / architectural` after Kevin pointed at aARP + RTGF + Shared Ontology as the core jurisdictional mechanism
- **I2 and I7** strengthened by citing the existing OBO + A2A reference implementation at [`kevin-biot/obo-standard/examples/integrations/a2a/`](https://github.com/kevin-biot/obo-standard/tree/main/examples/integrations/a2a) — which the AI had not opened until prompted to
- **PACT three-layer distinction** (public spec extraction / private internal ontology + tooling / deployer-authored production packs) clarified after the AI's first-pass conflated the three layers
- **A15 architectural demotion at decision path** cited from `pact-public/docs/architecture/security-unsigned-error-instruction-injection.md` and `intent-first-bounded-execution-pattern.md` — architecture docs the AI had not consulted in the first pass
- **SAPP role-based API surface** with the regulator/customer/integrity endpoints cited only after Kevin pointed at their existence

Every correction cited existing evidence more precisely. No correction retracted a claim that had been accurate.

## Why this matters for any reader producing their own BR rating

A self-assessment produced by an AI alone is not a self-assessment. It is a generative approximation of what a self-assessment would look like if the architecture were knowable from the AI's accessible evidence. For BR-3+ attestations — where specialist underwriters, regulators, and auditors will consume the rating — the force-function discipline is not optional.

The anti-pattern this method specifically counters:

- **A14 — autonomy-slider / approval fatigue** (see [antipatterns.md](./antipatterns.md)). Applied to assessment authoring, A14 becomes "AI drafts, busy human glances and ships, candidate becomes final". That is the mechanism by which AI drift enters a published artefact carrying a human signature. The demotion path — moving A14 from `exhibited` to `not_exhibited` for an authoring process — is exactly the force-function pattern documented here: candidate output is never accepted without the domain-holder actively pointing at under-attestations and obligating the AI to dig.
- **A7 — LLM-as-judge / recursive agent evaluation**. An AI assessment that receives only AI review does not escape A7. The human domain-holder is the ground-truth gate.

## Prescription for deployers applying this framework to their own systems

If you are producing a Blast Radius self-assessment, vendor attestation, or any architectural rating under this framework:

1. **Assume the first-pass candidate is under-attested.** Its errors are not random — they are systematic conservative defaults in places the AI could not see the architecture.
2. **Be prepared to point at specific under-attestations** from your own domain knowledge. Short pointers ("check X", "what about Y") work; full answers are not needed — the AI should dig on the pointer.
3. **Require a change-log entry and version bump for each correction.** Prior versions retained in git. A rating that required no corrections should be suspect; a rating with a transparent correction chain is stronger, not weaker.
4. **Iterate until you stop seeing under-attestations, not until the AI declares convergence.** The AI will converge on what it can see; you are the gate for what it cannot.
5. **Publish the authoring method** alongside the rating. Self-attestation by an AI alone is materially different from self-attestation produced under the force function; downstream readers (regulators, underwriters) should know which they are consuming.

## Operational reading

At the meta-level, this repository is itself a worked example of how a framework can be applied honestly to its own creation. The framework's own authors produced its central worked example (the Lane2 self-assessment) under the force function; the framework's own anti-patterns (A14, A7) classify the failure mode the method avoids; the framework's own honesty discipline (publish corrections transparently, retain prior versions, version-bump each change) is exercised on the authoring process itself.

The framework is usable in isolation. It is *credible* because it has been subjected to its own tests.
