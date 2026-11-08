"""Verify a fixed finite-catalog analytical derivative; never admit evidence."""
from pathlib import Path
from collections import Counter
import hashlib,json
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-finite-catalog-semantics'
DATA_PIN='183fe1013d4d7dec69bc2e53c67ff0b23316b90c917a2b8d1a9fa8c869b3329a'
SCHEMA_PIN='13d456de3ee33a69e9fd34debae151a64a6f9de4157ab735af6545571ad0b20f'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def require(ok,reason):
 if not ok:raise ValueError(reason)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 rows=v['scenario_analysis'];cases=[c for r in rows for c in r['cases']]
 require(len(rows)==len({r['scenario_id'] for r in rows})==36,'scenario scope')
 require(len(cases)==len({c['case_id'] for c in cases})==141,'case scope')
 require(sum(c['existing_accepted_reference_count'] for c in cases)==5590,'reference scope')
 require(Counter(c['source_fit'] for c in cases)==v['counts']['source_fit_counts'],'fit accounting')
 require(v['counts']['source_fit_counts']=={'DIRECT_FINITE_PROPERTY':50,'PARTIAL_EXPECTATION_WITNESS':74,'CROSS_CASE_COMPLEMENT_REQUIRED':3,'PREPARATION_CONTRACT_JOIN_REQUIRED':11,'APPLICABILITY_CLARIFICATION_REQUIRED':3},'fit scope')
 require(v['counts']['cross_case_coordinate_pairs']==192 and v['counts']['cross_case_environment_matched_pairs']==125 and v['counts']['cross_case_environment_different_pairs']==67,'context comparison scope')
 for k,x in v['boundaries'].items():
  if k in {'new_qualification_credit','new_qualifying_tests','runtime_witness_joins_verified'}:require(type(x)is int and x==0,'credit/runtime inflation')
  else:require(x is False,'maturity or disclosure inflation')
 require(sha(canonical(v))==DATA_PIN,'reviewed derivative identity');return True
