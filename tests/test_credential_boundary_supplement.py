"""Source-projection integrity and claim guards, not SDK runtime validation."""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

REPORT=Path(__file__).resolve().parents[1]/'reports/postcert/2026-11-06-credential-boundaries'
SCENARIOS={'credential-expired','credential-replayed','credential-rotated','signature-mismatch','credential-missing','directory-unavailable'}
ROLES={'client-python','client-typescript','client-rust'}


def _validate_crypto(row):
    if row['proof_kind']!='TEST_LOCAL_CRYPTO_POLICY_WITH_REAL_ED25519_LIBRARY':
        raise ValueError('crypto source scope')
    for key in ['production_sdk_validator_invoked','production_replay_store_tested',
                'new_credential_acceptance_tested','fixture_mutation_applied_to_live_state']:
        if row[key] is not False: raise ValueError('crypto production inflation')


def _validate_missing(row):
    if row['client_constructor_invoked'] is not (row['component']=='client-rust') or row['explicit_network_call_count_asserted'] is not False:
        raise ValueError('missing-secret assertion scope')


def _validate_unavailable(row):
    if row['transport_failure_exercised_by_fixture'] is not (row['component']!='client-rust'):
        raise ValueError('unavailable fixture scope')
    if row['configured_discovery_url_explicitly_asserted'] is not (row['component']=='client-python') or row['expected_request_count']!=1:
        raise ValueError('network assertion scope')


def _validate_row(row):
    if row['component']!=row['case_id'].split('::')[0]: raise ValueError('component')
    count=96 if row['component']=='client-python' else 48
    if type(row['existing_accepted_coordinates']) is not int or row['existing_accepted_coordinates']!=count:
        raise ValueError('coordinates')
    for key in ['raw_runtime_outputs_reinspected','current_development_runtime_verified',
                'full_catalog_obligation_proven','installed_package_equivalence_proven']:
        if row[key] is not False: raise ValueError('scope inflation')
    if type(row['new_execution_count']) is not int or row['new_execution_count']!=0 or type(row['new_qualification_credit']) is not int or row['new_qualification_credit']!=0:
        raise ValueError('credit inflation')
    scenario=row['case_id'].split('::')[1]
    if scenario=='credential-missing': _validate_missing(row)
    elif scenario=='directory-unavailable': _validate_unavailable(row)
    else: _validate_crypto(row)


def _validate_sources(sources, rows):
    identities={(s['repository'],s['commit'],s['path']) for s in sources}
    if len(sources)!=21 or len(identities)!=21: raise ValueError('source set')
    for source in sources:
        if not re.fullmatch('[0-9a-f]{40}',source['commit']) or not re.fullmatch('[0-9a-f]{64}',source['sha256']):
            raise ValueError('source digest')
        if Path(source['path']).is_absolute() or '..' in Path(source['path']).parts:
            raise ValueError('source locator')
    for row in rows:
        if row['test_source'] not in sources: raise ValueError('unbound case source')


def _validate_authority(data):
    if data['schema']!='iicp.postcert-credential-boundaries.v1': raise ValueError('schema')
    if data['qualified_candidate_manifest_sha256']!='sha256:e7c9aa192be21cdc5ee96e793ab97084137452653cde7580cffd22cf3890618a':
        raise ValueError('candidate')
    if type(data['new_runtime_executions']) is not int or data['new_runtime_executions']!=0:
        raise ValueError('execution inflation')
    flags=['qualification_credit_changed','product_defect_or_evidence_invalidation_inferred',
           'successor_qualified','independent_interoperability_established','programme_complete',
           'historical_inventory_complete']
    if any(data[key] is not False for key in flags): raise ValueError('unsupported promotion')
    if data['controlled_evidence']['private_records_publicly_retrievable'] is not False:
        raise ValueError('private access claim')


