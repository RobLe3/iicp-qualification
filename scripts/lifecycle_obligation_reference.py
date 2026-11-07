"""Verify a dated informational lifecycle contract map, not runtime conformance."""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-07-lifecycle-obligations'
DATA_PIN='a1dfdfa81fcbf08861b8e47896b827fc4db4318c07ea941114f0d342a0945cc6'
SCHEMA_PIN='1664f8130e5b9f86e2995b99d178f9823a74124243848646b658bf0db5dd6e8f'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(test,message):
 if not test:raise ValueError(message)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 require(len(v['obligations'])==len({x['obligation_id'] for x in v['obligations']})==10,'ten distinct obligations')
 require(len(v['vector_consumer_cells'])==len({(r['component'],r['vector_id']) for r in v['vector_consumer_cells']})==48,'48 unique vector/component cells')
 require(sum(r['fixture_state_label_walk'] for r in v['vector_consumer_cells'])==15,'15 state-only walks')
 require(sum(r['explicit_terminal_rejection_from_vector'] for r in v['vector_consumer_cells'])==1,'one explicit terminal rejection')
 require(len(v['source_blobs'])==40,'40 source blobs')
 require(sha(canonical(v))==DATA_PIN,'reviewed lifecycle derivative identity');return True
def source_link(ref):
 s=ref['source'];return f"https://github.com/{s['repository']}/blob/{s['commit']}/{s['path']}#L{ref['start_line']}-L{ref['end_line']}"
def render(v):
 validate(v)
 lines=['# Service lifecycle: obligations and source-consumer boundaries','','This is a reviewed source-bound reference supplement, not a new qualification result. It maps **10 amendment obligations**, **16 fixture vectors across three SDKs (48 source-consumer cells)** and **14 predicate source ranges**. Forty exact public-source blobs are retained by the controlled review. No SDK, HTTP adapter, backend, database, lifecycle diagnostic or qualification workload was run for this mapping.','',
 '## Keep the authority layers separate','','The frozen project feature baseline classifies service lifecycle as REQUIRED_STABLE within its coordinated scope. The underlying proposed profile remains 0.1.2-draft; its explicit opt-in amendment is 0.4.0-draft, and the portable fixture is 0.2.0-draft. Project scope does not ratify these drafts, require them for all base IICP conformance or mount control routes by default. The amendment explicitly adds expired/timed_out migration and negotiated replay; the earlier table alone is not evidence that those refinements are defects.','']
 for a in v['authority_layers']:lines.append(f"- [{a['id']}]({source_link(a['ref'])}): {a['status']}.")
 lines += ['','## Obligations, source predicates and limits','','Each link resolves to exact qualified or frozen source. A partial source join is not a whole-obligation PASS. The negotiation obligation is not mapped by this bounded review; that is not a claim that no negotiation tests exist elsewhere.','','| Obligation | Source predicates | Remaining limitation |','|---|---|---|']
 for o in v['obligations']:
  j=next(r for r in v['semantic_predicate_joins'] if r['obligation_id']==o['obligation_id']);refs='; '.join(f"[{r['ref_id']}]({source_link(r)})" for r in j['predicate_source_refs']) or ('[See selected transition-fixture consumers below](#what-the-selected-transition-fixture-consumers-actually-read)' if o['obligation_id']=='lifecycle-terminality-and-alias' else 'Not mapped in this batch')
  lines.append(f"| [{cell(o['obligation_id'])}]({source_link(o['authority_ref'])}) — {cell(o['required_behavior'])} | {refs} | {cell(j['limitation'])} |")
 lines += ['','## What the selected transition-fixture consumers actually read','','All three fixture copies match the exact frozen Protocol bytes. Their selected loops consume the five valid/alias vectors as state-label walks: 15 source applications. Those loops do not validate every supplied sequence or finality field. TypeScript also explicitly checks the LIFECYCLE-03 post-terminal refusal. These are source applications, not 16 newly executed tests or whole-fixture conformance. Other functions exercise related predicates, so an unconsumed entry is not a global test-absence finding.','','| Vector | Fixture expectation | Python loop | TypeScript loop | Rust loop |','|---|---|---|---|---|']
 for f in v['fixture_vector_domain']:
  cells=[]
  for c in ['client-python','client-typescript','client-rust']:
   r=next(r for r in v['vector_consumer_cells'] if r['component']==c and r['vector_id']==f['id']);label='State-label walk' if r['fixture_state_label_walk'] else 'Terminal refusal only' if r['explicit_terminal_rejection_from_vector'] else 'Not consumed here';cells.append(f"[{label}]({source_link(r['source_ref'])})")
  lines.append('| '+ ' | '.join([f['id'],cell(f['expected']),*cells])+' |')
 lines += ['','## Admission and reproducibility boundary','','The admitted process-crash scenarios select different functions from these transition-fixture loops. A source file appearing in a receipt cannot credit every function in that file. See the [materialized assertion context](../2026-11-07-materialized-assertions/README.md) for the accepted installed-package consumer paths. Original PASS results, receipts and certificates remain unchanged.','',
 'Python/Rust HTTP source assertions cover synthetic test adapters, not deployment identity or billing integration. Cancellation evidence levels are distinct: a requested cancellation, transport abort, backend acknowledgement, execution stop and released local handle are not interchangeable. Accounting helpers compare pure decisions, not prices or production ledger effects.','',
 'Run `python3.13 -B scripts/lifecycle_obligation_reference.py` from the reviewed reporting repository to verify fixed data/schema identity, generated Markdown and manifest. This check does not retrieve private archives, execute product tests or reproduce historical qualification. Complete semantic IFRB, historical preservation and corrected-candidate qualification remain separate gates.','',
 'This package grants no qualification credit, external interoperability or certification, baseline freeze, cloud access, deployment or release authority.','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated narrative differs')
 m=json.loads((DATA/'manifest.json').read_bytes());require(m=={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'runtime_executions':0,'whole_capability_verified':False},'manifest differs');return True
if __name__=='__main__':check();print('PASS: source-obligation derivative only; no runtime or qualification execution.')
