# Directory registration and capability witnesses

These are selected ordinary post-certification observations, not qualification receipts or a complete functional reference. They add **zero qualification credit** and do not change the accepted candidate, original evidence or five project-operated certificates.

## Executed methods and environments

| Profile | Backend | Passing distinct methods | Actual method executions | Failed method executions |
|---|---|---:|---:|---:|
| php-sqlite | SQLite memory / in-process Laravel HTTP kernel | 4 | 5 | 1 |
| rust-memory | InMemoryRepo / in-process HTTP kernel | 3 | 3 | 0 |
| rust-mysql | MySqlRepo / disposable tmpfs database / in-process HTTP kernel | 1 | 1 | 0 |

The profiles are not a matched platform comparison. Do not add refusal inputs, assertions, synthetic controls and executed methods into a coverage percentage.

### PHP / SQLite

Three frozen EffectiveCapabilityProfileTest methods passed with 16 assertions. A new empty-capability method first failed on a Laravel-default response-shape expectation, after its 422 assertion passed. The original failed response body was not retained; no runtime error-code or unchanged-row claim is inferred for that failed attempt. Source review supported the existing IICP error envelope, not the new oracle. Only the corrected private method was rerun: it passed seven assertions, including validation_error and unchanged node count. The three original successes were not repeated. Four distinct methods therefore have passing evidence across five executions, not one clean four-method run.

### Rust / InMemoryRepo

Three original frozen methods passed once each: registration/discovery of two variants; duplicate variants and invalid limits; malformed, duplicate and oversized profile sets. The original selector expected the wrong test namespace and refused before method execution. A reviewed selector successor reused the existing build and listing. This in-memory evidence does not establish database persistence.

### Rust / MySQL

One new private cfg(test) method passed once. Actual HTTP-kernel registration used MySqlRepo. Two variants survived closure of the writer pool and readback through a fresh reader pool, node-detail and discovery. Six invalid inputs returned 422 / validation_error: empty capabilities, duplicate variants, negative token limit, malformed profile, duplicate profile and oversized profile set. Checked positive capability fields and one node / two capability row counts remained unchanged after each refusal.

The native predecessor refused its actual host-port boundary before application execution. The Linux successor compiled successfully but its executable-discovery wrapper then failed before listing or application execution. A separately reviewed continuation reused the exact Cargo-produced ELF without rebuild or permission change. Successful execution does not establish the sole earlier glob failure cause. Both failures remain failures.

The database was disposable tmpfs MySQL 8.0.46. Fresh-pool readback is not crash/restart or disk durability. Resource captures preceded exact-owned removal; separate parent-performed readback was inspected by an independent reviewer. This is not external certification.

## Method-to-observation index

- `php-sqlite / Tests\Feature\EffectiveCapabilityProfileTest::test_shared_fixture_is_exactly_pinned` (ORIGINAL_FROZEN): shared fixture exact pin. Retained evidence ID: `php-witness`.
- `php-sqlite / Tests\Feature\EffectiveCapabilityProfileTest::test_effective_variant_survives_registration_and_node_projection` (ORIGINAL_FROZEN): one effective variant survives registration and node projection. Retained evidence ID: `php-witness`.
- `php-sqlite / Tests\Feature\EffectiveCapabilityProfileTest::test_exact_duplicates_and_duplicate_variant_ids_are_rejected` (ORIGINAL_FROZEN): exact duplicate and duplicate variant identifiers refused. Retained evidence ID: `php-witness`.
- `php-sqlite / Tests\Feature\PostcertEmptyCapabilityTest::test_empty_capabilities_refused_without_new_node` (PRIVATE_TEST_ONLY): empty capabilities refused with validation_error and unchanged node count. Retained evidence ID: `php-witness`.
- `rust-memory / tests::effective_capability_variants_survive_registration_and_discovery` (ORIGINAL_FROZEN): HTTP kernel201 registration; same in-memory state discover; two variants retained; selected version,phase,variant,feature and optional-extension assertions. Retained evidence ID: `rust-memory-witness`.
- `rust-memory / tests::registration_rejects_duplicate_capability_variants_and_invalid_limits` (ORIGINAL_FROZEN): duplicate intent/variant and negative token limit refused. Retained evidence ID: `rust-memory-witness`.
- `rust-memory / tests::registration_rejects_malformed_or_oversized_capability_profiles` (ORIGINAL_FROZEN): malformed, duplicate and oversized profile sets refused. Retained evidence ID: `rust-memory-witness`.
- `rust-mysql / tests::postcert_registration_persists_variants_and_refuses_invalid_mysql` (PRIVATE_TEST_ONLY): two registered variants retained through fresh-pool node-detail and discovery; six invalid inputs refused with 422 / validation_error; checked positive capability fields and one node / two capability rows unchanged after each refusal. Retained evidence ID: `rust-mysql-witness`.

