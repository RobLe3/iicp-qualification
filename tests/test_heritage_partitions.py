"""Bounded private partition discovery controls."""

import copy
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import heritage_partitions as hp
import test_heritage


class PartitionTests(unittest.TestCase):
    setUp = test_heritage.HeritageTests.setUp

    def pages(self, steps):
        pages = []
        while not pages or not pages[-1]["discovery_exhausted"]:
            pages.append(hp.discover(self.config, pages[-1] if pages else None, steps))
        return pages

    def test_resume_matches_single_discovery(self):
        (self.root / "a").mkdir()
        (self.root / "a" / "x").write_text("x")
        small = self.pages(1)
        large = self.pages(20)
        self.assertEqual(
            [r for p in small for r in p["records"]],
            [r for p in large for r in p["records"]],
        )
        self.assertTrue(hp.validate_chain(self.config, small)["discovery_exhausted"])
        self.assertEqual(self.pages(1), small)

    def test_config_or_checkpoint_tampering_refuses(self):
        page = hp.discover(self.config, steps=1)
        changed = copy.deepcopy(self.config)
        changed["max_file_bytes"] += 1
        with self.assertRaises(ValueError):
            hp.discover(changed, page)
        page["frontier"] = []
        with self.assertRaises(ValueError):
            hp.discover(self.config, page)

    def test_missing_duplicate_pages_refused(self):
        pages = self.pages(1)
        with self.assertRaises(ValueError):
            hp.validate_chain(self.config, pages[1:])
        with self.assertRaises(ValueError):
            hp.validate_chain(self.config, pages + [pages[-1]])

    def test_changed_queued_directory_refuses(self):
        (self.root / "a").mkdir()
        page = hp.discover(self.config, steps=1)
        (self.root / "a" / "new").write_text("new")
        with self.assertRaises(ValueError):
            hp.discover(self.config, page)

    def test_symlink_not_followed(self):
        (self.root / "link").symlink_to("/tmp")
        pages = self.pages(20)
        self.assertIn(
            {"root_id": "fixture", "relative_path": "link"}, pages[0]["records"]
        )
        with patch.object(
            hp.heritage, "load_canonical", return_value=copy.deepcopy(self.canonical)
        ):
            inv = hp.inventory_partition(self.config, pages[0])["inventory"]
        self.assertEqual(
            next(r for r in inv["objects"] if r["relative_path"] == "link")[
                "availability"
            ],
            "UNSAFE",
        )

    def test_directory_bound_is_gap_not_completeness(self):
        with patch.object(hp, "DIRECTORY_LIMIT", 1):
            (self.root / "extra").write_text("x")
            page = hp.discover(self.config, steps=1)
        self.assertEqual(page["gaps"][0]["code"], "directory-bound")
        self.assertFalse(page["historical_inventory_complete"])

    def test_existing_output_and_public_output_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d).resolve() / "out.json"
            path.write_text("preserve")
            with self.assertRaises(FileExistsError):
                hp.heritage.write_private(path, {})
            self.assertEqual(path.read_text(), "preserve")

    def test_partition_preserves_gaps_and_pin_once(self):
        pages = self.pages(1)
        inventories = []
        for page in pages:
            with patch.object(
                hp.heritage,
                "load_canonical",
                return_value=copy.deepcopy(self.canonical),
            ):
                result = hp.inventory_partition(self.config, page)
            hp.validate_inventory(self.config, result)
            inventories.append(result)
        ids = [o["evidence_id"] for p in inventories for o in p["inventory"]["objects"]]
        self.assertEqual(len(ids), len(set(ids)))
        changed = copy.deepcopy(inventories[0])
        changed["partition"]["gaps"].append(
            {
                "code": "unsafe-root",
                "root_id": "fixture",
                "relative_path": "",
                "directory_stamp": None,
            }
        )
        with self.assertRaises(ValueError):
            hp.validate_inventory(self.config, changed)

    def test_changed_content_is_mismatch_not_credit(self):
        page = hp.discover(self.config, steps=20)
        (self.root / "receipt.json").write_text("modified")
        with patch.object(
            hp.heritage, "load_canonical", return_value=copy.deepcopy(self.canonical)
        ):
            result = hp.inventory_partition(self.config, page)
        self.assertEqual(result["inventory"]["objects"][0]["integrity"], "MISMATCH")
        self.assertEqual(
            result["inventory"]["canonical"]["receipts"][0]["evidence_ids"], []
        )


if __name__ == "__main__":
    unittest.main()
