# Six-component defect register and stabilization proposal

## Executive decision

**Do not start a speculative product-repair batch.** The bounded audit found 15 current open issues, including an unresolved supported-scope Rust recovery investigation and an experimental relay report whose fallback/diagnostic boundary still needs assessment. It does not establish a zero-known-defect baseline.

Across the six pinned frozen-to-current comparisons, all 26 intervening commits touch 29 distinct per-repository paths confined to qualification scripts, tests or CI. No product-source path changed in those complete comparisons. This is source-scope evidence, not automatic proof that changed qualification tooling is evidence-compatible.

## Pinned component scope

| Component | Frozen commit | Current main | Open issues | Closed since freeze |
|---|---|---|---:|---:|
| client-python | `9c5b3d894ee89ef9fcde52ea0ad99d388ed62183` | `0cf46aae4beba4304de55ef99cc3a22f72784f30` | 2 | 1 |
| client-typescript | `97c768d8b9e90756773103e432c273a7d98ba08e` | `23a57f7c17cabd9867514d85f248004cdb40617e` | 1 | 2 |
| client-rust | `0b8b529262977b6482dd7900d473e7d152ba9293` | `4020dadd150d7975be468f04a588dfa5346899a5` | 6 | 0 |
| directory-php | `2dfd228b49c587150a44f448cea1351a9f039d32` | `11e63a1b2a3846d376810d260bf9ccbbf59b3d7c` | 2 | 0 |
| directory-rust | `b95a362ad8f974334994ca73cd20210388a2362f` | `6a886a633d50e106ef1e2d5ff21b9e9002e070da` | 2 | 1 |
| management | `9b9c910fe6443068e71152f1a95f41639041c647` | `723de26a5f0d62dbd160546fd598c513b0b3bee6` | 2 | 0 |

## Open dispositions

