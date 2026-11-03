"""Read-only mapping of canonically admitted project-operated certificates."""
from __future__ import annotations

import importlib
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from report_common import require

DIRECTORY = "reports/pre1-qualification/certificates"
TARGETS = {"linux-aarch64", "linux-x86_64", "macos-arm64", "windows-x86_64"}
PATHS = {f"{DIRECTORY}/{name}.json" for name in TARGETS | {"ecosystem"}}
PATTERN = r'"schema"[[:space:]]*:[[:space:]]*"iicp\.pre1-(target|ecosystem)(-qualification)?-certificate\.'


def discover(root: Path, commit: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "grep", "-l", "-E", PATTERN, commit, "--",
         "reports/*.json", "reports/**/*.json", "project/*.json", "project/**/*.json"],
        capture_output=True, text=True, check=False,
    )
    require(result.returncode in {0, 1}, "certificate source discovery failed")
    files = [line.removeprefix(commit + ":") for line in result.stdout.splitlines()]
    inventory = set(subprocess.check_output(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", commit, "--", DIRECTORY], text=True
    ).splitlines())
    require(not inventory or inventory == PATHS, "partial or unexpected canonical certificate inventory")
    require(set(files) == inventory, "unrecognized, altered or noncanonical certificate schema")
    dirty = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all", "--", DIRECTORY], text=True
    )
    require(not dirty, "certificate evidence is not committed")
    if files:
        merged = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", commit,
                                 "refs/remotes/origin/main"], capture_output=True, check=False)
        require(merged.returncode == 0, "certificate source is not on known merged main")
    return sorted(files)


def compilers(root: Path) -> tuple:
    modules = tuple(importlib.import_module(name) for name in (
        "compile_pre1_target_certificate", "compile_pre1_ecosystem_certificate"))
    for module in modules:
        require(Path(module.__file__).resolve().parent == (root / "scripts").resolve(),
                "certificate validator belongs to a different source checkout")
    return modules


def validate_payloads(values: dict[str, dict], data: dict, receipts: list[dict],
                      ledger: dict, ledger_digest: str, target, ecosystem, schema: dict) -> None:
    require(set(values) == TARGETS | {"ecosystem"}, "incomplete certificate evidence")
    targets = [values[name] for name in sorted(TARGETS)]
    ecosystem._validate_targets(targets)
    bindings = ecosystem._shared_bindings(targets)
    expected = {"candidate_manifest_sha256": data["candidate"]["manifest_sha256"],
                "executor_registry_sha256": data["registry"]["binding_sha256"],
                "shard_plan_sha256": data["plan"]["plan_sha256"],
                "sentinel_ledger_sha256": ledger_digest}
    require(bindings == expected, "certificate authority differs from admitted evidence")
    ecosystem._validate_plan_bindings(bindings, data["plan"])
    ecosystem._validate_plan_coverage(targets, data["plan"])
    sentinels = {row["target"]: row["receipt_sha256"] for row in ledger["sentinels"]}
    for name in sorted(TARGETS):
        certificate = values[name]
        require(certificate["target"] == name, "certificate file target differs")
        admitted = [row for row in receipts if row["target"] == name]
        require(sorted(certificate["receipt_sha256s"]) == sorted(row["receipt_file_sha256"] for row in admitted),
                "certificate does not bind exactly admitted campaign receipts")
        admission = certificate.get("admission_sentinel_sha256")
        if admission is None:
            admission = next((row["receipt_file_sha256"] for row in admitted if row["shard_index"] == 0), None)
        require(admission == sentinels[name], "certificate admission sentinel differs")
    value = values["ecosystem"]
    require(not list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value)),
            "ecosystem certificate schema failed")
    require(value["certificate_sha256"] == ecosystem.digest(value), "ecosystem certificate digest differs")
    require(all(value[key] == item for key, item in bindings.items()), "ecosystem authority differs")
    require(value["targets"] == ecosystem._target_rows(targets), "ecosystem target certificate links differ")
    for field in ("shards_passed", "support_cells", "edge_executions"):
        require(value[field] == sum(item[field] for item in targets), "ecosystem certificate totals differ")


