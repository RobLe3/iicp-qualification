# Stabilization readiness: bounded Rust recovery evidence

Two controlled recovery observations passed against the frozen Rust Node implementation on 3 November 2026. This supplement records what those observations establish, preserves the earlier failed attempts, and keeps the remaining questions open. It does not change the accepted integration qualification or establish a defect-free reference baseline.

## What passed

The single sequence completed two controls and two Node cases in **543.23 seconds**. Numeric listener-ownership checks and exact host-local TCP-port controls passed before the Node cases. Each Node case recorded nine heartbeats at the default 30-second interval, with recovery checks every two heartbeats and grace three.

- **Synthetic route restoration:** three available heartbeats, three unavailable, then three available. There was one initial registration and no restart. The runtime-availability handle was controlled by the fixture; actual route or tunnel discovery was not exercised.
- **Heartbeat refusal:** three HTTP 200 heartbeats, three HTTP 401 heartbeats paired with HTTP 403 re-registration responses, then three HTTP 200 heartbeats. The fake Directory accepted the existing token again. This does **not** demonstrate credential repair or a successful new registration.

All 17 input pins remained unchanged. The independent review rechecked retained numeric ownership records, exact-child reaping and the two fixture listener absence assertions. These checks are bounded evidence, not a host-wide resource census. Read the [result](observer-result.json) and [independent review](observer-review.json) for precise scope.

## What did not become complete

Three bounded subclaims gained evidence; **all ten owner-level questions remain open**. Read the preserved [pre-observation matrix](decision-matrix.json) together with its [additive decision delta](decision-delta.json), not as competing current states. The matrix's earlier missing-proof statements are historical inputs; the delta identifies exactly what changed.

Rust SDK #183 still lacks the original incident's causal chain, real route/tunnel observations, default-cadence exit-76 exhaustion, actual supervisor/cooldown evidence and durable operator-host recovery. Experimental relay and fallback questions under #175 were not exercised. Native Windows lifetime-isolation assurance and the 21 formal unresolved criteria were not resolved.

The finite accepted campaign remains **64 shards, 218 support cells, 5,590 edge executions, four sentinels and five project-operated certificates**. This supplement adds zero qualification credit. Independent external certification and stable release readiness remain separate and unestablished by these observations. The [canonical reporting surface](../../STATUS.md) remains the current derivative; this is a dated supplement.

## Failures remain visible

The [attempt history](attempt-history.json) preserves the initial network-control failure, the subsequent listener-ownership guard stop and this passing successor. A successful numeric observer does not establish why the earlier observer failed: its raw polling output was not retained. The tests did not alter product source or retry a failed workload automatically.

## Historical inventory is still partial

The separate historical scan later stopped at discovery page 895 with `SOURCE_DIRECTORY_CHANGED`. Its terminal records 79 original and 816 completed successor partitions. Those terminal counters are not a new validation of the later combined inventory. The published, independently reviewed prefix remains pages **0–313**. The exact changed directory was not localized, and no history reset or retry occurred.

Read the [retained terminal-gap disposition](history-terminal-gap.json). The [earlier bounded checkpoint](../2026-11-03-closeout/README.md) remains unchanged. Historical completeness is **false**; later unreviewed pages must not be silently substituted for that checkpoint.

## Delivery state and next step

At sealing, three of four bounded readiness-delivery gates are complete: decision assessment, reviewed diagnostic preparation, and observed/reviewed execution. The fourth is publication and verified handoff of this disposition. Its later completion must be recorded separately rather than rewriting this sealed package. These four delivery gates are not the ten technical questions or the full post-qualification programme.

Use the [owner disposition](OWNER_DISPOSITION.md) as the proposed issue update, then follow the [handoff](HANDOFF.md). Further runtime work requires an exact proposal for a still-missing boundary, not repetition of these passing cases. No AWS access, product repair, qualification run, evidence admission, deployment or release follows from this document.
