"""Validate minimized source analysis; no network, SDK imports or product tests."""
from pathlib import Path
import copy,hashlib,json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports/postcert/2026-11-06-sdk-network-readiness'
COMPONENTS={'client-python','client-typescript','client-rust'}
SCENARIOS={'dns-failure','tls-failure','partial-response','dynamic-public-route-readiness'}
TARGETS={'linux-aarch64','linux-x86_64','macos-arm64','windows-x86_64'}

def false_flags(value,keys):
    for key in keys:
        if value[key] is not False:raise ValueError('authority or assertion inflation')

def zero_counts(value,keys):
    for key in keys:
        if type(value[key]) is not int or value[key]!=0:raise ValueError('execution or credit inflation')

def validate_metadata(data,analysis):
    if data['schema']!='iicp.postcert-sdk-network-readiness-source-review.v1':raise ValueError('schema')
    if data['candidate_manifest_sha256']!=analysis['candidate_manifest_sha256']:raise ValueError('candidate')
    false_flags(data,['accepted_results_changed','successor_qualified_or_frozen','historical_inventory_complete','independent_interoperability_established','programme_complete'])
    zero_counts(data,['new_runtime_executions','new_qualification_credit'])
    if data['counts']!={'case_definitions':12,'source_references':33,'existing_coordinate_references':768,'coordinate_references_per_target':192,'source_findings':5}:raise ValueError('counts')

def validate_source(source):
    if not re.fullmatch('[0-9a-f]{40}',source['commit']) or not re.fullmatch('[0-9a-f]{64}',source['sha256']):raise ValueError('source hash')
    if Path(source['path']).is_absolute() or '..' in Path(source['path']).parts:raise ValueError('source path')
    expected=f"https://github.com/{source['repository']}/blob/{source['commit']}/{source['path']}"
    if source['url']!=expected:raise ValueError('source URL')

def source_index(data):
    if len(data['sources'])!=33 or len({s['source_id'] for s in data['sources']})!=33:raise ValueError('source identity')
    sources={s['source_id']:s for s in data['sources']}
    for source in sources.values():validate_source(source)
    return sources

def validate_reference(ref,sources):
    if ref['source_id'] not in sources:raise ValueError('unbound source')
    a,b=ref['lines']
    if type(a) is not int or type(b) is not int or not 1<=a<=b:raise ValueError('span')
    if not re.fullmatch('[0-9a-f]{64}',ref['span_sha256']):raise ValueError('span hash')

def validate_case_claims(row):
    if row['case_id']!=row['component']+'::'+row['scenario_id']:raise ValueError('case identity')
    false_flags(row,['full_catalog_obligation_proven','raw_private_outputs_reinspected','standalone_execution_authorized'])
    zero_counts(row,['new_runtime_executions','new_qualification_credit'])
    if not row['selected_sources'] or not row['not_established']:raise ValueError('unbounded claim')
    if row['scenario_id']=='partial-response' and row['coverage']!='SCHEMA_INVALID_OR_BRANCH_NOT_TRUNCATION':raise ValueError('OR branch inflation')
    if row['scenario_id']=='dynamic-public-route-readiness' and not row['coverage'].endswith('_SUBPROPERTY_ONLY'):raise ValueError('lifecycle inflation')

def validate_original_assignment(aid,row,original):
    r=original[aid]
    if r['component']!=row['component'] or r['scenario_id']!=row['scenario_id'] or r['observed_disposition']!='ACCEPTED_PASS':raise ValueError('foreign or diagnostic assignment')

def validate_case_assignments(row,original):
    from collections import Counter
    ids=row['existing_assignment_ids'];expected=96 if row['component']=='client-python' else 48
    if len(ids)!=expected or len(set(ids))!=expected:raise ValueError('row assignment count')
    if dict(Counter(original[x]['target'] for x in ids))!=row['recorded_targets']:raise ValueError('target counts')
    if dict(Counter(original[x]['runtime'] for x in ids))!=row['recorded_runtimes']:raise ValueError('runtime counts')
    for aid in ids:validate_original_assignment(aid,row,original)
    return ids

def validate_cases(data,analysis,sources):
    expected_cases={f'{c}::{s}' for c in COMPONENTS for s in SCENARIOS}
    if len(data['cases'])!=12 or {r['case_id'] for r in data['cases']}!=expected_cases:raise ValueError('case set')
    original={r['assertion_id']:r for r in analysis['assertions']};observed=[]
    for row in data['cases']:
        validate_case_claims(row)
        refs=row['selected_sources']+row['helper_sources']+row['positive_source_controls']+row['protocol_context']['sources']
        for ref in refs:validate_reference(ref,sources)
        observed+=validate_case_assignments(row,original)
    expected={r['assertion_id'] for r in original.values() if r['component'] in COMPONENTS and r['scenario_id'] in SCENARIOS}
    if len(observed)!=768 or len(set(observed))!=768 or set(observed)!=expected:raise ValueError('assignment universe')

def validate(data,analysis):
    validate_metadata(data,analysis)
    validate_cases(data,analysis,source_index(data))
    if len(data['findings'])!=5 or len({x['id'] for x in data['findings']})!=5:raise ValueError('findings')
    raw=json.dumps(data)
    for forbidden in ['/Users/','arn:aws:','AWS_ACCESS_KEY_ID','BEGIN PRIVATE KEY','confirmation_code']:
        if forbidden in raw:raise ValueError('private payload')

class SdkNetworkReadinessSupplement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((REPORT/'source-map.json').read_text())
        cls.analysis=json.loads((ROOT/'reports/analysis-v2/analysis.json').read_text())
    def test_fixed_map_and_original_public_joins(self):validate(self.data,self.analysis)
    def test_public_analysis_pin(self):self.assertEqual(self.data['public_analysis_sha256'],hashlib.sha256((ROOT/'reports/analysis-v2/analysis.json').read_bytes()).hexdigest())
    def test_manifest(self):
        manifest=json.loads((REPORT/'manifest.json').read_text())
        self.assertEqual({'README.md','source-map.json'},{r['path'] for r in manifest['files']})
        for row in manifest['files']:self.assertEqual(row['sha256'],hashlib.sha256((REPORT/row['path']).read_bytes()).hexdigest())
    def reject(self,change):
        data=copy.deepcopy(self.data);change(data)
        with self.assertRaises((ValueError,KeyError)):validate(data,self.analysis)
    def test_credit_inflation(self):self.reject(lambda d:d.update(new_qualification_credit=1))
    def test_frozen_successor_inflation(self):self.reject(lambda d:d.update(successor_qualified_or_frozen=True))
    def test_duplicate_case(self):self.reject(lambda d:d['cases'].append(copy.deepcopy(d['cases'][0])))
    def test_foreign_assignment(self):self.reject(lambda d:d['cases'][0]['existing_assignment_ids'].__setitem__(0,'foreign'))
    def test_partial_response_not_truncation(self):self.reject(lambda d:next(c for c in d['cases'] if c['scenario_id']=='partial-response').update(coverage='ALL_TRANSPORT_ERRORS'))
    def test_private_host_path(self):self.reject(lambda d:d.update(private='/Users/synthetic-marker'))
    def test_unknown_source_reference(self):self.reject(lambda d:d['cases'][0]['selected_sources'][0].update(source_id='foreign'))
    def test_target_applicability_inflation(self):self.reject(lambda d:d['cases'][0]['recorded_targets'].update(unknown=1))
    def test_full_lifecycle_claim(self):self.reject(lambda d:d['cases'][0].update(full_catalog_obligation_proven=True))
if __name__=='__main__':unittest.main()
