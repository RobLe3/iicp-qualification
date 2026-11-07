"""Read-only validation/rendering of a dated SDK source-analysis reference."""
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'reports/postcert/2026-11-07-release-recovery'
DATA_PIN = '35973f2395fc6f6aa6ee231caf52602527d6ac18889eca7a75133745c3672cd3'
SCHEMA_PIN = 'fa2d24da2646d1aa63d31c7e6ae9a87570d8216a6c77c8d9d1be359543f156dc'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def load():
    return json.loads((DATA / 'analysis.json').read_bytes())

def validate(value):
    privacy(value)
    raw = (DATA / 'analysis.schema.json').read_bytes()
    require(sha(raw) == SCHEMA_PIN, 'schema identity')
    Draft202012Validator(json.loads(raw)).validate(value)
    require(len(value['cases']) == len({r['case_id'] for r in value['cases']}) == 19, 'nineteen unique cases')
    require(sum(r['existing_coordinate_count'] for r in value['cases']) == 1200, 'existing reference count')
    require(len(value['correction_source_joins']) == 3, 'three selected source joins')
    require(sha(canonical(value)) == DATA_PIN, 'reviewed source interpretation identity')
    return True

def cell(value):
    return str(value).replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br>').replace('|', '\\|')

def render(value):
    validate(value)
    lines = ['# SDK release and recovery assertion depth', '',
      'This reviewed source analysis covers **19 case definitions** and **1,200 existing accepted coordinate references** across the three SDKs. It does not execute those cases, add qualification credit or establish complete semantic contracts.', '',
      '## What the selected tests actually assert', '',
      '| Case | Selected assertion depth | Predicate | Explicit limit |',
      '|---|---|---|---|']
    for row in value['cases']:
        lines.append(f"| [{row['case_id']}]({row['source_url']}) | {cell(row['assertion_depth'])} | {cell(row['selected_predicate'])} | {cell(row['limitations'])} |")
    lines += ['', '## Cross-SDK distinctions', '',
      'The selected offline-install bodies inspect lock, workflow and source text; they do not themselves run a network-disabled install. Minimum-version metadata differs from a fresh minimum-toolchain build. Other retained quality or qualification evidence can provide different observations; these limits do not claim that such evidence is absent.', '',
      'Python and Rust exercise an interrupted SQLite transaction and competing terminal transitions in the described test bodies. TypeScript restores a fully written snapshot of running state after a deliberate child exit. The Rust parent asserts non-success, not the exact child abort cause. Do not turn these into identical persistence guarantees.', '',
      'Python and TypeScript inject installer failure and check no fake re-exec. The selected Rust rollback test inspects source strings and ordering. These are not actual restoration of a previous artifact after partial installation.', '',
      'Rust unsupported-version checks runtime configuration, while Python and TypeScript check updater version syntax. The selected Rust PID recovery case does not execute neighboring Linux reused-live-PID refusal controls.', '',
      '## Historical updater source corrections', '',
      '| Owner | Correction source | Qualified source |', '|---|---|---|']
    for row in value['correction_source_joins']:
        repo = row['owner'].split('#')[0]
        lines.append(f"| [{row['owner']}]({row['owner_url']}) | [{row['correction_commit'][:10]}]({row['correction_url']}) | [{row['qualified_commit'][:10]}](https://github.com/{repo}/tree/{row['qualified_commit']}) |")
    lines += ['',
      'Qualified source requests an exact top-level PyPI version, an exact npm version with lifecycle scripts disabled, and an exact Cargo version with locked resolution, explicit registry and the supplied feature string. No installer, registry, re-exec or updater loop was invoked by this analysis. Source inclusion does not prove artifact authenticity, offline dependency availability, reversible installation or whole-issue acceptance.', '',
      '## Provenance and accounting', '',
      'The controlled analysis retains 36 exact qualified source blobs and 13 byte-identical accepted-harness views. The [machine-readable analysis](analysis.json) binds public source paths, digests, declared entrypoints, assertion-depth classes and limitations. Controlled original receipts and captures are not distributed here; digests do not make unavailable original content publicly inspectable.', '',
      'The partial source frontier now covers 104 of 147 definitions and 5,430 of 5,808 existing coordinate references; 43 definitions and 378 coordinates remain outside it. The universe includes six support definitions plus 141 edge definitions, and 218 support plus 5,590 edge coordinates. These are **source-reference accounting**, not newly executed tests, complete capabilities or new credit.', '',
      'The selected correction register has 20 owner records: 17 source inclusions and three development-only corrections. These are not 20 distinct product defects or complete supported-scope clearance. The earlier [dated owner-body audit](../2026-11-07-owner-audit/README.md) retains its original 17-record source snapshot.', '',
      'Historical completeness, all-six defect clearance, a corrected frozen reference and whole-contract conformance remain unestablished. Existing qualification authority is unchanged. No AWS access, workload, original-evidence rewrite, deployment or release follows from this report.', '',
      '## Verify', '',
      'From this repository with its pinned Python 3.13 dependencies:', '',
      '```sh', 'python3.13 -B scripts/release_recovery_reference.py', '```', '',
      'This verifies the reviewed data identity, closed schema, deterministic Markdown and integrity manifest. It does not rerun the original SDK tests or verify unavailable private artifacts.']
    return '\n'.join(lines) + '\n'

def check():
    value = load()
    validate(value)
    require((DATA / 'README.md').read_text() == render(value), 'generated narrative differs')
    manifest = json.loads((DATA / 'manifest.json').read_bytes())
    expected = {name: sha((DATA / name).read_bytes()) for name in ['analysis.json', 'analysis.schema.json', 'README.md']}
    require(manifest == {'schema': 'iicp.sdk-release-recovery-manifest.v1', 'files': expected, 'qualification_credit': 0, 'full_programme_complete': False}, 'manifest identity')
    return True

if __name__ == '__main__':
    check()
    print('PASS: dated source-analysis consistency; no SDK execution or qualification credit')
