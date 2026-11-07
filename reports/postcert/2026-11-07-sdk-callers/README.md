# Actual SDK caller reference slice

This reviewed derivative records fifteen ordinary local caller outcomes: five each for the original Python, TypeScript and Rust SDK submit implementations. It adds **zero qualification credit**. Original acceptance, candidate identity and certificates remain authoritative; this is not a qualified successor or complete functional baseline.

## What executed

| Case | Observed outcome in each SDK | POST calls | Ranker calls |
|---|---|---:|---:|
| Authorized positive | Selected synthetic provider B | 1 | 1 |
| Denied candidates excluded | Selected synthetic provider B | 1 | 1 |
| Foreign ranker choice | Refused: `IICP-CANDIDATE-RANKER-REFUSED` | 0 | 1 |
| No eligible provider | Refused: `IICP-POLICY-ROUTING` | 0 | 0 |
| Ranker abstention | Selected synthetic provider A | 1 | 1 |

Higher-scored disallowed-region and keyless providers were placed before eligible providers. The authorized positive still selected B. A foreign ranker reference was refused before dispatch; abstention retained built-in A selection. Actual request encryption ran. The callback receives a live in-process request: this is not isolation of arbitrary ranker code.

## Source and environment boundary

The [normalized observations](observations.json) pin fifteen original source files at exact repository revisions. Python uses real modules and intercepted HTTP aliases. TypeScript uses strict compilation of the original modules and instance-level HTTP seams. Rust uses original caller/policy/selection/types with a declared private `cfg(test)` HTTP variant; its executable is not an unmodified whole-crate artifact.

| SDK | Actual local toolchain |
|---|---|
| python | CPython 3.11.15 |
| typescript | Node 22.23.2 / TypeScript 5.9.3 |
| rust | Rust/Cargo 1.98.0 |

All observations ran on one local macOS ARM64 host. Python used explicit mixed existing dependency locations, not the original qualified environment. Source, compiler, loaded-module and instrumented-executable identities are retained privately. Local runtime agreement does not demonstrate the four-platform qualification matrix.

## Retained failed bootstrap

The first TypeScript stage failed while its launcher created a local IPC socket, before caller launch. Its original failed disposition and captures remain retained. After stopping, a separately reviewed ordinary-engineering successor used strict ahead-of-time compilation and direct Node execution, without relaxing network denial. The failed stage was not erased or relabelled PASS. Python and the successful Rust build were not repeated. The sole IPC failure cause is not established.

The Rust build also retained an optional debug-stripping warning; review did not treat it as a caller failure or suppress it. Rust executed **one test method containing five outcomes**, with 250 unrelated methods filtered out. Separately, 23 synthetic result-contract controls passed. These counts are not added together.

## Limits

- Synthetic Directory/provider responses; no real DNS, TLS, final HTTP transport admission or provider execution.
- Ranker receives a live in-process request; no claim that an arbitrary ranker cannot leak it.
- Real request encryption does not establish encrypted-response handling, external authorization or joint interoperability.
- OS network denial is not exhaustive attempted-I/O telemetry; owned process-group observation is not an escaped-daemon proof.
- Python mixed dependencies, compiled TypeScript and Rust test-only instrumentation do not establish original qualification environment equivalence.
- Public hashes identify retained private records; they do not distribute those bytes or permit public reproduction of the original executions.
- These fifteen outcomes are a bounded caller sample, not fifteen newly credited qualification assertions or complete functional reference coverage.

## Verify this public derivative

```sh
python3.13 -B scripts/sdk_caller_reference.py check
python3.13 -B -m unittest discover -s tests -p "test_sdk_caller_reference.py" -v
```

These commands check the closed schema, case/history accounting, fixed scope, source links, sanitization, deterministic text and integrity manifest. They **do not rerun the SDK callers**, reproduce private observations or authenticate an arbitrary package copy. Obtain the expected manifest digest from the reviewed PR. `render` regenerates only this reviewed derivative's README and manifest; it does not publish them.

[Root #1678](https://github.com/RobLe3/iicp.network/issues/1678) owns the executable reference. The [earlier enclosing-contract analysis](../2026-11-07-enclosing-capability/README.md) retains its distinct static-source and Directory gaps. Historical completeness, whole supported-scope defect clearance, successor qualification/freeze, external interoperability and release gates remain incomplete.