def validate(data):
    _validate_authority(data)
    rows=data['case_links']; expected={f'{role}::{s}' for role in ROLES for s in SCENARIOS}
    if len(rows)!=18 or {row['case_id'] for row in rows}!=expected: raise ValueError('case identity')
    for row in rows: _validate_row(row)
    if data['counts']!={'selected_cases':18,'test_local_crypto_cases':12,'production_boundary_cases':6,
                       'existing_accepted_coordinate_references':1152,'per_component':{role:6 for role in ROLES}}:
        raise ValueError('counts')
    _validate_sources(data['source_files'], rows)
    if data['crypto_fixture_context']!={'version':'0.2.0-draft','status':'pre-normative','fixture_sha256':'48be1f06e79da7849367f48deeb7a5ffa71a1de0e21800491dc6bf55d016fb94'}:
        raise ValueError('fixture status')
    if any(marker in json.dumps(data) for marker in ['/Users/','arn:aws:','AKIA','authorization.json']):
        raise ValueError('private marker')
    return True


class CredentialBoundarySupplementTests(unittest.TestCase):
    def setUp(self): self.data=json.loads((REPORT/'source-map.json').read_text())
    def test_positive_projection_and_manifest(self):
        self.assertTrue(validate(self.data))
        manifest=json.loads((REPORT/'manifest.json').read_text())
        self.assertEqual({r['path'] for r in manifest['files']},{'README.md','source-map.json'})
        for r in manifest['files']: self.assertEqual(hashlib.sha256((REPORT/r['path']).read_bytes()).hexdigest(),r['sha256'])
    def test_duplicate_case_refused(self):
        self.data['case_links'][-1]=copy.deepcopy(self.data['case_links'][0])
        with self.assertRaises(ValueError): validate(self.data)
    def test_foreign_candidate_refused(self):
        self.data['qualified_candidate_manifest_sha256']='sha256:'+'0'*64
        with self.assertRaises(ValueError): validate(self.data)
    def test_runtime_inflation_refused(self):
        self.data['new_runtime_executions']=1
        with self.assertRaises(ValueError): validate(self.data)
    def test_credit_inflation_refused(self):
        self.data['case_links'][0]['new_qualification_credit']=1
        with self.assertRaises(ValueError): validate(self.data)
    def test_coordinate_inflation_refused(self):
        self.data['case_links'][0]['existing_accepted_coordinates']+=1
        with self.assertRaises(ValueError): validate(self.data)
    def test_crypto_production_claim_refused(self):
        self.data['case_links'][0]['production_sdk_validator_invoked']=True
        with self.assertRaises(ValueError): validate(self.data)
    def test_whole_obligation_claim_refused(self):
        self.data['case_links'][0]['full_catalog_obligation_proven']=True
        with self.assertRaises(ValueError): validate(self.data)
    def test_rust_transport_claim_refused(self):
        next(r for r in self.data['case_links'] if r['case_id']=='client-rust::directory-unavailable')['transport_failure_exercised_by_fixture']=True
        with self.assertRaises(ValueError): validate(self.data)
    def test_python_constructor_claim_refused(self):
        next(r for r in self.data['case_links'] if r['case_id']=='client-python::credential-missing')['client_constructor_invoked']=True
        with self.assertRaises(ValueError): validate(self.data)
    def test_missing_source_refused(self):
        self.data['source_files'].pop()
        with self.assertRaises(ValueError): validate(self.data)
    def test_private_locator_refused(self):
        self.data['source_files'][0]['path']='/Users/synthetic/private'
        with self.assertRaises(ValueError): validate(self.data)
    def test_history_or_external_promotion_refused(self):
        for field in ['historical_inventory_complete','independent_interoperability_established','successor_qualified']:
            data=copy.deepcopy(self.data); data[field]=True
            with self.assertRaises(ValueError): validate(data)
    def test_private_digest_not_public_retrieval(self):
        self.data['controlled_evidence']['private_records_publicly_retrievable']=True
        with self.assertRaises(ValueError): validate(self.data)
