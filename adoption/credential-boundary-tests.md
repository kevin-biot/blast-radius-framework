# Signed Credential Boundary Tests

**Date:** 2026-10-27
**Package:** Tooling v0.5.15; framework definitions 0.5.11 and profile spec 0.1.1 unchanged

This completes the next local implementation step in [identity and threat coverage](./alignment-implementation.md). The experiment checks signed runtime credentials at a separate HTTP tool boundary and observes durable effects. It does not establish a company policy, a business mandate, the real-world identity of a bearer, or legal authority.

## Task List

| Task | Acceptance Criteria | Result |
|---|---|---|
| C01: Credential checks | Real asymmetric tokens; fixed key/algorithm, issuer, audience, type, tenant, scope and time checks; no token-directed key discovery | Implemented with pinned PyJWT 2.15.1 and Ed25519 keys; positive and negative HTTP cases |
| C02: Isolation | Separate agent/control credentials; idempotency bound to tenant/principal/client; shared per-tenant budget | Implemented; context-bound receipts, request-field/header checks and concurrent-principal regression test |
| C03: In-flight changes | Pause a real request, change credential validity before commit and compare commit-time checking with an unsafe control | Revocation, actual expiry and unavailable local revocation state tested in both modes |
| C04: Explicit limits | Demonstrate already-committed residuals and bearer reuse without mislabeling them as new policy violations | Both controls retained; future work denied after revocation and reuse bounded by tenant budget |
| C05: Reproducible evidence | Export schemas, per-tenant receipts, source digests and a checkable packet without exporting credentials | Execution evidence 0.1.1 plus hash-bound context and issuer public key; check-only command; CI allowlist |
| C06: Threat mapping | Identify relevant OWASP categories and untested aspects | Selected mappings below; no full OWASP, OAuth, WIMSE or ACS conformance claim |

## Apparatus and Policy

The in-memory fixture issuer creates short-lived JWTs. Its private key is never serialized or sent to the tool process. The separate loopback tool receives only the fixture issuer's public key and its own administrative secret. The test harness holds both roles to inject failures; this is not hostile-host protection or independent assessment. No real identity provider, organization, production credential, external model or external network target is involved.

