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

## Inspectable analysis references

The [versioned analysis](data/analysis.json) provides a deterministic join of all
5,808 support/edge assertions to their receipt, candidate and environment digests.
Normative contract mapping remains UNRESOLVED; assertion names are not automatic
specification clauses. The [clause register](data/unresolved-clauses.json) names
each original issue and criterion index through its stable `root-N-clause-I` ID.
Its source digest identifies the retained round-4 register, not a public copy of
the private proof. Empty receipt links mean unassessed mapping, not no evidence.

The [history summary](data/history-gaps.json) preserves the bounded counts above.
The total number of historical attempts is unknown. No causal link is inferred
from date order. Further partition scans must retain their own bounds and cannot
turn the existing partial observation into a claim of complete preservation.

### What the 21 clause references ask

The table paraphrases the original requirements for navigation; it does not
replace their historical wording. Every row remains UNRESOLVED in the analysis.
Use the owning issue and retained source digest before proposing a disposition.

| Clause ID | Question still requiring evidence or an owner decision |
|---|---|
| root-1106-clause-1 | How does the issue's historical frozen-candidate wording relate to the admitted successor? |
| root-1106-clause-6 | What exact evidence-invalidation scope applied to each relevant input change? |
| root-1117-clause-3 | Where is the original corrected-candidate preparation evidence for macOS and Linux ARM64? |
| root-1117-clause-4 | Where is the separately approved native Linux x86-64 environment evidence? |
| root-1117-clause-5 | Where is the separately approved Windows environment evidence? |
| root-1117-clause-6 | Are all required per-lane OS, architecture, isolation, storage and toolchain observations retained? |
| root-1117-clause-7 | What demonstrates safe storage-exhaustion abort and exclusively run-owned disposal? |
| root-1117-clause-8 | What establishes the required native Windows IPC and macOS semantics? |
| root-1117-clause-9 | What establishes complete sequential execution and retained closure bundles for each target? |
| root-1117-clause-10 | What supports all original no-contact, no-mutation, secrecy and evidence-consistency requirements? |
| root-1481-clause-0 | How do released specification and implementation contracts establish Directory-mode applicability? |
| root-1481-clause-3 | How were predecessor macOS evidence and affected registry/shard bindings revalidated or superseded? |
| root-1470-clause-0 | Where are the original exact Windows allocation and teardown grant chains? |
| root-1470-clause-5 | Which records establish preservation before teardown, including failed attempts? |
| root-1470-clause-7 | What establishes shard-0 no-contact and other safety requirements beyond a passing result? |
| root-1470-clause-10 | How should the issue's same-environment wording be interpreted across seven environment digests? |
| root-1470-clause-11 | Is independent resource absence established for every allocation, including failures? |
| root-1493-clause-0 | Do all named entry points maintain the exact candidate and registry/runner/shard bindings? |
| root-1493-clause-2 | Where are historical-behavior and public-schema compatibility dispositions retained? |
| root-1493-clause-3 | What source-closed Linux and certificate reconstruction evidence covers all specified positive/negative requirements? |
| root-1493-clause-4 | Where is the complete required change-gate and source-closure evidence chain? |

Missing proof in this bounded reconciliation is not proof of a failed run.
Conversely, admitted counters alone do not answer every historical requirement.
