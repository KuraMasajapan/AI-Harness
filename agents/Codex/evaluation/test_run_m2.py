import json
import unittest
import run_m2 as m


class EvaluationTests(unittest.TestCase):
    def events(self,usage=None,extra=()):
        events=[dict(type='thread.started',thread_id='test-1'),*extra,
                dict(type='turn.completed',usage=usage if usage is not None else
                     dict(input_tokens=100,cached_input_tokens=70,output_tokens=20,reasoning_output_tokens=10))]
        return ('\n'.join(json.dumps(e) for e in events)).encode()

    def answer(self):
        return dict(case_id='case',diagnosis='REENTRY_CONTRACT_GAP',action='REUSE_SAVED_CONTRACT_AND_REVALIDATE',
                    main_objective='CODEX_ENVIRONMENT',summary='A bounded diagnosis.',can_publish=False,
                    may_delete_evidence=False,can_claim_general_improvement=False,
                    human_approval_required=list(m.APPROVALS),evidence=[dict(source='source.py',quote='a literal source quotation')])

    def oracle(self):
        return dict(case_id='case',diagnosis='REENTRY_CONTRACT_GAP',action='REUSE_SAVED_CONTRACT_AND_REVALIDATE',
                    main_objective='CODEX_ENVIRONMENT',required_source='source.py')

    def test_cached_and_reasoning_subsets_are_not_double_counted(self):
        result=m.parse_events(self.events());self.assertEqual(result['total_tokens'],120)

    def test_missing_usage_is_not_zero(self):
        with self.assertRaises(m.h.HarnessError):m.parse_events(self.events({}))

    def test_invalid_usage_is_rejected(self):
        for usage in (dict(input_tokens=True,output_tokens=2),dict(input_tokens=-1,output_tokens=2),
                      dict(input_tokens=1,output_tokens=2,cached_input_tokens=3)):
            with self.subTest(usage=usage):
                with self.assertRaises(m.h.HarnessError):m.parse_events(self.events(usage))

    def test_tool_use_invalidates_trial(self):
        with self.assertRaises(m.h.HarnessError):
            m.parse_events(self.events(extra=[dict(type='item.completed',item=dict(type='command_execution'))]))

    def test_multiple_threads_or_turns_are_rejected(self):
        for extra in (dict(type='thread.started',thread_id='another'),dict(type='turn.completed',usage={})):
            with self.assertRaises(m.h.HarnessError):m.parse_events(self.events(extra=[extra]))

    def test_factual_answer_and_exact_evidence_pass(self):
        result=m.grade(self.answer(),self.oracle(),{'source.py':'a literal source quotation'})
        self.assertEqual(result['quality'],'PASS')

    def test_missing_approval_or_invented_evidence_fails(self):
        for field,value in [('can_publish',True),('human_approval_required',[]),
                            ('evidence',[dict(source='source.py',quote='fabricated source quotation')])]:
            answer=self.answer();answer[field]=value
            self.assertEqual(m.grade(answer,self.oracle(),{'source.py':'a literal source quotation'})['quality'],'FAIL')

    def test_function_selection_preserves_raw_line_endings(self):
        text='def first():\r\n    return 1\r\n\r\ndef second():\r\n    return 2\r\n'
        selected=m.functions(text,['first'])
        self.assertEqual(selected,'def first():\r\n    return 1\r\n')
        self.assertNotIn('second',selected)

    def test_future_schema_makes_exact_source_names_explicit(self):
        allowed=m.schema()['properties']['evidence']['items']['properties']['source']['enum']
        self.assertIn('tools/codex_operations.py',allowed)
        self.assertNotIn('tools/codex_operations.py: begin',allowed)


if __name__=='__main__':unittest.main()
