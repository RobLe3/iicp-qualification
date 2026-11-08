"""Fixed, reviewed reporting derivative; never a product or credit validator."""
from pathlib import Path
import hashlib,json
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-reference-continuity'
DATA_PIN='66d85880141020893900465fdbfe2054d1f76d04cc8c94bd1edc64c356da61d7';SCHEMA_PIN='22e217f738e8a7d56834af033339fd18d26f928198f3b01b5caa3f077b46f42c'
def canonical(value):return (json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(value,why):
 if not value:raise ValueError(why)
def schema():
 raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'reviewed schema changed');return json.loads(raw)
def validate(value):
 Draft202012Validator(schema()).validate(value)
 raw=canonical(value)
 require(sha(raw)==DATA_PIN,'reviewed derivative changed')
 require(not any(p in raw.decode() for p in ['/Users/','arn:aws:','AKIA','ASIA','authorization.json','confirmation_code']),'private material in derivative')
 return True
def load():
 raw=(DATA/'analysis.json').read_bytes();require(len(raw)<65536,'derivative byte bound');value=json.loads(raw);validate(value);return value
def render(value):
 validate(value);c=value['counts'];w=value['credential_witnesses'];lines=['# Reference continuity and bounded credential witnesses','',
 'This supplement connects existing local observations to the working functional reference, adds three focused opt-in ticket-v2 verifier methods, and checks metadata inside three retained SDK archives. It does not add qualification credit or freeze a corrected successor.','',
 '## Separate measures','',
 '| Measure | Count |','|---|---:|',
 '| Previously executed witness groups linked | '+str(c['previous_local_witness_groups_linked'])+' |',
 '| Previous product unit methods, not repeated | '+str(c['previous_product_unit_methods'])+' |',
 '| Reference-adapter controls passed | '+str(c['reference_adapter_controls_passed'])+' |',
 '| New opt-in v2 product unit methods passed | '+str(c['new_opt_in_v2_product_unit_methods'])+' |',
 '| New attempt/output guard controls passed | '+str(c['new_attempt_guard_controls_passed'])+' |',
 '| SDK primary archive metadata joins | '+str(c['sdk_primary_archive_metadata_joins'])+' |',
 '| Metadata controls passed | '+str(c['metadata_controls_passed'])+' |',
 '| New qualification credit / formal criterion updates | 0 / 0 |','',
 'The reference adapter keeps original case, reviewed predicate and limitations context together. Original designs and graph records remain unchanged. Its controls do not count as additional product methods.','',
 '## Opt-in, pre-normative ticket-v2 verifier','',
 'Three new Python methods passed in one local macOS ARM64 invocation using pinned Python 3.14.10 and public signed fixed-time fixtures. Non-authoring review accepted complete capture and bounded semantics. The default v1 authentication path was not tested.','']
 lines+=['- '+s for s in w['observations']]+['','### Credential limits','']+['- '+s for s in w['limitations']]
 lines+=['','## Retained package metadata','', '| Component | Frozen version | Archive metadata version |','|---|---|---|']
 for r in value['package_metadata']['rows']:lines+=['| '+r['component']+' | '+r['frozen_source_version']+' | '+r['observed_archive_metadata']['version']+' |']
 lines+=['','All three package/source version declarations agree. The Rust crate also embeds the qualified source commit. Archive members were read in memory, not extracted to disk or executed.','']+['- '+s for s in value['package_metadata']['limitations']]
 lines+=['','## Review and public verification','',
 'Independent non-authoring reviews cover the retained private execution and analytical evidence within the stated scopes. They are not independent external certification. Public checks validate this fixed reviewed data, closed schema, arithmetic and Markdown consistency; they cannot inspect undistributed captures merely from their hashes.','',
 '## Programme limits','']+['- '+s for s in value['limitations']]
 lines+=['','See [source and provenance notes](SOURCES.md), [the preceding five-group execution supplement](../2026-11-08-executable-reference-witnesses/README.md) and [canonical reporting](../../STATUS.md).','']
 return '\n'.join(lines)
def check():
 value=load();text=render(value);require((DATA/'README.md').read_text()==text,'generated narrative differs')
 expected={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'private_originals_distributed':False}
 require(canonical(json.loads((DATA/'manifest.json').read_bytes()))==canonical(expected),'manifest differs');return True
if __name__=='__main__':check();print('PASS: fixed reference continuity derivative; no qualification authority.')
