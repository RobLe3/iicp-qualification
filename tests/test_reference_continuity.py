import copy,importlib.util,json,unittest
from pathlib import Path
from jsonschema import ValidationError
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reference_continuity',ROOT/'scripts/reference_continuity.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ReferenceContinuity(unittest.TestCase):
 def bad(self,change):
  value=copy.deepcopy(m.load());change(value)
  with self.assertRaises((ValueError,ValidationError)):m.validate(value)
 def test_exact_reviewed_data(self):self.assertTrue(m.validate(m.load()))
 def test_generated_narrative_and_manifest(self):self.assertTrue(m.check())
 def test_deterministic_render(self):self.assertEqual(m.render(m.load()),m.render(m.load()))
 def test_no_added_credit(self):self.bad(lambda x:x['counts'].update(qualification_credit=3))
 def test_no_whole_case_promotion(self):self.bad(lambda x:x['counts'].update(whole_original_cases_completed=3))
 def test_no_criterion_promotion(self):self.bad(lambda x:x['counts'].update(formal_criterion_updates=3))
 def test_no_bool_count_substitution(self):self.bad(lambda x:x['counts'].update(qualification_credit=False))
 def test_no_float_count_substitution(self):self.bad(lambda x:x['counts'].update(new_opt_in_v2_product_unit_methods=3.0))
 def test_no_default_v1_inference(self):self.bad(lambda x:x['credential_witnesses'].update(default_v1_path_tested=True))
 def test_no_rotation_procedure_inference(self):self.bad(lambda x:x['credential_witnesses']['observations'].append('Rotation procedure established.'))
 def test_no_omitted_credential_limits(self):self.bad(lambda x:x['credential_witnesses'].update(limitations=[]))
 def test_no_omitted_archive_limits(self):self.bad(lambda x:x['package_metadata'].update(limitations=[]))
 def test_no_archive_runtime_inference(self):self.bad(lambda x:x['package_metadata']['rows'][0].update(new_runtime_self_report_executed=True))
 def test_no_installer_linkage_inference(self):self.bad(lambda x:x['package_metadata']['rows'][0].update(historical_offline_installer_linkage_resolved=True))
 def test_no_registry_publication_inference(self):self.bad(lambda x:x['package_metadata']['rows'][0].update(sdk_tag_or_registry_publication_verified=True))
 def test_no_foreign_source(self):self.bad(lambda x:x['credential_witnesses'].update(source_commit='0'*40))
 def test_no_foreign_candidate(self):self.bad(lambda x:x.update(original_candidate_identity='sha256:'+'0'*64))
 def test_no_complete_history_inference(self):self.bad(lambda x:x['boundaries'].update(historical_inventory_complete=True))
 def test_no_private_path(self):self.bad(lambda x:x['credential_witnesses'].update(raw_capture='/Users/private/capture'))
 def test_no_new_authority(self):self.bad(lambda x:x['boundaries'].update(qualification_authority_changed=True))
 def test_no_external_certification(self):self.bad(lambda x:x['boundaries'].update(independent_external_certification_established=True))
 def test_no_unknown_field(self):self.bad(lambda x:x.update(unreviewed_findings=[]))
 def test_no_frozen_successor_inference(self):self.bad(lambda x:x['boundaries'].update(corrected_successor_frozen=True))
 def test_fixed_check_not_private_execution_proof(self):
  text=m.render(m.load());self.assertIn('cannot inspect undistributed captures',text);self.assertIn('default v1 authentication path was not tested',text)
if __name__=='__main__':unittest.main()
