# Questionnaire to Profile Conversion

*Design note for tooling that converts the BRF vendor questionnaire into a draft machine-readable BR profile.*

**Gap addressed:** missing questionnaire-to-profile tooling
**Status:** design note
**Date:** 2026-04-23

---

## 1. Goal

BRF already has:

- a prose vendor questionnaire in [`../framework.md`](../framework.md)
- a machine-readable target shape in [`../spec/br-profile.schema.json`](../spec/br-profile.schema.json)

The missing tool is the bridge between them.

The converter should:

1. ingest structured answers to the questionnaire
2. draft a schema-valid profile wherever possible
3. flag unresolved evidence and inconsistencies explicitly
4. never silently convert narrative uncertainty into false precision

---

## 2. Inputs and outputs

### Input

A structured questionnaire object, ideally JSON, with:

- one field per questionnaire item
- optional evidence references
- optional confidence / completeness annotations

### Output

A package with three artefacts:

1. **draft BR profile**
2. **open issues report**
3. **consistency warnings report**

The converter should never emit only the profile. The unresolved and warning artefacts are part of the output contract.

---

## 3. Conversion discipline

### 3.1 Direct mappings

Some questionnaire items map directly:

| Questionnaire area | Profile target |
|---|---|
| tuple disclosure | axis tiers |
| composition disclosure | `composition` object |
| invariants | `invariants` object |
| anti-pattern attestation | `anti_patterns` object |
| reversibility plan | `V` narrative and evidence refs |
| observability evidence | `O` narrative and evidence refs |

### 3.2 Derived mappings

Some fields require derivation:

| Source answer | Derived target |
|---|---|
| interaction override explanations | `aggregation.ordinal_class` rationale |
| underwriter disclosure + evidence quality | `aggregation.cardinal_score` readiness |
| modifiers narrative | `delta_adv`, `tau`, residual-vs-inherent sections |

### 3.3 Non-convertible answers

Some answers must remain unresolved unless stronger evidence is supplied:

- vague statements like "monitored continuously"
- undocumented claims like "fully reversible"
- policy claims without snapshot references
- open-world systems claiming BR-2 or BR-3

The converter must emit these as explicit unresolved items rather than guessing.

---

## 4. Output structure

Suggested output package:

```text
conversion-output/
  draft-profile.json
  open-issues.json
  warnings.json
  conversion-summary.md
```

### `open-issues.json`

Use for missing evidence or unresolved fields:

```json
[
  {
    "field": "invariants.I2",
    "severity": "blocking",
    "reason": "evidence binding claimed but no signature or anchor evidence supplied"
  }
]
```

### `warnings.json`

Use for inconsistency or plausibility problems:

```json
[
  {
    "field": "components[1].worldview",
    "severity": "high",
    "reason": "open-world component conflicts with declared BR-3 final class"
  }
]
```

---

## 5. Rules the converter must enforce

1. **Schema validity is necessary, not sufficient.**
   A valid JSON object is not automatically a credible profile.

2. **Open-world floor must be enforced.**
   If any component is open-world, BR-4 minimum applies.

3. **Derived values must be explainable.**
   Every computed or inferred field should carry a rationale trace.

4. **No silent defaulting on high-stakes fields.**
   Invariants, composition, worldview, and consequence should never be silently filled.

5. **Evidence references are first-class.**
   The converter should preserve which answer supported which profile field.

---

## 6. Suggested implementation phases

### Phase 1 — deterministic mapper

- JSON input only
- no natural-language parsing
- explicit field-to-field mapping

### Phase 2 — assisted intake

- form UI or CLI wizard
- controlled vocabulary for common answers
- built-in consistency checking

### Phase 3 — guided narrative extraction

- optional assisted extraction from prose answers
- always produces unresolved items for human confirmation

The sequence matters. Phase 1 should ship before any language-assisted intake is attempted.

---

## 7. Why this closes the gap

The gap was not the lack of a questionnaire or the lack of a schema. The gap was the absence of a disciplined bridge between them.

This converter design closes that by defining:

- the input contract
- the output contract
- the non-silent error model
- the enforcement rules that prevent cosmetic profile generation
