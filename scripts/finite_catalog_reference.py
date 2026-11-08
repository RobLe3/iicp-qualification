"""Verify a fixed finite-catalog analytical derivative; never admit evidence."""
from pathlib import Path
from collections import Counter
import hashlib,json
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-finite-catalog-semantics'
DATA_PIN='183fe1013d4d7dec69bc2e53c67ff0b23316b90c917a2b8d1a9fa8c869b3329a'
SCHEMA_PIN='13d456de3ee33a69e9fd34debae151a64a6f9de4157ab735af6545571ad0b20f'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def require(ok,reason):
 if not ok:raise ValueError(reason)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);raw=(DATA/'analysis.schema.json').read_bytes();require(sha(raw)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(raw)).validate(v)
 rows=v['scenario_analysis'];cases=[c for r in rows for c in r['cases']]
 require(len(rows)==len({r['scenario_id'] for r in rows})==36,'scenario scope')
 require(len(cases)==len({c['case_id'] for c in cases})==141,'case scope')
 require(sum(c['existing_accepted_reference_count'] for c in cases)==5590,'reference scope')
 require(Counter(c['source_fit'] for c in cases)==v['counts']['source_fit_counts'],'fit accounting')
 require(v['counts']['source_fit_counts']=={'DIRECT_FINITE_PROPERTY':50,'PARTIAL_EXPECTATION_WITNESS':74,'CROSS_CASE_COMPLEMENT_REQUIRED':3,'PREPARATION_CONTRACT_JOIN_REQUIRED':11,'APPLICABILITY_CLARIFICATION_REQUIRED':3},'fit scope')
 require(v['counts']['cross_case_coordinate_pairs']==192 and v['counts']['cross_case_environment_matched_pairs']==125 and v['counts']['cross_case_environment_different_pairs']==67,'context comparison scope')
 for k,x in v['boundaries'].items():
  if k in {'new_qualification_credit','new_qualifying_tests','runtime_witness_joins_verified'}:require(type(x)is int and x==0,'credit/runtime inflation')
  else:require(x is False,'maturity or disclosure inflation')
 require(sha(canonical(v))==DATA_PIN,'reviewed derivative identity');return True
def render(v):
 validate(v)
 lines=['# Finite catalog: source properties, context and remaining evidence','','This reviewed source interpretation adds no product correction, workload, qualification credit or frozen reference. Exact controlled catalog wording remains private.','',
 '## Scope and different units','','- **36 scenario interpretations**, covering **141 existing edge definitions** and **5,590 accepted reference coordinates**.','- **50 direct finite source properties**, **74 partial witnesses**, **3 cross-case complements**, **11 preparation-contract joins** and **3 applicability clarifications**. These are not completed requirement counts.','- **192 cross-case coordinate pairs**:125 have equal retained environment metadata;67 differ. **Zero newly verified runtime witness joins**.','- **52 private synthetic controls passed**, followed by bounded non-authoring source review. Public validation is a separate fixed-derivative check, not a qualification rerun.','',
 '## How to read this','','The original accepted campaign remains authoritative and unchanged. A source-witness gap is not a demonstrated product failure. A direct finite property is not whole catalog conformance. Do not promote raw test names, source existence, modeled error handling or current preparer code into historical runtime evidence.','',
 'The original PHP rate feature case asserts a Retry-After response header; the later offline clamp expression is a separate slice. The confidentiality downgrade and partial-response expectations permit alternative branches: disclose unexamined alternatives without requiring every alternative to recognize a selected finite property.','',
 '## Source-grounded scenario interpretations','']
 for row in v['scenario_analysis']:
  lines+=['### '+row['scenario_id'],'',row['interpretation'],'']
  for c in row['cases']:
   lines+=['- **'+c['component']+' — '+c['source_fit']+'**: '+c['supported_source_property'],
           '  Limit/gap: '+c['unresolved_or_excluded_scope'], '  Next evidence action: '+c['next_evidence_action']]
  lines+=['']
 lines+=['## Limits','']+['- '+x for x in v['limitations']]
 lines+=['','See [source/provenance notes](SOURCES.md), the [earlier functional reader](../2026-11-07-functional-reference/README.md), [Directory adapter supplement](../2026-11-08-directory-contract-semantics/README.md) and [canonical status](../../STATUS.md).','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'narrative differs')
 expected={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'new_qualification_credit':0,'private_originals_distributed':False}
 require(json.loads((DATA/'manifest.json').read_text())==expected,'manifest differs');return True
if __name__=='__main__':check();print('PASS: fixed finite-catalog source interpretation; no qualification authority.')
