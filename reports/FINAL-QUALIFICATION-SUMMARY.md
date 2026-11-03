# Final PRE-1 integration qualification summary

Qualification source: `306fa59b707f26c74befd0065087685a1716f991`. Snapshot: 2026-11-02T23:02:39Z.

The declared finite integration campaign has completed with accepted evidence:
64/64 shards, 218/218 support cells, 5,590/5,590 edge executions, four admission
sentinels and five project-operated certificates. Accepted certificates report
zero skips, flakes and waivers. This does not establish absence of all defects.

| Target | Shards | Support cells | Edge executions |
| --- | ---: | ---: | ---: |
| Linux ARM64 | 16 | 59 | 1,501 |
| Linux x86-64 | 16 | 59 | 1,501 |
| macOS ARM64 | 16 | 50 | 1,294 |
| Windows x86-64 | 16 | 50 | 1,294 |

## Evidence and scope

The system boundary comprises Python, TypeScript and Rust SDKs, PHP and Rust
Directories, and Management. Coverage is limited to the frozen support and
scenario assignments; it is not a claim about arbitrary runtime combinations.
The [status record](status.json) binds the candidate and provides certificate
derivatives; [receipts](receipts.json) identify accepted assignments and source
hashes. [Reporting policy](../REPORTING.md) explains authority and privacy.

Linux ARM64 and macOS ARM64 are project-operated local lanes. Linux x86-64 and
Windows x86-64 use project-operated temporary AWS environments. Local execution
must not be equated with bare-metal execution for every component: consult the
bound environments for isolation, runtimes and comparative Directory conditions.

The canonical five certificate files were admitted by root PR #1674. The root
repository and retained execution archive are access-restricted. Public
consistency checks do not reproduce those private sources or establish external
certification; source-aware checks additionally use the retained canonical inputs.

## History and limitations

The [event register](events.json) contains 56 selected events, not every attempt.
Historical inventory completeness remains false. Campaign history includes
product, harness, environmental and evidence-lifecycle investigations; a detailed
causal chronology remains under reconciliation. Subsequent success must not be
used to invent root causes or erase earlier failures.

Integration qualification does not establish independent third-party
certification, arbitrary-operator interoperability, performance qualification,
representative usability, production readiness or stable release authorization.
The supported-scope defect audit and separate release gates remain outstanding.
Private logs are not reproduced here. A digest is not proof that every original
artifact is still available; unavailable history must remain explicitly unresolved.

## Verification

Use the supported Python 3.13 environment and pinned dependencies:

```sh
python3.13 -B scripts/qualification_status.py check
python3.13 -B -m unittest discover -s tests -v
```

The first command checks public consistency. Maintainers perform the additional
source-aware check with the private pinned context. Neither command launches
qualification workloads or issues certificates.