### client-python
- [Clarify the trust scope of MCP gateway policy receipts](https://github.com/RobLe3/iicp-client-python/issues/142): **TRUST_SCOPE_QUESTION_NOT_DEFECT**. Issue explicitly requires no signing/candidate change; Protocol#256 owns shared semantic decision. Reported release is not automatically frozen candidate equivalence. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
- [[pre-1.0] Freeze the Python API and qualify the declared support matrix](https://github.com/RobLe3/iicp-client-python/issues/119): **RELEASE_OR_OPERATIONAL_GATE_NOT_CONFIRMED_DEFECT**. Criterion-level reconciliation required; current issue state is not a candidate runtime defect proof. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
### client-typescript
- [[pre-1.0] Freeze the TypeScript API and qualify Node 22/24 support](https://github.com/RobLe3/iicp-client-typescript/issues/104): **RELEASE_OR_OPERATIONAL_GATE_NOT_CONFIRMED_DEFECT**. Criterion-level reconciliation required; current issue state is not a candidate runtime defect proof. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
### client-rust
- [[recovery] Diagnose supervised providers absent from Directory after repeated exit-76 recovery](https://github.com/RobLe3/iicp-client-rust/issues/183): **SUPPORTED_SCOPE_INVESTIGATION**. Frozen recovery module matches reported implementation; six actual Node controls passed under synthetic route handling. Full CLI/tunnel/supervisor/original incident cause remains unproven. Next: Assess original route/tunnel/supervisor boundary only under separately scoped investigation; do not repeat six passing controls or infer a correction.
- [[relay][reachability] Reject self-reported relays without a verified worker endpoint](https://github.com/RobLe3/iicp-client-rust/issues/175): **EXPERIMENTAL_RELAY_WITH_SUPPORTED_BOUNDARY_REVIEW**. Keep relay experimental; determine whether fail-closed local-only and safe diagnostic behavior affects supported scope before exclusion. Next: Keep relay experimental; determine whether supported fail-closed fallback and bounded registration diagnostics require a narrowly reproduced correction.
- [[post-1.0][transport] Implement experimental QUIC stream-per-CALL](https://github.com/RobLe3/iicp-client-rust/issues/160): **DEFERRED_RESEARCH_OR_FEATURE**. Preserve existing activation/support exclusions. Not evidence of a supported-scope product defect. Next: Retain the existing deferred/experimental scope; no stabilization expansion without supported-boundary evidence.
- [[research][native] Harden TCP before any later stable admission](https://github.com/RobLe3/iicp-client-rust/issues/158): **DEFERRED_RESEARCH_OR_FEATURE**. Preserve existing activation/support exclusions. Not evidence of a supported-scope product defect. Next: Retain the existing deferred/experimental scope; no stabilization expansion without supported-boundary evidence.
- [[pre-1.0] Freeze the Rust API and qualify the declared target matrix](https://github.com/RobLe3/iicp-client-rust/issues/150): **RELEASE_OR_OPERATIONAL_GATE_NOT_CONFIRMED_DEFECT**. Criterion-level reconciliation required; current issue state is not a candidate runtime defect proof. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
- [Evaluate opt-in MeshLLM ensemble alias after upstream stabilization](https://github.com/RobLe3/iicp-client-rust/issues/98): **DEFERRED_RESEARCH_OR_FEATURE**. Preserve existing activation/support exclusions. Not evidence of a supported-scope product defect. Next: Retain the existing deferred/experimental scope; no stabilization expansion without supported-boundary evidence.
### directory-php
- [[pre-1.0] Qualify the PHP compatibility-anchor support boundary](https://github.com/RobLe3/iicp-directory-php/issues/140): **RELEASE_OR_OPERATIONAL_GATE_NOT_CONFIRMED_DEFECT**. Criterion-level reconciliation required; current issue state is not a candidate runtime defect proof. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
- [[research][registration] Tune registration burst and steady-state limits from evidence](https://github.com/RobLe3/iicp-directory-php/issues/65): **DEFERRED_RESEARCH_OR_FEATURE**. Preserve existing activation/support exclusions. Not evidence of a supported-scope product defect. Next: Retain the existing deferred/experimental scope; no stabilization expansion without supported-boundary evidence.
### directory-rust
- [[pre-1.0] Qualify stable API and persistent non-serving operations](https://github.com/RobLe3/iicp-directory-rust/issues/102): **RELEASE_OR_OPERATIONAL_GATE_NOT_CONFIRMED_DEFECT**. Criterion-level reconciliation required; current issue state is not a candidate runtime defect proof. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
- [Complete Rust directory public-preview parity; retain Genesis cutover gates](https://github.com/RobLe3/iicp-directory-rust/issues/1): **RELEASE_OR_OPERATIONAL_GATE_NOT_CONFIRMED_DEFECT**. Criterion-level reconciliation required; current issue state is not a candidate runtime defect proof. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
### management
- [External authorization evaluator binding on management-profile-v1](https://github.com/RobLe3/iicp-management/issues/168): **OPTIONAL_FUTURE_BINDING**. Non-activating evaluator requirements; explicitly outside frozen qualification baseline. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.
- [[pre-1.0] Freeze stable contracts and pass representative administrator workflows](https://github.com/RobLe3/iicp-management/issues/143): **RELEASE_OR_OPERATIONAL_GATE_NOT_CONFIRMED_DEFECT**. Criterion-level reconciliation required; current issue state is not a candidate runtime defect proof. Next: Reconcile the owning acceptance contract without closing from qualification counters alone.

## Closed defects and original failure preservation

Four issues closed on or after their component freeze date were examined, plus three specifically linked older Rust issues. Their closure dates are not evidence that their fixes postdate the candidate. Five reviewed repair PR merge commits are verified ancestors of the corresponding frozen commit. Fourteen affected product-source blobs also match current main.

- Python #136 / PR137: Windows private-store ACL correction included in frozen source.
- TypeScript #115 and #116 / PR117: Windows npm builder and native ACL corrections included in frozen source.
- Rust #171 / PR170: Windows trust-store persistence/permission corrections included in frozen source.
- Rust Directory #142 / PR143: bracketed IPv6 parsing and guarded rejection correction included in the exact frozen merge commit.
- Rust Directory PR108: MySQL confidentiality-key persistence correction predates and is included in the frozen candidate. Do not confuse a later similarly described failure with proof that this historical correction was absent.
- Rust #9 and #10: historical tunnel/recovery closures remain closed and retained; #183 is a later recurrence investigation, not a retroactive declaration that the original work was never delivered.

Historical closure narratives were read, but their original native test receipts were not re-executed or comprehensively reconstructed. Existing accepted campaign evidence remains separate.

## Consolidated stabilization proposal

- **stage1:** Complete documentation-first review and criterion dispositions. Preserve original qualified candidate and original failures.
- **stage2:** Resolve Rust183 supported-scope investigation and Rust175 supported fallback/diagnostic boundary before deciding a product correction is needed.
- **stage3:** If a supported defect is reproduced, consolidate only demonstrated corrections with reproducing regression assertions, threat/compatibility review and exact source identities into one stabilization successor.
- **stage4:** Apply existing candidate-impact and qualification rules; do not inherit credit into changed product artifacts without current policy. Independently review before execution or merge.
- **no_change_case:** If investigations establish external/operator causes or explicitly excluded experimental behavior, retain the qualified candidate and document bounded dispositions; do not create speculative product fixes.

## Review and stopping boundaries

Require independent review of this register’s exact issue/source comparisons. Any new native experiment or product correction needs its own bounded proposal. Keep documentation-first work moving without manufacturing repairs. The 21 root qualification clauses are a separate reconciliation register and are unchanged.

## Coverage and limitations

- Read-only GitHub queries and local Git ancestry; no tests or workloads executed by this register.
- Closed query covers closure dates on/after each component frozen-commit date, capped100; all six returned below cap.
- Linked older coverage is specifically Rust9,10,171 and correctionPR108; not every historical issue recursively.
- Current main pins are observed snapshots, not production or released versions.
- Complete returned compare lists cover26commits/29paths; path classification does not establish all quality-only compatibility semantics.
- No issue changes, product edits, candidate rebind, source-pin rewrite or acceptance change.
- Full native regression receipts for historical closures were not independently reconstructed here.
- All21root issue-clause questions remain separately unresolved.
