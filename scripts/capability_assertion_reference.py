"""Check/render analytical assertion mappings and replay minimized fixture values only."""
from pathlib import Path
from decimal import Decimal
import argparse
import hashlib
import json
import math
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-07-capability-assertions'
JSON_PIN='52fa37907aa9006d54c1c7c44a1b9e54bf4274c419a196831d8dadba34bafae0'
SCHEMA_PIN='713d6e613cc00a37534800240ab78c6a1a1b2f36639ffc6fae65ef200485306c'
EXPECTED_CAPABILITIES=[{'input_modalities': ['text'],
  'intent': 'urn:iicp:intent:llm:chat:v1',
  'limits': {'context_tokens': {'unit': 'tokens', 'value': 8192}},
  'models': ['fixture-small'],
  'output_modalities': ['text'],
  'phase': 1,
  'variant_id': 'text-basic',
  'version': '1.0.0'},
 {'claim_provenance': {'source': 'runtime_introspection'},
  'extensions': {'org.example.optional-batching': {'required': False, 'value': {'enabled': True}}},
  'features': ['structured_output', 'tool_calling'],
  'input_modalities': ['text', 'image'],
  'intent': 'urn:iicp:intent:llm:chat:v1',
  'models': ['fixture-vision'],
  'output_modalities': ['text'],
  'supported_profiles': ['urn:iicp:profile:service-lifecycle:v1'],
  'variant_id': 'vision-tools'}]
SET_KEYS=['execution_capabilities', 'features', 'input_modalities', 'models', 'output_modalities', 'supported_profiles']
def numeric_equal(wanted, found):
    if type(wanted) not in (int, float) or type(found) not in (int, float):
        return False
    if (type(wanted) is float and not math.isfinite(wanted)) or (type(found) is float and not math.isfinite(found)):
        return False
    return Decimal(str(wanted)) == Decimal(str(found))

def semantic_subset(wanted, found, key=''):
    if type(wanted) in (int,float):
        return numeric_equal(wanted, found)
    if isinstance(wanted, dict):
        return isinstance(found, dict) and all(k in found and semantic_subset(v,found[k],k)
                                              for k,v in wanted.items())
    if isinstance(wanted, list):
        if not isinstance(found,list) or len(wanted)!=len(found):
            return False
        if key in SET_KEYS:
            return all(isinstance(x,str) for x in found) and len(set(found))==len(found) and set(found)==set(wanted)
        return all(semantic_subset(x,y) for x,y in zip(wanted,found))
    return type(found) is type(wanted) and found == wanted

def capabilities_ok(found):
    if not isinstance(found,list) or len(found)!=2:
        return False
    for wanted in EXPECTED_CAPABILITIES:
        matches=[c for c in found if isinstance(c,dict) and c.get('intent')==wanted['intent']
                 and c.get('variant_id')==wanted['variant_id']]
        if len(matches)!=1 or not semantic_subset(wanted,matches[0]):
            return False
    return True

def status_is(value, expected):
    return type(value) is int and value == expected

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def replay_vectors(v):
    if json.dumps(v['expected_capabilities'],sort_keys=True)!=json.dumps(EXPECTED_CAPABILITIES,sort_keys=True):
        raise ValueError('SOURCE_EXPECTATION_REINTERPRETED')
    if not capabilities_ok(v['observed_detail_capabilities']) or not capabilities_ok(v['observed_discovery_capabilities']):
        raise ValueError('SELECTED_CAPABILITY_PREDICATE')
    names=['empty','duplicate','negative-limit','malformed-profile','duplicate-profile','oversized-profiles']
    rows=v['observed_refusals']
    if len(rows)!=6 or [r['case'] for r in rows]!=names:
        raise ValueError('EXACT_REFUSAL_SET')
    for row in rows:
        if not status_is(row['status'],422) or row['error_code']!='validation_error' or row['row_counts']!=[1,2] or any(type(n) is not int for n in row['row_counts']):
            raise ValueError('REFUSAL_OR_CHECKED_STATE')
    empty=v['observed_php_empty']
    if not status_is(empty['status'],422) or empty['error_code']!='validation_error' or type(empty['node_count_before']) is not int or type(empty['node_count_after']) is not int or empty['node_count_before']!=empty['node_count_after']:
        raise ValueError('PHP_EMPTY_REFUSAL')
    return True

def load():
    return json.loads((DATA/'assertions.json').read_bytes())

def validate(value):
    privacy(value)
    raw=(DATA/'assertions.schema.json').read_bytes()
    if sha(raw)!=SCHEMA_PIN:
        raise ValueError('REVIEWED_SCHEMA_IDENTITY')
    Draft202012Validator(json.loads(raw)).validate(value)
    canonical=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    if sha(canonical)!=JSON_PIN:
        raise ValueError('REVIEWED_ASSERTION_SNAPSHOT_IDENTITY')
    rows=value['rows']
    pairs=[(r['assertion_id'],r['profile_id']) for r in rows]
    if len(rows)!=36 or len(set(pairs))!=36 or len({p[0] for p in pairs})!=12:
        raise ValueError('ASSERTION_MATRIX')
    observed={s:sum(r['status']==s for r in rows) for s in value['counts']}
    if observed!=value['counts'] or sum(observed.values())!=36:
        raise ValueError('STATUS_ACCOUNTING')
    replay_vectors(value['vectors'])
    return True

