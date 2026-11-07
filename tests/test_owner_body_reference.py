import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from jsonschema import ValidationError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import owner_body_reference as ref

class OwnerBodyReferenceTests(unittest.TestCase):
    def setUp(self):self.value=ref.load();self.original=copy.deepcopy(self.value)
    def reject(self):
        self.assertNotEqual(ref.canonical(self.value),ref.canonical(self.original),'negative control must change the reviewed representation')
        with self.assertRaises((ValueError,ValidationError)):ref.validate(self.value)
    def test_positive_reviewed_snapshot(self):self.assertTrue(ref.validate(self.value))
    def test_positive_package_and_generated_readme(self):self.assertTrue(ref.check())
    def test_counts_are_snapshot_not_defects(self):
        self.assertEqual(len(self.value['owners']),276)
        self.assertEqual(self.value['distinct_defect_count'],'NOT_ESTABLISHED')
        self.assertFalse(self.value['all_six_supported_defect_clearance'])
    def test_deterministic_render(self):self.assertEqual(ref.render(self.value),ref.render(copy.deepcopy(self.value)))
    def test_all_six_component_counts(self):self.assertEqual(sum(x['closed_records'] for x in self.value['source_snapshots']),261)
    def test_missing_owner(self):self.value['owners'].pop();self.reject()
    def test_duplicate_owner(self):self.value['owners'][0]=copy.deepcopy(self.value['owners'][1]);self.reject()
    def test_foreign_repository(self):self.value['owners'][0]['owner_id']='Other/repo#1';self.reject()
    def test_wrong_owner_url(self):self.value['owners'][0]['url']='https://example.invalid/issues/1';self.reject()
    def test_changed_body_digest(self):self.value['owners'][0]['body_sha256']='sha256:'+'0'*64;self.reject()
    def test_missing_body_digest(self):del self.value['owners'][0]['body_sha256'];self.reject()
    def test_body_as_whole_acceptance(self):self.value['owners'][0]['whole_contract_status']='PASS';self.reject()
    def test_owner_as_qualification_credit(self):self.value['owners'][0]['qualification_credit']=1;self.reject()
    def test_body_class_change_requires_new_review(self):
        row=next(r for r in self.value['owners'] if r['problem_class']!='EVIDENCE_GAP')
        self.assertNotEqual(row['problem_class'],'EVIDENCE_GAP')
        row['problem_class']='EVIDENCE_GAP';self.reject()
    def test_negative_helper_refuses_a_noop_control(self):
        with self.assertRaisesRegex(AssertionError,'negative control must change'):
            self.reject()
    def test_state_change_not_silently_accepted(self):self.value['owners'][0]['owner_state']='OPEN';self.reject()
    def test_float_counters(self):self.value['counts']['closed_body_records']=261.0;self.reject()
    def test_wrong_closed_count(self):self.value['counts']['closed_body_records']=260;self.reject()
    def test_missing_component_snapshot(self):self.value['source_snapshots'].pop();self.reject()
    def test_duplicate_component_snapshot(self):self.value['source_snapshots'][0]=copy.deepcopy(self.value['source_snapshots'][1]);self.reject()
    def test_old_directory_source_identity(self):self.value['source_snapshots'][3]['qualified_source_commit']='633e018293b57691b9f2b9a4587f7726f88f9e53';self.reject()
    def test_history_complete_from_issue_bodies(self):self.value['historical_inventory_complete']=True;self.reject()
    def test_whole_supported_clearance_from_snapshot(self):self.value['all_six_supported_defect_clearance']=True;self.reject()
    def test_native_execution_from_source(self):self.value['new_runtime_validation']=True;self.reject()
    def test_missing_selected_correction(self):self.value['selected_corrections'].pop();self.reject()
    def test_duplicate_selected_correction(self):self.value['selected_corrections'][0]=copy.deepcopy(self.value['selected_corrections'][1]);self.reject()
    def test_development_fix_does_not_inherit_credit(self):
        row=next(r for r in self.value['selected_corrections'] if r['owner_id']=='RobLe3/iicp-client-python#145')
        row['disposition']='CORRECTION_SOURCE_IN_QUALIFIED_SOURCE';self.reject()
    def test_source_join_as_new_native_result(self):self.value['selected_corrections'][0]['new_native_validation']=True;self.reject()
    def test_source_join_as_whole_issue_clearance(self):self.value['selected_corrections'][0]['whole_issue_acceptance_verified']=True;self.reject()
    def test_foreign_qualified_source_url(self):self.value['selected_corrections'][0]['qualified_source_url']='https://example.invalid/source';self.reject()
    def test_wrong_candidate(self):self.value['candidate_digest']='sha256:'+'0'*64;self.reject()
    def test_suspected_mismatch_not_confirmed(self):
        next(r for r in self.value['owners'] if r['owner_id']=='RobLe3/iicp-directory-php#11')['problem_class']='OWNER_REPORTED_PRODUCT_DEFECT';self.reject()
    def test_clarity_change_not_runtime_defect(self):
        next(r for r in self.value['owners'] if r['owner_id']=='RobLe3/iicp-directory-php#60')['problem_class']='OWNER_REPORTED_PRODUCT_DEFECT';self.reject()
    def test_duplicate_source_body_not_reinterpreted(self):
        next(r for r in self.value['owners'] if r['owner_id']=='RobLe3/iicp-client-rust#4')['body_sha256']='sha256:'+'0'*64;self.reject()
    def test_private_path_refused(self):self.value['owners'][0]['assessment']='/Users/synthetic-marker/private-capture';self.reject()
    def test_private_credential_marker_refused(self):self.value['owners'][0]['assessment']='AWS_ACCESS_KEY_ID=SYNTHETIC_MARKER';self.reject()
    def test_account_shaped_synthetic_marker_refused(self):self.value['owners'][0]['assessment']='synthetic 123456789012 marker';self.reject()
    def test_unreviewed_extra_field_refused(self):self.value['owners'][0]['raw_capture']='synthetic';self.reject()
    def test_changed_prose_requires_new_identity(self):self.value['owners'][0]['assessment']+=' unsupported assurance';self.reject()
    def test_manifest_missing_member_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            data=Path(tmp);shutil.copytree(ref.DATA,data,dirs_exist_ok=True)
            p=data/'manifest.json';manifest=json.loads(p.read_text());del manifest['files']['README.md'];p.write_text(json.dumps(manifest))
            with patch.object(ref,'DATA',data),self.assertRaises(ValueError):ref.check()
    def test_generated_readme_drift_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            data=Path(tmp);shutil.copytree(ref.DATA,data,dirs_exist_ok=True);(data/'README.md').write_text('unreviewed')
            with patch.object(ref,'DATA',data),self.assertRaises(ValueError):ref.check()
if __name__=='__main__':unittest.main()
