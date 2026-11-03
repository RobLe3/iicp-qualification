"""Read-only checks for the additive, non-authorizing closeout checkpoint."""

import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from report_common import check_public  # noqa: E402 - repository-local script import

CORPUS = ROOT / "reports/qualification-heritage/supplements/2026-11-03-closeout"


class CloseoutCheckpointTests(unittest.TestCase):
    def test_manifest_members_and_boundaries(self):
        manifest = json.loads((CORPUS / "checkpoint-manifest.json").read_text())
        self.assertFalse(manifest["historical_inventory_complete"])
        self.assertEqual(manifest["qualification_credit_added"], 0)
        self.assertEqual(manifest["issue_1676_status"], "OPEN")
        self.assertEqual(manifest["delivery_gates_complete"], 9)
        self.assertEqual(
            set(manifest["members"]),
            {p.name for p in CORPUS.iterdir()} - {"checkpoint-manifest.json"},
        )
        for name, entry in manifest["members"].items():
            path = CORPUS / name
            self.assertFalse(path.is_symlink())
            data = path.read_bytes()
            self.assertEqual(entry["bytes"], len(data))
            self.assertEqual(
                entry["sha256"], "sha256:" + hashlib.sha256(data).hexdigest()
            )

    def test_existing_public_schema_and_source_identity(self):
        bundle = check_public()
        self.assertIsNotNone(bundle)
        original = ROOT / "reports/documentation-handoff/v2/SOURCE_INDEX.json"
        self.assertEqual(
            original.read_bytes(), (CORPUS / "SOURCE_INDEX.json").read_bytes()
        )
        for version, digest in [
            (
                "reports/qualification-heritage",
                "5f790e2ae92594baa2ffa0de8c7d7a7f37ecfbb97d35188105a81eca4cb766b3",
            ),
            (
                "reports/documentation-handoff/v2",
                "e805148387261890a774b3a68684998947311f6c3d51ec6fcaf683ff6d6bee3b",
            ),
        ]:
            self.assertEqual(
                hashlib.sha256(
                    (ROOT / version / "manifest.json").read_bytes()
                ).hexdigest(),
                digest,
            )

    def test_clause_dispositions_do_not_promote(self):
        data = json.loads((CORPUS / "clause-dispositions.sanitized.json").read_text())
        self.assertEqual(len(data["rows"]), 21)
        self.assertEqual(len({r["id"] for r in data["rows"]}), 21)
        self.assertEqual({r["criterion_verdict"] for r in data["rows"]}, {"UNVERIFIED"})
        self.assertEqual(
            sum(r["evidence_disposition"] == "PARTIAL" for r in data["rows"]), 18
        )
        self.assertEqual(data["qualification_credit_added"], 0)
        self.assertFalse(data["historical_inventory_complete"])

    def test_inventory_prefix_is_not_completeness(self):
        data = json.loads((CORPUS / "inventory-prefix.json").read_text())
        self.assertEqual(data["completed_partitions"], 314)
        self.assertEqual(data["unique_evidence_objects"], 271458)
        self.assertEqual(
            sum(data["availability"].values()), data["unique_evidence_objects"]
        )
        self.assertEqual(
            sum(data["integrity"].values()), data["unique_evidence_objects"]
        )
        self.assertEqual(data["unique_object_gap_pairs"], 572)
        self.assertEqual(data["canonical_receipts_resolved_across_prefix"], 64)
        self.assertFalse(data["historical_inventory_complete"])
        self.assertFalse(data["chain"]["discovery_exhausted"])
        self.assertEqual(data["qualification_credit_added"], 0)

    def test_gap_dispositions_cover_only_checkpoint_denominator(self):
        gaps = json.loads((CORPUS / "gap-dispositions.json").read_text())
        summary = json.loads((CORPUS / "inventory-prefix.json").read_text())
        categories = {row["id"]: row for row in gaps["categories"]}
        self.assertEqual(set(categories), {"oversize", "unsafe", "mismatch"})
        self.assertEqual(
            categories["oversize"]["count"], summary["availability"]["OVERSIZE"]
        )
        self.assertEqual(
            categories["unsafe"]["count"], summary["availability"]["UNSAFE"]
        )
        self.assertEqual(
            categories["mismatch"]["count"], summary["integrity"]["MISMATCH"]
        )
        self.assertEqual(sum(row["count"] for row in categories.values()), 572)
        for row in categories.values():
            self.assertEqual(
                row["owner_issue"], "https://github.com/RobLe3/iicp.network/issues/1676"
            )
            self.assertTrue(row["next_action"])
            self.assertEqual(row["source_sha256"], gaps["source_summary_sha256"])
        outside = gaps["outside_object_gap_denominator"]
        self.assertEqual(outside["remaining_frontier_entries"], 1250)
        self.assertEqual(outside["excluded_path_census"], "UNKNOWN")
        self.assertIsNone(outside["total_historical_attempts"])
        self.assertFalse(gaps["historical_inventory_complete"])
        self.assertEqual(gaps["qualification_credit_added"], 0)

    def test_json_links_and_targeted_privacy_scan(self):
        for path in CORPUS.iterdir():
            text = path.read_text()
            for pattern in (
                r"/Users/",
                r"arn:aws:",
                r"AKIA[A-Z0-9]+",
                r"\b\d{12}\b",
                r"Bearer\s",
            ):
                self.assertIsNone(re.search(pattern, text), (path.name, pattern))
            if path.suffix == ".json":
                json.loads(text)
            if path.suffix == ".md":
                for link in re.findall(r"\]\(([^)]+)\)", text):
                    if not link.startswith(("http", "#")):
                        self.assertTrue(
                            (path.parent / link.split("#")[0]).exists(),
                            (path.name, link),
                        )


if __name__ == "__main__":
    unittest.main()