def render(v):
 validate(v)
 lines=['# Finite catalog: source properties, context and remaining evidence','','This reviewed source interpretation adds no product correction, workload, qualification credit or frozen reference. Exact controlled catalog wording remains private.','',
 '## Scope and different units','','- **36 scenario interpretations**, covering **141 existing edge definitions** and **5,590 accepted reference coordinates**.','- **50 direct finite source properties**, **74 partial witnesses**, **3 cross-case complements**, **11 preparation-contract joins** and **3 applicability clarifications**. These are not completed requirement counts.','- **192 cross-case coordinate pairs**:125 have equal retained environment metadata;67 differ. **Zero newly verified runtime witness joins**.','- **52 private synthetic controls passed**, followed by bounded non-authoring source review. Public validation is a separate fixed-derivative check, not a qualification rerun.','',
 '## How to read this','','The original accepted campaign remains authoritative and unchanged. A source-witness gap is not a demonstrated product failure. A direct finite property is not whole catalog conformance. Do not promote raw test names, source existence, modeled error handling or current preparer code into historical runtime evidence.','',
 'The original PHP rate feature case asserts a Retry-After response header; the later offline clamp expression is a separate slice. The confidentiality downgrade and partial-response expectations permit alternative branches: disclose unexamined alternatives without requiring every alternative to recognize a selected finite property.','',
 '## Source-grounded scenario interpretations','']
 for row in v['scenario_analysis']:
  lines+=['### '+row['scenario_id'],'',row['interpretation'],'']
  for c in row['cases']:
   lines+=['- **'+c['component']+' — '+c['source_fit']+'**: '+c['supported_source_property'],
           '  Limit/gap: '+c['unresolved_or_excluded_scope'], '  Next evidence action: '+c['next_evidence_action']]
  lines+=['']
 lines+=['## Limits','']+['- '+x for x in v['limitations']]
 lines+=['','See [source/provenance notes](SOURCES.md), the [earlier functional reader](../2026-11-07-functional-reference/README.md), [Directory adapter supplement](../2026-11-08-directory-contract-semantics/README.md) and [canonical status](../../STATUS.md).','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'narrative differs')
 expected={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'new_qualification_credit':0,'private_originals_distributed':False}
 require(json.loads((DATA/'manifest.json').read_text())==expected,'manifest differs');return True

# Additive fixed derivative: caller roles and declared release dependency horizon.
CALLER_DATA=ROOT/'reports/postcert/2026-11-08-caller-source-and-release-horizon'
CALLER_DATA_PIN='6e74c9640288d82a3fcb51ca58343083b87c70b85beea3e1e5accb57bef44a53'
CALLER_SCHEMA_PIN='cfed6ad0f302c26042b02ec7b94445a6d94dc76ce263043431397cb4f1d092d3'
def load_callers():return json.loads((CALLER_DATA/'analysis.json').read_bytes())
def validate_callers(v):
 privacy(v);raw=(CALLER_DATA/'analysis.schema.json').read_bytes();require(sha(raw)==CALLER_SCHEMA_PIN,'caller schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 rows=v['caller_cases'];require(len(rows)==len({r['case_id'] for r in rows})==5,'caller scope');require(sum(r['existing_reference_count'] for r in rows)==206,'caller reference scope')
 require(v['counts']=={'caller_cases':5,'existing_references':206,'bounded_source_questions_resolved':4,'owner_scope_questions_retained':1,'working_reference_candidates':5,'new_reference_executions':0},'caller counts')
 release=v['release_horizon'];require((release['reviewed_owner_issue_count'],release['unchanged_owner_issue_count'],release['unchanged_policy_source_files'],release['previously_declared_prerequisite_owners_refreshed'])==(10,10,6,4),'release refresh scope')
 require(release['new_readiness_gate_passes']==0 and release['legal_applicability_assessed'] is False,'release maturity inflation')
 require(len(release['prerequisite_owner_states'])==4 and all(x['state']=='OPEN' for x in release['prerequisite_owner_states']),'prerequisite state')
 for k,x in v['boundaries'].items():
  if k=='new_qualification_credit':require(type(x)is int and x==0,'caller credit')
  else:require(x is False,'caller authority/disclosure inflation')
 require(sha(canonical(v))==CALLER_DATA_PIN,'reviewed caller identity');return True
def render_callers(v):
 validate_callers(v)
 lines=['# Caller roles and release dependencies: interpret the scoped evidence','','This additive source review preserves five original cases and206 existing reference coordinates. It neither changes qualification credit nor establishes a corrected frozen baseline.','',
 '## What the source settles','','Four bounded source questions are resolved and one owner-scope question remains explicit. There are five working reference designs, not five new product executions.','',
 'Optional saved-identity lookup can correctly return absence. Required CLI callers can still refuse with initialization guidance. PHP node-health recovery is not an injected Directory crash. Management logical generations and process/IPC ownership are different predicates. A restricted-Directory missing-decision refusal must retain its actual HTTP200 stimulus rather than be called a transport outage.','']
 for r in v['caller_cases']:
  lines+=['### '+r['case_id'],'',r['finding'],'','Supported finite source property: '+r['supported_property'],'','Not established: '+r['not_established'],'','Next: '+r['next_action'],'']
 lines+=['## Release dependency horizon','','Ten existing owner issues retain unchanged state/body/comment content; six policy/source files retain their reviewed hashes. Four previously declared dependency owners were also read without issue mutation:','', '| Owner | State |','|---|---|']
 lines += ['| '+x['repository']+'#'+str(x['issue'])+' | '+x['state']+' |' for x in v['release_horizon']['prerequisite_owner_states']]
 lines += ['', 'The canonical qualified-review slot remains a blank template with review_present=false. This is source status, not a legal conclusion or a claim about every possible external review. No new readiness pass, participant intake or release authority follows.','',
 '## Validation and limits','','Retained controls:34 source-role and6 original schema checks. Six focused successor checks validate the corrected finite fixture requirements. These are metadata/source-design controls, not product or qualification executions. Required public projection review and exact-head CI remain separate delivery gates.','']+['- '+x for x in v['limitations']]
 lines+=['','See [pinned sources](SOURCES.md), [the complete finite-catalog supplement](../2026-11-08-finite-catalog-semantics/README.md) and [canonical status](../../STATUS.md).',''];return '\n'.join(lines)
def check_callers():
 v=load_callers();text=render_callers(v);require((CALLER_DATA/'README.md').read_text()==text,'caller narrative differs');require(json.loads((CALLER_DATA/'manifest.json').read_text())=={'analysis_sha256':CALLER_DATA_PIN,'schema_sha256':CALLER_SCHEMA_PIN,'readme_sha256':sha(text.encode()),'new_qualification_credit':0,'private_originals_distributed':False},'caller manifest differs');return True

# Additive fixed derivative: executed finite local witnesses, never campaign credit.
WITNESS_DATA=ROOT/'reports/postcert/2026-11-08-executable-reference-witnesses'
WITNESS_DATA_PIN='e8a95439046d7f9d82fbe635ee0464bfa9b8c35bcd3afb2088c65d017862ab68'
WITNESS_SCHEMA_PIN='39994773aba47700952413406c2c769fa7e77f44881d5c690d3f216fbbe4be34'
def load_witnesses():return json.loads((WITNESS_DATA/'analysis.json').read_bytes())
def validate_witnesses(v):
 privacy(v);raw=(WITNESS_DATA/'analysis.schema.json').read_bytes();require(sha(raw)==WITNESS_SCHEMA_PIN,'witness schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 rows=v['groups'];require(len(rows)==len({r['original_case_id'] for r in rows})==5,'witness group scope')
 require(sum(r['local_unit_test_methods_passed'] for r in rows)==14 and sum(r['existing_reference_count'] for r in rows)==206,'witness unit/reference accounting')
 require(v['counts']=={'finite_witness_groups':5,'local_unit_test_methods_passed':14,'existing_reference_coordinates':206,'successful_profile_controls':8,'current_admission_controls':10,'retained_stopped_local_fixtures':2,'product_test_retries':0,'new_qualification_credit':0},'witness count scope')
 require(type(v['counts']['new_qualification_credit'])is int and v['counts']['new_qualification_credit']==0,'witness credit type')
 for r in rows:require(r['status']=='LOCAL_UNIT_PASS' and type(r['qualification_credit'])is int and r['qualification_credit']==0 and r['product_source_changed']is False,'witness admission/source inflation')
 require(all(x is False for x in v['boundaries'].values()),'witness authority/disclosure inflation')
 require(sha(canonical(v))==WITNESS_DATA_PIN,'reviewed witness identity');return True
def render_witnesses(v):
 validate_witnesses(v)
 lines=['# Finite reference witnesses: five local groups executed','','Five bounded local witness groups passed 14 unit test methods against unchanged qualified source. These are new local observations, not new qualification credit or a frozen corrected reference.','',
 '## Counts and scope','','| Component | Local test methods | Scope |','|---|---:|---|']
 for r in v['groups']:lines+=['| '+r['component']+' | '+str(r['local_unit_test_methods_passed'])+' | '+r['executed_scope']+' |']
 lines+=['','The five original case links retain 206 existing reference coordinates; none is newly credited. Eight actual profile controls and ten synthetic admission controls supported the local execution. Two newly created local fixtures are retained stopped, not deleted. Original refusals remain in the controlled archive.','',
 '## Per-group boundaries','']
 for r in v['groups']:
  lines+=['### '+r['working_reference_id'],'','Target/runtime: '+r['target']+' / '+r['runtime']+'. Original case link: `'+r['original_case_id']+'`.','']+['- '+x for x in r['limitations']]+['']
 lines+=['## What public validation can establish','','The fixed-data validator checks reviewed report identity, closed fields, arithmetic, privacy and Markdown/JSON consistency. It does not execute the SDKs, reconstruct original runs or verify inaccessible private captures. The non-authoring review accepted retained execution evidence within the stated scope; it is not external certification.','',
 '## Remaining limits','']+['- '+x for x in v['limitations']]
 lines+=['','See [source/provenance notes](SOURCES.md), [the preceding source/design interpretation](../2026-11-08-caller-source-and-release-horizon/README.md) and [canonical status](../../STATUS.md).',''];return '\n'.join(lines)
def check_witnesses():
 v=load_witnesses();text=render_witnesses(v);require((WITNESS_DATA/'README.md').read_text()==text,'witness narrative differs');require(json.loads((WITNESS_DATA/'manifest.json').read_text())=={'analysis_sha256':WITNESS_DATA_PIN,'schema_sha256':WITNESS_SCHEMA_PIN,'readme_sha256':sha(text.encode()),'new_qualification_credit':0,'private_originals_distributed':False},'witness manifest differs');return True

if __name__=='__main__':
 check();check_callers();check_witnesses();print('PASS: fixed reference derivatives; no qualification authority.')
