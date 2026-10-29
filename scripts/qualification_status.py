#!/usr/bin/env python3
"""Record, prepare, check and publish bounded qualification reports; never run tests."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
from report_common import (  # noqa: E402
    REPO,
    REPORT_FILES,
    canonical,
    check_public,
    encoded,
    load,
    require,
    sha,
    validate,
)


def run(*args: str, cwd: Path = REPO) -> str:
    return subprocess.check_output(
        list(args), cwd=cwd, text=True, stderr=subprocess.PIPE
    ).strip()


def now() -> str:
    return (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )


def atomic(path: Path, data: bytes) -> None:
    require(not path.is_symlink(), "symlink output is forbidden")
    path.parent.mkdir(parents=True, exist_ok=True)
    require(
        not any(parent.is_symlink() for parent in path.parents),
        "symlink output parent is forbidden",
    )
    fd, name = tempfile.mkstemp(prefix=".report-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def record(args: argparse.Namespace) -> None:
    require(
        args.inbox.parent.is_dir() and args.inbox.parent.stat().st_mode & 0o077 == 0,
        "private inbox parent must be owner-only",
    )
    source = args.source.resolve(strict=True)
    require(
        source.is_file() and not args.source.is_symlink(),
        "activity source must be a regular file",
    )
    source_digest = sha(source.read_bytes())
    event = {
        "kind": args.kind,
        "outcome": args.outcome,
        "reason": args.reason,
        "next_gate": args.next_gate,
        "occurred_at": args.occurred_at,
        "workload_launched": args.workload_launched,
        "source_sha256": source_digest,
        "qualification_credit": 0,
    }
    event["event_id"] = sha(canonical(event))
    validate({"schema": "iicp.qualification-events.v1", "events": [event]}, "events")
    # Serializes append operations; a reporting lock never touches workload ownership.
    with (args.inbox.parent / ".inbox.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        inbox = (
            load(args.inbox)
            if args.inbox.exists()
            else {"schema": "iicp.reporting-inbox.v1", "entries": []}
        )
        if any(x["event"]["event_id"] == event["event_id"] for x in inbox["entries"]):
            print("NO_CHANGE")
            return
        inbox["entries"].append(
            {"source": str(source), "source_sha256": source_digest, "event": event}
        )
        atomic(
            args.inbox, (json.dumps(inbox, indent=2, sort_keys=True) + "\n").encode()
        )
    print(event["event_id"])


def preserve_history(previous: dict, successor: dict) -> None:
    old = previous["events"]["events"]
    require(
        successor["events"]["events"][: len(old)] == old,
        "activity history cannot be rewritten",
    )
    for key, count in previous["status"]["accepted"].items():
        require(
            successor["status"]["accepted"][key] >= count,
            "credit decrease requires explicit review",
        )
    old_receipts = {
        x["receipt_file_sha256"]: x for x in previous["receipts"]["receipts"]
    }
    new_receipts = {
        x["receipt_file_sha256"]: x for x in successor["receipts"]["receipts"]
    }
    require(
        all(new_receipts.get(key) == value for key, value in old_receipts.items()),
        "accepted receipt projection changed",
    )


def material_identity(bundle: dict) -> tuple:
    status = bundle["status"]
    return tuple(
        status[key]
        for key in (
            "inputs_sha256",
            "events_sha256",
            "receipts_sha256",
            "reporting_policy_sha256",
        )
    )


def prepare(args: argparse.Namespace) -> dict:
    from collect_status import collect

    bundle = collect(
        args.root.resolve(),
        args.source_commit,
        args.sentinel,
        args.archive_root,
        args.inbox,
        args.verified_at or now(),
    )
    encoded(bundle)  # Validate before any public-tree write.
    if (REPO / "reports/status.json").exists():
        previous = check_public()
        preserve_history(previous, bundle)
        if material_identity(previous) == material_identity(bundle):
            return previous
    return bundle


def report_check(args: argparse.Namespace) -> None:
    current = check_public()
    if args.root:
        require(
            all((args.source_commit, args.sentinel, args.archive_root, args.inbox)),
            "freshness check needs complete source bindings",
        )
        fresh = prepare(args)
        require(
            encoded(current) == encoded(fresh),
            "STALE: registered activity or qualification inputs changed",
        )
    print(
        "PASS: public consistency"
        + (
            " and source freshness"
            if args.root
            else " only; private-source freshness not checked"
        )
    )


def eligible_changes(changed: list[str]) -> None:
    require(
        bool(changed) and set(changed) <= set(REPORT_FILES),
        "automatic publication is report-only",
    )


def write_report(bundle: dict) -> None:
    for relative, data in encoded(bundle).items():
        atomic(REPO / relative, data)


def publication_identity() -> str:
    remote = run("git", "remote", "get-url", "origin")
    require(
        remote
        in {
            "https://github.com/RobLe3/iicp-qualification.git",
            "git@github.com:RobLe3/iicp-qualification.git",
        },
        "unexpected public destination",
    )
    require(
        run("git", "branch", "--show-current") == "main",
        "publication starts from public main",
    )
    require(
        not run("git", "status", "--porcelain", "--untracked-files=all"),
        "public checkout must be clean",
    )
    base = run(
        "gh", "api", "repos/RobLe3/iicp-qualification/commits/main", "--jq", ".sha"
    )
    require(run("git", "rev-parse", "HEAD") == base, "local public main is stale")
    return base


def publish(args: argparse.Namespace) -> None:
    require(
        args.state_dir.is_dir() and args.state_dir.stat().st_mode & 0o077 == 0,
        "private publication state directory required",
    )
    with (args.state_dir / ".publication.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        base = publication_identity()
        source_main = run(
            "gh", "api", "repos/RobLe3/iicp.network/commits/main", "--jq", ".sha"
        )
        require(source_main == args.source_commit, "source is not current merged main")
        previous = check_public()
        bundle = prepare(args)
        if encoded(previous) == encoded(bundle):
            print("NO_CHANGE")
            return
        preserve_history(previous, bundle)
        tree_content = encoded(bundle)
        branch = "report/" + sha(canonical(bundle))[7:23]
        intent = {
            "schema": "iicp.reporting-publication.v1",
            "base": base,
            "source_commit": source_main,
            "branch": branch,
            "prepared_at": now(),
        }
        intent_path = args.state_dir / (branch.replace("/", "-") + ".json")
        require(
            not intent_path.exists(),
            "publication attempt already recorded; inspect retained outcome",
        )
        atomic(
            intent_path, (json.dumps(intent, indent=2, sort_keys=True) + "\n").encode()
        )
        run("git", "switch", "-c", branch)
        write_report(bundle)
        changed = run("git", "diff", "--name-only", base).splitlines()
        eligible_changes(changed)
        require(
            all(
                (REPO / path).read_bytes() == data
                for path, data in tree_content.items()
            ),
            "generated bytes changed",
        )
        run("git", "add", "--", *REPORT_FILES)
        run("git", "commit", "-m", "docs: refresh verified qualification report")
        head = run("git", "rev-parse", "HEAD")
        eligible_changes(run("git", "diff", "--name-only", base, head).splitlines())
        run("git", "push", "-u", "origin", branch)
        url = run(
            "gh",
            "pr",
            "create",
            "--repo",
            "RobLe3/iicp-qualification",
            "--base",
            "main",
            "--head",
            branch,
            "--title",
            "Refresh verified qualification report",
            "--body",
            "Deterministic report-only update under the reviewed reporting policy. No qualification authority or credit is granted by this PR.",
        )
        # Polling observes one required check. It never reruns CI or a workload.
        deadline = time.monotonic() + 180
        while True:
            pr = json.loads(
                run(
                    "gh",
                    "pr",
                    "view",
                    url,
                    "--repo",
                    "RobLe3/iicp-qualification",
                    "--json",
                    "headRefOid,baseRefOid,statusCheckRollup",
                )
            )
            require(
                pr["headRefOid"] == head and pr["baseRefOid"] == base,
                "PR identity changed",
            )
            checks = [
                x
                for x in pr["statusCheckRollup"]
                if x.get("name") == "qualification-report"
            ]
            require(len(checks) <= 1, "ambiguous required check")
            if checks and checks[0].get("status") == "COMPLETED":
                require(
                    checks[0].get("conclusion") == "SUCCESS", "public validation failed"
                )
                break
            require(
                time.monotonic() < deadline,
                "public validation remains pending; no merge",
            )
            time.sleep(5)
        require(
            run("gh", "api", "repos/RobLe3/iicp.network/commits/main", "--jq", ".sha")
            == source_main,
            "source advanced before report merge",
        )
        require(
            encoded(prepare(args)) == tree_content,
            "source or activity changed before report merge",
        )
        run(
            "gh",
            "pr",
            "merge",
            url,
            "--repo",
            "RobLe3/iicp-qualification",
            "--squash",
            "--match-head-commit",
            head,
        )
        result = {**intent, "head": head, "pull_request": url, "merged_at": now()}
        atomic(
            args.state_dir / (branch.replace("/", "-") + "-result.json"),
            (json.dumps(result, indent=2, sort_keys=True) + "\n").encode(),
        )
        run("git", "switch", "main")
        run("git", "pull", "--ff-only", "origin", "main")
        print(url)


def source_args(parser: argparse.ArgumentParser, required: bool) -> None:
    parser.add_argument("--root", type=Path, required=required)
    parser.add_argument("--source-commit", required=required)
    parser.add_argument("--sentinel", type=Path, required=required)
    parser.add_argument("--archive-root", type=Path, required=required)
    parser.add_argument("--inbox", type=Path, required=required)
    parser.add_argument("--verified-at")


def context_args(args: argparse.Namespace) -> None:
    context = getattr(args, "context", None)
    if not context:
        return
    require(
        context.is_file()
        and not context.is_symlink()
        and context.stat().st_mode & 0o077 == 0,
        "context must be an owner-only regular file",
    )
    value = load(context)
    expected = {
        "root",
        "source_commit",
        "sentinel",
        "archive_root",
        "inbox",
        "state_dir",
    }
    require(set(value) == expected, "invalid reporting context")
    for key, item in value.items():
        setattr(args, key, item if key == "source_commit" else Path(item))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("record", "finish"):
        rec = sub.add_parser(command)
        rec.add_argument("--inbox", type=Path, required=command == "record")
        rec.add_argument("--source", type=Path, required=True)
        for name in ("kind", "outcome", "reason", "next-gate", "occurred-at"):
            rec.add_argument("--" + name, required=True)
        rec.add_argument("--workload-launched", action="store_true")
        if command == "finish":
            rec.add_argument("--context", type=Path, required=True)
            rec.set_defaults(verified_at=None)
    source_args(sub.add_parser("prepare"), True)
    check = sub.add_parser("check")
    source_args(check, False)
    check.add_argument("--context", type=Path)
    pub = sub.add_parser("publish")
    source_args(pub, True)
    pub.add_argument("--state-dir", type=Path, required=True)
    args = parser.parse_args()
    context_args(args)
    if getattr(args, "source_commit", None):
        require(
            re.fullmatch(r"[0-9a-f]{40}", args.source_commit) is not None,
            "exact source commit required",
        )
    if args.command == "record":
        record(args)
    elif args.command == "finish":
        record(args)
        publish(args)
    elif args.command == "prepare":
        write_report(prepare(args))
        print("PREPARED: not published")
    elif args.command == "check":
        report_check(args)
    elif args.command == "publish":
        publish(args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        # Never dump captured subprocess output or arbitrary source data into public logs.
        print(
            f"REFUSED: {type(exc).__name__}: "
            + (
                str(exc)
                if isinstance(exc, ValueError)
                else "inspect private local context"
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)
