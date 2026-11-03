"""Private bounded discovery checkpoints; never qualification authority."""

from __future__ import annotations
import argparse
import copy
import fnmatch
import json
import os
import stat
from pathlib import Path
from jsonschema import Draft202012Validator
import qualification_heritage as heritage
from heritage_io import no_symlinks, safe_relative
from report_common import REPO, canonical, require, sha

DIRECTORY_LIMIT = 10000


def stamp(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mtime_ns, s.st_ctime_ns]


def validate(page, config):
    heritage.validate_config(config)
    schema = json.loads((REPO / "schemas/heritage-partitions-v1.json").read_text())
    require(
        not list(Draft202012Validator(schema).iter_errors(page)), "invalid partition"
    )
    require(page["config_sha256"] == sha(canonical(config)), "changed config")
    unsigned = {k: v for k, v in page.items() if k != "page_sha256"}
    require(page["page_sha256"] == sha(canonical(unsigned)), "changed checkpoint")
    roots = {r["id"] for r in config["roots"]}
    for d in page["directories"] + page["gaps"]:
        require(
            d["root_id"] in roots
            and (d["relative_path"] == "" or safe_relative(d["relative_path"])),
            "unsafe directory history",
        )
    keys = []
    for row in page["frontier"] + page["records"]:
        require(
            row["root_id"] in roots
            and (row["relative_path"] == "" or safe_relative(row["relative_path"])),
            "unsafe locator",
        )
        keys.append((row["root_id"], row["relative_path"]))
    require(len(keys) == len(set(keys)), "duplicate frontier or record")
    require(page["discovery_exhausted"] == (not page["frontier"]), "false exhaustion")
    require(len(page["records"]) <= config["max_files"], "partition bound")


def discover(config, previous=None, steps=1000):
    heritage.validate_config(config)
    require(
        type(steps) is int and 0 < steps <= min(config["max_files"], DIRECTORY_LIMIT),
        "invalid steps",
    )
    roots = {r["id"]: r for r in config["roots"]}
    gaps = []
    if previous is not None:
        validate(previous, config)
        require(not previous["discovery_exhausted"], "discovery already exhausted")
        frontier = copy.deepcopy(previous["frontier"])
        directories = copy.deepcopy(previous["directories"])
        for directory in directories:
            path = (
                Path(roots[directory["root_id"]]["path"]) / directory["relative_path"]
            )
            require(
                no_symlinks(path) and stamp(path) == directory["directory_stamp"],
                "previously discovered directory changed",
            )
    else:
        frontier = [
            {"root_id": rid, "relative_path": "", "directory_stamp": None}
            for rid in sorted(roots)
        ]
    if previous is None:
        directories = []
    records = []
    for _ in range(steps):
        if not frontier:
            break
        row = frontier.pop(0)
        root = roots[row["root_id"]]
        relative = row["relative_path"]
        path = Path(root["path"]) / relative
        try:
            if not no_symlinks(path):
                if relative:
                    records.append(
                        {"root_id": row["root_id"], "relative_path": relative}
                    )
                else:
                    gaps.append({"code": "unsafe-root", **row})
                continue
            s = path.lstat()
            if stat.S_ISDIR(s.st_mode):
                before = stamp(path)
                require(
                    row["directory_stamp"] is None or row["directory_stamp"] == before,
                    "directory changed since checkpoint",
                )
                children = []
                # Enumeration and sorting have a hard independent bound.
                with os.scandir(path) as entries:
                    for entry_index, entry in enumerate(entries):
                        if entry_index >= DIRECTORY_LIMIT:
                            raise OverflowError("directory limit")
                        child = f"{relative}/{entry.name}" if relative else entry.name
                        if any(
                            fnmatch.fnmatch(child, p) or fnmatch.fnmatch(entry.name, p)
                            for p in root["excludes"]
                        ):
                            continue
                        require(safe_relative(child), "unsafe discovered name")
                        ep = Path(entry.path)
                        ds = stamp(ep) if entry.is_dir(follow_symlinks=False) else None
                        children.append(
                            {
                                "root_id": row["root_id"],
                                "relative_path": child,
                                "directory_stamp": ds,
                            }
                        )
                require(stamp(path) == before, "directory changed during discovery")
                directories.append({**row, "directory_stamp": before})
                require(len(directories) <= DIRECTORY_LIMIT, "directory history bound")
                frontier = sorted(children, key=lambda x: x["relative_path"]) + frontier
                require(len(frontier) <= DIRECTORY_LIMIT * 2, "frontier bound")
            else:
                records.append({"root_id": row["root_id"], "relative_path": relative})
        except (OSError, OverflowError) as error:
            gaps.append(
                {
                    "code": "directory-bound"
                    if isinstance(error, OverflowError)
                    else "unavailable-path",
                    **row,
                }
            )
    page = {
        "schema": "iicp.heritage-partition.v1",
        "config_sha256": sha(canonical(config)),
        "index": previous["index"] + 1 if previous else 0,
        "previous_sha256": previous["page_sha256"] if previous else None,
        "frontier": frontier,
        "directories": directories,
        "records": records,
        "gaps": gaps,
        "discovery_exhausted": not frontier,
        "historical_inventory_complete": False,
        "qualification_credit": 0,
    }
    page["page_sha256"] = sha(canonical(page))
    validate(page, config)
    return page


