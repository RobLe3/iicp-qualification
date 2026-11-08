# Directory contracts: interpret the executed adapter, not the scenario name

This source-bound supplement reconciles six unchanged Directory owner conjunctions. It adds no workload, product repair, owner checkbox completion or qualification credit.

## Existing reference coverage

| Component | Existing support references | Existing edge references |
|---|---:|---:|
| PHP Directory | 6 | 126 |
| Rust Directory | 12 | 288 |

The 432 references cover 47 existing definitions and 32 original receipt references in the two declared Linux lanes. They are not new tests. Rust’s twelve cells combine two toolchains, two architectures and three modes—not a second Directory flavor or an invented database axis. Original receipt/proof envelopes were not reopened for this analysis.

## Shared definitions and output guards

Three exact fixture pairs match across the accepted PHP/Rust harness sources. The historical contract revision is **v1.10.80**, distinct from current component versions.

- **17 behavior-vector definitions** cover selected registration, eligibility, ranking, pricing and endpoint-refusal checks.
- **43 HTTP metadata records** describe method/path/auth/status scope. They are not 43 newly executed endpoint tests.
- **Seven byte-identical output-validation functions** guard the selected cross-flavor case. The exact driver revalidates the binding and validates owned output before writing its proof.

Existing acceptance plus exact bound driver/adapter output guards, not fresh raw-output inspection or an independent runtime reproduction. Eighteen existing cross-flavor coordinates use the bound case; do not relabel them as new vector executions or whole operational parity.

## Six effective Rust adapter contexts

| Case | Accepted adapter source predicate | Limitation |
|---|---|---|
| directory-rust::credential-missing | Installed HTTP POST /v1/peers without a bearer credential must return401. | Does not establish every protected route or authority role. |
| directory-rust::credential-expired | Installed snapshot HTTP checks a signed non-expired unregistered control (401 with specific registration cause), then an expired token (401/token_expired). | The non-expired unregistered control is not authorized snapshot access; registered authorized access is checked separately by rotation. |
| directory-rust::credential-rotated | Installed replica registration and snapshot access succeed; re-registration retains replica ID and changes token; old token fails401/rotated while replacement succeeds200. | Specific replica/snapshot role, not universal bearer revocation or all credential classes. |
| directory-rust::credential-replayed | Installed registration/heartbeat plus SQL observes first accepted HMAC verification, refuses replay from advancing verified_at, rotates challenges and accepts a fresh response afterward. | Heartbeat may still return200 while cryptographic liveness is refused; not raw fixture-set membership or all replay protocols. |
| directory-rust::signature-mismatch | Installed HTTP/SQL checks initial and valid heartbeat verification; one HMAC nibble is tampered, verified_at must not advance, challenge rotates, and subsequent valid response recovers. | Not the raw replica-event Ed25519 unit predicate; no claim about all signed event paths. |
| directory-rust::rate-limit | Installed registration accepts60 expected422 validation controls, refuses two admissions429/IICP-E034/retry_after60 within the bounded window, then validation recovers after the window. | Not a general throughput benchmark, universal rate policy or every rate-limited endpoint. |

Raw unit predicates remain preserved. For example, a token-issuance helper test is not the complete installed HTTP rotation case. The latter checks authorized access, old-token refusal and replacement success. The installed signature case checks heartbeat HMAC state, not the raw replica-event Ed25519 predicate.

## Owner contracts and release boundaries

Six whole clauses remain unverified. Their twenty-one proposed analytical atoms are source/evidence dispositions, not twenty-one completed requirements.

- Persistent production-equivalent REACH and production rollback remain separate preview-promotion/cutover gates. This analysis maps their ownership; it neither executes nor waives them.
- A frozen versioned reference is not a permanent future Rust operator-ABI promise. Documented HTTP/integrity changes remain subject to shared-contract review.
- PHP expand-first schema changes may remain after application rollback. Do not infer universal destructive migration reversal.
- The PHP-authority statement is a qualified-source policy boundary, not a fresh live-production observation.
- PHP node-health recovery, released-artifact operator recovery and production service recovery are distinct evidence scopes.
- Rust migration evidence follows documented empty-database bootstrap and incompatible-existing-schema refusal; it does not establish automatic incremental migrations.

## Validation and limitations

Private focused controls:31 overlay and16 owner-atom controls passed. These validate metadata/source relationships; they are not qualification tests or an independent implementation experiment. Required publication review and exact-head CI are separate gates.

- Counts are existing reference joins, not new executed tests. Root ledgers, accepted receipts and certificate validators remain qualification authority.
- Seventeen behavior-vector definitions and forty-three HTTP metadata records are different units; neither equals complete protocol conformance.
- Raw unit-test bodies can differ from the exact installed adapter dispatch. Preserve both source layers and their limits.
- A lookup for PHP PARITY.md was an invalid filename assumption at the pinned commit, not a product defect. Five actual release/operations/parity policies and two qualified READMEs were used.
- The initial analytical preparation refused an incorrect one-toolchain assumption. Corrected Rust coverage uses MSRV1.88 and Rust1.98.0, two Linux architectures and three modes, with one rust flavor.
- The six whole owner conjunctions remain unverified and unchanged. Twenty-one analytical atoms are not twenty-one completed owner requirements.
- Private source captures, original outputs, credentials and operational locators are not distributed here. The full post-certification programme remains incomplete.

See [pinned source references](SOURCES.md), [the preceding owner-contract audit](../2026-11-08-owner-contract-evidence/README.md) and [canonical qualification reporting](../../STATUS.md). Public checks validate this fixed derivative, schema, narrative and manifest; they do not reconstruct private original executions.
