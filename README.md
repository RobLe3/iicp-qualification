# IICP qualification

Public, source-linked reporting for IICP's pre-1.0 integration and qualification campaign.

## Current state

**[Read the current qualification report](reports/STATUS.md)** for accepted coverage, platform progress, the latest registered blocker and the next required gate. [Machine-readable status](reports/status.json), [receipt derivatives](reports/receipts.json) and [activity history](reports/events.json) support inspection without access to the private coordination repository.

Qualification asks whether the frozen candidate passes its declared finite set of support and edge-case assertions. It does not, by itself, establish independent interoperability, external certification or release readiness.

## What this repository owns

This repository owns public reporting and its validation. It **does not own qualification acceptance**. Accepted counts are derived from the merged ledgers in the private `RobLe3/iicp.network` coordination repository and checked using that repository's existing validators.

The private local evidence archive remains separate. Original receipts, failed output, authorization records and journals are not imported here. Public records are deliberately minimized derivatives with source digests. Those digests identify original evidence; they do not make unavailable original content independently inspectable.

The public report distinguishes accepted evidence, passing-but-unpromoted work, diagnostics, CI, refusals and failures. Historical failures are not rewritten after a correction. The activity index initially contains selected verified records; a complete historical inventory and the later functional reference baseline are not yet delivered.

## Verify the public report

Use Python 3.13 and an isolated environment:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -B scripts/qualification_status.py check
.venv/bin/python -B -m unittest discover -s tests -v
```

This verifies schema, scope, hashes, generated text and internal accounting. It cannot reproduce the original workloads or validate private evidence that is not distributed here. Maintainer-side source verification additionally uses the pinned private checkout and retained records; see [reporting operations](REPORTING.md).

## Reporting defaults

After a relevant activity completes, the agent records its terminal outcome and runs source-aware reconciliation. Report-only changes can be published automatically under the reviewed, bounded policy. Code, schemas, authority bindings, new narrative and policy changes require review. See [the update policy](REPORTING.md) and [agent instructions](AGENTS.md).

An unchanged input set creates no commit. A reporting failure remains visible in the private handoff and must not interrupt a workload or delay cleanup. The public page is an **as-of record**, not a continuously running monitor.

## Ecosystem sources

- [Protocol and capability boundary](https://github.com/RobLe3/IICP/tree/main/pre1)
- SDKs: [Python](https://github.com/RobLe3/iicp-client-python), [TypeScript](https://github.com/RobLe3/iicp-client-typescript), [Rust](https://github.com/RobLe3/iicp-client-rust)
- Directories: [PHP](https://github.com/RobLe3/iicp-directory-php), [Rust](https://github.com/RobLe3/iicp-directory-rust)
- [Management](https://github.com/RobLe3/iicp-management)

Publication, deployment, adoption, qualification and certification remain separate states. Nothing here authorizes a workload, cloud allocation, evidence promotion, release or deployment.

## PRE-1 qualification evidence

The finite integration campaign is complete; release readiness remains separate.
See [verified qualification status](https://github.com/RobLe3/iicp-qualification/blob/main/reports/STATUS.md)
and its reporting-policy limitations. Historical inventory is not complete.

Read the [final integration qualification summary](reports/FINAL-QUALIFICATION-SUMMARY.md)
for scope, platform distinctions and public verification limits.

## Documentation-agent handoff

Start with the [portable heritage corpus](reports/qualification-heritage/START_HERE.md)
for the source-linked baseline, coverage, reviewed findings and limitations.
Its manifest and offline verifier bind the packaged snapshot; obtain the expected
manifest digest from the reviewed publication rather than trusting a digest
computed from an unverified copy.

[Heritage tooling](HERITAGE.md) describes bounded inventory and private/public
separation. The corpus is a dated documentation foundation, not a complete private
archive or qualification authority. Historical completeness remains false.
Inventory work is tracked in [root issue #1676](https://github.com/RobLe3/iicp.network/issues/1676).

## Stabilization-readiness observations

The [3 November bounded successor supplement](reports/qualification-closeout/2026-11-03-stabilization-successor/README.md) records two passing controlled Rust Node transitions and their limits, preserves the earlier diagnostic failures, and retains all ten owner questions. It adds no qualification credit and does not close the Windows assurance or historical-inventory gaps.

## Post-qualification engineering inputs

[Read the reviewed-input package checkpoint](reports/postprocessing-final/2026-11-04/README.md) for normalized assertions, bounded engineering findings, DMSC source bindings and retained historical accounting. Its delivery progress is separate from historical completeness and release readiness.

## Stabilization observations

[The bounded 4 November findings](reports/stabilization/2026-11-04/README.md) preserve a diagnostic-disclosure failure and locally tested, unmerged correction. They do not alter qualification credit or close the remaining owner questions.

## Rust diagnostic correction

[Governed merge and successor qualification boundary](reports/stabilization/rust185-governed-closure-2026-11-04/README.md) records the narrow registration diagnostic fix, preserved failed validation and remaining candidate-impact gates.

## Post-processing continuation

[Staged milestone plan and documentation-agent supplement](reports/postprocessing-next/2026-11-05/README.md) separates completed inputs from pending lifecycle diagnostics and analysis. This additive plan is under review; it does not alter the sealed corpus or qualification results.

## Reviewed criterion and DMSC assessments

[The 5 November assessment package](reports/postprocessing-assessments/2026-11-05/README.md) distinguishes 41 reviewed criterion dispositions from 20 supported criteria, and 27 reviewed DMSC assessments from unestablished external interoperability. This additive package is under publication review.

## Lifecycle diagnostic follow-up

[The reviewed 5 November lifecycle supplement](reports/stabilization/2026-11-05-lifecycle/README.md) separates the instrumented CLI result, SUP76 recovery and a failing FALLBACK availability observation. It preserves the original uncertain results, unexecuted cases and unresolved owner requirements. These diagnostics add no qualification credit.

See the [reviewed FALLBACK successor closeout](reports/stabilization/2026-11-05-fallback-successor/README.md) for bounded corrected outcomes, preserved original failures and remaining relay-eligibility limits.

## Post-certification source-semantic checkpoint

[Read the 5 November source and recorded-proof analysis](reports/postcert/2026-11-05-source-semantics/README.md) for exact test-body limits, Directory assertion-depth differences and existing accepted case-proof linkage. This is an informative supplement, not a frozen executable baseline or new qualification credit.

## Selected confidentiality and identity assertions

[Read the reviewed capability-source slices](reports/postcert/2026-11-05-capability-slices/README.md) for selected confidentiality and identity-lifecycle predicates, exact source links and public coordinate-count verification. Shared fixtures do not imply identical assertion coverage or actual process restarts. This is partial source analysis, not a new qualification result or frozen reference baseline.

## Successor-source and owner-boundary audit

[The 6 November source and owner audit](reports/postcert/2026-11-06-source-owner-audit/README.md) compares six pinned component sources, preserves intermediate changes and separates six owner questions from whole-issue completion. It grants no artifact equivalence, qualification credit or execution authority.
