# IICP qualification heritage: start here

This handoff is a readable, source-linked foundation for another engineer or
agent. It explains the accepted qualification, the implementation boundary,
what the retained evidence can establish, and what still needs work. It is not
a new test campaign, an independent certificate or a release authorization.

## What is established

The declared finite PRE-1 campaign has **64 accepted shards, 218 support cells,
5,590 edge executions, four admission sentinels and five project-operated
certificates**. Each of four targets has shards 0–15 exactly once. The admitted
certificate set reports zero skips, flakes and waivers. Root PR #1674 admitted
the certificates; canonical root commit
`d9332b9f5a8e88bda28d48643dd4d9be6e1d0859` contains the current close-out handoff.
These counts describe admitted evidence—not all attempts or all possible behavior.
Sources: [status](data/status.json), [receipts](data/receipts.json),
[certificate derivatives](data/certificates.json), and [source authority](SOURCE_AUTHORITY.md).

## Read in this order

1. [Component baseline](COMPONENT_BASELINE.md): six components, the frozen
   candidate, 17 declared artifacts and supported runtime boundary.
2. [Coverage and gaps](COVERAGE_AND_GAPS.md): platform coverage, formal acceptance,
   remaining evidence questions and preservation limits.
3. [Reviewed findings](REVIEWED_FINDINGS.md): what the close-out review actually
   found, with root-cause confidence and the next discriminating checks.
4. [Source authority](SOURCE_AUTHORITY.md): which records own qualification,
   which are derivatives, and what a portable verification can establish.
5. [Agent brief](AGENT_BRIEF.md): exact launch prompt and safe next work.

For machine-readable inspection, start with [coverage](data/coverage.json),
[assignment scope](data/scope.json), [receipt derivatives](data/receipts.json),
[source index](SOURCE_INDEX.json) and the package manifest. From the corpus directory, with Python 3.13 and the
pinned `jsonschema==4.26.0` dependency available, run:

```bash
python3.13 -B verify.py --expected-manifest-sha256 sha256:<reviewed-manifest-digest>
```

Obtain that digest separately from the reviewed package or PR; do not simply
compute it from the copy being verified and call that authentication. Without
an external trusted digest, verification establishes bundled hash and public-data
consistency, not independent authenticity. The verifier does not install
dependencies automatically. Verification of a portable copy does not repeat
private root validation or native tests.

## Next engineering decision

Do not restart successful qualification merely to make this handoff richer.
First resolve the Windows workload-isolation assurance question and the remaining
21 qualification-related issue clauses. In parallel, use the bounded Rust SDK
#183 reproducer work to distinguish a supported-scope product defect from a
route, registration or supervisor problem. No current finding justifies silently
changing accepted evidence or claiming a zero-known-defect baseline.

The next milestone is a reviewed disposition and stabilization proposal, not
new feature development. Performance, representative usability, independent
interoperability, production readiness and stable publication retain separate
gates. No AWS operation, workload, cleanup or release is authorized by this package.

## What this package deliberately does not contain

Original private logs, credentials, account/resource identities, human approval
records and raw diagnostic envelopes are excluded. The DMSC manuscript is not
included: only its established crosswalk identities and source references may be
used here. Historical completeness remains **false**. A reader can verify the
portable files and inspect the claims, but cannot reconstruct every private run
from these derivatives.
