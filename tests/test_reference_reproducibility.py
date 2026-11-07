import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import reference_reproducibility as r

class ReferenceReproducibilityTests(unittest.TestCase):
    def setUp(self):self.v=r.load()
    def reject(self,mutate):
        mutate(self.v)
        with self.assertRaises(Exception):r.validate(self.v)
    def test_positive_integrity(self):self.assertTrue(r.check())
    def test_deterministic_render(self):self.assertEqual(r.render(self.v),r.render(copy.deepcopy(self.v)))
    def test_original_candidate(self):self.reject(lambda v:v.update(candidate_manifest_sha256='sha256:'+'0'*64))
    def test_no_credit(self):self.reject(lambda v:v.update(qualification_credit=1))
    def test_no_execution(self):self.reject(lambda v:v.update(new_runtime_executions=1))
    def test_no_freeze(self):self.reject(lambda v:v.update(baseline_frozen=True))
    def test_no_authority(self):self.reject(lambda v:v.update(execution_authorized=True))
    def test_no_history_complete(self):self.reject(lambda v:v.update(historical_inventory_complete=True))
    def test_no_whole_capability(self):self.reject(lambda v:v.update(whole_capability_completion=True))
    def test_duplicate_link(self):self.reject(lambda v:v['links'].__setitem__(1,copy.deepcopy(v['links'][0])))
    def test_missing_link(self):self.reject(lambda v:v['links'].pop())
    def test_unknown_link_property(self):self.reject(lambda v:v['links'][0].update(unsupported_claim=True))
    def test_duplicate_obligation(self):self.reject(lambda v:v['obligations'].__setitem__(1,copy.deepcopy(v['obligations'][0])))
    def test_missing_obligation(self):self.reject(lambda v:v['obligations'].pop())
    def test_dangling_obligation(self):self.reject(lambda v:v['links'][0].update(obligation_id='synthetic:unknown'))
    def test_unresolved_slice(self):self.reject(lambda v:v['links'][0].update(slice_id='synthetic-unknown'))
    def test_wrong_base_slice(self):self.reject(lambda v:v['links'][0].update(base_slice_node='ordinary-witness:other'))
    def test_missing_review(self):self.reject(lambda v:v['links'][0].update(review_refs=[]))
    def test_missing_scope(self):self.reject(lambda v:v['links'][0].update(scope_limit_count=0))
    def test_missing_source(self):self.reject(lambda v:v['obligations'][0].update(source_refs=[]))
    def test_contract_promotion(self):self.reject(lambda v:v['obligations'][0].update(whole_contract_satisfied=True))
    def test_link_contract_promotion(self):self.reject(lambda v:v['links'][0].update(whole_contract_satisfied=True))
    def test_link_credit(self):self.reject(lambda v:v['links'][0].update(new_qualification_credit=1))
    def test_link_runtime(self):self.reject(lambda v:v['links'][0].update(fresh_runtime_execution=True))
    def test_context_is_not_original_execution(self):self.reject(lambda v:v['links'][0].update(base_context_is_original_execution_proof=True))
    def test_role_promotion(self):self.reject(lambda v:v['links'][0].update(evidence_role='REUSED_REVIEWED_BOUNDED_RUNTIME_ASSERTION'))
    def test_gap_as_pass(self):
        row=next(x for x in self.v['links'] if x['evidence_role']=='GAP_CONTEXT_NOT_GLOBAL_ABSENCE')
        row['status']='VERIFIED_BOUNDED_OBSERVATION'
        with self.assertRaises(Exception):r.validate(self.v)
    def test_analytical_as_additional_observation(self):
        row=next(x for x in self.v['links'] if x['evidence_role']=='ANALYTICAL_REUSE_NOT_ADDITIONAL_OBSERVATION')
        row['observation_refs']=copy.deepcopy(row['review_refs'])
        with self.assertRaises(Exception):r.validate(self.v)
    def test_polarity_tamper(self):self.reject(lambda v:v['links'][0].update(polarity='POSITIVE_CONTROL'))
    def test_scope_tamper(self):self.reject(lambda v:v['links'][0]['supported_scope'].update(existing_status='PASS'))
    def test_pointer_tamper(self):self.reject(lambda v:v['links'][0]['scope_limit_ref'].update(json_pointer='/unknown'))
    def test_source_digest_tamper(self):self.reject(lambda v:v['obligations'][0]['source_refs'][0].update(retained_input_sha256='0'*64))
    def test_duplicate_artifact(self):self.reject(lambda v:v['artifact_readiness']['records'].__setitem__(1,copy.deepcopy(v['artifact_readiness']['records'][0])))
    def test_missing_artifact(self):self.reject(lambda v:v['artifact_readiness']['records'].pop())
    def test_false_available(self):
        row=next(x for x in self.v['artifact_readiness']['records'] if x['verified_copy_count']==0)
        row['availability']='AVAILABLE_AND_BYTE_VERIFIED_AT_EXAMINED_LOCATOR'
        with self.assertRaises(Exception):r.validate(self.v)
    def test_copies_as_artifacts(self):self.reject(lambda v:v['artifact_readiness'].update(artifacts_byte_verified=16))
    def test_wrong_observation_count(self):self.reject(lambda v:v['artifact_readiness'].update(locator_observations=38))
    def test_no_custody_inference(self):self.reject(lambda v:v['artifact_readiness'].update(original_custody_established=True))
    def test_no_reproduction_inference(self):self.reject(lambda v:v['artifact_readiness'].update(full_reproducibility_established=True))
    def test_no_archive_execution(self):self.reject(lambda v:v['artifact_readiness'].update(archive_extraction=True))
    def test_no_product_execution(self):self.reject(lambda v:v['artifact_readiness'].update(workload_executed=True))
    def test_no_global_loss_claim(self):self.reject(lambda v:v['artifact_readiness']['records'][0].update(availability='GLOBALLY_LOST'))
    def test_lineage_not_dropped(self):self.reject(lambda v:v['retained_lineage'].pop())
    def test_unknown_claim(self):self.reject(lambda v:v.update(independent_interoperability=True))
    def test_private_locator_refused(self):self.reject(lambda v:v.update(private_locator='/Users/synthetic/private'))
    def test_unknown_nested_claim(self):self.reject(lambda v:v['artifact_readiness'].update(performance_superiority=True))
    def test_no_boolean_credit(self):self.reject(lambda v:v.update(qualification_credit=False))

if __name__=='__main__':unittest.main()