## Exact source and evidence identities

The source metadata records frozen implementation revisions and public source links. Private witness and review digests identify retained originals; public validation does not retrieve or reproduce those originals. Newly authored test-only methods are not represented as original qualification methods. Historical pending-review fields in original witness records are preserved; separate review records bind the later accepted observations.

- [RobLe3/iicp-directory-php / tests/Feature/EffectiveCapabilityProfileTest.php](https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/tests/Feature/EffectiveCapabilityProfileTest.php), SHA-256 `25f2235fb239c1eeaa5e163f33b2e82f2c8b52dbe2664e5e99d06de924b063c0`.
- [RobLe3/iicp-directory-php / bootstrap/app.php](https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/bootstrap/app.php), SHA-256 `7ca622651c079da6b1ad6842b5aa5b2d5ed3b69afa1059239d685dce3b4920fe`.
- [RobLe3/iicp-directory-php / app/Http/Controllers/RegisterController.php](https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/app/Http/Controllers/RegisterController.php), SHA-256 `2ded78ffec0820fac57483a6f281e57ad214fd52d85bffb0cc19597f3c04403c`.
- [RobLe3/iicp-directory-php / composer.lock](https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/composer.lock), SHA-256 `f811bb53f3a4862d8a7b0cc8095a39ecfae655f5447fc8ef94a3b58c62a85ad9`.
- [RobLe3/iicp-directory-rust / src/main.rs](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/main.rs), SHA-256 `9de172ee8f008ae43977e91a23dc66cf9cf499c31a74251944331d848577d1a9`.
- [RobLe3/iicp-directory-rust / src/main_tests.rs](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/main_tests.rs), SHA-256 `80672e4fe2c45ddd325e41e02df09e28bb24f6e19444dd004b2d57eac9446251`.
- [RobLe3/iicp-directory-rust / src/repo.rs](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/repo.rs), SHA-256 `00a44453ef632cda1e5af47867a8de7c20dad52b231543d4df9e54b8032d053f`.
- [RobLe3/iicp-directory-rust / src/registration_store.rs](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/registration_store.rs), SHA-256 `c1e65f7aeb857d637dbef4716a956e295611ee32e24b80491e5834aa4e7b2234`.
- [RobLe3/iicp-directory-rust / Cargo.lock](https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/Cargo.lock), SHA-256 `4a47d155ad1eeed4587ed1b205788b9855d3027c0cbdceb28a5b932d98b15910`.

## Limits

- These are selected post-certification observations, not the original qualification execution or an accepted successor.
- Different backends, runtime contexts and assertion depths are not a matched cross-platform or whole-implementation equivalence experiment.
- PHP uses SQLite memory, testing allowances and fake external health; one variant and selected fields do not prove arbitrary extension or complete node-list preservation.
- Rust memory tests use InMemoryRepo and explicit liveness bypass; passing methods do not establish MySQL behavior.
- The separate Rust MySQL method demonstrates fresh-connection readback on tmpfs, not process crash, restart or disk durability.
- All three profiles use an in-process HTTP kernel; real HTTP/TLS, production startup and security are not established.
- PHP original three passing methods were not repeated; its newly authored oracle failed once and only that corrected method was rerun. This is not a clean four-method single run.
- Native MySQL topology refusal and Linux postcompile wrapper failure remain failures. Successful retained-artifact execution does not establish the sole earlier glob cause.
- Raw responses and private execution records are not distributed. Digests identify retained sources but do not make them publicly reproducible.
- Whole capability contracts, complete supported-scope defect clearance, historical preservation, semantic IFRB, successor freeze, external interoperability and release readiness remain incomplete.

## Offline verification

```sh
python3.13 -B scripts/directory_kernel_reference.py check
python3.13 -B -m unittest discover -s tests -p "test_directory_kernel_reference.py" -v
```

These commands validate reviewed metadata, closed schema, method/attempt accounting, lineage, source/evidence identities, sanitization, generated text and the manifest. They execute no Directory, database or workload. `render` regenerates only the package README and manifest; it does not publish. Obtain the expected manifest digest from the reviewed PR rather than trusting an arbitrary copy.

[Root #1678](https://github.com/RobLe3/iicp.network/issues/1678) owns the executable reference; [#1676](https://github.com/RobLe3/iicp.network/issues/1676) owns historical inventory. The [enclosing source mapping](../2026-11-07-enclosing-capability/README.md) and [SDK caller observations](../2026-11-07-sdk-callers/README.md) remain separate evidence layers. This supplement does not close whole capability contracts, authorize a successor or establish release readiness.
