import copy,sys,pathlib,unittest
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
import original_materialization_reference as m
class Controls(unittest.TestCase):
 def test_positive(self):self.assertTrue(m.validate(m.load()))
 def test_generated(self):self.assertTrue(m.check())
 def test_schema_tamper(self):
  old=pathlib.Path.read_bytes
  def wrong(path):return b'{}' if path.name=='analysis.schema.json' else old(path)
  with patch.object(pathlib.Path,'read_bytes',wrong):
   with self.assertRaises(ValueError):m.validate(m.load())
 def test_private_extra_field(self):
  v=m.load();v['private_locator']='/Users/synthetic/private'
  with self.assertRaises(Exception):m.validate(v)
changes=[
 ('candidate',('candidate_digest',),'sha256:'+'0'*64),
 ('materialization',('materialization_digest',),'sha256:'+'0'*64),
 ('file_count',('verified_counts','files'),30),
 ('companion_count',('verified_counts','package_build_companions'),11),
 ('artifact_count',('verified_counts','artifacts'),18),
 ('case_count',('verified_counts','existing_case_registry_joins'),148),
 ('assignment_count',('verified_counts','existing_assignment_materialization_references'),5809),
 ('template_execution',('existing_index_reuse','templates_executed'),1),
 ('duplicate_registry',('existing_index_reuse','new_registry_created'),True),
 ('qualification_credit',('boundaries','qualification_credit'),1),
 ('new_case_credit',('boundaries','new_case_or_assignment_credit'),1),
 ('product_execution',('boundaries','product_execution'),True),
 ('runtime_restore',('boundaries','runtime_restoration_proved'),True),
 ('historical_custody',('boundaries','historical_custody_proved'),True),
 ('historical_complete',('boundaries','historical_inventory_complete'),True),
 ('successor_selected',('boundaries','corrected_successor_selected'),True),
 ('freeze',('boundaries','corrected_reference_frozen'),True),
 ('release',('boundaries','release_authorized'),True),
 ('external_certification',('boundaries','external_certification_established'),True),
 ('classification_change',('scope_preservation','classification_changes'),1),
 ('waiver',('scope_preservation','applicable_existing_obligations_waived'),1),
 ('erase_scope_mismatch',('scope_history','prior_local_no_reread_clause_exceeded'),False),
 ('invent_precommitment',('scope_history','correction_recorded_after_observation'),False),
 ('authority_expansion',('scope_history','standing_goal_authority_expanded'),True),
 ('io_measurement',('original_checker','measured_total_io_bytes_available'),True),
 ('foreign_checker',('original_checker','source_files',0,'file_sha256'),'0'*64),
 ('original_changed',('boundaries','accepted_records_changed'),True),
 ('extraction',('boundaries','artifact_extraction'),True),
 ('other_case_missing',('existing_index_reuse','other_cases_inferred_missing_staging'),True),
 ('drop_history',('prior_limited_companion_observation','prior_observation_preserved'),False)]
def control(path,value):
 def run(self):
  v=m.load();node=v
  for part in path[:-1]:node=node[part]
  assert path[-1] in node if isinstance(node,dict) else 0<=path[-1]<len(node)
  node[path[-1]]=value
  with self.assertRaises(Exception):m.validate(v)
 return run
for name,path,value in changes:setattr(Controls,'test_refuse_'+name,control(path,value))
if __name__=='__main__':unittest.main()
