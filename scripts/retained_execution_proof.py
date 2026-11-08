"""Check a fixed, minimized provenance derivative; never reads private originals."""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-retained-execution-proof'
DATA_PIN='d84ea1d08981ebb7cfee7d2b3567d4de5196d44506c48890e3f52f988155f632'
SCHEMA_PIN='6a6a8a2696437916b68d1a6c8a381546d098e4c7fd2f88e5cc7d4861a2961376'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def load():return json.loads((DATA/'analysis.json').read_bytes())
def require(ok,why):
 if not ok:raise ValueError(why)
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 require(v['schema']=='iicp.public-retained-execution-proof.v1','version')
 require(v['artifact_availability']['distinct_current_verified']==17 and v['artifact_availability']['prior_verified']==15 and v['artifact_availability']['additional_verified']==2,'distinct artifact accounting')
 require(all(v['boundaries'][k] is False for k in ['historical_inventory_complete','whole_supported_scope_clearance','reference_frozen','external_certification_established','release_authorized']),'no authority or completeness promotion')
 require(all(type(v['boundaries'][k]) is int and v['boundaries'][k]==0 for k in ['qualification_credit','new_product_test_executions','new_issue_body_coverage']),'no credit or new execution')
 require(len({r['name'] for r in v['artifact_availability']['records']})==2,'distinct exact artifacts')
 require(sha(canonical(v))==DATA_PIN,'reviewed derivative identity');return True
def render(v):
 validate(v)
 a=v['artifact_availability'];lines=['# Retained artifact bytes and historical validation provenance','',
 '**Current original artifact byte identities: 17/17 at examined retained locators.** The earlier [15/17 locator audit](../2026-11-08-reference-reproducibility/README.md) remains unchanged at its dated scope. A separately examined retained ZIP contains the two exact Rust Directory Linux x86-64 members. Their bytes and sizes match the frozen candidate; the executable was neither extracted nor executed.','',
 '| Additional retained member | Bytes | SHA-256 |','|---|---:|---|']
 for r in a['records']:lines.append(f"| {r['name']} | {r['size_bytes']} | `{r['sha256']}` |")
 lines+=['','This is current byte availability, not complete historical custody, full companion/build validation, clean-environment reproduction or a newly frozen reference. The original qualification authority is unchanged.','',
 '## Native x86 portability provenance','',
 'The final [Rust Directory137 closure comment](https://github.com/RobLe3/iicp-directory-rust/issues/137#issuecomment-5752636558) points to rootPR1452 and its admitted native x86 artifact/closure projections, not just the earlier ARM-only sourcePR138. The later qualified-source fragment records the digest-pinned Bookworm builder/runtime and glibc2.36. These are historical records, not a new execution or fresh cloud absence check.','',
 '## Shared database fixture and CI','',
 'PHP and Rust test fixtures are byte-identical to the pinned Protocol pre-normative fixture. Both exact historical heads have successful dedicated database-job metadata:','',
 '| Implementation | Tested head | Historical job |','|---|---|---|']
 for r in v['shared_database_validation']['historical_ci']:lines.append(f"| {r['repository']} | `{r['tested_head']}` | [run {r['run']}]({r['url']}) |")
 lines+=['','The workflows select real disposable database tests for a shared positive budget,3599/3600-second boundary,persisted repository/service reload and negative deltas. PHP uses MariaDB withpcntl; Rust selects its ignored MySQL test explicitly. Original detailed job-log endpoints returned HTTP410. Successful step metadata and test-source assertions are not a recovered per-assertion transcript or independently verified zero-skip count.','',
 'Reload is modeled by service/repository reinitialization, not an OS process restart. PHP concurrency-test source survives unchanged at the qualified source; Rust adds optional arguments at five heartbeat calls. Historical passing CI is not a rerun at the changed qualified source.','',
 '## Remaining gaps and boundaries','',
 'Rust SDK148 original27-case Docker detail remains owner-reported: a later successful cleanup-only receipt lacks the source/case bindings to substitute for that original result. The current [27 selected correction-source records](../2026-11-08-correction-source-joins/README.md) are unchanged. No whole owner issue or formal criterion is closed here.','']
 lines += ['- '+s for s in v['limits']]
 lines+=['','No new product or qualification workload, cloud operation, evidence promotion, private archive distribution, package publication, deployment or release. The programme remains incomplete. Public verification checks this reviewed derivative; it cannot rehash undistributed private archive members.','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated text differs')
 m={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'private_archive_distributed':False};require(json.loads((DATA/'manifest.json').read_text())==m,'manifest identity');return True
if __name__=='__main__':check();print('PASS: retained-evidence derivative only; no original workload verification.')
