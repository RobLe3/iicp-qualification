# SDK release and recovery assertion depth

This reviewed source analysis covers **19 case definitions** and **1,200 existing accepted coordinate references** across the three SDKs. It does not execute those cases, add qualification credit or establish complete semantic contracts.

## What the selected tests actually assert

| Case | Selected assertion depth | Predicate | Explicit limit |
|---|---|---|---|
| [client-python::minimum-version](https://github.com/RobLe3/iicp-client-python/blob/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183/tests/test_pre1_release_boundaries.py) | DECLARED_METADATA_AND_RUNNING_INTERPRETER | Metadata requires Python>=3.11,<3.15; test checks that declaration, current interpreter>=3.11 and pre-1 package major. | No separate upper-bound execution assertion or fresh minimum-runtime build/install follows. |
| [client-python::offline-locked-install](https://github.com/RobLe3/iicp-client-python/blob/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183/tests/test_pre1_release_boundaries.py) | STATIC_SOURCE_TEXT_AND_LOCK_METADATA | Checks own package/version occur in uv.lock; quality source includes uv isolated locked run; release workflow contains build/venv/wheel-install strings. | No network-disabled installation, complete dependency closure retrieval or artifact reproduction is executed by this selected body. |
| [client-python::package-version-self-report](https://github.com/RobLe3/iicp-client-python/blob/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183/tests/test_pre1_release_boundaries.py) | PACKAGE_IMPORT_METADATA | Imports iicp_client; compares __version__ with pyproject version and package name. | Not a clean wheel install or subprocess CLI self-report. |
| [client-python::process-crash-restart](https://github.com/RobLe3/iicp-client-python/blob/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183/tests/test_service_lifecycle.py) | SQLITE_CRASH_AND_TWO_PROCESS_TERMINAL_RACE | Helper exits77 inside uncommitted BEGIN IMMEDIATE transition; reopened DB remains running/sequence1. Complete/fail children must return0/2; final state terminal/sequence2/events0,1,2. | SQLite persistence fixture, not real provider/service restart or durable historical Directory recovery; waits in body have no explicit timeout. |
| [client-python::rollback-last-supported](https://github.com/RobLe3/iicp-client-python/blob/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183/tests/test_updater.py) | INJECTED_INSTALL_FAILURE | auto_update_tick uses fake installerFalse; expects upgrade-failed and no fake reexec calls. Neighboring success control exists outside selected body. | No package manager is run, partial installation reversed, previous artifact restored or old runtime health verified. |
| [client-python::unsupported-version](https://github.com/RobLe3/iicp-client-python/blob/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183/tests/test_updater.py) | VERSION_CLASSIFIER_POSITIVE_AND_NEGATIVE | parse_version rejects rc spellings/v-prefix and accepts0.7.57 as(0,7,57). | This is updater candidate syntax, not runtime support negotiation or all unsupported protocol versions. |
| [client-rust::minimum-version](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/tests/pre1_release_boundaries.rs) | DECLARED_BUILD_METADATA | Cargo rust-version string and CARGO_PKG_RUST_VERSION equal1.86; package major0. | Build metadata is not an invocation of rustc1.86 or a minimum-toolchain dependency compilation. |
| [client-rust::offline-locked-install](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/tests/pre1_release_boundaries.rs) | STATIC_SOURCE_TEXT_AND_LOCK_METADATA | Checks Cargo.lock package/version; quality/release text contains package/--locked/install and crate lockfile listing. | No cargo --offline installation or complete cached dependency closure is executed by this selected body. |
| [client-rust::package-version-self-report](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/tests/pre1_release_boundaries.rs) | BUILD_METADATA_AND_README_TEXT | Compares package name/version with Cargo build environment; README must contain exact locked install command. | Does not invoke installed CLI, install a crate or compare binary payloads. |
| [client-rust::process-crash-restart](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/tests/service_lifecycle_sqlite.rs) | SQLITE_CRASH_AND_TWO_PROCESS_TERMINAL_RACE | Feature-gated SQLite helper aborts inside uncommitted immediate transaction. Reopen must retain running/sequence1; complete/fail children return0/2; terminal sequence2/events0,1,2. | Requires lifecycle-sqlite feature from dispatch; not real provider restart or power-loss equivalence; selected waits have no explicit timeout. Parent checks crash child non-success, not exact abort provenance; helper source supplies the intended mechanism. |
| [client-rust::rollback-last-supported](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/tests/pre1_release_boundaries.rs) | STATIC_SOURCE_TEXT_ASSERTION | Checks updater source strings for cargo/version/locked/registry/backoff test name; orders Node if-ok/reexec/failure text and record-result-success text. | Does not call installer, updater failure orchestration or actual rollback; source text does not prove runtime preservation under partial replacement. |
| [client-rust::stale-pid-or-lock](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/src/instance_lock.rs) | LOCAL_PID_FILE_RECOVERY | Writes high PID2147483647 in synthetic home then InstanceLock::acquire(force=false) must succeed. | Not a live reused PID or unverifiable owner negative assertion; Linux-specific reuse/refusal sibling tests exist outside selected body. Success assumes the chosen PID is absent in that environment. |
| [client-rust::unsupported-version](https://github.com/RobLe3/iicp-client-rust/blob/0b8b529262977b6482dd7900d473e7d152ba9293/src/runtime_config.rs) | CONFIG_REJECTION | Unknown runtime-config JSON field must fail parsing; schema_version99 must yield unsupported_schema_version. | Not updater SemVer rejection or every unsupported SDK/runtime version; selected body has no valid-config roundtrip assertion. |
| [client-typescript::minimum-version](https://github.com/RobLe3/iicp-client-typescript/blob/97c768d8b9e90756773103e432c273a7d98ba08e/tests/pre1_release_boundaries.test.ts) | DECLARED_METADATA_AND_RUNNING_INTERPRETER | Manifest engines are ^22.0.0 \|\| ^24.0.0; test checks that string, current Node major>=22 and package major0. | The >=22 assertion alone does not reject Node23/25; the declared allowed set and actual admitted runtime identities are separate. |
| [client-typescript::offline-locked-install](https://github.com/RobLe3/iicp-client-typescript/blob/97c768d8b9e90756773103e432c273a7d98ba08e/tests/pre1_release_boundaries.test.ts) | STATIC_SOURCE_TEXT_AND_LOCK_METADATA | Checks lockfileVersion3/root package name; quality/release text includes npm ci, npm pack and install --ignore-scripts. | No network-disabled npm installation, cache completeness or artifact reproduction is executed by this selected body. |
| [client-typescript::package-version-self-report](https://github.com/RobLe3/iicp-client-typescript/blob/97c768d8b9e90756773103e432c273a7d98ba08e/tests/pre1_release_boundaries.test.ts) | STATIC_SOURCE_TEXT_AND_LOCK_METADATA | Compares root lock version/name with package manifest; regex checks CLI source reads package.json. | Does not execute packed CLI or prove generated artifact identity. |
| [client-typescript::process-crash-restart](https://github.com/RobLe3/iicp-client-typescript/blob/97c768d8b9e90756773103e432c273a7d98ba08e/tests/service_lifecycle.test.ts) | SERIALIZED_SNAPSHOT_CHILD_EXIT | Child writes a fully written snapshot of running state synchronously then exits17; parent parses and restores snapshot to running state. | Not a crash mid-write/transaction, atomic persistent store, concurrent terminal-winner race or provider restart; child exit is deliberate after snapshot write. |
| [client-typescript::rollback-last-supported](https://github.com/RobLe3/iicp-client-typescript/blob/97c768d8b9e90756773103e432c273a7d98ba08e/tests/updater.test.ts) | INJECTED_INSTALL_FAILURE | autoUpdateTick uses fake async installerFalse; expects upgrade-failed, zero fake reexec calls and candidate retry blocked. Neighboring success control exists outside selected body. | No failed npm installation or actual previous-artifact restoration is exercised. |
| [client-typescript::unsupported-version](https://github.com/RobLe3/iicp-client-typescript/blob/97c768d8b9e90756773103e432c273a7d98ba08e/tests/updater.test.ts) | VERSION_CLASSIFIER_POSITIVE_AND_NEGATIVE | parseVersion rejects hyphenated rc/v-prefix and accepts0.7.57 tuple. | This is updater candidate syntax, not complete unsupported-runtime/protocol rejection. |

## Cross-SDK distinctions

The selected offline-install bodies inspect lock, workflow and source text; they do not themselves run a network-disabled install. Minimum-version metadata differs from a fresh minimum-toolchain build. Other retained quality or qualification evidence can provide different observations; these limits do not claim that such evidence is absent.

Python and Rust exercise an interrupted SQLite transaction and competing terminal transitions in the described test bodies. TypeScript restores a fully written snapshot of running state after a deliberate child exit. The Rust parent asserts non-success, not the exact child abort cause. Do not turn these into identical persistence guarantees.

Python and TypeScript inject installer failure and check no fake re-exec. The selected Rust rollback test inspects source strings and ordering. These are not actual restoration of a previous artifact after partial installation.

Rust unsupported-version checks runtime configuration, while Python and TypeScript check updater version syntax. The selected Rust PID recovery case does not execute neighboring Linux reused-live-PID refusal controls.

## Historical updater source corrections

| Owner | Correction source | Qualified source |
|---|---|---|
| [RobLe3/iicp-client-python#112](https://github.com/RobLe3/iicp-client-python/issues/112) | [1b60ce099d](https://github.com/RobLe3/iicp-client-python/commit/1b60ce099d33c049e40648b073e479f6ed77ef8f) | [9c5b3d894e](https://github.com/RobLe3/iicp-client-python/tree/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183) |
| [RobLe3/iicp-client-typescript#98](https://github.com/RobLe3/iicp-client-typescript/issues/98) | [27b0383e92](https://github.com/RobLe3/iicp-client-typescript/commit/27b0383e92b9ccfbc9b00f02382da513b4055029) | [97c768d8b9](https://github.com/RobLe3/iicp-client-typescript/tree/97c768d8b9e90756773103e432c273a7d98ba08e) |
| [RobLe3/iicp-client-rust#135](https://github.com/RobLe3/iicp-client-rust/issues/135) | [cf5b89a64e](https://github.com/RobLe3/iicp-client-rust/commit/cf5b89a64e0467fa0a74ea91565381b4ef22f10c) | [0b8b529262](https://github.com/RobLe3/iicp-client-rust/tree/0b8b529262977b6482dd7900d473e7d152ba9293) |

Qualified source requests an exact top-level PyPI version, an exact npm version with lifecycle scripts disabled, and an exact Cargo version with locked resolution, explicit registry and the supplied feature string. No installer, registry, re-exec or updater loop was invoked by this analysis. Source inclusion does not prove artifact authenticity, offline dependency availability, reversible installation or whole-issue acceptance.

## Provenance and accounting

The controlled analysis retains 36 exact qualified source blobs and 13 byte-identical accepted-harness views. The [machine-readable analysis](analysis.json) binds public source paths, digests, declared entrypoints, assertion-depth classes and limitations. Controlled original receipts and captures are not distributed here; digests do not make unavailable original content publicly inspectable.

The partial source frontier now covers 104 of 147 definitions and 5,430 of 5,808 existing coordinate references; 43 definitions and 378 coordinates remain outside it. The universe includes six support definitions plus 141 edge definitions, and 218 support plus 5,590 edge coordinates. These are **source-reference accounting**, not newly executed tests, complete capabilities or new credit.

The selected correction register has 20 owner records: 17 source inclusions and three development-only corrections. These are not 20 distinct product defects or complete supported-scope clearance. The earlier [dated owner-body audit](../2026-11-07-owner-audit/README.md) retains its original 17-record source snapshot.

Historical completeness, all-six defect clearance, a corrected frozen reference and whole-contract conformance remain unestablished. Existing qualification authority is unchanged. No AWS access, workload, original-evidence rewrite, deployment or release follows from this report.

## Verify

From this repository with its pinned Python 3.13 dependencies:

```sh
python3.13 -B scripts/release_recovery_reference.py
```

This verifies the reviewed data identity, closed schema, deterministic Markdown and integrity manifest. It does not rerun the original SDK tests or verify unavailable private artifacts.
