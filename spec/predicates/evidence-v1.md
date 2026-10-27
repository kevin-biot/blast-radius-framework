# BRF Evidence Predicate v1

**Predicate type:** `https://github.com/kevin-biot/blast-radius-framework/blob/main/spec/predicates/evidence-v1.md`

This custom in-toto predicate packages one BRF companion evidence file. It is not a SLSA provenance predicate, an in-toto supply-chain layout, a Sigstore bundle or a signed BR-profile attestation. Incompatible predicate changes require a new predicate URI.

## Statement and Envelope

The statement `_type` is `https://in-toto.io/Statement/v1`. Exactly one subject identifies the original evidence file's **exact bytes** by lowercase SHA-256. Its name is only a label, never an instruction to open a path or fetch a URL. Whitespace-only changes to the original file change the subject digest.

The DSSE `payloadType` is `application/vnd.in-toto+json`. Sign the DSSE v1 pre-authentication encoding of that UTF-8 media type and the serialized statement bytes. Do not reserialize or canonicalize the payload before signature verification. This profile uses Ed25519, supports a maximum of 32 signature entries and requires one valid signature against the one public key explicitly selected by the verifier. It implements no multi-key threshold policy. Additional DSSE envelope/signature fields are ignored; `keyid` is an unauthenticated hint and is never a trust decision.

The [statement schema](../evidence-statement.schema.json) defines these required predicate fields:

| Field | Meaning |
|---|---|
| `evidence_type` | `acs_trace`, `evaluation`, `execution` or `inventory_links` |
| `evidence_schema` | Respectively `acs-trace-evidence.schema.json`, `evaluation-evidence.schema.json`, `execution-evidence.schema.json` or `inventory-links.schema.json` |
| `issued_at` | Signer's declared creation time; not an independently trusted timestamp |
| `verification_scope` | Always `signature_and_subject_integrity_only` |
| `signing_context` | `caller_supplied_key` or `ephemeral_demo_key`; a signed declaration, not independent key provenance |
| `evidence` | Parsed contents of the original subject file, validated against the selected companion schema |

The verifier requires the supplied subject digest to match and the nested evidence to match its parsed contents without coercing booleans into numbers. Python's arbitrary-precision integers preserve nanosecond timestamps. Other consumers must preserve JSON value types and numeric precision when making the same binding check. This is not the RFC 8785 signing format used by native BRF attestations.

## Verification Boundary

Successful verification establishes that the authenticated payload was signed by a key corresponding to the supplied public key, and binds it to the supplied subject bytes. The caller must establish the key's owner, authorization, lifecycle and acceptance policy separately. No key discovery, certificate chain, organizational mandate, revocation service, freshness guarantee, transparency log, trusted timestamp, anchor proof or threshold trust store is implemented.

The original bundle is unchanged, including any native `signed: false`, `enforcement_status: not_verified` or unknown/inconclusive observations. Signing does not make those observations true, complete or independently assessed. A demo public key distributed beside an envelope is not evidence of an institutional signing identity.

## Upstream Basis

This profile follows [DSSE protocol 1.0.2](https://github.com/secure-systems-lab/dsse/blob/b531b787bb3e5f0c3e1c19cee84da1c5d569b061/protocol.md) and the [in-toto Statement v1 specification](https://github.com/in-toto/attestation/blob/df02077bf97218a8860a5c534eff1f1381f56984/spec/v1/statement.md), pinned to attestation release v1.2.0. It is a bounded implementation, not a claim of complete in-toto tooling conformance.
