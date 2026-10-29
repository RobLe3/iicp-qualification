# Reporting policy and operations

## Authority and privacy

`reporting-policy.json` binds the frozen candidate, executor registry, shard plan and sentinel ledger. `contracts/scope.json` contains only the finite public assignment identifiers, not private execution inputs. Changes to these contracts need review; the reporter cannot rebind authority.

The extractor reuses the root support, edge, receipt, sentinel and shard-assignment validators. It only credits complete receipts already referenced by merged canonical ledgers. Activity records always grant zero credit. A report PR does not promote evidence.

Public output uses a closed schema and fixed reason/next-gate templates. Do not copy arbitrary log messages, authorization codes, account identifiers, host paths or other private data into it. A new explanatory template is reviewed prose, not an automatic report update. Private event classification is an operator assertion linked to retained source bytes; it is not an independently inferred root cause.

## Required completion step

Record qualification and diagnostic outcomes (including failures, interruptions and refusals), terminal governed CI, correction merges, evidence admissions, cleanup verification, evidence gaps, changed blockers and expired authorizations. Ordinary polling and unrelated edits are not reporting events.

Use a private, owner-only reporting state directory inside the established qualification archive. Keep it outside this public checkout. Maintain one append-only `activity-inbox.json` across sessions; do not start a fresh inbox to discard inconvenient history. The inbox references source paths locally, while only their digests reach public output.

Record a verified activity using the installed, reviewed reporter:

```sh
python3.13 -B scripts/qualification_status.py record \
  --inbox "$PRIVATE_STATE/activity-inbox.json" \
  --source "$RETAINED_TERMINAL_RECORD" \
  --kind diagnostic --outcome FAIL --reason run-failed \
  --next-gate review-failure --occurred-at "$OBSERVED_UTC"
```

Use `--workload-launched` only when the retained record establishes a workload actually started. Use the source's observed time, not an invented execution time. Supported categories and templates are in the policy. Recording the same event again is a no-op.

For the normal completion step, use `finish --context "$PRIVATE_CONTEXT"` with the same activity arguments (without `--inbox`). It records the event and invokes the bounded publisher once. The owner-only context names the clean root checkout, exact source commit, sentinel ledger, archive root, existing inbox and publication state directory. A stale context refuses publication rather than silently switching sources. Keep this context outside Git.

From a clean public `main`, reconcile and conditionally publish:

```sh
python3.13 -B scripts/qualification_status.py publish \
  --root "$PINNED_ROOT_CHECKOUT" --source-commit "$MERGED_ROOT_COMMIT" \
  --sentinel "$RETAINED_SENTINEL_LEDGER" --archive-root "$PRIVATE_ARCHIVE" \
  --inbox "$PRIVATE_STATE/activity-inbox.json" --state-dir "$PRIVATE_STATE"
```

`prepare` accepts the same source arguments without `--state-dir` and writes a local preview only. It leaves report files modified; do not mistake that for publication or bypass the clean-checkout publication guard. Review and preserve a prepared preview before restoring a clean reporting checkout. `check` with those source arguments is read-only and rejects stale reports. Plain `check` verifies public consistency only.

Source checkouts must match the exact selected merged root commit. Existing root validators and transitive Python helpers must be clean. The reporter does not fetch or update a private checkout, reset files, authenticate to AWS, execute a workload or repair a failed test.

## Automatic publication boundary

The maintainer selected automatic bounded updates for this repository. Once the initial implementation and policy are independently reviewed, the publisher may create and merge only changes to the four generated files under `reports/`. It must reproduce their exact bytes from verified source inputs, preserve prior event and receipt records, and pass the required `qualification-report` check for the exact PR head/base. It checks the root main identity again before merge.

No manual approval is requested for a conforming generated update. Everything outside that allowlist follows normal review. This standing reporting permission never expands workload, source-repair, cloud, cleanup, evidence-admission or release authority.

Publication attempts are journaled before the first branch change. Failures leave the branch, intent and any PR intact for inspection; there is no blind retry, force-push or automatic deletion. The next agent reports the pending publication separately from accepted qualification state. Publication uses the existing local GitHub session; public CI receives no private repository credentials or evidence.

## Freshness and failure handling

At session start, compare the existing inbox and pinned qualification inputs with the report. At terminal activity handoff, record the new evidence first, then reconcile. Never declare reporting complete solely because `STATE.md` was edited or a local report was generated. Confirm the public merged commit when publication succeeds.

These controls cover registered activities. They cannot detect an unrecorded manual operation, an offline machine, or inaccessible remote evidence. No background watcher is installed. Report such uncertainty explicitly; do not label the report live or invent a zero-loss claim.

Reporting failure blocks the claim that the documentation handoff is complete. It does not block mandatory teardown, interrupt an admitted test or change an existing qualification acceptance decision. Never weaken production guards to make a status page green.

## Historical and future boundaries

Original records remain append-only in their owning archive. The public event list preserves its prior prefix; Git history preserves report snapshots, and main forbids force-push/deletion. A source-admitted credit reduction or new certificate pathway requires explicit review instead of silent automatic recalculation.

Qualification Heritage, a frozen functional reference baseline, DMSC enhancements and a complete historic incident inventory are later work. This reporting repository provides a narrow starting point, not a claim that those programmes are complete.
