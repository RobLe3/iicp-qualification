"""Independent zero-credit contract tests; fixtures never touch original ledgers."""
import copy
import hashlib
import json
import pathlib
import sys
import tempfile
import tarfile
import io
import subprocess
import unittest
import zipfile
from unittest.mock import patch
from jsonschema import Draft202012Validator, ValidationError

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import qualification_heritage as heritage


def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


class HeritageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name).resolve()
        self.payload = b'{"synthetic":"accepted-receipt"}\n'
        (self.root / 'receipt.json').write_bytes(self.payload)
        self.canonical = {
            'source_commit': 'a' * 40, 'status_sha256': 'sha256:' + 'b' * 64,
            'receipt_count': 1,
            'receipts': [{'receipt_file_sha256': digest(self.payload),
                          'target': 'windows-x86_64', 'shard_index': 1,
                          'evidence_ids': []}]}
        self.config = {
            'schema': 'iicp.heritage-config.v1',
            'roots': [{'id': 'fixture', 'path': str(self.root),
                       'kind': 'qualification', 'excludes': []}],
            'max_files': 20, 'max_file_bytes': 65536,
            'max_archive_members': 10, 'max_archive_uncompressed_bytes': 65536,
            'canonical_context': {'root': str(self.root), 'source_commit': 'a' * 40,
                                  'sentinel': str(self.root / 'sentinel.json'),
                                  'archive_root': str(self.root), 'inbox': str(self.root / 'inbox.json'),
                                  'verified_at': '2026-11-03T12:00:00Z'},
            'records': [{'root_id': 'fixture', 'relative_path': 'receipt.json',
                         'expected_sha256': digest(self.payload),
                         'occurred_at': '2026-11-01T12:00:00Z', 'supersedes': [],
                         'original_outcome': 'PASS'}]}

    def inventory(self, config=None):
        with patch.object(heritage, 'load_canonical', return_value=copy.deepcopy(self.canonical)):
            return heritage.inventory(copy.deepcopy(config or self.config))

    def test_positive_source_bound_receipt(self):
        value = self.inventory()
        heritage.check(value)
        self.assertEqual(value['qualification_credit'], 0)
        self.assertFalse(value['historical_inventory_complete'])
        self.assertEqual(len(value['canonical']['receipts'][0]['evidence_ids']), 1)
        row = value['objects'][0]
        self.assertEqual(row['integrity'], 'MATCH')
        self.assertEqual(row['admission_status'], 'ACCEPTED_REFERENCE')

    def test_altered_expected_receipt_cannot_join(self):
        (self.root / 'receipt.json').write_text('{"altered":true}')
        value = self.inventory()
        self.assertEqual(value['objects'][0]['integrity'], 'MISMATCH')
        self.assertEqual(value['objects'][0]['admission_status'], 'NOT_ESTABLISHED')
        self.assertEqual(value['canonical']['receipts'][0]['evidence_ids'], [])
        self.assertTrue(value['gaps'])

    def test_missing_original_is_reported_not_passed(self):
        (self.root / 'receipt.json').unlink()
        value = self.inventory()
        self.assertTrue(any(r['availability'] == 'MISSING' for r in value['objects']))
        self.assertTrue(value['gaps'])
        self.assertFalse(value['historical_inventory_complete'])

    def test_duplicate_identity_rejected(self):
        value = self.inventory(); value['objects'].append(copy.deepcopy(value['objects'][0]))
        with self.assertRaises(ValueError): heritage.check(value)

    def test_duplicate_canonical_assignment_rejected(self):
        value = self.inventory(); value['canonical']['receipts'].append(copy.deepcopy(value['canonical']['receipts'][0]))
        with self.assertRaises(ValueError): heritage.check(value)

    def test_supersession_self_cycle_rejected(self):
        value = self.inventory(); value['objects'][0]['supersedes'] = [value['objects'][0]['evidence_id']]
        with self.assertRaises(ValueError): heritage.check(value)

    def test_summary_denominator_corruption_rejected(self):
        value = self.inventory(); value['summary']['objects'] += 1
        with self.assertRaises(ValueError): heritage.check(value)

    def test_diagnostic_has_no_inferred_credit(self):
        (self.root / 'diagnostic.json').write_text('{"status":"PASS","qualification_credit":99}')
        value = self.inventory()
        self.assertEqual(value['qualification_credit'], 0)
        self.assertEqual(value['canonical']['receipt_count'], 1)
        diagnostic = next(r for r in value['objects'] if r['relative_path'] == 'diagnostic.json')
        self.assertEqual(diagnostic['admission_status'], 'NOT_ESTABLISHED')

    def test_test_source_is_not_runtime_interoperability(self):
        (self.root / 'test.py').write_text('assert True\n')
        value = self.inventory()
        self.assertEqual(value['dmsc']['claim_status'], 'UNASSESSED')
        self.assertEqual(next(r for r in value['objects'] if r['relative_path'] == 'test.py')['admission_status'], 'NOT_ESTABLISHED')

    def test_test_source_cannot_gain_runtime_maturity_field(self):
        value = self.inventory(); value['objects'][0]['runtime_verified'] = True
        with self.assertRaises(ValueError): heritage.check(value)

    def test_dmsc_claim_cannot_be_promoted(self):
        value = self.inventory(); value['dmsc']['claim_status'] = 'INTEROPERABILITY_PROVEN'
        with self.assertRaises(ValueError): heritage.check(value)

    def test_external_certification_inflation_rejected(self):
        value = self.inventory(); value['independent_external_certification'] = True
        with self.assertRaises(ValueError): heritage.check(value)

    def test_performance_inflation_rejected(self):
        value = self.inventory(); value['performance_qualified'] = True
        with self.assertRaises(ValueError): heritage.check(value)

    def test_unknown_dmsc_id_rejected(self):
        value = self.inventory(); value['dmsc']['architecture'].append('D99')
        with self.assertRaises(ValueError): heritage.check(value)

    def test_unknown_reviewer_id_rejected(self):
        value = self.inventory(); value['dmsc']['reviewer'].append('F01')
        with self.assertRaises(ValueError): heritage.check(value)

    def test_public_projection_drops_paths_and_payload(self):
        (self.root / 'private-marker.txt').write_text('SYNTHETIC-PRIVATE-MARKER')
        value = heritage.project(self.inventory()); encoded = json.dumps(value)
        for forbidden in [str(self.root), 'private-marker.txt', 'SYNTHETIC-PRIVATE-MARKER', 'relative_path', 'root_id']:
            self.assertNotIn(forbidden, encoded)
        self.assertFalse(value['historical_inventory_complete'])
        self.assertEqual(value['qualification_credit'], 0)

    def test_config_parent_traversal_rejected(self):
        config = copy.deepcopy(self.config); config['records'][0]['relative_path'] = '../outside.json'
        with self.assertRaises(ValueError): self.inventory(config)

    def test_symlink_target_never_retained(self):
        outside = self.root / 'outside'; outside.mkdir()
        (outside / 'marker').write_text('SYNTHETIC-NOT-READ')
        (self.root / 'link').symlink_to(outside / 'marker')
        value = self.inventory()
        row = next(r for r in value['objects'] if r['relative_path'] == 'link')
        self.assertEqual(row['availability'], 'UNSAFE')
        self.assertIsNone(row['sha256'])

    def test_archive_traversal_rejected_without_extracting(self):
        with zipfile.ZipFile(self.root / 'bad.zip', 'w') as z: z.writestr('../escape', b'marker')
        value = self.inventory(); row = next(r for r in value['objects'] if r['relative_path'] == 'bad.zip')
        self.assertEqual(row['archive_status'], 'UNSAFE')
        self.assertFalse((self.root.parent / 'escape').exists())

    def test_archive_uncompressed_bound(self):
        with zipfile.ZipFile(self.root / 'large.zip', 'w', compression=zipfile.ZIP_DEFLATED) as z: z.writestr('big', b'x' * 70000)
        value = self.inventory(); row = next(r for r in value['objects'] if r['relative_path'] == 'large.zip')
        self.assertEqual(row['archive_status'], 'OVERSIZE')

    def test_archive_positive_metadata(self):
        with zipfile.ZipFile(self.root / 'safe.zip', 'w') as z: z.writestr('evidence/marker', b'ok')
        value = self.inventory(); row = next(r for r in value['objects'] if r['relative_path'] == 'safe.zip')
        self.assertEqual(row['archive_status'], 'SAFE_METADATA')
        self.assertFalse((self.root / 'evidence').exists())

    def test_deterministic_same_inputs(self):
        self.assertEqual(self.inventory(), self.inventory())

    def test_stale_canonical_identity_rejected(self):
        self.canonical['source_commit'] = 'c' * 40
        with self.assertRaises(ValueError): self.inventory()

    def test_supersession_two_object_cycle_rejected(self):
        (self.root / 'second.json').write_text('{"other":true}')
        value = self.inventory()
        one, two = value['objects']
        one['supersedes'] = [two['evidence_id']]
        two['supersedes'] = [one['evidence_id']]
        with self.assertRaises(ValueError): heritage.check(value)

    def test_oversize_file_unread_and_uncredited(self):
        (self.root / 'big.bin').write_bytes(b'x' * 65537)
        value = self.inventory()
        row = next(r for r in value['objects'] if r['relative_path'] == 'big.bin')
        self.assertEqual(row['availability'], 'OVERSIZE')
        self.assertIsNone(row['sha256'])
        self.assertEqual(row['admission_status'], 'NOT_ESTABLISHED')

    def test_no_qualification_credit_override(self):
        value = self.inventory(); value['qualification_credit'] = 1
        with self.assertRaises(ValueError): heritage.check(value)

    def test_unsafe_archive_cannot_be_admitted(self):
        value = self.inventory(); value['objects'][0]['archive_status'] = 'UNSAFE'
        with self.assertRaises(ValueError): heritage.check(value)

    def test_known_missing_gap_cannot_be_hidden(self):
        (self.root / 'receipt.json').unlink()
        value = self.inventory(); value['gaps'] = []; value['summary']['unresolved'] = 0
        with self.assertRaises(ValueError): heritage.check(value)

    def test_public_target_cannot_contain_private_text(self):
        value = self.inventory(); value['canonical']['receipts'][0]['target'] = 'SYNTHETIC-PRIVATE-MARKER'
        with self.assertRaises(ValueError): heritage.project(value)

    def test_archive_member_bound(self):
        with zipfile.ZipFile(self.root / 'members.zip', 'w') as z:
            for n in range(11): z.writestr(str(n), b'x')
        value = self.inventory()
        self.assertEqual(next(r for r in value['objects'] if r['relative_path'] == 'members.zip')['archive_status'], 'OVERSIZE')

    def test_archive_duplicate_member_rejected(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(self.root / 'duplicate.zip', 'w') as z:
                z.writestr('same', b'a'); z.writestr('same', b'b')
        value = self.inventory()
        self.assertEqual(next(r for r in value['objects'] if r['relative_path'] == 'duplicate.zip')['archive_status'], 'UNSAFE')

    def test_archive_symlink_rejected(self):
        info = zipfile.ZipInfo('link'); info.create_system = 3; info.external_attr = 0o120777 << 16
        with zipfile.ZipFile(self.root / 'link.zip', 'w') as z: z.writestr(info, '../outside')
        value = self.inventory()
        self.assertEqual(next(r for r in value['objects'] if r['relative_path'] == 'link.zip')['archive_status'], 'UNSAFE')

    def test_tar_positive_metadata(self):
        with tarfile.open(self.root / 'safe.tar', 'w') as t:
            info = tarfile.TarInfo('safe'); info.size = 1; t.addfile(info, io.BytesIO(b'x'))
        value = self.inventory()
        self.assertEqual(next(r for r in value['objects'] if r['relative_path'] == 'safe.tar')['archive_status'], 'SAFE_METADATA')

    def test_tar_link_rejected(self):
        with tarfile.open(self.root / 'link.tar', 'w') as t:
            info = tarfile.TarInfo('link'); info.type = tarfile.SYMTYPE; info.linkname = '../outside'; t.addfile(info)
        value = self.inventory()
        self.assertEqual(next(r for r in value['objects'] if r['relative_path'] == 'link.tar')['archive_status'], 'UNSAFE')

    def test_compressed_tar_is_explicitly_uninspected(self):
        with tarfile.open(self.root / 'headers.tar.gz', 'w:gz', format=tarfile.PAX_FORMAT) as t:
            info = tarfile.TarInfo('x' * 70000); info.size = 1; t.addfile(info, io.BytesIO(b'x'))
        value = self.inventory()
        self.assertEqual(next(r for r in value['objects'] if r['relative_path'] == 'headers.tar.gz')['archive_status'], 'UNREADABLE')

    @unittest.skipUnless(hasattr(__import__('os'), 'mkfifo'), 'POSIX FIFO safety')
    def test_fifo_is_rejected_without_blocking(self):
        import os
        fifo = self.root / 'fifo'; os.mkfifo(fifo)
        code = "from pathlib import Path; from heritage_io import streamed_hash; import sys; streamed_hash(Path(sys.argv[1]), 100)"
        env = dict(os.environ, PYTHONPATH=str(ROOT / 'scripts'), PYTHONDONTWRITEBYTECODE='1')
        result = subprocess.run([sys.executable, '-B', '-c', code, str(fifo)], env=env, capture_output=True, timeout=3)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'nonregular', result.stderr)

    def test_diagnostic_class_cannot_join_even_matching_bytes(self):
        config = copy.deepcopy(self.config); config['roots'][0]['kind'] = 'diagnostic'
        value = self.inventory(config)
        self.assertEqual(value['canonical']['receipts'][0]['evidence_ids'], [])
        self.assertEqual(value['objects'][0]['admission_status'], 'NOT_ESTABLISHED')
        self.assertEqual(value['qualification_credit'], 0)
        self.assertTrue(value['gaps'])

    def test_public_projection_schema_positive_and_private_field_negative(self):
        schema = json.loads((ROOT / 'schemas/heritage-v1.json').read_text())
        validator = Draft202012Validator({'$ref': '#/$defs/public', '$defs': schema['$defs']})
        value = heritage.project(self.inventory()); validator.validate(value)
        value['private_path'] = str(self.root)
        with self.assertRaises(ValidationError): validator.validate(value)

    def test_originals_unchanged(self):
        before = (self.root / 'receipt.json').read_bytes(); self.inventory()
        self.assertEqual((self.root / 'receipt.json').read_bytes(), before)


if __name__ == '__main__': unittest.main()
