"""Bounded supplement integrity/claim controls; not source or runtime proof."""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/postcert/2026-11-06-timeout-and-source-checkpoint'


def validate_map(data):
    if data['schema'] != 'iicp.postcert-timeout-source-checkpoint.v1':
        raise ValueError('schema')
    if data['qualified_candidate_manifest_sha256'] != 'sha256:e7c9aa192be21cdc5ee96e793ab97084137452653cde7580cffd22cf3890618a':
        raise ValueError('candidate')
    if type(data['new_runtime_executions']) is not int or data['new_runtime_executions'] != 0:
        raise ValueError('execution inflation')
    for flag in ['qualification_credit_changed','successor_qualified','independent_interoperability_established','programme_complete','private_review_and_index_publicly_retrievable']:
        if data[flag] is not False:
            raise ValueError('unsupported completion or public-access claim')
    rows = data['timeout_source_links']
    expected = {'client-python::request-timeout':96,'client-typescript::request-timeout':48,'client-rust::request-timeout':48}
    if len(rows) != 3 or {x['case_id'] for x in rows} != set(expected):
        raise ValueError('case identity or duplicate')
    for row in rows:
        if type(row['existing_accepted_coordinate_references']) is not int or row['existing_accepted_coordinate_references'] != expected[row['case_id']]:
            raise ValueError('coordinate count')
        for flag in ['catalog_obligation_complete','retry_safety_proven','provider_terminal_state_proven','performance_comparability_proven']:
            if row[flag] is not False:
                raise ValueError('claim inflation')
    if data['timeout_existing_coordinate_references'] != sum(expected.values()):
        raise ValueError('coordinate sum')
    frontier = data['bounded_source_review_frontier']
    if (frontier['reviewed_case_definitions'],frontier['remaining_case_definitions'],frontier['declared_case_definitions'],frontier['existing_coordinate_references']) != (26,121,147,1224):
        raise ValueError('bounded frontier accounting')
    if data['profile_context']['relationship'] != 'INDIRECT_NOT_COMPLETE_PROFILE_CONFORMANCE':
        raise ValueError('profile overclaim')
    for row in data['source_files']:
        if not re.fullmatch('[0-9a-f]{40}',row['commit']) or not re.fullmatch('[0-9a-f]{64}',row['sha256']):
            raise ValueError('source digest')
        if Path(row['path']).is_absolute() or '..' in Path(row['path']).parts:
            raise ValueError('source path')
    for row in data['merged_development_sources']:
        if 'source_versions_changed' in row or row.get('iicp_component_versions_changed') is not False:
            raise ValueError('ambiguous component version claim')
    required = {('RobLe3/IICP','pre1/feature-baseline-v1.json'),('RobLe3/iicp.network','project/pre1-edge-case-catalog.json')}
    if not required <= {(row['repository'],row['path']) for row in data['source_files']}:
        raise ValueError('missing authority pin')
    public = json.dumps(data)
    if any(marker in public for marker in ['/Users/','arn:aws:','AKIA','authorization.json']):
        raise ValueError('forbidden operational marker')
    return True


class TimeoutSourceCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((REPORT/'source-map.json').read_text())
    def test_actual_data_and_manifest_integrity(self):
        self.assertTrue(validate_map(self.data))
        manifest = json.loads((REPORT/'manifest.json').read_text())
        self.assertEqual({x['path'] for x in manifest['files']},{'README.md','source-map.json'})
        for row in manifest['files']:
            self.assertEqual(hashlib.sha256((REPORT/row['path']).read_bytes()).hexdigest(),row['sha256'])
    def test_candidate_substitution_rejected(self):
        self.data['qualified_candidate_manifest_sha256'] = 'sha256:'+'0'*64
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_duplicate_case_rejected(self):
        self.data['timeout_source_links'][1] = copy.deepcopy(self.data['timeout_source_links'][0])
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_retry_claim_rejected(self):
        self.data['timeout_source_links'][0]['retry_safety_proven'] = True
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_new_execution_claim_rejected(self):
        self.data['new_runtime_executions'] = 1
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_qualification_promotion_rejected(self):
        self.data['successor_qualified'] = True
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_wrong_coordinate_count_rejected(self):
        self.data['timeout_source_links'][0]['existing_accepted_coordinate_references'] += 1
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_private_path_rejected(self):
        self.data['source_files'][0]['path'] = '/Users/synthetic/private'
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_base_profile_scope_inflation_rejected(self):
        self.data['profile_context']['relationship'] = 'COMPLETE_BASE_CONFORMANCE'
        with self.assertRaises(ValueError):validate_map(self.data)

    def test_ambiguous_component_version_field_rejected(self):
        self.data['merged_development_sources'][0]['source_versions_changed'] = False
        with self.assertRaises(ValueError):validate_map(self.data)
    def test_missing_catalog_pin_rejected(self):
        self.data['source_files'] = [row for row in self.data['source_files'] if row['path'] != 'project/pre1-edge-case-catalog.json']
        with self.assertRaises(ValueError):validate_map(self.data)
