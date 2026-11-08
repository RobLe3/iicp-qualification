# Seven historical correction-source joins

This supplement adds seven reviewed source-inclusion records to the [prior selected register](../2026-11-07-release-recovery/README.md): **27 selected owner records, 24 correction-source inclusions in the qualified sources and three development-only corrections**. These are not 27 distinct current product defects, 27 whole-issue closures or new qualification results.

The existing 261 closed-body and 15 open-body reviews are reused. A duplicate 104-body pass was rejected as an agent work-selection error and adds zero coverage; its evidence is retained privately. No product or campaign failure is inferred from that error. The qualified candidate, accepted receipts and certificates remain unchanged.

## Exact source findings

| Owner | Qualified source finding | Source / test declaration references |
|---|---|---|
| [RobLe3/iicp-client-rust#146](https://github.com/RobLe3/iicp-client-rust/issues/146) | Canonical IICP_HOME health paths and missing-only legacy fallback survive in the qualified CLI source. | [3 source anchors](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/src/bin/iicp_node.rs#L625); 5 test declarations |
| [RobLe3/iicp-client-rust#148](https://github.com/RobLe3/iicp-client-rust/issues/148) | Linux boot/start-time lock metadata distinguishes reused processes while current/unknown ownership remains protected. | [5 source anchors](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/src/instance_lock.rs#L168); 3 test declarations |
| [RobLe3/iicp-client-rust#44](https://github.com/RobLe3/iicp-client-rust/issues/44) | Shared public model state and successful re-registration updates survive in the helper and production heartbeat paths. | [4 source anchors](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/src/node.rs#L781); 3 test declarations |
| [RobLe3/iicp-directory-php#102](https://github.com/RobLe3/iicp-directory-php/issues/102) | SQL selects the newest timestamp per metric and resolves tied rows by ID before hydration. | [4 source anchors](https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/app/Http/Controllers/StatsController.php#L301); 1 test declarations |
| [RobLe3/iicp-directory-php#95](https://github.com/RobLe3/iicp-directory-php/issues/95) | Node-first and reputation row locks remain inside a bounded-retry transaction, with persisted hourly-window reset. | [5 source anchors](https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/app/Services/ReputationService.php#L64); 3 test declarations |
| [RobLe3/iicp-directory-rust#137](https://github.com/RobLe3/iicp-directory-rust/issues/137) | Digest-pinned Bookworm construction/runtime checks survive; this is not a native x86 execution result. | [5 source anchors](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/ops/pre1-artifact/Dockerfile#L5); 2 test declarations |
| [RobLe3/iicp-directory-rust#76](https://github.com/RobLe3/iicp-directory-rust/issues/76) | Dormancy reactivation and confirmed direct-route transition source survives, with transaction/signing boundaries. | [7 source anchors](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/db.rs#L981); 3 test declarations |

All seven correction commits or merges are ancestors of the exact original qualified component sources. Surviving source properties were inspected as well; ancestry alone would not establish that a change was not reverted. The machine-readable rows contain exact source commits, repository paths, file SHA-256 values, line anchors and test declaration names. Public source URLs link already-public component code, not private execution captures.

Twenty test declarations are listed, including baseline compatibility declarations in the Rust health CLI file. They are **not 20 newly executed or passing tests**. No product code, CLI, database, build, updater, probe or qualification workload was executed for this reconciliation.

## Limits retained per owner

### RobLe3/iicp-client-rust#146

Correction `5f0ee7a1b3fd1cc696b3e9dcf98ca2bac59e9676`; qualified source `0b8b529262977b6482dd7900d473e7d152ba9293`.

- Exact Git ancestry and source assertions only; no current runtime result, packaged-byte claim or new qualification.
- The five test-source declarations are not five newly executed/passing tests.
- The legacy-only-when-missing test sets no canonical snapshot; the preference test uses valid canonical and invalid legacy. This does not supply an executed invalid-canonical/valid-legacy counterpart.
- The no-fallback-on-invalid/read-error property remains a source-control-flow interpretation here, not fresh CLI execution.
- The original accepted candidate and previously reviewed body frontier remain unchanged; this join must receive independent review before adding it to the selected correction register.

### RobLe3/iicp-client-rust#148

Correction `3a13bbcb5c9433c0e5fcf26f8e43223922734130`; qualified source `0b8b529262977b6482dd7900d473e7d152ba9293`.

- Process-instance token is Linux-specific; no new Windows/macOS token capability is inferred. Unknown/current ownership refuses ordinary takeover.
- Retained PR body reports local unit/static and a27-case root Docker gate; these are owner-recorded results, not newly executed or rehydrated runtime proof.
- This does not re-audit every filesystem race or whole instance-lock security contract.

### RobLe3/iicp-client-rust#44

Correction `f428e9da82142c2d7ee8aaee70756f89134d52cf`; qualified source `0b8b529262977b6482dd7900d473e7d152ba9293`.

- Shared health-state reads and successful re-registration updates survive in helper and inlined production paths; source review is not a new HTTP/provider observation.
- Initial configuration seeding and effective-capability variants remain separate context; no claim every startup/registration path is fully covered.
- Old closure comments report rollout/REACH results and route a separate observation window to root469; original logs are not rehydrated here.

### RobLe3/iicp-directory-php#102

Correction `e340e7b83ef8aac5e4b270ceba844d9df6360efc`; qualified source `2dfd228b49c587150a44f448cea1351a9f039d32`.

- Source selects latest timestamp then largest ID among tied candidates per metric, not all historical rows for PHP-side deduplication.
- The source regression uses2000 historical rows and out-of-order backfill; no new load, latency, memory or capacity measurement was made.
- Reported production diagnosis/timing in the old PR is not independently rehydrated here and does not authorize operations or a new observation window.

### RobLe3/iicp-directory-php#95

Correction `f2d9bafe90dc17bd1353d7250b2e52e5f34443db`; qualified source `2dfd228b49c587150a44f448cea1351a9f039d32`.

- Qualified source refactors through upsertLocked/applyLocked and adds metrics-batch idempotency; it is not byte-identical to the original patch.
- Node-first locking scopes serialization to the existing authoritative node row. No arbitrary missing-node or universal DB behavior claim.
- Concurrency test requires mysql and pcntl, forks separate processes/connections and otherwise skips; source presence is not evidence those preconditions or executions passed here.
- PR source reports SQLite expected skips and a separate local MariaDB result; neither becomes qualification credit or an independent external result.

### RobLe3/iicp-directory-rust#137

Correction `ce77bfb7c601cca98b71234cc886c833b33978f2`; qualified source `b95a362ad8f974334994ca73cd20210388a2362f`.

- Build/runtime image manifests are digest-pinned; source enforces target platform, isolated non-root binary version execution and declared runtime glibc before admitting the fragment.
- Observed test-source bodies mock Docker commands/outputs; they are not native executable portability results.
- PR138 records an ARM result and explicitly leaves the x86 oldest-runtime replacement gate pending. No x86 closure is inferred from that source/PR or later accepted counts alone.
- D12 unresolved current x86 binary/release-manifest locators remain availability gaps, not proof of global loss or invalidation of original accepted receipts.

### RobLe3/iicp-directory-rust#76

Correction `955f3fb932597186a8d98044d9eac2f0a0769988`; qualified source `b95a362ad8f974334994ca73cd20210388a2362f`.

- The probe wrapper confirms a first failure with one additional probe. Direct transition storage is transaction/signing gated; heartbeat clears dormancy in its transaction.
- REACTIVATE append in the observed heartbeat path is conditional on configured signing material. No unconditional signed-event guarantee is inferred.
- Owner comments explicitly transferred independently authenticated valid-relay eligibility to Protocol59/root524 because relay_capable alone is insufficient. The original whole acceptance contract is not newly proved.
- Old local277-test/MySQL results are owner-recorded assertions; no native DB/probe/route execution or external interoperability occurred here.

## Original PHP concurrency CI provenance

For PHP #95, GitHub still supplies five completed-success check records at original PR head `1888fe5c3f4a1a97beeb9c4792a8e80a0cd4c706`, including `event-log-concurrency`. The [exact original workflow](https://github.com/RobLe3/iicp-directory-php/blob/1888fe5c3f4a1a97beeb9c4792a8e80a0cd4c706/.github/workflows/control-plane-parity.yml) configures MariaDB 11.4, `DB_CONNECTION=mysql` and PHP 8.3 with `pcntl`/`pdo_mysql`, then selects the reputation concurrency test alongside the event and credit classes.

This is primary historical check metadata and workflow construction, not only a PR-author claim. However, the single bounded detailed-log read returned HTTP 410. No assertion or skip transcript was acquired. The check success must not be expanded into an independently rehydrated four-worker assertion result, nor into a new execution of later qualified source with metrics-idempotency changes. No CI was restarted.

## Review and engineering validation

The controlled source cohort passed independent non-authoring review. Forty current private metadata controls passed. The first staged control run had eight fixture-target errors because the separately typed Rust #146 record sorted first; the corrected tests select the intended inline-source variant explicitly. The verifier and source requirements were not weakened, and original failure evidence remains retained. Staged test totals are not summed.

A public integrity PASS checks this fixed derivative, source-reference formatting, row partitions, generated text and manifest. It does not re-fetch or execute source, reconstruct private context, validate original runtime assertions, prove packaging or confer qualification authority. Opaque controlled source-row digests require authorized retained inputs.

Run `python3.13 -B scripts/correction_source_joins.py` from the reviewed reporting checkout. Use the [reference crosswalk and artifact availability supplement](../2026-11-08-reference-reproducibility/README.md) for its separate 15/17 current-byte result; source inclusion here does not fill those locator gaps.

Existing owners [reference #1678](https://github.com/RobLe3/iicp.network/issues/1678) and [history #1676](https://github.com/RobLe3/iicp.network/issues/1676) retain their acceptance contracts. Whole supported-scope/operational clearance, final successor source selection, required separately authorized qualification, historical completeness and a frozen semantic reference remain unestablished. Held private disclosure gates remain unchanged.

No new qualification credit, cloud authority, historical deletion, package publication, deployment, independent external certification or release is granted. The full post-certification programme remains incomplete.
