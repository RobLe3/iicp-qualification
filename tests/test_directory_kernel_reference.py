"""Offline derivative controls; never execute product methods or a database."""
from pathlib import Path
from unittest.mock import patch
import copy
import json
import sys
import tempfile
import unittest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import directory_kernel_reference as reference

class DirectoryKernelReference(unittest.TestCase):
    def setUp(self):
        self.value = reference.load()

    def reject(self, change):
        change(self.value)
        with self.assertRaises((ValueError, ValidationError)):
            reference.validate(self.value)

    def test_positive_schema(self):
        Draft202012Validator.check_schema(json.loads((reference.DATA/'observations.schema.json').read_bytes()))
        self.assertTrue(reference.validate(self.value))

    def test_package_integrity_and_narrative(self):
        self.assertEqual(reference.check_package(), self.value)

    def test_deterministic_render(self):
        self.assertEqual(reference.render(self.value), reference.render(copy.deepcopy(self.value)))

    def test_profiles_keep_distinct_execution_units(self):
        self.assertEqual([(p['passing_distinct_methods'],p['method_executions'],p['failed_method_executions'])
                         for p in self.value['execution_profiles']],[(4,5,1),(3,3,0),(1,1,0)])
        self.assertEqual(len(self.value['methods']),8)
        self.assertEqual(len(self.value['attempt_history']),9)

    def test_my_sql_refusals_are_not_six_methods(self):
        mysql = [r for r in self.value['methods'] if r['profile_id']=='rust-mysql']
        self.assertEqual(len(mysql),1)
        self.assertIn('six invalid',mysql[0]['assertions'][1])

    def test_no_whole_platform_or_performance_claim(self):
        text=reference.render(self.value)
        self.assertIn('not a matched platform comparison',text)
        self.assertIn('not crash/restart or disk durability',text)

    def test_missing_method(self): self.reject(lambda x:x['methods'].pop())
    def test_duplicate_method(self): self.reject(lambda x:x['methods'].__setitem__(1,copy.deepcopy(x['methods'][0])))
    def test_reordered_methods(self): self.reject(lambda x:x['methods'].reverse())
    def test_foreign_component(self): self.reject(lambda x:x['execution_profiles'][0].__setitem__('component','management'))
    def test_foreign_source(self): self.reject(lambda x:x['source_metadata'][0].__setitem__('commit','0'*40))
    def test_altered_source_digest(self): self.reject(lambda x:x['source_metadata'][0].__setitem__('sha256','0'*64))
    def test_missing_source_digest(self): self.reject(lambda x:x['source_metadata'][0].pop('sha256'))
    def test_foreign_source_url(self): self.reject(lambda x:x['source_metadata'][0].__setitem__('url','https://example.invalid'))
    def test_missing_review(self): self.reject(lambda x:x['evidence'].pop(1))
    def test_altered_private_pin(self): self.reject(lambda x:x['evidence'][0].__setitem__('sha256','0'*64))
    def test_original_bytes_public(self): self.reject(lambda x:x['evidence'][0].__setitem__('original_bytes_public',True))
    def test_missing_private_fixture_pin(self): self.reject(lambda x:x['evidence'].pop())
    def test_erased_failed_oracle(self): self.reject(lambda x:x['attempt_history'].pop(2))
    def test_failed_oracle_relabelled(self): self.reject(lambda x:x['attempt_history'][2].__setitem__('outcome','PASS'))
    def test_unchanged_originals_repeated(self): self.reject(lambda x:x['execution_profiles'][0].__setitem__('method_executions',8))
    def test_six_refusals_counted_as_methods(self): self.reject(lambda x:x['execution_profiles'][2].__setitem__('passing_distinct_methods',6))
    def test_setup_counted_as_method(self): self.reject(lambda x:x['attempt_history'][0].__setitem__('method_executions',1))
    def test_successor_lineage_missing(self): self.reject(lambda x:x['attempt_history'][-1].__setitem__('predecessor',None))
    def test_successor_cycle(self): self.reject(lambda x:x['attempt_history'][-1].__setitem__('predecessor','rust-retained-elf-successor'))
    def test_old_topology_relabelled(self): self.reject(lambda x:x['attempt_history'][6].__setitem__('outcome','PASS'))
    def test_compiler_failure_invented(self): self.reject(lambda x:x['attempt_history'][7].__setitem__('outcome','COMPILER_FAILED'))
    def test_method_origin_relabelled(self): self.reject(lambda x:x['methods'][-1].__setitem__('origin','ORIGINAL_FROZEN'))
    def test_backend_equivalence_invented(self): self.reject(lambda x:x['execution_profiles'][0].__setitem__('backend','MySQL'))
    def test_runtime_invented(self): self.reject(lambda x:x['execution_profiles'][1].__setitem__('runtime','all platforms'))
    def test_unknown_assertion(self): self.reject(lambda x:x['methods'][-1]['assertions'].append('all behavior qualified'))
    def test_bool_credit(self): self.reject(lambda x:x.__setitem__('qualification_credit',False))
    def test_float_credit(self): self.reject(lambda x:x.__setitem__('qualification_credit',0.0))
    def test_bool_count(self): self.reject(lambda x:x['execution_profiles'][2].__setitem__('method_executions',True))
    def test_float_count(self): self.reject(lambda x:x['attempt_history'][-1].__setitem__('methods_passed',1.0))
    def test_credit_inflation(self): self.reject(lambda x:x.__setitem__('qualification_credit',1))
    def test_workload_invention(self): self.reject(lambda x:x.__setitem__('qualification_workload_executed',True))
    def test_accepted_evidence_change(self): self.reject(lambda x:x.__setitem__('canonical_evidence_changed',True))
    def test_whole_capability(self): self.reject(lambda x:x.__setitem__('whole_capability_complete',True))
    def test_successor_freeze(self): self.reject(lambda x:x.__setitem__('successor_frozen',True))
    def test_complete_history(self): self.reject(lambda x:x.__setitem__('historical_inventory_complete',True))
    def test_external_interoperability(self): self.reject(lambda x:x.__setitem__('independent_interoperability_established',True))
    def test_crash_durability(self): self.reject(lambda x:x.__setitem__('crash_durability_verified',True))
    def test_real_http_tls(self): self.reject(lambda x:x.__setitem__('real_http_tls_verified',True))
    def test_private_evidence(self): self.reject(lambda x:x.__setitem__('private_evidence_included',True))
    def test_private_path(self): self.reject(lambda x:x['limits'].__setitem__(0,'/Users/SYNTHETIC/private'))
    def test_account_shape(self): self.reject(lambda x:x['limits'].__setitem__(0,'Synthetic account 123456789012'))
    def test_unknown_authority_field(self): self.reject(lambda x:x.__setitem__('qualification_authority',True))
    def test_missing_limitation(self): self.reject(lambda x:x['limits'].pop())

    def test_reviewed_snapshot_does_not_replace_independent_accounting(self):
        self.value['attempt_history'][-1]['method_executions']=2
        changed=copy.deepcopy(reference.REVIEWED)
        changed['attempt_history']=copy.deepcopy(self.value['attempt_history'])
        with patch.object(reference,'REVIEWED',changed):
            with self.assertRaisesRegex(ValueError,'ATTEMPT_ACCOUNTING'):
                reference.validate(self.value)

    def test_modified_readme_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)
            for f in reference.DATA.iterdir():
                if f.is_file():(target/f.name).write_bytes(f.read_bytes())
            (target/'README.md').write_text('Unsupported narrative')
            with patch.object(reference,'DATA',target):
                with self.assertRaisesRegex(ValueError,'STALE_GENERATED_NARRATIVE'):
                    reference.check_package()

    def test_modified_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)
            for f in reference.DATA.iterdir():
                if f.is_file():(target/f.name).write_bytes(f.read_bytes())
            (target/'manifest.json').write_text('{}')
            with patch.object(reference,'DATA',target):
                with self.assertRaisesRegex(ValueError,'MANIFEST_MISMATCH'):
                    reference.check_package()

if __name__=='__main__':
    unittest.main()
