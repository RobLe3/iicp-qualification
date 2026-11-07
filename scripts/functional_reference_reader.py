"""Verify a minimized reference reader, not its private graph or qualification."""
import collections,hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-07-functional-reference'
DATA_PIN='00ae39c34b565e8f8019a57dfa45ca65000f20767ccf8cb93b9ac91e8c781562'
SCHEMA_PIN='6186cc30422218e63edab8c356df047a3b9404c9dff7a57625980183574d796d'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(ok,message):
 if not ok:raise ValueError(message)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 rows=v['case_rows'];counts=v['graph_counts'];require(len(rows)==len({r['case_id'] for r in rows})==counts['case_definitions']==147,'147 distinct case rows')
 require(sum(r['case_id'].endswith('::support') for r in rows)==counts['support_case_definitions']==6 and counts['edge_case_definitions']==141,'case partition')
 require(sum(r['accepted_reference_count'] for r in rows)==counts['accepted_assignment_references']==5808,'5808 prior coordinate references')
 require(sum(r['accepted_reference_count'] for r in rows if r['case_id'].endswith('::support'))==counts['support_assignment_references']==218 and counts['edge_assignment_references']==5590,'coordinate partition')
 require(len(v['capability_dispositions'])==len({r['capability_id'] for r in v['capability_dispositions']})==28,'28 distinct family dispositions')
 groups=collections.Counter(r['reference_scope_group'] for r in v['capability_dispositions']);require(groups=={'SUPPORTED_OR_CONDITIONAL_SCOPE_REVIEW':22,'BOUNDARY_AND_NONPROMOTION_REVIEW':6},'22/6 scope distinction')
 require(len(v['catalog_obligations'])==counts['catalog_obligations']==36 and len(v['lifecycle_obligations'])==counts['lifecycle_obligations']==10,'catalog/profile obligation distinction')
 require(len(v['reference_slices'])==counts['ordinary_witness_slices']==9 and all(r['obligation_crosswalk']=='NOT_ESTABLISHED_IN_THIS_ASSEMBLY_INVENTORY_ONLY' for r in v['reference_slices']),'later slices inventory only')
 require(sha(canonical(v))==DATA_PIN,'reviewed reader identity');return True

def short_terms(row):
 values=[]
 for t in row['predicate_terms']:
  value=t['value'];values.extend([value] if isinstance(value,str) else [str(x) for x in value] if isinstance(value,list) else [json.dumps(value,sort_keys=True)])
 return '; '.join(values) or 'Source-body reference only; code is not reproduced in this minimized reader.'