def derivative(name: str, value: dict, file_digest: str, sentinels: dict) -> dict:
    return {"target": name, "certificate_file_sha256": file_digest,
            "certificate_sha256": value["certificate_sha256"],
            "candidate_manifest_sha256": value["candidate_manifest_sha256"],
            "executor_registry_sha256": value["executor_registry_sha256"],
            "shard_plan_sha256": value["shard_plan_sha256"],
            "receipt_file_sha256s": sorted(value.get("receipt_sha256s", [])),
            "admission_sentinel_file_sha256": sentinels.get(name),
            "target_certificate_sha256s": sorted(row["certificate_sha256"] for row in value.get("targets", [])),
            "classification": "project-operated-qualification",
            "admission_status": "accepted-in-merged-canonical-evidence"}


def collect_certificates(root: Path, commit: str, inputs: dict, bound_file, data: dict,
                         receipts: list[dict], ledger: dict, ledger_digest: str) -> list[dict]:
    paths = discover(root, commit)
    if not paths:
        return []
    target, ecosystem = compilers(root)
    values = {Path(path).stem: bound_file(root, path, commit, inputs) for path in paths}
    # Bind schemas as well as the Python validator closure already captured by the collector.
    schema = bound_file(root, "project/schemas/pre1-ecosystem-qualification-certificate-v1.schema.json", commit, inputs)
    for version in sorted({row["schema"].rsplit(".", 1)[-1] for name, row in values.items() if name != "ecosystem"}):
        require(version in {"v1", "v2"}, "unsupported certificate schema version")
        bound_file(root, f"project/schemas/pre1-target-qualification-certificate-{version}.schema.json", commit, inputs)
    validate_payloads(values, data, receipts, ledger, ledger_digest, target, ecosystem, schema)
    sentinels = {row["target"]: row["receipt_sha256"] for row in ledger["sentinels"]}
    return [derivative(name, values[name], inputs[f"{DIRECTORY}/{name}.json"], sentinels)
            for name in sorted(values)]


def validate_derivatives(status: dict, receipts: list[dict]) -> None:
    rows = status.get("certificates", [])
    require(status["accepted"]["certificates"] == len(rows), "certificate count differs from admission mapping")
    if not rows:
        return
    require(len(rows) == 5 and {row["target"] for row in rows} == TARGETS | {"ecosystem"},
            "certificate admission mapping is partial or duplicated")
    require(len({row["certificate_sha256"] for row in rows}) == 5, "certificate digest is duplicated")
    for field in ("shards", "support_cells", "edge_executions", "sentinels"):
        require(status["accepted"][field] == status["required"][field],
                "certificates require complete campaign and sentinels")
    targets = {row["target"]: row for row in rows}
    sentinels = {row["target"]: row["receipt_file_sha256"] for row in status["sentinels"]}
    for name, row in targets.items():
        for field in ("candidate_manifest_sha256", "executor_registry_sha256", "shard_plan_sha256"):
            require(row[field] == status["authority"][field], "certificate derivative authority differs")
        if name == "ecosystem":
            require(row["receipt_file_sha256s"] == [] and row["admission_sentinel_file_sha256"] is None,
                    "ecosystem derivative contains target evidence")
            require(row["target_certificate_sha256s"] == sorted(targets[t]["certificate_sha256"] for t in TARGETS),
                    "ecosystem derivative links differ")
        else:
            expected = sorted(r["receipt_file_sha256"] for r in receipts if r["target"] == name)
            require(row["receipt_file_sha256s"] == expected and len(expected) == 16,
                    "certificate derivative receipt scope differs")
            require(row["admission_sentinel_file_sha256"] == sentinels[name], "certificate derivative sentinel differs")
            require(row["target_certificate_sha256s"] == [], "target derivative contains ecosystem links")
