"""Historical synthetic inputs stay pinned when current reporting advances."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import handoff_fixture as fixture


class HistoricalFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name)

    def copied_corpus(self):
        destination = self.parent / 'copied-corpus'
        shutil.copytree(fixture.CORPUS, destination)
        return destination

    def test_frozen_source_and_all_auxiliary_bytes(self):
        bundle, repo = fixture.historical_fixture(self.parent)
        manifest = json.loads((fixture.CORPUS / 'manifest.json').read_bytes())
        self.assertEqual(bundle['status']['source_commit'], manifest['source_commit'])
        expected = {
            'contracts/scope.json': 'contracts/scope.json',
            'reporting-policy.json': 'reporting-policy.json',
            'schemas/report-v1.json': 'schemas/report-v1.json',
            'requirements.txt': 'requirements.txt',
            'scripts/report_common.py': 'validation/report_common.py',
            'scripts/certificate_reporting.py': 'validation/certificate_reporting.py',
        }
        for destination, source in expected.items():
            self.assertEqual((repo / destination).read_bytes(), (fixture.CORPUS / source).read_bytes())
        for name in ('status', 'receipts', 'events'):
            self.assertEqual(bundle[name], json.loads((fixture.CORPUS / 'data' / (name + '.json')).read_bytes()))

    def test_current_report_is_not_read(self):
        original = Path.read_bytes
        live_reports = fixture.ROOT / 'reports'
        def guarded(path):
            if path in [live_reports / (name + '.json') for name in ('status', 'receipts', 'events')]:
                raise AssertionError('historical fixture attempted current report input')
            return original(path)
        with patch.object(Path, 'read_bytes', guarded):
            bundle, _ = fixture.historical_fixture(self.parent)
        self.assertEqual(bundle['status']['source_commit'], 'd9332b9f5a8e88bda28d48643dd4d9be6e1d0859')

    def test_changed_manifest_refused_before_output(self):
        corpus = self.copied_corpus()
        with (corpus / 'manifest.json').open('ab') as stream:
            stream.write(b'\n')
        with patch.object(fixture, 'CORPUS', corpus), self.assertRaisesRegex(ValueError, 'trust anchor'):
            fixture.historical_fixture(self.parent)
        self.assertFalse((self.parent / 'frozen-repository').exists())

    def test_changed_member_refused_before_output(self):
        corpus = self.copied_corpus()
        with (corpus / 'data/status.json').open('ab') as stream:
            stream.write(b'\n')
        with patch.object(fixture, 'CORPUS', corpus), self.assertRaisesRegex(ValueError, 'member differs'):
            fixture.historical_fixture(self.parent)
        self.assertFalse((self.parent / 'frozen-repository').exists())

    def test_symlink_member_refused(self):
        corpus = self.copied_corpus()
        target = corpus / 'data/status.json'
        target.unlink()
        target.symlink_to(fixture.CORPUS / 'data/status.json')
        with patch.object(fixture, 'CORPUS', corpus), self.assertRaisesRegex(ValueError, 'symlink fixture member'):
            fixture.historical_fixture(self.parent)

    def test_existing_destination_not_overwritten(self):
        repo = self.parent / 'frozen-repository'
        repo.mkdir()
        marker = repo / 'marker'
        marker.write_bytes(b'synthetic-existing')
        with self.assertRaises(FileExistsError):
            fixture.historical_fixture(self.parent)
        self.assertEqual(marker.read_bytes(), b'synthetic-existing')
