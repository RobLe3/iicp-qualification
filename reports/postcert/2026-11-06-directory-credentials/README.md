# Directory credential assertions: what the selected cases cover

**6 November 2026.** This source review adds ten PHP/Rust Directory case links to the post-certification evidence foundation. It records selected assertions and their limits, not new qualification results or a product-defect verdict.

Read the [source map](source-map.json), [SDK credential review](../2026-11-06-credential-boundaries/README.md), [documentation-agent entry point](../../qualification-heritage/START_HERE.md) and [accepted qualification report](../../STATUS.md). Historical evidence remains under root [#1676](https://github.com/RobLe3/iicp.network/issues/1676); stabilization remains under [#1678](https://github.com/RobLe3/iicp.network/issues/1678).

## Different assertions behind common scenario names

| Scenario | PHP Directory selected body | Rust Directory selected body |
|---|---|---|
| Expired credential | Snapshot request returns 401 and `token_expired` for an expired replica JWT | Direct production verifier returns the distinct `Expired` enum |
| Missing credential | Consumer-token issuance without Authorization returns 401 | Peer exchange without Authorization returns 401 |
| Replayed credential | Signed gossip vectors compare replay IDs with a supplied seen-ID list | In-memory heartbeat challenge sequence accepts a first HMAC answer and refuses reuse after rotation |
| Rotated credential | Registration, first-token acceptance, re-registration, old-token refusal and replacement acceptance | Two issued JWTs differ; the first verifies with expected claims |
| Signature mismatch | Production event applier rejects a changed signature and reports verification failure | Production event verifier rejects, preserves high-water 0 and leaves discovery empty |

These rows concern different credentials, endpoints and state stores. They must not be pooled as identical cross-component security experiments.

### Rotation: source coverage is not missing implementation

The [PHP round-trip test](https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/tests/Feature/ReplicaTokenRoundTripTest.php#L85-L118) includes both positive acceptance and refusal of the superseded token. It uses a loopback DID/health fixture, local application mode and an explicit development HTTP allowance; it is not arbitrary production-deployment evidence.

The [Rust issuance test](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/auth.rs#L259-L267) does not call the registration/snapshot endpoints. Separate [production handlers](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/federation_handlers.rs) store the latest token hash and compare it during snapshot authentication. The selected test's narrower assertion does not show that production rotation enforcement is absent.

### Replay and missing-token limits

PHP's gossip test uses real Ed25519 verification and production canonicalization, but its replay decision is a test-local lookup in fixture-supplied data. The shared membership fixture is `0.1.0-draft`, pre-normative. No live replay store or first-use/second-use transaction is exercised by that body.

Rust's [heartbeat challenge test](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/main_tests.rs#L3030-L3060) invokes the stateful in-memory repository with real HMAC calculations. Its implementation installs the next challenge on every call, including refusal. This is not a persistent replay store, generic nonce table or assertion that all repository state remains unchanged after refusal.

The missing-token tests are status-only denials at different endpoints. PHP's neighboring positive consumer-token test requires a configured Genesis key and can skip when that prerequisite is absent. Rust's neighboring positive peer tests use a fixture bearer with permissive in-memory token verification. Those source controls do not establish that the corresponding production credential-validation mechanisms were exercised here. No historical skip or qualification failure is inferred from an unselected test's conditional code.

### Signature and expiry limits

PHP explicitly supplies a verification key; its development unsigned-event allowance does not bypass checking a present invalid signature. The selected body does not assert a database snapshot or high-water value. Rust's selected body additionally asserts unchanged high-water and empty in-memory discovery. Neither supplies an expected predecessor hash, so complete chain continuity is not established by these cases.

PHP checks the expiry error code at an endpoint; Rust checks an enum from the verifier. Supporting handlers contain recovery guidance, but the selected cases do not execute re-registration or every temporal boundary.

## Applicability and provenance

The ten links reference **90 existing accepted coordinates**, not new executions:

- PHP: five cases × two Linux targets × three recorded modes × PHP 8.3 = 30.
- Rust: five cases × two Linux targets × three recorded modes × two runtimes (`msrv-1.88`, `rust-1.98.0`) = 60.

The targets are Linux ARM64 and Linux x86-64. These selected Directory assignments do not add native macOS or Windows Directory execution evidence. Recorded mode labels are accepted-index applicability metadata, not proof that each selected body configures every advertised deployment mode. In particular, fixture-local configuration must remain distinct from a production-mode claim.

Twenty-six retained source files matched their qualified and accepted-harness Git versions. The map pins those files, the catalog and the canonical Protocol fixture. Source equality does not prove installed-package equivalence, current deployment or a new runtime reproduction. Recorded command templates are not standalone reproduction instructions.

The bounded frontier now contains **54 partial reviewed case links out of 147**, with 93 outside it and 2,466 existing accepted coordinate references. Prior 44 rows are preserved. These counts are not 54 complete normative contracts. Private index/review hashes identify retained evidence but do not make it publicly retrievable.

## Validation and remaining work

Run the repository's Python 3.13 consistency check and unit tests. Supplement controls protect the exact projection's identities, accounting and claim boundaries; they are not Directory runtime or universal security tests. The three report files reproduce from retained source-review inputs. Do not hand-edit generated output to change a finding.

Continue the remaining supported-scope defect dispositions, 93 source definitions outside this bounded frontier and successor artifact/environment/harness closure. Historical preservation remains incomplete. Original qualification, certificates and acceptance authority are unchanged. No cloud operation, qualification workload, external interoperability, verified successor freeze, deployment or release follows from this source supplement.
