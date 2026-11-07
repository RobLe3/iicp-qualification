"""Offline snapshot and semantic-replay controls; no product or database launch."""
from pathlib import Path
from unittest.mock import patch
import copy
import json
import sys
import tempfile
import unittest
from jsonschema import Draft202012Validator,ValidationError
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import capability_assertion_reference as reference

class CapabilityAssertions(unittest.TestCase):
    def setUp(self):self.value=reference.load();self.vectors=copy.deepcopy(self.value['vectors'])
    def reject(self,change):
        change(self.value)
        with self.assertRaises((ValueError,ValidationError)):reference.validate(self.value)
    def replay_reject(self,change):
        change(self.vectors)
        with self.assertRaises(ValueError):reference.replay_vectors(self.vectors)
    def test_authorized_positive_vectors(self):self.assertTrue(reference.replay_vectors(self.vectors))
    def test_schema_valid(self):
        Draft202012Validator.check_schema(json.loads((reference.DATA/'assertions.schema.json').read_bytes()))
        self.assertTrue(reference.validate(self.value))
    def test_generated_package(self):self.assertEqual(reference.check_package(),self.value)
    def test_deterministic_render(self):self.assertEqual(reference.render(self.value),reference.render(copy.deepcopy(self.value)))
    def test_selected_units_and_not_new_gates(self):
        self.assertEqual(len(self.value['rows']),36);self.assertEqual(self.value['assertion_ids'],12)
        self.assertEqual(sorted(self.value['counts'].values()),[3,14,19]);self.assertFalse(self.value['new_qualification_gates_defined'])
    def test_gap_is_not_a_defect_or_pass(self):
        rows=[r for r in self.value['rows'] if '.IDLESS.' in r['assertion_id']]
        self.assertEqual(len(rows),6);self.assertTrue(all(r['status']=='NOT_EXERCISED_IN_SELECTED_WITNESSES' for r in rows))
    def test_unknown_required_and_union_unexercised(self):
        rows=[r for r in self.value['rows'] if r['assertion_id'].endswith('RETAIN-OR-REFUSE') or r['assertion_id'].endswith('NO-CROSS-VARIANT-UNION')]
        self.assertEqual(len(rows),6);self.assertTrue(all(r['status']=='NOT_EXERCISED_IN_SELECTED_WITNESSES' for r in rows))
    def test_no_positive_capabilities_cannot_pass_denials_only(self):self.replay_reject(lambda v:v.__setitem__('observed_detail_capabilities',[]))
    def test_missing_discovery_positive(self):self.replay_reject(lambda v:v.__setitem__('observed_discovery_capabilities',[]))
    def test_duplicate_variants_refused(self):self.replay_reject(lambda v:v['observed_detail_capabilities'].__setitem__(1,copy.deepcopy(v['observed_detail_capabilities'][0])))
    def test_variant_order_semantic(self):
        self.vectors['observed_detail_capabilities'].reverse();self.assertTrue(reference.replay_vectors(self.vectors))
    def test_string_set_order_semantic(self):
        self.vectors['observed_detail_capabilities'][1]['features'].reverse();self.assertTrue(reference.replay_vectors(self.vectors))
    def test_duplicate_set_members_refused(self):self.replay_reject(lambda v:v['observed_detail_capabilities'][1].__setitem__('features',['tool_calling','tool_calling']))
    def test_numeric_representation_semantic(self):
        self.vectors['observed_detail_capabilities'][0]['limits']['context_tokens']['value']=8192
        self.assertTrue(reference.replay_vectors(self.vectors))
    def test_wrong_numeric_value(self):self.replay_reject(lambda v:v['observed_detail_capabilities'][0]['limits']['context_tokens'].__setitem__('value',8191))
    def test_bool_is_not_numeric_value(self):self.replay_reject(lambda v:v['observed_detail_capabilities'][0]['limits']['context_tokens'].__setitem__('value',True))
    def test_bool_phase_is_not_integer(self):self.replay_reject(lambda v:v['observed_detail_capabilities'][0].__setitem__('phase',True))
    def test_wrong_unit(self):self.replay_reject(lambda v:v['observed_detail_capabilities'][0]['limits']['context_tokens'].__setitem__('unit','bytes'))
    def test_extension_payload_lost(self):self.replay_reject(lambda v:v['observed_detail_capabilities'][1]['extensions']['org.example.optional-batching'].pop('value'))
    def test_extension_flag_changed(self):self.replay_reject(lambda v:v['observed_detail_capabilities'][1]['extensions']['org.example.optional-batching'].__setitem__('required',True))
    def test_expected_values_cannot_recalibrate(self):self.replay_reject(lambda v:v['expected_capabilities'][0]['limits']['context_tokens'].__setitem__('value',8191))
    def test_missing_refusal(self):self.replay_reject(lambda v:v['observed_refusals'].pop())
    def test_wrong_refusal_class(self):self.replay_reject(lambda v:v['observed_refusals'][0].__setitem__('error_code','unknown'))
    def test_wrong_refusal_status(self):self.replay_reject(lambda v:v['observed_refusals'][0].__setitem__('status',201))
    def test_float_refusal_status(self):self.replay_reject(lambda v:v['observed_refusals'][0].__setitem__('status',422.0))
    def test_changed_stored_rows(self):self.replay_reject(lambda v:v['observed_refusals'][0].__setitem__('row_counts',[2,2]))
    def test_bool_stored_count(self):self.replay_reject(lambda v:v['observed_refusals'][0].__setitem__('row_counts',[True,2]))
    def test_php_empty_float_status(self):self.replay_reject(lambda v:v['observed_php_empty'].__setitem__('status',422.0))
    def test_php_empty_count_changed(self):self.replay_reject(lambda v:v['observed_php_empty'].__setitem__('node_count_after',1))
    def test_php_empty_bool_count(self):self.replay_reject(lambda v:v['observed_php_empty'].__setitem__('node_count_after',False))
    def test_missing_row(self):self.reject(lambda x:x['rows'].pop())
    def test_duplicate_row(self):self.reject(lambda x:x['rows'].__setitem__(1,copy.deepcopy(x['rows'][0])))
    def test_unexercised_promoted(self):
        row=next(r for r in self.value['rows'] if r['status']=='NOT_EXERCISED_IN_SELECTED_WITNESSES')
        self.assertNotEqual(row['status'],'VERIFIED_BOUNDED_OBSERVATION')
        row['status']='VERIFIED_BOUNDED_OBSERVATION'
        with self.assertRaises(ValueError):reference.validate(self.value)
    def test_changed_authority_lines(self):self.reject(lambda x:x['rows'][0].__setitem__('authority_lines',[1,1]))
    def test_foreign_protocol(self):self.reject(lambda x:x.__setitem__('protocol_commit','0'*40))
    def test_foreign_source_hash(self):self.reject(lambda x:x['source_metadata'][0].__setitem__('sha256','0'*64))
    def test_missing_evidence(self):self.reject(lambda x:x['evidence'].pop())
    def test_qualification_credit(self):self.reject(lambda x:x.__setitem__('qualification_credit',1))
    def test_new_qualification_gates(self):self.reject(lambda x:x.__setitem__('new_qualification_gates_defined',True))
    def test_complete_history(self):self.reject(lambda x:x.__setitem__('historical_inventory_complete',True))
    def test_successor_freeze(self):self.reject(lambda x:x.__setitem__('successor_frozen',True))
    def test_interoperability_claim(self):self.reject(lambda x:x.__setitem__('independent_interoperability_established',True))
    def test_private_path(self):self.reject(lambda x:x['limits'].__setitem__(0,'/Users/SYNTHETIC/private'))
    def test_raw_private_evidence(self):self.reject(lambda x:x.__setitem__('private_raw_evidence_included',True))
    def test_unknown_authority(self):self.reject(lambda x:x.__setitem__('authority','canonical'))
    def test_edited_markdown_refused(self):
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)
            for f in reference.DATA.iterdir():
                if f.is_file():(target/f.name).write_bytes(f.read_bytes())
            (target/'README.md').write_text('Unsupported claim')
            with patch.object(reference,'DATA',target):
                with self.assertRaisesRegex(ValueError,'STALE_GENERATED_NARRATIVE'):reference.check_package()
    def test_altered_schema_refused(self):
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)
            for f in reference.DATA.iterdir():
                if f.is_file():(target/f.name).write_bytes(f.read_bytes())
            (target/'assertions.schema.json').write_text('{}')
            with patch.object(reference,'DATA',target):
                with self.assertRaisesRegex(ValueError,'REVIEWED_SCHEMA_IDENTITY'):reference.validate(self.value)

if __name__=='__main__':unittest.main()
