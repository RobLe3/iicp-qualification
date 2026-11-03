"""Independent synthetic no-loss history and authority tests."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import test_heritage
import heritage_segmented as s


class SegmentedReviewTests(unittest.TestCase):
    setUp = test_heritage.HeritageTests.setUp

    def chain(self):
        (self.root / "0file").write_text("x")
        path = self.root
        for _ in range(24):
            path = path / "a"
            path.mkdir()
        p = s.v1.discover(self.config, steps=6)
        pages = [p]
        segments = {}
        while not pages[-1]["discovery_exhausted"]:
            q, segments = s.advance(self.config, pages[-1], segments, 6)
            pages.append(q)
        return pages, segments

    def test_multiple_segments_preserve_history_and_record_once(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            pages, segments = self.chain()
            r = s.validate_chain(self.config, pages, segments)
            self.assertEqual(r["history_directories"], 25)
            self.assertGreater(len(segments), 1)
            self.assertEqual(r["discovered_records"], 2)
            self.assertFalse(r["historical_inventory_complete"])
            for old, new in zip(pages, pages[1:]):
                self.assertEqual(new["previous_sha256"], old["page_sha256"])
                self.assertEqual(new["origin_v1_sha256"], pages[0]["page_sha256"])

    def test_global_duplicate_across_v1_v2_rejected(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            pages, segments = self.chain()
            q = copy.deepcopy(pages[-1])
            q["records"].append(pages[0]["records"][0])
            q.pop("page_sha256")
            s.seal(q)
            with self.assertRaisesRegex(ValueError, "duplicate partition record"):
                s.validate_chain(self.config, [*pages[:-1], q], segments)

    def test_segmented_inventory_cannot_rebind_or_add_credit(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            pages, segments = self.chain()
            q = pages[-1]
            with patch.object(
                s.v1.heritage,
                "load_canonical",
                return_value=copy.deepcopy(self.canonical),
            ):
                w = s.inventory_partition(self.config, q, segments)
            bad = copy.deepcopy(w)
            bad["qualification_credit"] = 1
            with self.assertRaises(ValueError):
                s.validate_inventory(self.config, bad, segments)
            bad = copy.deepcopy(w)
            bad["history_segment_sha256"] = []
            with self.assertRaises(ValueError):
                s.validate_inventory(self.config, bad, segments)

    def test_segment_reference_traversal_refused_before_read(self):
        config = self.root / "config.json"
        config.write_text(json.dumps(self.config))
        previous = self.root / "previous.json"
        previous.write_text(json.dumps({"history_segments": ["../../outside"]}))
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(Path(s.__file__)),
                "--config",
                str(config),
                "--previous",
                str(previous),
                "--segments",
                str(self.root),
                "--output",
                str(self.root / "output.json"),
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("INVALID_INPUT", result.stderr)
        self.assertFalse((self.root / "output.json").exists())


if __name__ == "__main__":
    unittest.main()
