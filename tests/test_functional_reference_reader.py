import copy,sys,unittest
from pathlib import Path
from jsonschema.exceptions import ValidationError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import functional_reference_reader as ref
class FunctionalReferenceReaderTests(unittest.TestCase):
 def setUp(self):self.value=ref.load();self.original=copy.deepcopy(self.value)
 def reject(self):
  self.assertNotEqual(ref.canonical(self.value),ref.canonical(self.original),'negative control must change representation')
  with self.assertRaises((ValueError,ValidationError)):ref.validate(self.value)
 def test_positive_control(self):self.assertTrue(ref.check())
 def test_render_deterministic(self):self.assertEqual(ref.render(self.value),ref.render(copy.deepcopy(self.value)))
 def test_147_case_rows(self):self.assertEqual(sum(x.startswith('| [') for x in ref.render(self.value).splitlines()),147)
 def test_36_catalog_and28_family_rows(self):self.assertEqual(sum(x.startswith('| ') for x in ref.render(self.value).splitlines()),36+28+147+3)
 def test_foreign_candidate(self):self.value['candidate_manifest_sha256']='sha256:'+'0'*64;self.reject()
 def test_false_frozen_baseline(self):self.value['baseline_frozen']=True;self.reject()
 def test_execution_authority(self):self.value['execution_authorized']=True;self.reject()
 def test_credit_inflation(self):self.value['qualification_credit']=64;self.reject()
 def test_bool_credit(self):self.value['qualification_credit']=False;self.reject()
 def test_float_definition_count(self):self.value['graph_counts']['case_definitions']=147.0;self.reject()
 def test_missing_case(self):self.value['case_rows'].pop();self.reject()
 def test_duplicate_case(self):self.value['case_rows'][0]=copy.deepcopy(self.value['case_rows'][1]);self.reject()
 def test_missing_coordinate_references(self):self.value['case_rows'][0]['accepted_reference_count']-=1;self.reject()
 def test_changed_target_applicability(self):self.value['case_rows'][0]['recorded_targets']=['foreign-target'];self.reject()
 def test_unknown_source_identity(self):self.value['source_input_digests'][0]='0'*64;self.reject()
 def test_changed_case_map(self):self.value['case_rows'][0]['case_map_url']='https://example.invalid/foreign';self.reject()
 def test_raw_to_runtime_promotion(self):self.value['case_rows'][0]['new_runtime_executions']=1;self.reject()
 def test_source_to_full_conformance(self):self.value['case_rows'][0]['full_semantic_conformance']=True;self.reject()
 def test_changed_predicate(self):next(r for r in self.value['case_rows'] if r['predicate_terms'])['predicate_terms'][0]['value']='all production behavior verified';self.reject()
 def test_context_removed(self):next(r for r in self.value['case_rows'] if r['effective_context_terms'])['effective_context_terms']=[];self.reject()
 def test_scope_limit_removed(self):next(r for r in self.value['case_rows'] if r['limitation_terms'])['limitation_terms']=[];self.reject()
 def test_source_code_body_export(self):self.value['case_rows'][0]['raw_source_code']='synthetic non-sensitive marker';self.reject()
 def test_controlled_locator_export(self):self.value['case_rows'][0]['review_ref']['input_path']='/Users/synthetic/private-marker';self.reject()
 def test_review_pointer_change(self):self.value['case_rows'][0]['review_ref']['json_pointer']='/foreign';self.reject()
 def test_unsupported_promoted(self):next(r for r in self.value['capability_dispositions'] if r['classification']=='UNSUPPORTED')['reference_scope_group']='SUPPORTED_OR_CONDITIONAL_SCOPE_REVIEW';self.reject()
 def test_optional_blanket_excluded(self):next(r for r in self.value['capability_dispositions'] if r['classification']=='OPTIONAL_STABLE')['reference_scope_group']='BOUNDARY_AND_NONPROMOTION_REVIEW';self.reject()
 def test_unmapped_means_no_tests_overclaim(self):self.value['capability_dispositions'][0]['disposition']='NO_TESTS_EXIST';self.reject()
 def test_later_slice_as_credit(self):self.value['reference_slices'][0]['qualification_credit']=1;self.reject()
 def test_later_slice_as_reviewed_obligation(self):self.value['reference_slices'][0]['obligation_crosswalk']='VERIFIED';self.reject()
 def test_lifecycle_as_complete(self):self.value['lifecycle_obligations'][0]['whole_obligation_verified']=True;self.reject()
 def test_controlled_catalog_text_export_refused(self):self.value['catalog_obligations'][0]['expected_behavior']='always pass';self.reject()
 def test_timeout_negative_flags_visible(self):
  for c in ['client-python','client-typescript','client-rust']:
   r=next(r for r in self.value['case_rows'] if r['case_id']==c+'::request-timeout');f={x['field']:x['value'] for x in r['scope_flags']};self.assertIs(f['retry_safety_proven'],False);self.assertIs(f['provider_terminal_state_proven'],False)
 def test_staged_credential_flags_are_raw_labeled(self):
  for c in ['client-python','client-typescript']:
   for scenario in ['credential-expired','credential-replayed','credential-rotated','signature-mismatch']:
    r=next(r for r in self.value['case_rows'] if r['case_id']==c+'::'+scenario);self.assertEqual(r['scope_interpretation_layer'],'RAW_DECLARED_SOURCE_SCOPE_REQUIRES_EFFECTIVE_CONTEXT');self.assertTrue(r['effective_context_terms'])
 def test_no_catalog_prose_exported(self):
  self.assertTrue(all('expected_behavior' not in r and r['expectation_status']=='CONTROLLED_CATALOG_TEXT_NOT_DISTRIBUTED' for r in self.value['catalog_obligations']))
 def test_historical_completeness(self):self.value['historical_inventory_complete']=True;self.reject()
 def test_global_semantic_completeness(self):self.value['whole_capability_completion']=True;self.reject()
 def test_unknown_claim(self):self.value['independent_external_certification']=True;self.reject()
 def test_graph_digest_changed(self):self.value['private_graph_sha256']='0'*64;self.reject()
 def test_noop_negative(self):
  with self.assertRaisesRegex(AssertionError,'must change'):self.reject()
if __name__=='__main__':unittest.main()