def render(value):
    validate(value)
    profiles=value['profiles']
    labels={'VERIFIED_BOUNDED_OBSERVATION':'bounded observation',
            'PARTIAL_OBSERVATION':'partial fields only',
            'NOT_EXERCISED_IN_SELECTED_WITNESSES':'not exercised here'}
    lines=['# Capability requirements and observed assertion depth','',
        'This additive reference connects four existing capability source-contract IDs to twelve '
        'selected analytical questions across three local backend profiles. It defines **no new '
        'qualification gates**. The 36 rows are not campaign assignments, a comprehensive specification '
        'or a requirement to execute 19 additional tests. Existing owners must disposition applicability '
        'to the supported scope before any new workload is planned.','',
        '## What the evidence supports','',
        '- 14 profile/assertion rows have bounded observations.',
        '- 3 rows have only part of the stated field checks.',
        '- 19 rows have no selected runtime witness.',
        '- Whole parent-contract conformance remains **unverified for all four**.','',
        'These counts are an evidence map, not a defect count, truth probability or qualification '
        'percentage. Original qualification, receipts, certificates and earlier dated source-only '
        'NOT_EXECUTED records remain unchanged. Later local observations do not establish that '
        'these same assertions executed in the original campaign.','',
        '| Selected assertion question | PHP / SQLite | Rust / memory | Rust / MySQL |',
        '|---|---|---|---|']
    for aid in dict.fromkeys(r['assertion_id'] for r in value['rows']):
        matching=[r for r in value['rows'] if r['assertion_id']==aid]
        lines.append('| `'+aid+'` | '+' | '.join(labels[next(r['status'] for r in matching if r['profile_id']==p)] for p in profiles)+' |')
    lines+=['','## Important distinctions','',
        'The selected PHP duplicate method changes a field while retaining intent/variant_id, '
        'so its passing refusal isolates the nonidentical same-pair case. The selected Rust duplicate '
        'inputs are exact clones with explicit IDs: one refusal can satisfy either duplicate rule, '
        'so it does not isolate the nonidentical same-pair branch. Neither implementation is shown '
        'defective by that evidence gap. No selected method exercises ID-less exact duplicates or '
        'distinct ID-less same-intent variants.','',
        'PHP checks an optional extension required flag, but not its payload value. The Rust '
        'in-memory method checks the payload value, but not the flag. The MySQL method checks '
        'both. PHP checks a typed limit unit but not the numeric value; presence in an input '
        'object is not a successful output assertion.','',
        'The MySQL capture replay verifies both declared variants, including selected limits and '
        'extension fields. Variant order and declared string-set order are not frozen; 8192 and '
        '8192.0 compare numerically. This finite fixture does not establish arbitrary numeric '
        'precision, crash durability, real HTTP/TLS, production security or four-platform equivalence.','',
        '## Source and authority boundary','',
        'The pinned Protocol revision is `2d240649cf8d11a235132658a599e22ebcba6620`. '
        'Its node-capability-format document describes itself as draft and normative for '
        'REGISTER/NODELIST. The effective-service contract describes an accepted additive '
        'pre-normative Profile whose adoption remains parity-gated. This bridge does not '
        'ratify the Profile or create a capability-requirements endpoint.','']
    for row in value['source_metadata']:
        lines.append('- ['+row['path']+']('+row['url']+'), SHA-256 `'+row['sha256']+'`.')
    lines+=['','Each row identifies exact source lines, evidence IDs, proof basis and limitations. '
        'An executed pinned test assertion, a replayed capture and merely present source code are '
        'different evidence classes. The [preceding method/environment package]'
        '(../2026-11-07-directory-kernels/README.md) preserves the separate SQLite, in-memory and '
        'tmpfs-MySQL contexts and failed attempts.','',
        '## Minimized executable vectors','',
        'The JSON exports only allowlisted synthetic-fixture capability values, refusal classes '
        'and checked row counts. Node identifiers, endpoints, error messages, host paths and '
        'credentials are excluded. Private source digests bind the retained observations but '
        'do not make their original bytes publicly accessible or independently authenticatable. '
        'The pure replay functions compare these selected values; they do not execute a Directory, '
        'database, qualification controller or network request.','',
        '## Offline verification','', '```sh',
        'python3.13 -B scripts/capability_assertion_reference.py check',
        'python3.13 -B -m unittest discover -s tests -p "test_capability_assertion_reference.py" -v',
        '```','',
        'The checker verifies the reviewed snapshot/schema, row accounting, minimized vectors, '
        'deterministic Markdown and manifest. `render` only regenerates this package README and '
        'manifest; it does not publish. Obtain the expected manifest digest from the reviewed PR.','',
        '## Limits','']+['- '+x for x in value['limits']]
    lines+=['','[Root #1678](https://github.com/RobLe3/iicp.network/issues/1678) owns this reference work. '
        'Protocol Profile adoption remains with [IICP #55](https://github.com/RobLe3/IICP/issues/55); '
        'historical preservation remains with [root #1676](https://github.com/RobLe3/iicp.network/issues/1676). '
        'No product defect, qualification credit, external interoperability, successor freeze or release '
        'authority is established by this analytical supplement.','']
    return '\n'.join(lines)

def manifest():
    return {'schema':'iicp.capability-assertion-public-manifest.v1','qualification_credit':0,
            'files':{n:sha((DATA/n).read_bytes()) for n in ('assertions.json','assertions.schema.json','README.md')}}

def check_package():
    value=load();validate(value)
    if (DATA/'README.md').read_text()!=render(value):raise ValueError('STALE_GENERATED_NARRATIVE')
    if json.loads((DATA/'manifest.json').read_bytes())!=manifest():raise ValueError('MANIFEST_MISMATCH')
    return value

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=('check','render'));args=ap.parse_args()
    if args.command=='render':
        text=render(load());(DATA/'README.md').write_text(text);(DATA/'manifest.json').write_text(json.dumps(manifest(),indent=2,sort_keys=True)+'\n')
    else:check_package()
    print('PASS: analytical snapshot and selected semantic values only; qualificationcredit0')

if __name__=='__main__':main()
