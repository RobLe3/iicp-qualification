# The qualified component baseline

The frozen successor is
`sha256:e7c9aa192be21cdc5ee96e793ab97084137452653cde7580cffd22cf3890618a`.
It is an immutable qualification candidate, not a coordinated stable release.
The source-version column below must not be read as a registry publication or
production deployment claim.

| Component | Frozen source version | Frozen source commit | Declared artifacts |
|---|---|---|---:|
| Python SDK | 0.7.110 | `9c5b3d894ee89ef9fcde52ea0ad99d388ed62183` | 2 |
| TypeScript SDK | 0.7.110 | `97c768d8b9e90756773103e432c273a7d98ba08e` | 2 |
| Rust SDK | 0.7.110 | `0b8b529262977b6482dd7900d473e7d152ba9293` | 2 |
| PHP Directory | 1.10.94 | `2dfd228b49c587150a44f448cea1351a9f039d32` | 2 |
| Rust Directory | 0.1.16 | `b95a362ad8f974334994ca73cd20210388a2362f` | 3 |
| Management | 0.11.0 | `9b9c910fe6443068e71152f1a95f41639041c647` | 6 |
| **Total** | | | **17** |

The artifacts are Python sdist/wheel; TypeScript npm tarball/package-content
manifest; Rust crate/vendored offline package; PHP release archive/manifest;
Rust Directory Linux ARM64 and x86-64 release artifacts/manifest; and Management
four target binaries, crate and release manifest. Seventeen artifact entries are
not seventeen independently qualified products or seventeen certificates.

Source: [frozen successor manifest at the canonical root revision](https://github.com/RobLe3/iicp.network/blob/d9332b9f5a8e88bda28d48643dd4d9be6e1d0859/project/pre1-stability-successor-frozen.json).
Access to the root source may require repository permission. The source index
and public status retain the candidate identity without implying public access
to every original artifact.

## Runtime and implementation boundary

The candidate pins CPython 3.11–3.14, Node 22/24, PHP 8.3 and stable Rust 1.98.0.
Rust client and Management MSRV is 1.86.0; Rust Directory MSRV is 1.88.0.
Qualification covers declared combinations, not every Cartesian combination of
these runtimes, modes and targets. Consult the [assignment scope](data/scope.json).

The Directories have Linux support cells. Windows/macOS client comparison with
PHP and Rust Directory fixtures is not qualification of native Windows/macOS
Directory deployments. Local-only, public and restricted mode assignments remain
part of the finite support contract; they do not authorize contact with operated
production Directories.

Frozen product identity, test-harness identity and execution environment are
separate bindings. A retained run may use a later source-closed test harness while
executing the frozen packaged product. Do not substitute a checkout's current
HEAD for the tested artifact identity.

## What remains outside the baseline claim

Experimental relay/native transports, future federation and optional evaluator
bindings must retain their own support dispositions. Passing same-project PHP/Rust
fixtures does not establish independent clean-room interoperability. No Genesis
cutover, service deployment or artifact publication follows from qualification.
