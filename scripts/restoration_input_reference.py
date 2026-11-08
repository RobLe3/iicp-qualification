"""Validate a minimized restoration-input derivative, not original runtime evidence."""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-restoration-inputs'
DATA_PIN='fd3951129bcf1542800fbb9b5facaf8e116fe9140c8bbe9806fa887e460ef34a'
SCHEMA_PIN='f268b5c96e35b5c5a7fd1b6af89d83a4e67f8b8eb755313f92bb490c659fc54e'
def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
def require(condition,message):
 if not condition:raise ValueError(message)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(value):
 privacy(value)
 schema=(DATA/'analysis.schema.json').read_bytes();require(sha(schema)==SCHEMA_PIN,'reviewed schema differs')
 Draft202012Validator(json.loads(schema)).validate(value)
 require(value['classification']['existing_assignment_references']==5808,'existing coordinate scope')
 require(value['classification']['component_scoped_groups']==529,'identity grouping scope')
 b=value['boundaries']
 require(type(b['qualification_credit']) is int and b['qualification_credit']==0 and type(b['new_assignment_credit']) is int and b['new_assignment_credit']==0,'no new credit')
 require(all(v is False for k,v in b.items() if k not in ['qualification_credit','new_assignment_credit']),'no evidence, execution or maturity promotion')
 require(value['new_raw_locator_question']['additional_locators']==0,'known hit is not additional discovery')
 require(sha(canonical(value))==DATA_PIN,'reviewed derivative changed')
 return True
def render(value):
 validate(value);c=value['classification'];a=value['original_metadata_availability'];q=value['new_raw_locator_question']
 lines=['# Original restoration inputs: identity and availability','',
 'This audit distinguishes recorded identities from retained original metadata and executable runtime restoration. It adds no qualification credit.','',
 '## Identity classification','',
 f"All {c['existing_assignment_references']:,} existing assignment references were grouped across six components and seven roles, producing {c['component_scoped_groups']} component-scoped groups. These are not new tests or missing-file counts.",'',
 '| Role | Distinct recorded digests |','|---|---:|']
 lines += [f"| {k.removesuffix('_sha256').replace('_',' ')} | {v} |" for k,v in c['distinct_digests_by_role'].items()]
 lines += ['','## Retained original metadata','',
 '| Identity unit | Resolved | Recorded |','|---|---:|---:|']
 for key,label in [('package_binding_identities','Full package bindings'),('qualification_environment_identities','Qualification environments'),('runtime_map_identities','Runtime maps')]:
  lines.append(f"| {label} | {a[key]['resolved']} | {a[key]['recorded']} |")
 lines += ['',
 'The resolved objects are macOS metadata. The raw prepared-result file matches the reference in all sixteen macOS receipts. A full binding identity match does not prove that installed trees, private transient inputs or executable environments remain available.','',
 '## Bounded locator result','',
 f"One new query examined {q['metadata_inventories']} retained metadata inventories for {q['distinct_raw_identities']} raw publication-file identities referenced by {q['receipt_references']} receipts. Its one hit was the already-known macOS publication: zero additional locators. Seven identities were unlocated in that prefix; global absence or evidence loss was not established.",'',
 '## Findings','']+['- '+s for s in value['findings']]
 lines += ['','## Preserved refusals and corrections','']+['- '+s for s in value['preserved_observations']]
 lines += ['','## Verification and limits','',
 'Focused synthetic metadata controls: 19 grouping, 17 binding-observer, 12 environment-observer and 8 locator-target/attempt controls passed. These do not execute products or establish runtime restoration. Exact non-authoring private reviews are pinned in the machine-readable derivative.','']+['- '+s for s in value['limits']]
 lines += ['',
 'The [original materialization report](../2026-11-08-original-materialization/README.md) remains unchanged. Canonical qualification authority remains the root records at `'+value['canonical_root_commit']+'`; candidate `'+value['candidate_digest']+'`.','',
 'No workload, cloud use, evidence promotion, deployment or release is authorized by this report.','']
 return '\n'.join(lines)
def check():
 value=load();text=render(value);require((DATA/'README.md').read_text()==text,'generated narrative differs')
 manifest={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'private_originals_distributed':False}
 require(json.loads((DATA/'manifest.json').read_text())==manifest,'generated manifest differs');return True
if __name__=='__main__':check();print('PASS: restoration-input reporting derivative only; no original object or runtime recheck.')
