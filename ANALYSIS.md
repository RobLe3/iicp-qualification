# Non-authorizing qualification analysis, version 1

The analysis generator joins admitted public receipt derivatives to the existing
support-cell and edge-assertion scope. It first runs the existing report bundle
validator; it does not replace that validator or admit evidence. The result is a
private working artifact, not an automatically published reporting file.

```bash
python3.13 -B scripts/qualification_analysis.py \
  --data reports/qualification-heritage/data \
  --links /approved/private/analysis-links.json \
  --output /approved/private/analysis-result.json
```

Use the supported Python environment and pinned dependencies. The output must be
outside this checkout and absent before execution. No overwrite, AWS call,
workload, archive deletion or source-authority mutation occurs. Input records are
schema-validated, but approving their asserted source references remains a human
review responsibility; a digest alone does not establish a historical claim.
The generator does not open or rehash the originals behind `source_sha256` or
the fixed DMSC pins. Their availability and content integrity require separately
retained caller evidence; generator success is not a source-resolution PASS.

The `qualification-analysis-v1.json` contract deliberately separates:

- An assertion-to-receipt join over existing admitted assignments.
- Unresolved owner-issue clause references, with no implied assertion mapping.
- Partial historical references with **UNKNOWN** causal links; chronology cannot
  manufacture parent/child causation.
- DMSC architecture IDs D01–D14 and reviewer IDs V01–V13, all **UNASSESSED**.

The DMSC contract pins the three source-catalog hashes for the architecture
crosswalk, reviewer crosswalk and registry. It includes no manuscript or private
locator. A later DMSC revision requires an explicitly reviewed contract change;
passing IICP assertions do not establish protocol equivalence or interoperability.

For the current complete public scope, the result contains 5,808 assertion rows
(218 support cells plus 5,590 edge executions), not 5,808 additional credits.
Canonical candidate/environment/receipt identities are preserved on each row.
Formal requirements are not automatically reconstructed from assertion names.
Historical completeness stays false and new qualification credit stays zero.

The separate `templates/qualification-heritage/DOCUMENTATION_FIRST.md` is the
successor handoff direction. Previously sealed corpora remain byte-identical.
