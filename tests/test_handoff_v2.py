"""V2 author tests: portable data semantics, no private inputs or original writes."""

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import package_handoff_v2 as p
import qualification_analysis as qa


class V2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = p.REPO / "reports/qualification-heritage"
        cls.bundle = {
            n: json.loads((base / "data" / f"{n}.json").read_text())
            for n in ("status", "receipts", "events")
        }
        cls.records = json.loads((base / "SOURCE_INDEX.json").read_text())["records"]
        links = json.loads((p.REPO / p.SCHEMA).read_text())["$defs"]["reviewed_links"][
            "const"
        ]
        a = qa.generate(
            **cls.bundle,
            scope=json.loads((base / "data/scope.json").read_text()),
            links=links,
        )
        cls.extras = {
            "analysis.json": a,
            "unresolved-clauses.json": {
                "schema": "iicp.handoff-unresolved-clauses.v1",
                "requirements": a["requirements"],
            },
            "dmsc-sources.json": {
                "schema": "iicp.handoff-dmsc-sources.v1",
                "sources": a["dmsc_sources"],
                "records": a["dmsc"],
            },
            "history-gaps.json": json.loads((p.REPO / p.SCHEMA).read_text())["const"],
        }
        cls.notes = {n: ("# Synthetic " + n + "\n").encode() for n in p.v1.NARRATIVES}
        cls.members = p.build_members(cls.bundle, cls.records, cls.notes, cls.extras)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "corpus"
        self.root.mkdir()
        for name, data in self.members.items():
            q = self.root / name
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_bytes(data)

    def mutate(self, name, value):
        data = p.v1.encoded(value)
        (self.root / name).write_bytes(data)
        m = json.loads((self.root / "manifest.json").read_text())
        m["members"][name] = {"sha256": p.sha(data), "bytes": len(data)}
        (self.root / "manifest.json").write_bytes(p.v1.encoded(m))

    def check(self):
        return p.verify(self.root, p.sha((self.root / "manifest.json").read_bytes()))

    def test_positive(self):
        self.assertTrue(self.check()["trust_anchor_checked"])

    def test_duplicate_analysis_assertion(self):
        a = copy.deepcopy(self.extras["analysis.json"])
        a["assertions"].append(a["assertions"][0])
        self.mutate("data/analysis.json", a)
        with self.assertRaises(ValueError):
            self.check()

    def test_analysis_source_altered(self):
        a = copy.deepcopy(self.extras["analysis.json"])
        a["source_commit"] = "a" * 40
        self.mutate("data/analysis.json", a)
        with self.assertRaises(ValueError):
            self.check()

    def test_history_completeness_inflation(self):
        a = copy.deepcopy(self.extras["history-gaps.json"])
        a["historical_inventory_complete"] = True
        self.mutate("data/history-gaps.json", a)
        with self.assertRaises(ValueError):
            self.check()

    def test_private_metadata_field(self):
        a = copy.deepcopy(self.extras["history-gaps.json"])
        a["private_locator"] = "/Users/synthetic"
        self.mutate("data/history-gaps.json", a)
        with self.assertRaises(ValueError):
            self.check()

    def test_dmsc_maturity_inflation(self):
        a = copy.deepcopy(self.extras["dmsc-sources.json"])
        a["records"][0]["assessment"] = "VERIFIED"
        self.mutate("data/dmsc-sources.json", a)
        with self.assertRaises(ValueError):
            self.check()

    def test_dropped_clause_even_recomputed(self):
        a = copy.deepcopy(self.extras["analysis.json"])
        links = {
            "schema": "iicp.qualification-analysis-links.v1",
            "source_commit": a["source_commit"],
            "requirements": a["requirements"][1:],
            "history": a["history"],
            "dmsc_sources": a["dmsc_sources"],
        }
        a = qa.generate(
            **self.bundle,
            scope=json.loads((p.REPO / "contracts/scope.json").read_text()),
            links=links,
        )
        self.mutate("data/analysis.json", a)
        self.mutate(
            "data/unresolved-clauses.json",
            {
                "schema": "iicp.handoff-unresolved-clauses.v1",
                "requirements": a["requirements"],
            },
        )
        with self.assertRaises(ValueError):
            self.check()

    def test_missing_metadata_even_resealed(self):
        target = self.root / "data/history-gaps.json"
        target.unlink()
        m = json.loads((self.root / "manifest.json").read_text())
        del m["members"]["data/history-gaps.json"]
        (self.root / "manifest.json").write_bytes(p.v1.encoded(m))
        with self.assertRaises(ValueError):
            self.check()

    def test_changed_receipt_binding(self):
        a = copy.deepcopy(self.extras["analysis.json"])
        a["assertions"][0]["receipt_file_sha256"] = "sha256:" + "0" * 64
        self.mutate("data/analysis.json", a)
        with self.assertRaises(ValueError):
            self.check()

    def test_no_anchor_refused(self):
        with self.assertRaises(ValueError):
            p.verify(self.root, None)

    def test_v1_unchanged(self):
        r = p.v1.verify_corpus(
            p.REPO / "reports/qualification-heritage",
            "sha256:5f790e2ae92594baa2ffa0de8c7d7a7f37ecfbb97d35188105a81eca4cb766b3",
        )
        self.assertEqual(r["files"], 21)


if __name__ == "__main__":
    unittest.main()
