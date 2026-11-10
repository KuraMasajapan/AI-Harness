import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import codex_views as v
import codex_harness as h


class ViewsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'agents/Codex/GOALS.md'
        self.source.parent.mkdir(parents=True)
        self.source.write_text('Shared fixture only', encoding='utf-8')
        self.packet = dict(schema=1, sharing='DRAFT_NOT_SENT', entries=[dict(
            id='goal', revision=1, classification='SHARED_CANDIDATE', status='ACTIVE',
            project='test', text='Do not replace primary evidence.',
            source_path='agents/Codex/GOALS.md', source_sha256=h.digest(self.source.read_bytes()),
            expires_at='2030-01-01T00:00:00Z')])
        self.packet_path = self.root / 'packet.json'
        self.state = dict(task_id='test', revision=1, recorded_at='2026-11-07T00:00:00Z',
                          branch='codex/test', head='a' * 40, dirty=True, operation='OPEN',
                          freshness='CURRENT', acceptance='NOT_VERIFIED',
                          checks=[dict(id='unit', status='NOT_CURRENT', reason='<script>alert(1)</script>')],
                          goal='<img src=x onerror=alert(1)>', next_step='Verify first', review_required=['Human review'])

    def compile(self, packet=None):
        self.packet_path.write_text(json.dumps(packet or self.packet), encoding='utf-8')
        return v.compile_memory(self.root, self.packet_path, datetime(2026, 11, 7, tzinfo=timezone.utc))

    def test_stale_gate_and_untrusted_html_remain_visible_and_escaped(self):
        html = v.render(self.state, ['checks'], [])
        self.assertIn('NOT_CURRENT', html)
        self.assertIn('NOT_VERIFIED', html)
        self.assertNotIn('<script>', html)
        self.assertNotIn('<img ', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('現在状態は再生成', html)

    def test_three_cycles_preserve_history_and_failed_refresh_preserves_view(self):
        with patch.object(v, 'collect', return_value=self.state):
            for _ in range(3):
                result = v.dashboard(self.root, 'test')
        page = Path(result['output'])
        history = h.read_json(page.parent / 'history.json')
        self.assertEqual(len(history), 3)
        for row in history:
            self.assertTrue((page.parent / row['file']).is_file())
            snapshot = (page.parent / row['file']).read_text(encoding='utf-8')
            self.assertNotIn('href="state.json"', snapshot)
        original = page.read_bytes()
        with patch.object(v, 'collect', side_effect=h.HarnessError('unavailable')):
            with self.assertRaises(h.HarnessError):
                v.dashboard(self.root, 'test')
        self.assertEqual(page.read_bytes(), original)

    def test_semantic_diff_ignores_generation_time(self):
        changed = dict(self.state, recorded_at='later')
        self.assertEqual(v.differences(self.state, changed), [])
        changed['checks'] = []
        self.assertEqual(v.differences(self.state, changed), ['checks'])

    def test_memory_draft_and_provenance_no_implicit_send(self):
        self.assertIn('DRAFT_NOT_SENT', self.compile())
        result = v.memory_draft(self.root, self.packet_path)
        self.assertEqual(result['network_calls'], 0)
        provenance = h.read_json(Path(result['output']).parent / 'provenance.json')
        self.assertEqual(provenance['output_sha256'], h.digest(Path(result['output']).read_bytes()))

    def test_memory_rejects_private_and_duplicate_entries(self):
        for classification in ('PRIVATE', 'AI_SPECIFIC', ''):
            packet = copy.deepcopy(self.packet)
            packet['entries'][0]['classification'] = classification
            with self.assertRaises(h.HarnessError):
                self.compile(packet)
        packet = copy.deepcopy(self.packet)
        packet['entries'] *= 2
        with self.assertRaises(h.HarnessError):
            self.compile(packet)

    def test_memory_rejects_stale_source_and_expired_record(self):
        packet = copy.deepcopy(self.packet)
        packet['entries'][0]['source_sha256'] = '0' * 64
        with self.assertRaises(h.HarnessError):
            self.compile(packet)
        packet = copy.deepcopy(self.packet)
        packet['entries'][0]['expires_at'] = '2026-11-06T00:00:00Z'
        with self.assertRaises(h.HarnessError):
            self.compile(packet)

    def test_runtime_and_path_escape_not_exported(self):
        for source in ('.harness-runtime/private.md', 'agents/Codex/../../../../private.md'):
            packet = copy.deepcopy(self.packet)
            packet['entries'][0]['source_path'] = source
            with self.assertRaises((h.HarnessError, OSError)):
                self.compile(packet)

    def test_collection_uses_wrapper_status_without_promoting_it(self):
        task = dict(goal='goal', next_step='next', review_required=[])
        operation = dict(state='OPEN', freshness='CURRENT', verification=dict(
            acceptance='NOT_VERIFIED', checks=[dict(id='unit', status='NOT_CURRENT', reason='Runtime changed')]))
        with patch.object(h, 'load_task', return_value=dict(revision=4, task=task)), \
             patch.object(v.operations, 'operation', return_value=operation), \
             patch.object(v, 'git', side_effect=['codex/test', 'a' * 40, '?? dirty']):
            state = v.collect(self.root, 'test')
        self.assertEqual(state['checks'][0]['status'], 'NOT_CURRENT')
        self.assertEqual(state['acceptance'], 'NOT_VERIFIED')

    def test_resume_plan_prioritizes_reconciliation_and_preserves_context(self):
        task = dict(goal='goal', next_step='next', required_checks=['unit'],
                    critical=[dict(id='protect', text='既存証拠を保持', source='Human')],
                    decisions=[dict(text='decision', reason='why', source='Human')],
                    review_required=['Human review'])
        saved = dict(revision=4, task=task)
        for fresh, status, action in (
            ('CURRENT', 'PASS', 'RECONFIRM'),
            ('CURRENT', 'NOT_CURRENT', 'VERIFY_REQUIRED'),
            ('STALE', 'PASS', 'RECONCILE'),
        ):
            with self.subTest(action=action):
                current = dict(state='OPEN', freshness=fresh, verification=dict(
                    revision=4, mechanical_checks_pass=status == 'PASS',
                    acceptance='REVIEW_REQUIRED' if status == 'PASS' else 'NOT_VERIFIED',
                    checks=[dict(id='unit', status=status)]))
                with patch.object(h, 'load_task', return_value=saved), \
                     patch.object(v.operations, 'operation', return_value=current):
                    result = v.resume_plan(self.root, 'test')
                self.assertEqual(result['action'], action)
                self.assertEqual(result['critical'], task['critical'])
                self.assertEqual(result['decisions'], task['decisions'])

    def test_resume_plan_missing_checks_never_reconfirm_and_revision_race_stops(self):
        saved = dict(revision=4, task=dict(goal='goal', next_step='next', required_checks=['unit'],
                                         critical=[], decisions=[], review_required=[]))
        verification = dict(revision=4, mechanical_checks_pass=True, checks=[])
        current = dict(state='OPEN', freshness='CURRENT', verification=verification)
        with patch.object(h, 'load_task', return_value=saved), \
             patch.object(v.operations, 'operation', return_value=current):
            self.assertEqual(v.resume_plan(self.root, 'test')['action'], 'VERIFY_REQUIRED')
            verification['revision'] = 5
            with self.assertRaises(h.HarnessError):
                v.resume_plan(self.root, 'test')


if __name__ == '__main__':
    unittest.main()
