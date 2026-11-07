# Six-component owner-body audit

This dated, non-authorizing supplement indexes **276 reviewed public issue bodies** from six component trackers: 261 CLOSED and 15 OPEN. It is not a count of defects, a proof of resolution, a complete historical archive or a corrected qualified baseline.

## Source universe and verification boundary

The snapshots were captured sequentially on 7 November 2026, approximately 15:11–15:12 UTC. Every CLOSED body in that declared snapshot has a reviewed interpretation; OPEN bodies have a separate scope disposition. This does not cover every comment, timeline, PR-only finding, private record or unfiled operational anomaly. Original body/snapshot bytes are retained in the controlled archive, not distributed here. Hashes identify those originals; they do not make missing or restricted content publicly available.

| Component tracker | Closed bodies | Open bodies | Total bodies |
|---|---:|---:|---:|
| [iicp-client-python](https://github.com/RobLe3/iicp-client-python/issues) | 33 | 2 | 35 |
| [iicp-client-rust](https://github.com/RobLe3/iicp-client-rust/issues) | 46 | 6 | 52 |
| [iicp-client-typescript](https://github.com/RobLe3/iicp-client-typescript/issues) | 27 | 1 | 28 |
| [iicp-directory-php](https://github.com/RobLe3/iicp-directory-php/issues) | 27 | 2 | 29 |
| [iicp-directory-rust](https://github.com/RobLe3/iicp-directory-rust/issues) | 31 | 2 | 33 |
| [iicp-management](https://github.com/RobLe3/iicp-management/issues) | 97 | 2 | 99 |
| **Total** | **261** | **15** | **276** |

CLOSED is an owner-tracker state, not a claim that every unchecked acceptance clause passed. The machine-readable [audit](audit.json) preserves reported historical problems, requirements, suspected findings and uncertainty separately. Rust issues 3 and 4 retain both owner identities but identical source-body hashes; two records do not establish two distinct defect observations.

## Selected correction-source inclusions

Seventeen selected owner records have separate source joins: fourteen corrections are included in the qualified source; three are only in post-qualified development source. Some concern harness, packaging or release integrity. This is neither a complete defect register nor new native validation. Source ancestry and inspected code do not prove every acceptance clause, packaged-byte equivalence, runtime behavior or security property.

| Owner | Source disposition | Qualified source | Correction source |
|---|---|---|---|
| [RobLe3/iicp-client-python#136](https://github.com/RobLe3/iicp-client-python/issues/136) | included in qualified source | [9c5b3d894e](https://github.com/RobLe3/iicp-client-python/tree/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183) | [9c1e8812a1](https://github.com/RobLe3/iicp-client-python/commit/9c1e8812a1cdd5cbd9501778696f264463f5d8ea) |
| [RobLe3/iicp-client-python#145](https://github.com/RobLe3/iicp-client-python/issues/145) | development only | [9c5b3d894e](https://github.com/RobLe3/iicp-client-python/tree/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183) | [6504a60010](https://github.com/RobLe3/iicp-client-python/commit/6504a6001003cf3a95c16614101da94fe8adcb50) |
| [RobLe3/iicp-client-rust#168](https://github.com/RobLe3/iicp-client-rust/issues/168) | included in qualified source | [0b8b529262](https://github.com/RobLe3/iicp-client-rust/tree/0b8b529262977b6482dd7900d473e7d152ba9293) | [97c2558e29](https://github.com/RobLe3/iicp-client-rust/commit/97c2558e298abb57b7295ec0839a7ad8ad70a08f) |
| [RobLe3/iicp-client-rust#169](https://github.com/RobLe3/iicp-client-rust/issues/169) | included in qualified source | [0b8b529262](https://github.com/RobLe3/iicp-client-rust/tree/0b8b529262977b6482dd7900d473e7d152ba9293) | [97c2558e29](https://github.com/RobLe3/iicp-client-rust/commit/97c2558e298abb57b7295ec0839a7ad8ad70a08f) |
| [RobLe3/iicp-client-rust#171](https://github.com/RobLe3/iicp-client-rust/issues/171) | included in qualified source | [0b8b529262](https://github.com/RobLe3/iicp-client-rust/tree/0b8b529262977b6482dd7900d473e7d152ba9293) | [97c2558e29](https://github.com/RobLe3/iicp-client-rust/commit/97c2558e298abb57b7295ec0839a7ad8ad70a08f) |
| [RobLe3/iicp-client-rust#185](https://github.com/RobLe3/iicp-client-rust/issues/185) | development only | [0b8b529262](https://github.com/RobLe3/iicp-client-rust/tree/0b8b529262977b6482dd7900d473e7d152ba9293) | [6bf7e01025](https://github.com/RobLe3/iicp-client-rust/commit/6bf7e0102560b9ab6217049374d3ee79629fd9ed) |
| [RobLe3/iicp-client-typescript#115](https://github.com/RobLe3/iicp-client-typescript/issues/115) | included in qualified source | [97c768d8b9](https://github.com/RobLe3/iicp-client-typescript/tree/97c768d8b9e90756773103e432c273a7d98ba08e) | [da23060066](https://github.com/RobLe3/iicp-client-typescript/commit/da23060066632edeee7bbe2d4259e8698a4d985f) |
| [RobLe3/iicp-client-typescript#116](https://github.com/RobLe3/iicp-client-typescript/issues/116) | included in qualified source | [97c768d8b9](https://github.com/RobLe3/iicp-client-typescript/tree/97c768d8b9e90756773103e432c273a7d98ba08e) | [da23060066](https://github.com/RobLe3/iicp-client-typescript/commit/da23060066632edeee7bbe2d4259e8698a4d985f) |
| [RobLe3/iicp-client-typescript#124](https://github.com/RobLe3/iicp-client-typescript/issues/124) | development only | [97c768d8b9](https://github.com/RobLe3/iicp-client-typescript/tree/97c768d8b9e90756773103e432c273a7d98ba08e) | [65f2c213d3](https://github.com/RobLe3/iicp-client-typescript/commit/65f2c213d321a400f1f92d89ab138519d9b2b11f) |
| [RobLe3/iicp-directory-php#54](https://github.com/RobLe3/iicp-directory-php/issues/54) | included in qualified source | [2dfd228b49](https://github.com/RobLe3/iicp-directory-php/tree/2dfd228b49c587150a44f448cea1351a9f039d32) | [81a4b78697](https://github.com/RobLe3/iicp-directory-php/commit/81a4b7869779356ee12042fdcfe4a1efda20b786) |
| [RobLe3/iicp-directory-php#55](https://github.com/RobLe3/iicp-directory-php/issues/55) | included in qualified source | [2dfd228b49](https://github.com/RobLe3/iicp-directory-php/tree/2dfd228b49c587150a44f448cea1351a9f039d32) | [81a4b78697](https://github.com/RobLe3/iicp-directory-php/commit/81a4b7869779356ee12042fdcfe4a1efda20b786) |
| [RobLe3/iicp-directory-rust#55](https://github.com/RobLe3/iicp-directory-rust/issues/55) | included in qualified source | [b95a362ad8](https://github.com/RobLe3/iicp-directory-rust/tree/b95a362ad8f974334994ca73cd20210388a2362f) | [db50b91862](https://github.com/RobLe3/iicp-directory-rust/commit/db50b91862ccc5a885db57d1cb8254859b514bf3) |
| [RobLe3/iicp-directory-rust#100](https://github.com/RobLe3/iicp-directory-rust/issues/100) | included in qualified source | [b95a362ad8](https://github.com/RobLe3/iicp-directory-rust/tree/b95a362ad8f974334994ca73cd20210388a2362f) | [b307e5a68e](https://github.com/RobLe3/iicp-directory-rust/commit/b307e5a68e391b17e07ac8465c41c3a1382c2858) |
| [RobLe3/iicp-directory-rust#142](https://github.com/RobLe3/iicp-directory-rust/issues/142) | included in qualified source | [b95a362ad8](https://github.com/RobLe3/iicp-directory-rust/tree/b95a362ad8f974334994ca73cd20210388a2362f) | [b95a362ad8](https://github.com/RobLe3/iicp-directory-rust/commit/b95a362ad8f974334994ca73cd20210388a2362f) |
| [RobLe3/iicp-management#139](https://github.com/RobLe3/iicp-management/issues/139) | included in qualified source | [9b9c910fe6](https://github.com/RobLe3/iicp-management/tree/9b9c910fe6443068e71152f1a95f41639041c647) | [fdd0552d5e](https://github.com/RobLe3/iicp-management/commit/fdd0552d5e818aa9964a0da9ffbde0d69c72b887) |
| [RobLe3/iicp-management#141](https://github.com/RobLe3/iicp-management/issues/141) | included in qualified source | [9b9c910fe6](https://github.com/RobLe3/iicp-management/tree/9b9c910fe6443068e71152f1a95f41639041c647) | [db087f649c](https://github.com/RobLe3/iicp-management/commit/db087f649c43910c4e307a01b211283ceff2acf7) |
| [RobLe3/iicp-management#159](https://github.com/RobLe3/iicp-management/issues/159) | included in qualified source | [9b9c910fe6](https://github.com/RobLe3/iicp-management/tree/9b9c910fe6443068e71152f1a95f41639041c647) | [f2ce523ab5](https://github.com/RobLe3/iicp-management/commit/f2ce523ab54f9135f5acad6aee7368482f48f0af) |

The three development-only records concern SDK registration missing-token diagnostics. Their fixes do not transfer old credit to changed artifacts. Selected Windows source includes permission and IPC corrections, but this supplement runs no Windows tests. A named-pipe receive wait is bounded; subsequent cancellation/join is not claimed to have a universal bound. Directory TLS policy checks and strict seed-signature guards do not establish live TLS identity for every endpoint, complete authenticated snapshot bootstrap or joint federation interoperability.

## What remains open

- Full six-component supported-scope defect clearance.
- Exact correction/reproduction/native-evidence joins beyond these selected slices.
- Complete historical source discovery and preservation.
- Corrected successor qualification and immutable functional-reference freeze.
- Separately owned performance, representative-operation and release requirements.

The original qualification ledgers and five project-operated certificates remain authoritative for their original candidate. This supplement changes no accepted receipts, assignments, candidate, acceptance semantics or qualification credit. It establishes neither independent external certification nor release, deployment or publication authority.

## Reproduce public consistency checks

```sh
python3.13 -B scripts/owner_body_reference.py check
python3.13 -B -m unittest discover -s tests -v
```

The checker verifies the pinned sanitized snapshot, schema, membership, counts, temporal classes, source links, privacy markers and generated Markdown. It does not fetch mutable GitHub issues or independently reproduce private originals, source execution or reviewer judgment. New analysis or changed snapshots require normal source review; the report-only publisher cannot modify this package.

Owner: [post-certification programme, root #1678](https://github.com/RobLe3/iicp.network/issues/1678). Historical preservation remains under [root #1676](https://github.com/RobLe3/iicp.network/issues/1676).
