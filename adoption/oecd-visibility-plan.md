# OECD Visibility Plan

*Plan for making BRF discoverable inside the OECD Catalogue of Tools & Metrics for Trustworthy AI ecosystem.*

**Gap addressed:** missing visibility inside the OECD ecosystem
**Status:** plan
**Date:** 2026-04-23

---

## 1. Goal

The goal is straightforward:

- people who start from the OECD catalogue should be able to discover BRF
- they should understand what BRF is without confusing it for a generic model-metrics library

This is a distribution task, not a framework-definition task.

---

## 2. What to submit

There are two sensible OECD-facing submissions:

1. **BRF as a procedural / governance tool**
2. **A worked example as a use case**

The first is the priority. The second should follow once the first is stable.

---

## 3. Submission posture for BRF itself

Recommended framing:

- tool type: procedural / governance / audit / risk management
- problem solved: operational blast-radius classification for deployed agentic systems
- distinctive feature: architecture-first rating, compositional reasoning, attestable profile shape, invariant-based evidence expectations
- what it is not: not a model benchmark leaderboard; not a generic trustworthiness checklist; not a substitute for law, audit, or insurance underwriting

Key artefacts to cite:

- [`../README.md`](../README.md)
- [`../framework.md`](../framework.md)
- [`../spec/README.md`](../spec/README.md)
- [`../oecd-catalogue-assessment.md`](../oecd-catalogue-assessment.md)

---

## 4. Submission posture for a worked example

The most obvious candidate is the Lane2 worked example in [`../reports/lane2/`](../reports/lane2/).

Use it to show:

- what a populated BR profile looks like
- what honest gaps look like
- how executive, technical, and remediation layers compose

Avoid presenting it as universal evidence of the framework's correctness. Present it as:

- a worked example
- a self-assessment
- a transparent demonstration of method

---

## 5. Dependencies before submission

Before submitting BRF into the OECD ecosystem, make sure:

1. the OECD comparison note is published
2. the adoption-workstream docs in this directory exist
3. the repo front page points clearly at both
4. the wording is consistent about what BRF does and does not do

These conditions are now materially satisfied in this repo.

---

## 6. Suggested metadata

Minimum metadata to prepare:

- name
- short description
- category / tool type
- target audience
- link to primary documentation
- link to machine-readable artefacts
- link to worked example
- maintainer contact
- licence

This should be drafted once and reused across OECD submission, website copy, and future partner briefings.

---

## 7. Why this closes the gap

The gap was simply that useful people looking in the OECD ecosystem would not find BRF there.

This plan closes that by defining:

- what to submit
- how to frame it
- which artefacts to cite
- what must be in place before the submission is made