The tool fixes `EdDSA` with Ed25519 keys, issuer `https://issuer.example.invalid/brf-fixture`, audience `urn:brf:fixture:credential-ledger`, token type `at+jwt` and required scope `ledger:increment`. It requires issuer, subject, audience, expiry, issued-at, not-before, token ID, client ID, scope and the private `brf_tenant` claim. Integer timestamps, a maximum 300-second lifetime and zero leeway are fixture policy choices. Scope tokens use the syntax in [RFC 6749 section 3.3](https://www.rfc-editor.org/rfc/rfc6749.html#section-3.3). Ambiguous JSON, claim types and duplicate Authorization headers are rejected.

Signature, issuer and audience checks use the explicitly configured key and [PyJWT API](https://pyjwt.readthedocs.io/en/2.15.1/api.html), not values supplied by an untrusted token. These selected checks follow [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html) and the access-token distinctions in [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068.html). This is not a complete OAuth/OIDC authorization server or RFC 9068 implementation: it supports a deliberately narrow algorithm/audience/claim profile and local HTTP rather than a production TLS deployment.

JWT `kid` is part of the signed protected header, unlike DSSE's outer key hint. It still does not establish a trust anchor: this fixture ignores it for key selection. Key-discovery and unsupported critical headers are rejected, and no key URL, issuer URI or endpoint is fetched. A token signed by the wrong key cannot become trusted by naming the expected issuer or key hint.

Revocation is local state keyed by a digest of `(issuer, jti)`, not by the JWT's transport encoding. Reissuing the same credential identity with a different signed header does not evade revocation. Administrative revocation, availability faults and commits serialize through the same SQLite database. `commit_recheck` verifies current credentials and state inside the commit transaction; `admission_only` deliberately retains the earlier admission decision. The unavailability injection is a local state flag, **not** an external revocation-provider outage test.

## Cases and Results

The runner executes 34 fixed cases: 20 admission cases, three idempotency namespace cases, three retry/revocation/control-plane cases, six in-flight comparisons, and two residual/bearer controls. It uses no LLM sampling and estimates no population failure rate.

| Case Group | Required Observation |
|---|---|
| Valid credentials and a non-selecting key hint | One allowed commit per case |
| Wrong signature, tampered claims, issuer, audience, tenant, scope, token type/algorithm, time or required fields | Rejected request; no protected commit or other-tenant mutation |
| Pre-revoked credential, unavailable revocation state, admin secret used as access token | Rejected; unavailable state fails closed |
| Same operation ID in different tenant/principal/client contexts | Distinct authorized receipts, not another identity's cached response |
| Retry using a revoked credential; same issuer/token ID with changed encoding | Rejected before returning a cached receipt or creating an effect |
| Agent credential sent to an administrative endpoint | Rejected; no administrative mutation |
| Revoke, expire or make local state unavailable while paused before commit | Recheck mode commits zero; admission-only control commits one and records a violation |
| Revoke after commit but before response | Original one-unit effect remains; new work is denied; residual reported |
| Reuse a valid bearer under new operation IDs | Three allowed one-unit commits, then budget denial; holder binding is not provided |

All 34 predeclared outcomes matched in the local run, including three deliberately unsafe admission-only cases. Passing experimental expectations does not mean all modes are safe. The bearer-reuse control is not labeled a policy violation: possession is sufficient under this fixture's bearer semantics. It demonstrates that signature verification and idempotency do not prevent reuse under new operation IDs or prove who holds a credential.

The expiry cases wait for actual wall-clock expiry while the request is paused, with a bounded monotonic timeout. The harness then releases the request. These are local clock observations, not trusted timestamps or evidence about distributed clock skew. Revocation that acknowledges before the commit checkpoint blocks the selected strict cases; it cannot roll back an earlier commit or guarantee zero delay after every real-world revocation.

## Packet and Validation

`evidence.json` uses companion execution-evidence version **0.1.1** with `kind: credential_boundary`. Legacy ACS/async bundles remain valid as 0.1.0. This does not change BR-profile spec 0.1.1. The packet includes hash bindings to `credential-context.json` and `issuer-public.pem`; its source digests identify the fixture code and dependency pins. Existing DSSE `execution` packaging remains usable without changing the custom predicate URI.

The context records HTTP outcomes, candidate issuer/token-ID fingerprints, tenant balances and credential-bound receipt identities. Fingerprints for denied credentials are candidate identifiers, not proof of successful authentication. It contains no JWT, administrative secret, raw token ID or private key. Receipt principals and client IDs are verified fixture-issuer claims, not independently verified human identities.

The standard execution projection totals both tenant balances; `active` describes resource-grant state, **not** credential validity. Operation IDs need not be globally unique. Use the case and receipt sequence together with tenant, principal and client context; do not deduplicate across identities by operation ID alone.

```sh
bash tools/install-integrations-local.sh
.tools/integration-env/bin/python tools/run_credential_boundary.py --run-dir .tools/credential-example
.tools/integration-env/bin/python tools/run_credential_boundary.py --run-dir .tools/credential-example --check-only
python3 tools/validate_json_schema.py spec/execution-evidence.schema.json .tools/credential-example/evidence.json
python3 tools/validate_json_schema.py spec/credential-context.schema.json .tools/credential-example/credential-context.json
bash tools/check-alignment-local.sh
```

Execution requires a new directory and refuses to reset existing evidence. The check-only command starts no service: it validates schemas, capture/key bindings, case correlation and internal receipt/balance/summary arithmetic. It never follows an arbitrary capture path. These checks establish internal consistency, not authentic observation or external authority; a hostile producer can fabricate an internally consistent unsigned packet. Exit 0 means all expected outcomes matched, 1 means a valid packet with an experimental mismatch, 2 means invalid input or an operational failure.

CI retains only the execution bundle, credential context and issuer public key in addition to the earlier allowlist. Private signing keys are never written; temporary fixture-admin files are removed on ordinary shutdown, not guaranteed after a crash. Review identifiers and metadata before sharing non-fixture evidence. This experiment does not add authentication to the separate upstream ACS Guardian or certify its deployment.

## Selected OWASP Mapping

The project maps these scenarios to two [OWASP Agentic Top 10 categories](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/); OWASP has not reviewed or endorsed this fixture.

| Category | Relevant Cases | Not Established |
|---|---|---|
| ASI03: Identity and Privilege Abuse | Issuer/audience/tenant/scope checks, control-plane separation, scoped idempotency, revocation and bearer reuse | Federated identity, holder-bound tokens, key lifecycle, external mandate or compromise resistance |
| ASI02: Tool Misuse and Exploitation | Bounded repeated tool use, cross-principal budgets and actual committed effects | Planner behavior, prompt-injection resistance, other tools/destinations or production task safety |

Delegation-chain attenuation, real OAuth/OIDC providers, issuer rotation/federation, distributed revocation/caches, clock skew, holder-bound credentials, hostile hosts and independent reproduction remain open. Company-policy and legal-mandate evidence belongs to external governance; it is not something this runtime validates or grants. Existing framework definitions, floors and ratings remain unchanged.

## Verification and Change Control

Local verification on 2026-10-27 passed 44 base tests and 60 integration tests (104 total), including 15 credential regression tests. All 34 credential cases matched their predeclared outcomes, including the three admission-only negative controls. Existing ACS, OPA, Inspect, asynchronous-effect, DSSE and CycloneDX checks passed; four profiles and one component card retained their original ratings and versions. Generated evidence schemas, packet bindings and internal accounting validated. Python compilation, shell syntax and new-relative-link checks passed; five historical changelog links predate this package.

The fixture-only CI allowlist adds exactly three credential files (23 selected files in total), with no JWT, administrative secret or private-key path. Hosted verification is checked after publication and recorded in the annotated release tag. The unrelated DAREB note is neither edited nor staged.
