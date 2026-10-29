# Agent instructions: public qualification reporting

This repository is a public reporting surface, not qualification authority. Read README.md and REPORTING.md before changes. Keep the private evidence archive separate and unchanged.

## Default after relevant work

1. Read the current report and verify its timestamp and source bindings at session start.
2. For a terminal qualification, diagnostic, CI, correction, admission, cleanup or blocker activity, register its retained source in the existing private inbox. Preserve failures and distinguish refusal from workload execution.
3. Run the source-aware reporting check and bounded publisher using the reviewed implementation. Do not report completion while a required documentation update is unrecorded or publication is pending.
4. Unchanged evidence is a no-op. Do not manufacture status events or commits for routine polling.
5. If reporting fails, preserve its evidence and report the publication gap. Never delay cleanup or interrupt a test to repair reporting.

Only deterministic allowlisted report data is eligible for automatic publication/merge. Code, schemas, templates, policies and authority changes need independent review. Run `python3.13 -B -m unittest discover -s tests -v` and `python3.13 -B scripts/qualification_status.py check` before proposing such changes. A public consistency PASS does not establish source freshness or product correctness.

Use isolated branches, existing local GitHub authentication and the free GitHub plan. No AWS access, workload, ledger writes, private artifact upload, force-push, historical deletion, deployment or release follows from this reporting policy. Do not modify the campaign controller to obtain a documentation update.
