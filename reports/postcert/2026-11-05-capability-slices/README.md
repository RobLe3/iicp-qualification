# What selected confidentiality and identity tests establish

**5 November 2026.** This supplement maps selected test assertions to existing accepted records for the original PRE-1 candidate. It helps a documentation agent describe demonstrated scope without treating test names, fixture rows or successful accounting as complete behavioral evidence.

Read [the minimized source analysis](source-analysis.json). It pins exact source files, line ranges, fixture and contract revisions, selected-coordinate counts and retained review identities. The earlier [source-semantic checkpoint](../2026-11-05-source-semantics/README.md) covers eligibility and effective-capability assertions. Neither supplement is qualification authority or a frozen executable functional reference.

## Scope at a glance

| Partial slice | Selected SDK cases | Existing accepted coordinates | Per qualified target |
|---|---:|---:|---:|
| Confidentiality | 9 | 576 | 144 |
| Identity lifecycle | 3 | 192 | 48 |
| Distinct combined scope | 12 | 768 | 192 |

These are references within the existing accepted campaign, not additional tests or new credit. Python has more runtime combinations than TypeScript or Rust; do not interpret its larger coordinate count as stronger behavioral assurance. No SDK or qualification tests were executed to prepare these analyses.

The underlying test files were compared byte-for-byte at their exact qualified-product and accepted-harness source revisions. That establishes source identity, not independent reproduction of the original installed-artifact execution. The five shared identity-fixture rows are source inputs, not five native executions per SDK.

## Confidentiality: three bounded predicates

The nine selected cases cover three predicates across the three SDKs:

1. A request envelope whose ciphertext has been modified is rejected by the local decrypt helper.
2. Default all-keyless discovery is refused before provider task dispatch, subject to the plaintext-debug override configuration.
3. A keyless higher-score candidate is skipped while a keyed candidate receives a confidentiality envelope naming its key.

The keyed-route assertions differ. Python and TypeScript explicitly assert that the request contains no plaintext `payload` field. Rust uses a partial JSON body match for the selected recipient key; that selected test does **not** independently assert plaintext-payload absence. This is an assertion-coverage difference, not evidence that Rust transmits plaintext.

The tamper cases also differ: Python flips different bits from TypeScript and Rust and accepts different error forms. All three exercise local cryptographic helpers. They do not establish provider HTTP error codes, a common wire experiment, replay protection or independent cross-implementation interoperability.

Three additional source-only bodies assert successful encryption/decryption roundtrips. They provide a positive counterpart to the negative source assertions, but this supplement does not infer additional accepted joins or execution results for them.

### Keep the shipped confidentiality boundary explicit

