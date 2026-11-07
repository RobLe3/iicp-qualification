"""Public metadata controls only; do not execute private SDK cases."""
from pathlib import Path
import copy
import json
import sys
import unittest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import sdk_caller_reference as reference

class CallerReference(unittest.TestCase):
    def setUp(self):
        self.value = reference.load()

    def reject(self, change):
        change(self.value)
        with self.assertRaises((ValueError, ValidationError)):
            reference.validate(self.value)

    def test_positive_schema(self):
        Draft202012Validator.check_schema(json.loads((reference.DATA / 'observations.schema.json').read_bytes()))
        self.assertTrue(reference.validate(self.value))

    def test_package_integrity_and_generated_narrative(self):
        self.assertEqual(reference.check_package(), self.value)

    def test_render_deterministic(self):
        self.assertEqual(reference.render(self.value), reference.render(copy.deepcopy(self.value)))

    def test_actual_case_matrix_counts(self):
        rows = self.value['case_outcomes']
        self.assertEqual(len(rows), 15)
        for sdk in reference.SDKS:
            selected = [r for r in rows if r['sdk'] == sdk]
            self.assertEqual(len(selected), 5)
            self.assertEqual(sum(r['post_calls'] for r in selected), 3)
            self.assertEqual(sum(r['error_code'] is not None for r in selected), 2)

    def test_missing_case(self): self.reject(lambda x: x['case_outcomes'].pop())
    def test_duplicate_case(self): self.reject(lambda x: x['case_outcomes'].__setitem__(1, copy.deepcopy(x['case_outcomes'][0])))
    def test_reordered_case(self): self.reject(lambda x: x['case_outcomes'].reverse())
    def test_foreign_sdk(self): self.reject(lambda x: x['case_outcomes'][0].__setitem__('sdk', 'management'))
    def test_wrong_selection(self): self.reject(lambda x: x['case_outcomes'][0].__setitem__('selected', 'a'))
    def test_denied_dispatch(self): self.reject(lambda x: x['case_outcomes'][2].__setitem__('post_calls', 1))
    def test_empty_set_ranker_called(self): self.reject(lambda x: x['case_outcomes'][3].__setitem__('ranker_calls', 1))
    def test_wrong_refusal(self): self.reject(lambda x: x['case_outcomes'][2].__setitem__('error_code', 'UNKNOWN'))
    def test_missing_nullable_error(self): self.reject(lambda x: x['case_outcomes'][0].pop('error_code'))
    def test_missing_nullable_selection(self): self.reject(lambda x: x['case_outcomes'][2].pop('selected'))
    def test_bool_count(self): self.reject(lambda x: x['case_outcomes'][0].__setitem__('get_calls', True))
    def test_float_count(self): self.reject(lambda x: x['case_outcomes'][0].__setitem__('post_calls', 1.0))
    def test_bool_credit(self): self.reject(lambda x: x.__setitem__('qualification_credit', False))
    def test_float_credit(self): self.reject(lambda x: x.__setitem__('qualification_credit', 0.0))
    def test_wrong_source_revision(self): self.reject(lambda x: x['source_metadata'][0].__setitem__('commit', '0' * 40))
    def test_wrong_source_digest(self): self.reject(lambda x: x['source_metadata'][0].__setitem__('sha256', '0' * 64))
    def test_missing_source_digest(self): self.reject(lambda x: x['source_metadata'][0].pop('sha256'))
    def test_wrong_source_url(self): self.reject(lambda x: x['source_metadata'][0].__setitem__('url', 'https://example.invalid'))
    def test_duplicate_source(self): self.reject(lambda x: x['source_metadata'].__setitem__(1, copy.deepcopy(x['source_metadata'][0])))
    def test_altered_private_evidence_digest(self): self.reject(lambda x: x['evidence'].__setitem__('matrix_sha256', '0' * 64))
    def test_erased_failed_attempt(self): self.reject(lambda x: x['attempt_history'].pop(1))
    def test_failure_relabelled_pass(self): self.reject(lambda x: x['attempt_history'][1].__setitem__('outcome', 'PASS'))
    def test_successor_lineage_dropped(self): self.reject(lambda x: x['attempt_history'][2].__setitem__('supersedes', None))
    def test_successor_cycle(self): self.reject(lambda x: x['attempt_history'][2].__setitem__('supersedes', x['attempt_history'][2]['attempt_id']))
    def test_attempt_case_inflation(self): self.reject(lambda x: x['attempt_history'][1].__setitem__('actual_case_outcomes_pass', 5))
    def test_float_attempt_count(self): self.reject(lambda x: x['attempt_history'][0].__setitem__('actual_case_outcomes_pass', 5.0))
    def test_credit(self): self.reject(lambda x: x.__setitem__('qualification_credit', 1))
    def test_qualification_run(self): self.reject(lambda x: x.__setitem__('qualification_workload_executed', True))
    def test_whole_capability(self): self.reject(lambda x: x.__setitem__('whole_capability_complete', True))
    def test_successor_freeze(self): self.reject(lambda x: x.__setitem__('successor_frozen', True))
    def test_complete_history(self): self.reject(lambda x: x.__setitem__('historical_inventory_complete', True))
    def test_independent_interoperability(self): self.reject(lambda x: x.__setitem__('independent_interoperability_established', True))
    def test_provider_transport_invention(self): self.reject(lambda x: x.__setitem__('real_provider_transport_verified', True))
    def test_restricted_auth_invention(self): self.reject(lambda x: x.__setitem__('restricted_or_ticketed_auth_exercised', True))
    def test_response_encryption_invention(self): self.reject(lambda x: x.__setitem__('encrypted_responses_exercised', True))
    def test_private_artifact_inclusion(self): self.reject(lambda x: x.__setitem__('private_evidence_included', True))
    def test_original_environment_equivalence(self): self.reject(lambda x: x.__setitem__('qualified_environment_equivalence', True))
    def test_toolchain_relabelled(self): self.reject(lambda x: x['execution_profiles'][0].__setitem__('runtime', 'CPython 3.13'))
    def test_host_scope_expanded(self): self.reject(lambda x: x.__setitem__('host_scope', 'ALL_FOUR_PLATFORMS'))
    def test_private_path(self): self.reject(lambda x: x['limits'].__setitem__(0, '/Users/SYNTHETIC/private'))
    def test_account_shape(self): self.reject(lambda x: x['limits'].__setitem__(0, 'Synthetic account 123456789012'))
    def test_privacy_marker_specific(self):
        self.value['limits'][0] = '/Users/SYNTHETIC/private'
        with self.assertRaisesRegex(ValueError, 'PRIVATE_MARKER'):
            reference.validate(self.value)

    def test_unknown_authority_field(self): self.reject(lambda x: x.__setitem__('acceptance_authority', True))

if __name__ == '__main__':
    unittest.main()
