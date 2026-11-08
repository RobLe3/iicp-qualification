"""Validate a fixed public source-inclusion derivative; never execute products."""
import collections,hashlib,json,re
from pathlib import Path,PurePosixPath
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-correction-source-joins'
DATA_PIN='b51422811f9099d775b4811f2b2b7fc5d6a653b497ce5b6005354dc161e67aa3'
SCHEMA_PIN='135cec7fc5fec9133a974deb570742f0e04c7864bbaf3c8abe878b594a8cbdce'
CANDIDATE='sha256:e7c9aa192be21cdc5ee96e793ab97084137452653cde7580cffd22cf3890618a'
IDS={'RobLe3/iicp-client-rust#44','RobLe3/iicp-client-rust#146','RobLe3/iicp-client-rust#148','RobLe3/iicp-directory-php#95','RobLe3/iicp-directory-php#102','RobLe3/iicp-directory-rust#76','RobLe3/iicp-directory-rust#137'}
QUAL={'RobLe3/iicp-client-rust':'0b8b529262977b6482dd7900d473e7d152ba9293','RobLe3/iicp-directory-php':'2dfd228b49c587150a44f448cea1351a9f039d32','RobLe3/iicp-directory-rust':'b95a362ad8f974334994ca73cd20210388a2362f'}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(ok,message):
 if not ok:raise ValueError(message)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def source_ref(repo,r):
 require(r['source_commit']==QUAL[repo] and r['evidence_role']=='QUALIFIED_SOURCE_REFERENCE_NOT_EXECUTION','qualified source reference role/binding')
 path=PurePosixPath(r['repository_path']);require(not path.is_absolute() and '..' not in path.parts,'public repository path')
 require(bool(re.fullmatch('[0-9a-f]{64}',r['file_sha256'])) and type(r['line']) is int and r['line']>0,'source integrity/line')
 require(r['url']==f"https://github.com/{repo}/blob/{r['source_commit']}/{r['repository_path']}#L{r['line']}",'exact public source URL')
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 require(v['schema']=='iicp.public-additional-correction-source-joins.v1' and v['candidate_digest']==CANDIDATE,'original candidate binding')
 require(v['state']=='REVIEWED_SOURCE_INCLUSION_NOT_WHOLE_DEFECT_CLEARANCE','bounded source state')
 for k in ['qualification_credit','new_product_test_executions']:require(type(v[k]) is int and v[k]==0,'no runtime/credit')
 for k in ['whole_supported_scope_clearance','historical_inventory_complete','baseline_frozen','execution_authorized']:require(v[k] is False,'no authority/completeness promotion')
 require(v['counts']=={'prior_selected_records':20,'additional_selected_records':7,'total_selected_records':27,'qualified_source_inclusions':24,'development_only_corrections':3,'test_source_declarations':20,'body_records_already_reviewed':261,'new_body_coverage':0},'27selected records and20declarations, not new tests/body coverage')
 old=v['prior_selected_records'];rows=v['rows'];require(len(old)==len({r['issue'] for r in old})==20,'20distinct prior records')
 priorcounts=collections.Counter(r['disposition'] for r in old);require(priorcounts=={'CORRECTION_SOURCE_IN_QUALIFIED_SOURCE':17,'POSTQUALIFIED_DEVELOPMENT_CORRECTION_ONLY':3},'prior17/3 source partition')
 require(len(rows)==len({r['issue'] for r in rows})==7 and {r['issue'] for r in rows}==IDS,'seven distinct exact new source joins')
 require(not ({r['issue'] for r in rows}&{r['issue'] for r in old}),'no prior-record duplication')
 declarations=0
 for r in rows:
  require(r['repository']==r['issue'].split('#')[0] and r['qualified_source_commit']==QUAL[r['repository']],'issue/qualified source identity')
  require(r['issue_url']=='https://github.com/'+r['repository']+'/issues/'+r['issue'].split('#')[1],'issue URL')
  require(r['disposition']=='CORRECTION_SOURCE_IN_QUALIFIED_SOURCE','source inclusion not fresh runtime pass')
  require(r['native_validation_executed_here'] is False and r['whole_issue_acceptance_verified_here'] is False and type(r['qualification_credit']) is int and r['qualification_credit']==0,'row nonpromotion')
  require(len(r['source_refs'])>=3 and r['test_declarations'] and len(r['limits'])>=3,'source and limits required')
  for sr in r['source_refs']:source_ref(r['repository'],sr)
  for t in r['test_declarations']:
   source_ref(r['repository'],t['source_ref']);require(t['execution_here']=='NOT_EXECUTED','test-source existence is not pass');declarations+=1
 require(declarations==20,'20source declarations')
 ci=v['php95_original_ci_provenance'];require(ci['new_ci_execution'] is False and ci['qualification_credit']==0,'old CI is not a new run or qualification')
 require(len(ci['checks'])==len({x['id'] for x in ci['checks']})==len({x['name'] for x in ci['checks']})==5 and all(x['head_sha']==ci['original_pr_head'] and x['status']=='completed' and x['conclusion']=='success' for x in ci['checks']),'exact original successful check metadata')
 require(ci['detailed_job_log_readback']=='HTTP_410_NO_ASSERTION_OR_SKIP_TRANSCRIPT_ACQUIRED','no invented detailed historical runtime assertions')
 require(sha(canonical(v))==DATA_PIN,'reviewed derivative identity');return True

