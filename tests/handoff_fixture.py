"""Pinned public historical inputs for synthetic handoff-builder tests only."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'reports/qualification-heritage'
# Reviewed committed V1 corpus, not a digest recalculated from arbitrary input.
MANIFEST_SHA256 = '5f790e2ae92594baa2ffa0de8c7d7a7f37ecfbb97d35188105a81eca4cb766b3'


def historical_fixture(parent):
    manifest_path = CORPUS / 'manifest.json'
    if manifest_path.is_symlink():
        raise ValueError('symlink fixture manifest')
    raw = manifest_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError('historical fixture trust anchor differs')
    manifest = json.loads(raw)
    members = {}
    for name, binding in manifest['members'].items():
        path = CORPUS / name
        if path.is_symlink():
            raise ValueError('symlink fixture member')
        data = path.read_bytes()
        if len(data) != binding['bytes'] or 'sha256:' + hashlib.sha256(data).hexdigest() != binding['sha256']:
            raise ValueError('historical fixture member differs')
        members[name] = data
    bundle = {name: json.loads(members['data/' + name + '.json']) for name in ('status', 'receipts', 'events')}
    if bundle['status']['source_commit'] != manifest['source_commit']:
        raise ValueError('historical fixture source differs')
    repo = Path(parent) / 'frozen-repository'
    repo.mkdir()
    paths = {name: name for name in ('contracts/scope.json', 'reporting-policy.json', 'schemas/report-v1.json', 'requirements.txt')}
    paths.update({'scripts/' + name: 'validation/' + name for name in ('report_common.py', 'certificate_reporting.py')})
    for destination, source in paths.items():
        target = repo / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(members[source])
    return bundle, repo
