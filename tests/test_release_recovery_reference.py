import copy
import json
import re
from pathlib import Path
import sys
import unittest
from jsonschema import ValidationError
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import release_recovery_reference as ref

class ReleaseRecoveryReferenceTests(unittest.TestCase):
    def setUp(self):
        self.value = ref.load()
        self.original = copy.deepcopy(self.value)
    def reject(self):
        self.assertNotEqual(ref.canonical(self.value), ref.canonical(self.original), 'negative control must change the reviewed representation')
        with self.assertRaises((ValueError, ValidationError)):
            ref.validate(self.value)
    def row(self, key):
        return next(r for r in self.value['cases'] if r['case_id'] == key)
    def test_positive_reviewed_package(self):self.assertTrue(ref.check())
    def test_render_deterministic(self):self.assertEqual(ref.render(self.value), ref.render(copy.deepcopy(self.value)))
    def test_pipe_and_newline_cells_are_escaped(self):
        self.assertEqual(ref.cell('a|b\nc\r\nd\re'), 'a\\|b<br>c<br>d<br>e')
    def test_typescript_engine_table_has_four_columns(self):
        line = next(line for line in ref.render(self.value).splitlines() if line.startswith('| [client-typescript::minimum-version]'))
        self.assertEqual(len(re.findall(r'(?<!\\)\|', line)), 5)
        self.assertIn(r'^22.0.0 \|\| ^24.0.0', line)
    def test_missing_case(self):self.value['cases'].pop();self.reject()
    def test_duplicate_case(self):self.value['cases'][0]=copy.deepcopy(self.value['cases'][1]);self.reject()
    def test_changed_command(self):self.value['cases'][0]['declared_command'].append('--foreign');self.reject()
    def test_source_identity_substitution(self):self.value['cases'][0]['source_sha256']='0'*64;self.reject()
    def test_candidate_substitution(self):self.value['candidate_digest']='sha256:'+'0'*64;self.reject()
    def test_runtime_promotion(self):self.value['new_runtime_executions']=1;self.reject()
    def test_credit_promotion(self):self.value['new_qualification_credit']=1;self.reject()
    def test_whole_contract_promotion(self):self.value['cases'][0]['whole_contract_verified']=True;self.reject()
    def test_complete_history_promotion(self):self.value['historical_inventory_complete']=True;self.reject()
    def test_frozen_reference_promotion(self):self.value['frozen_reference']=True;self.reject()
    def test_metadata_as_offline_execution(self):self.row('client-rust::offline-locked-install')['assertion_depth']='ACTUAL_OFFLINE_INSTALL';self.reject()
    def test_snapshot_as_sqlite_race(self):self.row('client-typescript::process-crash-restart')['assertion_depth']='SQLITE_CRASH_AND_TWO_PROCESS_TERMINAL_RACE';self.reject()
    def test_config_schema_as_semver(self):self.row('client-rust::unsupported-version')['assertion_depth']='VERSION_CLASSIFIER_POSITIVE_AND_NEGATIVE';self.reject()
    def test_private_marker(self):self.value['limits'].append('/Users/synthetic-marker/private-capture');self.reject()
    def test_extra_unreviewed_field(self):self.value['unreviewed_claim']='synthetic';self.reject()
    def test_noop_negative_helper_refused(self):
        with self.assertRaisesRegex(AssertionError, 'negative control must change'):
            self.reject()

if __name__ == '__main__':unittest.main()
