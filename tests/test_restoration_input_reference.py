import copy
import unittest
from jsonschema import ValidationError
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import restoration_input_reference as module

class RestorationInputReferenceTests(unittest.TestCase):
    def setUp(self):self.value=module.load()
    def reject(self,edit):
        value=copy.deepcopy(self.value);edit(value)
        with self.assertRaises((ValueError,ValidationError)):module.validate(value)
    def test_positive_reviewed_derivative(self):self.assertTrue(module.validate(self.value))
    def test_exact_generated_outputs(self):self.assertTrue(module.check())
    def test_deterministic_rendering(self):self.assertEqual(module.render(self.value),module.render(copy.deepcopy(self.value)))
    def test_identity_role_counts_preserved(self):self.assertEqual(self.value['classification']['distinct_digests_by_role']['test_dependencies_sha256'],171)
    def test_no_new_credit(self):self.reject(lambda v:v['boundaries'].update(qualification_credit=1))
    def test_no_boolean_credit(self):self.reject(lambda v:v['boundaries'].update(qualification_credit=False))
    def test_no_new_assignments(self):self.reject(lambda v:v['boundaries'].update(new_assignment_credit=10))
    def test_no_runtime_promotion(self):self.reject(lambda v:v['boundaries'].update(runtime_execution_performed=True))
    def test_no_qualification_promotion(self):self.reject(lambda v:v['boundaries'].update(qualification_workloads_performed=True))
    def test_no_historical_completeness_promotion(self):self.reject(lambda v:v['boundaries'].update(historical_inventory_complete=True))
    def test_no_successor_freeze_promotion(self):self.reject(lambda v:v['boundaries'].update(corrected_successor_frozen=True))
    def test_no_external_certification(self):self.reject(lambda v:v['boundaries'].update(independent_external_certification_established=True))
    def test_known_hit_not_new_locator(self):self.reject(lambda v:v['new_raw_locator_question'].update(additional_locators=1))
    def test_unlocated_not_global_loss(self):self.reject(lambda v:v['new_raw_locator_question'].update(global_absence_established=True))
    def test_not_all_binding_metadata_resolved(self):self.reject(lambda v:v['original_metadata_availability']['package_binding_identities'].update(resolved=236))
    def test_not_a_restored_installed_tree(self):self.reject(lambda v:v['original_metadata_availability'].update(installed_tree_restoration_established=True))
    def test_no_private_paths(self):self.reject(lambda v:v['limits'].append('/Users/synthetic/private-marker'))
    def test_no_account_shapes(self):self.reject(lambda v:v['findings'].append('123456789012'))
    def test_no_aws_resource_identity(self):self.reject(lambda v:v['findings'].append('arn:aws:synthetic'))
    def test_source_substitution_refused(self):self.reject(lambda v:v.update(canonical_root_commit='0'*40))
    def test_no_raw_captures(self):self.reject(lambda v:v.update(private_capture='synthetic'))
    def test_missing_limit_refused(self):self.reject(lambda v:v['limits'].pop())
    def test_no_extra_component_group_coverage(self):self.reject(lambda v:v['classification'].update(component_scoped_groups=530))
    def test_review_identity_substitution_refused(self):self.reject(lambda v:v['private_review_digests'][0].update(sha256='0'*64))

if __name__=='__main__':unittest.main()