The pinned [S.16 confidentiality document](https://github.com/RobLe3/IICP/blob/2d240649cf8d11a235132658a599e22ebcba6620/spec/v1.9/iicp-confidentiality.md#L289-L307) distinguishes shipped Tier-1 conformance from the Tier-2 target. Its section 6 explicitly permits a transitional plaintext debugging escape hatch through an explicit opt-in override. Broad purpose-level “no opt-out” wording must not erase that stated exception.

Rust clears the plaintext-debug override in the selected refusal test. The selected Python and TypeScript bodies do not independently clear that ambient variable. Their assertion meaning is therefore configuration-sensitive; this analysis does not reconstruct every private process environment.

**Tier 1 provides no forward secrecy against node-key compromise.** The executing node can read work it executes. Request encryption does not establish response encryption, metadata confidentiality, key-rotation compliance, executor blindness or complete Tier-2 conformance. Selected helper tests must not be used to claim otherwise.

## Identity lifecycle: one fixture, different assertion depth

All three selected SDK tests use the same [five-row E050 lifecycle fixture](https://github.com/RobLe3/IICP/blob/2d240649cf8d11a235132658a599e22ebcba6620/research/pre-normative-profiles/fixtures/e050-client-credential-lifecycle-v1.json). It identifies itself as **implementation-evidence-only** and grants no production activation. It contains three successful acknowledgment scenarios and two refusal scenarios.

| Selected assertion | Python | TypeScript | Rust |
|---|---|---|---|
| Outgoing current-token projection | Asserted | Asserted | Asserted |
| Mocked acknowledgment and in-memory successor-token continuity | Asserted | Asserted | Not exercised by selected body |
| Requested-endpoint projection | Not asserted by selected body | Not asserted by selected body | Asserted |
| Endpoint commitment or rollback | Not asserted | Not asserted | Not asserted |
| Durable credential storage | Not asserted | Not asserted | Not asserted |
| Actual supervised process restart | Not exercised | Not exercised | Not exercised |
| External Directory-loss liveness | Not asserted | Not asserted | Not asserted |

Rust's selected body seeds a token, changes an endpoint and calls a helper that returns the registration payload. It does not invoke HTTP registration or consume acknowledgment status and token values. Python and TypeScript mock registration acknowledgments and assert outgoing/current token behavior. Their refusal checks do not establish exact E050 error-code semantics: Python expects an HTTP status exception; TypeScript accepts rejection generally.

A fixture row named `supervised-restart` does not establish that a supervised process restarted. A declared invariant about Directory-loss liveness is not evidence that the selected test asserted it. These source bodies cannot close historical provider-recovery questions such as Rust issue #183. Other retained evidence must be examined separately before deciding whether a behavior is established, defective or unresolved.

## What can be checked publicly

The source analysis provides immutable repository/commit/path links and complete-file digests. Readers can inspect each assertion at its pinned source range and verify the source bytes with Git. Public receipt derivatives support the selected coordinate counts; they do not expose private raw output or replace original receipt verification.

Run this **read-only accounting comparison** from the repository root at the reviewed supplement revision:

```python
import collections
import hashlib
import json
from pathlib import Path

root = Path('.')
analysis = json.loads((root / 'reports/postcert/2026-11-05-capability-slices/source-analysis.json').read_text())
raw = (root / 'reports/receipts.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == analysis['public_receipt_derivative']['sha256']
selected = {row['case_id']: row['existing_accepted_coordinate_count'] for row in analysis['case_mappings']}
counts = collections.Counter()
seen = set()
for receipt in json.loads(raw)['receipts']:
    assert receipt['admission_status'] == 'accepted-in-merged-ledgers'
    assert receipt['candidate_manifest_sha256'] == analysis['candidate_manifest_sha256']
    for assignment in receipt['edge_executions']:
        assert assignment not in seen
        seen.add(assignment)
        scenario, cell = assignment.split('::')
        case_id = cell.split('|')[0] + '::' + scenario
        if case_id in selected:
            counts[case_id] += 1
assert dict(counts) == selected
assert sum(counts.values()) == 768
print('PASS: 12 selected case mappings, 768 existing coordinate references; no new credit')
```

This comparison checks published accounting references only. Reproducing controlled source-map generation, original receipt validation or private review findings requires authorized access to the retained archive. A review digest identifies a record; it does not make that record publicly preserved or independently inspectable.

## Validation and remaining work

The controlled confidentiality derivative passed 27 offline integrity controls and byte-identical regeneration. Initial review found a Python boolean/numeric-equality weakness in its verifier and an incomplete contract excerpt; both were corrected, with original findings retained. The identity slice passed 12 offline structural checks and deterministic regeneration. These checks assess derived analysis, not SDK conformance or native qualification.

The complete post-certification programme remains open under [root issue #1676](https://github.com/RobLe3/iicp.network/issues/1676). Both capability families remain partial; historical inventory completeness is false. This supplement does not resolve the remaining 21 unverified formal criterion clauses, establish zero known supported-scope defects or freeze a successor baseline.

The original candidate, 64 accepted shards and five project-operated certificates remain unchanged. Later development fixes—including [Python PR #146](https://github.com/RobLe3/iicp-client-python/pull/146) and [TypeScript PR #125](https://github.com/RobLe3/iicp-client-typescript/pull/125)—are separate source revisions, not newly qualified artifacts. No credit is transferred to corrected code here.

No independent external certification, DMSC interoperability, performance qualification, release readiness or deployment authority follows from this work. Next steps are the remaining source-semantic mappings and supported-defect dispositions, followed by the separately governed successor-qualification decision where required.
