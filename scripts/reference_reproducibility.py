"""Validate a minimized evidence crosswalk; never execute or admit evidence."""
import collections
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-08-reference-reproducibility'
DATA_PIN='23c490062957d8b54e81cb58148f851d169205bdd51314f9567b0d6a825e2338'
SCHEMA_PIN='0c9f16aa87c4b5b3f71537cb1fd2cb3f1ab836dd0e2f3eac63989597f5b2b656'
CANDIDATE='sha256:e7c9aa192be21cdc5ee96e793ab97084137452653cde7580cffd22cf3890618a'
ROLES={'ANALYTICAL_REUSE_NOT_ADDITIONAL_OBSERVATION':36,'GAP_CONTEXT_NOT_GLOBAL_ABSENCE':19,'NON_NORMATIVE_COMPARISON':2,'REUSED_ORDINARY_CALLER_OBSERVATION':5,'REUSED_PARTIAL_MATCHING_PROJECTION':2,'REUSED_REVIEWED_BOUNDED_RUNTIME_ASSERTION':14,'REUSED_REVIEWED_PARTIAL_RUNTIME_ASSERTION':3,'REUSED_SOURCE_FUNCTION_OBSERVATION':9,'REUSED_SOURCE_HELPER_OBSERVATION':5,'SOURCE_INTERPRETATION_NOT_RUNTIME':4,'SOURCE_INTERPRETATION_NO_SELECTED_DIRECTORY_OBSERVATION':4}
SLICES={'protocol-body-predicates','rate-helper-fragments','capability-selection-pure-helpers','enclosing-capability-source-and-name-guard-observations','actual-sdk-submit-caller-controls','php-capability-kernel-method-witnesses','rust-directory-capability-kernel-method-witnesses','actual-rust-mysql-registration-readback','capability-assertion-depth-bridge'}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(ok,message):
    if not ok:raise ValueError(message)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
    privacy(v)
    raw=(DATA/'analysis.schema.json').read_bytes()
    require(sha(raw)==SCHEMA_PIN,'schema identity')
    Draft202012Validator(json.loads(raw)).validate(v)
    require(v['candidate_manifest_sha256']==CANDIDATE,'original candidate binding')
    for k in ['baseline_frozen','execution_authorized','historical_inventory_complete','whole_capability_completion']:
        require(v[k] is False,'no authority/completeness promotion')
    for k in ['qualification_credit','new_runtime_executions']:
        require(type(v[k]) is int and v[k]==0,'no new credit or execution')
    rows=v['links'];obligations=v['obligations'];counts=v['counts']
    require(len(rows)==len({r['id'] for r in rows})==counts['mapping_links']==103,'103 distinct typed links')
    require(len(obligations)==len({r['id'] for r in obligations})==counts['scoped_obligations']==43,'43 distinct scoped obligations')
    ids={r['id'] for r in obligations}
    require({r['slice_id'] for r in rows}==SLICES and counts['reference_slices']==counts['slices_with_scoped_links']==9,'nine selected slices')
    require(dict(collections.Counter(r['evidence_role'] for r in rows))==counts['by_evidence_role']==ROLES,'evidence role partition')
    require(counts['directory_bridge_original_statuses']=={'NOT_EXERCISED_IN_SELECTED_WITNESSES':19,'PARTIAL_OBSERVATION':3,'VERIFIED_BOUNDED_OBSERVATION':14},'original bridge accounting')
    require(counts['new_qualification_credit']==counts['new_runtime_executions']==0,'counted credit/runtime remain zero')
    for r in obligations:
        require(r['source_refs'] and r['whole_contract_satisfied'] is False,'obligation provenance and incomplete contract')
    for r in rows:
        require(r['obligation_id'] in ids,'dangling obligation')
        require(r['base_slice_node']=='ordinary-witness:'+r['slice_id'],'base slice identity')
        require(r['fresh_runtime_execution'] is False and r['whole_contract_satisfied'] is False and r['base_context_is_original_execution_proof'] is False,'link nonpromotion')
        require(type(r['new_qualification_credit']) is int and r['new_qualification_credit']==0,'no link credit')
        require(r['review_refs'] and r['scope_limit_count']>0,'review and scoped limits required')
        if r['evidence_role']=='GAP_CONTEXT_NOT_GLOBAL_ABSENCE':require(r['status']=='NOT_EXERCISED_IN_SELECTED_WITNESSES','gap is not observed pass')
        if r['evidence_role']=='ANALYTICAL_REUSE_NOT_ADDITIONAL_OBSERVATION':require(not r['observation_refs'],'analytical reuse is not additional observation')
    a=v['artifact_readiness'];artifacts=a['records']
    require(len(artifacts)==len({(r['component'],r['name']) for r in artifacts})==a['artifacts_required']==17,'17 original artifact identities')
    available=[r for r in artifacts if r['availability']=='AVAILABLE_AND_BYTE_VERIFIED_AT_EXAMINED_LOCATOR']
    missing=[r for r in artifacts if r['availability']=='UNRESOLVED_IN_EXAMINED_LOCATORS']
    require(len(available)==a['artifacts_byte_verified']==15 and len(missing)==a['artifacts_unresolved']==2,'15/2 examined artifact partition')
    require(all(r['verified_copy_count']>0 for r in available) and all(r['verified_copy_count']==0 for r in missing),'availability requires matching copies')
    require(sum(r['verified_copy_count'] for r in artifacts)==a['matching_copies']==16,'copies are not distinct artifacts')
    require(sum(r['observation_count'] for r in artifacts)==a['locator_observations']==37,'37 retained locator observations')
    for k in ['original_custody_established','full_reproducibility_established','archive_extraction','workload_executed']:
        require(a[k] is False,'artifact identity is not custody/execution/reproduction')
    require(len(v['retained_lineage'])==4 and len({r['slice_id'] for r in v['retained_lineage']})==4,'four retained lineage contexts')
    require(sha(canonical(v))==DATA_PIN,'reviewed derivative bytes')
    return True

