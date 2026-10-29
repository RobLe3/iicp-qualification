"""Read pinned root evidence using its existing validators. No ledger writes."""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

from report_common import REPO, canonical, load, require, sha

INPUTS = {
    "candidate": "project/pre1-stability-successor-frozen.json",
    "registry": "project/pre1-successor-executor-registry.json",
    "plan": "project/pre1-successor-qualification-shard-plan.json",
    "matrix": "project/pre1-support-matrix.json",
    "support": "project/pre1-support-results.json",
    "catalog": "project/pre1-edge-case-catalog.json",
    "edges": "project/pre1-edge-case-results.json",
}


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def bound_file(root: Path, relative: str, commit: str, inputs: dict) -> dict:
    path = root / relative
    require(
        not Path(relative).is_absolute() and ".." not in Path(relative).parts,
        "foreign evidence reference",
    )
    require(
        path.resolve().is_relative_to(root.resolve()) and not path.is_symlink(),
        "unsafe evidence path",
    )
    data = path.read_bytes()
    original = subprocess.check_output(
        ["git", "-C", str(root), "show", f"{commit}:{relative}"]
    )
    require(data == original, "source contents differ from pinned commit")
    inputs[relative] = sha(data)
    return json.loads(data)


def private_events(path: Path) -> tuple[dict, str]:
    journal = load(path)
    require(
        set(journal) == {"schema", "entries"}
        and journal["schema"] == "iicp.reporting-inbox.v1",
        "invalid private journal",
    )
    events = []
    for entry in journal["entries"]:
        require(
            set(entry) == {"source", "source_sha256", "event"}, "invalid private entry"
        )
        source = Path(entry["source"])
        require(
            source.is_absolute() and source.is_file() and not source.is_symlink(),
            "missing private activity evidence",
        )
        require(
            sha(source.read_bytes()) == entry["source_sha256"],
            "private activity source changed",
        )
        event = entry["event"]
        require(
            event["source_sha256"] == entry["source_sha256"],
            "activity source binding mismatch",
        )
        events.append(event)
    return {"schema": "iicp.qualification-events.v1", "events": events}, sha(
        canonical(journal)
    )


def validator_modules(root: Path, commit: str, inputs: dict) -> dict:
    require(git(root, "rev-parse", "HEAD") == commit, "root checkout revision differs")
    require(
        not git(
            root, "status", "--porcelain", "--untracked-files=all", "--", "scripts"
        ),
        "validator source is not clean",
    )
    # Bind every tracked Python helper, including transitive imports. Do not execute a working-tree substitute.
    for relative in git(root, "ls-files", "scripts").splitlines():
        if relative.endswith(".py"):
            path = root / relative
            require(not path.is_symlink(), "symlinked validator dependency")
            data = path.read_bytes()
            original = subprocess.check_output(
                ["git", "-C", str(root), "show", f"{commit}:{relative}"]
            )
            require(data == original, "validator dependency differs from pinned commit")
            inputs[relative] = sha(data)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / "scripts"))
    names = (
        "check_pre1_support_matrix",
        "check_pre1_edge_cases",
        "check_pre1_qualification_receipt",
        "compile_pre1_sentinel_ledger",
        "plan_pre1_qualification_shards",
    )
    return {name: importlib.import_module(name) for name in names}


def receipt_derivative(receipt: dict, digest: str) -> dict:
    return {
        "receipt_id": receipt["receipt_id"],
        "receipt_file_sha256": digest,
        "candidate_manifest_sha256": receipt["candidate_manifest_sha256"],
        "executor_registry_sha256": receipt["execution_bindings"][
            "executor_registry_sha256"
        ],
        "environment_sha256": receipt["execution_bindings"][
            "qualification_environment_sha256"
        ],
        "assignment_sha256": receipt["shard"]["assignment_sha256"],
        "target": receipt["target"],
        "shard_index": receipt["shard"]["shard_index"],
        "started_at": receipt["started_at"],
        "finished_at": receipt["finished_at"],
        "admission_status": "accepted-in-merged-ledgers",
        "evidence_class": "qualification",
        "status": "PASS",
        "original_access": "private",
        "is_derivative": True,
        "support_cells": sorted(receipt["coverage"]["support_cells"]),
        "edge_executions": sorted(receipt["coverage"]["edge_executions"]),
    }


def validate_shard_binding(shard: dict, plan: dict) -> None:
    require(
        shard["plan_sha256"] == plan["plan_sha256"],
        "receipt binds a different shard plan",
    )
    require(
        shard["shard_count"] == plan["shards_per_target"],
        "receipt shard count differs from frozen plan",
    )
    rows = [
        row
        for row in plan["shards"]
        if row["target"] == shard["target"]
        and row["shard_index"] == shard["shard_index"]
    ]
    require(
        len(rows) == 1 and rows[0]["assignment_sha256"] == shard["assignment_sha256"],
        "receipt assignment binding differs from frozen plan",
    )


