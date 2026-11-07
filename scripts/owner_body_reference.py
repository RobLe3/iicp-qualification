"""Validate/render a dated owner-body audit; never credits or executes qualification."""
import argparse
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-07-owner-audit'
JSON_PIN='147a274f241542f1f399efed76f9b592583b5409ec9aaf4f2b3c17bf9ff8d8dd'
SCHEMA_PIN='8a9d12620a2736d27f506905b47513c171a583fd34097571d23fc51e1eb97bf7'
REPOSITORIES={
 'RobLe3/iicp-client-python':(35,2,33,'9c5b3d894ee89ef9fcde52ea0ad99d388ed62183'),
 'RobLe3/iicp-client-typescript':(28,1,27,'97c768d8b9e90756773103e432c273a7d98ba08e'),
 'RobLe3/iicp-client-rust':(52,6,46,'0b8b529262977b6482dd7900d473e7d152ba9293'),
 'RobLe3/iicp-directory-php':(29,2,27,'2dfd228b49c587150a44f448cea1351a9f039d32'),
 'RobLe3/iicp-directory-rust':(33,2,31,'b95a362ad8f974334994ca73cd20210388a2362f'),
 'RobLe3/iicp-management':(99,2,97,'9b9c910fe6443068e71152f1a95f41639041c647')}
DEVELOPMENT_ONLY={'RobLe3/iicp-client-python#145','RobLe3/iicp-client-typescript#124','RobLe3/iicp-client-rust#185'}
SELECTED=DEVELOPMENT_ONLY|{'RobLe3/iicp-client-python#136','RobLe3/iicp-client-typescript#115','RobLe3/iicp-client-typescript#116','RobLe3/iicp-client-rust#168','RobLe3/iicp-client-rust#169','RobLe3/iicp-client-rust#171','RobLe3/iicp-directory-rust#142','RobLe3/iicp-directory-php#54','RobLe3/iicp-directory-php#55','RobLe3/iicp-directory-rust#100','RobLe3/iicp-directory-rust#55','RobLe3/iicp-management#139','RobLe3/iicp-management#141','RobLe3/iicp-management#159'}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(condition,reason):
    if not condition:raise ValueError(reason)
