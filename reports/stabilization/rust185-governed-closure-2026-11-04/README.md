# Rust registration diagnostic correction: governed merge and qualification boundary

On 4 November 2026, [Rust PR #186](https://github.com/RobLe3/iicp-client-rust/pull/186) merged the narrow correction for [issue #185](https://github.com/RobLe3/iicp-client-rust/issues/185). When a successful registration response lacks a token, the error no longer renders arbitrary response fields. Rejection, token aliases, alias precedence and existing empty-token behavior are preserved. Synthetic markers demonstrated the original disclosure; no production exposure or real-secret incident is claimed.

The reviewed head `077c1cb9b05a8b5406dcd689ba578fd1a38b9366` merged as `6bf7e0102560b9ab6217049374d3ee79629fd9ed`. Its tree `b6dca547fb2dd9ffea3866782f418ba233fd41a5` exactly matches the reviewed tree. Only `src/node.rs` changed relative to base `4020dadd150d7975be468f04a588dfa5346899a5`. [The merge receipt](product-merge.json) binds the local validation, independent review and single required CI run.

## Validation and preserved failure

The first local validation stopped because a child process resolved Python 3.9 without `tomllib`. That failed receipt and output remain retained. The reviewed recovery changed only process-local PATH, repeated the failed group once and completed the previously unrun targets. It did not rerun passing groups or change source.

[Combined local validation](local-validation.json) records 658 passing Rust tests and eight existing ignored tests. Those are development-suite exclusions, not qualification skips or waivers. Required CI [41826531854](https://github.com/RobLe3/iicp-client-rust/actions/runs/41826531854) passed, including Linux container and systemd checks, in one attempt. The earlier bounded affected-case replay remains separate evidence; no new diagnostic replay for the formatted committed head is claimed. [Independent exact-head review](product-independent-review.json) passed before merge.

## Issue acceptance disposition

| Issue #185 requirement | Evidence | Disposition |
|---|---|---|
| Narrow correction and synthetic failing/passing distinction | Original bounded diagnostic, affected replay and exact-head review | Satisfied within the documented fixture scope |
| Preserve aliases, rejection and safety checks | Two new unit assertions, local validation and required CI | Satisfied for this correction |
| Focused and governed gates; independent review before merge | Local validation, exact-head review and PR #186 CI/merge receipt | Satisfied |
| Determine candidate/evidence impact before successor claims | [Reviewed impact](candidate-impact.json), [review](candidate-impact-review.json), preserved proposal | Satisfied as an impact determination, not successor qualification |
| Preserve original failure and private captures | Retained source digests in linked records; minimized public derivatives only | Satisfied as reviewed retention, not public reproduction of private captures |

This supports closure of the narrow code-defect issue. It does not close Rust #183 or #175, the ten broader owner questions, or the 21 unverified assurance clauses. It does not establish the cause of the original provider-recovery incident.

## Corrected development main is not the qualified candidate

The [premerge successor proposal](PREMERGE_SUCCESSOR_PROPOSAL.md) and its review are preserved unchanged, including their historical stopped-state wording. This dated supplement records the later successful recovery and merge; it does not rewrite that earlier evidence.

The four intervening frozen-to-base files were already admitted harness changes. The new registration correction is a product-source change. The existing direct Rust scope contains 48 support cells and 1,296 edge executions; this is an impact denominator, not proof that every assertion exercised the changed path or permission to carry forward other credit.

Existing receipt rules bind the whole candidate and global executor registry. Root #1588 remains research, not a compatibility exception. The original 64-shard qualification and five project-operated certificates remain evidence for the original frozen candidate. They do not certify corrected development main. No successor artifacts, candidate, ledger, registry, shard plan or certificate were written by this work; no qualification execution occurred.

The next step is an explicitly reviewed, non-executing successor design under the existing qualification owners: map the new regressions, determine any catalog changes, pin sources and package/toolchain consequences, and recompute required scope. Artifact construction, identity changes and execution require their own existing approval gates. No registry release, version tag, deployment, AWS action or adoption change occurred.

The completed bounded postprocessing programme remains 8/8. That delivery status is not a claim that stabilization, historical completeness, external certification or stable release readiness is complete.
