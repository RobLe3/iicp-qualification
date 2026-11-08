# Retained artifact bytes and historical validation provenance

**Current original artifact byte identities: 17/17 at examined retained locators.** The earlier [15/17 locator audit](../2026-11-08-reference-reproducibility/README.md) remains unchanged at its dated scope. A separately examined retained ZIP contains the two exact Rust Directory Linux x86-64 members. Their bytes and sizes match the frozen candidate; the executable was neither extracted nor executed.

| Additional retained member | Bytes | SHA-256 |
|---|---:|---|
| iicp-directory-rs-0.1.16-linux-x86_64 | 15125392 | `sha256:bba617940d00cfebfb1d01f029800de5c5d4ca6ed1ed9789d3b1d65e64aab4a5` |
| iicp-directory-rs-0.1.16-release-manifest.json | 349 | `sha256:9d23eacd64195de99ccd2f68468811ff249badeaad611061cdac5e7e9e288d46` |

This is current byte availability, not complete historical custody, full companion/build validation, clean-environment reproduction or a newly frozen reference. The original qualification authority is unchanged.

## Native x86 portability provenance

The final [Rust Directory137 closure comment](https://github.com/RobLe3/iicp-directory-rust/issues/137#issuecomment-5752636558) points to rootPR1452 and its admitted native x86 artifact/closure projections, not just the earlier ARM-only sourcePR138. The later qualified-source fragment records the digest-pinned Bookworm builder/runtime and glibc2.36. These are historical records, not a new execution or fresh cloud absence check.

## Shared database fixture and CI

PHP and Rust test fixtures are byte-identical to the pinned Protocol pre-normative fixture. Both exact historical heads have successful dedicated database-job metadata:

| Implementation | Tested head | Historical job |
|---|---|---|
| RobLe3/iicp-directory-php | `959a2f685eb9e82b565c07010b281d2de3c66549` | [run 31312389950](https://github.com/RobLe3/iicp-directory-php/actions/runs/31312389950/job/93242076898) |
| RobLe3/iicp-directory-rust | `78fa52d55306ae1daae1dc362ca6a72a0befac99` | [run 31312126949](https://github.com/RobLe3/iicp-directory-rust/actions/runs/31312126949/job/93241417565) |

The workflows select real disposable database tests for a shared positive budget,3599/3600-second boundary,persisted repository/service reload and negative deltas. PHP uses MariaDB withpcntl; Rust selects its ignored MySQL test explicitly. Original detailed job-log endpoints returned HTTP410. Successful step metadata and test-source assertions are not a recovered per-assertion transcript or independently verified zero-skip count.

Reload is modeled by service/repository reinitialization, not an OS process restart. PHP concurrency-test source survives unchanged at the qualified source; Rust adds optional arguments at five heartbeat calls. Historical passing CI is not a rerun at the changed qualified source.

## Remaining gaps and boundaries

Rust SDK148 original27-case Docker detail remains owner-reported: a later successful cleanup-only receipt lacks the source/case bindings to substitute for that original result. The current [27 selected correction-source records](../2026-11-08-correction-source-joins/README.md) are unchanged. No whole owner issue or formal criterion is closed here.

- Current byte availability is not complete historical custody or reproducibility.
- Historical successful CI step metadata and source-selected assertions are not detailed per-test output.
- Modeled repository/service reload is not an OS process restart experiment.
- Later success or source ancestry does not reexecute earlier tests at a changed source.
- The earlier dated15/17 locator observation remains unchanged; this is an additive result.
- The original candidate, accepted receipts, certificates and current27-record source register remain unchanged.
- Raw logs, private source locators, cloud identities and controlled archives are not distributed.
- Archive reader checks are observational and size-bounded, not hard CPU limits or adversarial snapshot isolation.
- PHP freezes its policy clock; Rust uses an advancing database clock, so source and successful step metadata do not prove universal exact-second timing.

No new product or qualification workload, cloud operation, evidence promotion, private archive distribution, package publication, deployment or release. The programme remains incomplete. Public verification checks this reviewed derivative; it cannot rehash undistributed private archive members.
