"""Non-authorizing joins over already validated public qualification derivatives."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from jsonschema import Draft202012Validator

from report_common import REPO, canonical, check_bundle, load, require, sha


def validate(value: dict, kind: str) -> None:
    schema = load(REPO / "schemas/qualification-analysis-v1.json")
    Draft202012Validator(
        {"$ref": "#/$defs/" + kind, "$defs": schema["$defs"]}
    ).validate(value)


def generate(
    status: dict, receipts: dict, events: dict, scope: dict, links: dict
) -> dict:
    """Cross-reference only; existing report validators retain accounting authority."""
    check_bundle(status, receipts, events)
    require(scope == load(REPO / "contracts/scope.json"), "foreign scope")
    validate(links, "links")
    require(links["source_commit"] == status["source_commit"], "mixed source revision")
    known = {r["receipt_id"]: r for r in receipts["receipts"]}
    require(len(known) == len(receipts["receipts"]), "duplicate receipt identifier")
    for name in ("requirements", "history"):
        ids = [row["id"] for row in links[name]]
        require(len(set(ids)) == len(ids), "duplicate link identifier")
        for row in links[name]:
            require(
                set(row["receipt_ids"]) <= known.keys(), "unresolved receipt reference"
            )
    assertions = []
    for category in ("support_cells", "edge_executions"):
        index = {}
        for receipt in receipts["receipts"]:
            for assertion in receipt[category]:
                require(assertion not in index, "duplicate assertion")
                index[assertion] = receipt
        require(set(index) == set(scope[category]), "incomplete assertion scope")
        for assertion in sorted(index):
            receipt = index[assertion]
            assertions.append(
                {
                    "kind": category,
                    "assertion_id": assertion,
                    "receipt_id": receipt["receipt_id"],
                    "receipt_file_sha256": receipt["receipt_file_sha256"],
                    "candidate_manifest_sha256": receipt["candidate_manifest_sha256"],
                    "environment_sha256": receipt["environment_sha256"],
                    "target": receipt["target"],
                    "contract_mapping_status": "UNRESOLVED",
                }
            )
    value = {
        "schema": "iicp.qualification-analysis.v1",
        "non_authorizing": True,
        "qualification_credit_added": 0,
        "historical_inventory_complete": False,
        "source_commit": status["source_commit"],
        "inputs": {
            key: sha(canonical(value))
            for key, value in [
                ("status", status),
                ("receipts", receipts),
                ("events", events),
                ("scope", scope),
                ("links", links),
            ]
        },
        "assertions": assertions,
        "requirements": links["requirements"],
        "history": links["history"],
        "dmsc_sources": links["dmsc_sources"],
        "dmsc": [
            {"id": name, "assessment": "UNASSESSED", "assertion_ids": []}
            for name in [
                *[f"D{i:02}" for i in range(1, 15)],
                *[f"V{i:02}" for i in range(1, 14)],
            ]
        ],
        "limitations": [
            "DERIVATIVE_NOT_AUTHORITY",
            "REQUIREMENT_LINKS_UNRESOLVED",
            "HISTORY_PARTIAL",
            "NO_INTEROPERABILITY_CLAIM",
        ],
    }
    validate(value, "analysis")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--links", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    require(
        not output.is_relative_to(REPO.resolve()),
        "analysis output must be private/external",
    )
    data = {
        name: load(args.data / (name + ".json"))
        for name in ("status", "receipts", "events", "scope")
    }
    result = generate(**data, links=load(args.links))
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print("PASS: non-authorizing analysis generated")


if __name__ == "__main__":
    main()
