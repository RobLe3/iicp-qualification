"""Explicit documentation-first v2 packaging; v1 artifacts remain untouched."""

from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
import package_qualification_handoff as v1  # noqa: E402
import qualification_analysis as analysis  # noqa: E402
from report_common import REPO, require, sha  # noqa: E402
from heritage_io import no_symlinks, open_regular  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

EXTRAS = (
    "analysis.json",
    "unresolved-clauses.json",
    "history-gaps.json",
    "dmsc-sources.json",
)
SCHEMA = "schemas/handoff-v2-metadata.json"


def check_extras(bundle, extras):
    require(set(extras) == set(EXTRAS), "exact v2 metadata required")
    a = extras["analysis.json"]
    links = {
        "schema": "iicp.qualification-analysis-links.v1",
        "source_commit": a["source_commit"],
        "requirements": a["requirements"],
        "history": a["history"],
        "dmsc_sources": a["dmsc_sources"],
    }
    metadata_schema = json.loads((REPO / SCHEMA).read_text())
    Draft202012Validator(metadata_schema["$defs"]["reviewed_links"]).validate(links)
    expected = analysis.generate(
        bundle["status"],
        bundle["receipts"],
        bundle["events"],
        json.loads((REPO / "contracts/scope.json").read_text()),
        links,
    )
    require(a == expected, "analysis differs from existing validated source joins")
    require(
        extras["unresolved-clauses.json"]
        == {
            "schema": "iicp.handoff-unresolved-clauses.v1",
            "requirements": a["requirements"],
        },
        "clause copy differs",
    )
    require(
        extras["dmsc-sources.json"]
        == {
            "schema": "iicp.handoff-dmsc-sources.v1",
            "sources": a["dmsc_sources"],
            "records": a["dmsc"],
        },
        "DMSC copy differs",
    )
    Draft202012Validator(json.loads((REPO / SCHEMA).read_text())).validate(
        extras["history-gaps.json"]
    )


V2_CHECK = """    from qualification_analysis import generate
    from jsonschema import Draft202012Validator
    analysis=load('data/analysis.json')
    links={'schema':'iicp.qualification-analysis-links.v1','source_commit':analysis['source_commit'],'requirements':analysis['requirements'],'history':analysis['history'],'dmsc_sources':analysis['dmsc_sources']}
    Draft202012Validator(load('schemas/handoff-v2-metadata.json')['$defs']['reviewed_links']).validate(links)
    check(analysis==generate(status,receipts,events,scope,links),'analysis semantic mismatch')
    check(load('data/unresolved-clauses.json')=={'schema':'iicp.handoff-unresolved-clauses.v1','requirements':analysis['requirements']},'clause copy differs')
    check(load('data/dmsc-sources.json')=={'schema':'iicp.handoff-dmsc-sources.v1','sources':analysis['dmsc_sources'],'records':analysis['dmsc']},'DMSC copy differs')
    Draft202012Validator(load('schemas/handoff-v2-metadata.json')).validate(load('data/history-gaps.json'))
"""


def verifier_source(members):
    source = v1.verifier_source()
    # Derive only from reviewed v1 source. Never mutate the sealed v1 verifier.
    source = source.replace(
        "iicp.qualification-documentation-handoff.v1",
        "iicp.qualification-documentation-handoff.v2",
    )
    # Replace the exact-members expression, leaving all base integrity checks intact.
    line = next(x for x in source.splitlines() if "'required corpus members'" in x)
    replacement = (
        "    members=m['members'];check(isinstance(members,dict) and set(members)==set("
        + repr(sorted(members))
        + "),'required corpus members')"
    )
    source = source.replace(line, replacement)
    bindings = {
        n: sha(members[n])
        for n in (
            "validation/qualification_analysis.py",
            "schemas/qualification-analysis-v1.json",
            SCHEMA,
        )
    }
    insertion = (
        "    for name,trusted in "
        + repr(bindings)
        + ".items():\n        check(members.get(name,{}).get('sha256')==trusted,'unreviewed v2 validation component')\n"
    )
    source = source.replace(
        "    # Import only after", insertion + "    # Import only after"
    )
    source = source.replace(
        "    return {'manifest_sha256'", V2_CHECK + "    return {'manifest_sha256'"
    )
    return source


