"""Public derivative controls; these do not execute the private observations."""
from pathlib import Path
import copy,json,hashlib,re,unittest
from jsonschema import Draft202012Validator,ValidationError
R=Path(__file__).resolve().parents[1];D=R/'reports/postcert/2026-11-07-enclosing-capability'
PRODUCT={'client-python':'9c5b3d894ee89ef9fcde52ea0ad99d388ed62183','client-typescript':'97c768d8b9e90756773103e432c273a7d98ba08e','client-rust':'0b8b529262977b6482dd7900d473e7d152ba9293','directory-php':'2dfd228b49c587150a44f448cea1351a9f039d32','directory-rust':'b95a362ad8f974334994ca73cd20210388a2362f'}
HARNESS={'client-python':'0cf46aae4beba4304de55ef99cc3a22f72784f30','client-typescript':'23a57f7c17cabd9867514d85f248004cdb40617e','client-rust':'4020dadd150d7975be468f04a588dfa5346899a5','directory-php':'134c0a0f297a120c2e97d5dc891dcac90c293a57','directory-rust':'6a886a633d50e106ef1e2d5ff21b9e9002e070da'}
COUNTS={'client-python':96,'client-typescript':48,'client-rust':48,'directory-php':6,'directory-rust':12}
ASSERTIONS={'client-python':'test_profile_fixture_native_policy_scenarios_use_real_routing_gate','client-typescript':'profile fixture native policy scenarios use the routing gate','client-rust':'profile_fixture_native_policy_scenarios_use_routing_gate','directory-php':'test_shared_registration_cases_preserve_recovery_and_rollback','directory-rust':'rust_policy_primitives_execute_the_php_behavior_fixture'}
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def load():return json.loads((D/'findings.json').read_bytes())
def windows(x):
 rows=x['source_windows'];ids=[s['id']for s in rows]
 if len(set(ids))!=36:raise ValueError('WINDOW_SET')
 for s in rows:
  expected=(HARNESS if s['source_role']=='ACCEPTED_HARNESS'else PRODUCT)[s['component']]
  if s['commit']!=expected or s['source_role']not in ['ACCEPTED_HARNESS','FROZEN_PRODUCT_OR_PROTOCOL']:raise ValueError('SOURCE_ROLE')
  if s['source_url']!='https://github.com/'+s['repository']+'/blob/'+s['commit']+'/'+s['path']+'#L'+str(s['start_line'])+'-L'+str(s['end_line']):raise ValueError('SOURCE_URL')
  if not 1<=s['start_line']<=s['end_line']or any(not re.fullmatch('[0-9a-f]{64}',s[k])for k in ['source_sha256','span_sha256']):raise ValueError('SPAN_BINDING')
 return set(ids)
def cases(x,ids):
 seen=set()
 for row in x['cases']:
  c=row['component']
  if c not in PRODUCT or c in seen or row['case_id']!=c+'::cross-flavor-equivalence':raise ValueError('CASE_SET')
  seen.add(c)
  if row['assertion']!=ASSERTIONS[c]or row['qualified_product_source_commit']!=PRODUCT[c]or row['accepted_harness_source_commit']!=HARNESS[c]:raise ValueError('CASE_BINDING')
  if row['existing_accepted_coordinate_count']!=COUNTS[c]or row['declared_body_span']not in ids or any(s not in ids for s in row['dispatch_spans']):raise ValueError('CASE_JOIN')
  if row['assessment']!='PARTIAL_SOURCE_AND_DISPATCH_SEMANTICS_NOT_FULL_CAPABILITY_CONFORMANCE':raise ValueError('CASE_SCOPE')
 if seen!=set(PRODUCT):raise ValueError('CASE_SET')
def coordinates(x):
 raw=(R/'reports/analysis-v2/analysis.json').read_bytes()
 if sha(raw)!=x['original_public_analysis_sha256']:raise ValueError('ANALYSIS')
 expected={r['assertion_id']for r in json.loads(raw)['assertions']if r.get('scenario_id')=='cross-flavor-equivalence'}
 ids=x['coordinate_refs']
 if len(ids)!=210 or len(set(ids))!=210 or set(ids)!=expected:raise ValueError('COORDINATE_SET')
def clauses(x,ids):
 rows=x['normative_clauses']
 if {r['id']for r in rows}!={'CAP-UNIQUE','CAP-EMPTY','CAP-PRESERVE','CAP-NODELIST'}:raise ValueError('OBLIGATIONS')
 for r in rows:
  if r['new_runtime_conformance']!='NOT_EXECUTED'or r['complete_normative_conformance']!='UNVERIFIED'or r['dedicated_test_execution_claimed']is not False:raise ValueError('RUNTIME_PROMOTION')
  if not r['source_spans']or any(i not in ids for i in r['source_spans']):raise ValueError('CLAUSE_SOURCE')
