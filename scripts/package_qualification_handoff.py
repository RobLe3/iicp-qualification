#!/usr/bin/env python3
"""Build and verify a reviewed, non-publishing qualification documentation corpus."""

from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
from report_common import REPO, canonical, check_public, require, sha  # noqa:E402
from heritage_io import no_symlinks  # noqa:E402

SOURCE = "d9332b9f5a8e88bda28d48643dd4d9be6e1d0859"
NARRATIVES = (
    "START_HERE.md",
    "AGENT_BRIEF.md",
    "COVERAGE_AND_GAPS.md",
    "SOURCE_AUTHORITY.md",
    "REVIEWED_FINDINGS.md",
    "COMPONENT_BASELINE.md",
)
EXPECTED_COUNTS = {
    "shards": 64,
    "support_cells": 218,
    "edge_executions": 5590,
    "sentinels": 4,
    "certificates": 5,
}
VERIFIER = r'''#!/usr/bin/env python3
"""Verify public corpus integrity and existing public accounting; never private execution."""
import argparse,hashlib,json,os,re,stat,sys
from pathlib import Path
sys.dont_write_bytecode=True

def check(condition,message):
    if not condition:raise ValueError(message)

def verify(root,expected=None):
    root=Path(root).absolute()
    check(not any(p.is_symlink() for p in (root,*root.parents)), 'symlink corpus')
    fd=os.open(root/'manifest.json',os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        info=os.fstat(stream.fileno())
        check(stat.S_ISREG(info.st_mode) and info.st_size<=131072,'manifest must be bounded regular file')
        manifest_bytes=stream.read(131073)
        check(len(manifest_bytes)<=131072,'manifest size')
    digest='sha256:'+hashlib.sha256(manifest_bytes).hexdigest()
    if expected:check(digest==expected,'manifest trust anchor mismatch')
    m=json.loads(manifest_bytes)
    check(set(m)=={'schema','source_commit','candidate_manifest_sha256','accepted','historical_inventory_complete','independent_external_certification','qualification_credit','members'},'manifest fields')
    check(m['schema']=='iicp.qualification-documentation-handoff.v1','manifest schema')
    check(re.fullmatch('[0-9a-f]{40}',m['source_commit']) is not None,'source identity')
    check(m['historical_inventory_complete'] is False and m['independent_external_certification']=='NOT_ESTABLISHED' and m['qualification_credit']==0,'authority inflation')
    members=m['members'];check(isinstance(members,dict) and set(members)==set(__EXPECTED_MEMBERS__),'required corpus members')
    check(all(isinstance(n,str) and n and not Path(n).is_absolute() and '..' not in Path(n).parts and '\\' not in n and ':' not in n for n in members),'member path')
    found=set()
    for p in root.rglob('*'):
        check(not p.is_symlink(),'symlink member')
        if p.is_file():found.add(p.relative_to(root).as_posix())
        elif p.is_dir():check(any(n.startswith(p.relative_to(root).as_posix()+'/') for n in members),'unbound directory')
        else:raise ValueError('nonregular member')
    check(found==set(members)|{'manifest.json'},'missing or extra member')
    for n,d in members.items():
        check(set(d)=={'sha256','bytes'},'member metadata')
        p=root/n;check(p.stat().st_size==d['bytes'] and d['bytes']<=8*1024*1024,'member size')
        check('sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256'],'member changed')
    for name,trusted in __PINNED_VALIDATION__.items():
        check(members.get(name,{}).get('sha256')==trusted,'unreviewed validation component')
    # Import only after all corpus bytes have passed the supplied external anchor/hash checks.
    sys.path.insert(0,str(root/'validation'))
    from report_common import check_bundle
    def load(n):return json.loads((root/n).read_text())
    status=load('data/status.json');receipts=load('data/receipts.json');events=load('data/events.json')
    check_bundle(status,receipts,events)
    check(m['source_commit']==status['source_commit'] and m['candidate_manifest_sha256']==status['authority']['candidate_manifest_sha256'],'manifest authority differs')
    check(m['accepted']==status['accepted']=={'shards':64,'support_cells':218,'edge_executions':5590,'sentinels':4,'certificates':5},'baseline counts')
    check(load('data/certificates.json')=={'schema':'iicp.qualification-certificate-derivatives.v1','certificates':status['certificates']},'certificate copy differs')
    check((root/'data/scope.json').read_bytes()==(root/'contracts/scope.json').read_bytes(),'scope copy differs')
    check((root/'data/reporting-policy.json').read_bytes()==(root/'reporting-policy.json').read_bytes(),'policy copy differs')
    scope=load('data/scope.json')
    coverage={'schema':'iicp.qualification-documentation-coverage.v1','support_cells':scope['support_cells'],'edge_executions':scope['edge_executions'],'scenario_ids':sorted({x.split('::',1)[0] for x in scope['edge_executions']}),'platforms':status['platforms']}
    check(load('data/coverage.json')==coverage,'coverage derivative differs')
    index=load('SOURCE_INDEX.json')
    check(set(index)=={'schema','source_commit','qualification_authority','records'} and index['schema']=='iicp.qualification-documentation-sources.v1' and index['source_commit']==m['source_commit'] and index['qualification_authority']=='RobLe3/iicp.network','source index contract')
    check(len(index['records'])==len(__EXPECTED_SOURCES__) and {r.get('path') for r in index['records']}==set(__EXPECTED_SOURCES__),'source index completeness')
    for row in index['records']:
        check(set(row)=={'path','sha256','url'},'source record fields')
        check(re.fullmatch(r'(project|reports/pre1-qualification/certificates)/[A-Za-z0-9_.\-/]+\.json',row['path']) is not None and '..' not in Path(row['path']).parts,'source record path')
        check(row['url']=='https://github.com/RobLe3/iicp.network/blob/'+m['source_commit']+'/'+row['path'],'source locator')
        check(re.fullmatch('sha256:[0-9a-f]{64}',row['sha256']) is not None,'source hash')
    return {'manifest_sha256':digest,'trust_anchor_checked':bool(expected),'files':len(members),'private_source_reverification':False,'qualification_credit':0}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd());p.add_argument('--expected-manifest-sha256');a=p.parse_args()
    try:print(json.dumps(verify(a.root,a.expected_manifest_sha256),sort_keys=True))
    except (ValueError,OSError,KeyError,ImportError) as e:print('REFUSED: '+str(e),file=sys.stderr);raise SystemExit(1)
'''


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def safe_prose(data):
    text = data.decode("utf-8")
    forbidden = (
        r"/Users/",
        r"/home/",
        r"arn:aws:",
        r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
        r"\b\d{12}\b",
        r"-----BEGIN .*PRIVATE KEY-----",
    )
    require(
        not any(re.search(pattern, text) for pattern in forbidden),
        "private marker in public corpus",
    )