def build_members(bundle, records, narratives, extras):
    check_extras(bundle, extras)
    members = v1.build_members(bundle, records, narratives)
    for n in EXTRAS:
        members["data/" + n] = v1.encoded(extras[n])
    for source, target in [
        ("scripts/qualification_analysis.py", "validation/qualification_analysis.py"),
        (
            "schemas/qualification-analysis-v1.json",
            "schemas/qualification-analysis-v1.json",
        ),
        (SCHEMA, SCHEMA),
    ]:
        members[target] = (REPO / source).read_bytes()
    members.pop("manifest.json")
    members["verify.py"] = verifier_source(members).encode()
    manifest = json.loads(
        v1.build_members(bundle, records, narratives)["manifest.json"]
    )
    manifest["schema"] = "iicp.qualification-documentation-handoff.v2"
    manifest["members"] = {
        n: {"sha256": sha(data), "bytes": len(data)}
        for n, data in sorted(members.items())
    }
    require(
        all(len(data) <= 8 * 1024 * 1024 for data in members.values()),
        "oversize member",
    )
    members["manifest.json"] = v1.encoded(manifest)
    return members


def prepare(output, inputs):
    require(
        no_symlinks(output)
        and output.absolute() == REPO / "reports/documentation-handoff/v2",
        "unreviewed v2 destination",
    )
    require(
        {p.name for p in output.iterdir()} == set(v1.NARRATIVES),
        "initial v2 narratives only",
    )
    baseline = REPO / "reports/qualification-heritage"
    v1.verify_corpus(
        baseline,
        "sha256:5f790e2ae92594baa2ffa0de8c7d7a7f37ecfbb97d35188105a81eca4cb766b3",
    )
    bundle = {
        n: json.loads((baseline / "data" / f"{n}.json").read_text())
        for n in ("status", "receipts", "events")
    }
    records = json.loads((baseline / "SOURCE_INDEX.json").read_text())["records"]
    extras = {n: json.loads((inputs / n).read_text()) for n in EXTRAS}
    members = build_members(
        bundle, records, {n: (output / n).read_bytes() for n in v1.NARRATIVES}, extras
    )
    for n, data in sorted(members.items(), key=lambda x: x[0] == "manifest.json"):
        if n in v1.NARRATIVES:
            require((output / n).read_bytes() == data, "narrative changed")
        else:
            v1.write_exclusive(output / n, data)
    return verify(output, sha(members["manifest.json"]))


def verify(corpus, expected):
    require(no_symlinks(corpus), "unsafe corpus")
    require(expected is not None, "v2 external reviewed manifest digest required")
    # Authenticate supplied verifier bytes through manifest before executing it.
    with os.fdopen(open_regular(corpus / "manifest.json"), "rb") as stream:
        manifest = stream.read(131073)
    require(len(manifest) <= 131072, "manifest bound")
    require(sha(manifest) == expected, "manifest trust anchor mismatch")
    m = json.loads(manifest)
    with os.fdopen(open_regular(corpus / "verify.py"), "rb") as stream:
        code = stream.read(131073)
    require(len(code) <= 131072, "verifier bound")
    require(sha(code) == m["members"]["verify.py"]["sha256"], "verifier changed")
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-c",
            code.decode(),
            "--root",
            str(corpus),
            "--expected-manifest-sha256",
            expected,
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    require(result.returncode == 0, "v2 portable verification refused")
    return json.loads(result.stdout)


def snapshot(corpus, destination, expected):
    result = verify(corpus, expected)
    require(no_symlinks(destination), "unsafe snapshot parent")
    require(
        destination.absolute()
        == Path("/Users/roble/development/iicp.qualification/documentation-handoff"),
        "unreviewed snapshot destination",
    )
    destination.mkdir(mode=0o700, exist_ok=True)
    require(
        destination.stat().st_uid == os.getuid()
        and destination.stat().st_mode & 0o077 == 0,
        "private snapshot parent required",
    )
    target = destination / result["manifest_sha256"].removeprefix("sha256:")
    target.mkdir(mode=0o700)
    for path in sorted(corpus.rglob("*")):
        if path.is_file():
            with os.fdopen(open_regular(path), "rb") as stream:
                data = stream.read(8 * 1024 * 1024 + 1)
            require(len(data) <= 8 * 1024 * 1024, "snapshot member bound")
            v1.write_exclusive(target / path.relative_to(corpus), data, 0o444)
    verify(target, expected)
    for path in sorted(target.rglob("*"), reverse=True):
        if path.is_dir():
            path.chmod(0o555)
    target.chmod(0o555)
    return {
        "manifest_sha256": expected,
        "snapshot": str(target),
        "byte_identity_verified": True,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--mode", required=True, choices=["prepare-v2", "verify-v2", "snapshot-v2"]
    )
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--inputs", type=Path)
    p.add_argument("--destination-root", type=Path)
    p.add_argument("--expected-manifest-sha256")
    a = p.parse_args()
    if a.mode == "prepare-v2":
        require(a.inputs is not None, "inputs required")
        result = prepare(a.output, a.inputs)
    elif a.mode == "snapshot-v2":
        require(a.destination_root is not None, "destination required")
        result = snapshot(a.output, a.destination_root, a.expected_manifest_sha256)
    else:
        result = verify(a.output, a.expected_manifest_sha256)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
