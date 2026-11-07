# Capability requirements and observed assertion depth

This additive reference connects four existing capability source-contract IDs to twelve selected analytical questions across three local backend profiles. It defines **no new qualification gates**. The 36 rows are not campaign assignments, a comprehensive specification or a requirement to execute 19 additional tests. Existing owners must disposition applicability to the supported scope before any new workload is planned.

## What the evidence supports

- 14 profile/assertion rows have bounded observations.
- 3 rows have only part of the stated field checks.
- 19 rows have no selected runtime witness.
- Whole parent-contract conformance remains **unverified for all four**.

These counts are an evidence map, not a defect count, truth probability or qualification percentage. Original qualification, receipts, certificates and earlier dated source-only NOT_EXECUTED records remain unchanged. Later local observations do not establish that these same assertions executed in the original campaign.

| Selected assertion question | PHP / SQLite | Rust / memory | Rust / MySQL |
|---|---|---|---|
| `CAP-EMPTY.NONEMPTY.ACCEPT` | bounded observation | bounded observation | bounded observation |
| `CAP-EMPTY.EMPTY.REFUSE422` | bounded observation | not exercised here | bounded observation |
| `CAP-UNIQUE.DISTINCT-ID.ACCEPT` | not exercised here | bounded observation | bounded observation |
| `CAP-UNIQUE.SAME-PAIR.NONIDENTICAL.REFUSE` | bounded observation | not exercised here | not exercised here |
| `CAP-UNIQUE.IDLESS.EXACT-DUPLICATE.REFUSE` | not exercised here | not exercised here | not exercised here |
| `CAP-UNIQUE.IDLESS.DISTINCT.ACCEPT` | not exercised here | not exercised here | not exercised here |
| `CAP-PRESERVE.NODE-DETAIL.SELECTED` | bounded observation | not exercised here | bounded observation |
| `CAP-PRESERVE.OPTIONAL-EXTENSION.FLAG-AND-VALUE` | partial fields only | partial fields only | bounded observation |
| `CAP-PRESERVE.TYPED-LIMIT.VALUE-AND-UNIT` | partial fields only | not exercised here | bounded observation |
| `CAP-NODELIST.TWO-VARIANTS.IDENTITY` | not exercised here | bounded observation | bounded observation |
| `CAP-NODELIST.MATCH.NO-CROSS-VARIANT-UNION` | not exercised here | not exercised here | not exercised here |
| `CAP-NODELIST.REQUIRED-EXTENSION.RETAIN-OR-REFUSE` | not exercised here | not exercised here | not exercised here |

## Important distinctions

The selected PHP duplicate method changes a field while retaining intent/variant_id, so its passing refusal isolates the nonidentical same-pair case. The selected Rust duplicate inputs are exact clones with explicit IDs: one refusal can satisfy either duplicate rule, so it does not isolate the nonidentical same-pair branch. Neither implementation is shown defective by that evidence gap. No selected method exercises ID-less exact duplicates or distinct ID-less same-intent variants.

PHP checks an optional extension required flag, but not its payload value. The Rust in-memory method checks the payload value, but not the flag. The MySQL method checks both. PHP checks a typed limit unit but not the numeric value; presence in an input object is not a successful output assertion.

The MySQL capture replay verifies both declared variants, including selected limits and extension fields. Variant order and declared string-set order are not frozen; 8192 and 8192.0 compare numerically. This finite fixture does not establish arbitrary numeric precision, crash durability, real HTTP/TLS, production security or four-platform equivalence.

## Source and authority boundary

The pinned Protocol revision is `2d240649cf8d11a235132658a599e22ebcba6620`. Its node-capability-format document describes itself as draft and normative for REGISTER/NODELIST. The effective-service contract describes an accepted additive pre-normative Profile whose adoption remains parity-gated. This bridge does not ratify the Profile or create a capability-requirements endpoint.

- [spec/v1.9/node-capability-format.md](https://github.com/RobLe3/IICP/blob/2d240649cf8d11a235132658a599e22ebcba6620/spec/v1.9/node-capability-format.md), SHA-256 `9dfb7e20ed011439119fcf00e3d37358b7d92ffff63bbb66b9f65e83e743925e`.
- [docs/architecture/effective-service-capability-semantics.md](https://github.com/RobLe3/IICP/blob/2d240649cf8d11a235132658a599e22ebcba6620/docs/architecture/effective-service-capability-semantics.md), SHA-256 `8afeb2a854d0e6b58a2a8f52945b0155a2175a83c8fa7742cb2e330d7f2e161d`.
- [schemas/effective-capability-advertisement-v1.json](https://github.com/RobLe3/IICP/blob/2d240649cf8d11a235132658a599e22ebcba6620/schemas/effective-capability-advertisement-v1.json), SHA-256 `707da7eebc5e8b55a720386ca713c977beeadd640f4b09eb48ea99573d2b1ab0`.

Each row identifies exact source lines, evidence IDs, proof basis and limitations. An executed pinned test assertion, a replayed capture and merely present source code are different evidence classes. The [preceding method/environment package](../2026-11-07-directory-kernels/README.md) preserves the separate SQLite, in-memory and tmpfs-MySQL contexts and failed attempts.

## Minimized executable vectors

The JSON exports only allowlisted synthetic-fixture capability values, refusal classes and checked row counts. Node identifiers, endpoints, error messages, host paths and credentials are excluded. Private source digests bind the retained observations but do not make their original bytes publicly accessible or independently authenticatable. The pure replay functions compare these selected values; they do not execute a Directory, database, qualification controller or network request.

## Offline verification

```sh
python3.13 -B scripts/capability_assertion_reference.py check
python3.13 -B -m unittest discover -s tests -p "test_capability_assertion_reference.py" -v
```

The checker verifies the reviewed snapshot/schema, row accounting, minimized vectors, deterministic Markdown and manifest. `render` only regenerates this package README and manifest; it does not publish. Obtain the expected manifest digest from the reviewed PR.

## Limits

- 36rows are12selected analytical questions across3local backend profiles,not campaign assignments,all normative requirements,or mandatory new execution gates.
- 14bounded observations,3partial observations and19unexercised rows are not a product-defect count or qualification percentage.
- Passing method/source assertions and rechecked captured values have different proof bases; missing evidence does not show defective code.
- The Profile contract is additive,opt-in and parity-gated; this bridge does not resolve its supported-scope adoption or create a new endpoint.
- Observed vectors are exact allowlisted projections of existing synthetic fixture captures; node IDs,endpoints,private paths,raw error details and credentials are excluded.
- Public checks replay these minimized vectors and validate reviewed source/row identities; they cannot retrieve or independently authenticate unavailable private originals.
- Original failures and dated source-only NOT_EXECUTED records remain preserved. No original qualification credit,full capability conformance,crash durability,real HTTP/TLS,production security,external interoperability or successor freeze is inferred.

[Root #1678](https://github.com/RobLe3/iicp.network/issues/1678) owns this reference work. Protocol Profile adoption remains with [IICP #55](https://github.com/RobLe3/IICP/issues/55); historical preservation remains with [root #1676](https://github.com/RobLe3/iicp.network/issues/1676). No product defect, qualification credit, external interoperability, successor freeze or release authority is established by this analytical supplement.
