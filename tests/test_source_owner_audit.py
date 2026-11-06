"""Informative snapshot integrity is not qualification acceptance."""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

import jsonschema

ROOT = Path(__file__).resolve().parents[1] / 'reports/postcert/2026-11-06-source-owner-audit'


def safe_public(value):
    text = json.dumps(value, ensure_ascii=False)
    forbidden = (r'/Users/', r'/home/', r'arn:aws:', r'\b\d{12}\b', r'AKIA[0-9A-Z]{16}', r'-----BEGIN .*PRIVATE KEY-----')
    if any(re.search(pattern, text) for pattern in forbidden):
        raise ValueError('private marker in informative public derivative')


class SourceOwnerAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'source-analysis.json').read_bytes())
        cls.schema = json.loads((ROOT / 'schema.json').read_bytes())
        cls.validator = jsonschema.Draft202012Validator(cls.schema)

    def rejected(self, changed):
        with self.assertRaises(jsonschema.ValidationError):
            self.validator.validate(changed)

    def test_positive_schema_and_privacy(self):
        jsonschema.Draft202012Validator.check_schema(self.schema)
        self.validator.validate(self.data)
        safe_public(self.data)

    def test_manifest_members(self):
        manifest = json.loads((ROOT / 'manifest.json').read_bytes())
        self.assertEqual({row['path'] for row in manifest['files']}, {'README.md', 'source-analysis.json', 'schema.json'})
        for row in manifest['files']:
            path = ROOT / row['path']
            self.assertFalse(path.is_symlink())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row['sha256'])

    def test_counts_are_source_paths_not_defects(self):
        self.assertEqual(sum(x['range_commit_count'] for x in self.data['components']), 42)
        self.assertEqual(sum(x['net_changed_path_count'] for x in self.data['components']), 39)
        self.assertEqual(sum(x['net_src_path_count'] for x in self.data['components']), 6)
        for row in self.data['components']:
            self.assertEqual(row['net_changed_path_count'], len(row['paths']))
            self.assertEqual(row['net_src_path_count'], sum('PRODUCT_RUNTIME_SOURCE' in p['path_roles'] for p in row['paths']))

    def test_unknown_top_level_refused(self):
        data = copy.deepcopy(self.data); data['new_authority'] = True
        self.rejected(data)

    def test_foreign_source_refused(self):
        data = copy.deepcopy(self.data); data['components'][0]['qualified_source'] = 'a' * 40
        self.rejected(data)

    def test_duplicate_component_refused(self):
        data = copy.deepcopy(self.data); data['components'][0] = copy.deepcopy(data['components'][1])
        self.rejected(data)

    def test_credit_inflation_refused(self):
        data = copy.deepcopy(self.data); data['qualification_credit_added'] = 1
        self.rejected(data)

    def test_complete_defect_audit_claim_refused(self):
        data = copy.deepcopy(self.data); data['supported_scope_defect_audit_complete'] = True
        self.rejected(data)

    def test_issue_closure_claim_refused(self):
        data = copy.deepcopy(self.data); data['owner_findings'][0]['owner_contract_complete'] = True
        self.rejected(data)

    def test_external_interoperability_claim_refused(self):
        data = copy.deepcopy(self.data); data['external_interoperability_established'] = True
        self.rejected(data)

    def test_artifact_equivalence_claim_refused(self):
        data = copy.deepcopy(self.data); data['components'][0]['artifact_equivalence_established'] = True
        self.rejected(data)

    def test_private_locator_field_refused(self):
        data = copy.deepcopy(self.data); data['owner_findings'][0]['source_location'] = '/Users/synthetic/marker'
        self.rejected(data)

    def test_private_marker_in_allowed_prose_refused(self):
        data = copy.deepcopy(self.data); data['limits'][0] = '/Users/synthetic/marker'
        with self.assertRaises(ValueError): safe_public(data)

    def test_missing_review_reference_refused(self):
        data = copy.deepcopy(self.data); del data['review_digests']['owner_boundaries']
        self.rejected(data)

    def test_synthetic_evidence_cannot_gain_credit(self):
        data = copy.deepcopy(self.data); data['owner_findings'][0]['new_qualification_credit'] = 1
        self.rejected(data)

    def test_unknown_role_refused(self):
        data = copy.deepcopy(self.data); data['components'][0]['paths'][0]['path_roles'] = ['QUALIFIED_UNIVERSALLY_SAFE']
        self.rejected(data)

    def test_qualification_execution_authority_refused(self):
        data = copy.deepcopy(self.data); data['qualification_execution_authorized'] = True
        self.rejected(data)

    def test_successor_freeze_claim_refused(self):
        data = copy.deepcopy(self.data); data['successor_frozen'] = True
        self.rejected(data)
