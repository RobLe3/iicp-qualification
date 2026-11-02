"""Synthetic, zero-credit controls for canonical certificate reporting."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import certificate_reporting as cert
import report_common as common


def synthetic_bundle():
    bundle = copy.deepcopy(common.check_public())
    status = bundle["status"]
    rows = []
    sentinels = {r["target"]: r["receipt_file_sha256"] for r in status["sentinels"]}
    for i, name in enumerate(sorted(cert.TARGETS | {"ecosystem"}), 1):
        rows.append({"target": name, "certificate_file_sha256": "sha256:" + f"{i+10:064x}",
                     "certificate_sha256": "sha256:" + f"{i:064x}",
                     **{k:status["authority"][k] for k in ("candidate_manifest_sha256", "executor_registry_sha256", "shard_plan_sha256")},
                     "receipt_file_sha256s": sorted(r["receipt_file_sha256"] for r in bundle["receipts"]["receipts"] if r["target"] == name),
                     "admission_sentinel_file_sha256": sentinels.get(name),
                     "target_certificate_sha256s": [],
                     "classification": "project-operated-qualification", "admission_status": "accepted-in-merged-canonical-evidence"})
    rows[0]["target_certificate_sha256s"] = sorted(r["certificate_sha256"] for r in rows[1:])
    status["certificates"] = rows
    status["accepted"]["certificates"] = 5
    return bundle


class DerivativeTests(unittest.TestCase):
    def setUp(self):
        self.bundle = synthetic_bundle()

    def check(self, bundle=None):
        value = bundle or self.bundle
        common.check_bundle(value["status"], value["receipts"], value["events"])

    def test_positive_complete_synthetic_set(self):
        self.check()
        self.assertIn("not external certification", common.render(self.bundle["status"], self.bundle["events"]))

    def test_zero_without_admission_remains_valid(self):
        self.check(common.check_public())

    def test_partial_and_duplicate_mapping_refused(self):
        for replacement in (self.bundle["status"]["certificates"][:-1],
                            self.bundle["status"]["certificates"][:-1] + [self.bundle["status"]["certificates"][0]]):
            value = copy.deepcopy(self.bundle)
            value["status"]["certificates"] = replacement
            with self.assertRaises(ValueError):
                self.check(value)

    def test_incomplete_totals_refused_even_with_complete_shard_count(self):
        for field in ("support_cells", "edge_executions", "sentinels", "shards"):
            with self.subTest(field=field):
                value = copy.deepcopy(self.bundle)
                value["status"]["accepted"][field] -= 1
                with self.assertRaisesRegex(ValueError, "complete campaign"):
                    cert.validate_derivatives(value["status"], value["receipts"]["receipts"])

    def test_foreign_authority_refused(self):
        for field in ("candidate_manifest_sha256", "executor_registry_sha256", "shard_plan_sha256"):
            with self.subTest(field=field):
                value = copy.deepcopy(self.bundle)
                value["status"]["certificates"][1][field] = "sha256:" + "f" * 64
                with self.assertRaisesRegex(ValueError, "authority differs"):
                    self.check(value)

    def test_altered_links_and_unaccepted_receipts_refused(self):
        for field, replacement in (("receipt_file_sha256s", ["sha256:" + "f"*64]),
                                   ("admission_sentinel_file_sha256", "sha256:" + "f"*64),
                                   ("target_certificate_sha256s", ["sha256:" + "f"*64])):
            value = copy.deepcopy(self.bundle)
            value["status"]["certificates"][1][field] = replacement
            with self.assertRaises(ValueError):
                self.check(value)
        self.bundle["status"]["certificates"][0]["target_certificate_sha256s"] = []
        with self.assertRaisesRegex(ValueError, "links differ"):
            self.check()

    def test_private_or_external_claim_fields_refused(self):
        for key, value in (("source_path", "/private/marker"), ("independent_certification", True)):
            bundle = copy.deepcopy(self.bundle)
            bundle["status"]["certificates"][0][key] = value
            with self.assertRaises(ValueError):
                self.check(bundle)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("config", "user.name", "Synthetic fixture")
        (self.root / "README").write_text("synthetic zero-credit repository\n")
        self.commit()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True, stderr=subprocess.DEVNULL).strip()

    def commit(self, merged=True):
        self.git("add", ".")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "synthetic fixture")
        self.head = self.git("rev-parse", "HEAD")
        if merged:
            self.git("update-ref", "refs/remotes/origin/main", self.head)

    def write_set(self):
        for name in cert.TARGETS | {"ecosystem"}:
            path = self.root / cert.DIRECTORY / (name + ".json")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"schema": "iicp.pre1-" + ("ecosystem" if name == "ecosystem" else "target") + "-qualification-certificate.v1"}))

    def test_genuine_absence_is_zero(self):
        self.assertEqual(cert.discover(self.root, self.head), [])

    def test_positive_exact_known_merged_set(self):
        self.write_set(); self.commit()
        self.assertEqual(set(cert.discover(self.root, self.head)), cert.PATHS)

    def test_altered_all_schema_markers_are_not_zero(self):
        self.write_set()
        for path in (self.root / cert.DIRECTORY).glob('*.json'):
            path.write_text('{"schema":"unknown"}')
        self.commit()
        with self.assertRaisesRegex(ValueError, "unrecognized"):
            cert.discover(self.root, self.head)

    def test_partial_and_extra_inventory_refused(self):
        self.write_set()
        (self.root / cert.DIRECTORY / "ecosystem.json").unlink()
        self.commit()
        with self.assertRaisesRegex(ValueError, "inventory"):
            cert.discover(self.root, self.head)
        self.write_set()
        (self.root / cert.DIRECTORY / "duplicate.json").write_text('{}')
        self.commit()
        with self.assertRaisesRegex(ValueError, "inventory"):
            cert.discover(self.root, self.head)

    def test_uncommitted_and_unmerged_sets_refused(self):
        self.write_set()
        with self.assertRaisesRegex(ValueError, "not committed"):
            cert.discover(self.root, self.head)
        self.commit(merged=False)
        with self.assertRaisesRegex(ValueError, "not on known merged main"):
            cert.discover(self.root, self.head)

    def test_noncanonical_certificate_refused(self):
        self.write_set()
        p = self.root / "reports" / "foreign.json"
        p.write_text('{"schema":"iicp.pre1-target-certificate.v1"}')
        self.commit()
        with self.assertRaisesRegex(ValueError, "noncanonical"):
            cert.discover(self.root, self.head)
