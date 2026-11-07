"""Check a reviewed, informative successor decision; never select or qualify."""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy
from release_recovery_reference import cell
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'reports/postcert/2026-11-07-successor-decision'
DATA_PIN='f8d66b14139b7a4888bc9b31d33b73e3a54c35c811a9e6b7269e461ff2560e2e'
SCHEMA_PIN='71b1dee4d1738796d8e0ecf464d2a05f7442016a91c6b82567a83e315a2df9a8'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def require(test,message):
 if not test:raise ValueError(message)
def load():return json.loads((DATA/'analysis.json').read_bytes())
def validate(v):
 privacy(v);s=(DATA/'analysis.schema.json').read_bytes();require(sha(s)==SCHEMA_PIN,'schema identity');Draft202012Validator(json.loads(s)).validate(v)
 rows=v['component_source_rows'];counts=v['counts'];slots=v['artifact_slots']
 components={r['component'] for r in rows}
 require(len(rows)==len(components)==counts['components']==6,'six distinct components')
 require(len(slots)==len({r['slot_id'] for r in slots})==counts['original_artifact_slots']==17,'17 distinct original artifact slots')
 require({r['component'] for r in slots}==components,'artifact component partition')
 require(sum(len(r['changed_component_paths']) for r in rows)==counts['changed_component_paths']==71,'71 source-path rows')
 require(sum(r['public_head_changed_since_prior_audit'] for r in rows)==counts['public_component_heads_advanced_since_prior_audit']==4,'four advanced public heads')
 require(len(v['selected_advisory_source_rows'])==counts['selected_advisory_component_rows']==18,'18 selected advisory/component rows')
 require(len(v['maintained_source_floor_checks'])==counts['maintained_floor_lock_checks']==6,'six selected floor checks')
 require(len(v['decision_gates'])==6,'six unresolved decision gates')
 require(v['binding_rehearsal']['original_positive_controls']==64 and v['binding_rehearsal']['synthetic_candidate_digest_rejections']==64 and v['binding_rehearsal']['component_source_mutation_rejections']==384,'existing-helper control counts')
 require(all(not r['successor_source_selected'] for r in rows),'no source selection')
 require(all(r['successor_source_commit'] is None and r['successor_artifact_sha256'] is None for r in slots),'no successor artifacts')
 require(sha(canonical(v))==DATA_PIN,'reviewed decision identity');return True