def canonical(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
def load():return json.loads((DATA/'audit.json').read_bytes())
def validate(value):
    privacy(value)
    schema=(DATA/'audit.schema.json').read_bytes()
    require(sha(schema)==SCHEMA_PIN,'SCHEMA_IDENTITY')
    Draft202012Validator(json.loads(schema)).validate(value)
    for flag in ['all_six_supported_defect_clearance','historical_inventory_complete','new_runtime_validation']:
        require(value[flag] is False,'NO_COMPLETENESS_OR_RUNTIME_PROMOTION')
    require(type(value['qualification_credit']) is int and value['qualification_credit']==0,'NO_NEW_CREDIT')
    counts=value['counts']
    require(all(type(v) is int for v in counts.values()),'EXACT_INTEGER_COUNTS')
    require(counts=={'owner_body_records':276,'closed_body_records':261,'open_body_records':15,'selected_correction_records':17,'correction_source_in_qualified_source':14,'development_only_corrections':3},'SNAPSHOT_COUNTS')
    snapshots=value['source_snapshots']
    require(len(snapshots)==6 and {s['repository'] for s in snapshots}==set(REPOSITORIES),'SIX_SNAPSHOT_MEMBERSHIP')
    owners=value['owners'];ids=[r['owner_id'] for r in owners]
    require(len(owners)==276 and len(set(ids))==276,'OWNER_IDENTITY_UNIQUENESS')
    lookup={r['owner_id']:r for r in owners}
    for snapshot in snapshots:
        repo=snapshot['repository'];total,opened,closed,qualified=REPOSITORIES[repo]
        require(all(type(snapshot[k]) is int for k in ['issue_records','open_records','closed_records']),'SNAPSHOT_INTEGER_COUNTS')
        require((snapshot['issue_records'],snapshot['open_records'],snapshot['closed_records'])==(total,opened,closed),'COMPONENT_COUNTS')
        require(snapshot['qualified_source_commit']==qualified,'ACCEPTED_COMPONENT_SOURCE')
        rows=[r for r in owners if r['owner_id'].split('#')[0]==repo]
        require(len(rows)==total and sum(r['owner_state']=='OPEN' for r in rows)==opened and sum(r['owner_state']=='CLOSED' for r in rows)==closed,'BODY_STATE_ACCOUNTING')
        for row in rows:
            number=row['owner_id'].split('#')[1]
            require(number.isdecimal() and str(int(number))==number and int(number)>0,'OWNER_NUMBER')
            require(row['url']==f'https://github.com/{repo}/issues/{number}','OWNER_PUBLIC_LOCATOR')
            require(row['whole_contract_status']=='NOT_ESTABLISHED_BY_BODY_REVIEW','BODY_NOT_WHOLE_CONTRACT')
            require(type(row['qualification_credit']) is int and row['qualification_credit']==0,'BODY_NOT_CREDIT')
    require(ids==sorted(ids,key=lambda s:(s.split('#')[0],int(s.split('#')[1]))),'DETERMINISTIC_OWNER_ORDER')
    require(lookup['RobLe3/iicp-client-rust#3']['body_sha256']==lookup['RobLe3/iicp-client-rust#4']['body_sha256'],'DUPLICATE_BODY_NOT_ERASED')
    require(lookup['RobLe3/iicp-directory-php#11']['problem_class']=='OWNER_REPORTED_SUSPECTED_DEFECT','SUSPECTED_NOT_CONFIRMED')
    require(lookup['RobLe3/iicp-directory-php#60']['problem_class']=='CLOSED_CHANGE_OR_REVIEW_RECORD','CLARITY_NOT_DEMONSTRATED_DEFECT')
    corrections=value['selected_corrections']
    require(len(corrections)==17 and {r['owner_id'] for r in corrections}==SELECTED,'SELECTED_SOURCE_COHORT')
    for row in corrections:
        key=row['owner_id'];repo=key.split('#')[0]
        require(lookup[key]['owner_state']=='CLOSED' and row['owner_url']==lookup[key]['url'],'SELECTED_OWNER_JOIN')
        require(row['qualified_source_commit']==REPOSITORIES[repo][3],'QUALIFIED_SOURCE_JOIN')
        expected='POSTQUALIFIED_DEVELOPMENT_CORRECTION_ONLY' if key in DEVELOPMENT_ONLY else 'CORRECTION_SOURCE_IN_QUALIFIED_SOURCE'
        require(row['disposition']==expected,'TEMPORAL_SOURCE_CLASS')
        require(row['qualified_source_url']==f'https://github.com/{repo}/tree/'+row['qualified_source_commit'],'QUALIFIED_SOURCE_URL')
        require(row['correction_source_url']==f'https://github.com/{repo}/commit/'+row['correction_source_revision'],'CORRECTION_SOURCE_URL')
        require(row['new_native_validation'] is False and row['whole_issue_acceptance_verified'] is False,'SOURCE_NOT_NATIVE_OR_WHOLE_CLEARANCE')
        require(type(row['qualification_credit']) is int and row['qualification_credit']==0,'SOURCE_NOT_CREDIT')
    require([r['owner_id'] for r in corrections]==sorted(SELECTED,key=lambda s:(s.split('#')[0],int(s.split('#')[1]))),'DETERMINISTIC_CORRECTION_ORDER')
    require(sha(canonical(value))==JSON_PIN,'SNAPSHOT_IDENTITY')
    return True

def render(value):
    validate(value)
    lines=['# Six-component owner-body audit','',
      'This dated, non-authorizing supplement indexes **276 reviewed public issue bodies** from six '
      'component trackers: 261 CLOSED and 15 OPEN. It is not a count of defects, a proof of resolution, '
      'a complete historical archive or a corrected qualified baseline.','',
      '## Source universe and verification boundary','',
      'The snapshots were captured sequentially on 7 November 2026, approximately 15:11–15:12 UTC. '
      'Every CLOSED body in that declared snapshot has a reviewed interpretation; OPEN bodies have '
      'a separate scope disposition. This does not cover every comment, timeline, PR-only finding, '
      'private record or unfiled operational anomaly. Original body/snapshot bytes are retained in '
      'the controlled archive, not distributed here. Hashes identify those originals; they do not '
      'make missing or restricted content publicly available.','',
      '| Component tracker | Closed bodies | Open bodies | Total bodies |',
      '|---|---:|---:|---:|']
    for repo in sorted(REPOSITORIES):
        total,opened,closed,_=REPOSITORIES[repo]
        lines.append(f'| [{repo.split("/")[1]}](https://github.com/{repo}/issues) | {closed} | {opened} | {total} |')
    lines+=['| **Total** | **261** | **15** | **276** |','',
      'CLOSED is an owner-tracker state, not a claim that every unchecked acceptance clause passed. '
      'The machine-readable [audit](audit.json) preserves reported historical problems, requirements, '
      'suspected findings and uncertainty separately. Rust issues 3 and 4 retain both owner identities '
      'but identical source-body hashes; two records do not establish two distinct defect observations.','',
      '## Selected correction-source inclusions','',
      'Seventeen selected owner records have separate source joins: fourteen corrections are included '
      'in the qualified source; three are only in post-qualified development source. Some concern '
      'harness, packaging or release integrity. This is neither a complete defect register nor new '
      'native validation. Source ancestry and inspected code do not prove every acceptance clause, '
      'packaged-byte equivalence, runtime behavior or security property.','',
      '| Owner | Source disposition | Qualified source | Correction source |',
      '|---|---|---|---|']
    for row in value['selected_corrections']:
        label='development only' if row['owner_id'] in DEVELOPMENT_ONLY else 'included in qualified source'
        lines.append(f'| [{row["owner_id"]}]({row["owner_url"]}) | {label} | [{row["qualified_source_commit"][:10]}]({row["qualified_source_url"]}) | [{row["correction_source_revision"][:10]}]({row["correction_source_url"]}) |')
    lines+=['','The three development-only records concern SDK registration missing-token diagnostics. '
      'Their fixes do not transfer old credit to changed artifacts. Selected Windows source includes '
      'permission and IPC corrections, but this supplement runs no Windows tests. A named-pipe receive '
      'wait is bounded; subsequent cancellation/join is not claimed to have a universal bound. '
      'Directory TLS policy checks and strict seed-signature guards do not establish live TLS identity '
      'for every endpoint, complete authenticated snapshot bootstrap or joint federation interoperability.','',
      '## What remains open','',
      '- Full six-component supported-scope defect clearance.',
      '- Exact correction/reproduction/native-evidence joins beyond these selected slices.',
      '- Complete historical source discovery and preservation.',
      '- Corrected successor qualification and immutable functional-reference freeze.',
      '- Separately owned performance, representative-operation and release requirements.','',
      'The original qualification ledgers and five project-operated certificates remain authoritative '
      'for their original candidate. This supplement changes no accepted receipts, assignments, '
      'candidate, acceptance semantics or qualification credit. It establishes neither independent '
      'external certification nor release, deployment or publication authority.','',
      '## Reproduce public consistency checks','',
      '```sh','python3.13 -B scripts/owner_body_reference.py check',
      'python3.13 -B -m unittest discover -s tests -v','```','',
      'The checker verifies the pinned sanitized snapshot, schema, membership, counts, temporal classes, '
      'source links, privacy markers and generated Markdown. It does not fetch mutable GitHub issues '
      'or independently reproduce private originals, source execution or reviewer judgment. '
      'New analysis or changed snapshots require normal source review; the report-only publisher '
      'cannot modify this package.','',
      'Owner: [post-certification programme, root #1678](https://github.com/RobLe3/iicp.network/issues/1678). '
      'Historical preservation remains under [root #1676](https://github.com/RobLe3/iicp.network/issues/1676).','']
    return '\n'.join(lines)

def check():
    value=load();validate(value)
    require((DATA/'README.md').read_text()==render(value),'GENERATED_README')
    manifest=json.loads((DATA/'manifest.json').read_bytes())
    require(set(manifest)=={'schema','files','qualification_credit','whole_goal_complete'} and manifest['schema']=='iicp.owner-body-package-manifest.v1','MANIFEST_SHAPE')
    require(manifest['qualification_credit']==0 and manifest['whole_goal_complete'] is False,'MANIFEST_NOT_AUTHORITY')
    require(set(manifest['files'])=={'audit.json','audit.schema.json','README.md'},'MANIFEST_MEMBERS')
    require(all(sha((DATA/n).read_bytes())==pin for n,pin in manifest['files'].items()),'MANIFEST_DIGEST')
    return True

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['check','render']);args=parser.parse_args()
    if args.command=='check':check();print('PASS: dated owner-body/source snapshot consistency; no qualification credit or runtime validation')
    else:print(render(load()),end='')
if __name__=='__main__':main()
