"""Verify a dated source-context successor without running any recorded case."""
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'reports/postcert/2026-11-07-materialized-assertions'
DATA_PIN = '4b8fc5708cab748ade74dd5a84afaae106f887fcaac46ce57c8fdb2977650a73'
SCHEMA_PIN = 'cfba1a86d9a9dcd441f79f7e1aa6c4f7416c3b6777224a75cdeb0fdc37f8f153'

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
    require(len(value['cases']) == len({r['case_id'] for r in value['cases']}) == 43, '43 unique added cases')
    require(sum(r['existing_reference_count'] for r in value['cases']) == 378, '378 existing references')
    require(value['source_frontier']['partial_definitions'] == 147, 'declared frontier')
    require(sha(canonical(value)) == DATA_PIN, 'reviewed context identity')
    return True

def render(value):
    validate(value)
    lines = ['# Materialized assertion context and final source-reference frontier', '',
      'This successor clarifies the difference between a declared test fixture and its effective packaged execution. It adds **43 bounded source mappings** and **378 existing reference links**, completing the declared source-reference frontier at **147/147 definitions and 5,808/5,808 references**. It does not complete functional conformance, historical preservation or a corrected reference baseline.', '',
      '**No probe, SDK case, installer, database operation or qualification workload was run by this source review.** Process, disk and database actions below describe existing accepted-harness code, not actions authorized by this document.', '',
      '## Why execution context matters', '',
      'Earlier raw-source reports remain unchanged. Their source statements must not be read as exhaustive descriptions of staged consumers or installed-binary probes. This is an additive context successor, not changed qualification acceptance.', '']
    for row in value['context_clarifications']:
        lines += [f"### {row['case_id']}", '', f"**Raw layer:** {row['raw_layer']}", '', f"**Packaged layer:** {row['materialized_layer']}", '', row['effect'], '']
    lines += ['## Crypto scope remains bounded', '',
      'Python and TypeScript staged crypto helpers call installed SDK validators and production replay-cache classes. The four selected Rust crypto-fixture methods still use test-local policy and real Ed25519 verification: one exact frozen crate was digest-verified and its member matched the qualified source. A separate Rust runtime-verifier test file also exists in that crate; this source review does not establish its full historical execution. A generic assertion-adapter label is not proof that all component paths invoke the same validator.', '',
      'The fixtures remain pre-normative, version 0.2.0-draft. Calling a runtime validator does not make the profile normative or demonstrate persistent replay handling, live credential rotation, federation or independent interoperability. Separate Rust build-receipt gates cover build/install/version, not an unreported complete verifier test run.', '',
      '## Effective predicates for the 43 added definitions', '',
      '| Declaration and accepted adapter | Effective role | Source-derived packaged predicate | Limit |',
      '|---|---|---|---|']
    for row in value['cases']:
        locator = f"[{row['case_id']}]({row['raw_source_url']}); [adapter]({row['accepted_pipeline_url']})"
        lines.append(f"| {locator} | {cell(row['effective_source_role'])} | {cell(row['packaged_predicate'])} | {cell(row['limits'])} |")
    lines += ['', '## Provenance, applicability and remaining work', '',
      'The controlled review retains 43 qualified source captures, 32 raw qualified/accepted-harness input equalities, 12 accepted execution-pipeline files and the separately pinned minimum-runtime helper. Reconstructed staged source is text/literal analysis, not a workload. Applicability comes from the original accepted assignments: Directory targets are Linux-only; Management retains its own four-target/runtime scope. A source runner accepting another target name does not create qualification credit.', '',
      'The 147-definition universe comprises six support definitions and 141 edge definitions. Its 5,808 references comprise 218 support cells and 5,590 edge executions. All 104 predecessor review rows remain; no declared case IDs are outside the source-reference index. This is not a complete universe of historical attempts, defects or normative capability obligations.', '',
      'Original accepted PASS results, receipts, candidate and five project-operated certificates are unchanged. Historical completeness remains false. Known-defect disposition, complete semantic reference, private disclosure clearance, applicable successor qualification and final programme audit remain separate. There is no new product-defect verdict, qualification credit, external certification, release or deployment authority.', '',
      'Repository links and digests identify source. Controlled original captures are not distributed, and unavailable or restricted content is not made publicly retrievable by a link or hash.', '',
      '## Verify the derivative', '',
      'From the reviewed repository with its pinned Python 3.13 dependencies:', '',
      '```sh', 'python3.13 -B scripts/assertion_context_reference.py', '```', '',
      'This checks reviewed data/schema identity, generated Markdown and manifest only. Do not execute the recorded declarations or probes under this documentation permission.']
    return '\n'.join(lines) + '\n'

def check():
    value = load()
    validate(value)
    require((DATA / 'README.md').read_text() == render(value), 'generated text differs')
    expected = {n: sha((DATA / n).read_bytes()) for n in ['analysis.json', 'analysis.schema.json', 'README.md']}
    manifest = json.loads((DATA / 'manifest.json').read_bytes())
    require(manifest == {'schema': 'iicp.assertion-context-manifest.v1', 'files': expected, 'qualification_credit': 0, 'full_programme_complete': False}, 'manifest identity')
    return True

if __name__ == '__main__':
    check()
    print('PASS: source-context derivative only; no recorded case executed')