def source_link(r):return f"https://github.com/{r['repository']}/blob/{r['commit']}/{r['path']}"
def render(v):
 validate(v)
 lines=['# Stabilization successor: source and qualification decision inputs','','**Prepare, do not launch or freeze.** This dated supplement connects six qualified component sources, six observed public development heads, seventeen original artifact slots and the existing candidate-binding policy. It selects no successor source or artifact and grants no qualification credit.','',
 'The original accepted campaign remains 64 shards, 218 support cells, 5,590 edge executions and five project-operated certificates for its frozen candidate. A corrected, zero-known-supported-defect reference is not established by those totals. The [existing stabilization owner](https://github.com/RobLe3/iicp.network/issues/1678) retains the incomplete acceptance contract.','',
 '## Source horizon, not automatic adoption','','These public heads were observed sequentially at the UTC times retained in analysis.json. They are not an atomic freeze. Four advanced since the earlier audit. The 71 changed component/path rows include source, dependency, configuration, fixture and tooling inputs; they are not 71 defects or artifact-equivalence results.','',
 '| Component | Qualified source | Observed public development source | Net changed paths |','|---|---|---|---|']
 for r in v['component_source_rows']:
  repo='https://github.com/'+r['repository']+'/tree/'
  lines.append(f"| {cell(r['component'])} | [{r['qualified_source'][:12]}]({repo+r['qualified_source']}) | [{r['observed_public_head'][:12]}]({repo+r['observed_public_head']}) | {len(r['changed_component_paths'])} |")
 lines += ['','The machine-readable slot table retains all seventeen original artifact identities and build/package-manifest digests. Every successor slot is explicitly unselected. A source-path count or unchanged version label is not artifact identity. Any justified reuse of exact artifact bytes is distinct from carrying qualification credit to a changed candidate.','',
 '## What the metadata controls establish','','The retained review ran only the existing candidate-binding helper against derived views of the 64 accepted receipts: 64 original positive controls passed, 64 synthetic changed-candidate controls were rejected, and six component-source mutations produced 384 rejections. These are helper applications, not qualification executions. The synthetic substitutions are contradictory controls, not valid newly built candidate manifests.','',
 'This does not reproduce complete receipt validation, package proofs, environment safety, preservation/closure checks or certificate compilation. No original receipt was changed and no new receipt was issued.','',
 '## Selected dependency evidence, not an exploitability assessment','','The maintained floor functions reject the three qualified Cargo locks and accept the three observed development locks. This compares selected source policy and locked versions; it is not a fresh complete vulnerability audit, compiled-feature result or demonstration of exploitation. Public source owners already maintain the dependency updates; this supplement does not recreate or automatically adopt them.','',
 '| Component | Advisory source | Qualified locked version / range disposition | Development locked version / range disposition |','|---|---|---|---|']
 for r in v['selected_advisory_source_rows']:
  versions=r['versions'];q=versions['qualified'];d=versions['public-development']
  lines.append(f"| {cell(r['component'])} | [{r['advisory_id']}]({r['primary_source']['public_page']}) | {cell(q['version'])}: {cell(q['range_status'])} | {cell(d['version'])}: {cell(d['range_status'])} |")
 lines += ['','Advisory conditions remain material: qualified rustls 0.23.45 is already patched for [0285](https://rustsec.org/advisories/RUSTSEC-2026-0285.html). [0348](https://rustsec.org/advisories/RUSTSEC-2026-0348.html) concerns non-default Brotli certificate decompression; applications without that feature are unaffected. [0382](https://rustsec.org/advisories/RUSTSEC-2026-0382.html) requires the specified certificate-anchor/path conditions. [0386](https://rustsec.org/advisories/RUSTSEC-2026-0386.html) is an informational Unix AsyncFd safety finding, not a Windows exposure finding. [0338](https://rustsec.org/advisories/RUSTSEC-2026-0338.html) concerns unordered reads rather than the default ordered path. [0343](https://rustsec.org/advisories/RUSTSEC-2026-0343.html) affects quinn-proto 0.11.17, not 0.11.15/0.11.16, and excludes the specified safe datagram API. Exact upstream revisions and digests are in analysis.json. None of these lock comparisons establishes an affected IICP runtime path.','',
 '## Consolidated remaining decisions','','1. Complete supported-scope and operational dispositions, including explicit unresolved evidence and controlled source prerequisites.','2. Select the exact minimal corrected sources and version/candidate identity; do not automatically adopt public main.','3. Bind all final artifacts, dependencies, build/package manifests, environments, harnesses and assignments.','4. Independently review corrected-defect regressions and the formal qualification required by current policy.','5. Obtain separate applicable execution and resource authority.','6. Freeze only after required regressions, qualification, certificates and supported-scope defect clearance pass.','',
 'The existing target compiler requires sixteen receipts with shard indices 0–15 per target; the ecosystem compiler joins four targets. Candidate-bound admission remains separate and adds no duplicate campaign credit. This is not an automatic schedule, a decision about additional admission executions, or a rule that every documentation/tooling edit outside an unchanged candidate reruns workloads. Scoped compatibility research under #1588 is not an existing exception.','',
 '## Pinned policy sources','']
 for r in v['policy_sources']:lines.append(f"- [{r['path']}]({source_link(r)}), SHA-256 `{r['sha256']}`.")
 lines += ['','## Reproduce and limits','','Run `python3.13 -B scripts/successor_decision_reference.py` from the reviewed reporting checkout. It verifies the fixed public data/schema, internal partitions, generated narrative and manifest. It does not fetch private records, rerun the retained helper controls, execute product tests or establish current source freshness. The controlled source review retains those separate inputs and results.','',
 'This is an informational derivative, not qualification authority, a frozen executable reference, external certification, cloud authorization, package publication, deployment or release permission. Historical completeness and the full post-certification programme remain incomplete.','']
 return '\n'.join(lines)
def check():
 v=load();text=render(v);require((DATA/'README.md').read_text()==text,'generated narrative differs')
 m=json.loads((DATA/'manifest.json').read_bytes());require(m=={'analysis_sha256':DATA_PIN,'schema_sha256':SCHEMA_PIN,'readme_sha256':sha(text.encode()),'qualification_credit':0,'qualification_workloads':0,'successor_sources_selected':0,'successor_artifacts_bound':0,'baseline_frozen':False},'manifest differs');return True
if __name__=='__main__':check();print('PASS: informative successor-decision derivative; no source selection or qualification execution.')