def build_members(bundle, source_records, narratives, repo=REPO):
    require(set(narratives) == set(NARRATIVES), "six reviewed narratives required")
    status = bundle["status"]
    require(status["source_commit"] == SOURCE, "unexpected canonical source")
    require(status["accepted"] == EXPECTED_COUNTS, "incomplete baseline")
    members = {name: data for name, data in narratives.items()}
    for name in ("status", "receipts", "events"):
        members[f"data/{name}.json"] = encoded(bundle[name])
    for path in (
        "contracts/scope.json",
        "reporting-policy.json",
        "schemas/report-v1.json",
        "requirements.txt",
    ):
        members[path] = (repo / path).read_bytes()
    members["data/scope.json"] = members["contracts/scope.json"]
    members["data/reporting-policy.json"] = members["reporting-policy.json"]
    for name in ("report_common.py", "certificate_reporting.py"):
        members["validation/" + name] = (repo / "scripts" / name).read_bytes()
    members["data/certificates.json"] = encoded(
        {
            "schema": "iicp.qualification-certificate-derivatives.v1",
            "certificates": status["certificates"],
        }
    )
    scope = json.loads(members["contracts/scope.json"])
    members["data/coverage.json"] = encoded(
        {
            "schema": "iicp.qualification-documentation-coverage.v1",
            "support_cells": scope["support_cells"],
            "edge_executions": scope["edge_executions"],
            "scenario_ids": sorted(
                {x.split("::", 1)[0] for x in scope["edge_executions"]}
            ),
            "platforms": status["platforms"],
        }
    )
    members["SOURCE_INDEX.json"] = encoded(
        {
            "schema": "iicp.qualification-documentation-sources.v1",
            "source_commit": SOURCE,
            "qualification_authority": "RobLe3/iicp.network",
            "records": source_records,
        }
    )
    members["verify.py"] = verifier_source(repo).encode()
    for name, data in members.items():
        require(len(data) <= 8 * 1024 * 1024, "oversize corpus member")
        if name.endswith(".md") or name == "SOURCE_INDEX.json":
            safe_prose(data)
    manifest = {
        "schema": "iicp.qualification-documentation-handoff.v1",
        "source_commit": SOURCE,
        "candidate_manifest_sha256": status["authority"]["candidate_manifest_sha256"],
        "accepted": status["accepted"],
        "historical_inventory_complete": False,
        "independent_external_certification": "NOT_ESTABLISHED",
        "qualification_credit": 0,
        "members": {
            name: {"sha256": sha(data), "bytes": len(data)}
            for name, data in sorted(members.items())
        },
    }
    members["manifest.json"] = encoded(manifest)
    return members


