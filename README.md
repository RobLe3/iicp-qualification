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