def collect(
    root: Path,
    commit: str,
    sentinel: Path,
    archive: Path,
    inbox: Path,
    verified_at: str,
) -> dict:
    policy = load(REPO / "reporting-policy.json")
    inputs = {}
    modules = validator_modules(root, commit, inputs)
    data = {
        name: bound_file(root, path, commit, inputs) for name, path in INPUTS.items()
    }
    candidate, registry, plan = data["candidate"], data["registry"], data["plan"]
    authority = {
        "candidate_file_sha256": inputs[INPUTS["candidate"]],
        "candidate_manifest_sha256": candidate["manifest_sha256"],
        "executor_registry_sha256": registry["binding_sha256"],
        "shard_plan_sha256": plan["plan_sha256"],
        "sentinel_ledger_sha256": load(sentinel)["ledger_sha256"],
    }
    require(
        authority == policy["authority"],
        "authority differs from reviewed reporting policy",
    )
    support_check = modules["check_pre1_support_matrix"]
    edge_check = modules["check_pre1_edge_cases"]
    receipt_check = modules["check_pre1_qualification_receipt"]
    require(
        not support_check.validate(data["matrix"], data["support"], root, candidate),
        "canonical support validation failed",
    )
    require(
        not edge_check.validate(
            data["catalog"], data["edges"], data["matrix"], root, candidate
        ),
        "canonical edge validation failed",
    )
    shard_check = modules["plan_pre1_qualification_shards"]
    require(
        not shard_check._validate_plan_bindings(
            plan, candidate, data["matrix"], data["catalog"], registry
        ),
        "shard-plan binding failed",
    )
    credited_support, credited_edges = {}, {}
    for row in data["support"]["results"]:
        if row["status"] == "PASS":
            credited_support.setdefault(row["evidence_ref"], []).append(row["cell_id"])
    for row in data["edges"]["results"]:
        if row["status"] == "PASS":
            credited_edges.setdefault(row["evidence_ref"], []).append(
                f"{row['scenario_id']}::{row['cell_id']}"
            )
    derivatives = []
    for ref in sorted(set(credited_support) | set(credited_edges)):
        receipt = bound_file(root, ref, commit, inputs)
        require(
            receipt["status"] == "PASS"
            and receipt["evidence_class"] == "qualification",
            "unaccepted evidence class",
        )
        require(
            not receipt_check.validate(receipt, candidate, registry),
            "original receipt validation failed",
        )
        require(
            sorted(receipt["coverage"]["support_cells"])
            == sorted(credited_support.get(ref, [])),
            "partial or mismatched support admission",
        )
        require(
            sorted(receipt["coverage"]["edge_executions"])
            == sorted(credited_edges.get(ref, [])),
            "partial or mismatched edge admission",
        )
        sh = receipt["shard"]
        validate_shard_binding(sh, plan)
        assignment = shard_check.reconstruct_assignment(
            data["matrix"],
            data["catalog"],
            sh["target"],
            sh["shard_index"],
            sh["shard_count"],
        )
        require(
            assignment["support"] == sorted(receipt["coverage"]["support_cells"])
            and assignment["edge"] == sorted(receipt["coverage"]["edge_executions"]),
            "receipt differs from frozen assignment",
        )
        derivatives.append(receipt_derivative(receipt, inputs[ref]))
    ledger = load(sentinel)
    require(
        not modules["compile_pre1_sentinel_ledger"].validate_ledger(
            ledger, candidate, registry, plan
        ),
        "sentinel ledger invalid",
    )
    inputs["sentinel-ledger"] = sha(sentinel.read_bytes())
    sentinels = []
    for row in ledger["sentinels"]:
        path = archive / row["receipt"]
        require(
            path.resolve().is_relative_to(archive.resolve()) and not path.is_symlink(),
            "foreign sentinel reference",
        )
        require(
            sha(path.read_bytes()) == row["receipt_sha256"],
            "sentinel receipt digest differs",
        )
        sentinel_receipt = load(path)
        require(
            not receipt_check.validate(sentinel_receipt, candidate, registry),
            "sentinel receipt validation failed",
        )
        validate_shard_binding(sentinel_receipt["shard"], plan)
        require(
            sentinel_receipt["shard"]["shard_index"] == 0
            and sentinel_receipt["target"] == row["target"],
            "sentinel target or index differs",
        )
        sentinels.append(
            {
                "target": row["target"],
                "receipt_file_sha256": row["receipt_sha256"],
                "extra_campaign_credit": 0,
            }
        )
    # Certificate admission is deliberately not inferred from a file name or a successful run.
    certificate_search = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "grep",
            "-l",
            "-E",
            '"schema"[[:space:]]*:[[:space:]]*"iicp\\.pre1-(target|ecosystem)-certificate\\.',
            commit,
            "--",
            "reports/*.json",
            "reports/**/*.json",
            "project/*.json",
            "project/**/*.json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        certificate_search.returncode == 1,
        "certificate evidence or inspection error requires reviewed report mapping",
    )
    events, _ = private_events(inbox)
    receipts = {
        "schema": "iicp.qualification-receipt-index.v1",
        "receipts": sorted(derivatives, key=lambda x: (x["target"], x["shard_index"])),
    }
    status = {
        "schema": "iicp.qualification-status.v1",
        "source_repository": "RobLe3/iicp.network",
        "source_commit": commit,
        "verified_at": verified_at,
        "authority": authority,
        "inputs_sha256": sha(canonical(inputs)),
        "events_sha256": sha(canonical(events)),
        "receipts_sha256": sha(canonical(receipts)),
        "reporting_policy_sha256": sha((REPO / "reporting-policy.json").read_bytes()),
        "required": policy["required"],
        "accepted": {
            "shards": len(derivatives),
            "support_cells": sum(len(x["support_cells"]) for x in derivatives),
            "edge_executions": sum(len(x["edge_executions"]) for x in derivatives),
            "sentinels": len(sentinels),
            "certificates": 0,
        },
        "platforms": [],
        "sentinels": sorted(sentinels, key=lambda x: x["target"]),
        "non_authorizing": True,
        "historical_inventory_complete": False,
        "validation_scope": "retained-receipts-and-merged-ledgers",
    }
    for target in policy["targets"]:
        indexes = sorted(x["shard_index"] for x in derivatives if x["target"] == target)
        status["platforms"].append(
            {
                "target": target,
                "accepted_shards": indexes,
                "remaining_shards": [i for i in range(16) if i not in indexes],
            }
        )
    return {"status": status, "receipts": receipts, "events": events}
