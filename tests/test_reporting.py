"""Zero-credit reporting tests. No Docker, cloud or qualification workload."""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import report_common as common  # noqa: E402
import qualification_status as cli  # noqa: E402
from collect_status import private_events  # noqa: E402
from collect_status import validator_modules  # noqa: E402
from collect_status import validate_shard_binding  # noqa: E402


class ReportingTests(unittest.TestCase):
    def protection(self):
        return {
            "required_status_checks": {
                "strict": True,
                "contexts": ["qualification-report"],
            },
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
        }

    def setUp(self):
        self.bundle = common.check_public()

    def check(self, bundle):
        common.check_bundle(bundle["status"], bundle["receipts"], bundle["events"])

    def rebinding(self, bundle):
        bundle["status"]["events_sha256"] = common.sha(
            common.canonical(bundle["events"])
        )
        bundle["status"]["receipts_sha256"] = common.sha(
            common.canonical(bundle["receipts"])
        )

    def event(self, outcome="FAIL", launched=True):
        reason = {"PASS": "run-completed", "REFUSED": "preflight-refused"}.get(
            outcome, "run-failed"
        )
        e = {
            "kind": "diagnostic",
            "outcome": outcome,
            "reason": reason,
            "next_gate": "review-failure",
            "occurred_at": "2026-10-29T12:00:00Z",
            "workload_launched": launched,
            "source_sha256": "sha256:" + "a" * 64,
            "qualification_credit": 0,
        }
        e["event_id"] = common.sha(common.canonical(e))
        return e

    def test_current_public_bundle(self):
        self.check(self.bundle)

    def test_accounting_totals_match_receipts(self):
        a = self.bundle["status"]["accepted"]
        self.assertEqual(a["shards"], len(self.bundle["receipts"]["receipts"]))

    def test_actual_cli_check(self):
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(common.REPO / "scripts/qualification_status.py"),
                "check",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("private-source freshness not checked", result.stdout)

    def test_deterministic_render(self):
        self.assertEqual(
            common.encoded(self.bundle), common.encoded(copy.deepcopy(self.bundle))
        )

    def test_unknown_private_field_rejected(self):
        self.bundle["status"]["private_path"] = "/private/SYNTHETIC_SECRET"
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_private_marker_in_assignment_rejected(self):
        self.bundle["receipts"]["receipts"][0]["support_cells"].append(
            "synthetic-secret-marker"
        )
        self.rebinding(self.bundle)
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_freeform_reason_rejected(self):
        e = self.event()
        e["reason"] = "SYNTHETIC_SECRET"
        with self.assertRaises(ValueError):
            common.validate(
                {"schema": "iicp.qualification-events.v1", "events": [e]}, "events"
            )

    def test_unknown_schema_rejected(self):
        self.bundle["status"]["schema"] = "foreign"
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_mixed_candidate_rejected(self):
        self.bundle["receipts"]["receipts"][0]["candidate_manifest_sha256"] = (
            "sha256:" + "0" * 64
        )
        self.rebinding(self.bundle)
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_mixed_registry_rejected(self):
        self.bundle["receipts"]["receipts"][0]["executor_registry_sha256"] = (
            "sha256:" + "0" * 64
        )
        self.rebinding(self.bundle)
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_duplicate_receipt_rejected(self):
        self.bundle["receipts"]["receipts"].append(
            copy.deepcopy(self.bundle["receipts"]["receipts"][0])
        )
        self.rebinding(self.bundle)
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_diagnostic_cannot_be_credited(self):
        self.bundle["receipts"]["receipts"][0]["evidence_class"] = "diagnostic"
        self.rebinding(self.bundle)
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_sentinel_cannot_be_credited_by_relabel(self):
        self.bundle["receipts"]["receipts"][0]["evidence_class"] = "sentinel"
        self.rebinding(self.bundle)
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_unpromoted_pass_adds_no_credit(self):
        before = copy.deepcopy(self.bundle["status"]["accepted"])
        self.bundle["events"]["events"].append(self.event("PASS"))
        self.rebinding(self.bundle)
        self.check(self.bundle)
        self.assertEqual(before, self.bundle["status"]["accepted"])

    def test_refusal_has_no_workload_or_credit(self):
        event = self.event("REFUSED", False)
        self.assertFalse(event["workload_launched"])
        self.bundle["events"]["events"].append(event)
        self.rebinding(self.bundle)
        self.check(self.bundle)
        self.assertEqual(event["qualification_credit"], 0)

    def test_mutated_digest_rejected(self):
        self.bundle["status"]["receipts_sha256"] = "sha256:" + "0" * 64
        with self.assertRaises(ValueError):
            self.check(self.bundle)

    def test_history_rewrite_rejected(self):
        other = copy.deepcopy(self.bundle)
        other["events"]["events"] = []
        with self.assertRaises(ValueError):
            cli.preserve_history(self.bundle, other)

    def test_credit_decrease_requires_review(self):
        other = copy.deepcopy(self.bundle)
        other["status"]["accepted"]["shards"] -= 1
        with self.assertRaises(ValueError):
            cli.preserve_history(self.bundle, other)

    def test_receipt_derivative_rewrite_rejected(self):
        other = copy.deepcopy(self.bundle)
        other["receipts"]["receipts"][0]["status"] = "FAIL"
        with self.assertRaises(ValueError):
            cli.preserve_history(self.bundle, other)

    def test_generated_paths_positive_control(self):
        cli.eligible_changes(["reports/status.json", "reports/STATUS.md"])

    def test_code_policy_and_workflow_not_auto_publishable(self):
        for path in (
            "scripts/qualification_status.py",
            "reporting-policy.json",
            ".github/workflows/report.yml",
            "README.md",
        ):
            with self.assertRaises(ValueError):
                cli.eligible_changes(["reports/status.json", path])

    def test_missing_check_not_green(self):
        with self.assertRaises(ValueError):
            cli.eligible_changes([])

    def test_timestamp_and_unrelated_commit_are_noop(self):
        other = copy.deepcopy(self.bundle)
        other["status"]["verified_at"] = "2026-10-30T12:00:00Z"
        other["status"]["source_commit"] = "a" * 40
        self.assertEqual(
            cli.material_identity(self.bundle), cli.material_identity(other)
        )

    def test_registered_activity_makes_snapshot_stale(self):
        other = copy.deepcopy(self.bundle)
        other["events"]["events"].append(self.event())
        self.rebinding(other)
        self.assertNotEqual(
            cli.material_identity(self.bundle), cli.material_identity(other)
        )
        args = argparse.Namespace(
            root=Path("."),
            source_commit="a" * 40,
            sentinel=True,
            archive_root=True,
            inbox=True,
        )
        with (
            patch.object(cli, "prepare", return_value=other),
            self.assertRaisesRegex(ValueError, "STALE"),
        ):
            cli.report_check(args)

    def test_reconciliation_clears_stale(self):
        args = argparse.Namespace(
            root=Path("."),
            source_commit="a" * 40,
            sentinel=True,
            archive_root=True,
            inbox=True,
        )
        with patch.object(cli, "prepare", return_value=self.bundle):
            cli.report_check(args)

    def test_private_source_integrity_and_missing_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp).resolve()
            source = p / "terminal.json"
            source.write_text('{"result":"synthetic"}')
            event = self.event()
            event["source_sha256"] = common.sha(source.read_bytes())
            event["event_id"] = common.sha(
                common.canonical({k: v for k, v in event.items() if k != "event_id"})
            )
            inbox = p / "inbox.json"
            inbox.write_text(
                json.dumps(
                    {
                        "schema": "iicp.reporting-inbox.v1",
                        "entries": [
                            {
                                "source": str(source),
                                "source_sha256": event["source_sha256"],
                                "event": event,
                            }
                        ],
                    }
                )
            )
            self.assertEqual(private_events(inbox)[0]["events"], [event])
            source.write_text("changed")
            with self.assertRaises(ValueError):
                private_events(inbox)
            source.unlink()
            with self.assertRaises(ValueError):
                private_events(inbox)

    def test_record_cli_idempotent_private_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp).resolve()
            os.chmod(p, 0o700)
            source = p / "synthetic.json"
            source.write_text('{"result":"failed"}')
            command = [
                sys.executable,
                "-B",
                str(common.REPO / "scripts/qualification_status.py"),
                "record",
                "--inbox",
                str(p / "inbox.json"),
                "--source",
                str(source),
                "--kind",
                "diagnostic",
                "--outcome",
                "FAIL",
                "--reason",
                "run-failed",
                "--next-gate",
                "review-failure",
                "--occurred-at",
                "2026-10-29T12:00:00Z",
                "--workload-launched",
            ]
            a = subprocess.run(command, capture_output=True, text=True)
            b = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(a.returncode, 0, a.stderr)
            self.assertEqual(b.stdout.strip(), "NO_CHANGE")
            self.assertEqual(
                len(json.loads((p / "inbox.json").read_text())["entries"]), 1
            )

    def test_symlink_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp).resolve()
            target = p / "original"
            target.write_text("preserve")
            link = p / "link"
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                cli.atomic(link, b"new")
            self.assertEqual(target.read_text(), "preserve")

    def test_failed_publication_preserves_intent(self):
        successor = copy.deepcopy(self.bundle)
        successor["events"]["events"].append(self.event())
        self.rebinding(successor)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp).resolve()
            os.chmod(p, 0o700)
            args = argparse.Namespace(state_dir=p, source_commit="a" * 40)

            def fake(*argv, **kw):
                if argv[:2] == ("gh", "api"):
                    return "a" * 40
                raise OSError("synthetic Git boundary stop")

            with (
                patch.object(cli, "publication_identity", return_value="b" * 40),
                patch.object(cli, "prepare", return_value=successor),
                patch.object(cli, "run", side_effect=fake),
            ):
                with self.assertRaises(OSError):
                    cli.publish(args)
            self.assertEqual(len(list(p.glob("report-*.json"))), 1)

    def publication_fixture(
        self, changed_head=False, concurrent_base=False, final_base_changed=False
    ):
        successor = copy.deepcopy(self.bundle)
        successor["events"]["events"].append(self.event())
        self.rebinding(successor)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp).resolve()
            os.chmod(p, 0o700)
            calls = []
            for name, content in common.encoded(successor).items():
                path = p / name
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(content)

            def fake(*argv, **kw):
                calls.append(argv)
                if argv[:2] == ("gh", "api"):
                    if argv[2].endswith("/protection"):
                        return json.dumps(self.protection())
                    if argv[2] == "repos/RobLe3/iicp-qualification/commits/main":
                        return ("e" if final_base_changed else "b") * 40
                    return "a" * 40
                if argv[:3] == ("git", "diff", "--name-only"):
                    return "\n".join(common.REPORT_FILES)
                if argv[:3] == ("git", "rev-parse", "HEAD"):
                    return "c" * 40
                if argv[:3] == ("gh", "pr", "create"):
                    return "https://github.com/RobLe3/iicp-qualification/pull/999999"
                if argv[:3] == ("gh", "pr", "view"):
                    return json.dumps(
                        {
                            "headRefOid": ("d" if changed_head else "c") * 40,
                            "baseRefOid": ("e" if concurrent_base else "b") * 40,
                            "statusCheckRollup": [
                                {
                                    "name": "qualification-report",
                                    "status": "COMPLETED",
                                    "conclusion": "SUCCESS",
                                }
                            ],
                        }
                    )
                return ""

            args = argparse.Namespace(state_dir=p, source_commit="a" * 40)
            with (
                patch.object(cli, "REPO", p),
                patch.object(cli, "publication_identity", return_value="b" * 40),
                patch.object(cli, "prepare", return_value=successor),
                patch.object(cli, "write_report"),
                patch.object(cli, "verify_committed_report"),
                patch.object(cli, "run", side_effect=fake),
            ):
                if changed_head or concurrent_base or final_base_changed:
                    with self.assertRaises(ValueError):
                        cli.publish(args)
                    self.assertFalse(any(c[:3] == ("gh", "pr", "merge") for c in calls))
                else:
                    cli.publish(args)
                    self.assertTrue(any(c[:3] == ("gh", "pr", "merge") for c in calls))
                    self.assertEqual(len(list(p.glob("*-result.json"))), 1)

    def test_synthetic_positive_publication_through_actual_implementation(self):
        self.publication_fixture()

    def test_changed_pr_head_cannot_merge(self):
        self.publication_fixture(changed_head=True)

    def test_concurrent_public_base_cannot_merge(self):
        self.publication_fixture(concurrent_base=True)

    def test_base_advances_after_green_check_cannot_merge(self):
        self.publication_fixture(final_base_changed=True)

    def test_refusal_cannot_claim_launched_workload(self):
        e = self.event("REFUSED", True)
        with self.assertRaises(ValueError):
            common.validate(
                {"schema": "iicp.qualification-events.v1", "events": [e]}, "events"
            )

    def test_protection_positive_and_missing_guards(self):
        cli.validate_protection(self.protection())
        for key in self.protection():
            data = self.protection()
            del data[key]
            with self.assertRaises(ValueError):
                cli.validate_protection(data)
        data = self.protection()
        data["required_status_checks"]["strict"] = False
        with self.assertRaises(ValueError):
            cli.validate_protection(data)

    def test_committed_report_must_match_generated_bytes(self):
        with patch.object(cli.subprocess, "check_output", return_value=b"changed"):
            with self.assertRaisesRegex(ValueError, "committed report differs"):
                cli.verify_committed_report(
                    "a" * 40, {"reports/status.json": b"expected"}
                )
        with patch.object(cli.subprocess, "check_output", return_value=b"expected"):
            cli.verify_committed_report("a" * 40, {"reports/status.json": b"expected"})

    def test_assume_unchanged_helper_cannot_bypass_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp).resolve()
            (p / "scripts").mkdir()
            helper = p / "scripts/helper.py"
            helper.write_text("value = 1\n")

            def git(*args):
                return subprocess.check_output(
                    ["git", "-C", str(p), *args], stderr=subprocess.PIPE, text=True
                ).strip()

            git("init", "-b", "main")
            git("config", "user.name", "Synthetic")
            git("config", "user.email", "synthetic@example.invalid")
            git("add", ".")
            git("commit", "-m", "synthetic helper")
            head = git("rev-parse", "HEAD")
            git("update-index", "--assume-unchanged", "scripts/helper.py")
            helper.write_text("value = 2\n")
            self.assertEqual(git("status", "--porcelain"), "")
            with self.assertRaisesRegex(ValueError, "dependency differs"):
                validator_modules(p, head, {})

    def test_exact_plan_and_assignment_positive_and_foreign_bindings(self):
        receipt = self.bundle["receipts"]["receipts"][0]
        plan = {
            "plan_sha256": self.bundle["status"]["authority"]["shard_plan_sha256"],
            "shards_per_target": 16,
            "shards": [
                {
                    "target": receipt["target"],
                    "shard_index": receipt["shard_index"],
                    "assignment_sha256": receipt["assignment_sha256"],
                }
            ],
        }
        shard = {
            **plan["shards"][0],
            "plan_sha256": plan["plan_sha256"],
            "shard_count": 16,
        }
        validate_shard_binding(shard, plan)
        for field, value in [
            ("plan_sha256", "sha256:" + "0" * 64),
            ("assignment_sha256", "sha256:" + "0" * 64),
            ("shard_count", 32),
        ]:
            with self.assertRaises(ValueError):
                validate_shard_binding({**shard, field: value}, plan)


if __name__ == "__main__":
    unittest.main()