def render(v):
    validate(v)
    lines=['# Reference obligations and original artifact availability','',
    'This additive supplement maps nine existing reference slices to 43 scoped obligations through 103 typed links. It also records current exact-byte availability for 15 of 17 original frozen artifacts at examined local locations. **It is not a frozen baseline, new qualification, complete preservation or a clean-environment reproduction.**','',
    'The [7 November assembly](../2026-11-07-functional-reference/README.md) remains a dated inventory-only snapshot for these nine later slices. This successor adds their reviewed obligation crosswalk without rewriting that earlier result. Original accepted qualification and receipts are unchanged.','',
    '## Evidence roles, not additional tests','',
    '| Role | Links |','|---|---:|']
    for role,n in sorted(v['counts']['by_evidence_role'].items()):lines.append(f'| {cell(role)} | {n} |')
    lines+=['',
    'Neither 103 links nor 43 obligations is a count of new tests or completed normative contracts. The analytical bridge reuses 36 earlier rows: 14 bounded observations, three partial and 19 not exercised in the selected witnesses. The four whole parent capability contracts remain unverified. A missing selected witness is not global absence of tests or a demonstrated product defect.','',
    'Source body predicates are synthetic helper checks, not endpoint or lifecycle execution. Rate-helper records with equal bytes retain separate provenance and must not be summed as independent fixture coverage. Caller observations use local synthetic transport seams: the retained three-SDK matrix has nine allowed-policy controls and six refusal controls, not an external authorization or provider execution experiment. Directory method observations retain their SQLite, memory or bounded MySQL environment limits.','',
    'Exact statements, scope-limit text and source bodies remain controlled. Public SHA-256 identifiers and JSON pointers preserve a route for an authorized resolver; they do not make private originals publicly retrievable. The machine-readable link rows retain evidence roles, polarity and scoped fields. Read those with their controlled limitations before drawing conclusions.','',
    '## Slice joins','', '| Slice | Links | Distinct scoped obligations |','|---|---:|---:|']
    for slice_id in sorted(SLICES):
        selected=[r for r in v['links'] if r['slice_id']==slice_id]
        lines.append(f"| {cell(slice_id)} | {len(selected)} | {len({r['obligation_id'] for r in selected})} |")
    lines+=['','Obligations may be shared across slices. Per-slice counts must not be summed into distinct global coverage. The 43 distinct IDs are inspectable in `analysis.json`; all whole-contract completion flags remain false.','',
    '## Original artifact availability','',
    'The frozen candidate binding is `'+v['candidate_manifest_sha256']+'`. The audit observed 37 exact local locators: 16 matching copies cover 15 distinct expected artifacts. Two remain unresolved at the examined locations. Filename and size alone were not credited as byte identity. No archive was extracted, no artifact executed, no rebuild or download performed and no source artifact changed.','',
    '| Component | Original artifact | Availability at examined locators | Matching copies |','|---|---|---|---:|']
    for r in v['artifact_readiness']['records']:
        lines.append(f"| {cell(r['component'])} | {cell(r['name'])} | {r['availability']} | {r['verified_copy_count']} |")
    lines+=['',
    'The unresolved Rust Directory Linux x86-64 binary and release manifest are not proven globally lost. The declared release tag did not resolve with existing repository access; a distribution declaration is not proof of publication. The local source universe is explicitly bounded, not an exhaustive historical discovery.','',
    'Exact matching bytes establish current content identity only. Companion manifests, build receipts, archive structure, original custody and clean-environment reproducibility remain separate checks. The guarded reader does not replace the existing candidate-artifact verifier. Its 13 synthetic controls passed; these are reader controls, not product qualification tests. IO figures reserve expected sizes rather than measure bytes read. Time checks are sampled before reads, not hard cancellation or proof of completion within a deadline.','',
    '## Failure history and review','',
    '| Slice | Preserved lineage classification |','|---|---|']
    for r in v['retained_lineage']:lines.append(f"| {cell(r['slice_id'])} | {cell(r['class'])} |")
    lines+=['',
    'Later success does not establish the cause of earlier failure. The PHP predecessor expected Laravel-default error structure; its HTTP 422 assertion passed, raw failure body was not retained and the final node-count assertion was not reached. The separate corrected test is not a product correction. The MySQL predecessor failures retain an unverified sole cause. Original failed stages, namespace refusals and reviewed successors remain distinct.','',
    'Private independent reviews accepted the scoped crosswalk and byte audit. During audit review, new packet file permissions were normalized to owner-only without changing bytes; the containing directory was already owner-only and no exposure was established. This is not evidence of a security defect in the frozen product.','',
    '## Verification and remaining gates','',
    'Run `python3.13 -B scripts/reference_reproducibility.py` in this reviewed checkout. It validates fixed public data/schema identity, joins, role partitions, artifact accounting, generated Markdown and manifest. It does not load private sources, repeat observations, execute products, verify qualification acceptance or establish custody. Source reproduction requires the retained controlled review inputs.','',
    'Historical completeness remains false. Supported-scope defect/operational reconciliation, final successor source selection, formally required successor qualification and a complete semantic baseline remain open. Use [reference owner #1678](https://github.com/RobLe3/iicp.network/issues/1678) and [historical owner #1676](https://github.com/RobLe3/iicp.network/issues/1676); this supplement closes neither acceptance contract.','',
    'No new qualification credit, whole-capability conformance, independent external certification, cloud authority, package publication, deployment or release is granted. The full post-certification programme remains incomplete.','']
    return '\n'.join(lines)

def check():
    v=load();text=render(v)
    require((DATA/'README.md').read_text()==text,'generated Markdown differs')
    expected={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'new_runtime_executions':0,'baseline_frozen':False,'private_sources_distributed':False}
    require(json.loads((DATA/'manifest.json').read_bytes())==expected,'manifest differs')
    return True
if __name__=='__main__':
    check();print('PASS: public scoped crosswalk/artifact accounting; not private reproduction or qualification.')
