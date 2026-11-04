# Rust #185: successor verification proposal

## Decision and boundary

The proposed correction changes product source, not only tooling. The four intervening frozen-to-base changes were already admitted harness changes at `4020dadd150d7975be468f04a588dfa5346899a5`. They must remain in the provenance account, but are not four new product fixes. The new `src/node.rs` change cannot be admitted under that tool-only allowance.

The proposed reviewed identity is `077c1cb9b05a8b5406dcd689ba578fd1a38b9366`, tree `b6dca547fb2dd9ffea3866782f418ba233fd41a5`; the publication attempt stopped during local validation before publication, so no merge identity exists for this attempt. The reported environment failure is Python3.9 lacking tomllib; its separately retained terminal record must govern any recovery decision. Its diagnostic behavior preserves rejection and token-alias precedence while removing arbitrary response rendering. The two new regression assertions are not automatically entries in the admitted edge catalog.

The current certificates continue to describe the immutable original six-component candidate, not corrected development main. A successful product CI or merge must not be reported as successor qualification. No original receipt, certificate, manifest or ledger is changed by this analysis.

## Direct impact versus qualification accounting

The existing declared Rust scope contains 48 support cells and 1,296 edge executions across four targets, two runtimes, two Directory flavors and three modes. This is an impact denominator, not permission to carry forward the rest of the candidate's credit or a claim that all 1,296 assertions exercise registration diagnostics. The exact existing scenario/assertion map and artifact digests are retained in `candidate-impact.sanitized.json`.

The Rust crate and vendored offline package, package/build receipts and six-component candidate digest need successor identities if rebuilt with the fix. An unchanged component artifact may be reusable only if the existing composer validates its exact component, source and toolchain bindings. Artifact-fragment reuse is not qualification-receipt reuse.

The receipt validator rejects a different whole-candidate digest or six-component artifact map and checks the global executor-registry digest. Sentinel, shard-plan and certificate bindings must also match. Root #1588 is an open architecture investigation, not a scoped compatibility exception. Under the current policy a successor qualification claim needs a complete successor ledger under its reviewed identity; a Rust-only replay is development evidence, not a complete replacement certificate.

The edge catalog says newly reproduced failures are added before promotion. Root #1106/#1493 must decide the exact new scenario/assertion mapping and recompute required counts and assignments. The old 64/218/5,590 totals must not be copied into a changed successor catalog without re-expansion.

## Ordered gates and owners

1. **Rust #185: exact product correction.** Complete required focused tests, independent exact-head review, governed CI and conditional merge. Record the actual merge identity and source bytes. Closure of the narrow code-defect issue requires its full acceptance contract; this does not close #183/#175 or confer qualification.
2. **Root #1106/#1493: non-executing successor design.** Pin the merged six-component sources, the two new regressions and any catalog addition, package/toolchain closure, changed artifact identities and global registry/plan consequences. Preserve the old candidate and evidence. This stage needs an explicit approved preparation workflow before writing successor manifests or building artifacts.
3. **Root #1117/#1470: execution readiness.** Prepare fresh source-bound four-target sentinel/campaign packets with exact current policies, cleanup, evidence retention, native Windows assurance disposition and funding/authentication prerequisites. Resolve the original 21 unverified clauses through their owners rather than treating this proposal as a waiver.
4. **Separate execution authority.** Only an approved bound campaign may execute. No allocation, AWS login, runtime workload, retry or spending follows from this proposal. Expected scope follows the new plan's own expanded assignments, not guessed old counts.
5. **Root #1493: evidence admission and certificates.** Validate complete successor receipts, independently verified closure and source bindings, then separately review/admit target and ecosystem certificates. Never rewrite old certificates or transfer credit by narrative.

## Command templates after their gates are approved

These are source-inspected entry points, **not executed commands**. All variables must resolve to an independently reviewed compatible layout and exact files. Existing selected-path guards still apply; arbitrary private paths are not assumed accepted. Output paths must be new. No placeholder may point at a canonical accepted artifact for overwrite.

```sh
python3.13 -B scripts/check_pre1_stability_candidate.py --manifest "$SUCCESSOR_CANDIDATE" --strict --json
python3.13 -B scripts/check_pre1_executor_registry.py --registry "$SUCCESSOR_REGISTRY" --candidate "$SUCCESSOR_CANDIDATE" --matrix "$SUCCESSOR_MATRIX" --catalog "$SUCCESSOR_CATALOG" --workspace-root "$PINNED_WORKSPACE" --strict --json
python3.13 -B scripts/plan_pre1_qualification_shards.py --candidate "$SUCCESSOR_CANDIDATE" --registry "$SUCCESSOR_REGISTRY" --matrix "$SUCCESSOR_MATRIX" --catalog "$SUCCESSOR_CATALOG" --runners "$SUCCESSOR_RUNNERS" --shards-per-target 16 --require-ready --output "$NEW_PLAN_OUTPUT"
python3.13 -B scripts/check_pre1_qualification_receipt.py "$NEW_RECEIPT" --candidate "$SUCCESSOR_CANDIDATE" --registry "$SUCCESSOR_REGISTRY" --json
```

Existing `compose_pre1_candidate_artifacts.py` and `freeze_pre1_candidate_artifacts.py` own artifact composition/freeze; `compile_pre1_sentinel_ledger.py`, `compile_pre1_target_certificate.py` and `compile_pre1_ecosystem_certificate.py` own compilation. Their required inputs must come from the approved successor workflow; invoking them now would skip those prerequisites. No new generic controller or alternative qualification authority is proposed.

## Remaining policy/authority blockers

No successor candidate, catalog change, artifact construction, global rebind, campaign execution or certificate admission is currently authorized by this read-only impact work. No scoped credit exception exists. The complete successor scope and native Windows assurance resolution need owner decisions before scheduling qualification. This is a proposal for a coherent next workflow, not a request for repeated approval at every unchanged gate.