def guard(x):
 rows=x['name_guard_observations'];names=[r['name']for r in rows]
 if len(set(names))!=11 or {r['name']for r in rows if not r['same_outcome']}!={'1org.example','0aa.example'}:raise ValueError('GUARD_DIFFERENCE')
 for r in rows:
  if r['same_outcome']!=(r['php_accepts']==r['rust_accepts']):raise ValueError('GUARD_MARKER')
  if r['name']in ['org.example','a.b']and(r['php_accepts']is not True or r['rust_accepts']is not True):raise ValueError('POSITIVE_CONTROL')
 c=x['current_guard_context']
 if c['commit']!='407818227036b37eb12e8f37eb4bb9926387255e'or c['same_as_frozen_guard']is not True:raise ValueError('CURRENT_PIN')
 if c['source_url']!='https://github.com/'+c['repository']+'/blob/'+c['commit']+'/'+c['path']:raise ValueError('CURRENT_URL')
def privacy(x):
 raw=json.dumps(x)
 for marker in ['/Users/','/root/','arn:aws:','GHSA-','authorization.json']:
  if marker in raw:raise ValueError('PRIVATE_MARKER')
 if re.search(r'\b[0-9]{12}\b',raw):raise ValueError('ACCOUNT_SHAPE')
def validate(x):
 Draft202012Validator(json.loads((D/'findings.schema.json').read_bytes())).validate(x)
 ids=windows(x);cases(x,ids);coordinates(x);clauses(x,ids);guard(x);privacy(x);return True
class Findings(unittest.TestCase):
 def test_positive_closed_schema(self):Draft202012Validator.check_schema(json.loads((D/'findings.schema.json').read_bytes()));self.assertTrue(validate(load()))
 def reject(self,fn):
  x=load();fn(x)
  with self.assertRaises((ValueError,ValidationError,KeyError)):validate(x)
 def test_credit(self):self.reject(lambda x:x.__setitem__('qualification_credit',1))
 def test_boolean_credit(self):self.reject(lambda x:x.__setitem__('qualification_credit',False))
 def test_freeze(self):self.reject(lambda x:x.__setitem__('successor_frozen',True))
 def test_full_capability(self):self.reject(lambda x:x.__setitem__('whole_capability_complete',True))
 def test_history(self):self.reject(lambda x:x.__setitem__('historical_inventory_complete',True))
 def test_interoperability(self):self.reject(lambda x:x.__setitem__('independent_interoperability_established',True))
 def test_workload(self):self.reject(lambda x:x.__setitem__('qualification_workload_executed',True))
 def test_duplicate_case(self):self.reject(lambda x:x['cases'].__setitem__(0,copy.deepcopy(x['cases'][1])))
 def test_wrong_assertion(self):self.reject(lambda x:x['cases'][0].__setitem__('assertion','unexecuted_capability_test'))
 def test_harness_product_confusion(self):self.reject(lambda x:x['cases'][0].__setitem__('accepted_harness_source_commit',PRODUCT[x['cases'][0]['component']]))
 def test_duplicate_coordinate(self):self.reject(lambda x:x['coordinate_refs'].__setitem__(0,x['coordinate_refs'][1]))
 def test_foreign_coordinate(self):self.reject(lambda x:x['coordinate_refs'].__setitem__(0,'diagnostic-only'))
 def test_missing_coordinate(self):self.reject(lambda x:x['coordinate_refs'].pop())
 def test_dropped_obligation(self):self.reject(lambda x:x['normative_clauses'].pop())
 def test_static_to_runtime(self):self.reject(lambda x:x['normative_clauses'][0].__setitem__('new_runtime_conformance','PASS'))
 def test_test_source_to_execution(self):self.reject(lambda x:x['normative_clauses'][0].__setitem__('dedicated_test_execution_claimed',True))
 def test_directory_full_contract(self):self.reject(lambda x:x['normative_clauses'][0].__setitem__('complete_normative_conformance','PASS'))
 def test_role_rebind(self):self.reject(lambda x:x['source_windows'][0].__setitem__('commit',HARNESS[x['source_windows'][0]['component']]))
 def test_missing_digest(self):self.reject(lambda x:x['source_windows'][0].pop('span_sha256'))
 def test_bad_window(self):self.reject(lambda x:x['source_windows'][0].__setitem__('start_line',0))
 def test_duplicate_window(self):self.reject(lambda x:x['source_windows'].__setitem__(0,copy.deepcopy(x['source_windows'][1])))
 def test_erased_guard_difference(self):self.reject(lambda x:x['name_guard_observations'][1].__setitem__('same_outcome',True))
 def test_all_denied_not_positive(self):self.reject(lambda x:x['name_guard_observations'][0].__setitem__('php_accepts',False))
 def test_normative_defect_invented(self):self.reject(lambda x:x['name_guard_scope'].__setitem__('normative_defect_confirmed',True))
 def test_http_invented(self):self.reject(lambda x:x['name_guard_scope'].__setitem__('http_executed',True))
 def test_prescriptive_grammar_invented(self):self.reject(lambda x:x['name_guard_scope'].__setitem__('normative_uniform_name_grammar_established',True))
 def test_private_locator(self):self.reject(lambda x:x['limits'].__setitem__(0,'/Users/SYNTHETIC/private'))
 def test_unknown_authority_field(self):self.reject(lambda x:x.__setitem__('acceptance_authority','yes'))
 def test_manifest_hashes(self):
  m=json.loads((D/'manifest.json').read_bytes());self.assertEqual(set(m['files']),{'findings.json','findings.schema.json','README.md'})
  for n,h in m['files'].items():self.assertEqual(sha((D/n).read_bytes()),h)
if __name__=='__main__':unittest.main()
