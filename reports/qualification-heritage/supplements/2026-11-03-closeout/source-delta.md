# Source-delta reconciliation: 15 mismatches

## Decision

The 14 DMSC mismatches are current-source differences, not demonstrated loss of the pinned originals. Every original pinned file is still retrievable byte-for-byte from the retained v0.3.1 source package. All 14 current files match the corresponding v0.4.0 package members. This establishes distinct retained byte sets—not approval, semantic equivalence or permission to substitute versions. Original pins remain unchanged.

The mutable reporting inbox now has 64 entries. Serializing its first 62 entries using its existing sorted, indented JSON format reproduces the exact previously pinned SHA-256. This establishes preservation of that pinned prefix with two appended entries at this observation. It does not independently approve the appended events or prove future immutability.

## Exact DMSC source comparisons

| Source | Pinned originals retained | Current matches scan | Current matches v0.4.0 package |
|---|---|---|---|
| manuscript/metadata.json | Yes | True | True |
| scripts/artifact_names.py | Yes | False | True |
| scripts/build.py | Yes | False | True |
| scripts/check_links.py | Yes | True | True |
| scripts/package_sources.py | Yes | True | True |
| scripts/rebuild_check.py | Yes | True | True |
| scripts/reference_checks.py | Yes | True | True |
| scripts/stage_candidate.py | Yes | True | True |
| scripts/validate.py | Yes | True | True |
| world_model/architecture-model.json | Yes | True | True |
| world_model/dmsc-crosswalk.json | Yes | False | True |
| world_model/editorial-contract.md | Yes | True | True |
| world_model/reviewer-crosswalk.json | Yes | True | True |
| world_model/sources.json | Yes | True | True |

Source digests and package digests are in `source-delta.sanitized.json`; private locators remain in the private sibling only. No archive members were extracted to disk, no source was edited, and no pins were updated.

## Effect on the 21 unresolved clauses

All 21 remain **UNVERIFIED**, with zero new passes. These source deltas do not resolve original human approval chains, every failed allocation’s absence proof, the meaning of historical environment wording, or historical-candidate supersession decisions. The reviewed clause supplement remains the owning evidence map.

The historical scan remains partial and refused. Historical completeness remains false. DMSC D01–D14 and V01–V13 mappings remain unassessed; no qualification, interoperability or certification claim is added.

## Next step

Independently review the byte comparisons and prefix reconstruction. Keep v0.3.1 and v0.4.0 references separate in later documentation; assess any semantic document update under its own source authority. Continue the outstanding clause lookups rather than using these resolved byte-preservation questions to close unrelated requirements.