def write_exclusive(path, data, mode=0o644):
    require(no_symlinks(path), "unsafe output")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def prepare(context, output):
    from collect_status import collect, INPUTS

    output = output.resolve(strict=True)
    require(
        output == REPO / "reports/qualification-heritage",
        "unreviewed corpus destination",
    )
    require(
        {p.name for p in output.iterdir()} == set(NARRATIVES),
        "unbound or missing initial narratives",
    )
    public = check_public()
    require(context["source_commit"] == SOURCE, "source context differs")
    fresh = collect(
        Path(context["root"]),
        SOURCE,
        Path(context["sentinel"]),
        Path(context["archive_root"]),
        Path(context["inbox"]),
        public["status"]["verified_at"],
    )
    require(
        canonical(public) == canonical(fresh),
        "public reporting snapshot requires refresh",
    )
    records = []
    paths = set(INPUTS.values()) | {
        f"reports/pre1-qualification/certificates/{t}.json"
        for t in [
            "linux-aarch64",
            "linux-x86_64",
            "macos-arm64",
            "windows-x86_64",
            "ecosystem",
        ]
    }
    for path in sorted(paths):
        blob = subprocess.check_output(
            ["git", "-C", context["root"], "show", SOURCE + ":" + path]
        )
        records.append(
            {
                "path": path,
                "sha256": sha(blob),
                "url": f"https://github.com/RobLe3/iicp.network/blob/{SOURCE}/{path}",
            }
        )
    members = build_members(
        public, records, {n: (output / n).read_bytes() for n in NARRATIVES}
    )
    for name, data in sorted(
        members.items(), key=lambda item: item[0] == "manifest.json"
    ):
        if name in NARRATIVES:
            require((output / name).read_bytes() == data, "narrative changed")
        else:
            write_exclusive(output / name, data)
    verify_corpus(output)
    return sha(members["manifest.json"])


