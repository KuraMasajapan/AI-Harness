"""Evidence byte preservation and bounded report/snapshot continuation."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import test_codex_environment as fixture
import codex_evidence as s
import codex_operations as o

e, h = fixture.e, fixture.h


class EvidenceTests(unittest.TestCase):
    setUp = fixture.EnvironmentTests.setUp
    run_check = fixture.EnvironmentTests.run_check

    def attempt(self, result):
        return Path(result['attempt']).name

    def test_original_bytes_remain_readable_after_worktree_changes(self):
        before=(self.root/'policy.md').read_bytes();result=self.run_check()
        (self.root/'policy.md').write_bytes(b'changed after verification')
        page=s.read_file(self.root,'pilot',self.attempt(result),'policy.md')
        self.assertEqual(page['text'],before.decode())
        with self.assertRaisesRegex(h.HarnessError,'SNAPSHOT_STALE'):
            s.read_file(self.root,'pilot',self.attempt(result),'policy.md',expected='0'*64)
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])
        self.assertEqual((self.root/'policy.md').read_bytes(),b'changed after verification')

    def test_repeated_snapshots_reuse_objects_without_deleting_evidence(self):
        first=self.run_check();second=self.run_check()
        objects=[p for p in (h.runtime(self.root)/'objects').rglob('*') if p.is_file()]
        self.assertEqual(len(objects),1)
        self.assertTrue((self.root/first['receipt']).exists())
        self.assertTrue((self.root/second['receipt']).exists())

    def test_corrupt_object_is_not_repaired_or_overwritten(self):
        result=self.run_check();listing=s.listing(self.root,'pilot',self.attempt(result))
        p=self.root/listing['files'][0]['object_path'];p.write_bytes(b'corrupt fixture')
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])
        with self.assertRaisesRegex(h.HarnessError,'corrupt'):self.run_check()
        self.assertEqual(p.read_bytes(),b'corrupt fixture')

    def test_manifest_corruption_is_rejected(self):
        result=self.run_check();path=(self.root/result['receipt']).with_name('inputs.json')
        manifest=h.read_json(path);manifest['inputs']['policy.md']='0'*64;h.atomic_json(path,manifest)
        with self.assertRaisesRegex(h.HarnessError,'manifest corrupt'):
            s.listing(self.root,'pilot',self.attempt(result))
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_snapshot_failure_cannot_leave_previous_pass_current(self):
        self.run_check();original=h.atomic_json
        def fail(path,value):
            if Path(path).name=='inputs.json':raise OSError('Synthetic storage failure')
            original(path,value)
        with patch.object(h,'atomic_json',side_effect=fail):
            with self.assertRaises(OSError):self.run_check()
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_change_between_archive_and_execution_is_stale(self):
        other=self.root/'other.py';other.write_bytes(b'old')
        original=h.verify
        def changed(*args,**kwargs):
            other.write_bytes(b'new')
            return original(*args,**kwargs)
        with patch.object(h,'verify',side_effect=changed):
            result=e.verify(self.root,'pilot','unit',self.activation,
                            [fixture.sys.executable,'-c','print("PILOT_OK")'],['other.py'],'PILOT_OK')
        self.assertEqual(result['status'],'STALE')
        self.assertEqual(s.read_file(self.root,'pilot',self.attempt(result),'other.py')['text'],'old')

    def test_binary_input_is_preserved_even_when_text_preview_is_lossy(self):
        binary=self.root/'input.bin';binary.write_bytes(b'\xff\x00raw')
        manifest=s.archive(self.root,h.watched(self.root,['input.bin']))
        path=s.object_path(self.root,manifest['inputs']['input.bin'])
        self.assertEqual(path.read_bytes(),binary.read_bytes())
        page=e.preview(self.root,path.relative_to(self.root).as_posix(),expected=manifest['inputs']['input.bin'])
        self.assertTrue(page['decoded_with_replacement'])

    def test_explicit_external_reference_bytes_are_also_frozen(self):
        external=self.root/'external.py';external.write_bytes(b'original reference')
        manifest=s.archive(self.root,h.watched(self.root,['policy.md']),
                           [dict(path=str(external),sha256=h.digest(external.read_bytes()))])
        path=h.task_dir(self.root,'pilot')/'attempts'/'external-test'/'inputs.json'
        h.atomic_json(path,manifest);external.write_bytes(b'new reference')
        page=s.listing(self.root,'pilot','external-test')
        row=next(r for r in page['files'] if r['source_type']=='EXTERNAL_REFERENCE')
        self.assertEqual((self.root/row['object_path']).read_bytes(),b'original reference')

    def test_paths_and_invalid_object_hashes_cannot_escape(self):
        with self.assertRaises(h.HarnessError):s.object_path(self.root,'../escape')
        with self.assertRaises(h.HarnessError):s.archive(self.root,{'../escape':'0'*64})
        with self.assertRaises(h.HarnessError):s.listing(self.root,'pilot','../escape')

    def test_report_pages_keep_all_attempt_totals(self):
        for _ in range(3):self.run_check()
        first=o.report(self.root,'pilot',limit=1)
        second=o.report(self.root,'pilot',offset=first['next_offset'],limit=1,expected=first['report_sha256'])
        self.assertEqual(len(first['attempts']),1)
        self.assertEqual(first['attempt_count'],3)
        self.assertEqual(first['verification_seconds'],second['verification_seconds'])
        self.assertNotEqual(first['attempts'][0]['attempt'],second['attempts'][0]['attempt'])

    def test_report_rejects_changed_observations_between_pages(self):
        result=self.run_check();page=o.report(self.root,'pilot',limit=1)
        o.observe_view(self.root,'pilot',result['output'])
        with self.assertRaisesRegex(h.HarnessError,'REPORT_STALE'):
            o.report(self.root,'pilot',expected=page['report_sha256'])

    def test_snapshot_listing_pages_are_bounded_and_hash_pinned(self):
        other=self.root/'second.md';other.write_bytes(b'two')
        manifest=s.archive(self.root,h.watched(self.root,['policy.md','second.md']))
        h.atomic_json(s.manifest_path(self.root,'pilot','page-test'),manifest)
        first=s.listing(self.root,'pilot','page-test',limit=1)
        second=s.listing(self.root,'pilot','page-test',offset=first['next_offset'],limit=1,expected=first['manifest_hash'])
        self.assertEqual(first['file_count'],2);self.assertIsNone(second['next_offset'])
        self.assertNotEqual(first['files'][0]['path'],second['files'][0]['path'])
        with self.assertRaises(h.HarnessError):s.listing(self.root,'pilot','page-test',expected='0'*64)


if __name__=='__main__':unittest.main()
