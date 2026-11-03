"""Independent partition accounting controls, synthetic and zero-credit."""

import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import heritage_partitions as hp
import test_heritage


class PartitionReviewTests(unittest.TestCase):
    setUp = test_heritage.HeritageTests.setUp

    def inventory(self, page):
        with patch.object(
            hp.heritage, "load_canonical", return_value=copy.deepcopy(self.canonical)
        ):
            return hp.inventory_partition(self.config, page)

    def test_bounded_gap_survives_inventory_and_summary(self):
        (self.root / "extra").write_text("x")
        with patch.object(hp, "DIRECTORY_LIMIT", 1):
            page = hp.discover(self.config, steps=1)
        result = self.inventory(page)
        self.assertEqual(result["partition"]["gaps"], page["gaps"])
        self.assertEqual(
            result["parent_config_sha256"], hp.sha(hp.canonical(self.config))
        )
        summary = hp.validate_chain(self.config, [page])
        self.assertTrue(summary["discovery_exhausted"])
        self.assertFalse(summary["discovery_complete"])
        self.assertEqual(summary["unresolved_discovery_gaps"], 1)
        self.assertFalse(summary["historical_inventory_complete"])

    def test_explicit_pin_not_double_inspected_across_pages(self):
        pages = []
        values = []
        while not pages or not pages[-1]["discovery_exhausted"]:
            pages.append(hp.discover(self.config, pages[-1] if pages else None, 1))
            values.append(self.inventory(pages[-1]))
        objects = [x for v in values for x in v["inventory"]["objects"]]
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0]["relative_path"], "receipt.json")
        self.assertTrue(hp.validate_chain(self.config, pages)["discovery_complete"])

    def test_gap_traversal_refused_even_rehashed(self):
        (self.root / "extra").write_text("x")
        with patch.object(hp, "DIRECTORY_LIMIT", 1):
            page = hp.discover(self.config, steps=1)
        page["gaps"][0]["relative_path"] = "../outside"
        page["page_sha256"] = hp.sha(
            hp.canonical({k: v for k, v in page.items() if k != "page_sha256"})
        )
        with self.assertRaises(ValueError):
            hp.validate(page, self.config)

    def test_wrong_parent_inventory_binding_refused(self):
        result = self.inventory(hp.discover(self.config, steps=1))
        result["parent_config_sha256"] = "sha256:" + "0" * 64
        with self.assertRaises(ValueError):
            hp.validate_inventory(self.config, result)

    def test_previously_scanned_directory_change_refused(self):
        page = hp.discover(self.config, steps=1)
        (self.root / "new").write_text("x")
        with self.assertRaises(ValueError):
            hp.discover(self.config, page, 1)


if __name__ == "__main__":
    unittest.main()
