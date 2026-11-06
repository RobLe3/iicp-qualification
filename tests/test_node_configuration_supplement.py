"""Validate an informative public source capsule; never run SDK or qualification commands."""
from pathlib import Path
import copy,hashlib,json,unittest
from jsonschema import Draft202012Validator,ValidationError
from test_sdk_network_readiness_supplement import false_flags,zero_counts,validate_source,validate_reference
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports/postcert/2026-11-06-node-configuration'
COMPONENTS={'client-python','client-typescript','client-rust'}
SCENARIOS={'config-missing','config-malformed','config-permission-denied'}
REPOS={'RobLe3/iicp-client-python','RobLe3/iicp-client-typescript','RobLe3/iicp-client-rust','RobLe3/IICP'}
TOP={'schema','state','candidate_manifest_sha256','public_analysis_file_sha256','qualification_derivative_source_commit','source_index_file_sha256','catalog_file_sha256','catalog_text_republished','sources','cases','counts','limitations','non_authorizing','accepted_results_changed','successor_qualified_or_frozen','whole_capability_completion','independent_interoperability_established','historical_inventory_complete','new_runtime_executions','new_qualification_credit','programme_complete'}
def validate_header(data,analysis):
    if set(data)!=TOP or data['schema']!='iicp.postcert-node-configuration-source-capsule.v1':raise ValueError('schema')
    if data['state']!='SOURCE_INTERPRETATION_NOT_FROZEN_IFRB' or data['candidate_manifest_sha256']!=analysis['candidate_manifest_sha256']:raise ValueError('candidate or state')
    if data['non_authorizing'] is not True:raise ValueError('authority')
    false_flags(data,['catalog_text_republished','accepted_results_changed','successor_qualified_or_frozen','whole_capability_completion','independent_interoperability_established','historical_inventory_complete','programme_complete'])
    zero_counts(data,['new_runtime_executions','new_qualification_credit'])
    expected={'case_definitions':9,'source_references':32,'existing_coordinate_references':576,'coordinate_references_per_target':{t:144 for t in ['linux-aarch64','linux-x86_64','macos-arm64','windows-x86_64']}}
    if data['counts']!=expected:raise ValueError('counts')
def sources_index(data):
    if len(data['sources'])!=32 or len({s['source_id'] for s in data['sources']})!=32:raise ValueError('source count')
    for s in data['sources']:
        if s['repository'] not in REPOS:raise ValueError('source repository')
        validate_source(s)
    return {s['source_id']:s for s in data['sources']}
def validate_case(row,sources):
    if row['case_id']!=row['component']+'::'+row['scenario_id']:raise ValueError('case identity')
    false_flags(row,['full_catalog_obligation_proven','new_runtime_execution']);zero_counts(row,['new_qualification_credit'])
    if not row['limitations'] or not row['source_postconditions']:raise ValueError('missing limits')
    validate_reference(row['source_assertion'],sources)
    src=sources[row['source_assertion']['source_id']]
    if src['repository']!='RobLe3/iicp-'+row['component'] or src['commit']!=row['qualified_product_source_commit']:raise ValueError('mixed source')
    if row['capability_context']['association']!='INDIRECT_SCOPE_CONTEXT_NOT_CAPABILITY_COMPLETION':raise ValueError('capability inflation')
def validate_coordinates(row,existing):
    for ref in row['existing_coordinate_refs']:
        pub=existing.get(ref['assertion_id'])
        if pub is None or pub['component']!=row['component'] or pub['scenario_id']!=row['scenario_id']:raise ValueError('coordinate identity')
        if any(ref[k]!=pub[k] for k in ['target','runtime','mode','directory_flavor','receipt_file_sha256']):raise ValueError('coordinate binding')
def validate_capsule(data,analysis):
    validate_header(data,analysis);sources=sources_index(data);existing={r['assertion_id']:r for r in analysis['assertions']}
    expected={c+'::'+s for c in COMPONENTS for s in SCENARIOS};actual=[r['case_id'] for r in data['cases']]
    if len(actual)!=9 or set(actual)!=expected:raise ValueError('case set')
    refs=[]
    for row in data['cases']:
        validate_case(row,sources);validate_coordinates(row,existing);refs.extend(r['assertion_id'] for r in row['existing_coordinate_refs'])
    if len(refs)!=576 or len(set(refs))!=576:raise ValueError('duplicate/missing coordinates')
    text=json.dumps(data).lower()
    if any(token in text for token in ['/users/','/home/','ghsa-','authorization.json','aws_account','access_key','private_payload']):raise ValueError('private material')
class NodeConfigurationCapsuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((REPORT/'source-map.json').read_text());cls.analysis=json.loads((ROOT/'reports/analysis-v2/analysis.json').read_text())
    def rejects(self,edit):
        data=copy.deepcopy(self.data);edit(data)
        with self.assertRaises(ValueError):validate_capsule(data,self.analysis)
    def test_valid_capsule(self):validate_capsule(self.data,self.analysis)
    def test_manifest_and_public_analysis_pins(self):
        manifest=json.loads((REPORT/'manifest.json').read_text())
        self.assertEqual({r['path'] for r in manifest['files']},{'README.md','source-map.json','source-map.schema.json'})
        for row in manifest['files']:self.assertEqual(hashlib.sha256((REPORT/row['path']).read_bytes()).hexdigest(),row['sha256'])
        self.assertEqual(hashlib.sha256((ROOT/'reports/analysis-v2/analysis.json').read_bytes()).hexdigest(),self.data['public_analysis_file_sha256'])
    def test_json_schema_valid(self):
        schema=json.loads((REPORT/'source-map.schema.json').read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(self.data)
    def test_json_schema_rejects_authority(self):
        schema=json.loads((REPORT/'source-map.schema.json').read_text());data=copy.deepcopy(self.data);data['non_authorizing']=False
        with self.assertRaises(ValidationError):Draft202012Validator(schema).validate(data)
    def test_json_schema_rejects_case_private_field(self):
        schema=json.loads((REPORT/'source-map.schema.json').read_text());data=copy.deepcopy(self.data);data['cases'][0]['raw_private_capture']='SYNTHETIC'
        with self.assertRaises(ValidationError):Draft202012Validator(schema).validate(data)
    def test_wrong_candidate(self):self.rejects(lambda d:d.update(candidate_manifest_sha256='sha256:'+'0'*64))
    def test_duplicate_case(self):self.rejects(lambda d:d['cases'].__setitem__(0,copy.deepcopy(d['cases'][1])))
    def test_missing_case(self):self.rejects(lambda d:d['cases'].pop())
    def test_foreign_coordinate(self):self.rejects(lambda d:d['cases'][0]['existing_coordinate_refs'][0].update(assertion_id='foreign'))
    def test_mismatched_receipt(self):self.rejects(lambda d:d['cases'][0]['existing_coordinate_refs'][0].update(receipt_file_sha256='sha256:'+'0'*64))
    def test_private_source_url(self):self.rejects(lambda d:d['sources'][0].update(url='file:///Users/private'))
    def test_full_conformance_inflation(self):self.rejects(lambda d:d['cases'][0].update(full_catalog_obligation_proven=True))
    def test_runtime_inflation(self):self.rejects(lambda d:d.update(new_runtime_executions=1))
    def test_credit_inflation(self):self.rejects(lambda d:d.update(new_qualification_credit=1))
    def test_private_extra_field(self):self.rejects(lambda d:d.update(private_payload='SYNTHETIC'))
if __name__=='__main__':unittest.main()
