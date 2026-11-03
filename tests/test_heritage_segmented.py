"""Synthetic history-cap localization and no-loss successor controls."""

import copy
import unittest
from unittest.mock import patch
import test_heritage
import heritage_segmented as s


class SegmentedTests(unittest.TestCase):
    setUp = test_heritage.HeritageTests.setUp

    def predecessor(self):
        path = self.root
        for _ in range(12):
            path = path / "a"
            path.mkdir()
        return s.v1.discover(self.config, steps=6)

    def test_exact_guard_and_sanitized_code(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            p = self.predecessor()
            with self.assertRaisesRegex(
                ValueError, "directory history bound"
            ) as caught:
                s.v1.discover(self.config, p, steps=6)
            self.assertEqual(
                s.v1.refusal_code(caught.exception), "DIRECTORY_HISTORY_LIMIT"
            )
        self.assertEqual(
            s.v1.refusal_code(ValueError("/private/path")), "INVALID_INPUT"
        )

    def test_segmented_positive_full_history_chain(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            p = self.predecessor()
            before = copy.deepcopy(p)
            q, segments = s.advance(self.config, p, {}, 6)
            self.assertEqual(p, before)
            self.assertEqual(q["previous_sha256"], p["page_sha256"])
            self.assertEqual(q["origin_v1_sha256"], p["page_sha256"])
            self.assertEqual(q["history_directory_count"], 12)
            self.assertEqual(len(segments), 1)
            result = s.validate_chain(self.config, [p, q], segments)
            self.assertEqual(result["history_directories"], 12)
            self.assertFalse(result["historical_inventory_complete"])
            while not q["discovery_exhausted"]:
                q, segments = s.advance(self.config, q, segments, 6)
            self.assertGreater(q["history_directory_count"], 3)

    def test_missing_tampered_segments_and_config_refused(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            p = self.predecessor()
            q, segments = s.advance(self.config, p, {}, 6)
            with self.assertRaises(ValueError):
                s.validate(q, self.config, {})
            changed = copy.deepcopy(segments)
            next(iter(changed.values()))["directories"].pop()
            with self.assertRaises(ValueError):
                s.validate(q, self.config, changed)
            c = copy.deepcopy(self.config)
            c["max_file_bytes"] += 1
            with self.assertRaises(ValueError):
                s.advance(c, q, segments, 6)

    def test_archived_directory_change_refuses(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            p = self.predecessor()
            q, segments = s.advance(self.config, p, {}, 6)
            (self.root / "a" / "changed").write_text("synthetic")
            with self.assertRaisesRegex(
                ValueError, "previously discovered directory changed"
            ):
                s.advance(self.config, q, segments, 6)

    def test_dropped_history_detected_by_chain(self):
        with patch.object(s.v1, "DIRECTORY_LIMIT", 10):
            p = self.predecessor()
            q, segments = s.advance(self.config, p, {}, 6)
            q["history_segments"] = []
            q["history_directory_count"] = len(q["directories"])
            q.pop("page_sha256")
            s.seal(q)
            with self.assertRaisesRegex(ValueError, "lost or changed historical stamp"):
                s.validate_chain(self.config, [p, q], {})

    def test_v1_original_limit_not_raised(self):
        self.assertEqual(s.v1.DIRECTORY_LIMIT, 10000)
        self.assertEqual(s.MAX_SEGMENTS, 256)


if __name__ == "__main__":
    unittest.main()