def render(v):
 validate(v);rows=v['case_rows']
 lines=['# Proposed functional reference: obligations, source predicates and evidence','','This source-bound reader connects the existing finite qualification to reviewed source assertions. It is **not a frozen functional baseline, a new qualification result or a successor selection**. The original prototype and accepted evidence remain unchanged.','',
 '## What this adds','','The controlled reference graph has 147 reviewed case-definition joins and 5,808 existing assignment references linked to 64 original receipts. The partition is six support definitions and 141 edge definitions, with 218 support and 5,590 edge references. These are reference relationships, not new executions or complete normative contracts.','',
 'The graph separates capability authority, 36 catalog expectations, ten scoped lifecycle obligations, reviewed source predicates, effective package context, accepted references and nine later reference slices. The later slices include analytical work and ordinary observations; their obligation crosswalk remains unestablished in this assembly. Do not sum them into qualification credit or family coverage.','',
 'The controlled documentation handoff provides the full graph and query tool. Case queries reach predicates, limits, staged context, assignments and receipts; an exact node-ID selector reaches other nodes. No runtime executor is supplied. The private graph and controlled review inputs are not distributed here. Their digests identify evidence without making private originals publicly retrievable.','',
 '## Existing catalog obligations','','Catalog expectations and actual selected predicates are separate. This public reader lists scenario identifiers/categories, not controlled catalog wording. Exact expectations remain in the private graph; opaque provenance does not authorize public disclosure. Follow the case rows below without treating a scenario name as proof of the whole expected behavior.','','| Catalog scenario | Category / expectation access | Case definitions | Existing references |','|---|---|---|---|']
 for o in sorted(v['catalog_obligations'],key=lambda x:x['scenario_id']):
  selected=[r for r in rows if r['scenario_id']==o['scenario_id']];lines.append(f"| {cell(o['scenario_id'])} | {cell(o['category'])} / controlled text not distributed | {len(selected)} | {sum(r['accepted_reference_count'] for r in selected)} |")
 lines+=['','## Family scope and explicit relations','','The 28 existing families split into 22 supported/conditional scope dispositions and six experimental/research/unsupported boundary dispositions. This is not 28 required positive execution families. Optional stable behavior requires its supported configuration; it is not blanket-excluded. An unmapped family means no exact relation in this assembly, not that no tests exist. No whole-family conformance is newly established.','','| Family | Existing classification | Disposition group | Relationship |','|---|---|---|---|']
 for r in v['capability_dispositions']:lines.append(f"| {cell(r['capability_id'])} | {r['classification']} | {r['reference_scope_group']} | {r['disposition']} |")
 lines+=['','## Case predicates, materialization and limits','','The 147 rows below preserve exact declared selectors and minimized reviewed interpretations. Scope prose that embeds controlled catalog expectations is minimized; exact private source values remain in the controlled graph. Case-map links identify original source selections, not standalone reproduction commands. Installed-package staging can rewrite imports/helpers or replace a selector with an installed probe. Read effective context with raw-source interpretations; neither overwrites the other. No product test or qualification workload was executed for this assembly.','','| Case / declared source | Selected reviewed predicate | Effective context and limits | Existing references |','|---|---|---|---|']
 for r in rows:
  raw=r['scope_interpretation_layer']=='RAW_DECLARED_SOURCE_SCOPE_REQUIRES_EFFECTIVE_CONTEXT'
  label='Historical/raw source limits (not exhaustive staged behavior): ' if raw else 'Selected source limits: '
  scope=label+'; '.join(r['limitation_terms']) if r['limitation_terms'] else label+'No additional prose limit exported; retain scoped flags and no-conformance boundary.'
  flags='Scoped source flags'+(' (historical/raw layer)' if raw else '')+': '+'; '.join(x['field']+'='+str(x['value']).lower() for x in r['scope_flags']) if r['scope_flags'] else ''
  context='; '.join('Effective staged layer: '+x['materialized_layer']+' Effect on prior interpretation: '+x['effect'] for x in r['effective_context_terms'])
  combined='; '.join(x for x in [scope,flags,context] if x)
  lines.append(f"| [{cell(r['case_id'])}]({r['case_map_url']}) | {cell(('Historical/raw predicate: ' if raw else 'Selected source predicate: ')+short_terms(r))} | {cell(combined)} | {r['accepted_reference_count']} |")
 lines+=['','## Lifecycle and remaining work','','The lifecycle supplement retains ten opt-in/pre-normative obligations. Nine have partial source joins; negotiation remains unmapped there. Project REQUIRED_STABLE classification does not ratify the draft or make its optional amendment a universal base-protocol requirement. See the [source-bound lifecycle supplement](../2026-11-07-lifecycle-obligations/README.md).','',
 'Remaining work includes scoped positive/negative semantic dispositions, explicit obligation crosswalks for ordinary reference slices, supported-scope operational clearance and the final source/artifact/regression/qualification decision. The [successor decision](../2026-11-07-successor-decision/README.md) keeps source selection and execution authority separate. Historical completeness remains false; receipt-byte availability does not prove complete private-output preservation. Existing owners remain [reference #1678](https://github.com/RobLe3/iicp.network/issues/1678) and [history #1676](https://github.com/RobLe3/iicp.network/issues/1676).','',
 '## Verification boundary','','Run `python3.13 -B scripts/functional_reference_reader.py` in the reviewed reporting checkout. It checks fixed public data/schema identity, internal partitions, generated text and manifest. It does not reconstruct the controlled graph, fetch private inputs, reproduce source analysis, execute a workload or confer qualification acceptance. Opaque controlled-input digests and JSON pointers require the authorized retained source resolver.','',
 'This package grants no qualification credit, reference freeze, independent external certification, cloud access, source publication outside this reviewed projection, package publication, deployment or release. The full post-certification programme remains incomplete.','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated reader differs');m=json.loads((DATA/'manifest.json').read_bytes());require(m=={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'new_runtime_executions':0,'baseline_frozen':False,'controlled_graph_distributed':False},'reader manifest differs');return True
if __name__=='__main__':check();print('PASS: minimized reference-reader integrity; no controlled-source or qualification validation.')
