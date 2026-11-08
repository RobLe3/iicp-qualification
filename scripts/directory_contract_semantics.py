"""Validate one minimized source-analysis derivative, not qualification authority."""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-directory-contract-semantics'
DATA_PIN='f4fea01d2853b9b060f9a06e0a4615cf6d9baa769cc4a7c452b93740246c77ff'
SCHEMA_PIN='eabeaab1a181f0a5bc449009e63d3fee1a6c454db0d16b654bd3669b19300e78'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(ok,why):
 if not ok:raise ValueError(why)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 r=v['reference_accounting'];require((r['case_definitions'],r['support_definitions'],r['edge_definitions'])==(47,2,45),'definition scope');require((r['existing_reference_count'],r['existing_support_references'],r['existing_edge_references'])==(432,18,414),'reference scope');require(r['components']=={'directory-php':132,'directory-rust':300} and r['original_receipt_reference_count']==32,'component scope');require(r['targets']==['linux-aarch64','linux-x86_64'],'applicability')
 s=v['shared_contracts'];require((s['byte_equal_fixture_pairs'],s['behavior_vector_definitions'],s['http_route_metadata_definitions'])==(3,17,43),'different evidence units');require(s['contract_version']=='v1.10.80','historical contract version')
 require(v['shared_validation']['byte_equal_source_functions']==7 and v['shared_validation']['existing_cross_flavor_coordinates']==18,'validator source scope')
 require(len(v['rust_adapter_context'])==6 and len({r['case_id'] for r in v['rust_adapter_context']})==6,'adapter scope')
 require(len(v['owner_clauses'])==6 and len({c['owner_clause_id'] for c in v['owner_clauses']})==6 and sum(len(c['proposed_atom_ids']) for c in v['owner_clauses'])==21 and all(c['whole_clause_verified'] is False for c in v['owner_clauses']),'owner scope/credit')
 for k,x in v['boundaries'].items():
  if k in {'new_qualification_credit','new_qualifying_tests','whole_owner_clause_changes','product_source_repairs'}:require(type(x)is int and x==0,'new authority or credit')
  else:require(x is False,'maturity promotion')
 require(v['validation']=={'private_overlay_controls':31,'private_owner_atom_controls':16,'source_and_metadata_only':True},'validation role')
 require(sha(canonical(v))==DATA_PIN,'reviewed derivative identity');return True
def render(v):
 validate(v);r=v['reference_accounting'];s=v['shared_contracts'];lines=['# Directory contracts: interpret the executed adapter, not the scenario name','',
 'This source-bound supplement reconciles six unchanged Directory owner conjunctions. It adds no workload, product repair, owner checkbox completion or qualification credit.','',
 '## Existing reference coverage','',
 '| Component | Existing support references | Existing edge references |','|---|---:|---:|','| PHP Directory | 6 | 126 |','| Rust Directory | 12 | 288 |','',
 'The 432 references cover 47 existing definitions and 32 original receipt references in the two declared Linux lanes. They are not new tests. Rust’s twelve cells combine two toolchains, two architectures and three modes—not a second Directory flavor or an invented database axis. Original receipt/proof envelopes were not reopened for this analysis.','',
 '## Shared definitions and output guards','',
 'Three exact fixture pairs match across the accepted PHP/Rust harness sources. The historical contract revision is **v1.10.80**, distinct from current component versions.','',
 '- **17 behavior-vector definitions** cover selected registration, eligibility, ranking, pricing and endpoint-refusal checks.','- **43 HTTP metadata records** describe method/path/auth/status scope. They are not 43 newly executed endpoint tests.','- **Seven byte-identical output-validation functions** guard the selected cross-flavor case. The exact driver revalidates the binding and validates owned output before writing its proof.','',
 v['shared_validation']['inference']+' Eighteen existing cross-flavor coordinates use the bound case; do not relabel them as new vector executions or whole operational parity.','',
 '## Six effective Rust adapter contexts','',
 '| Case | Accepted adapter source predicate | Limitation |','|---|---|---|']
 lines += [f"| {cell(x['case_id'])} | {cell(x['effective_source_predicate'])} | {cell(x['limitation'])} |" for x in v['rust_adapter_context']]
 lines += ['',
 'Raw unit predicates remain preserved. For example, a token-issuance helper test is not the complete installed HTTP rotation case. The latter checks authorized access, old-token refusal and replacement success. The installed signature case checks heartbeat HMAC state, not the raw replica-event Ed25519 predicate.','',
 '## Owner contracts and release boundaries','',
 'Six whole clauses remain unverified. Their twenty-one proposed analytical atoms are source/evidence dispositions, not twenty-one completed requirements.','']+['- '+t for t in v['policy_findings']]
 lines += ['','## Validation and limitations','',
 'Private focused controls:31 overlay and16 owner-atom controls passed. These validate metadata/source relationships; they are not qualification tests or an independent implementation experiment. Required publication review and exact-head CI are separate gates.','']+['- '+t for t in v['limitations']]
 lines += ['','See [pinned source references](SOURCES.md), [the preceding owner-contract audit](../2026-11-08-owner-contract-evidence/README.md) and [canonical qualification reporting](../../STATUS.md). Public checks validate this fixed derivative, schema, narrative and manifest; they do not reconstruct private original executions.','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated narrative differs');require(json.loads((DATA/'manifest.json').read_text())=={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'new_qualification_credit':0,'private_originals_distributed':False},'manifest differs');return True
if __name__=='__main__':check();print('PASS: fixed Directory source-analysis derivative; no new qualification authority.')
