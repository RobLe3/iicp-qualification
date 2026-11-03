"""Offline derivative joins; no workloads or mutation of accepted evidence."""

import copy
import sys
import unittest
from jsonschema.exceptions import ValidationError
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import qualification_analysis as qa


class AnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = qa.REPO / "reports/qualification-heritage/data"
        cls.inputs = {
            name: qa.load(data / (name + ".json"))
            for name in ("status", "receipts", "events", "scope")
        }
        cls.links = {
            "schema": "iicp.qualification-analysis-links.v1",
            "source_commit": cls.inputs["status"]["source_commit"],
            "requirements": [
                {
                    "id": "root-1470-clause-1",
                    "owner": "https://github.com/RobLe3/iicp.network/issues/1470",
                    "source_sha256": "sha256:" + "a" * 64,
                    "disposition": "UNRESOLVED",
                    "receipt_ids": [],
                    "mapping_status": "UNASSESSED",
                    "causal_status": "UNKNOWN",
                    "causal_parent_ids": [],
                }
            ],
            "history": [],
            "dmsc_sources": {
                "architecture_crosswalk": "sha256:fc966e33388ab934a0e6aafe2994eb18e6d5446c42038c81309097674c04dd92",
                "reviewer_crosswalk": "sha256:9fb95bf870e95b59aae12ca16aae1d77c3d69e317a33c7fa96522e07e637a3d2",
                "source_registry": "sha256:d047386446a4485b5fb5fa787bab9caf8bc56bc2b750f186fb58b930a47a6cc9",
            },
        }

    def test_positive_deterministic_complete_join(self):
        first = qa.generate(**self.inputs, links=self.links)
        self.assertEqual(first, qa.generate(**self.inputs, links=self.links))
        self.assertEqual(5808, len(first["assertions"]))
        self.assertEqual(64, len({r["receipt_id"] for r in first["assertions"]}))
        self.assertEqual(27, len(first["dmsc"]))
        self.assertTrue(all(r["assessment"] == "UNASSESSED" for r in first["dmsc"]))
        self.assertEqual(0, first["qualification_credit_added"])
        self.assertFalse(first["historical_inventory_complete"])

    def test_missing_receipt_rejected(self):
        values = copy.deepcopy(self.inputs)
        values["receipts"]["receipts"].pop()
        with self.assertRaises(ValueError):
            qa.generate(**values, links=self.links)

    def test_duplicate_link_rejected(self):
        links = copy.deepcopy(self.links)
        links["requirements"].append(links["requirements"][0])
        with self.assertRaises(ValidationError):
            qa.generate(**self.inputs, links=links)

    def test_foreign_receipt_link_rejected(self):
        links = copy.deepcopy(self.links)
        links["requirements"][0]["receipt_ids"] = ["foreign"]
        with self.assertRaises(ValueError):
            qa.generate(**self.inputs, links=links)

    def test_source_mismatch_rejected(self):
        links = copy.deepcopy(self.links)
        links["source_commit"] = "a" * 40
        with self.assertRaises(ValueError):
            qa.generate(**self.inputs, links=links)

    def test_private_extra_field_rejected(self):
        links = copy.deepcopy(self.links)
        links["requirements"][0]["private_locator"] = "/private/synthetic"
        with self.assertRaises(ValidationError):
            qa.generate(**self.inputs, links=links)

    def test_maturity_promotion_rejected(self):
        links = copy.deepcopy(self.links)
        links["requirements"][0]["disposition"] = "PASS"
        with self.assertRaises(ValidationError):
            qa.generate(**self.inputs, links=links)

    def test_inferred_cause_rejected(self):
        links = copy.deepcopy(self.links)
        links["history"] = [copy.deepcopy(links["requirements"][0])]
        links["history"][0]["causal_parent_ids"] = ["adjacent-event"]
        with self.assertRaises(ValidationError):
            qa.generate(**self.inputs, links=links)

    def test_changed_dmsc_pin_rejected(self):
        links = copy.deepcopy(self.links)
        links["dmsc_sources"]["architecture_crosswalk"] = "sha256:" + "b" * 64
        with self.assertRaises(ValidationError):
            qa.generate(**self.inputs, links=links)

    def test_foreign_scope_rejected(self):
        values = copy.deepcopy(self.inputs)
        values["scope"]["support_cells"].pop()
        with self.assertRaises(ValueError):
            qa.generate(**values, links=self.links)


if __name__ == "__main__":
    unittest.main()
