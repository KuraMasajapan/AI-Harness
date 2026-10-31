"""Branch operation, runtime freshness, and observed-volume regressions."""
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import test_codex_environment as fixture

e, h = fixture.e, fixture.h
import codex_operations as o


class OperationTests(unittest.TestCase):
    setUp = fixture.EnvironmentTests.setUp
    run_check = fixture.EnvironmentTests.run_check

    def test_begin_and_reentry_do_not_duplicate_operation(self):
        first=o.begin(self.root,'pilot',self.contract)
        second=o.begin(self.root,'pilot')
        self.assertEqual(first['state'],'OPEN')
        self.assertTrue(second['reused'])
        self.assertEqual(first['operation_id'],second['operation_id'])
        self.assertEqual(o.latest(self.root,'pilot')['sequence'],1)
        self.assertEqual(second['saved_context']['critical'],self.task['critical'])

    def test_first_begin_requires_explicit_contract(self):
        with self.assertRaises(h.HarnessError):o.begin(self.root,'pilot')
        self.assertIsNone(o.latest(self.root,'pilot'))

    def test_stale_reentry_requires_explicit_refresh(self):
        first=o.begin(self.root,'pilot',self.contract)
        (self.root/'policy.md').write_text('New source',encoding='utf-8')
        with self.assertRaisesRegex(h.HarnessError,'SOURCE_STALE'):o.begin(self.root,'pilot')
        current=o.begin(self.root,'pilot',refresh=True)
        self.assertEqual(current['operation_id'],first['operation_id'])
        self.assertEqual(o.latest(self.root,'pilot')['sequence'],2)
        self.assertEqual(current['freshness'],'CURRENT')

    def test_user_goal_correction_is_not_silently_reused(self):
        o.begin(self.root,'pilot',self.contract)
        task=deepcopy(self.task);task['goal']='Corrected main objective'
        h.checkpoint(self.root,'pilot',task,1,'Current user correction')
        with self.assertRaises(h.HarnessError):o.begin(self.root,'pilot')
        current=o.begin(self.root,'pilot',refresh=True)
        self.assertEqual(current['saved_context']['goal'],task['goal'])

    def test_next_step_change_can_reenter_without_reactivation(self):
        first=o.begin(self.root,'pilot',self.contract)
        task=deepcopy(self.task);task['next_step']='Next step only'
        h.checkpoint(self.root,'pilot',task,1)
        second=o.begin(self.root,'pilot')
        self.assertEqual(first['activation'],second['activation'])
        self.assertEqual(second['saved_context']['next_step'],'Next step only')

    def test_finish_requires_current_checks(self):
        o.begin(self.root,'pilot',self.contract)
        with self.assertRaises(h.HarnessError):o.finish(self.root,'pilot')
        self.assertEqual(o.latest(self.root,'pilot')['state'],'OPEN')

    def test_finish_is_not_adoption_or_human_approval(self):
        first=o.begin(self.root,'pilot',self.contract);self.run_check()
        final=o.finish(self.root,'pilot')
        self.assertEqual(final['state'],'CHECKED')
        self.assertEqual(final['acceptance'],'REVIEW_REQUIRED')
        self.assertEqual(final['report']['adoption'],'BRANCH_TRIAL')
        next_operation=o.begin(self.root,'pilot',self.contract)
        self.assertNotEqual(next_operation['operation_id'],first['operation_id'])
        self.assertTrue((h.task_dir(self.root,'pilot')/'operations'/first['operation_id']).is_dir())

    def test_corrupt_history_cannot_be_reused(self):
        result=o.begin(self.root,'pilot',self.contract)
        p=h.task_dir(self.root,'pilot')/'operations'/result['operation_id']/'event-000001.json'
        record=h.read_json(p);record['state']='FORGED';h.atomic_json(p,record)
        with self.assertRaises(h.HarnessError):o.begin(self.root,'pilot')

    def test_uncommitted_event_does_not_corrupt_previous_committed_state(self):
        o.begin(self.root,'pilot',self.contract)
        prior=o.latest(self.root,'pilot');original=h.atomic_json
        values={k:prior[k] for k in ('activation','task_contract','started_at')}
        values.update(state='CHECKED',event='FINISHED')
        def fail_pointer(path,value):
            if Path(path).name=='active-operation.json':raise OSError('Synthetic failed pointer save')
            original(path,value)
        with patch.object(h,'atomic_json',side_effect=fail_pointer):
            with self.assertRaises(OSError):o.append(self.root,'pilot',prior['operation_id'],values,prior)
        self.assertEqual(o.latest(self.root,'pilot')['event_hash'],prior['event_hash'])
        self.assertEqual(o.latest(self.root,'pilot')['state'],'OPEN')

    def test_current_execution_failure_is_not_mislabeled_as_stale(self):
        self.run_check('print("PILOT_OK"); raise SystemExit(1)')
        self.assertEqual(e.gate(self.root,'pilot')['checks'][0]['status'],'FAIL')

    def test_environment_change_invalidates_pass_without_storing_values(self):
        result=self.run_check()
        with patch.dict(os.environ,{'PYTHONPATH':'private-path-value-never-store'}):
            self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])
        invocation=(self.root/result['receipt']).with_name('invocation.json').read_text(encoding='utf-8')
        self.assertNotIn('private-path-value-never-store',invocation)
        self.assertTrue(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_adapter_change_invalidates_pass_without_explicit_watch(self):
        self.run_check();original=Path.read_bytes;target=Path(e.__file__).resolve()
        def changed(path):
            return b'changed adapter' if path.resolve()==target else original(path)
        with patch.object(Path,'read_bytes',changed):
            self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_runtime_change_during_execution_is_stale(self):
        original=e.runtime_fingerprint
        calls=0
        def changed(root,command):
            nonlocal calls
            calls+=1;value=original(root,command)
            if calls>1:value['platform']='changed'
            return value
        with patch.object(e,'runtime_fingerprint',side_effect=changed):result=self.run_check()
        self.assertEqual(result['status'],'STALE')

    def test_paged_output_rejects_mixed_log_versions(self):
        p=self.root/'log.txt';p.write_text('original Japanese 日本語',encoding='utf-8')
        first=e.preview(self.root,'log.txt',count=5)
        p.write_text('modified Japanese 日本語',encoding='utf-8')
        with self.assertRaisesRegex(h.HarnessError,'OUTPUT_STALE'):
            e.preview(self.root,'log.txt',offset=first['next_offset'],expected=first['sha256'])

    def test_streamed_preview_handles_unicode_chunk_boundaries_and_invalid_utf8(self):
        raw=b'a'*65535+'日本語'.encode('utf-8')+b'\xfftail'
        (self.root/'log.txt').write_bytes(raw)
        with patch.object(Path,'read_bytes',side_effect=AssertionError('Do not load the entire log')):
            page=e.preview(self.root,'log.txt',offset=65534,count=20,stream=True)
        self.assertEqual(page['text'],raw.decode('utf-8',errors='replace')[65534:])
        self.assertTrue(page['decoded_with_replacement'])
        self.assertEqual(page['sha256'],h.digest(raw))

    def test_runtime_hash_tracks_executable_bytes(self):
        p=self.root/'fake.exe';p.write_bytes(b'first')
        first=e.runtime_fingerprint(self.root,[str(p)])
        p.write_bytes(b'second')
        self.assertNotEqual(first,e.runtime_fingerprint(self.root,[str(p)]))

    def test_telemetry_observes_actual_views_and_keeps_tokens_unknown(self):
        self.run_check();report=o.report(self.root,'pilot')
        self.assertEqual(report['attempt_count'],1)
        self.assertEqual(report['recorded_view_count'],1)
        self.assertGreater(report['displayed_text_bytes'],0)
        self.assertIsNone(report['model_tokens'])
        self.assertIsNone(report['human_interventions'])
        self.assertEqual(report['quality_regression'],'UNRESOLVED')

    def test_incomplete_attempt_is_partial_not_zero_cost(self):
        folder=h.task_dir(self.root,'pilot')/'attempts'/'interrupted';folder.mkdir(parents=True)
        report=o.report(self.root,'pilot')
        self.assertEqual(report['metrics_status'],'PARTIAL')
        self.assertIsNone(report['verification_seconds'])
        self.assertEqual(report['attempts'][0]['status'],'INCOMPLETE')

    def test_metrics_save_failure_does_not_change_functional_result(self):
        original=h.atomic_json
        def fail_view(path,value):
            if Path(path).parent.name=='views':raise OSError('Synthetic full disk')
            original(path,value)
        with patch.object(h,'atomic_json',side_effect=fail_view):result=self.run_check()
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['observation']['status'],'UNAVAILABLE')
        self.assertTrue(e.gate(self.root,'pilot')['mechanical_checks_pass'])
        report=o.report(self.root,'pilot')
        self.assertEqual(report['metrics_status'],'PARTIAL')
        self.assertIsNone(report['displayed_text_bytes'])
        self.assertEqual(report['missing_view_observations'],1)


if __name__=='__main__':unittest.main()
