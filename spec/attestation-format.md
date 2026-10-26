# BR Attestation Format

*Signed, anchored, verifiable — the output a vendor produces to claim a BR profile.*

**Version:** 0.1.1
**Date:** 2026-10-26
**Part of:** [spec/](./) — machine-readable conformance artefacts for the Blast Radius Framework

---

## Purpose

A BR profile (`br-profile.schema.json`) is the *content*. An **attestation** is the signed, anchored, third-party-verifiable *form* that content takes when a deployer, integrator, or vendor claims a BR rating.

An attestation is what an auditor, underwriter, or regulator receives. Signing and anchoring support attribution and integrity under the verifier's trust assumptions. They do not establish factual truth, legal admissibility, regulatory compliance, or insurance coverage on their own.

This specification defines:

1. The canonical serialisation of a profile
2. The signature envelope
3. The anchoring requirement
4. The verification procedure

---

## 1. Canonical serialisation

Profiles are serialised as JSON following **JCS (JSON Canonicalization Scheme, RFC 8785)** before signing. JCS specifies:

- UTF-8 encoding
- Sorted object keys (lexicographic)
- No insignificant whitespace
- Numbers in shortest-round-trip form
- `\u` escapes only where required

The canonical serialisation is deterministic: two implementations of JCS produce byte-identical output for the same logical input. This makes signatures reproducible.

**COSE:** legacy schemas allow the COSE-Sign1 label, but this revision does not define an interoperable COSE payload profile. Do not claim BRF-JCS-0.1.1 conformance for a COSE envelope. A separately specified and tested COSE profile is future work.

---

## 2. Signature envelope

A signed attestation is a JSON object with the profile content plus a `signature` object:

```json
{
  "schema_version": "0.1.1",
  "framework_version": "0.5",
  "profile_id": "...",
  ...
  "signature": {
    "algorithm": "Ed25519",
    "signer_id": "did:web:example.com:attestations:2026-q2",
    "signature_value": "base64...",
    "payload_profile": "BRF-JCS-0.1.1",
    "signed_payload_canonical_form": "JCS-RFC8785",
    "signed_at": "2026-04-21T10:30:00Z"
  }
}
```

### Signing procedure

New JSON attestations MUST declare `signature.payload_profile: "BRF-JCS-0.1.1"` and `signed_payload_canonical_form: "JCS-RFC8785"`.

1. Populate the profile and the complete signature metadata, including `algorithm`, `signer_id`, `signed_at`, canonical form, and payload profile.
2. Copy the object, remove the top-level `anchor` member, and set the existing `signature.signature_value` member to the empty string. Keep every other member, including unknown extension fields.
3. JCS-canonicalise that copy and sign those bytes with the declared algorithm.
4. Replace the original object's empty `signature_value` with the base64 signature. Add the external anchor only after signing.

Verification MUST reconstruct exactly the same copy. Removing `signature_value` entirely is a different byte sequence and is invalid for this profile. This is a BRF payload convention, not a JWS envelope. Legacy v0.1 attestations omitted the payload-profile marker and admitted ambiguous constructions; reissue them or verify only with an explicitly documented historical construction. Never guess which construction verifies.

The reference byte construction and HMAC-only test helper are in [`../tools/attestation_payload.py`](../tools/attestation_payload.py). HMAC test vectors demonstrate byte handling; they provide no independent witness or asymmetric signature verification. COSE deployments require their own explicit, interoperable COSE profile; this helper does not implement one.

### Algorithm selection

