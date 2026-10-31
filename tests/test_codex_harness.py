"""Failure-focused tests, isolated from production/task records and external APIs."""
from copy import deepcopy
import importlib.util
import json
import errno
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'tools' / 'codex_harness.py'
spec = importlib.util.spec_from_file_location('harness', MODULE)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def task():
    return {'goal': 'Ship a verified local change', 'next_step': 'Inspect changed code',
            'critical': [{'id': 'keep-data', 'text': 'Do not delete user data.', 'source': 'user request'}],
            'decisions': [{'text': 'Keep exact constraints', 'reason': 'Avoid lossy summaries', 'source': 'proposal A'}],
            'required_checks': ['unit'], 'review_required': ['Review requirement coverage']}


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.file = self.root / 'code.py'
        self.file.write_text('version = 1\n', encoding='utf-8')
        h.checkpoint(self.root, 'work', task(), 0)

    def run_check(self, code='print("CHECK_OK")', marker='CHECK_OK', timeout=5, watch=None):
        return h.verify(self.root, 'work', 'unit', [sys.executable, '-c', code], watch or ['code.py'], marker, timeout)

    def test_exact_context_survives_new_process(self):
        proc = subprocess.run([sys.executable, str(MODULE), '--root', str(self.root), 'resume', 'work'], capture_output=True, check=True)
        result = json.loads(proc.stdout)
        self.assertEqual(result['saved_context']['task']['critical'], task()['critical'])
        self.assertEqual(result['verification']['acceptance'], 'NOT_VERIFIED')

    def test_cannot_silently_remove_critical(self):
        updated = task(); updated['critical'] = [{'id': 'other', 'text': 'Other instruction', 'source': 'new user request'}]
        with self.assertRaises(h.HarnessError): h.checkpoint(self.root, 'work', updated, 1)
        h.checkpoint(self.root, 'work', updated, 1, 'User explicitly replaced scope')
        self.assertEqual(h.load_task(self.root, 'work')['revision'], 2)
        old = h.read_json(h.task_dir(self.root, 'work') / 'revision-000001.json')
        self.assertEqual(old['task']['critical'], task()['critical'])

    def test_stale_writer_rejected(self):
        h.checkpoint(self.root, 'work', task(), 1)
        with self.assertRaises(h.HarnessError): h.checkpoint(self.root, 'work', task(), 1)

    def test_concurrent_writer_rejected(self):
        with h.locked(h.task_dir(self.root, 'work')):
            with self.assertRaises(h.HarnessError): h.checkpoint(self.root, 'work', task(), 1)

    def test_interrupted_temp_file_is_not_committed_revision(self):
        (h.task_dir(self.root, 'work') / '.pending-broken').write_text('{')
        self.assertEqual(h.load_task(self.root, 'work')['revision'], 1)

    def test_missing_critical_and_duplicate_ids_rejected(self):
        for value in ([], task()['critical'] * 2):
            updated = task(); updated['critical'] = value
            with self.assertRaises(h.HarnessError): h.validate_task(updated)

    def test_corrupt_current_state_fails_closed(self):
        (h.task_dir(self.root, 'work') / 'revision-000001.json').write_text('{')
        with self.assertRaises(ValueError): h.resume(self.root, 'work')

    def test_missing_evidence_not_pass(self):
        self.assertFalse(h.gate(self.root, 'work')['mechanical_checks_pass'])

    def test_valid_evidence_requires_semantic_review(self):
        self.assertEqual(self.run_check()['status'], 'PASS')
        result = h.gate(self.root, 'work')
        self.assertTrue(result['mechanical_checks_pass'])
        self.assertEqual(result['acceptance'], 'REVIEW_REQUIRED')

    def test_exit_zero_without_marker_is_unconfirmed(self):
        self.assertEqual(self.run_check('print("nothing checked")')['status'], 'UNCONFIRMED')

    def test_failure_with_marker_not_pass(self):
        self.assertEqual(self.run_check('print("CHECK_OK"); raise SystemExit(1)')['status'], 'FAIL')

    def test_zero_or_all_skipped_tests_not_pass(self):
        for output in ['Ran 0 tests in 0.0s\nOK', 'Ran 2 tests in 0.0s\nOK (skipped=2)', 'no tests ran']:
            self.assertEqual(self.run_check('print(' + repr(output) + ')', marker=output)['status'], 'UNCONFIRMED')

    def test_source_change_invalidates_evidence(self):
        self.run_check()
        self.file.write_text('version = 2\n')
        self.assertEqual(h.gate(self.root, 'work')['checks'][0]['status'], 'STALE')

    def test_new_file_in_watched_directory_invalidates_evidence(self):
        directory = self.root / 'src'; directory.mkdir(); (directory / 'a.py').write_text('x=1')
        self.run_check(watch=['src'])
        (directory / 'b.py').write_text('x=2')
        self.assertEqual(h.gate(self.root, 'work')['checks'][0]['status'], 'STALE')

    def test_deleted_watch_invalidates_evidence(self):
        self.run_check(); self.file.unlink()
        self.assertEqual(h.gate(self.root, 'work')['checks'][0]['status'], 'STALE')

    def test_changed_contract_invalidates_evidence(self):
        self.run_check()
        updated = task(); updated['goal'] = 'Changed requirements'
        h.checkpoint(self.root, 'work', updated, 1)
        self.assertEqual(h.gate(self.root, 'work')['checks'][0]['status'], 'STALE')

    def test_progress_only_update_keeps_valid_evidence(self):
        self.run_check()
        updated = task(); updated['next_step'] = 'Report verified result'
        h.checkpoint(self.root, 'work', updated, 1)
        self.assertTrue(h.gate(self.root, 'work')['mechanical_checks_pass'])

    def test_failed_final_save_cannot_reveal_previous_pass(self):
        self.run_check()
        original = h.atomic_json
        def fail_final(path, value):
            if value.get('status') == 'FAIL':
                raise OSError(errno.ENOSPC, 'Simulated full disk')
            return original(path, value)
        with patch.object(h, 'atomic_json', side_effect=fail_final):
            with self.assertRaises(OSError): self.run_check('raise SystemExit(1)')
        result = h.gate(self.root, 'work')
        self.assertFalse(result['mechanical_checks_pass'])
        self.assertEqual(result['checks'][0]['status'], 'RUNNING')

    def test_atomic_replace_failure_preserves_prior_state(self):
        path = self.root / 'state.json'; h.atomic_json(path, {'revision': 1})
        with patch.object(h.os, 'replace', side_effect=OSError(errno.ENOSPC, 'Simulated full disk')):
            with self.assertRaises(OSError): h.atomic_json(path, {'revision': 2})
        self.assertEqual(h.read_json(path), {'revision': 1})
        self.assertEqual(list(self.root.glob('.pending-*')), [])

    def test_concurrent_verification_of_same_check_rejected(self):
        with h.locked(h.task_dir(self.root, 'work') / 'verify-unit'):
            with self.assertRaises(h.HarnessError): self.run_check()

    def test_corrupt_disposable_index_is_rebuilt(self):
        (self.root / 'a.md').write_text('exact source')
        cache = h.runtime(self.root) / 'index.json.gz'; cache.write_bytes(b'partial gzip')
        with patch.object(h, 'git_files', return_value=['a.md']):
            result = h.search(self.root, 'exact')
        self.assertTrue(result['index']['recovered_cache'])
        self.assertEqual(result['matches'], 1)

    def test_changed_log_invalidates_evidence(self):
        record = self.run_check(); (self.root / record['log']).write_text('altered')
        self.assertEqual(h.gate(self.root, 'work')['checks'][0]['status'], 'STALE')

    def test_change_during_test_invalidates_evidence(self):
        result = self.run_check('from pathlib import Path; Path("code.py").write_text("v=2"); print("CHECK_OK")')
        self.assertEqual(result['status'], 'STALE')

    def test_timeout_is_not_success(self):
        result = self.run_check('import time; time.sleep(2)', timeout=.05)
        self.assertEqual(result['status'], 'TIMEOUT')
        self.assertFalse(h.gate(self.root, 'work')['mechanical_checks_pass'])

    def test_nonexistent_executable_is_blocked(self):
        result = h.verify(self.root, 'work', 'unit', ['__nonexistent_executable_39848__'], ['code.py'], 'OK')
        self.assertEqual(result['status'], 'BLOCKED')

    def test_no_checks_is_not_vacuous_pass(self):
        value = task(); value['required_checks'] = []
        h.checkpoint(self.root, 'work', value, 1)
        self.assertFalse(h.gate(self.root, 'work')['mechanical_checks_pass'])

    def test_paths_cannot_escape(self):
        for value in ['../outside.md', str(self.root.parent / 'outside.md'), '.git/config']:
            with self.assertRaises(h.HarnessError): h.within(self.root, value)
        with self.assertRaises(h.HarnessError): h.task_dir(self.root, '../outside')

    def test_symlink_escape_rejected_when_available(self):
        link = self.root / 'escape'
        try: link.symlink_to(self.root.parent, target_is_directory=True)
        except OSError: self.skipTest('Symlink permission unavailable')
        with self.assertRaises(h.HarnessError): h.within(self.root, 'escape/file.md')

    def test_exact_source_pagination_and_changed_sha(self):
        path = self.root / 'notes.md'; path.write_text('制約\nline 2\nlast\n', encoding='utf-8')
        result = h.source(self.root, 'notes.md', count=2)
        self.assertEqual(result['text'], '制約\nline 2')
        self.assertEqual(result['next_start'], 3)
        path.write_text('new')
        with self.assertRaises(h.HarnessError): h.source(self.root, 'notes.md', expected=result['sha256'])

    def test_search_cache_refresh_and_explicit_pagination(self):
        for name in ['a.md', 'b.md']: (self.root / name).write_text('# Constraints\nkeep exact\n')
        with patch.object(h, 'git_files', return_value=['a.md', 'b.md']):
            first = h.search(self.root, 'keep', limit=1)
            self.assertEqual(first['matches'], 2); self.assertEqual(first['next_offset'], 1)
            second = h.search(self.root, 'keep', limit=1, offset=1)
            self.assertNotEqual(first['hits'][0]['path'], second['hits'][0]['path'])
            self.assertEqual(second['index']['parsed'], 0)
            (self.root / 'a.md').write_text('unrelated')
            third = h.search(self.root, 'keep')
            self.assertEqual(third['matches'], 1); self.assertEqual(third['index']['parsed'], 1)

    def test_cli_verify_argument_order(self):
        proc = subprocess.run([sys.executable, str(MODULE), '--root', str(self.root), 'verify', 'work', 'unit',
                               '--watch', 'code.py', '--marker', 'CHECK_OK', '--', sys.executable, '-c', 'print("CHECK_OK")'], capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['status'], 'PASS')


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.base = {'conditions': {'suite_revision': '1', 'model': 'fixed', 'settings': {}, 'sources': 'fixed'},
                     'runs': [{'case_id': 'retain', 'repeat': 1, 'quality': 'PASS', 'tokens': 100, 'seconds': 100}]}
        self.new = deepcopy(self.base)
        self.new['runs'][0].update(tokens=70, seconds=80)

    def test_paired_improvement(self):
        self.assertEqual(h.compare(self.base, self.new)['verdict'], 'ELIGIBLE_FOR_REVIEW')

    def test_faster_but_wrong_is_rejected(self):
        self.new['runs'][0]['quality'] = 'FAIL'
        self.assertEqual(h.compare(self.base, self.new)['verdict'], 'REJECT')

    def test_missing_tokens_cannot_claim_savings(self):
        self.new['runs'][0]['tokens'] = None
        result = h.compare(self.base, self.new)
        self.assertEqual(result['verdict'], 'INSUFFICIENT_EVIDENCE')
        self.assertIsNone(result['metrics']['tokens']['reduction'])

    def test_changed_model_rejected(self):
        self.new['conditions']['model'] = 'different'
        with self.assertRaises(h.HarnessError): h.compare(self.base, self.new)

    def test_missing_pair_rejected(self):
        self.new['runs'][0]['case_id'] = 'other'
        with self.assertRaises(h.HarnessError): h.compare(self.base, self.new)

    def test_duplicate_pair_rejected(self):
        self.new['runs'].append(self.new['runs'][0])
        with self.assertRaises(h.HarnessError): h.compare(self.base, self.new)

    def test_nonfinite_metric_rejected(self):
        self.new['runs'][0]['tokens'] = float('nan')
        with self.assertRaises(h.HarnessError): h.compare(self.base, self.new)

    def test_unknown_quality_not_accepted(self):
        self.new['runs'][0]['quality'] = 'UNKNOWN'
        self.assertEqual(h.compare(self.base, self.new)['verdict'], 'REJECT')

    def test_one_regression_not_hidden_by_average(self):
        self.base['runs'].append({'case_id': 'other', 'repeat': 1, 'quality': 'PASS', 'tokens': 10, 'seconds': 10})
        self.new['runs'].append({'case_id': 'other', 'repeat': 1, 'quality': 'PASS', 'tokens': 11, 'seconds': 11})
        self.assertEqual(h.compare(self.base, self.new)['verdict'], 'INSUFFICIENT_EVIDENCE')


if __name__ == '__main__':
    unittest.main()
