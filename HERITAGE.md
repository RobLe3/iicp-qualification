# Qualification heritage foundation

This offline inventory helps locate and verify retained qualification evidence.
It does not admit results, issue certificates or replace the canonical root
validators. A successful inventory check means that the inspected inventory
satisfies its declared contract—not that the entire campaign history survives.

## Authority and source roles

The root repository's merged ledgers, frozen candidate, runner and executor
bindings, and certificate records remain qualification authority. The existing
`collect_status` collector supplies accepted receipt derivatives and performs
its existing source-bound validation. The heritage inventory must not derive
credit from filenames, a `PASS` field, an archive member or an operator note.

Component repositories own their source implementations. Record frozen source
commits separately from current branches and dirty working trees. A different
commit is not proof of different runtime behavior. CI receipts establish their
own checked scope; they do not become native qualification results.

Private run archives retain original approvals, attempts, failures, diagnostic
results and cleanup records. Reporting inbox entries are operator classifications
linked to retained bytes, not an independently inferred causal history. Previous
partial inventories and review reports are useful discovery inputs, not complete
inventories or new admission authority.

The DMSC manuscript, source registry and crosswalks are informative document
inputs. Pin their contents without editing them or rebuilding the document.
D01–D14 architecture records and V01–V13 reviewer records are mapping targets,
not evidence of joint interoperability or an endorsement.

## Private configuration and traversal

Keep the configuration, absolute source locators, manifests and detailed gap
reports in an owner-only directory outside this public checkout. The configured
source roots define the inspected universe. They are not a claim that all
historical sources have been discovered.

Use explicit expected hashes for known authoritative objects. A newly computed
hash records observed bytes; by itself it does not establish their original
identity or durable preservation. Resolve accepted receipt references through
the existing collector and keep each original receipt's admission classification.

Discovery exclusions and explicit verification are separate operations. An
explicitly pinned record may be checked even when its containing directory is
excluded from general traversal. This permits verification of selected DMSC
inputs or canonical receipts without scanning unrelated private material.

Prune Git internals, dependency trees, build caches and the inventory's own output
and working directories. Record excluded root/pattern rules. The exact census of pruned locations and their
contents remains unexamined. Exclusion is not
a finding that the location contains no evidence. Do not follow symlinks or
extract archives. Record size, member-count and expansion limits as limitations;
large or inaccessible objects remain gaps rather than successes. Metadata-only
inspection is not proof that all original bytes remain recoverable.

The initial implementation inspects bounded classic ZIP and uncompressed TAR
metadata only. ZIP64 and oversized ZIP central directories are refused as
limitations; compressed TAR is explicitly uninspected (`UNREADABLE`), not
decompressed. The fixed parser limits supplement the configured member and size
budgets. These dispositions are gaps, not findings that an archive is corrupt.

## Interpretation and review

Keep these questions separate:

1. Was an object discovered and readable?
2. Do its bytes match a previously pinned identity?
3. Does its provenance resolve to the claimed candidate and execution?
4. Was the result admitted by the existing qualification authority?
5. Is the inspected historical universe complete?

A missing object, an unresolved provenance link and a contradicted claim are
not interchangeable. Preserve original outcomes and parent/successor links.
Do not turn an unexecuted, diagnostic, rejected or historical record into credit.
Do not infer successful teardown from absent logs or an empty inventory.

The current reporting contract requires `historical_inventory_complete: false`.
This foundation does not change that policy. A future completeness declaration
would require its own reviewed contract and supporting reconciliation.

## Publication and operational boundary

Public projections must contain only reviewed, content-minimized fields. Do not
publish private paths, arbitrary filenames, identifiers, approval codes or raw
logs. An offline projection is a preview, not publication. The existing bounded
publisher still owns only its established generated-file allowlist; heritage
code, schemas and narrative changes require normal independent review.

No AWS access, workload, source repair, cleanup, evidence promotion or publication
follows from an inventory result. Mandatory teardown must never wait for heritage
maintenance. Original evidence remains unchanged by this tooling; later deletion,
backup or migration requires its separately reviewed preservation controls.

Root issue #1676 coordinates inventory work. Individual qualification issues
retain their own acceptance criteria and authority. Close an issue only after its
full contract is satisfied; recording its unresolved gaps is not completion.

## Local commands

Use the pinned Python 3.13 environment and reviewed dependencies. All output
paths must be absolute paths to new files beneath an owner-only directory outside
this checkout. Parent-relative output paths are refused by the containment guard.
The commands do not publish or overwrite an existing output.

```sh
python3.13 -B scripts/qualification_heritage.py inventory \
  --config "$PRIVATE_CONFIG" --output "$PRIVATE_STATE/inventory.json"
python3.13 -B scripts/qualification_heritage.py check \
  --input "$PRIVATE_STATE/inventory.json"
python3.13 -B scripts/qualification_heritage.py project \
  --input "$PRIVATE_STATE/inventory.json" \
  --output "$PRIVATE_STATE/projection-preview.json"
```

Plain `check` validates the captured inventory. Adding `--config "$PRIVATE_CONFIG"`
repeats the bounded read-only source verification and refuses a changed inventory;
it is a stronger, separate check, not a claim that plain validation reread every
source. Preserve a refused result and investigate the changed object rather than
replacing the baseline. Keep the projection preview private until its normal
review and publication controls are satisfied.
