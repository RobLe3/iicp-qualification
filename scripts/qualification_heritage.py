#!/usr/bin/env python3
"""Non-publishing heritage inventory, check and minimized projection. Zero credit."""

from __future__ import annotations
import argparse
import copy
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
from jsonschema import Draft202012Validator, FormatChecker  # noqa: E402
from report_common import REPO, canonical, sha, require  # noqa: E402
from heritage_io import (  # noqa: E402
    archive_status,
    discovered,
    no_symlinks,
    safe_relative,
    streamed_hash,
)


def load_canonical(context):
    from collect_status import collect

    b = collect(
        Path(context["root"]),
        context["source_commit"],
        Path(context["sentinel"]),
        Path(context["archive_root"]),
        Path(context["inbox"]),
        context["verified_at"],
    )
    return {
        "source_commit": context["source_commit"],
        "status_sha256": sha(canonical(b["status"])),
        "receipt_count": len(b["receipts"]["receipts"]),
        "receipts": [
            {
                "receipt_file_sha256": r["receipt_file_sha256"],
                "target": r["target"],
                "shard_index": r["shard_index"],
                "evidence_ids": [],
            }
            for r in b["receipts"]["receipts"]
        ],
    }


def evidence_id(root_id, relative):
    return sha(canonical([root_id, relative]))


def inspect(root, relative, config, metadata):
    eid = evidence_id(root["id"], relative)
    r = {
        "evidence_id": eid,
        "root_id": root["id"],
        "relative_path": relative,
        "kind": root["kind"],
        "availability": "MISSING",
        "integrity": "UNVERIFIED",
        "sha256": None,
        "size_bytes": None,
        "occurred_at": metadata.get("occurred_at"),
        "original_outcome": metadata.get("original_outcome"),
        "admission_status": "NOT_ESTABLISHED",
        "supersedes": metadata.get("supersedes", []),
        "archive_status": "NOT_ARCHIVE",
    }
    path = Path(root["path"]) / relative
    if not safe_relative(relative) or not no_symlinks(path):
        r["availability"] = "UNSAFE"
        return r
    try:
        digest, size = streamed_hash(path, config["max_file_bytes"])
        r.update(
            availability="RETAINED", sha256=digest, size_bytes=size, integrity="HASHED"
        )
        if metadata.get("expected_sha256"):
            r["integrity"] = (
                "MATCH" if digest == metadata["expected_sha256"] else "MISMATCH"
            )
        r["archive_status"] = archive_status(path, config)
        if streamed_hash(path, config["max_file_bytes"])[0] != digest:
            r["integrity"] = "MISMATCH"
    except FileNotFoundError:
        pass
    except OverflowError:
        r["availability"] = "OVERSIZE"
    except ValueError:
        r["availability"] = "UNSAFE"
    except OSError:
        r["availability"] = "UNREADABLE"
    return r


def validate_config(c):
    allowed = {
        "schema",
        "roots",
        "max_files",
        "max_file_bytes",
        "max_archive_members",
        "max_archive_uncompressed_bytes",
        "canonical_context",
        "records",
        "dmsc_architecture_ids",
        "dmsc_reviewer_ids",
    }
    require(
        isinstance(c, dict)
        and set(c) <= allowed
        and c.get("schema") == "iicp.heritage-config.v1",
        "invalid config",
    )
    for k in (
        "max_files",
        "max_file_bytes",
        "max_archive_members",
        "max_archive_uncompressed_bytes",
    ):
        require(type(c.get(k)) is int and 0 < c[k] <= 2**40, "invalid bound")
    ids = set()
    for r in c["roots"]:
        require(set(r) == {"id", "path", "kind", "excludes"}, "invalid root contract")
        require(
            re.fullmatch("[a-z0-9][a-z0-9-]{0,79}", r["id"]) and r["id"] not in ids,
            "duplicate/invalid root",
        )
        require(
            Path(r["path"]).is_absolute()
            and re.fullmatch("[a-z0-9][a-z0-9-]{0,79}", r["kind"]),
            "invalid root",
        )
        require(all(isinstance(x, str) for x in r["excludes"]), "invalid exclusions")
        ids.add(r["id"])
    records = set()
    for r in c.get("records", []):
        require(
            set(r)
            <= {
                "root_id",
                "relative_path",
                "expected_sha256",
                "occurred_at",
                "supersedes",
                "original_outcome",
            },
            "invalid record",
        )
        key = (r["root_id"], r["relative_path"])
        require(
            key not in records
            and r["root_id"] in ids
            and safe_relative(r["relative_path"]),
            "duplicate/unsafe record",
        )
        records.add(key)
        if r.get("expected_sha256"):
            require(
                re.fullmatch("sha256:[0-9a-f]{64}", r["expected_sha256"]),
                "invalid expected digest",
            )
    require(len(records) <= c["max_files"], "explicit records exceed bound")


