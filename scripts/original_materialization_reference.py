"""Verify a minimized original-materialization derivative; never opens private artifacts."""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-original-materialization'
DATA_PIN='f7f6d40178f169876dc4373217ccf887e97aa37152efbaafff1c089a8b7b5a42'
SCHEMA_PIN='2674d040b6a3338826a8a6244fb6b6f98a8adebb8de6965f505794eca0395412'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(ok,why):
 if not ok:raise ValueError(why)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 require(v['verified_counts']=={'components':6,'artifacts':17,'package_build_companions':12,'files':29,'existing_assignment_materialization_references':5808,'existing_case_registry_joins':147},'original counts, not execution credit')
 b=v['boundaries'];require(all(x is False for k,x in b.items() if k not in ['qualification_credit','new_case_or_assignment_credit']),'no authority, execution, custody or restoration promotion');require(type(b['qualification_credit']) is int and b['qualification_credit']==0 and type(b['new_case_or_assignment_credit']) is int and b['new_case_or_assignment_credit']==0,'zero new credit')
 require(v['existing_index_reuse']['new_registry_created'] is False and v['existing_index_reuse']['templates_executed']==0,'reuse, not new executor')
 require(sha(canonical(v))==DATA_PIN,'reviewed derivative changed');return True
def render(v):
 validate(v);c=v['verified_counts'];scope=v['scope_preservation']
 lines=['# Original reference materialization:29files verified','',
 '**The unchanged root verifier passed for all six original candidate components:17artifacts plus12package/build companions.** Its materialization digest matches the original freeze record and all5808existing accepted assignment references.','',
 '| Measure | Verified |','|---|---:|',f"| Original components | {c['components']}/6 |",f"| Original artifact identities | {c['artifacts']}/17 |",f"| Original package/build companions | {c['package_build_companions']}/12 |",f"| Complete materialization files | {c['files']}/29 |",'',f"Candidate:`{v['candidate_digest']}`. Materialization:`{v['materialization_digest']}`.",'',
 '## Verification scope','',
 'The original composition receipt named the retained output root. The existing checker hashed files, validated original package/build documents and inspected Management tar member sets and executable modes. It did not build, install, extract or execute a product. Existing PASS fields were checked, not recreated or rerun.','',
 'The earlier48-path companion observation found10distinct exact companions at four bounded roots;22paths were absent and16held other historical versions. That result remains preserved. Following the original composition receipt resolved the full12companion set at its declared root. Absence at earlier roots was not global loss.','',
 'The earlier [17/17 artifact-byte supplement](../2026-11-08-retained-execution-proof/README.md) remains a dated result. This adds full original package/build-companion verification; it does not turn the original candidate into a corrected successor.','',
 'The local contract initially said no artifact reread. Full materialization verification necessarily reread17artifacts and12companions. A retrospective scope correction preserves that mismatch; it does not pretend the wording was updated beforehand or grant new standing authority.','',
 '## Reuse the existing reference machinery','',
 'All147existing case definitions match the accepted registry assertion marker, harness source, tracked-tree binding and outer driver template. A second driver registry is unnecessary. These joins are existing-source relationships, not147new tests.','',
 'Seven specific staging-context notes match39cases; this does not mean the other108lack generic staging. Raw aliases and unexpanded driver templates are not a standalone restored runtime.','',
 f"The [pinned Protocol feature baseline]({scope['feature_baseline_url']}) retains17required,2compatibility,3conditionaloptional and6experimental/research/unsupported families. No classification or applicable existing assertion is changed by this report.",'',
 '## Remaining gates','']
 lines+=['- '+s for s in v['remaining_gates']]
 lines+=['','## Limits','']+['- '+s for s in v['limits']]
 lines+=['','No cloud access, qualification workload, evidence promotion, package publication, deployment, external certification or release is authorized. The full post-certification programme remains incomplete.','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated text differs');m={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'private_originals_distributed':False};require(json.loads((DATA/'manifest.json').read_text())==m,'manifest identity');return True
if __name__=='__main__':check();print('PASS: reviewed original-materialization derivative only; no private-byte or runtime recheck.')