def verifier_source(repo=REPO):
    bindings = {
        "validation/report_common.py": sha(
            (repo / "scripts/report_common.py").read_bytes()
        ),
        "validation/certificate_reporting.py": sha(
            (repo / "scripts/certificate_reporting.py").read_bytes()
        ),
        "schemas/report-v1.json": sha((repo / "schemas/report-v1.json").read_bytes()),
        "reporting-policy.json": sha((repo / "reporting-policy.json").read_bytes()),
        "contracts/scope.json": sha((repo / "contracts/scope.json").read_bytes()),
    }
    members = (
        set(NARRATIVES)
        | {
            "data/status.json",
            "data/receipts.json",
            "data/events.json",
            "data/scope.json",
            "data/reporting-policy.json",
            "data/certificates.json",
            "data/coverage.json",
            "SOURCE_INDEX.json",
            "verify.py",
            "requirements.txt",
        }
        | set(bindings)
    )
    from collect_status import INPUTS

    sources = set(INPUTS.values()) | {
        f"reports/pre1-qualification/certificates/{t}.json"
        for t in [
            "linux-aarch64",
            "linux-x86_64",
            "macos-arm64",
            "windows-x86_64",
            "ecosystem",
        ]
    }
    return (
        VERIFIER.replace("__PINNED_VALIDATION__", repr(bindings))
        .replace("__EXPECTED_MEMBERS__", repr(sorted(members)))
        .replace("__EXPECTED_SOURCES__", repr(sorted(sources)))
    )


def verify_corpus(corpus, expected=None):
    require(no_symlinks(corpus), "unsafe corpus")
    argv = [sys.executable, "-B", "-c", verifier_source(), "--root", str(corpus)]
    if expected:
        argv += ["--expected-manifest-sha256", expected]
    result = subprocess.run(
        argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30
    )
    require(result.returncode == 0, "portable verification refused")
    return json.loads(result.stdout)


def snapshot(corpus, destination, context):
    result = verify_corpus(corpus)
    digest = result["manifest_sha256"]
    destination = destination.absolute()
    require(no_symlinks(destination), "unsafe snapshot parent")
    require(
        destination
        == Path("/Users/roble/development/iicp.qualification/documentation-handoff"),
        "unreviewed snapshot destination",
    )
    destination.mkdir(mode=0o700, exist_ok=True)
    require(
        destination.stat().st_uid == os.getuid()
        and destination.stat().st_mode & 0o077 == 0,
        "private snapshot parent required",
    )
    target = destination / digest.removeprefix("sha256:")
    target.mkdir(mode=0o700)
    for path in sorted(corpus.rglob("*")):
        if path.is_file():
            write_exclusive(target / path.relative_to(corpus), path.read_bytes(), 0o444)
    verify_corpus(target, digest)
    for path in sorted(target.rglob("*"), reverse=True):
        if path.is_dir():
            path.chmod(0o555)
    target.chmod(0o555)
    locators = destination / "private-locators"
    locators.mkdir(mode=0o700, exist_ok=True)
    mapping = {
        "schema": "iicp.qualification-handoff-private-locators.v1",
        "manifest_sha256": digest,
        "source_root": context["root"],
        "archive_root": context["archive_root"],
        "sentinel": context["sentinel"],
        "source_commit": SOURCE,
        "public_corpus": str(corpus),
    }
    write_exclusive(
        locators / (digest.removeprefix("sha256:") + ".json"), encoded(mapping), 0o600
    )
    return {
        "manifest_sha256": digest,
        "snapshot": str(target),
        "byte_identity_verified": True,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("prepare")
    a.add_argument("--context", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("verify")
    a.add_argument("--corpus", type=Path, required=True)
    a.add_argument("--expected-manifest-sha256")
    a = sub.add_parser("snapshot")
    a.add_argument("--corpus", type=Path, required=True)
    a.add_argument("--destination-root", type=Path, required=True)
    a.add_argument("--context", type=Path, required=True)
    a = p.parse_args()
    if a.command == "prepare":
        result = prepare(json.loads(a.context.read_text()), a.output)
    elif a.command == "verify":
        result = verify_corpus(a.corpus, a.expected_manifest_sha256)
    else:
        result = snapshot(
            a.corpus, a.destination_root, json.loads(a.context.read_text())
        )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print("REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(1)
