"""Validate a minimized reporting derivative, not undistributed helper execution."""
from pathlib import Path
import copy,hashlib,json,re,unittest
from jsonschema import Draft202012Validator,ValidationError
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'reports/postcert/2026-11-06-capability-selection'
IMPL={'client-python','client-typescript','client-rust','directory-php','directory-rust'}
CASES={'text_chat_uses_complete_single_variant','vision_and_tools_match_one_variant','cross_variant_union_is_forbidden','unknown_required_fails_closed','unknown_preference_does_not_change_eligibility','limit_is_unsatisfied','stale_required_claim_fails_closed','policy_denial_is_not_capability_absence','unknown_optional_extension_is_preserved'}
EXTRA={'known_preference_absent_from_matching_intent','known_preference_only_in_limit_excluded_variant'}
COMMITS={'RobLe3/iicp-client-python':'9c5b3d894ee89ef9fcde52ea0ad99d388ed62183','RobLe3/iicp-client-typescript':'97c768d8b9e90756773103e432c273a7d98ba08e','RobLe3/iicp-client-rust':'0b8b529262977b6482dd7900d473e7d152ba9293','RobLe3/iicp-directory-php':'2dfd228b49c587150a44f448cea1351a9f039d32','RobLe3/iicp-directory-rust':'b95a362ad8f974334994ca73cd20210388a2362f','RobLe3/IICP':'2d240649cf8d11a235132658a599e22ebcba6620'}
def load():return json.loads((D/'findings.json').read_bytes())
def validate_matching(x):
 rows=x['shared_matching_projection'];pairs=[(r['implementation'],r['scenario'])for r in rows]
 if len(set(pairs))!=45 or set(pairs)!={(i,c)for i in IMPL for c in CASES}:raise ValueError('MATCHING_SET')
 for r in rows:
  if r['status']!='PASS' or r['directory_extension_storage_or_wire_preservation']!='NOT_EXECUTED':raise ValueError('UNSUPPORTED_PROMOTION')
  if r['asserted_fields'] not in [['eligible','variant_ids','preference_unavailable'],['eligible','refusal_code'],['eligible','variant_ids','preference_unavailable','preserved_extensions']]:raise ValueError('FIELD_SCOPE')

def validate_extra(x):
 rows=x['extra_observations'];pairs=[(r['implementation'],r['scenario'])for r in rows]
 if len(set(pairs))!=10 or set(pairs)!={(i,c)for i in IMPL for c in EXTRA}:raise ValueError('EXTRA_SET')
 for r in rows:
  if r['hard_projection']!='PASS' or r['diagnostic_flag_oracle']!='UNSPECIFIED_BY_ORIGINAL_SHARED_FIXTURE' or r['observed_preference_unavailable']!=(r['implementation'].startswith('client-')):raise ValueError('DIAGNOSTIC_DIFFERENCE')
  if not r['variant_ids'] or len(set(r['variant_ids']))!=len(r['variant_ids']):raise ValueError('VARIANT_SET')

def validate_sources(x):
 sources=x['sources'];ids=[(s['repository'],s['commit'],s['path'])for s in sources]
 if len(set(ids))!=33 or len({s['sha256']for s in sources})!=28:raise ValueError('SOURCE_SET')
 for s in sources:
  if COMMITS.get(s['repository'])!=s['commit'] or not re.fullmatch('[0-9a-f]{64}',s['sha256']) or not s['path'] or '..'in s['path'].split('/') or s['path'].startswith('/'):raise ValueError('SOURCE_BINDING')
  if s['url']!='https://github.com/'+s['repository']+'/blob/'+s['commit']+'/'+s['path']:raise ValueError('SOURCE_URL')

def validate_privacy(x):
 for k in ['private_bundle_manifest_sha256','private_observations_sha256']:
  if not re.fullmatch('[0-9a-f]{64}',x['evidence'][k]):raise ValueError('EVIDENCE_DIGEST')
 raw=json.dumps(x)
 for marker in ['/Users/','/root/','arn:aws:','GHSA-','authorization.json']:
  if marker in raw:raise ValueError('PRIVATE_MARKER')
 if re.search(r'\b[0-9]{12}\b',raw):raise ValueError('ACCOUNT_SHAPE')

