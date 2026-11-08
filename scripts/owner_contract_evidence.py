"""Check a minimized owner-contract derivative, never original authority or credit."""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-owner-contract-evidence'
DATA_PIN='b353cf8cefc9343ad9a0f33ebbf4996c7fc6c445d5680fcfc086035483f0b8ac'
SCHEMA_PIN='eb43db68c8a8133d028dd6fdc8bc58f420d6c7c85117ece7c8b6fa1abca29df2'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(ok,message):
 if not ok:raise ValueError(message)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity differs');Draft202012Validator(json.loads(raw)).validate(v)
 require(v['owner_clause_accounting']=={'total':37,'checked_preserved':18,'unchecked_preserved':19,'checkbox_changes':0},'no owner progress inflation')
 require(len(v['clauses'])==19 and sum(v['category_counts'].values())==19 and v['category_counts']['REPRESENTATIVE_HUMAN_EVIDENCE']==6,'scope partition differs')
 b=v['boundaries'];require(all(type(x)is int and x==0 for k,x in b.items() if k in ['new_qualification_credit','owner_checkbox_changes','issue_closures','product_source_repairs','new_qualifying_tests']),'no new credit or edits');require(all(x is False for k,x in b.items() if k not in ['new_qualification_credit','owner_checkbox_changes','issue_closures','product_source_repairs','new_qualifying_tests']),'no maturity or authority promotion')
 require(v['package_context_joins']['existing_reference_count']==192,'existing proof scope');require(all(not r['whole_owner_clause_verified'] and not r['clean_install_transaction_proved_by_this_join'] for r in v['package_context_joins']['rows']),'partial evidence promoted')
 require(sha(canonical(v))==DATA_PIN,'reviewed derivative changed');return True
def render(v):
 validate(v);lines=['# Remaining owner contracts: evidence is not a defect count','',
 'The six component owners remain open with **18 of 37 clauses checked**. This supplement classifies the nineteen unchecked clauses without changing any checkbox, owner, acceptance rule or qualification credit.','',
 '## Nineteen open clauses, eight evidence classes','',
 '| Class | Clauses |','|---|---:|']
 lines += [f"| {cell(k.replace('_',' ').lower())} | {cell(count)} |" for k,count in v['category_counts'].items()]
 lines += ['',
 'Six clauses concern representative human evidence. Existing release/adoption owners retain those requirements; evidence reconciliation is not participant intake or a waiver. The other thirteen remain technical or conjunctive evidence work. An unchecked clause is not, by itself, a demonstrated product failure.','',
 '## Runtime metadata already has bounded declarations','',
 '| Component | Observed candidate version | Declared bound |','|---|---|---|']
 lines += [f"| {cell(r['component'])} | {cell(r['version'])} | `{cell(r['declared_runtime_bound'])}` |" for r in v['runtime_bounds']]
 lines += ['',
 'Qualified source, observed public-main metadata and exact frozen package members agree. The matrix declares CPython 3.11–3.14 and Node 22/24 runtime families. Version metadata alone does not restrict interpreter implementations. This does not prove every allowed patch/interpreter or the clauses’ post-matrix timing and publication conditions. **No runtime-bound source repair is proposed, and neither whole clause is marked complete.**','',
 '## Accepted package proof context','',
 'Three owner-clause joins reference **192 existing offline-lock coordinates**: Python 96, Rust 48 and TypeScript 48. Exact original proof and installed-context identities match; no SDK test was rerun.','']
 lines += ['- **'+name+':** '+text for name,text in v['package_context_joins']['materialized_context'].items()]
 lines += ['',
 'The raw selected predicate and its outer installed execution context must remain distinct. None of these joins completes the entire package/catalog owner clause.','',
 '## Representative gates remain separate','',
 'The canonical policy retains fourteen workflows, at least twenty observations each and 95% unassisted success per workflow, with the median inside its published budget and zero manual secret transfers or unresolved severe friction. Failures and abandonments remain in the denominator. Seven workflows are Management-specific.','',
 'At least 280 workflow observations would be needed to satisfy the fourteen independent minimums; that is **not** a requirement for 280 distinct people. Overall observation totals are not established by this audit. Intake remains closed; maintainer rehearsals and automation do not count as representative participants.','',
 '## Preserved observations','']+['- '+s for s in v['source_observation_notes']]
 lines += ['','## Validation and limits','',
 'Focused private synthetic controls passed: 16 metadata-snapshot, 25 owner-map and 18 existing-proof-join controls. Required source and exact-head reviews remain separate from those tests. Public checks validate this fixed derivative, not the original private artifacts.','']+['- '+s for s in v['limits']]
 lines += ['',
 'The [previous restoration-input audit](../2026-11-08-restoration-inputs/README.md) remains unchanged. No cloud, qualification workload, participant collection, package publication, production operation or release is authorized. The full post-certification programme remains incomplete.','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated narrative differs');expected={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'new_qualification_credit':0,'private_originals_distributed':False};require(json.loads((DATA/'manifest.json').read_text())==expected,'manifest differs');return True
if __name__=='__main__':check();print('PASS: minimized owner-contract evidence only; no new clause, runtime or qualification authority.')