def render(v):
 validate(v)
 lines=['# Seven historical correction-source joins','',
 'This supplement adds seven reviewed source-inclusion records to the [prior selected register](../2026-11-07-release-recovery/README.md): **27 selected owner records, 24 correction-source inclusions in the qualified sources and three development-only corrections**. These are not 27 distinct current product defects, 27 whole-issue closures or new qualification results.','',
 'The existing 261 closed-body and 15 open-body reviews are reused. A duplicate 104-body pass was rejected as an agent work-selection error and adds zero coverage; its evidence is retained privately. No product or campaign failure is inferred from that error. The qualified candidate, accepted receipts and certificates remain unchanged.','',
 '## Exact source findings','', '| Owner | Qualified source finding | Source / test declaration references |','|---|---|---|']
 for r in v['rows']:
  first=r['source_refs'][0];lines.append(f"| [{cell(r['issue'])}]({r['issue_url']}) | {cell(r['scoped_source_finding'])} | [{len(r['source_refs'])} source anchors]({first['url']}); {len(r['test_declarations'])} test declarations |")
 lines+=['',
 'All seven correction commits or merges are ancestors of the exact original qualified component sources. Surviving source properties were inspected as well; ancestry alone would not establish that a change was not reverted. The machine-readable rows contain exact source commits, repository paths, file SHA-256 values, line anchors and test declaration names. Public source URLs link already-public component code, not private execution captures.','',
 'Twenty test declarations are listed, including baseline compatibility declarations in the Rust health CLI file. They are **not 20 newly executed or passing tests**. No product code, CLI, database, build, updater, probe or qualification workload was executed for this reconciliation.','',
 '## Limits retained per owner','']
 for r in v['rows']:
  lines+=['### '+r['issue'],'',f"Correction `{r['correction_commit']}`; qualified source `{r['qualified_source_commit']}`.",'']
  lines+=['- '+x for x in r['limits']];lines+=['']
 lines+=['## Original PHP concurrency CI provenance','',
 'For PHP #95, GitHub still supplies five completed-success check records at original PR head `1888fe5c3f4a1a97beeb9c4792a8e80a0cd4c706`, including `event-log-concurrency`. The [exact original workflow]('+v['php95_original_ci_provenance']['original_workflow_url']+') configures MariaDB 11.4, `DB_CONNECTION=mysql` and PHP 8.3 with `pcntl`/`pdo_mysql`, then selects the reputation concurrency test alongside the event and credit classes.','',
 'This is primary historical check metadata and workflow construction, not only a PR-author claim. However, the single bounded detailed-log read returned HTTP 410. No assertion or skip transcript was acquired. The check success must not be expanded into an independently rehydrated four-worker assertion result, nor into a new execution of later qualified source with metrics-idempotency changes. No CI was restarted.','',
 '## Review and engineering validation','',
 'The controlled source cohort passed independent non-authoring review. Forty current private metadata controls passed. The first staged control run had eight fixture-target errors because the separately typed Rust #146 record sorted first; the corrected tests select the intended inline-source variant explicitly. The verifier and source requirements were not weakened, and original failure evidence remains retained. Staged test totals are not summed.','',
 'A public integrity PASS checks this fixed derivative, source-reference formatting, row partitions, generated text and manifest. It does not re-fetch or execute source, reconstruct private context, validate original runtime assertions, prove packaging or confer qualification authority. Opaque controlled source-row digests require authorized retained inputs.','',
 'Run `python3.13 -B scripts/correction_source_joins.py` from the reviewed reporting checkout. Use the [reference crosswalk and artifact availability supplement](../2026-11-08-reference-reproducibility/README.md) for its separate 15/17 current-byte result; source inclusion here does not fill those locator gaps.','',
 'Existing owners [reference #1678](https://github.com/RobLe3/iicp.network/issues/1678) and [history #1676](https://github.com/RobLe3/iicp.network/issues/1676) retain their acceptance contracts. Whole supported-scope/operational clearance, final successor source selection, required separately authorized qualification, historical completeness and a frozen semantic reference remain unestablished. Held private disclosure gates remain unchanged.','',
 'No new qualification credit, cloud authority, historical deletion, package publication, deployment, independent external certification or release is granted. The full post-certification programme remains incomplete.','']
 return '\n'.join(lines)

def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated Markdown differs')
 require(json.loads((DATA/'manifest.json').read_bytes())=={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'product_tests_executed':0,'whole_issue_acceptance':False,'controlled_originals_distributed':False},'manifest differs');return True
if __name__=='__main__':check();print('PASS: fixed public correction-source joins; no original runtime or qualification validation.')
