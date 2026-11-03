# Retained historical reconciliation

The single retained-only execution validated page/inventory pairs 0–894 using the existing merged chain and inventory validators. It did not rerun discovery, inventory collection, integration tests or AWS operations. The source manifest was hashed before processing and every listed input was rehashed after processing. The execution receipt separately pins the reconciliation script and output captures.

The 895 pairs contain 778,978 unique evidence identities and 71,781 distinct content digests. These are retained inventory references, not 778,978 independent campaign events. Availability and integrity remain separate: a retained object can have a digest mismatch. The 15 MISMATCH entries remain unresolved by this accounting step. Archive metadata marked UNREADABLE remains an explicit limitation; no extraction was attempted.

All 64 canonical receipt digests have at least one resolved join across the combined prefix. The 56,223 per-partition unresolved-join occurrences reflect partition-local absence and must not be presented as missing canonical receipts. No diagnostic or historical object receives qualification credit.

Discovery remains incomplete: 118 frontier entries and one recorded discovery gap remain. The terminal successor refused at page 895 with SOURCE_DIRECTORY_CHANGED. A single metadata-only comparison of the 116,148 recorded directory locators found 116,147 identical stamps and one current difference: the declared archive-root directory has unchanged device/inode and changed modification/change timestamps. No children were enumerated for that comparison. This current difference does not establish the original refusal's exact causal circumstances or identify which operation changed the directory. No reset, exclusion change or retry followed.

The previously published 0–313 snapshot is unchanged. Independent comparison matched 634 earlier input pins against this run's manifest and directly verified its one separately retained launch receipt. That launch receipt was not included in this run's before/after pin universe; the separate independent check supplies its retained-byte comparison.

Historical inventory completeness remains false. This is an additive retained-history accounting result, not an expansion of the prior snapshot, a qualification authority change, or a claim of complete preservation. Publication and final gate credit require independent review.
