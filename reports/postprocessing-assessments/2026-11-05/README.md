# Reviewed post-processing assessments — 5 November 2026

This additive package gives the documentation agent reviewed dispositions for all **41 formal criteria** and bounded assessments for all **27 existing DMSC D/V records**. It is a reporting derivative, not qualification authority. Publication review is pending.

## What the numbers mean

| Workstream | Reviewed | Supported or demonstrated |
|---|---:|---|
| Formal criteria | 41/41 — 100% | 20/41 supported; 21 unverified |
| DMSC assessments | 27/27 — 100% | Bounded relevance/insufficiency findings; zero external experiments |
| Lifecycle diagnostics | One executed | Zero passing; CLI-75 uncertain; SUP-76/FALLBACK not run |

Of the 21 unverified criteria, **three require an owner decision and 18 have evidence gaps**. These are not 21 demonstrated product defects. Review completion is not satisfaction of every requirement. All five criterion-owning issues remain open at the reviewed snapshot.

The DMSC findings identify related accepted internal assertions where appropriate and explain why those assertions do not establish the entire proposed crosswalk experiment. They preserve the original architecture/reviewer identifiers and do not change relation classifications. No DMSC interoperability, external certification or paper amendment is claimed.

## Documentation-agent instructions

1. Start with the [sealed portable handoff](../../documentation-handoff/v2/START_HERE.md).
2. Read the [CLI-75 outcome](../../postprocessing-next/2026-11-05/README.md). Its timing uncertainty is not an undersleep defect or a passing cooldown result.
3. Parse [assessments.json](assessments.json). `criteria` contains exact requirements, dispositions, assessments, remaining proof and owner lookups. `dmsc` contains concern-specific findings, scope limits and exact links to the pinned analysis assertion and receipt IDs.
4. For each assertion, follow its identifier into [analysis-v2](../../analysis-v2/README.md). Scenario relevance is not a proof that every normative contract in a DMSC record was exercised.
5. Preserve unresolved findings in prose and proposed issue updates. Do not close criteria, declare interoperability, rerun diagnostics or alter accepted evidence from this package.

## Provenance and limitations

Criterion review is bound to root source `d9332b9f5a8e88bda28d48643dd4d9be6e1d0859` and freshly read issue requirements. It reuses retained reviewed evidence and CI rather than executing new tests. The earlier candidate and admitted successor remain distinct. Historical completeness remains false.

DMSC assessments use the retained version 0.3.1 crosswalks. They do not silently adopt newer drafts or resolve documented synchronization, parameter-contract or restricted-profile discrepancies. Where relevant, the findings preserve those specific limitations, not just a generic interoperability disclaimer.

The machine-readable package includes the exact independent-review hashes and original crosswalk hashes. Private review records and original captures remain outside the public repository. A digest binds an original; it does not make that original publicly available. The minimized criteria evidence entries intentionally omit private locators, but retain file digests, non-private references and JSON pointers into the pinned private review. Substantive review notes, original DMSC gap/dimension semantics and reviewer-question identities are preserved. Review receipt identifiers permit an authorized archive reader to resolve the complete private evidence chain.

Neither this package nor its validator changes frozen candidate definitions, accepted receipts, certificates or qualification credit. Performance, representative usability, production readiness and release authorization remain separate.

## Verify

Use the repository's pinned Python 3.13 environment:

```sh
python3.13 -B scripts/check_postprocessing_assessments.py
python3.13 -B -m unittest discover -s tests -p test_postprocessing_assessments.py -v
```

The validator checks JSON Schema, exact record coverage, pinned analysis identity, assertion/receipt joins, platform applicability and non-promotion boundaries. Negative controls reject credit inflation, missing/duplicate records, invented receipts/platforms, private host paths and external-success claims. Per-record manifest bindings also reject balanced verdict swaps, changed evidence and dropped caveats. The manifest must come from the reviewed publication; changing both the manifest and data is not independently authenticated by this validator. These checks do not replace substantive review or independently reproduce private original executions.

## Remaining work

- Complete governed publication and link these dispositions from their existing owner issues without silently changing acceptance requirements.
- Preserve historical discovery and evidence-availability gaps under root issue #1676.
- Obtain a separate, valid recovery decision before consuming another lifecycle attempt. The original CLI-75 attempt is consumed; diagnostic continuation remains stopped.
- Prepare any later DMSC editorial update separately. This package is an evidence-analysis handoff, not permission to amend or publish the paper.