| Algorithm | When to use |
|---|---|
| **Ed25519** | Recommended default. Deterministic, compact, fast, no parameter choices. |
| **ES256** (ECDSA P-256) | When HSM or existing PKI restricts to NIST curves. |
| **ES384** (ECDSA P-384) | High-assurance deployments where P-256 is considered insufficient. |
| **RS256** (RSASSA-PKCS1-v1_5 with SHA-256) | Only where the receiver requires this RSA algorithm. |
| **PS256** (RSASSA-PSS with SHA-256) | RSA-PSS deployments; distinct from RS256 per [RFC 7518](https://www.rfc-editor.org/rfc/rfc7518.html). |
| **HMAC-SHA256** | Only for intra-organisation attestations with out-of-band key exchange. Not suitable for external distribution. |

### Key management

For BR-3+ attestations, signing keys must:

- Be stored in HSM or equivalent hardware-backed key store
- Have a documented rotation schedule (at least annually)
- Have a compromise-response procedure
- Be referenced by a stable signer_id that resolves to a publishable key history

For BR-4+ attestations, add:

- Key ceremonies witnessed or video-recorded
- Dual control on key generation
- Evidence of the HSM's attestation certificate

For BR-5 attestations:

- Independent auditor review of key management
- Annual penetration test of the signing infrastructure

---

## 3. Anchoring requirement

A signature proves the attestation was made by the holder of a private key at some point. An **anchor** proves the attestation existed at a specific time and has not been substituted.

Anchoring is required for BR-4 and BR-5. Recommended but optional for BR-3.

### Acceptable anchor types

**SAPP (Lane2's Secure Agent Payment Protocol — evidence-anchoring layer)** — recommended reference design. Independent signing keys, Merkle-proof commitments, evidence scoring, liability allocation built in. Cryptographically anchors a Merkle root covering the signed attestation. Third-party verifiers can retrieve the root and confirm inclusion. (SAPP's full scope is compliant cross-organisational payments with cryptographically verified regulatory adherence; the evidence layer is what attestation-format targets.)

**OpenTimestamps** — suitable for attestations that do not need the scoring/liability machinery SAPP provides. Anchors a hash to the Bitcoin blockchain; timestamp is proven by block inclusion. Free, public, permissionless.

**RFC 3161 TSA (Time-Stamping Authority)** — suitable where a trusted third-party TSA is already in the deployer's PKI. Produces a TSA-signed timestamp token over the attestation hash.

**Custom Merkle proof** — acceptable if the deployer operates an append-only log with independent witness (e.g. certificate-transparency-style). Must be specified in `anchor.anchor_type` as `MerkleProof-Custom` with `anchor_uri` resolving to the log.

### Anchor binding

The anchor commitment binds to the canonical serialisation of the attestation payload (profile + signature):

```
anchor_commitment = Merkle_root(...attestations in the batch... including our attestation hash)

where:
attestation hash = SHA-256(JCS(profile with populated signature, excluding top-level anchor))
```

A verifier recomputes the attestation hash and verifies inclusion in the Merkle root.

### Anchor freshness

Anchors have a timestamp. The anchor timestamp must not be more than a specified skew behind the `signature.signed_at`:

| BR Class | Maximum anchor-to-signature skew |
|---|---|
| BR-3 | 24 hours |
| BR-4 | 1 hour |
| BR-5 | 5 minutes |

Larger skew means the attestation was held before anchoring, which permits undetected substitution. The BR-5 tolerance is tight because the whole insurability frame rests on evidence that resists this attack.

---

## 4. Verification procedure

An auditor, underwriter, or regulator verifies an attestation as follows:

### Step 1 — Recover the public key

1. From `signature.signer_id`, resolve the public key:
   - `did:web:example.com:attestations:2026-q2` → fetch the DID document, find the verification method for the `2026-q2` key
   - X.509 subject → validate the certificate chain to a trusted root
   - Fingerprint → look up in the trust list the verifier already has

2. Confirm the key is in-date: the attestation's `signed_at` must fall within the key's validity period.

### Step 2 — Verify the signature

1. Require a supported `payload_profile`; for BRF-JCS-0.1.1, remove the top-level `anchor` and set `signature.signature_value` to the empty string on a copy
2. JCS-canonicalise that copy, preserving all other metadata and profile members
3. Verify the signature over the canonical bytes using the recovered public key
4. Confirm the algorithm matches `signature.algorithm`

### Step 3 — Verify the anchor (BR-3+ if present; BR-4+ required)

1. Resolve `anchor.anchor_uri` and retrieve the proof
2. Compute the attestation hash as `SHA-256(JCS(payload including the populated signature but excluding the top-level anchor))`
3. Verify Merkle inclusion (or TSA token, or blockchain inclusion) using the proof
4. Confirm `anchor.anchor_timestamp` is within allowed skew from `signature.signed_at`

### Step 4 — Verify profile consistency

1. Confirm `schema_version` matches a known schema
2. Validate the profile against `br-profile.schema.json`
3. Recompute `aggregation.ordinal_class` from the axes and modifiers, confirming agreement with the declared class
4. If `aggregation.cardinal_score` is present, require the calibration, observations and filter state needed to reproduce it. A filtered estimate cannot in general be reproduced from current axis tiers alone; mark it unverified when those inputs are absent. The score does not establish insurance coverage.

### Step 5 — Spot-check invariant claims

For each invariant with `conformance_test_results`:

1. Retrieve the test result artefact from `evidence_uri`
2. For at least one test per invariant per BR-3+ attestation, re-run the test and confirm the result

### Step 6 — Check attestation expiry

1. If `attestation_expiry` has passed, the attestation is stale. Insurability and regulatory claims must not be made on stale attestations.

An attestation that passes all six steps is accepted. Failures are documented with the step at which verification failed; the attestation is rejected.

---

## 5. Composition attestations

When System X composes with System Y (per `framework.md §7.1` pairwise composition rule), the composed profile must carry:

- Its own signature and anchor
- A reference to Y's independent attestation (signed by Y's deployer, anchored independently)
- The computed composed profile with §7.1 rules applied

