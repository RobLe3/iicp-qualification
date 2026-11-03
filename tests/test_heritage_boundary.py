"""Heritage never expands the existing report publisher's authority."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import report_common


class HeritagePublisherBoundary(unittest.TestCase):
    def test_generated_file_allowlist_is_unchanged(self):
        expected = ('reports/status.json', 'reports/receipts.json',
                    'reports/events.json', 'reports/STATUS.md')
        policy = json.loads((ROOT / 'reporting-policy.json').read_text())
        self.assertEqual(tuple(policy['automatic_publication']['allowed_paths']), expected)
        self.assertEqual(report_common.REPORT_FILES, expected)
        self.assertTrue(policy['automatic_publication']['human_review_required_for_other_changes'])
        self.assertFalse(policy['automatic_publication']['source_authority_changes_allowed'])
        self.assertFalse(policy['automatic_publication']['raw_evidence_upload_allowed'])
        self.assertFalse(policy['automatic_publication']['qualification_execution_allowed'])

    def test_existing_completeness_claim_remains_false(self):
        status = json.loads((ROOT / 'reports/status.json').read_text())
        self.assertIs(status['historical_inventory_complete'], False)


if __name__ == '__main__':
    unittest.main()
