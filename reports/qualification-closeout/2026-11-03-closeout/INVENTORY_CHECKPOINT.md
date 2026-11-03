# Reviewed historical-inventory checkpoint

This is an immutable **partial prefix**, not the terminal result of the active
scan. At 2026-11-03T17:04:42.603904Z, 314 completed page/inventory pairs (indices
0–313) were pinned and independently checked with the existing validators.
Later pages are outside this checkpoint.

| Measurement | Count |
|---|---:|
| Unique evidence-object locators | 271,458 |
| Distinct content digests | 33,936 |
| Retained objects | 270,901 |
| Oversized objects | 556 |
| Unsafe objects | 1 |
| Expected-hash matches | 112 |
| Expected-hash mismatches | 15 |
| Newly hashed objects, without an expected-hash comparison | 270,774 |
| Unique object/gap pairs | 572 |
| Canonical receipt references resolved across the prefix | 64 |
| Remaining discovery frontier entries | 1,250 |

The chain retains 42,669 directory observations in four history segments. It
combines 79 original partitions with 235 successor partitions; the earlier
page-79 refusal remains preserved. A separately authorized diagnostic identified
the original directory-history bound. Segmentation did not erase the old refusal
or reset discovered-object accounting.

The 19,964 per-partition `canonical-receipt-unresolved` occurrences are repeated
local join gaps, **not 19,964 missing accepted receipts**. Across the prefix, all
64 canonical receipt references resolve. Repeated content digests do not create
additional qualification credit. Object counts are not execution-attempt counts.

The [machine-readable summary](inventory-prefix.json) records zero unresolved
*discovery* gaps within this validated chain. That does not eliminate the 572
object/gap pairs, excluded paths, remaining frontier or unknown historical
universe. All enumerated records are classified NOT_ARCHIVE by this inventory;
this checkpoint makes no claim that excluded archive contents were inspected.
The [source-delta analysis](source-delta.md) supplies separate bounded preservation
observations for selected mismatches, not permission to rewrite their original
scan classifications.

**Historical completeness remains false.** The declared roots and exclusions
bound the sample; excluded material is unexamined. No historical total, zero-loss
claim, additional qualification credit or completed cleanup universe follows.

The retained private prefix manifest is identified by
`sha256:17bae9686ac6261320486577fc07c47fd408e1edb87049a88e602197420c663f`.
Its locators are not published. The independently reviewed summary is
`sha256:36b2ce2f756e5825c3f51f23f5f0847a4e13ad12d397cfc6be11bc5c51b3d734`.
Review identity: `sha256:f4688f8c870f5e8cf25ac6dfae519a6dbcbe221b1738d02a874597610cf011eb`.
