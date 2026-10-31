"""Recovery must not depend on unreadable old activation or bypass authority."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import test_codex_environment as fixture
import codex_operations as o

e,h=fixture.e,fixture.h


class ExplicitRefreshTests(unittest.TestCase):
    setUp=fixture.EnvironmentTests.setUp
    run_check=fixture.EnvironmentTests.run_check

    def unreadable(self, activation, error):
        original=h.read_json
        def read(path):
            if Path(path)==self.root/activation:raise error
            return original(path)
        return patch.object(h,'read_json',side_effect=read)

    def test_explicit_refresh_recovers_open_without_reading_old_activation(self):
        first=o.begin(self.root,'pilot',self.contract);self.activation=first['activation'];self.run_check()
        with self.unreadable(first['activation'],FileNotFoundError('fixture')):
            current=o.begin(self.root,'pilot',self.contract,refresh=True)
            self.assertEqual(current['freshness'],'CURRENT')
            self.assertEqual(first['operation_id'],current['operation_id'])
            self.assertNotEqual(first['activation'],current['activation'])
            self.assertFalse(current['verification']['mechanical_checks_pass'])
        (self.root/'policy.md').write_text('Changed',encoding='utf-8')
        with self.assertRaisesRegex(h.HarnessError,'SOURCE_STALE'):
            o.begin(self.root,'pilot')

    def test_explicit_refresh_recovers_checked_with_corrupt_old_json(self):
        first=o.begin(self.root,'pilot',self.contract);self.run_check();o.finish(self.root,'pilot')
        with self.unreadable(first['activation'],json.JSONDecodeError('fixture','',0)):
            current=o.begin(self.root,'pilot',self.contract,refresh=True)
        self.assertNotEqual(first['operation_id'],current['operation_id'])
        self.assertEqual(current['freshness'],'CURRENT')

    def test_missing_or_corrupt_activation_without_both_explicit_flags_stops(self):
        first=o.begin(self.root,'pilot',self.contract)
        for error in (FileNotFoundError('fixture'),json.JSONDecodeError('fixture','',0)):
            for contract,refresh in ((None,False),(self.contract,False),(None,True)):
                with self.subTest(error=type(error).__name__,explicit=contract is not None,refresh=refresh):
                    before=o.latest(self.root,'pilot')['event_hash']
                    with self.unreadable(first['activation'],error):
                        with self.assertRaisesRegex(h.HarnessError,'explicit --contract with --refresh'):
                            o.begin(self.root,'pilot',contract,refresh)
                    self.assertEqual(o.latest(self.root,'pilot')['event_hash'],before)

    def test_malformed_activation_shape_is_a_clean_failure(self):
        first=o.begin(self.root,'pilot',self.contract)
        original=h.read_json
        for bad in ([],{},dict(contract=[])):
            with self.subTest(bad=bad):
                with patch.object(h,'read_json',side_effect=lambda p:bad if Path(p)==self.root/first['activation'] else original(p)):
                    with self.assertRaisesRegex(h.HarnessError,'explicit --contract with --refresh'):
                        o.begin(self.root,'pilot',refresh=True)

    def test_healthy_refresh_preserves_operation_rules_and_current_evidence(self):
        first=o.begin(self.root,'pilot',self.contract);self.run_check()
        current=o.begin(self.root,'pilot',self.contract,refresh=True)
        self.assertEqual(first['operation_id'],current['operation_id'])
        self.assertEqual(o.latest(self.root,'pilot')['event'],'REVALIDATED')
        self.assertTrue(current['verification']['mechanical_checks_pass'])

    def test_invalid_explicit_contract_does_not_change_operation_history(self):
        o.begin(self.root,'pilot',self.contract)
        for change in ('branch','base_commit','sources'):
            bad=deepcopy(self.contract)
            bad[change]={'branch':'wrong','base_commit':'0'*40,'sources':[dict(path='absent.md',authority='ACTIVE')]}[change]
            before=o.latest(self.root,'pilot')['event_hash']
            with self.subTest(change=change):
                with self.assertRaises(h.HarnessError):o.begin(self.root,'pilot',bad,True)
                self.assertEqual(o.latest(self.root,'pilot')['event_hash'],before)

    def test_event_chain_corruption_cannot_be_bypassed(self):
        first=o.begin(self.root,'pilot',self.contract)
        directory=h.task_dir(self.root,'pilot')/'operations'/first['operation_id']
        path=directory/'event-000001.json';event=h.read_json(path);event['state']='CORRUPTED'
        h.atomic_json(path,event)
        with patch.object(e,'activate') as activate:
            with self.assertRaisesRegex(h.HarnessError,'history corrupt'):
                o.begin(self.root,'pilot',self.contract,True)
            activate.assert_not_called()

    def test_explicit_refresh_with_new_goal_invalidates_old_contract_evidence(self):
        first=o.begin(self.root,'pilot',self.contract);self.activation=first['activation'];self.run_check()
        task=deepcopy(self.task);task['goal']='Changed objective from current user'
        h.checkpoint(self.root,'pilot',task,1,'User changed objective')
        current=o.begin(self.root,'pilot',self.contract,refresh=True)
        self.assertEqual(current['freshness'],'CURRENT')
        self.assertEqual(current['saved_context']['goal'],task['goal'])
        self.assertFalse(current['verification']['mechanical_checks_pass'])
        self.assertEqual(current['verification']['checks'][0]['status'],'STALE')


if __name__=='__main__':unittest.main()
