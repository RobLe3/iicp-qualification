# Qualification status

Verified snapshot: **2026-10-29T10:47:44Z**.

`[###############-----]` **49/64 accepted shards**

Support cells: **169/218** · Edge executions: **4373/5590**
Sentinels: **4/4** · Project-operated certificates: **0/5**

| Target | Accepted shard indexes | Remaining indexes |
|---|---|---|
| linux-x86_64 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | None |
| linux-aarch64 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | None |
| macos-arm64 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | None |
| windows-x86_64 | 0 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 |

## Latest registered activity

- Recorded outcome: **REFUSED** (blocker, 2026-10-29T10:09:35.350236Z).
- The Windows continuation stopped before tests because the review record used bare digest strings where the caller required a sha256: prefix. The digest values matched. This is a review-to-caller formatting failure, not a new Windows workload result.
- Actual workload launched in this activity: **false**.
- Next gate: Review the pending metadata-only recovery, then use the existing exact validation and CI gates. No workload is authorized by this report.

## Evidence and limits

- Source: private `RobLe3/iicp.network`, commit `a8191a952e9fb44ac143ca87921052d106d9a340`.
- [Receipt derivatives](receipts.json) map each credited assignment to its original receipt digest.
- [Activity history](events.json) is a selected, append-only register, not a complete historical inventory.
- Accepted totals come only from merged canonical ledgers. Passing CI, diagnostics and unpromoted runs add no credit.
- Source validators checked retained receipts and ledger accounting; no workload or live resource inspection was run for this report.
- Original private receipts/captures are not reproduced here. Public consistency checks cannot independently verify their contents or the product behavior.
- Sentinel records are listed separately and grant no extra campaign credit. A receipt counts toward a campaign only when explicitly admitted in its canonical ledgers.
- Zero certificates means none were found in the inspected canonical tracked evidence. It is not an exhaustive search of private storage.
- This is an as-of report, not a live monitor or execution authorization. Unknown/unregistered activity and retention completeness remain unresolved.
- Qualification within a finite scope is not independent interoperability, external certification, deployment or release readiness.
