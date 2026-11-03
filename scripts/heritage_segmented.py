"""Versioned immutable directory-history segments; v1 pages remain unmodified."""

from __future__ import annotations
import argparse
import copy
import json
import os
import re
from pathlib import Path
from jsonschema import Draft202012Validator
import heritage_partitions as v1
from heritage_io import open_regular, no_symlinks
from report_common import REPO, require, sha, canonical

MAX_SEGMENTS = 256


def seal(value):
    value["page_sha256"] = sha(canonical(value))
    return value


def segment(rows):
    return {
        "schema": "iicp.heritage-history-segment.v1",
        "directories": copy.deepcopy(rows),
    }


def validate(page, config, segments):
    schema = json.loads((REPO / "schemas/heritage-segmented-v2.json").read_text())
    require(
        not list(Draft202012Validator(schema).iter_errors(page)),
        "invalid segmented page",
    )
    require(
        page["page_sha256"]
        == sha(canonical({k: v for k, v in page.items() if k != "page_sha256"})),
        "changed checkpoint",
    )
    require(
        len(page["history_segments"]) <= MAX_SEGMENTS, "history segment count bound"
    )
    require(
        len(set(page["history_segments"])) == len(page["history_segments"]),
        "duplicate history segment",
    )
    require(
        set(segments) == set(page["history_segments"]),
        "missing or foreign history segment",
    )
    plain = to_v1(page)
    v1.validate(plain, config)
    seen = {(d["root_id"], d["relative_path"]) for d in page["directories"]}
    require(len(seen) == len(page["directories"]), "duplicate directory stamp")
    count = len(seen)
    roots = {r["id"] for r in config["roots"]}
    for digest in page["history_segments"]:
        s = segments[digest]
        require(
            set(s) == {"schema", "directories"}
            and s["schema"] == "iicp.heritage-history-segment.v1",
            "invalid segment",
        )
        require(sha(canonical(s)) == digest, "history segment digest mismatch")
        require(
            0 < len(s["directories"]) <= v1.DIRECTORY_LIMIT,
            "history segment size bound",
        )
        # Reuse the exact v1 directory locator/stamp schema, without live I/O.
        probe = copy.deepcopy(plain)
        probe["directories"] = s["directories"]
        probe.pop("page_sha256")
        seal(probe)
        v1.validate(probe, config)
        for d in s["directories"]:
            key = (d["root_id"], d["relative_path"])
            require(
                key not in seen and d["root_id"] in roots, "duplicate history directory"
            )
            seen.add(key)
        count += len(s["directories"])
    require(count == page["history_directory_count"], "history count mismatch")


def to_v1(page):
    plain = {
        k: copy.deepcopy(v)
        for k, v in page.items()
        if k
        not in (
            "history_segments",
            "history_directory_count",
            "origin_v1_sha256",
            "page_sha256",
        )
    }
    plain["schema"] = "iicp.heritage-partition.v1"
    return seal(plain)


def advance(config, previous, segments, steps=1000):
    require(
        type(steps) is int
        and 0 < steps <= min(config["max_files"], v1.DIRECTORY_LIMIT),
        "invalid steps",
    )
    segments = copy.deepcopy(segments)
    if previous["schema"] == "iicp.heritage-partition.v1":
        v1.validate(previous, config)
        require(not segments, "unexpected predecessor segments")
        prior = copy.deepcopy(previous)
        origin = previous["page_sha256"]
        refs = []
    else:
        validate(previous, config, segments)
        prior = to_v1(previous)
        origin = previous["origin_v1_sha256"]
        refs = list(previous["history_segments"])
    # Validate every archived stamp before continuing; segmentation never discards
    # prior source-change checks. Active stamps are checked by the v1 discoverer.
    roots = {r["id"]: r for r in config["roots"]}
    for digest in refs:
        for d in segments[digest]["directories"]:
            path = Path(roots[d["root_id"]]["path"]) / d["relative_path"]
            require(
                no_symlinks(path) and v1.stamp(path) == d["directory_stamp"],
                "previously discovered directory changed",
            )
    if len(prior["directories"]) + steps > v1.DIRECTORY_LIMIT:
        # First validate the active set, then move identical rows to an immutable
        # content-addressed segment. The logical history and parent identity stay.
        for d in prior["directories"]:
            path = Path(roots[d["root_id"]]["path"]) / d["relative_path"]
            require(
                no_symlinks(path) and v1.stamp(path) == d["directory_stamp"],
                "previously discovered directory changed",
            )
        s = segment(prior["directories"])
        digest = sha(canonical(s))
        segments[digest] = s
        refs.append(digest)
        require(len(refs) <= MAX_SEGMENTS, "history segment count bound")
        prior["directories"] = []
        prior.pop("page_sha256")
        seal(prior)
    successor = v1.discover(config, prior, steps)
    successor.pop("page_sha256")
    successor.update(
        schema="iicp.heritage-partition.v2",
        previous_sha256=previous["page_sha256"],
        history_segments=refs,
        history_directory_count=sum(len(segments[d]["directories"]) for d in refs)
        + len(successor["directories"]),
        origin_v1_sha256=origin,
    )
    seal(successor)
    validate(successor, config, segments)
    return successor, segments


