# Timeout semantics and source-correction checkpoint

**6 November 2026.** This additive documentation handoff distinguishes test assertions, accepted execution references and later development corrections. It is not qualification authority or a frozen functional reference.

Read [the source map](source-map.json), [earlier semantic checkpoint](../2026-11-05-source-semantics/README.md), [heritage handoff](../../qualification-heritage/START_HERE.md) and [qualification report](../../STATUS.md). History remains owned by root [#1676](https://github.com/RobLe3/iicp.network/issues/1676); stabilization remains under [#1678](https://github.com/RobLe3/iicp.network/issues/1678).

## What the timeout tests check

Three exact qualified SDK test bodies assert numeric backend `error_code: 408`:

- **Python:** injects `httpx.TimeoutException` through a mock. It checks 408 and a timed-out message; it does not wait for a configured deadline.
- **TypeScript:** a synthetic fetch rejects when the handler abort signal fires. A one-millisecond timer is configured and 408 is asserted.
- **Rust:** a local listener accepts a connection and sleeps while a ten-millisecond request timeout expires. The test asserts 408, not a measured timing bound.

Production paths and shared helpers support this bounded source interpretation. Successful chat and separate connection-refusal/502 tests provide source context, not additional selected-case execution credit.

The three case bindings reference **192 existing accepted coordinates: 96 Python, 48 TypeScript and 48 Rust**. These are references into the retained accepted index, not newly inspected runtime outputs or new executions. Reproducing that private index requires authorized archive access.

The catalog obligation is broader: “Bound the attempt and preserve retry safety.” These three bodies do not assert safe retry, duplicate suppression, acknowledged provider cancellation or provider terminal state. Other assertions may address those requirements; this supplement neither proves complete coverage nor declares a product failure.

The pinned Service Lifecycle Profile is **0.1.2-draft**, proposed and not required for base IICP conformance. Its negotiated provider-attempt semantics are distinct from a local transport timeout. The qualified capability baseline's stated service-lifecycle feature scope does not make these helper tests complete profile conformance.

## Review accounting

The bounded frontier contains **26 reviewed case-source links out of 147 declared definitions**, leaving 121 outside this frontier. Selected cases reference 1,224 existing accepted coordinates. Reviews are partial source/dispatch assessments, not 26 complete normative contracts. This increment adds three reviewed links and 192 references, with zero new executions or qualification credit.

An earlier private checkpoint appended eight Directory reviews but retained an old overlapping remainder. The corrected partition is disjoint; the original checkpoint and accepted results are preserved. This is derived-accounting correction, not rewritten campaign history.

## Later development corrections

Three five-file dependency corrections merged after independent review and required hosted CI:

| Component | PR | Merge commit | Hosted jobs |
|---|---|---|---|
| Rust SDK | [#192](https://github.com/RobLe3/iicp-client-rust/pull/192) | `54e4bdaaee6daadc07d27e1258ed9c27539bd9a0` | 1/1 PASS |
| Rust Directory | [#151](https://github.com/RobLe3/iicp-directory-rust/pull/151) | `407818227036b37eb12e8f37eb4bb9926387255e` | 7/7 PASS |
| Management | [#169](https://github.com/RobLe3/iicp-management/pull/169) | `53f8ad0736c2abec89e0297d244ee5871a82e904` | 2/2 PASS |

These are development-source integrations, not newly qualified artifacts. Dependency versions changed; IICP component versions did not. PR descriptions retain incidental Windows/RNG dependency-edge changes. Directory's inherited RSA package advisory remains a bounded finding, not global security clearance.

Management's first local gate failed because the validation caller selected a temporary path exceeding the native Unix-socket limit. Its unchanged failed test passed under a shorter private temporary path, followed by only the remaining blocked checks: 180 distinct passing Rust tests across retained segments, plus clippy and conformance. This is not an uninterrupted original local gate PASS. Hosted CI subsequently passed both required jobs.

[Reporting PR #99](https://github.com/RobLe3/iicp-qualification/pull/99) records terminal observations: events advanced 150→160 with prior prefix and accepted receipt bytes preserved. It is an as-of snapshot, not a live monitor or complete historical inventory.

## Verification and next work

The map pins source files, exact commits and content digests, including the catalog obligation and qualified feature baseline. Public SDK/Protocol sources can be inspected directly; access to a private coordination-repository source still requires the appropriate repository permission. Controlled review/index digests identify retained records; they do not make those private records publicly retrievable. Run this repository's Python 3.13 checks and unit tests. Supplement controls check integrity, accounting and claim boundaries, not runtime correctness or complete source semantics.

Next: reconcile remaining case/contract relationships and supported-scope findings, determine final successor artifact/environment/harness bindings, and obtain separately required verification authority. Historical completeness remains false. No workload, cloud operation, accepted credit, certificate, external interoperability, reference freeze or release is authorized by this supplement.