def inventory(config):
    validate_config(config)
    c = copy.deepcopy(config)
    roots = sorted(c["roots"], key=lambda r: r["id"])
    canonical_index = load_canonical(c["canonical_context"])
    objects = []
    gaps = []
    require(
        canonical_index["source_commit"] == c["canonical_context"]["source_commit"],
        "stale canonical identity",
    )
    metadata = {(r["root_id"], r["relative_path"]): r for r in c.get("records", [])}
    selected = set(metadata)
    for root in roots:
        path = Path(root["path"])
        if not no_symlinks(path):
            gaps.append({"code": "unsafe-root", "evidence_id": None})
            continue
        if not path.is_dir():
            gaps.append({"code": "missing-root", "evidence_id": None})
            continue
        discovery_errors = []
        for relative in discovered(path, root["excludes"], discovery_errors):
            key = (root["id"], relative)
            if key in selected:
                continue
            if len(selected) >= c["max_files"]:
                gaps.append({"code": "discovery-bound-reached", "evidence_id": None})
                break
            selected.add(key)
        gaps.extend(
            {"code": "unreadable-discovery-directory", "evidence_id": None}
            for _ in discovery_errors
        )
    rootmap = {r["id"]: r for r in roots}
    for key in sorted(selected):
        objects.append(inspect(rootmap[key[0]], key[1], c, metadata.get(key, {})))
    byhash = {}
    for r in objects:
        if (
            r["availability"] == "RETAINED"
            and r["integrity"] in ("HASHED", "MATCH")
            and r["archive_status"] in ("NOT_ARCHIVE", "SAFE_METADATA")
            and r["kind"] not in ("diagnostic", "rejected", "sentinel")
        ):
            byhash.setdefault(r["sha256"], []).append(r)
        if (
            r["availability"] != "RETAINED"
            or r["integrity"] == "MISMATCH"
            or r["archive_status"] in ("UNSAFE", "OVERSIZE", "UNREADABLE")
        ):
            gaps.append({"code": "object-unresolved", "evidence_id": r["evidence_id"]})
    for r in canonical_index["receipts"]:
        matches = byhash.get(r["receipt_file_sha256"], [])
        r["evidence_ids"] = sorted(m["evidence_id"] for m in matches)
        for m in matches:
            m["admission_status"] = "ACCEPTED_REFERENCE"
        if not matches:
            gaps.append({"code": "canonical-receipt-unresolved", "evidence_id": None})
    for r in objects:
        for parent in r["supersedes"]:
            if parent not in {x["evidence_id"] for x in objects}:
                gaps.append(
                    {
                        "code": "supersession-reference-unresolved",
                        "evidence_id": r["evidence_id"],
                    }
                )
    value = {
        "schema": "iicp.qualification-heritage.v1",
        "historical_inventory_complete": False,
        "qualification_credit": 0,
        "config_sha256": sha(canonical(c)),
        "roots": [{"id": r["id"], "kind": r["kind"]} for r in roots],
        "exclusions": [
            {"root_id": r["id"], "pattern": p}
            for r in roots
            for p in sorted(r["excludes"])
        ],
        "objects": objects,
        "canonical": canonical_index,
        "gaps": sorted(gaps, key=lambda g: (g["code"], g["evidence_id"] or "")),
        "dmsc": {
            "architecture": c.get(
                "dmsc_architecture_ids", [f"D{i:02}" for i in range(1, 15)]
            ),
            "reviewer": c.get("dmsc_reviewer_ids", [f"V{i:02}" for i in range(1, 14)]),
            "claim_status": "UNASSESSED",
        },
        "summary": {
            "objects": len(objects),
            "retained": sum(r["availability"] == "RETAINED" for r in objects),
            "unresolved": len(gaps),
            "credited_receipt_count": canonical_index["receipt_count"],
        },
    }
    check(value)
    return value


