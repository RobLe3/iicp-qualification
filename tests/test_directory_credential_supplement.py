"""Bounded report identity/claim guards; never execute Directory tests."""
import copy,hashlib,json,re,unittest
from pathlib import Path
REPORT=Path(__file__).resolve().parents[1]/'reports/postcert/2026-11-06-directory-credentials'
ROLES={'directory-php','directory-rust'}
SCENARIOS={'credential-expired','credential-missing','credential-replayed','credential-rotated','signature-mismatch'}

def validate_row(row):
    if row['component']!=row['case_id'].split('::')[0]:raise ValueError('component')
    for flag in ['raw_runtime_outputs_reinspected','full_catalog_obligation_proven',
                 'installed_package_equivalence_proven','recorded_modes_prove_test_body_mode_configuration',
                 'command_is_standalone_reproduction']:
        if row[flag] is not False:raise ValueError('assertion inflation')
    for key in ['new_runtime_executions','new_qualification_credit']:
        if type(row[key]) is not int or row[key]!=0:raise ValueError('execution/credit inflation')
    if row['applicable_recorded_targets']!=['linux-aarch64','linux-x86_64']:raise ValueError('target applicability')
    if row['applicable_recorded_modes']!=['local-only','public','restricted']:raise ValueError('mode applicability')
    expected_runtimes=['php-8.3'] if row['component']=='directory-php' else ['msrv-1.88','rust-1.98.0']
    if row['applicable_recorded_runtimes']!=expected_runtimes:raise ValueError('runtime applicability')
    if type(row['existing_coordinate_references']) is not int or row['existing_coordinate_references']!=6*len(expected_runtimes):
        raise ValueError('coordinate count')


def validate_semantic_flags(rows):
    by_id={row['case_id']:row for row in rows}
    for role in ROLES:
        rotation=by_id[role+'::credential-rotated']
        for flag in ['old_token_rejection_asserted','replacement_token_acceptance_asserted','selected_catalog_transition_asserted']:
            if rotation[flag] is not (role=='directory-php'):raise ValueError('rotation assertion depth')
        replay=by_id[role+'::credential-replayed']
        if replay['persistent_replay_store_exercised'] is not False:raise ValueError('persistent replay inflation')
        if replay['in_memory_challenge_repository_invoked'] is not (role=='directory-rust'):raise ValueError('replay contract')
        signature=by_id[role+'::signature-mismatch']
        if signature['high_water_unchanged_asserted'] is not (role=='directory-rust'):raise ValueError('signature assertion depth')
    if by_id['directory-rust::credential-missing']['fixture_token_verification_enabled'] is not False:
        raise ValueError('permissive fixture inflation')
    if by_id['directory-php::credential-missing']['positive_source_control_conditional'] is not True:
        raise ValueError('positive prerequisite missing')


def validate_sources(sources,rows):
    if len(sources)!=28 or len({(r['repository'],r['path']) for r in sources})!=28:raise ValueError('source set')
    for source in sources:
        if not re.fullmatch('[0-9a-f]{40}',source['commit']) or not re.fullmatch('[0-9a-f]{64}',source['sha256']):raise ValueError('source digest')
        if Path(source['path']).is_absolute() or '..' in Path(source['path']).parts:raise ValueError('source locator')
    for row in rows:
        if row['test_source'] not in sources:raise ValueError('unbound test source')


def validate_authority(data):
    if data['schema']!='iicp.postcert-directory-credential-source-review.v1':raise ValueError('schema')
    if data['candidate_manifest_sha256']!='sha256:e7c9aa192be21cdc5ee96e793ab97084137452653cde7580cffd22cf3890618a':raise ValueError('candidate')
    for flag in ['accepted_results_changed','successor_qualified_or_frozen','product_defect_or_qualification_invalidation_inferred',
                 'historical_inventory_complete','independent_interoperability_established','programme_complete']:
        if data[flag] is not False:raise ValueError('authority inflation')
    for key in ['new_runtime_executions','new_qualification_credit']:
        if type(data[key]) is not int or data[key]!=0:raise ValueError('new execution or credit')
    if data['controlled_evidence']['private_records_publicly_retrievable'] is not False:raise ValueError('private retrieval claim')


