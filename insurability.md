# Insurance Evidence and Blast Radius

*An underwriting evidence companion, not a coverage or pricing model.*

**Version:** 0.2
**Reviewed:** 2026-10-26; supersedes the April 0.1 conclusions
**Companions:** [framework](./framework.md), [claims policy](./adoption/claims-and-evidence.md), [public-criteria crosswalk](./adoption/crosswalk-specialist-underwriters.md)

## 1. What BRF can contribute

A BRF assessment describes reachable actions, affected populations, coupling, reversibility, consequence and observability in a declared deployment. It can help an insurer or broker ask better questions and inspect evidence. A BR class is neither a coverage decision nor a loss distribution.

Keep four conclusions separate: the architecture's reachable effects; the evidence supporting that description; legal compliance; and insurance coverage under a named policy. A runtime can check a technical permission but cannot decide the external validity of the corporate mandate or the policy contract.

## 2. Evidence packet for underwriting discussion

| Question | Useful BRF material | Additional evidence needed |
|---|---|---|
| What can act, on whose behalf, and within what limit? | A-axis, component cards and delegation context | Issuer/mandate records, contracts and tested admission paths |
| Who or what can be affected? | R/K, deployment graph and population accounting | Exposure units, geography and aggregation across customers |
| Can failures propagate? | C, topology and isolation tests | Common-cause incidents, shared infrastructure and bypass tests |
| Can effects be reversed? | V, rollback and compensation tests | External receipts, recovery time and unrecoverable losses |
| Can decisions be reconstructed? | O, policy snapshots, signed evidence | Verified provenance, completeness and retention/access controls |
| How often and how severely does failure occur? | Versioned evaluation and incident results | Representative denominators, loss data, dependence and uncertainty |
| Is the proposed loss covered? | A scoped evidence packet | Actual wording, endorsements, exclusions, limits and insurer determination |

Signed evidence helps detect alteration under stated trust assumptions. It does not prove a claim true, make a trace complete, establish legal admissibility or imply low measurement error.

## 3. Quantitative limits

Frequency (λ), loss severity (called σ in the historical BRF narrative) and uncertainty (υ) require a defined product, exposure and observation process. They are not recoverable from an ordinal BR class alone.

The optional cardinal score and Kalman extension are research models. Their normalization, weights, observation model, bias, covariance and calibration need publication and validation. **σ_B(t) is uncertainty in a proposed index, not a validated identity with actuarial υ.** Neither a small σ_B nor a missing cardinal score determines whether an insurer can quote.

Composition requires explicit assumptions. Typed interfaces do not alone prove containment; a shared model, policy service or credential can create common causes. Use conditional probabilities and exposure budgets rather than arithmetic on BR classes. See the [validation programme](./adoption/execution-boundary-research.md).

## 4. What current public offerings establish

The [October review](./adoption/external-review-2026-10.md) records distinct public offerings for model performance, agent liability and assurance-backed coverage. The [specialist crosswalk](./adoption/crosswalk-specialist-underwriters.md) maps public due-diligence themes. These materials establish that offerings exist, not that BRF or any assessed deployment has been accepted by an insurer.

For a coverage statement, record the named insurer/product, insured entity, covered activity, jurisdiction, policy period, wording/endorsements, limits, exclusions and the source of the decision. Otherwise state **coverage not established**. Do not infer the effect of a Verisk form or any endorsement without the applicable contract.

## 5. Correction record

The April companion argued that BRF invariants and insurability were equivalent, that nondeterminism made systems unpriceable, and that absent evidence universally blocked regulated deployment. Those categorical conclusions are withdrawn. The architectural questions remain useful, but the legal and commercial conclusions require separate evidence.

Historical assessments retain their numeric profiles and dated provenance; this correction does not re-sign, re-rate or independently verify them. The remaining research agenda is to publish reproducible boundary tests, calibrated measurements and an independent assessment before claiming quantitative or market validation.
