# Analysis-ready qualification dataset, version 2

This is a dated, non-authorizing derivative of root commit
`d9332b9f5a8e88bda28d48643dd4d9be6e1d0859` and public reporting commit
`feaa4ef4d465665caf0fa8d78b45c71c00787eb5`. It does not replace qualification
ledgers, accepted receipts, source contracts or the original v1 analysis.

## What can be compared

`analysis.json` joins all **5,808 accepted assertions**: 218 support cells and
5,590 edge executions. Each row identifies the canonical cell, applicable
scenario, component, runtime, Directory flavor, mode, target and accepted receipt.
Dimensions come from the exact pinned support matrix and scenario catalog, not
from guessing what an identifier means. Source equality and authoritative scope
membership are checked before generating rows.

Comparison groups hold component/runtime/flavor/mode/scenario constant and vary
only the applicable target. Every group states its denominator and excluded
targets. A Directory target absent from its declared matrix is **not applicable
within this pinned scope**, not an inferred pass or a statement about every
possible implementation. This compares accepted dispositions only. Raw-output,
semantic, timing, performance and normative equivalence are not established.

## Chronology is not causality

The dataset preserves 74 public events with their original reported timestamps,
source digests and dispositions. These timestamps are not relabelled as original
execution times. Three reviewed-register anchors connect the six-component audit,
21-clause disposition and partial historical inventory; their execution times
remain unknown. Chronological ordering supplies no causal links. All causal
statuses remain UNKNOWN, all parent lists empty and historical completeness false.
The registers do not turn failures, diagnostics or repeated content into credit.

## DMSC metadata bridge

`dmsc-association.json` inventories 51 original source pins. The private source
readback verified original bytes either at their current location or in the
retained v0.3.1 source package; no manuscript content is copied here. Current hashes
remain separate from original pins. This is a dated retention observation, not
approval of newer sources, paper amendment, semantic equivalence or independent
interoperability. D01–D14 and V01–V13 remain UNASSESSED with no assertion mappings.
The frozen candidate is associated as context only; the paper is not treated as
having tested, endorsed or certified that candidate.

## Reproduce and validate

Use the repository's pinned Python 3.13 dependencies. The generator reuses the
existing public qualification validator and v1 join before adding dimensions:

```sh
python3.13 -B scripts/qualification_analysis_v2.py --output /private/new-analysis.json
python3.13 -B -m unittest discover -s tests -p test_qualification_analysis_v2.py -v
```

The output must not exist. Repository writes are restricted to the designated v2
derivative path; other output belongs outside the repository. Tests compare the
checked-in dataset to a deterministic regeneration and reject mixed candidates,
duplicates, incorrect applicability, diagnostic credit, invented causality,
private dimensions, altered denominators and DMSC maturity promotion.

The input snapshot is deliberately retained so later report publication does not
silently change this dataset. It duplicates public derivatives for reproducible
analysis, not a competing authority. Existing publisher permissions are unchanged;
this dataset, schemas and narrative require ordinary independent review.

## Dated source-drift observation

An independent readback at `2026-11-03T21:55:56.590990Z` found that
`validation-inputs/editorial-review.json` changed after this metadata snapshot:
its snapshot hash was `cf255b36f9b141766010a05b38090305655da943f9c2938ffe2c6588e13d209a`
and the later observed hash was
`89097895c75984b3a99071c0777e4b57a1d18649edb726eeaf3557e6184dc256`.
All 51 original pins remained retrievable in that review (26 matching current
bytes, 25 matching retained v0.3.1 package members). The snapshot is deliberately
not refreshed or relabelled as the latest manuscript state. Retained review
identity: `sha256:deae15ec9444cf077529417ae6e638774a57ca7c65f52a49547f99f42c8a061c`.
