"""Public report contract. This module does not grant qualification credit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

REPO = Path(__file__).resolve().parents[1]
REPORT_FILES = (
    "reports/status.json",
    "reports/receipts.json",
    "reports/events.json",
    "reports/STATUS.md",
)


def canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load(path: Path) -> object:
    if path.is_symlink() or not path.is_file():
        raise ValueError("required regular file is unavailable")
    return json.loads(path.read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(value: dict, kind: str) -> None:
    schema = load(REPO / "schemas/report-v1.json")
    validator = Draft202012Validator(
        {"$ref": f"#/$defs/{kind}", "$defs": schema["$defs"]},
        format_checker=FormatChecker(),
    )
    errors = list(validator.iter_errors(value))
    require(
        not errors, f"invalid {kind} contract (unknown or unsafe fields are forbidden)"
    )
    if kind == "events":
        for event in value["events"]:
            if event["outcome"] in {"REFUSED", "EXPIRED"}:
                require(
                    not event["workload_launched"],
                    "refusal or expiry cannot claim workload launch",
                )
            if event["reason"] == "run-completed":
                require(
                    event["outcome"] == "PASS" and event["workload_launched"],
                    "completion event is contradictory",
                )
            if event["reason"] == "run-failed":
                require(
                    event["outcome"] == "FAIL" and event["workload_launched"],
                    "failure event is contradictory",
                )
            if event["reason"] in {"preflight-refused", "review-format-refusal"}:
                require(event["outcome"] == "REFUSED", "refusal event is contradictory")


def check_bundle(status: dict, receipts: dict, events: dict) -> None:
    for kind, value in (("status", status), ("receipts", receipts), ("events", events)):
        validate(value, kind)
    policy = load(REPO / "reporting-policy.json")
    scope = load(REPO / "contracts/scope.json")
    require(
        sha(canonical(scope)) == policy["scope_sha256"],
        "public scope differs from reviewed policy",
    )
    require(
        status["reporting_policy_sha256"]
        == sha((REPO / "reporting-policy.json").read_bytes()),
        "report policy binding mismatch",
    )
    require(
        status["authority"] == policy["authority"], "qualification authority changed"
    )
    require(
        status["receipts_sha256"] == sha(canonical(receipts)),
        "receipt index digest mismatch",
    )
    require(
        status["events_sha256"] == sha(canonical(events)),
        "activity index digest mismatch",
    )
    seen, support, edges = set(), set(), set()
    for receipt in receipts["receipts"]:
        key = (receipt["target"], receipt["shard_index"])
        require(key not in seen, "duplicate credited shard")
        seen.add(key)
        require(
            receipt["candidate_manifest_sha256"]
            == policy["authority"]["candidate_manifest_sha256"],
            "mixed candidate",
        )
        require(
            receipt["executor_registry_sha256"]
            == policy["authority"]["executor_registry_sha256"],
            "mixed registry",
        )
        for field, observed in (("support_cells", support), ("edge_executions", edges)):
            values = receipt[field]
            require(set(values) <= set(scope[field]), "foreign or unsafe assignment")
            require(
                len(values) == len(set(values)) and not observed.intersection(values),
                "duplicate credited assignment",
            )
            observed.update(values)
    require(len(seen) == status["accepted"]["shards"], "shard total mismatch")
    require(
        len(support) == status["accepted"]["support_cells"], "support total mismatch"
    )
    require(len(edges) == status["accepted"]["edge_executions"], "edge total mismatch")
    require(status["required"] == policy["required"], "required scope changed")
    for field, count in status["accepted"].items():
        require(
            count <= status["required"][field], "accepted count exceeds declared scope"
        )
    require(
        status["accepted"]["sentinels"] == len(status["sentinels"]),
        "sentinel total mismatch",
    )
    require(
        {x["target"] for x in status["sentinels"]} == set(policy["targets"]),
        "sentinel targets mismatch",
    )
    require(
        status["accepted"]["certificates"] == 0,
        "certificate reporting needs reviewed admission mapping",
    )
    require(
        [x["target"] for x in status["platforms"]] == policy["targets"],
        "platform set mismatch",
    )
    for row in status["platforms"]:
        indexes = sorted(index for target, index in seen if target == row["target"])
        require(row["accepted_shards"] == indexes, "platform credit mismatch")
        require(
            row["remaining_shards"] == [x for x in range(16) if x not in indexes],
            "remaining work mismatch",
        )
    event_ids = []
    for event in events["events"]:
        content = {key: val for key, val in event.items() if key != "event_id"}
        require(event["event_id"] == sha(canonical(content)), "event identity mismatch")
        event_ids.append(event["event_id"])
    require(len(event_ids) == len(set(event_ids)), "duplicate activity")


def render(status: dict, events: dict) -> str:
    a, r = status["accepted"], status["required"]
    filled = a["shards"] * 20 // r["shards"]
    lines = [
        "# Qualification status",
        "",
        f"Verified snapshot: **{status['verified_at']}**.",
        "",
        f"`[{'#' * filled}{'-' * (20 - filled)}]` **{a['shards']}/{r['shards']} accepted shards**",
        "",
        f"Support cells: **{a['support_cells']}/{r['support_cells']}** · Edge executions: **{a['edge_executions']}/{r['edge_executions']}**",
        f"Sentinels: **{a['sentinels']}/{r['sentinels']}** · Project-operated certificates: **{a['certificates']}/{r['certificates']}**",
        "",
        "| Target | Accepted shard indexes | Remaining indexes |",
        "|---|---|---|",
    ]
    for row in status["platforms"]:
        accepted = ", ".join(map(str, row["accepted_shards"])) or "None"
        remaining = ", ".join(map(str, row["remaining_shards"])) or "None"
        lines.append(f"| {row['target']} | {accepted} | {remaining} |")
    policy = load(REPO / "reporting-policy.json")
    lines += ["", "## Latest registered activity", ""]
    if events["events"]:
        event = events["events"][-1]
        lines += [
            f"- Recorded outcome: **{event['outcome']}** ({event['kind']}, {event['occurred_at']}).",
            f"- {policy['reasons'][event['reason']]}",
            f"- Actual workload launched in this activity: **{str(event['workload_launched']).lower()}**.",
            f"- Next gate: {policy['next_gates'][event['next_gate']]}",
        ]
    else:
        lines += [
            "No operational activity has been registered; current runtime state is UNKNOWN."
        ]
    lines += [
        "",
        "## Evidence and limits",
        "",
        f"- Source: private `RobLe3/iicp.network`, commit `{status['source_commit']}`.",
        "- [Receipt derivatives](receipts.json) map each credited assignment to its original receipt digest.",
        "- [Activity history](events.json) is a selected, append-only register, not a complete historical inventory.",
        "- Accepted totals come only from merged canonical ledgers. Passing CI, diagnostics and unpromoted runs add no credit.",
        "- Source validators checked retained receipts and ledger accounting; no workload or live resource inspection was run for this report.",
        "- Original private receipts/captures are not reproduced here. Public consistency checks cannot independently verify their contents or the product behavior.",
        "- Sentinel records are listed separately and grant no extra campaign credit. A receipt counts toward a campaign only when explicitly admitted in its canonical ledgers.",
        "- Zero certificates means none were found in the inspected canonical tracked evidence. It is not an exhaustive search of private storage.",
        "- This is an as-of report, not a live monitor or execution authorization. Unknown/unregistered activity and retention completeness remain unresolved.",
        "- Qualification within a finite scope is not independent interoperability, external certification, deployment or release readiness.",
        "",
    ]
    return "\n".join(lines)


def encoded(bundle: dict) -> dict[str, bytes]:
    check_bundle(bundle["status"], bundle["receipts"], bundle["events"])
    result = {
        f"reports/{name}.json": (
            json.dumps(bundle[name], indent=2, sort_keys=True) + "\n"
        ).encode()
        for name in ("status", "receipts", "events")
    }
    result["reports/STATUS.md"] = render(bundle["status"], bundle["events"]).encode()
    return result


def check_public(root: Path = REPO) -> dict:
    bundle = {
        name: load(root / f"reports/{name}.json")
        for name in ("status", "receipts", "events")
    }
    expected = encoded(bundle)
    require(
        all((root / path).read_bytes() == data for path, data in expected.items()),
        "generated report bytes differ",
    )
    return bundle
