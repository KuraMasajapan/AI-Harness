"""Real workflow regression discovered during the M2 read-only pilot."""
from copy import deepcopy
import unittest
import test_codex_environment as fixture
import codex_operations as o

e, h = fixture.e, fixture.h


class CheckedReentryTests(unittest.TestCase):
    setUp = fixture.EnvironmentTests.setUp
    run_check = fixture.EnvironmentTests.run_check

    def checked(self):
        first=o.begin(self.root,'pilot',self.contract)
        self.run_check();o.finish(self.root,'pilot')
        return first

    def test_checked_operation_restarts_with_saved_contract(self):
        first=self.checked();current=o.begin(self.root,'pilot')
        self.assertEqual(current['freshness'],'CURRENT')
        self.assertNotEqual(first['operation_id'],current['operation_id'])
        self.assertEqual(current['saved_context']['critical'],self.task['critical'])
        self.assertEqual(h.read_json(self.root/current['activation'])['contract'],self.contract)

    def test_checked_operation_does_not_silently_accept_changed_source(self):
        self.checked();before=o.latest(self.root,'pilot')
        (self.root/'policy.md').write_text('Changed source',encoding='utf-8')
        with self.assertRaisesRegex(h.HarnessError,'SOURCE_STALE'):o.begin(self.root,'pilot')
        self.assertEqual(o.latest(self.root,'pilot')['event_hash'],before['event_hash'])

    def test_checked_operation_requires_goal_reconciliation(self):
        self.checked();task=deepcopy(self.task);task['goal']='New user objective'
        h.checkpoint(self.root,'pilot',task,1,'User correction')
        with self.assertRaisesRegex(h.HarnessError,'Operation contract changed'):o.begin(self.root,'pilot')
        current=o.begin(self.root,'pilot',refresh=True)
        self.assertEqual(current['saved_context']['goal'],task['goal'])
        self.assertFalse(current['verification']['mechanical_checks_pass'])

    def test_progress_only_update_does_not_need_new_contract(self):
        self.checked();task=deepcopy(self.task);task['next_step']='Continue current objective'
        h.checkpoint(self.root,'pilot',task,1)
        current=o.begin(self.root,'pilot')
        self.assertEqual(current['freshness'],'CURRENT')
        self.assertEqual(current['saved_context']['next_step'],task['next_step'])


if __name__=='__main__':unittest.main()