def directory_map(page, segments):
    rows = list(page["directories"])
    for digest in page.get("history_segments", []):
        rows.extend(segments[digest]["directories"])
    return {(d["root_id"], d["relative_path"]): d["directory_stamp"] for d in rows}


def validate_chain(config, pages, segments):
    require(bool(pages), "missing partitions")
    previous = None
    seen = set()
    history = {}
    origin = None
    for index, page in enumerate(pages):
        if page["schema"] == "iicp.heritage-partition.v1":
            require(origin is None, "v1 page after v2")
            v1.validate(page, config)
        else:
            if origin is None:
                require(previous is not None, "v2 requires v1 predecessor")
                origin = previous["page_sha256"]
            validate(page, config, {d: segments[d] for d in page["history_segments"]})
            require(page["origin_v1_sha256"] == origin, "changed origin")
        require(
            page["index"] == index
            and page["previous_sha256"]
            == (previous["page_sha256"] if previous else None),
            "broken partition chain",
        )
        current = directory_map(page, segments)
        require(
            all(current.get(k) == v for k, v in history.items()),
            "lost or changed historical stamp",
        )
        history = current
        for row in page["records"]:
            key = (row["root_id"], row["relative_path"])
            require(key not in seen, "duplicate partition record")
            seen.add(key)
        require(
            index == len(pages) - 1 or not page["discovery_exhausted"],
            "page after exhaustion",
        )
        previous = page
    return {
        "partitions": len(pages),
        "discovered_records": len(seen),
        "history_directories": len(history),
        "unresolved_discovery_gaps": sum(len(p["gaps"]) for p in pages),
        "discovery_exhausted": pages[-1]["discovery_exhausted"],
        "historical_inventory_complete": False,
        "qualification_credit": 0,
    }


def inventory_partition(config, page, segments):
    validate(page, config, segments)
    result = v1.inventory_partition(config, to_v1(page))
    wrapped = {
        "schema": "iicp.heritage-segmented-inventory.v2",
        "partition": copy.deepcopy(page),
        "base_inventory": result,
        "history_segment_sha256": list(page["history_segments"]),
        "historical_inventory_complete": False,
        "qualification_credit": 0,
    }

    validate_inventory(config, wrapped, segments)
    return wrapped


def validate_inventory(config, wrapped, segments):
    require(
        set(wrapped)
        == {
            "schema",
            "partition",
            "base_inventory",
            "history_segment_sha256",
            "historical_inventory_complete",
            "qualification_credit",
        },
        "invalid segmented inventory",
    )
    require(
        wrapped["schema"] == "iicp.heritage-segmented-inventory.v2"
        and wrapped["historical_inventory_complete"] is False
        and wrapped["qualification_credit"] == 0,
        "invalid inventory authority",
    )
    validate(wrapped["partition"], config, segments)
    require(
        wrapped["history_segment_sha256"] == wrapped["partition"]["history_segments"],
        "inventory segment mismatch",
    )
    require(
        wrapped["base_inventory"]["partition"] == to_v1(wrapped["partition"]),
        "inventory partition mismatch",
    )
    v1.validate_inventory(config, wrapped["base_inventory"])


def read_json(path):
    with os.fdopen(open_regular(path), "rb") as f:
        raw = f.read(32 * 1024 * 1024 + 1)
    require(len(raw) <= 32 * 1024 * 1024, "input size bound")
    return json.loads(raw)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--previous", required=True, type=Path)
    p.add_argument("--segments", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--steps", type=int, default=1000)
    a = p.parse_args()
    c = read_json(a.config)
    previous = read_json(a.previous)
    refs = previous.get("history_segments", [])
    require(
        isinstance(refs, list) and len(refs) <= MAX_SEGMENTS,
        "invalid segment references",
    )
    require(
        all(
            isinstance(d, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", d) for d in refs
        ),
        "unsafe segment reference",
    )
    require(len(set(refs)) == len(refs), "duplicate history segment")
    segments = {
        d: read_json(a.segments / (d.removeprefix("sha256:") + ".json")) for d in refs
    }
    page, allsegments = advance(c, previous, segments, a.steps)
    for digest, value in allsegments.items():
        if digest not in segments:
            v1.heritage.write_private(
                a.segments / (digest.removeprefix("sha256:") + ".json"), value
            )
    v1.heritage.write_private(a.output, page)
    print("PASS: segmented history preserved; no completeness or qualification credit")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit("REFUSED: " + v1.refusal_code(error))
