import unittest,json,hashlib,copy,re
from pathlib import Path
from collections import Counter
from jsonschema import Draft202012Validator,ValidationError
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'reports/postcert/2026-11-06-successor-policy'
class PolicyProjection(unittest.TestCase):
 def setUp(self):self.x=json.loads((B/'requirements.json').read_text());self.schema=json.loads((B/'requirements.schema.json').read_text());self.v=Draft202012Validator(self.schema)
 def test_shape_positive(self):Draft202012Validator.check_schema(self.schema);self.v.validate(self.x)
 def test_integrity(self):
  for name,h in json.loads((B/'manifest.json').read_text())['files'].items():self.assertEqual(hashlib.sha256((B/name).read_bytes()).hexdigest(),h)
 def test_scope_matches_pinned_public_assignments(self):
  raw=(ROOT/'reports/analysis-v2/analysis.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),self.x['public_analysis_file_sha256']);data=json.loads(raw);self.assertEqual(data['candidate_manifest_sha256'],self.x['original_candidate_manifest_sha256']);counts=Counter((r['target'],r['kind']) for r in data['assertions']);r=self.x['conditional_requirements'];self.assertEqual(len(r['targets']),4)
  for t in r['targets']:self.assertEqual(t['support_cells'],counts[t['target'],'support_cells']);self.assertEqual(t['edge_executions'],counts[t['target'],'edge_executions']);self.assertEqual(t['campaign_shards'],16)
  self.assertEqual(r['totals'],{'shards':64,'support_cells':218,'edge_executions':5590});self.assertEqual(r['sentinel_entries'],4);self.assertEqual(r['source_bound_target_certificates']+r['ecosystem_certificate'],5)
 def test_no_authorization_promotion(self):
  self.x['execution_authorized']=True
  with self.assertRaises(ValidationError):self.v.validate(self.x)
 def test_no_certificate_issuance_promotion(self):
  self.x['certificate_issued']=True
  with self.assertRaises(ValidationError):self.v.validate(self.x)
 def test_no_credit_inflation(self):
  self.x['qualification_credit_added']=1
  with self.assertRaises(ValidationError):self.v.validate(self.x)
 def test_no_missing_target(self):
  self.x['conditional_requirements']['targets'].pop()
  with self.assertRaises(ValidationError):self.v.validate(self.x)
 def test_no_claim_public_private_source_reproduction(self):
  self.x['bounded_verification']['private_primary_proof_publicly_reproducible']=True
  with self.assertRaises(ValidationError):self.v.validate(self.x)
 def test_no_retention_certificate_conflation(self):
  self.assertTrue(self.x['determination']['artifact_row_retention_exists']);self.assertFalse(self.x['determination']['artifact_row_retention_is_different_candidate_certificate_eligibility']);self.assertFalse(self.x['determination']['unchanged_candidate_reporting_changes_automatically_require_requalification'])
 def test_no_private_material_or_commands(self):
  text=(B/'requirements.json').read_text()
  for marker in ['/Users/','/root/','arn:aws:','GHSA-','authorization.json','worktree','argv','source_code']:self.assertNotIn(marker,text)
  self.assertTrue(self.x['non_authorizing']);self.assertFalse(self.x['successor_frozen']);self.assertFalse(self.x['historical_inventory_complete']);self.assertFalse(self.x['independent_external_certification_established'])
 def test_primary_references_identify_source_not_new_authority(self):
  self.assertEqual(self.x['owner'],'RobLe3/iicp.network#1678');self.assertEqual(len(self.x['source_files']),7)
  for row in self.x['source_files']:self.assertEqual(row['repository'],'RobLe3/iicp.network');self.assertRegex(row['commit'],r'^[0-9a-f]{40}$');self.assertRegex(row['sha256'],r'^[0-9a-f]{64}$');self.assertTrue(row['path'].startswith('scripts/'))
 def test_unknown_field_rejected(self):
  self.x['new_acceptance_authority']='approved'
  with self.assertRaises(ValidationError):self.v.validate(self.x)
if __name__=='__main__':unittest.main()
