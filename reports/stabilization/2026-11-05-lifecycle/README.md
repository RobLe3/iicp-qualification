# Lifecycle diagnostics: reviewed outcomes and remaining gap

As of 5 November 2026. This is an additive post-qualification diagnostic supplement, not a new qualification admission or a claim that the lifecycle workstream is complete.

The tests used Rust source [`b3d4399f0b2d937c2c7777bb1520309ba1480b1b`](https://github.com/RobLe3/iicp-client-rust/tree/b3d4399f0b2d937c2c7777bb1520309ba1480b1b), the unchanged reviewed CLI binary, and one separately approved instrumented CLI variant. These are distinct diagnostic subjects; their outcomes do not modify the frozen qualified candidate, accepted receipts or five project-operated certificates. Current qualification accounting remains in the [canonical report](../../STATUS.md).

## Outcomes

| Diagnostic subject | Reviewed outcome | Boundary |
|---|---|---|
| Original uninstrumented CLI75 | UNVERIFIED | External timing interval crossed the required cooldown threshold. Preserved, not replaced. |
| Separately approved instrumented CLI75 | PASS | Internal cooldown timing verified for the distinct instrumented variant only. |
| Original SUP76 attempt | UNVERIFIED | Stopped at registration. Fixture identity length conflicted with source normalization; rejected request body was not retained, so exclusive runtime causation is not claimed. |
| Approved SUP76 successor | PASS | Three fixture-network phases; CLI exits 76/76/0, two planned supervisor restarts, restored Directory presence and three healthy heartbeats. Independent sampled absence covered 16 journaled identities. |
| FALLBACK: healthy HTTPS surface, unavailable native transport | FAIL | Actual self-attested candidate selection and an identity-bound heartbeat advertising available=true/status=available while the selected native endpoint was unavailable. Independent sampled absence covered 11 journaled identities. |
| FALLBACK: separate self-report-only and no-candidate cases | NOT RUN | The first failing case stopped the ordered sequence. These cases receive no pass or coverage credit. |

The SUP76 scope is fixture-network transport through the actual CLI and a run-owned supervisor. It does not establish public Internet/NAT reachability or production supervisor behavior. SUP76 did not establish fail-closed public availability: heartbeats remained available=true during route loss, while recovery used registry-route evidence. Original failed and uncertain attempts remain separate records.

## What the FALLBACK observation establishes

An independent, process-local TLS observer verified the fixture's HTTPS surface. The actual CLI discovery/election selected the advertised candidate. The native endpoint remained owned and non-listening through the product observation; independent probes timed out. Same-profile synthetic controls had established allowed-target access and denial of an unlisted target before product launch.

The actual heartbeat advertised public availability despite that unavailable route. Local CLI health remained good. The mock Directory accepted the fixture registration; this does not establish production PHP/Rust Directory acceptance or actual public exposure. The captured CLI exited 0 after the controller's graceful stop, but this did not turn the failing assertion into PASS. The outer controller result is UNVERIFIED with normal exit 2; the retained diagnostic classifier separately records FAIL. Capture was complete and cleanup was independently checked.

The CLI's own native connection attempts were not observable in its logging and remain UNVERIFIED. An independent transport probe is not evidence of a CLI connect syscall. Candidate selection, successful native binding, Directory convergence and verified relay eligibility are separate states; no successful binding or verified-positive relay authority was fabricated.

## Ownership and next decision

The finding corroborates the existing selection/availability gap tracked in [Rust #175](https://github.com/RobLe3/iicp-client-rust/issues/175). It closes neither that issue nor [Rust #183](https://github.com/RobLe3/iicp-client-rust/issues/183); the latter's historical Directory-absence cause is not established by this fixture. [Protocol #59](https://github.com/RobLe3/IICP/issues/59) remains the pre-normative relay-eligibility owner. Internal project diagnostics are not independent interoperability or external certification.

The FALLBACK attempt is consumed. No automatic retry or source-repair budget was reset. A separately reviewed recovery proposal requests a narrow fail-closed availability correction, its regression and independent-review gates, and one source-bound successor diagnostic. It is a proposal, not execution authority.

Lifecycle groups with an admitted attempt: 3/3. Successful predecessor groups: 2/3. Within FALLBACK, 1/3 planned cases ran and 0/3 passed. These denominators must not be combined into one completion score. Criterion dispositions remain 41/41 reviewed (20 supported, 21 unverified), and DMSC assessments 27/27 reviewed; neither metric turns unresolved evidence into PASS. Historical preservation completeness remains unestablished.

## Evidence and public verification limits

The digests below identify original private records and their independent reviews. Authorized documentation agents can resolve their retained locations through the private handoff source index. Public readers can verify this derivative's version history and follow the linked source/owner records, but cannot reproduce private captures from these hashes alone. No raw captures, credentials, account identities or private artifact paths are published here.

| Retained record | SHA-256 |
|---|---|
| original cli disposition | `156831a44e27dd814e14addf661dc983e4debe3e5685bcef89ce8151e703a0e7` |
| instrumented cli predecessor | `b7f7073330274e0b182a55edc81899e60b8dce798bae0bd3a3dee5ed9d286c37` |
| original sup76 disposition | `87853306b2990fad1d64727c6d1e172f9bdb10fae53314ddcb0c51c4b4d10475` |
| sup76 successor terminal | `7d6546a3478e36bd27197205d22e587d816851fdcb872db9720fc78db86154af` |
| sup76 successor review | `2474f26d88791ec7fe56a17faa32dec1109f9f3755a32f93a3063dbbccd376ed` |
| fallback terminal | `1ed12fa3b352e6242e4b856f15d2e5c86ac1ee5247ef6f46dadd13b472c058cf` |
| fallback review | `ed3cada75da81f83105b9672ea98910932a0d78d9cefd2c5dd90aa9e6fce1dbf` |
| fallback fresh absence | `b6fab3713d42a453a657c5f3928f39bc4bf466674e0baa2b9dabdbf80e0d4fdc` |

This supplement adds zero qualification credit. Performance, external interoperability, representative usability and release authorization retain their separate gates.
