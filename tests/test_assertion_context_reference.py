import copy
import re
import sys
import unittest
from pathlib import Path
from jsonschema import ValidationError
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import assertion_context_reference as ref

class AssertionContextReferenceTests(unittest.TestCase):
    def setUp(self):self.value=ref.load();self.original=copy.deepcopy(self.value)
    def reject(self):
        self.assertNotEqual(ref.canonical(self.value),ref.canonical(self.original),'negative fixture must change representation')
        with self.assertRaises((ValueError,ValidationError)):ref.validate(self.value)
    def row(self,key):return next(r for r in self.value['cases'] if r['case_id']==key)
    def test_positive_reviewed_source_package(self):self.assertTrue(ref.check())
    def test_render_determinism(self):self.assertEqual(ref.render(self.value),ref.render(copy.deepcopy(self.value)))
    def test_all43_table_rows_have_four_columns(self):
        lines=[s for s in ref.render(self.value).splitlines() if s.startswith('| [')]
        self.assertEqual(len(lines),43)
        for line in lines:self.assertEqual(len(re.findall(r'(?<!\\)\|',line)),5)
    def test_missing_case(self):self.value['cases'].pop();self.reject()
    def test_duplicate_case(self):self.value['cases'][0]=copy.deepcopy(self.value['cases'][1]);self.reject()
    def test_pipeline_identity_substitution(self):self.value['cases'][0]['accepted_pipeline']['sha256']='0'*64;self.reject()
    def test_raw_declaration_as_actual_probe(self):self.row('directory-rust::disk-full')['effective_source_role']='RAW_ERROR_INJECTION_ONLY';self.reject()
    def test_management_optional_skip_claim(self):self.row('management::package-version-self-report')['effective_source_role']='OPTIONAL_MISSING_ENV_SKIP';self.reject()
    def test_source_coverage_as_conformance(self):self.value['source_frontier']['whole_capability_conformance']=True;self.reject()
    def test_source_coverage_as_reference_freeze(self):self.value['corrected_reference_frozen']=True;self.reject()
    def test_historical_completeness_promotion(self):self.value['historical_inventory_complete']=True;self.reject()
    def test_qualification_credit(self):self.value['new_qualification_credit']=1;self.reject()
    def test_new_runtime_claim(self):self.value['new_runtime_executions']=1;self.reject()
    def test_wrong_reference_total(self):self.value['cases'][0]['existing_reference_count']+=1;self.reject()
    def test_foreign_directory_platform(self):self.row('directory-rust::disk-full')['applicable_targets'].append('windows-x86_64');self.reject()
    def test_pre_normative_fixture_not_promoted(self):self.value['crypto_fixture_context']['status']='stable-normative';self.reject()
    def test_uniform_crypto_validator_not_inferred(self):self.value['rust_crypto_scope']['observed_path']='All three SDK fixture paths invoke the same production verifier';self.reject()
    def test_declared_command_change(self):self.value['cases'][0]['declaration_command'].append('--unreviewed');self.reject()
    def test_private_marker(self):self.value['limits'].append('/Users/synthetic-marker/private-capture');self.reject()
    def test_unreviewed_field(self):self.value['unreviewed_claim']='synthetic';self.reject()
    def test_negative_noop_guard(self):
        with self.assertRaisesRegex(AssertionError,'must change'):self.reject()

if __name__=='__main__':unittest.main()
