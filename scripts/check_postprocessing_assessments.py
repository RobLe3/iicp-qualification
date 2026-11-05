"""Read-only public derivative checks; never awards qualification credit."""
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'reports/postprocessing-assessments/2026-11-05'
def validate(data):
    schema=json.loads((ROOT/'schemas/postprocessing-assessments.schema.json').read_text())
    Draft202012Validator(schema).validate(data)
    bindings=json.loads((PACKAGE/'manifest.json').read_text())['record_sha256']
    for group in ['criteria','dmsc']:
        for row in data[group]:
            if hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=bindings.get(row['id']):raise ValueError('reviewed record binding')
    raw=json.dumps(data)
    if any(marker in raw for marker in ['/Users/','/home/','arn:aws:','AKIA','ASIA']):raise ValueError('private operational content')
    if data['counts']!={'criteria_reviewed':41,'criteria_supported':20,'criteria_unverified':21,'dmsc_reviewed':27,'external_experiments':0}:raise ValueError('scope counts')
    rows=data['criteria'];expected={f'root-{n}-clause-{i}' for n,total in [(1106,7),(1117,11),(1470,13),(1493,5),(1481,5)] for i in range(total)}
    if len(rows)!=41 or {r['id'] for r in rows}!=expected:raise ValueError('criterion coverage')
    if sum(r['reviewed_disposition']=='PASS' for r in rows)!=20 or sum(r['reviewed_disposition']=='UNVERIFIED' for r in rows)!=21:raise ValueError('criterion support inflation')
    for r in rows:
        if r['reviewed_disposition']=='UNVERIFIED' and not r['missing_proof']:raise ValueError('unresolved clause lacks gap')
    p=ROOT/'reports/analysis-v2/analysis.json'
    if hashlib.sha256(p.read_bytes()).hexdigest()!=data['analysis_sha256']:raise ValueError('analysis binding')
    analysis=json.loads(p.read_text());expected={f'D{i:02}' for i in range(1,15)}|{f'V{i:02}' for i in range(1,14)}
    if len(data['dmsc'])!=27 or {r['id'] for r in data['dmsc']}!=expected:raise ValueError('crosswalk coverage')
    for r in data['dmsc']:
        if r['crosswalk_relation_change']!='NONE' or r['external_experiment_status']!='NOT_ESTABLISHED':raise ValueError('maturity inflation')
        selected=[a for a in analysis['assertions'] if a['scenario_id'] in r['scenario_ids']]
        if r['related_assertion_ids']!=[a['assertion_id'] for a in selected] or r['related_assertion_count']!=len(selected):raise ValueError('assertion mapping')
        if r['related_receipt_ids']!=sorted({a['receipt_id'] for a in selected}):raise ValueError('receipt mapping')
        if r['targets']!=sorted({a['target'] for a in selected}):raise ValueError('applicability')
    return True
if __name__=='__main__':
    p=PACKAGE/'assessments.json';manifest=json.loads((PACKAGE/'manifest.json').read_text())
    schema=json.loads((ROOT/'schemas/postprocessing-assessments.schema.json').read_text())
    Draft202012Validator(schema['$defs']['publicationManifest']).validate(manifest)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=manifest['files']['assessments.json']:raise ValueError('package digest')
    validate(json.loads(p.read_text()))
    print('PASS: 41 dispositions and 27 bounded assessments; no qualification credit or interoperability established')