def check(value):
    schema = json.loads((REPO / "schemas/heritage-v1.json").read_text())
    errors = list(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value)
    )
    require(not errors, "invalid heritage schema")
    roots = {r["id"] for r in value["roots"]}
    require(len(roots) == len(value["roots"]), "duplicate roots")
    objects = {r["evidence_id"]: r for r in value["objects"]}
    require(len(objects) == len(value["objects"]), "duplicate objects")
    for r in objects.values():
        require(
            r["root_id"] in roots
            and safe_relative(r["relative_path"])
            and r["evidence_id"] == evidence_id(r["root_id"], r["relative_path"]),
            "foreign object identity",
        )
        require(
            r["availability"] != "RETAINED"
            or (r["sha256"] is not None and r["size_bytes"] is not None),
            "retained content unresolved",
        )
        require(r["evidence_id"] not in r["supersedes"], "self supersession")
    pending = {eid: set(r["supersedes"]) & objects.keys() for eid, r in objects.items()}
    while pending:
        ready = {eid for eid, parents in pending.items() if not parents}
        require(ready, "cyclic supersession")
        pending = {
            eid: parents - ready for eid, parents in pending.items() if eid not in ready
        }
    receipts = value["canonical"]["receipts"]
    require(
        len(receipts) == value["canonical"]["receipt_count"], "receipt count mismatch"
    )
    require(
        len({(r["target"], r["shard_index"]) for r in receipts}) == len(receipts),
        "duplicate assignment",
    )
    require(
        len({r["receipt_file_sha256"] for r in receipts}) == len(receipts),
        "duplicate receipt",
    )
    joined = set()
    for r in receipts:
        require(len(set(r["evidence_ids"])) == len(r["evidence_ids"]), "duplicate join")
        for eid in r["evidence_ids"]:
            require(eid in objects, "missing joined object")
            o = objects[eid]
            require(
                o["sha256"] == r["receipt_file_sha256"]
                and o["availability"] == "RETAINED"
                and o["integrity"] in ("HASHED", "MATCH")
                and o["archive_status"] in ("NOT_ARCHIVE", "SAFE_METADATA")
                and o["kind"] not in ("diagnostic", "rejected", "sentinel")
                and o["admission_status"] == "ACCEPTED_REFERENCE",
                "invalid admission join",
            )
            joined.add(eid)
    require(
        all(
            (r["admission_status"] == "ACCEPTED_REFERENCE")
            == (r["evidence_id"] in joined)
            for r in objects.values()
        ),
        "unbacked admission",
    )
    expected = {
        "objects": len(objects),
        "retained": sum(r["availability"] == "RETAINED" for r in objects.values()),
        "unresolved": len(value["gaps"]),
        "credited_receipt_count": len(receipts),
    }
    require(value["summary"] == expected, "summary mismatch")
    required = Counter()
    for o in objects.values():
        if (
            o["availability"] != "RETAINED"
            or o["integrity"] == "MISMATCH"
            or o["archive_status"] in ("UNSAFE", "OVERSIZE", "UNREADABLE")
        ):
            required[("object-unresolved", o["evidence_id"])] += 1
        for previous in o["supersedes"]:
            if previous not in objects:
                required[("supersession-reference-unresolved", o["evidence_id"])] += 1
    for receipt in receipts:
        if not receipt["evidence_ids"]:
            required[("canonical-receipt-unresolved", None)] += 1
    actual = Counter((g["code"], g["evidence_id"]) for g in value["gaps"])
    require(all(actual[k] >= n for k, n in required.items()), "known gaps omitted")


def project(value):
    check(value)
    result = {
        "schema": "iicp.qualification-heritage-public.v1",
        "historical_inventory_complete": False,
        "qualification_credit": 0,
        "config_sha256": value["config_sha256"],
        "canonical": copy.deepcopy(value["canonical"]),
        "summary": copy.deepcopy(value["summary"]),
        "dmsc": copy.deepcopy(value["dmsc"]),
    }
    schema = json.loads((REPO / "schemas/heritage-v1.json").read_text())
    require(
        not list(
            Draft202012Validator(
                schema["$defs"]["public"], format_checker=FormatChecker()
            ).iter_errors(result)
        ),
        "invalid public heritage projection",
    )
    return result


def write_private(path, value):
    path = path.absolute()
    require(no_symlinks(path), "unsafe output")
    parent = path.parent.stat()
    require(
        parent.st_uid == os.getuid() and parent.st_mode & 0o077 == 0,
        "output requires private parent",
    )
    require(
        not path.is_relative_to(REPO), "outputs must remain outside public checkout"
    )
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(value, f, sort_keys=True, indent=2)
        f.write("\n")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("inventory")
    a.add_argument("--config", required=True, type=Path)
    a.add_argument("--output", required=True, type=Path)
    a = sub.add_parser("check")
    a.add_argument("--input", required=True, type=Path)
    a.add_argument("--config", type=Path)
    a = sub.add_parser("project")
    a.add_argument("--input", required=True, type=Path)
    a.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    if a.command == "inventory":
        write_private(a.output, inventory(json.loads(a.config.read_text())))
    else:
        value = json.loads(a.input.read_text())
        check(value)
        if a.command == "project":
            write_private(a.output, project(value))
        elif a.config:
            require(
                inventory(json.loads(a.config.read_text())) == value,
                "source inventory changed",
            )
    print(
        "PASS: bounded derivative; historical completeness not established; no publication"
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print("REFUSED: " + type(error).__name__, file=sys.stderr)
        raise SystemExit(1)
