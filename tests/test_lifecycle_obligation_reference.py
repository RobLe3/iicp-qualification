import copy,re,sys,unittest
from pathlib import Path
from jsonschema.exceptions import ValidationError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import lifecycle_obligation_reference as ref
class LifecycleObligationReferenceTests(unittest.TestCase):
 def setUp(self):self.value=ref.load();self.original=copy.deepcopy(self.value)
 def reject(self):
  self.assertNotEqual(ref.canonical(self.value),ref.canonical(self.original),'negative fixture must change representation')
  with self.assertRaises((ValueError,ValidationError)):ref.validate(self.value)
 def test_positive_control(self):self.assertTrue(ref.check())
 def test_render_deterministic(self):self.assertEqual(ref.render(self.value),ref.render(copy.deepcopy(self.value)))
 def test_ten_obligation_rows_three_columns(self):
  rows=[r for r in ref.render(self.value).splitlines() if r.startswith('| [lifecycle-')];self.assertEqual(len(rows),10)
  for r in rows:self.assertEqual(len(re.findall(r'(?<!\\)\|',r)),4)
 def test_sixteen_fixture_rows_five_columns(self):
  rows=[r for r in ref.render(self.value).splitlines() if r.startswith('| LIFECYCLE-')];self.assertEqual(len(rows),16)
  for r in rows:self.assertEqual(len(re.findall(r'(?<!\\)\|',r)),6)
 def test_only_negotiation_is_unmapped_in_obligation_table(self):
  rows=[r for r in ref.render(self.value).splitlines() if r.startswith('| [lifecycle-')]
  self.assertEqual(sum('Not mapped in this batch' in r for r in rows),1)
  terminal=next(r for r in rows if '[lifecycle-terminality-and-alias]' in r)
  self.assertIn('See selected transition-fixture consumers below',terminal)
 def test_qualification_credit(self):self.value['qualification_credit']=1;self.reject()
 def test_bool_credit(self):self.value['qualification_credit']=False;self.reject()
 def test_float_count(self):self.value['counts']['fixture_vectors']=16.0;self.reject()
 def test_candidate_substitution(self):self.value['candidate_digest']='sha256:'+'0'*64;self.reject()
 def test_ratifcation_promotion(self):self.value['authority_layers'][1]['status']='RATIFIED';self.reject()
 def test_reference_freeze(self):self.value['baseline_frozen']=True;self.reject()
 def test_history_completion(self):self.value['historical_inventory_complete']=True;self.reject()
 def test_source_as_runtime(self):self.value['vector_consumer_cells'][0]['runtime_executed_in_this_batch']=True;self.reject()
 def test_source_as_campaign_credit(self):self.value['vector_consumer_cells'][0]['campaign_execution_inferred']=True;self.reject()
 def test_walk_as_full_vector(self):self.value['vector_consumer_cells'][0]['full_vector_field_conformance_proven']=True;self.reject()
 def test_unconsumed_vector_inflation(self):self.value['vector_consumer_cells'][9]['fixture_state_label_walk']=True;self.reject()
 def test_duplicate_component_cell(self):self.value['vector_consumer_cells'][0]=copy.deepcopy(self.value['vector_consumer_cells'][1]);self.reject()
 def test_missing_vector(self):self.value['fixture_vector_domain'].pop();self.reject()
 def test_expected_outcome_altered(self):self.value['fixture_vector_domain'][2]['expected']='accept';self.reject()
 def test_source_hash_substitution(self):self.value['source_blobs'][0]['sha256']='0'*64;self.reject()
 def test_foreign_source_commit(self):self.value['vector_consumer_cells'][0]['source_ref']['source']['commit']='0'*40;self.reject()
 def test_heading_only_exclusion(self):self.value['authority_layers'][-1]['ref']['end_line']=self.value['authority_layers'][-1]['ref']['start_line'];self.reject()
 def test_unqualified_function_promotion(self):self.value['campaign_dispatch_boundary'][0]['selected_fixture_loop_is_this_case']=True;self.reject()
 def test_backend_termination_overclaim(self):self.value['semantic_predicate_joins'][8]['runtime_observation']='BACKEND_STOPPED';self.reject()
 def test_private_locator_refused(self):self.value['limits'].append('/Users/synthetic-marker/private-capture');self.reject()
 def test_unknown_claim_refused(self):self.value['unreviewed_claim']='synthetic';self.reject()
 def test_negative_noop_guard(self):
  with self.assertRaisesRegex(AssertionError,'must change'):self.reject()
if __name__=='__main__':unittest.main()
