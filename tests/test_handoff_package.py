"""Portable handoff checks use existing public derivatives, never private sources."""

import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import package_qualification_handoff as package
from report_common import check_public


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve() / "corpus"
        self.root.mkdir()
        self.bundle = check_public()
        self.notes = {
            n: ("# Reviewed " + n + "\n").encode() for n in package.NARRATIVES
        }
        from collect_status import INPUTS

        paths = set(INPUTS.values()) | {
            f"reports/pre1-qualification/certificates/{t}.json"
            for t in [
                "linux-aarch64",
                "linux-x86_64",
                "macos-arm64",
                "windows-x86_64",
                "ecosystem",
            ]
        }
        self.records = [
            {
                "path": n,
                "sha256": "sha256:" + "0" * 64,
                "url": f"https://github.com/RobLe3/iicp.network/blob/{package.SOURCE}/{n}",
            }
            for n in sorted(paths)
        ]

    def tearDown(self):
        self.temp.cleanup()

    def write(self, members):
        for n, b in members.items():
            p = self.root / n
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b)

    def test_deterministic_builder(self):
        self.assertEqual(
            package.build_members(self.bundle, self.records, self.notes),
            package.build_members(self.bundle, self.records, self.notes),
        )

    def test_portable_positive(self):
        m = package.build_members(self.bundle, self.records, self.notes)
        self.write(m)
        d = "sha256:" + hashlib.sha256(m["manifest.json"]).hexdigest()
        r = package.verify_corpus(self.root, d)
        self.assertTrue(r["trust_anchor_checked"])
        self.assertFalse(r["private_source_reverification"])

    def test_changed_narrative(self):
        self.write(package.build_members(self.bundle, self.records, self.notes))
        (self.root / "START_HERE.md").write_text("altered")
        with self.assertRaises(ValueError):
            package.verify_corpus(self.root)

    def test_private_marker_refused(self):
        self.notes["START_HERE.md"] = b"private /Users/synthetic/no-real-data"
        with self.assertRaises(ValueError):
            package.build_members(self.bundle, self.records, self.notes)

    def test_wrong_source_refused(self):
        b = copy.deepcopy(self.bundle)
        b["status"]["source_commit"] = "a" * 40
        with self.assertRaises(ValueError):
            package.build_members(b, self.records, self.notes)

    def test_trusted_manifest_required_for_identity(self):
        self.write(package.build_members(self.bundle, self.records, self.notes))
        with self.assertRaises(ValueError):
            package.verify_corpus(self.root, "sha256:" + "0" * 64)

    def test_extra_member_refused(self):
        self.write(package.build_members(self.bundle, self.records, self.notes))
        (self.root / "extra.txt").write_text("synthetic")
        with self.assertRaises(ValueError):
            package.verify_corpus(self.root)

    def test_symlink_refused(self):
        self.write(package.build_members(self.bundle, self.records, self.notes))
        p = self.root / "START_HERE.md"
        p.unlink()
        p.symlink_to(self.root / "AGENT_BRIEF.md")
        with self.assertRaises(ValueError):
            package.verify_corpus(self.root)


if __name__ == "__main__":
    unittest.main()
