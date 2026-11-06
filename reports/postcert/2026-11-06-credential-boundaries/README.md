# Credential-boundary source review

**6 November 2026.** This additive handoff examines 18 selected case definitions across the Python, TypeScript and Rust SDKs. It separates assertions in test source from wider security obligations. It does not change qualification acceptance or establish a verified successor baseline.

Read the [machine-readable source map](source-map.json), [earlier timeout checkpoint](../2026-11-06-timeout-and-source-checkpoint/README.md), [documentation-agent entry point](../../qualification-heritage/START_HERE.md) and [qualification report](../../STATUS.md). Historical evidence remains owned by root [#1676](https://github.com/RobLe3/iicp.network/issues/1676); stabilization remains under [#1678](https://github.com/RobLe3/iicp.network/issues/1678).

## What the selected crypto tests establish

Twelve cases, four per SDK, use real Ed25519 libraries with the same pinned pre-normative fixture. Their policy decisions are implemented inside the test files; they do not invoke an SDK production ticket validator.

| Case family | Selected assertion | Important limit |
|---|---|---|
| Expired credential | Reject a signing key outside its fixture validity window | Not all ticket-claim or membership-expiry behavior; the key-time branch precedes the signature-validity branch |
| Replayed credential | Reject a fixture whose supplied `jti_seen` value is true, after earlier gates | No live replay store, first-use/second-use sequence or production accepted-state snapshot |
| Rotated credential | Reject a key already marked revoked | No rotation operation or acceptance of a newly installed credential in the selected body |
| Signature mismatch | Reject a tampered claim using the real signature-verification result | Not every identity/domain mismatch or a production trust-bundle admission path |

Separate portable-vector methods in the same files check active and retiring-key acceptance as well as rejection vectors. These are useful positive source controls, not extra executions credited by this review. Fixture-specific sorted JSON serialization must not be represented as demonstrated universal canonicalization conformance.

The shared fixture is version `0.2.0-draft`, with status `pre-normative`. Its existence and test use do not make all of its behavior a universal base-protocol production requirement.

## Missing credentials and Directory failures

The six remaining cases invoke production SDK boundaries, with different assertion depth:

- **Missing credential:** Python and TypeScript directly call their secret resolvers and expect an unavailable-credential error. Rust calls client construction with a missing secret-file locator and asserts an error. None of these selected bodies includes a network spy. Supporting constructor source resolves the secret before creating the HTTP client, but that is distinct from an end-to-end anonymous-escalation test.
- **Directory unavailable:** Python injects a connection error and checks one request plus the configured URL prefix. TypeScript injects a connection-like fetch failure and checks one fetch; it does not explicitly assert the URL. Rust uses a local server returning HTTP 200 with compatible negotiation metadata but no required restricted-domain decision, then asserts an error and one server request. Rust therefore tests missing-decision refusal, not transport unavailability.

The retained modules also contain successful authenticated-discovery controls. This review inspected their source; it did not execute them. One-request assertions in these fixtures do not establish universal network isolation, every redirect behavior or all failure classes.

## Provenance and accounting

The source map pins the exact qualified commits, test/production paths, catalog obligations and fixture bytes. Nineteen retained test, production and SDK-fixture files were compared with the corresponding accepted-harness source bytes. Equality is source-file evidence, not installed-package equivalence or a reproduction of the original runtime.

The 18 case links reference **1,152 existing accepted coordinates: 576 Python, 288 TypeScript and 288 Rust**. These counts come from the controlled accepted case index; they are not newly inspected raw outputs, new executions or additional qualification credit. The public map identifies private index and review inputs by digest. Those digests do not make the private originals publicly retrievable.

The catalog obligations are broader than several selected assertions. These are partial source-coverage findings, not automatic evidence that the product is defective or that accepted qualification is invalid. Other cases or sources may support additional obligations; that requires separate tracing rather than an inference from a test name.

## Verification and next action

Run the repository's Python 3.13 public consistency check and unit tests. Supplement controls verify identity, accounting, file integrity and prohibited claim inflation; they do not independently establish SDK correctness or complete normative coverage. The three report files are generated from retained source-review inputs; do not hand-edit them to change a conclusion.

Continue the unresolved contract/assertion mappings and supported-scope defect dispositions before determining the successor candidate and its required formal verification. Historical preservation remains incomplete. No qualification workload, cloud action, certificate change, external interoperability, baseline freeze or release follows from this supplement.
