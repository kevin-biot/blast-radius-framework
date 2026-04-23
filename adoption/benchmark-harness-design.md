# Benchmark Harness Design

*Design note for a BRF benchmark and invariant-test companion repository.*

**Gap addressed:** missing reference harness
**Status:** design note
**Date:** 2026-04-23

---

## 1. Goal

The goal of the harness is not to replace the prose spec. The goal is to provide a reproducible execution layer that can:

- run BRF benchmark scenarios against realistic agent systems
- exercise invariant-oriented tests in a repeatable way
- emit signed result bundles attachable to a BR profile or attestation

The companion repo should make it easier to move from:

- "the framework says this should be tested"

to:

- "here is the result bundle showing how it was tested"

---

## 2. Scope

The harness should cover two classes of work:

1. **Archetype benchmarks**
   - customer support
   - code assistant
   - research agent
   - RAG workflow
   - clinical decision support
   - financial / payments operations

2. **Invariant-oriented conformance runs**
   - reproducibility
   - evidence binding checks
   - policy snapshot coherence
   - blast-radius containment
   - boundary integrity
   - observability / replay
   - bounded coupling

The harness should **not**:

- compute a final BR class automatically without disclosed human review
- substitute for the attestation verifier
- hide topology and trust assumptions inside the runner

---

## 3. Repository shape

Suggested top-level layout:

```text
brf-harness/
  README.md
  scenarios/
    archetypes/
    invariants/
  manifests/
    environments/
    systems/
    policies/
  runners/
  outputs/
    schema/
    examples/
  sign/
  docs/
```

### Key directories

- `scenarios/archetypes/` — scenario definitions for common system types
- `scenarios/invariants/` — one runnable scenario bundle per invariant test family
- `manifests/environments/` — environment contracts, including tool interfaces, tenancy model, reach boundaries, and reset semantics
- `manifests/systems/` — target-system descriptors so the runner knows what is under test
- `outputs/schema/` — JSON schema for the result bundle
- `sign/` — signing and anchoring helpers for result bundles

---

## 4. Execution model

Each run should have four inputs:

1. **target system manifest**
2. **environment manifest**
3. **scenario manifest**
4. **policy snapshot reference**

The runner should:

1. resolve the target and environment
2. execute the scenario under controlled conditions
3. capture traces, outputs, and failure modes
4. evaluate scenario-specific pass/fail criteria
5. emit a result bundle with provenance and hashes

The result should be a bundle that another party can inspect without rerunning the entire scenario immediately.

---

## 5. Result bundle shape

Minimum output object:

```json
{
  "bundle_version": "0.1",
  "run_id": "uuid-or-content-address",
  "scenario_id": "I4-T1-tenant-isolation",
  "target_system_id": "example-system",
  "target_system_version": "git-sha-or-release",
  "policy_snapshot_id": "policy-2026-04-23-001",
  "environment_id": "payments-sandbox-v1",
  "started_at": "2026-04-23T10:00:00Z",
  "completed_at": "2026-04-23T10:07:00Z",
  "operator": {
    "type": "human|ci|auditor",
    "id": "..."
  },
  "artifacts": [
    {
      "type": "trace|log|screenshot|event-stream|report",
      "uri": "...",
      "sha256": "..."
    }
  ],
  "evaluation": {
    "status": "pass|fail|inconclusive",
    "criteria": "...",
    "summary": "..."
  },
  "limits": [
    "what this run does not prove"
  ],
  "signature": {},
  "anchor": {}
}
```

This bundle should be suitable for reference from a future BR profile field such as:

- `invariants.I4.conformance_test_results[].evidence_uri`

---

## 6. Design principles

### 6.1 Environment realism over toy prompts

The harness should prefer realistic task environments over benchmark trivia. The point is to observe behavior under authority, reach, coupling, reversibility, and observability constraints.

### 6.2 Resettable state

Every environment must define:

- reset semantics
- tenancy boundaries
- rollback support
- known irreversibilities

Without reset semantics, repeated runs become non-comparable.

### 6.3 Threat-model explicitness

Every adversarial or misuse scenario must declare:

- attacker position
- allowed inputs
- accessible channels
- success criteria

Otherwise `delta_adv` outputs become uninterpretable.

### 6.4 Signed outputs

The harness should produce result bundles that can be signed and, where appropriate, anchored independently. Otherwise benchmark outputs remain narrative evidence rather than audit-grade evidence.

---

## 7. Minimum viable release

The first release should be deliberately small:

1. one environment abstraction
2. one archetype scenario
3. one invariant scenario each for I1, I4, I6, and I7
4. one result-bundle schema
5. one signing flow

That is enough to prove the harness shape without overcommitting the repo.

---

## 8. Why this closes the gap

The missing piece was not "more benchmark scores." The missing piece was a disciplined way to generate **attestable runtime evidence** aligned to BRF claims.

This harness design closes that by specifying:

- what to run
- how to run it
- what to emit
- how to preserve the result for later audit