def validate_fixed_metadata(data):
    if data['counts']!={'case_definitions':10,'source_files':26,'qualified_harness_git_reads':52,'existing_coordinate_references':90,'per_component':{'directory-php':5,'directory-rust':5}}:raise ValueError('batch accounting')
    if data['bounded_review_frontier']!={'all_existing_accepted_coordinates':5808,'case_definitions_not_reconciled_to_this_review_frontier':93,'declared_case_definitions':147,'existing_accepted_coordinates_in_selected_cases':2466,'explicitly_reconciled_case_definition_reviews':54}:raise ValueError('frontier accounting')
    if data['membership_fixture_context']!={'fixture_version':'0.1.0-draft','status':'pre-normative','sha256':'78cb70b19dabed5be0175555cf2b4bb123dd4bc77ce36b67b745f311f3d941d4'}:raise ValueError('fixture status')
    if any(marker in json.dumps(data) for marker in ['/Users/','arn:aws:','AKIA','authorization.json']):raise ValueError('private marker')


def validate(data):
    validate_authority(data)
    rows=data['case_links'];expected={f'{role}::{scenario}' for role in ROLES for scenario in SCENARIOS}
    if len(rows)!=10 or {row['case_id'] for row in rows}!=expected:raise ValueError('case identities')
    for row in rows:validate_row(row)
    validate_semantic_flags(rows)
    validate_sources(data['source_files'],rows)
    validate_fixed_metadata(data)
    return True

class DirectoryCredentialSupplementTests(unittest.TestCase):
    def setUp(self):self.data=json.loads((REPORT/'source-map.json').read_text())
    def row(self,identity):return next(r for r in self.data['case_links'] if r['case_id']==identity)
    def test_positive_map_and_manifest(self):
        self.assertTrue(validate(self.data))
        manifest=json.loads((REPORT/'manifest.json').read_text())
        self.assertEqual({r['path'] for r in manifest['files']},{'README.md','source-map.json'})
        for row in manifest['files']:self.assertEqual(hashlib.sha256((REPORT/row['path']).read_bytes()).hexdigest(),row['sha256'])
    def test_foreign_candidate_rejected(self):
        self.data['candidate_manifest_sha256']='sha256:'+'0'*64
        with self.assertRaises(ValueError):validate(self.data)
    def test_duplicate_case_rejected(self):
        self.data['case_links'][-1]=copy.deepcopy(self.data['case_links'][0])
        with self.assertRaises(ValueError):validate(self.data)
    def test_runtime_execution_inflation_rejected(self):
        self.data['new_runtime_executions']=1
        with self.assertRaises(ValueError):validate(self.data)
    def test_wrong_platform_applicability_rejected(self):
        self.row('directory-rust::credential-missing')['applicable_recorded_targets'].append('windows-x86_64')
        with self.assertRaises(ValueError):validate(self.data)
    def test_recorded_mode_not_execution_conformance(self):
        self.row('directory-php::credential-rotated')['recorded_modes_prove_test_body_mode_configuration']=True
        with self.assertRaises(ValueError):validate(self.data)
    def test_rust_rotation_scope_inflation_rejected(self):
        self.row('directory-rust::credential-rotated')['old_token_rejection_asserted']=True
        with self.assertRaises(ValueError):validate(self.data)
    def test_permissive_positive_not_credential_validation(self):
        self.row('directory-rust::credential-missing')['fixture_token_verification_enabled']=True
        with self.assertRaises(ValueError):validate(self.data)
    def test_replay_storage_inflation_rejected(self):
        self.row('directory-php::credential-replayed')['persistent_replay_store_exercised']=True
        with self.assertRaises(ValueError):validate(self.data)
    def test_missing_source_rejected(self):
        self.data['source_files'].pop()
        with self.assertRaises(ValueError):validate(self.data)
    def test_private_source_locator_rejected(self):
        self.data['source_files'][0]['path']='/Users/synthetic/private'
        with self.assertRaises(ValueError):validate(self.data)
    def test_incorrect_frontier_rejected(self):
        self.data['bounded_review_frontier']['explicitly_reconciled_case_definition_reviews']+=1
        with self.assertRaises(ValueError):validate(self.data)
    def test_history_and_interoperability_promotion_rejected(self):
        for key in ['historical_inventory_complete','independent_interoperability_established','programme_complete']:
            data=copy.deepcopy(self.data);data[key]=True
            with self.assertRaises(ValueError):validate(data)
    def test_coordinate_and_package_claims_rejected(self):
        for key,value in [('existing_coordinate_references',999),('installed_package_equivalence_proven',True)]:
            data=copy.deepcopy(self.data);data['case_links'][0][key]=value
            with self.assertRaises(ValueError):validate(data)
