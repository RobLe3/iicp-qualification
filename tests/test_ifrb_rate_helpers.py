import unittest,json,tempfile,shutil,copy,ast
from pathlib import Path
from unittest.mock import patch
from scripts import ifrb_rate_helpers as w

class Controls(unittest.TestCase):
 def expected(self):
  v=w.load_vectors();return {'python-relay':[[s['expected'] for s in c['steps']] for c in v['relay']],'typescript-relay':[[s['expected'] for s in c['steps']] for c in v['relay']],'rust-relay':[[s['expected'] for s in c['steps']] for c in v['relay']],'rust-registration':[c['expected'] for c in v['registration_step']],'php-redirect-clamp':[c['expected'] for c in v['retry_after_clamp']]}
 def test_pinned_sources(self):self.assertEqual(len(w.load_fragments()),5)
 def test_public_source_metadata(self):
  rows=json.loads((w.D/'fragments.json').read_text())['fragments']
  self.assertEqual(len(rows),5)
  for r in rows:self.assertTrue(r['source_url'].startswith('https://github.com/RobLe3/'));self.assertEqual(w.digest(r['code'].encode()),r['fragment_sha256'])
 def test_reject_changed_digest(self):
  with self.assertRaises(ValueError):w.checked(b'changed','0'*64)
 def test_reject_source_mutation(self):
  real=Path.read_bytes
  def read(p):
   data=real(p);return data+b'\n' if p.name=='fragments.json' else data
  with patch.object(Path,'read_bytes',read),self.assertRaises(ValueError):w.load_fragments()
 def test_reject_pin_mutation(self):
  real=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda p: b'{}' if p.name=='fragments.json' else real(p)),self.assertRaises(ValueError):w.load_fragments()
 def test_reject_vector_mutation(self):
  real=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda p:b'{}' if p.name=='vectors.json' else real(p)),self.assertRaises(ValueError):w.load_vectors()
 def test_positive_golden_is_accepted(self):self.assertTrue(w.verify_observations(self.expected(),w.load_vectors()))
 def reject(self,modify):
  a=self.expected();modify(a)
  with self.assertRaises(ValueError):w.verify_observations(a,w.load_vectors())
 def test_always_allow_rejected(self):self.reject(lambda a:a['python-relay'].__setitem__(1,[True]*3))
 def test_always_deny_rejected(self):self.reject(lambda a:a['typescript-relay'].__setitem__(0,[False]))
 def test_cross_source_shared_bucket_rejected(self):self.reject(lambda a:a['rust-relay'][2].__setitem__(2,False))
 def test_bad_exact_expiry_rejected(self):self.reject(lambda a:a['python-relay'][4].__setitem__(1,False))
 def test_sliding_window_rejected(self):self.reject(lambda a:a['rust-relay'][9].__setitem__(2,False))
 def test_rebind_consumption_rejected(self):self.reject(lambda a:a['typescript-relay'][7].__setitem__(1,False))
 def test_wrong_registration_reset_rejected(self):self.reject(lambda a:a['rust-registration'].__setitem__(3,[6,1000]))
 def test_zero_retry_rejected(self):self.reject(lambda a:a['php-redirect-clamp'].__setitem__(1,0))
 def test_int_cannot_substitute_bool(self):self.reject(lambda a:a['python-relay'][0].__setitem__(0,1))
 def test_missing_implementation_rejected(self):self.reject(lambda a:a.pop('typescript-relay'))
 def test_unexpected_implementation_rejected(self):self.reject(lambda a:a.__setitem__('foreign',[]))
 def test_truncated_steps_rejected(self):self.reject(lambda a:a['python-relay'][0].pop())
 def test_duplicate_result_rejected(self):self.reject(lambda a:a['rust-registration'].append(a['rust-registration'][0]))
 def test_fixed_vectors_unique_ids_and_positive_negative(self):
  v=w.load_vectors()
  for key in ['relay','registration_step','retry_after_clamp']:
   ids=[c['id'] for c in v[key]];self.assertEqual(len(ids),len(set(ids)))
  seen={s['expected'] for c in v['relay'] for s in c['steps']};self.assertEqual(seen,{True,False})
 def test_generated_programs_do_not_import_products_or_network(self):
  p=w.generate_programs(w.load_fragments(),w.load_vectors());self.assertEqual(len(p),3)
  for source in p.values():
   for forbidden in ['node:net','node:http','fetch(','curl ','aws ','run_pre1','vendor/autoload','use axum','serde_json'] :self.assertNotIn(forbidden,source)
 def test_generated_fragments_byte_preserved(self):
  f=w.load_fragments();p=w.generate_programs(f,w.load_vectors())
  for id,key in [('typescript-relay','typescript-witness.mts'),('rust-relay','rust-witness.rs'),('rust-registration','rust-witness.rs'),('php-redirect-clamp','php-witness.php')]:self.assertIn(f[id],p[key])
 def test_python_fragment_synthetic_boundary(self):
  f=w.load_fragments();v=w.load_vectors();self.assertEqual(w.python_relay(f['python-relay'],v['relay']),self.expected()['python-relay'])
 def test_python_forbidden_missing_method(self):
  with self.assertRaises(ValueError):w.python_relay('def wrong(): pass',w.load_vectors()['relay'])