def validate(x):
 Draft202012Validator(json.loads((D/'findings.schema.json').read_bytes())).validate(x)
 for fn in [validate_matching,validate_extra,validate_sources,validate_privacy]:fn(x)
 return True
class Findings(unittest.TestCase):
 def test_closed_schema_valid(self):Draft202012Validator.check_schema(json.loads((D/'findings.schema.json').read_bytes()));self.assertTrue(validate(load()))
 def reject(self,fn):
  x=load();fn(x)
  with self.assertRaises((ValueError,ValidationError)) as e:validate(x)
  self.assertIsNotNone(e.exception)
 def test_reject_duplicate_matching(self):self.reject(lambda x:x['shared_matching_projection'].__setitem__(0,copy.deepcopy(x['shared_matching_projection'][1])))
 def test_reject_missing_matching(self):self.reject(lambda x:x['shared_matching_projection'].pop())
 def test_reject_foreign_implementation(self):self.reject(lambda x:x['shared_matching_projection'][0].__setitem__('implementation','management'))
 def test_reject_test_source_as_execution(self):self.reject(lambda x:x['shared_matching_projection'][0].__setitem__('status','SOURCE_ONLY'))
 def test_reject_directory_storage_promotion(self):self.reject(lambda x:x['shared_matching_projection'][0].__setitem__('directory_extension_storage_or_wire_preservation','PASS'))
 def test_reject_credit(self):self.reject(lambda x:x.__setitem__('qualification_credit',1))
 def test_reject_full_baseline(self):self.reject(lambda x:x.__setitem__('whole_capability_complete',True))
 def test_reject_freeze(self):self.reject(lambda x:x.__setitem__('successor_frozen',True))
 def test_reject_historical_completion(self):self.reject(lambda x:x.__setitem__('historical_inventory_complete',True))
 def test_reject_interoperability(self):self.reject(lambda x:x.__setitem__('independent_interoperability_established',True))
 def test_reject_extra_oracle_invention(self):self.reject(lambda x:x['extra_observations'][0].__setitem__('diagnostic_flag_oracle','NORMATIVE'))
 def test_reject_erased_difference(self):self.reject(lambda x:x['extra_observations'][0].__setitem__('observed_preference_unavailable',False))
 def test_reject_candidate_substitution(self):self.reject(lambda x:x.__setitem__('candidate_digest','sha256:'+'0'*64))
 def test_reject_source_commit(self):self.reject(lambda x:x['sources'][0].__setitem__('commit','0'*40))
 def test_reject_missing_source_digest(self):self.reject(lambda x:x['sources'][0].pop('sha256'))
 def test_reject_malformed_source_digest(self):self.reject(lambda x:x['sources'][0].__setitem__('sha256',''))
 def test_reject_source_url(self):self.reject(lambda x:x['sources'][0].__setitem__('url','https://example.invalid'))
 def test_reject_duplicate_sources(self):self.reject(lambda x:x['sources'].__setitem__(0,copy.deepcopy(x['sources'][1])))
 def test_reject_public_private_bundle_claim(self):self.reject(lambda x:x['evidence'].__setitem__('private_bundle_included_in_public_package',True))
 def test_reject_private_locator(self):self.reject(lambda x:x['limits'].__setitem__(0,'/Users/SYNTHETIC/private'))
 def test_reject_unknown_field(self):self.reject(lambda x:x.__setitem__('authority','qualified'))
 def test_manifest_all_exact_bytes(self):
  m=json.loads((D/'manifest.json').read_bytes());self.assertEqual(set(m['files']),{'findings.json','findings.schema.json','README.md'})
  for n,h in m['files'].items():self.assertEqual(hashlib.sha256((D/n).read_bytes()).hexdigest(),h)
 def test_positive_and_negative_shared_cases(self):
  x=load();r=[r for r in x['shared_matching_projection']if r['implementation']=='client-python'];self.assertEqual(sum('refusal_code'in r['asserted_fields']for r in r),5);self.assertEqual(len(r),9)
if __name__=='__main__':unittest.main()
