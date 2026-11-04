# Bounded stabilization findings — 4 November 2026

The completed post-processing delivery remains **8/8**. This separate stabilization batch adds zero-credit observations and one narrowly demonstrated diagnostic-disclosure defect; it does not establish a zero-known-defect baseline or change the accepted qualification candidate.

## Actual observations

The original sequence passed nine cases and stopped on its tenth: an HTTP200 registration response without a token caused the error diagnostic to include the synthetic response body. Only synthetic markers were used; no real secret disclosure was observed. The failure is preserved, not converted into a pass by the later correction.

Before that failure, actual frozen Node execution observed default recovery checks after heartbeats 2, 4 and 6, then exit76 under persistent synthetic route loss. A separate strict-secured mock Directory scenario issued a new token after ownership proof, and three subsequent heartbeats used it. Refused renewal and the separately completed unused invalid-ownership case did not issue a new credential. This is a selected frozen PHP policy model, not execution against a PHP server, the default policy or deployed behavior.

The bounded diagnostic cases rejected recognized, unknown, malformed and oversized HTTP403 response bodies without exposing their synthetic markers. These cases do not prove universal response-parser safety. Directory-code visibility was recorded as an observation, not invented as a normative requirement.

The unused invalid-proof proposal was first refused before execution: its case-name guard always denied renewal, so the result would not have distinguished valid from revoked proof. The [retained pre-execution finding](invalid-proof-preexecution-refusal.json) records the correction to a shared ownership predicate and positive/negative checks before its single reviewed execution.

## Local correction, not an admitted successor

Owner: [Rust SDK #185](https://github.com/RobLe3/iicp-client-rust/issues/185), linked to #175 and #183 without closing either.

A one-file `src/node.rs` correction removes arbitrary response content from the missing-token error, preserves rejection, token-alias precedence and existing empty-token behavior, and adds two focused regression tests. Both tests and an offline locked build passed. One affected-case replay passed, with the same rejection outcome and synthetic marker absent. Passing earlier cases were not repeated.

The correction is **uncommitted, unpublished and unmerged**, on local base `4020dadd150d7975be468f04a588dfa5346899a5`. Exact proposed source SHA-256: `24f4b087990f3cdbd15e4b8b3cb8bf2a17d393effaef776206931703d2a54ce4`; diff SHA-256: `e432f0a3ad2742bb7a80a3835b86c7d1bbb3b25c786e7ed5bf2a1e1449a27eed`. No committed successor tree is claimed. [The runtime summary](runtime-summary.json) binds the source manifest, original failure and independent reviews.

Any product publication, full governed CI, merge or candidate update must follow its own approved exact-source workflow. Product identity changes cannot inherit qualification credit automatically; existing impact and qualification policy must determine the required successor verification. The current 64-shard evidence and five project-operated certificates remain unchanged.

## Assurance and remaining decisions

The [pre-runtime assurance refresh](pre-runtime-assurance.json) verified six unchanged component main references, 15 open issue identities, six matching frozen/current Rust source blobs, seven Windows guest bindings and 20 targeted retained-file hashes. Generated launchd settings are not original installed-settings evidence. No installed plist, service, AWS resource or production endpoint was accessed.

[The additive owner delta](owner-delta.json) leaves all ten owner questions open. The 21 formal clauses remain unverified. Actual route/tunnel recovery, original Rust#183 cause, real supervisor restart/cooldown, relay#175 and native Windows lifetime isolation remain outside these observations. Local macOS controls are not Windows enforcement evidence. Missing enforcement assurance is not proof of prohibited contact.

All executed cases recorded owned-child reap and exact listener absence; this is not an independent whole-host census. Historical completeness remains false. No workload or additional repair is authorized by this report.
