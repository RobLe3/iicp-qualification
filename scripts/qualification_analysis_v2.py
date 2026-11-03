"""Deterministic dimension joins; existing qualification accounting stays authoritative."""

from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
from jsonschema import Draft202012Validator
import qualification_analysis as v1
from report_common import REPO, canonical, load, require, sha

INPUTS = REPO / "reports/analysis-v2/inputs"
DIMENSIONS = ("component", "runtime", "target", "directory_flavor", "mode")
MATRIX_HASH = "sha256:627af9b927665e2d33ccd9ff8226abcf281c1b16f8c545f0e61d212a44650db2"
CATALOG_HASH = "sha256:bf11370545d54934673469d2dca34d3358093de1e59bebf32d62ee1c8ea59630"


def read_inputs(directory=INPUTS):
    require(
        sha((directory / "matrix.json").read_bytes()) == MATRIX_HASH,
        "matrix source drift",
    )
    require(
        sha((directory / "catalog.json").read_bytes()) == CATALOG_HASH,
        "catalog source drift",
    )
    return {
        n: load(directory / (n + ".json"))
        for n in (
            "status",
            "receipts",
            "events",
            "scope",
            "links",
            "matrix",
            "catalog",
            "registers",
        )
    }


def generate(status, receipts, events, scope, links, matrix, catalog, registers):
    # Exact canonical object equality also protects callers using in-memory inputs.
    require(matrix == load(INPUTS / "matrix.json"), "foreign matrix applicability")
    require(catalog == load(INPUTS / "catalog.json"), "foreign scenario applicability")
    base = v1.generate(status, receipts, events, scope, links)
    cells = {}
    for component in matrix["components"]:
        for runtime, target, flavor, mode in itertools.product(
            component["runtimes"],
            component["targets"],
            component["directory_flavors"],
            component["modes"],
        ):
            values = (component["id"], runtime, target, flavor, mode)
            key = "|".join(values)
            require(key not in cells, "duplicate matrix cell")
            cells[key] = dict(zip(DIMENSIONS, values))
    require(
        set(cells) == set(scope["support_cells"]),
        "matrix cells differ from authoritative scope",
    )
    scenarios = {s["id"]: s for s in catalog["scenarios"]}
    require(len(scenarios) == len(catalog["scenarios"]), "duplicate scenario")
    expected_edges = {
        s + "::" + c
        for s, row in scenarios.items()
        for c, dimensions in cells.items()
        if dimensions["component"] in row["applicable_components"]
    }
    require(
        expected_edges == set(scope["edge_executions"]),
        "scenario applicability differs from authoritative scope",
    )
    rows = []
    groups = {}
    for source in base["assertions"]:
        if source["kind"] == "edge_executions":
            scenario, cell = source["assertion_id"].split("::", 1)
            category = scenarios[scenario]["category"]
        else:
            scenario = None
            cell = source["assertion_id"]
            category = None
        dims = cells[cell]
        require(
            dims["target"] == source["target"], "receipt target differs from matrix"
        )
        row = {
            **source,
            **dims,
            "cell_id": cell,
            "scenario_id": scenario,
            "scenario_category": category,
            "observed_disposition": "ACCEPTED_PASS",
            "semantic_equivalence": "NOT_ESTABLISHED",
        }
        rows.append(row)
        key = (
            source["kind"],
            scenario or "",
            dims["component"],
            dims["runtime"],
            dims["directory_flavor"],
            dims["mode"],
        )
        groups.setdefault(key, []).append(row)
    comparisons = []
    all_targets = sorted(matrix["declared_targets"])
    for key, members in sorted(groups.items()):
        component = next(c for c in matrix["components"] if c["id"] == key[2])
        targets = sorted(component["targets"])
        require(
            sorted(r["target"] for r in members) == targets,
            "missing/duplicate applicable target",
        )
        comparisons.append(
            {
                "group_id": sha(canonical(list(key))),
                "kind": key[0],
                "scenario_id": key[1] or None,
                "component": key[2],
                "runtime": key[3],
                "directory_flavor": key[4],
                "mode": key[5],
                "applicable_targets": targets,
                "denominator": len(targets),
                "accepted_rows": len(members),
                "excluded_targets": [
                    {
                        "target": t,
                        "reason": "NOT_DECLARED_FOR_COMPONENT_IN_PINNED_MATRIX",
                    }
                    for t in all_targets
                    if t not in targets
                ],
                "assertion_ids": sorted(r["assertion_id"] for r in members),
                "comparison_scope": "ACCEPTED_DISPOSITION_ONLY",
                "raw_output_equivalence": "NOT_ESTABLISHED",
            }
        )
    chronology = []
    for event in sorted(
        events["events"], key=lambda x: (x["occurred_at"], x["event_id"])
    ):
        chronology.append(
            {
                "id": event["event_id"],
                "record_type": "REPORTED_EVENT",
                "reported_event_at": event["occurred_at"],
                "execution_at": None,
                "kind": event["kind"],
                "outcome": event["outcome"],
                "source_sha256": event["source_sha256"],
                "qualification_credit": 0,
                "causal_status": "UNKNOWN",
                "causal_parent_ids": [],
            }
        )
    require(
        registers == load(INPUTS / "registers.json"), "unreviewed register reference"
    )
    for record in registers:
        path = REPO / record["path"]
        require(
            path.is_relative_to(REPO) and not path.is_symlink(), "unsafe register path"
        )
        require(sha(path.read_bytes()) == record["sha256"], "register source drift")
        chronology.append(
            {
                "id": record["id"],
                "record_type": "REVIEWED_REGISTER",
                "reported_event_at": None,
                "execution_at": None,
                "kind": None,
                "outcome": None,
                "source_sha256": record["sha256"],
                "qualification_credit": 0,
                "causal_status": "UNKNOWN",
                "causal_parent_ids": [],
            }
        )
    value = {
        "schema": "iicp.qualification-analysis.v2",
        "non_authorizing": True,
        "qualification_credit_added": 0,
        "historical_inventory_complete": False,
        "source_commit": status["source_commit"],
        "candidate_manifest_sha256": status["authority"]["candidate_manifest_sha256"],
        "inputs": {
            k: sha(canonical(v))
            for k, v in [
                ("status", status),
                ("receipts", receipts),
                ("events", events),
                ("scope", scope),
                ("links", links),
                ("matrix", matrix),
                ("catalog", catalog),
                ("registers", registers),
            ]
        },
        "assertions": rows,
        "comparisons": comparisons,
        "chronology": chronology,
        "counts": {
            "support_cells": len(cells),
            "edge_executions": len(expected_edges),
            "assertions": len(rows),
            "comparison_groups": len(comparisons),
            "reported_events": len(events["events"]),
            "register_anchors": len(registers),
        },
        "limitations": [
            "PINNED_DERIVATIVE_NOT_AUTHORITY",
            "ACCEPTED_DISPOSITION_NOT_SEMANTIC_EQUIVALENCE",
            "EVENT_TIME_NOT_EXECUTION_TIME",
            "CAUSALITY_UNKNOWN",
            "HISTORY_INCOMPLETE",
            "NO_EXTERNAL_CERTIFICATION_OR_PERFORMANCE_CLAIM",
        ],
    }
    validate(value)
    return value


def validate(value):
    Draft202012Validator(
        load(REPO / "schemas/qualification-analysis-v2.json")
    ).validate(value)
    require(
        len({r["assertion_id"] for r in value["assertions"]})
        == len(value["assertions"]),
        "duplicate analysis assertion",
    )
    for row in value["assertions"]:
        require(
            row["candidate_manifest_sha256"] == value["candidate_manifest_sha256"],
            "mixed candidate",
        )
    require(value["counts"]["assertions"] == len(value["assertions"]), "count mismatch")


def check_exact(value):
    validate(value)
    require(
        value == generate(**read_inputs()), "analysis differs from pinned source joins"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(
        not any(p.is_symlink() for p in (args.output, *args.output.parents)),
        "unsafe output path",
    )
    output = args.output.resolve()
    require(
        not output.is_relative_to(REPO.resolve())
        or output == (REPO / "reports/analysis-v2/analysis.json").resolve(),
        "output outside permitted derivative path",
    )
    value = generate(**read_inputs())
    with args.output.open("x") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print("PASS non-authorizing pinned analysis v2")


if __name__ == "__main__":
    main()
