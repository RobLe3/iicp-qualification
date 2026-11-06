"""Independently prepared portable-package boundary and semantic tests."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import package_qualification_handoff as p
sys.path.insert(0, str(Path(__file__).resolve().parent))
from handoff_fixture import historical_fixture


class IndependentHandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve() / "corpus"
        self.root.mkdir()
        # Public committed derivative: this portability test must not depend on
        # private sibling checkouts or re-fetch canonical source material.
        source_index = json.loads(
            (
                Path(__file__).resolve().parents[1]
                / "reports/qualification-heritage/SOURCE_INDEX.json"
            ).read_text()
        )
        records = source_index["records"]
        bundle, self.fixture_repo = historical_fixture(Path(self.tmp.name).resolve())
        members = p.build_members(
            bundle,
            records,
            {n: ("# Synthetic " + n + "\n").encode() for n in p.NARRATIVES},
            repo=self.fixture_repo,
        )
        for name, data in members.items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    def reseal(self, name, value=None, remove=False):
        manifest = json.loads((self.root / "manifest.json").read_text())
        if remove:
            (self.root / name).unlink()
            del manifest["members"][name]
        else:
            data = p.encoded(value)
            (self.root / name).write_bytes(data)
            manifest["members"][name] = {"bytes": len(data), "sha256": p.sha(data)}
        (self.root / "manifest.json").write_bytes(p.encoded(manifest))

    def verify(self):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(self.root / "verify.py"),
                "--root",
                str(self.root),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def rejected(self):
        result = self.verify()
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_actual_portable_positive(self):
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["trust_anchor_checked"])

    def test_missing_narrative_even_resealed(self):
        self.reseal("AGENT_BRIEF.md", remove=True)
        self.rejected()

    def test_empty_source_index_even_resealed(self):
        value = json.loads((self.root / "SOURCE_INDEX.json").read_text())
        value["records"] = []
        self.reseal("SOURCE_INDEX.json", value)
        self.rejected()

    def test_duplicate_source_index_even_resealed(self):
        value = json.loads((self.root / "SOURCE_INDEX.json").read_text())
        value["records"].append(value["records"][0])
        self.reseal("SOURCE_INDEX.json", value)
        self.rejected()

    def test_certificate_copy_corruption_even_resealed(self):
        value = json.loads((self.root / "data/certificates.json").read_text())
        value["certificates"] = []
        self.reseal("data/certificates.json", value)
        self.rejected()

    def test_receipt_semantic_corruption_even_resealed(self):
        value = json.loads((self.root / "data/receipts.json").read_text())
        value["private_capture"] = "synthetic sensitive content"
        self.reseal("data/receipts.json", value)
        self.rejected()

    def test_source_locator_private_path_even_resealed(self):
        value = json.loads((self.root / "SOURCE_INDEX.json").read_text())
        value["records"][0]["url"] = "/Users/synthetic/private"
        self.reseal("SOURCE_INDEX.json", value)
        self.rejected()

    def test_manifest_fifo_refused_without_hang(self):
        target = self.root / "manifest.json"
        target.unlink()
        os.mkfifo(target)
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(self.root / "verify.py"),
                "--root",
                str(self.root),
            ],
            capture_output=True,
            text=True,
            timeout=3,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_source_symlink(self):
        target = self.root / "AGENT_BRIEF.md"
        target.unlink()
        target.symlink_to(self.root / "START_HERE.md")
        self.rejected()


if __name__ == "__main__":
    unittest.main()