class BundleControls(unittest.TestCase):
 def test_schema_and_closed_top_level(self):
  from jsonschema import Draft202012Validator
  schema=json.loads((w.D/'bundle.schema.json').read_text());Draft202012Validator.check_schema(schema)
  for name in ['fragments.json','vectors.json']:Draft202012Validator(schema).validate(json.loads((w.D/name).read_text()))
 def test_reject_unknown_schema_field(self):
  from jsonschema import Draft202012Validator,ValidationError
  x=json.loads((w.D/'fragments.json').read_text());x['foreign_authority']='accepted'
  with self.assertRaises(ValidationError):Draft202012Validator(json.loads((w.D/'bundle.schema.json').read_text())).validate(x)
 def test_reject_credit_inflation_schema(self):
  from jsonschema import Draft202012Validator,ValidationError
  x=json.loads((w.D/'fragments.json').read_text());x['qualification_credit']=1
  with self.assertRaises(ValidationError):Draft202012Validator(json.loads((w.D/'bundle.schema.json').read_text())).validate(x)
 def test_reject_successor_promotion_schema(self):
  from jsonschema import Draft202012Validator,ValidationError
  x=json.loads((w.D/'fragments.json').read_text());x['successor_frozen']=True
  with self.assertRaises(ValidationError):Draft202012Validator(json.loads((w.D/'bundle.schema.json').read_text())).validate(x)
 def test_manifest_integrity(self):
  m=json.loads((w.D/'manifest.json').read_text())
  for name,h in m['files'].items():self.assertEqual(w.digest((w.D/name).read_bytes()),h)
  self.assertEqual(w.digest((w.ROOT/'scripts/ifrb_rate_helpers.py').read_bytes()),m['runner_sha256'])
 def test_public_coordinate_joins(self):
  doc=json.loads((w.D/'fragments.json').read_text());raw=(w.ROOT/'reports/analysis-v2/analysis.json').read_bytes();self.assertEqual(w.digest(raw),doc['public_analysis_file_sha256']);a=json.loads(raw);index={r['assertion_id']:r for r in a['assertions']};seen=[]
  for f in doc['fragments']:
   for r in f['existing_coordinate_refs']:
    original=index[r['assertion_id']];self.assertEqual(original['component'],f['component']);self.assertEqual(original['scenario_id'],'rate-limit')
    for key,value in r.items():self.assertEqual(original[key],value)
    self.assertEqual(original['candidate_manifest_sha256'],doc['candidate_manifest_sha256']);seen.append(r['assertion_id'])
  self.assertEqual(len(seen),210);self.assertEqual(len(set(seen)),210)
 def test_privacy_and_authority_boundaries(self):
  raw=(w.D/'fragments.json').read_text()
  for forbidden in ['/Users/','/root/','arn:aws:','authorization.json','GHSA-','052530']:self.assertNotIn(forbidden,raw)
  d=json.loads(raw)
  for flag in ['acceptance_changed','successor_frozen','independent_interoperability_established','full_capability_complete','historical_inventory_complete']:self.assertIs(d[flag],False)
 def test_no_original_execution_entrypoint(self):
  source=(w.ROOT/'scripts/ifrb_rate_helpers.py').read_text()
  for forbidden in ['run_pre1_qualification_case','boto3','aws login','requests.get','httpx','import iicp_client']:self.assertNotIn(forbidden,source)
 def test_output_refuses_existing_directory(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);(p/'keep').write_bytes(b'unchanged')
   with patch.object(w,'run_bounded',side_effect=AssertionError('unexpected command')),self.assertRaises(FileExistsError):w.execute(p)
   self.assertEqual((p/'keep').read_bytes(),b'unchanged')
 def test_failed_command_retains_output_and_no_pass(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)
   with patch.object(w.subprocess,'run',return_value=type('R',(),{'returncode':7})()),self.assertRaisesRegex(ValueError,'COMMAND_FAILED'):w.run_bounded(['unused'],p,'failed')
   self.assertTrue((p/'failed.stdout').exists());self.assertEqual((p/'failed.exit').read_text(),'7\n');self.assertFalse((p/'observations.json').exists())
 def test_timeout_never_creates_observation_pass(self):
  import subprocess
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)
   with patch.object(w.subprocess,'run',side_effect=subprocess.TimeoutExpired('unused',1)),self.assertRaises(subprocess.TimeoutExpired):w.run_bounded(['unused'],p,'timed')
   self.assertTrue((p/'timed.stdout').exists());self.assertFalse((p/'observations.json').exists())

if __name__=='__main__':unittest.main()
