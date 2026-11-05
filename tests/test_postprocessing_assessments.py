import copy
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('assessment_check',ROOT/'scripts/check_postprocessing_assessments.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Assessments(unittest.TestCase):
    def setUp(self):self.data=json.loads((m.PACKAGE/'assessments.json').read_text())
    def test_positive(self):self.assertTrue(m.validate(self.data))
    def test_balanced_disposition_swap_rejected(self):
        passing=next(r for r in self.data['criteria'] if r['reviewed_disposition']=='PASS')
        uncertain=next(r for r in self.data['criteria'] if r['reviewed_disposition']=='UNVERIFIED')
        passing['reviewed_disposition'],uncertain['reviewed_disposition']='UNVERIFIED','PASS'
        with self.assertRaisesRegex(ValueError,'record binding'):m.validate(self.data)
    def test_evidence_change_rejected(self):
        self.data['criteria'][0]['evidence'][0]['sha256']='sha256:'+'0'*64
        with self.assertRaisesRegex(ValueError,'record binding'):m.validate(self.data)
    def test_review_caveat_drop_rejected(self):
        row=next(r for r in self.data['criteria'] if r['review_notes'])
        row['review_notes']=[]
        with self.assertRaisesRegex(ValueError,'record binding'):m.validate(self.data)
    def test_mutations_rejected(self):
        changes=[lambda d:d.update(qualification_credit_added=1),lambda d:d['criteria'].pop(),
          lambda d:d['criteria'][0].update(reviewed_disposition='UNVERIFIED'),
          lambda d:d['dmsc'][0].update(external_experiment_status='PASS'),
          lambda d:d['dmsc'][0].update(related_receipt_ids=['invented']),
          lambda d:d['dmsc'][0].update(targets=['invented']),
          lambda d:d['dmsc'][0].update(supported_assertion='/Users/private'),
          lambda d:d['dmsc'][0].update(id='D02')]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                altered=copy.deepcopy(self.data);change(altered)
                with self.assertRaises(Exception):m.validate(altered)
if __name__=='__main__':unittest.main()
