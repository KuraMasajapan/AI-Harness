"""Source/continuation/receipt/output negative controls. No AI calls or services."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import codex_environment as e
import codex_harness as h

REPOSITORY = Path(__file__).resolve().parents[1]


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for args in [('init', '-b', 'codex/test'), ('config','user.email','test@example.invalid'),
                     ('config','user.name','Synthetic test'), ('remote','add','origin','https://example.invalid/test')]:
            subprocess.run(['git','-C',str(self.root),*args], check=True,capture_output=True)
        (self.root / 'policy.md').write_text('Do not publish.\n',encoding='utf-8')
        subprocess.run(['git','-C',str(self.root),'add','policy.md'],check=True,capture_output=True)
        subprocess.run(['git','-C',str(self.root),'commit','-m','Synthetic fixture'],check=True,capture_output=True)
        folder = self.root / 'experiments/trinity/operations'; folder.mkdir(parents=True)
        for name in ('receipt.template.json','receipt.schema.json','check_receipt.py'):
            shutil.copyfile(REPOSITORY / 'experiments/trinity/operations' / name, folder / name)
        self.task = dict(goal='Improve Codex environment', next_step='Verify the adapter',
                         critical=[dict(id='scope',text='TRINITY is optional support only.',source='current user correction')],
                         decisions=[],required_checks=['unit'],review_required=['Check behavior and overhead'])
        h.checkpoint(self.root,'pilot',self.task,0)
        self.contract = dict(repository='https://example.invalid/test',branch='codex/test',
                             base_commit=e.git(self.root,'rev-parse','HEAD'),
                             sources=[dict(path='policy.md',authority='ACTIVE')])
        self.activation = e.activate(self.root,'pilot',self.contract)['activation']

    def run_check(self, code='print("PILOT_OK")'):
        return e.verify(self.root,'pilot','unit',self.activation,[sys.executable,'-c',code],['policy.md'],'PILOT_OK')

    def test_current_sources_and_existing_receipt_shape(self):
        result=self.run_check()
        self.assertEqual(result['status'],'PASS')
        final=h.read_json(self.root/result['receipt'])
        pre=h.read_json((self.root/result['receipt']).with_name('pre.json'))
        self.assertEqual(final['receipt_version'],'1')
        self.assertEqual(pre['expected_timing'],'BEFORE_EXECUTION')
        self.assertEqual(final['expected_timing'],'AFTER_EXECUTION')
        self.assertEqual(final['evidence']['executor_model']['status'],'UNRESOLVED')
        self.assertTrue(e.gate(self.root,'pilot')['mechanical_checks_pass'])
        self.assertEqual(e.gate(self.root,'pilot')['acceptance'],'REVIEW_REQUIRED')

    def test_wrong_branch_stops_before_command(self):
        subprocess.run(['git','-C',str(self.root),'switch','-c','wrong'],check=True,capture_output=True)
        with patch.object(h,'verify') as execute:
            with self.assertRaisesRegex(h.HarnessError,'branch'): self.run_check()
            execute.assert_not_called()

    def test_wrong_repository_stops_before_command(self):
        bad=deepcopy(self.contract);bad['repository']='https://example.invalid/other'
        with self.assertRaisesRegex(h.HarnessError,'repository'): e.activate(self.root,'pilot',bad)

    def test_wrong_base_rejected(self):
        bad=deepcopy(self.contract);bad['base_commit']='0'*40
        with self.assertRaisesRegex(h.HarnessError,'ancestor'): e.activate(self.root,'pilot',bad)

    def test_unavailable_is_not_claimed_nonexistent_everywhere(self):
        bad=deepcopy(self.contract);bad['sources'][0]['path']='missing.md'
        with self.assertRaisesRegex(h.HarnessError,'SOURCE_UNAVAILABLE'): e.activate(self.root,'pilot',bad)

    def test_source_authority_required(self):
        bad=deepcopy(self.contract);bad['sources'][0]['authority']='AUTO_APPROVED'
        with self.assertRaises(h.HarnessError):e.activate(self.root,'pilot',bad)

    def test_explicit_external_dependency_change_invalidates_activation(self):
        contract=deepcopy(self.contract)
        path=self.root/'external-validator.py';path.write_text('version=1',encoding='utf-8')
        contract['external_sources']=[dict(path=str(path),sha256=h.digest(path.read_bytes()))]
        active=e.activate(self.root,'pilot',contract)['activation']
        path.write_text('version=2',encoding='utf-8')
        with self.assertRaisesRegex(h.HarnessError,'EXTERNAL_SOURCE_STALE'):e.source_guard(self.root,'pilot',active)

    def test_source_change_stops_old_activation(self):
        (self.root/'policy.md').write_text('Changed policy',encoding='utf-8')
        with self.assertRaisesRegex(h.HarnessError,'SOURCE_STALE'):self.run_check()

    def test_source_change_after_pass_invalidates_gate(self):
        self.run_check();(self.root/'policy.md').write_text('New',encoding='utf-8')
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_another_task_activation_rejected(self):
        h.checkpoint(self.root,'another',self.task,0)
        with self.assertRaises(h.HarnessError):e.source_guard(self.root,'another',self.activation)

    def test_corrupt_activation_rejected(self):
        path=self.root/self.activation;value=h.read_json(path);value['task_id']='forged';h.atomic_json(path,value)
        with self.assertRaises(h.HarnessError):self.run_check()

    def test_helper_pass_cannot_bypass_environment_gate(self):
        h.verify(self.root,'pilot','unit',[sys.executable,'-c','print("PILOT_OK")'],['policy.md'],'PILOT_OK')
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_later_helper_pass_cannot_reuse_old_receipt(self):
        self.run_check()
        h.verify(self.root,'pilot','unit',[sys.executable,'-c','print("PILOT_OK")'],['policy.md'],'PILOT_OK')
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_task_change_between_prerecord_and_execution_is_stale(self):
        original=h.verify
        def changed(*args,**kwargs):
            task=deepcopy(self.task);task['goal']='Changed before execution'
            h.checkpoint(self.root,'pilot',task,1,'Synthetic correction')
            return original(*args,**kwargs)
        with patch.object(h,'verify',side_effect=changed):result=self.run_check()
        self.assertEqual(result['status'],'STALE')

    def test_missing_receipt_field_cannot_pass(self):
        result=self.run_check();path=self.root/result['receipt'];value=h.read_json(path)
        del value['evidence']['reviewer'];h.atomic_json(path,value)
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_goal_correction_invalidates_old_pass(self):
        self.run_check(); updated=deepcopy(self.task);updated['goal']='Corrected main goal'
        h.checkpoint(self.root,'pilot',updated,1,'User correction')
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_progress_update_keeps_valid_proof(self):
        self.run_check();updated=deepcopy(self.task);updated['next_step']='Review results'
        h.checkpoint(self.root,'pilot',updated,1)
        self.assertTrue(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_final_save_failure_cannot_expose_old_pass(self):
        self.run_check();original=h.atomic_json
        def fail_final(path,value):
            if Path(path).name=='final.json':raise OSError('Synthetic full disk')
            original(path,value)
        with patch.object(h,'atomic_json',side_effect=fail_final):
            with self.assertRaises(OSError):self.run_check()
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_log_tamper_invalidates_gate(self):
        result=self.run_check();(self.root/result['output']['path']).write_text('tampered',encoding='utf-8')
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_failure_preserves_full_log(self):
        result=self.run_check('print("PILOT_OK"); raise SystemExit(1)')
        self.assertEqual(result['status'],'FAIL');self.assertIn('PILOT_OK',result['output']['text'])
        self.assertFalse(e.gate(self.root,'pilot')['mechanical_checks_pass'])

    def test_large_single_line_pages_reconstruct_japanese(self):
        text='重要条件を保存'*1200
        (self.root/'huge.log').write_bytes(text.encode('utf-8'))
        pages=[];offset=0
        while True:
            page=e.preview(self.root,'huge.log',offset,1000);pages.append(page['text'])
            self.assertLessEqual(len(page['text']),1000);self.assertIsNone(page['tokens'])
            if page['next_offset'] is None:break
            offset=page['next_offset']
        self.assertEqual(''.join(pages),text)

    def test_dependency_not_silently_reimplemented(self):
        self.assertEqual(e.check_receipt(self.root,self.root/'absent.json')['status'],'UNAVAILABLE')


if __name__=='__main__':unittest.main()
