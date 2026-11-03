#!/usr/bin/env python3
"""Verify public corpus integrity and existing public accounting; never private execution."""
import argparse,hashlib,json,os,re,stat,sys
from pathlib import Path
sys.dont_write_bytecode=True

def check(condition,message):
    if not condition:raise ValueError(message)

def verify(root,expected=None):
    root=Path(root).absolute()
    check(not any(p.is_symlink() for p in (root,*root.parents)), 'symlink corpus')
    fd=os.open(root/'manifest.json',os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        info=os.fstat(stream.fileno())
        check(stat.S_ISREG(info.st_mode) and info.st_size<=131072,'manifest must be bounded regular file')
        manifest_bytes=stream.read(131073)
        check(len(manifest_bytes)<=131072,'manifest size')
    digest='sha256:'+hashlib.sha256(manifest_bytes).hexdigest()
    if expected:check(digest==expected,'manifest trust anchor mismatch')
    m=json.loads(manifest_bytes)
    check(set(m)=={'schema','source_commit','candidate_manifest_sha256','accepted','historical_inventory_complete','independent_external_certification','qualification_credit','members'},'manifest fields')
    check(m['schema']=='iicp.qualification-documentation-handoff.v2','manifest schema')
    check(re.fullmatch('[0-9a-f]{40}',m['source_commit']) is not None,'source identity')
    check(m['historical_inventory_complete'] is False and m['independent_external_certification']=='NOT_ESTABLISHED' and m['qualification_credit']==0,'authority inflation')
    members=m['members'];check(isinstance(members,dict) and set(members)==set(['AGENT_BRIEF.md', 'COMPONENT_BASELINE.md', 'COVERAGE_AND_GAPS.md', 'REVIEWED_FINDINGS.md', 'SOURCE_AUTHORITY.md', 'SOURCE_INDEX.json', 'START_HERE.md', 'contracts/scope.json', 'data/analysis.json', 'data/certificates.json', 'data/coverage.json', 'data/dmsc-sources.json', 'data/events.json', 'data/history-gaps.json', 'data/receipts.json', 'data/reporting-policy.json', 'data/scope.json', 'data/status.json', 'data/unresolved-clauses.json', 'reporting-policy.json', 'requirements.txt', 'schemas/handoff-v2-metadata.json', 'schemas/qualification-analysis-v1.json', 'schemas/report-v1.json', 'validation/certificate_reporting.py', 'validation/qualification_analysis.py', 'validation/report_common.py', 'verify.py']),'required corpus members')
    check(all(isinstance(n,str) and n and not Path(n).is_absolute() and '..' not in Path(n).parts and '\\' not in n and ':' not in n for n in members),'member path')
    found=set()
    for p in root.rglob('*'):
        check(not p.is_symlink(),'symlink member')
        if p.is_file():found.add(p.relative_to(root).as_posix())
        elif p.is_dir():check(any(n.startswith(p.relative_to(root).as_posix()+'/') for n in members),'unbound directory')
        else:raise ValueError('nonregular member')
    check(found==set(members)|{'manifest.json'},'missing or extra member')
    for n,d in members.items():
        check(set(d)=={'sha256','bytes'},'member metadata')
        p=root/n;check(p.stat().st_size==d['bytes'] and d['bytes']<=8*1024*1024,'member size')
        check('sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256'],'member changed')
    for name,trusted in {'validation/report_common.py': 'sha256:e36af3cb270ff3c8b04f29e764da0a247fca61fbcb7bd128891bfea0e0356878', 'validation/certificate_reporting.py': 'sha256:045a4f3cac3f07878a9b6c27ebd94e5ab1d0ee35cdd9a6d94f665357569b624f', 'schemas/report-v1.json': 'sha256:68cd637d01f6928b927712c05d6d3ed866ecdfea34e16baca6c4a7292bc38b64', 'reporting-policy.json': 'sha256:5da5eadd6443ba29207e9028999e9c474e4d8d2ffb5b6a3fa77e7cf7962f42ca', 'contracts/scope.json': 'sha256:7c2959da319754993f30ee90ca29646254edf9df0bcf5f57afe2929e8c5dbf49'}.items():
        check(members.get(name,{}).get('sha256')==trusted,'unreviewed validation component')
    for name,trusted in {'validation/qualification_analysis.py': 'sha256:ed01c0794d7444144e2ea3eb30134991b510bad9115ee1706462696508d0f9b9', 'schemas/qualification-analysis-v1.json': 'sha256:03600077cea3e1a2aaa5daab0f174d6d88cae9f1862441934873e7702eff3dea', 'schemas/handoff-v2-metadata.json': 'sha256:ff24526a7a008ed95fd5ca1e5583ab459e49a12bbeef2e21d805cc9411588f4c'}.items():
        check(members.get(name,{}).get('sha256')==trusted,'unreviewed v2 validation component')
    # Import only after all corpus bytes have passed the supplied external anchor/hash checks.
    sys.path.insert(0,str(root/'validation'))
    from report_common import check_bundle
    def load(n):return json.loads((root/n).read_text())
    status=load('data/status.json');receipts=load('data/receipts.json');events=load('data/events.json')
    check_bundle(status,receipts,events)
    check(m['source_commit']==status['source_commit'] and m['candidate_manifest_sha256']==status['authority']['candidate_manifest_sha256'],'manifest authority differs')
    check(m['accepted']==status['accepted']=={'shards':64,'support_cells':218,'edge_executions':5590,'sentinels':4,'certificates':5},'baseline counts')
    check(load('data/certificates.json')=={'schema':'iicp.qualification-certificate-derivatives.v1','certificates':status['certificates']},'certificate copy differs')
    check((root/'data/scope.json').read_bytes()==(root/'contracts/scope.json').read_bytes(),'scope copy differs')
    check((root/'data/reporting-policy.json').read_bytes()==(root/'reporting-policy.json').read_bytes(),'policy copy differs')
    scope=load('data/scope.json')
    coverage={'schema':'iicp.qualification-documentation-coverage.v1','support_cells':scope['support_cells'],'edge_executions':scope['edge_executions'],'scenario_ids':sorted({x.split('::',1)[0] for x in scope['edge_executions']}),'platforms':status['platforms']}
    check(load('data/coverage.json')==coverage,'coverage derivative differs')
    index=load('SOURCE_INDEX.json')
    check(set(index)=={'schema','source_commit','qualification_authority','records'} and index['schema']=='iicp.qualification-documentation-sources.v1' and index['source_commit']==m['source_commit'] and index['qualification_authority']=='RobLe3/iicp.network','source index contract')
    check(len(index['records'])==len(['project/pre1-edge-case-catalog.json', 'project/pre1-edge-case-results.json', 'project/pre1-stability-successor-frozen.json', 'project/pre1-successor-executor-registry.json', 'project/pre1-successor-qualification-shard-plan.json', 'project/pre1-support-matrix.json', 'project/pre1-support-results.json', 'reports/pre1-qualification/certificates/ecosystem.json', 'reports/pre1-qualification/certificates/linux-aarch64.json', 'reports/pre1-qualification/certificates/linux-x86_64.json', 'reports/pre1-qualification/certificates/macos-arm64.json', 'reports/pre1-qualification/certificates/windows-x86_64.json']) and {r.get('path') for r in index['records']}==set(['project/pre1-edge-case-catalog.json', 'project/pre1-edge-case-results.json', 'project/pre1-stability-successor-frozen.json', 'project/pre1-successor-executor-registry.json', 'project/pre1-successor-qualification-shard-plan.json', 'project/pre1-support-matrix.json', 'project/pre1-support-results.json', 'reports/pre1-qualification/certificates/ecosystem.json', 'reports/pre1-qualification/certificates/linux-aarch64.json', 'reports/pre1-qualification/certificates/linux-x86_64.json', 'reports/pre1-qualification/certificates/macos-arm64.json', 'reports/pre1-qualification/certificates/windows-x86_64.json']),'source index completeness')
    for row in index['records']:
        check(set(row)=={'path','sha256','url'},'source record fields')
        check(re.fullmatch(r'(project|reports/pre1-qualification/certificates)/[A-Za-z0-9_.\-/]+\.json',row['path']) is not None and '..' not in Path(row['path']).parts,'source record path')
        check(row['url']=='https://github.com/RobLe3/iicp.network/blob/'+m['source_commit']+'/'+row['path'],'source locator')
        check(re.fullmatch('sha256:[0-9a-f]{64}',row['sha256']) is not None,'source hash')
    from qualification_analysis import generate
    from jsonschema import Draft202012Validator
    analysis=load('data/analysis.json')
    links={'schema':'iicp.qualification-analysis-links.v1','source_commit':analysis['source_commit'],'requirements':analysis['requirements'],'history':analysis['history'],'dmsc_sources':analysis['dmsc_sources']}
    Draft202012Validator(load('schemas/handoff-v2-metadata.json')['$defs']['reviewed_links']).validate(links)
    check(analysis==generate(status,receipts,events,scope,links),'analysis semantic mismatch')
    check(load('data/unresolved-clauses.json')=={'schema':'iicp.handoff-unresolved-clauses.v1','requirements':analysis['requirements']},'clause copy differs')
    check(load('data/dmsc-sources.json')=={'schema':'iicp.handoff-dmsc-sources.v1','sources':analysis['dmsc_sources'],'records':analysis['dmsc']},'DMSC copy differs')
    Draft202012Validator(load('schemas/handoff-v2-metadata.json')).validate(load('data/history-gaps.json'))
    return {'manifest_sha256':digest,'trust_anchor_checked':bool(expected),'files':len(members),'private_source_reverification':False,'qualification_credit':0}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd());p.add_argument('--expected-manifest-sha256');a=p.parse_args()
    try:print(json.dumps(verify(a.root,a.expected_manifest_sha256),sort_keys=True))
    except (ValueError,OSError,KeyError,ImportError) as e:print('REFUSED: '+str(e),file=sys.stderr);raise SystemExit(1)
