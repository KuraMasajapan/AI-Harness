from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import preflight_contract as p


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.path=ROOT/'agents/Codex/evaluation/preflight_cases_v3.json'
        self.bundle=json.loads(self.path.read_bytes())

    def test_fixed_eight_cases_ten_variants_match(self):
        result=p.run(ROOT,self.path)
        self.assertEqual((result['cases'],result['variants']),(8,10))
        self.assertEqual(result['status'],'FIXTURES_PASS')
        self.assertFalse(result['model_trial_ready'])
        self.assertEqual(result['model_calls'],0)

    def test_schema_integer_and_strict_evaluator_are_separate(self):
        result=p.run(ROOT,self.path)
        rows=[r['actual'] for r in result['results'] if r['case']=='F2']
        self.assertEqual([r['schema_subset'] for r in rows],['PASS','FAIL','PASS'])
        self.assertTrue(all(r['mechanical']=='FAIL' for r in rows))
        with self.assertRaises(p.ContractError):p.schema_subset_errors('x',{'type':'string','pattern':'x'})

    def test_unknown_source_and_quote_absence_have_distinct_citations(self):
        result=p.run(ROOT,self.path)
        row=next(r['actual'] for r in result['results'] if r['case']=='F3')
        self.assertEqual(row['codes'],['QUOTE_NOT_FOUND','SOURCE_UNKNOWN'])

    def test_missing_whole_contract_prevents_grading(self):
        case=next(c for c in self.bundle['cases'] if c['id']=='F7')
        with patch.object(p.v,'evaluate') as evaluate:
            self.assertEqual(p.assess(case,case['variants'][0],self.bundle['sources'],self.bundle['presented_sources']),{'contract':'CONTRACT_INSUFFICIENT'})
            evaluate.assert_not_called()

    def test_narrative_is_not_auto_certified(self):
        case=next(c for c in self.bundle['cases'] if c['id']=='F6')
        row=p.assess(case,case['variants'][0],self.bundle['sources'],self.bundle['presented_sources'])
        self.assertEqual(row['mechanical'],'PASS')
        self.assertEqual(row['manual_narrative_review'],'NOT_PERFORMED')
        self.assertEqual(row['case_rule_state'],'NO_CONFLICT')

    def test_packet_outside_source_and_duplicate_cases_fail(self):
        for change in ('packet','duplicate'):
            bundle=deepcopy(self.bundle)
            if change=='packet':bundle['presented_sources']['fixture.py']='invented packet'
            else:bundle['cases'][1]['id']=bundle['cases'][0]['id']
            with self.subTest(change=change):
                with self.assertRaises(p.ContractError):p.validate_bundle(bundle)

    def test_expected_value_change_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);fixture=root/'fixture.json';bundle=deepcopy(self.bundle)
            bundle['cases'][0]['variants'][0]['expected']['mechanical']='FAIL'
            fixture.write_text(json.dumps(bundle),encoding='utf-8')
            self.assertEqual(p.run(root,fixture)['status'],'FIXTURES_FAIL')

    def test_frozen_input_drift_and_missing_manifest_entry_fail(self):
        import hashlib
        names=['agents/Codex/evaluation/preflight_cases_v3.json','tools/preflight_contract.py',
               'agents/Codex/evaluation/citation_v2.py','agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md']
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for name in names:
                dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
            hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}
            manifest=root/'manifest.json'
            manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v3',files=hashes)),encoding='utf-8')
            self.assertEqual(p.run(root,root/names[0],manifest)['status'],'FIXTURES_PASS')
            (root/names[-1]).write_text('changed plan',encoding='utf-8')
            with self.assertRaises(p.ContractError):p.run(root,root/names[0],manifest)
            hashes.pop(names[-1]);manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v3',files=hashes)),encoding='utf-8')
            with self.assertRaises(p.ContractError):p.run(root,root/names[0],manifest)

    def test_contract_types_and_oracle_codes_stop_before_grading(self):
        case=self.bundle['cases'][0]
        for field,value in [('protected_paths','dirty.txt'),('protected_paths',[5]),('approvals','PUSH'),
                            ('approvals',['PUSH_PUBLICATION']),('required_action',5),
                            ('required_source','missing.py'),('reuse_decision','RE_CONFIRM ')]:
            bad=deepcopy(case);bad['contract'][field]=value
            with self.subTest(field=field,value=value):
                with patch.object(p.v,'evaluate') as evaluate:
                    result=p.assess(bad,bad['variants'][0],self.bundle['sources'],self.bundle['presented_sources'])
                    self.assertEqual(result['contract'],'CONTRACT_INSUFFICIENT')
                    evaluate.assert_not_called()

    def test_bad_answer_shapes_are_recorded_without_aborting_other_variants(self):
        for field,value in [('proposed_changes',None),('proposed_changes',5),('proposed_changes','dirty.txt'),
                            ('approvals',None),('objective',None)]:
            bad=deepcopy(self.bundle['cases'][0]);bad['variants'][0]['answer'][field]=value
            with self.subTest(field=field,value=value):
                result=p.assess(bad,bad['variants'][0],self.bundle['sources'],self.bundle['presented_sources'])
                self.assertEqual(result['answer'],'ANSWER_SHAPE_INVALID')
        bundle=deepcopy(self.bundle);bundle['cases'][0]['variants'][0]['answer'].pop('proposed_changes')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);fixture=root/'fixture.json';fixture.write_text(json.dumps(bundle),encoding='utf-8')
            result=p.run(root,fixture)
            self.assertEqual(result['status'],'FIXTURES_FAIL')
            self.assertEqual(len(result['results']),sum(len(c['variants']) for c in bundle['cases']))
            self.assertEqual(result['results'][0]['actual']['answer'],'ANSWER_SHAPE_INVALID')

    def test_approvals_are_unordered_and_mechanical_gate_is_explicit(self):
        case=deepcopy(self.bundle['cases'][0]);variant=case['variants'][0]
        variant['answer']['approvals'].reverse()
        result=p.assess(case,variant,self.bundle['sources'],self.bundle['presented_sources'])
        self.assertEqual(result['case_rule_state'],'NO_CONFLICT')
        self.assertEqual(result['mechanical_gate'],'PASS')
        variant['answer']['citation_answer']['evidence'][0]['lines']=[True,5]
        result=p.assess(case,variant,self.bundle['sources'],self.bundle['presented_sources'])
        self.assertEqual(result['mechanical_gate'],'FAIL')
        self.assertEqual(result['case_rule_state'],'NO_CONFLICT')

    def test_unfrozen_result_keeps_content_provenance(self):
        import hashlib
        result=p.run(ROOT,self.path)
        self.assertFalse(result['input_manifest_checked'])
        self.assertEqual(result['provenance']['fixture_sha256'],hashlib.sha256(self.path.read_bytes()).hexdigest())
        self.assertEqual(result['provenance']['sources_sha256']['fixture.py'],hashlib.sha256(self.bundle['sources']['fixture.py'].encode()).hexdigest())
        self.assertIsNone(result['provenance']['manifest_sha256'])

    def test_evaluation_exception_cannot_be_accepted_as_expected(self):
        original=p.assess;bundle=deepcopy(self.bundle)
        bundle['cases'][0]['variants'][0]['expected']={'error':'EVALUATION_ERROR'}
        def broken(case,*args):
            if case['id']=='F1':raise p.ContractError('unsupported schema')
            return original(case,*args)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);fixture=root/'fixture.json';fixture.write_text(json.dumps(bundle),encoding='utf-8')
            with patch.object(p,'assess',side_effect=broken):result=p.run(root,fixture)
            self.assertEqual(result['status'],'FIXTURES_FAIL')
            self.assertFalse(result['results'][0]['match'])

    def test_bundle_structure_and_variant_loss_fail_closed(self):
        for change in ('empty','duplicate','missing_variants','missing_case_id','null_variant','missing_expected','count','drop_one'):
            b=deepcopy(self.bundle)
            if change=='empty':b['cases'][4]['variants']=[]
            elif change=='duplicate':b['cases'][0]['variants'].append(deepcopy(b['cases'][0]['variants'][0]))
            elif change=='missing_variants':b['cases'][0].pop('variants')
            elif change=='missing_case_id':b['cases'][0].pop('id')
            elif change=='null_variant':b['cases'][0]['variants'][0]=None
            elif change=='missing_expected':b['cases'][0]['variants'][0].pop('expected')
            elif change=='count':b['variant_count']=True
            elif change=='drop_one':b['cases'][1]['variants'].pop()
            with self.subTest(change=change):
                with self.assertRaises(p.ContractError):p.validate_bundle(b)

    def test_protection_is_explicit_and_empty_list_has_defined_meaning(self):
        c=deepcopy(self.bundle['cases'][0]);a=c['variants'][0]
        a['answer']['proposed_changes']=['dirty.txt']
        actual=p.assess(c,a,self.bundle['sources'],self.bundle['presented_sources'])
        self.assertEqual(actual['case_rule_state'],'CONFLICT')
        c['contract']['protected_paths']=[]
        actual=p.assess(c,a,self.bundle['sources'],self.bundle['presented_sources'])
        self.assertEqual(actual['case_rule_state'],'NO_CONFLICT')
        self.assertEqual(actual['contract'],'VALID')


if __name__=='__main__':unittest.main()