def validate_chain(config, pages):
    require(bool(pages), "missing partitions")
    previous = None
    seen = set()
    for index, page in enumerate(pages):
        validate(page, config)
        require(
            page["index"] == index and page["previous_sha256"] == previous,
            "broken partition chain",
        )
        require(
            index == len(pages) - 1 or not page["discovery_exhausted"],
            "page after exhaustion",
        )
        for row in page["records"]:
            key = (row["root_id"], row["relative_path"])
            require(key not in seen, "duplicate partition record")
            seen.add(key)
        previous = page["page_sha256"]
    return {
        "partitions": len(pages),
        "discovered_records": len(seen),
        "discovery_exhausted": pages[-1]["discovery_exhausted"],
        "unresolved_discovery_gaps": sum(len(p["gaps"]) for p in pages),
        "discovery_complete": pages[-1]["discovery_exhausted"]
        and not any(p["gaps"] for p in pages),
        "historical_inventory_complete": False,
        "qualification_credit": 0,
    }


def inventory_partition(config, page):
    validate(page, config)
    c = copy.deepcopy(config)
    metadata = {(r["root_id"], r["relative_path"]): r for r in c.get("records", [])}
    # Explicit pins are inspected once in page zero, not silently lost to exclusions.
    selected = {(r["root_id"], r["relative_path"]) for r in page["records"]}
    if page["index"] == 0:
        selected.update(metadata)
    else:
        selected.difference_update(metadata)
    require(
        len(selected) <= c["max_files"], "partition plus explicit pins exceed bound"
    )
    c["records"] = [
        metadata.get(k, {"root_id": k[0], "relative_path": k[1]})
        for k in sorted(selected)
    ]
    for root in c["roots"]:
        root["excludes"] = ["**"]
    result = {
        "schema": "iicp.heritage-partition-inventory.v1",
        "partition": copy.deepcopy(page),
        "parent_config_sha256": sha(canonical(config)),
        "inventory": heritage.inventory(c),
        "historical_inventory_complete": False,
        "qualification_credit": 0,
    }

    validate_inventory(config, result)
    return result


def validate_inventory(config, value):
    require(
        set(value)
        == {
            "schema",
            "partition",
            "parent_config_sha256",
            "inventory",
            "historical_inventory_complete",
            "qualification_credit",
        },
        "invalid inventory wrapper",
    )
    require(
        value["schema"] == "iicp.heritage-partition-inventory.v1"
        and value["historical_inventory_complete"] is False
        and value["qualification_credit"] == 0,
        "invalid inventory authority",
    )
    validate(value["partition"], config)
    require(
        value["parent_config_sha256"] == sha(canonical(config)), "wrong parent config"
    )
    heritage.check(value["inventory"])
    page = value["partition"]
    expected = {(r["root_id"], r["relative_path"]) for r in page["records"]}
    metadata = {
        (r["root_id"], r["relative_path"]): r for r in config.get("records", [])
    }
    if page["index"] == 0:
        expected.update(metadata)
    else:
        expected.difference_update(metadata)
    require(
        {(r["root_id"], r["relative_path"]) for r in value["inventory"]["objects"]}
        == expected,
        "partition inventory mismatch",
    )
    c = copy.deepcopy(config)
    c["records"] = [
        metadata.get(k, {"root_id": k[0], "relative_path": k[1]})
        for k in sorted(expected)
    ]
    for root in c["roots"]:
        root["excludes"] = ["**"]
    require(
        value["inventory"]["config_sha256"] == sha(canonical(c)),
        "partition config mismatch",
    )


def refusal_code(error):
    """Stable public reason codes; never emit arbitrary source paths/messages."""
    known = {
        "directory history bound": "DIRECTORY_HISTORY_LIMIT",
        "frontier bound": "FRONTIER_LIMIT",
        "previously discovered directory changed": "SOURCE_DIRECTORY_CHANGED",
        "directory changed since checkpoint": "SOURCE_DIRECTORY_CHANGED",
        "directory changed during discovery": "SOURCE_DIRECTORY_CHANGED",
        "changed config": "CONFIG_CHANGED",
        "changed checkpoint": "CHECKPOINT_CHANGED",
    }
    return known.get(
        str(error), "IO_REFUSAL" if isinstance(error, OSError) else "INVALID_INPUT"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["discover", "inventory", "check-chain"])
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--page", type=Path)
    p.add_argument("--pages", type=Path, nargs="+")
    p.add_argument("--steps", type=int, default=1000)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    config = json.loads(a.config.read_text())
    page = json.loads(a.page.read_text()) if a.page else None
    if a.command == "check-chain":
        require(a.pages is not None, "pages required")
        value = validate_chain(config, [json.loads(p.read_text()) for p in a.pages])
    elif a.command == "discover":
        value = discover(config, page, a.steps)
    else:
        require(page is not None, "page required")
        value = inventory_partition(config, page)
    heritage.write_private(a.output, value)
    print(
        "PASS: private bounded partition; no completeness or new qualification credit"
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit("REFUSED: " + refusal_code(error))
