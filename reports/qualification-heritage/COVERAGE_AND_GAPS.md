# Accepted coverage and unresolved evidence

## Accepted finite coverage

| Target | Accepted shards | Support cells | Edge executions |
|---|---:|---:|---:|
| Linux ARM64 | 16 | 59 | 1,501 |
| Linux x86-64 | 16 | 59 | 1,501 |
| macOS ARM64 | 16 | 50 | 1,294 |
| Windows x86-64 | 16 | 50 | 1,294 |
| **Total** | **64** | **218** | **5,590** |

Sources: [coverage](data/coverage.json), [receipts](data/receipts.json),
[status](data/status.json), and the canonical certificates linked by
[SOURCE_INDEX.json](SOURCE_INDEX.json). Four admission sentinels are prerequisites,
not four additional campaign shards. The five certificates consist of four target
certificates and one ecosystem certificate; they are project-operated.

Linux ARM64 and macOS ARM64 used project-operated local lanes. Linux x86-64 and
Windows x86-64 used temporary AWS-backed lanes. Environment bindings determine
container/native execution details; a local lane is not necessarily bare metal
for every component. Public receipt derivatives do not recreate the private host.

## Issue criteria are not identical to coverage counters

A reviewed close-out matrix contains 41 qualification-related clauses in five
root issues. Twenty are substantiated; 21 remain explicitly unverified:

| Existing owner | Unverified clauses | Remaining question classes |
|---|---:|---|
| root #1106 | 2 | Historical candidate supersession; input-change invalidation scope |
| root #1117 | 8 | Original authority/environment details, storage abort, native semantics, chronology and safety observations |
| root #1481 | 2 | Released-spec mode applicability; disposition of older macOS evidence |
| root #1470 | 5 | Original grants, failed-attempt preservation, no-contact assurance, environment wording and all-allocation closure |
| root #1493 | 4 | Entry-point binding coverage, historical compatibility, Linux provenance and original change gates |
| **Total** | **21** | |

These are neither 21 failed shards nor permission to waive requirements. Preserve
an explicit owner decision for old candidate wording and seven different Windows
environment digests. A successor is not byte-identical historical evidence.
Source: reviewed round-4 criterion disposition, summarized in
[reviewed findings](REVIEWED_FINDINGS.md). Private proof records remain restricted.

## Bounded preservation observation

The November 3 foundation inventory reached its declared **10,000-object cap**.
It recorded 9,940 readable/hash-retained objects, 61 object-gap records and three
discovery-bound records. All 64 accepted receipt references resolved through the
existing source-bound collector. Of the inspected objects, 13 were unsafe paths
and 47 exceeded the per-file bound; one retained archive had uninspected metadata.
The 64 gap records are not a count of 64 missing executions.

The inventory separately records 127 expected-hash matches and 9,813 newly hashed
objects. Newly hashing readable bytes is not independent proof of their original
identity or permanent retention. The canonical edge-result ledger exceeds the
inventory's 1 MiB file limit, while the existing canonical collector still reads
and validates it. An inventory size-limit gap is not missing canonical evidence.

Build/dependency/Git-internal exclusions and unenumerated sources remain explicit.
The earlier October 28 heritage-planning locator was not established by the
bounded search. A later partial inventory must not be substituted for it.
Historical completeness therefore stays **false**. Source: bounded foundation
rehearsal, inventory digest
`sha256:70a6c5678969b3e73f141a08300ab65f66b58b9a5fedc12d21fdf38d869eb894`.
This private inventory is not reproduced in the portable corpus.

## Separate readiness gates

Integration qualification does not establish performance/scale qualification,
representative onboarding or administrator usability, arbitrary-operator
interoperability, independent external certification, production readiness or
stable-release approval. Keep root #1174, #1107 and #1108 and their dependencies
separate. Public [events](data/events.json) describe selected registered activity,
not a complete count of attempts, corrections or failures.