The verifier performs Step 1–6 on both the composed attestation and Y's original. Rejection of Y's attestation cascades to the composed attestation.

This mirrors SOC 2 subservice organisation scoping.

---

## 6. Re-attestation triggers

A profile is point-in-time. Re-attestation is required on any of:

- Expiry of `attestation_expiry`
- Material change to any component (new tool, new reach, new integration)
- Trajectory review finding τ = drifting (material change observed)
- Key rotation (old signature still verifies historically, but new attestations must use the current key)
- Policy snapshot rotation where the new snapshot materially changes behaviour

A trivial re-attestation (no content change, just re-signature with current key) is acceptable at shorter cadences than the maximum expiry; deployers may re-attest monthly for operational signal even if the profile content is unchanged.

---

## 7. Interoperability notes

### With SAPP

SAPP's Merkle-anchored evidence infrastructure is the reference anchor for BR-4+ attestations. A BR attestation's `anchor.anchor_commitment` maps directly to the SAPP evidence record's commitment; the SAPP evidence scoring (10 categories, 0–1.0) can supplement the BR profile's `aggregation.cardinal_score.sigma_B`.

### With existing PKI

X.509 certificates, DIDs, JWKS endpoints, and similar existing PKI are acceptable for `signer_id` resolution. The schema does not prescribe a PKI — it prescribes that the PKI exists and is resolvable.

### With regulatory filings

BR attestations can support regulatory evidence packets. Article 26(6) concerns deployer log retention; it is not a general authority-access provision. An attestation does not replace the underlying logs, technical documentation or monitoring records. Apply the role, category and dates in the [current EU crosswalk](../adoption/crosswalk-eu-ai-act.md).

### With insurance submissions

Specialist underwriters (Munich Re aiSure, AIUC, Armilla via Lloyd's) can ingest a BR attestation as their minimum viable disclosure. `aggregation.cardinal_score.B_hat` and `sigma_B` populate directly into actuarial pricing models as the λ/σ/υ inputs. `anti_patterns` provides the disclosure the questionnaire in `framework.md §17` requires.

---

## 8. What an attestation is not

- **Not a guarantee.** An attestation is evidence of a claim, not a warranty that the claim will hold in all conditions. Insurability and regulatory admissibility depend on the attestation being honest, verifiable, and current.
- **Not a product endorsement.** Anyone can sign an attestation for their own system. Third-party certification (a separate auditor signing) is a stronger form and may be required by specific regulators or underwriters.
- **Not a legal opinion.** Regulatory mapping (K sub-tags, jurisdictional enforcement) is the deployer's claim. A regulator may disagree; the attestation is admissible evidence, not binding determination.

---

## 9. Open questions

1. **Third-party certification schema.** A separate attestation form for independent auditors (who sign a review of a deployer's self-attestation) is deferred to v0.2 of this spec.
2. **Anchor aggregation.** If a deployer operates many attestations, batching them under a single anchor reduces anchor cost. Batching semantics and per-attestation proof-of-inclusion are standard Merkle operations but not yet specified here.
3. **Revocation.** An attestation may need to be revoked before expiry (discovered flaw, key compromise, material fact changed). A revocation list mechanism (CRL-style or OCSP-style) is a v0.2 item.
4. **Translation from natural-language questionnaires.** The `framework.md §17` questionnaire is prose; a reference tool that converts a filled questionnaire into a valid profile is a v0.2 item.
