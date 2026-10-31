"""Independent v2 fixtures; never regrade frozen M2 answers."""
import sys
from pathlib import Path
import unittest
import tempfile
import json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'agents/Codex/evaluation'))
import citation_v2 as v


class CitationV2Tests(unittest.TestCase):
    def setUp(self):
        self.text='def begin():\r\n    return "begin original result"\r\n\r\ndef finish():\r\n    return "finish original result"\r\n'
        self.sources={'source.py':self.text,'notes.md':'Original readable observation text.'}
        self.oracle=dict(required_source='source.py',reuse_decision='RE_CONFIRM')
        self.quote='return "finish original result"'

    def run_case(self,citation=None,**kwargs):
        return v.evaluate(dict(reuse_decision='RE_CONFIRM',evidence=[citation if citation is not None else dict(source='source.py',quote=self.quote)]),self.sources,self.oracle,**kwargs)

    def codes(self,result):return [p['code'] for p in result['problems']]

    def test_exact_symbol_and_raw_match(self):
        r=self.run_case(dict(source='source.py',quote=self.quote,symbol='finish'))
        self.assertEqual(r['mechanical_quality'],'PASS');self.assertEqual(r['problems'],[])
        self.assertTrue(r['citations'][0]['raw_match'])
        self.assertEqual(r['citations'][0]['position_check'],'PERFORMED_MATCH')

    def test_absent_locator_and_semantics_are_unperformed(self):
        r=self.run_case()
        self.assertEqual(r['citations'][0]['position_check'],'NOT_PERFORMED')
        self.assertEqual(r['semantic_review'],'NOT_PERFORMED');self.assertEqual(r['acceptance'],'REVIEW_REQUIRED')

    def test_normalization_is_opt_in_and_preserves_raw_failure(self):
        c=dict(source='source.py',quote='def finish():\n    return "finish original result"',lines=[4,5])
        self.assertIn('QUOTE_NOT_FOUND',self.codes(self.run_case(c)))
        r=self.run_case(c,normalize_crlf=True)
        self.assertEqual(r['problems'],[]);self.assertFalse(r['citations'][0]['raw_match'])
        self.assertTrue(r['citations'][0]['normalized_match'])
        self.assertEqual(r['citations'][0]['position_check'],'PERFORMED_MATCH')

    def test_unknown_source_not_in_noncontainment_denominator(self):
        r=self.run_case(dict(source='source.py: finish',quote=self.quote))
        self.assertIn('SOURCE_UNKNOWN',self.codes(r));self.assertNotIn('QUOTE_NOT_FOUND',self.codes(r))
        self.assertIsNone(r['unsupported_citation_rate']);self.assertEqual(r['literal_unchecked'],1)

    def test_position_conflict_is_independent_from_literal(self):
        r=self.run_case(dict(source='source.py',quote=self.quote,symbol='begin'))
        self.assertEqual(r['mechanical_quality'],'PASS')
        self.assertIn('LOCATOR_CONFLICT',self.codes(r))
        self.assertEqual(r['citations'][0]['position_check'],'PERFORMED_CONFLICT')

    def test_bad_shapes_fail_without_crashing(self):
        for answer in (None,[],{},dict(evidence='bad'),dict(evidence=[]),dict(evidence=[None]),dict(evidence=[[]]),dict(evidence=[dict(source=[],quote='long enough quotation')])):
            with self.subTest(answer=answer):
                r=v.evaluate(answer,self.sources,self.oracle)
                self.assertEqual(r['mechanical_quality'],'FAIL')

    def test_bad_quote_types_and_short_and_missing(self):
        for value,code in ((None,'QUOTE_NOT_STRING'),([], 'QUOTE_NOT_STRING'),('return','QUOTE_TOO_SHORT'),('return "finish altered result"','QUOTE_NOT_FOUND')):
            with self.subTest(value=value):self.assertIn(code,self.codes(self.run_case(dict(source='source.py',quote=value))))

    def test_invalid_line_and_symbol_locators(self):
        for locator in (dict(lines=[5,4]),dict(lines=[1,99]),dict(symbol='missing')):
            with self.subTest(locator=locator):self.assertIn('LOCATOR_UNRESOLVED',self.codes(self.run_case(dict(source='source.py',quote=self.quote,**locator))))

    def test_locator_schema_violations_fail_mechanical_quality(self):
        for locator in (dict(lines=[True,5]),dict(lines=[0,4]),dict(lines='4,5'),dict(lines=[1]),
                        dict(lines=[1,2.0]),dict(lines=[-1,2]),dict(symbol=''),dict(symbol=['finish']),dict(symbol=None)):
            with self.subTest(locator=locator):
                r=self.run_case(dict(source='source.py',quote=self.quote,**locator))
                self.assertEqual(r['mechanical_quality'],'FAIL')
                self.assertIn('CITATION_TYPE_INVALID',self.codes(r))
                self.assertEqual(r['citations'][0]['position_check'],'NOT_PERFORMED')

    def test_invalid_locator_does_not_hide_other_diagnostics(self):
        for source in ('unknown.py','source.py'):
            with self.subTest(source=source):
                r=self.run_case(dict(source=source,quote=self.quote,symbol=[]))
                self.assertEqual(r['mechanical_quality'],'FAIL')
                self.assertIn('CITATION_TYPE_INVALID',self.codes(r))
                if source=='unknown.py':
                    self.assertIn('SOURCE_UNKNOWN',self.codes(r))
                    self.assertEqual(r['literal_unchecked'],1)
                else:
                    self.assertTrue(r['citations'][0]['raw_match'])
                    self.assertEqual(r['literal_checked'],1)
                self.assertEqual(r['citations'][0]['position_check'],'NOT_PERFORMED')

    def test_physical_lines_match_ast_with_non_newline_separators(self):
        for prefix in ('x=1\n\x0c','x="a\u2028b"\n','x="a\u0085b"\n','x="a\u2029b"\n'):
            for ending in ('\n','\r\n','\r'):
                with self.subTest(prefix=repr(prefix),ending=repr(ending)):
                    text=(prefix+'def finish():\n    '+self.quote+'\n').replace('\n',ending)
                    answer=dict(reuse_decision='RE_CONFIRM',evidence=[dict(source='source.py',quote=self.quote,symbol='finish',lines=[2,3])])
                    r=v.evaluate(answer,{'source.py':text},self.oracle)
                    self.assertEqual(r['citations'][0]['position_check'],'PERFORMED_MATCH')

    def test_crlf_counts_as_one_line_and_quote_stays_raw(self):
        for ending in ('\n','\r\n','\r'):
            with self.subTest(ending=repr(ending)):
                text=('def finish():\n    '+self.quote+'\n').replace('\n',ending)
                answer=dict(reuse_decision='RE_CONFIRM',evidence=[dict(source='source.py',quote=self.quote,symbol='finish',lines=[2,2])])
                r=v.evaluate(answer,{'source.py':text},self.oracle)
                self.assertEqual(r['citations'][0]['position_check'],'PERFORMED_MATCH')
                self.assertTrue(r['citations'][0]['raw_match'])

    def test_symbol_and_lines_must_intersect(self):
        r=self.run_case(dict(source='source.py',quote=self.quote,symbol='finish',lines=[1,2]))
        self.assertIn('LOCATOR_CONFLICT',self.codes(r))

    def test_duplicate_quotes_count_and_ambiguous_symbols(self):
        sources={'source.py':self.text+self.text}
        r=v.evaluate(dict(reuse_decision='RE_CONFIRM',evidence=[dict(source='source.py',quote=self.quote,symbol='finish')]),sources,self.oracle)
        self.assertEqual(len(r['citations'][0]['raw_occurrences']),2)
        self.assertIn('LOCATOR_UNRESOLVED',self.codes(r))

    def test_presented_scope_is_not_inferred_from_full_source(self):
        r=self.run_case(presented_sources={'source.py':self.text.split('\r\n\r\n')[0]})
        self.assertEqual(r['citations'][0]['presented_scope'],'PERFORMED_CONFLICT')
        self.assertEqual(r['mechanical_quality'],'PASS')

    def test_contract_fails_before_evaluation_and_enum_is_exact(self):
        s=v.validate_contract(self.sources,self.oracle)
        self.assertEqual(set(s['properties']['evidence']['items']['properties']['source']['enum']),set(self.sources))
        with self.assertRaises(ValueError):v.evaluate({},self.sources,dict(required_source='missing',reuse_decision='RE_CONFIRM'))

    def test_overexecution_fails_mechanical_decision(self):
        r=v.evaluate(dict(reuse_decision='RE_EXECUTE',evidence=[dict(source='source.py',quote=self.quote)]),self.sources,self.oracle)
        self.assertIn('REUSE_DECISION_MISMATCH',self.codes(r));self.assertEqual(r['mechanical_quality'],'FAIL')

    def test_no_fuzzy_width_or_trailing_space_repair(self):
        for quote in (self.quote+'   ',self.quote.replace('return','ｒｅｔｕｒｎ')):
            self.assertIn('QUOTE_NOT_FOUND',self.codes(self.run_case(dict(source='source.py',quote=quote),normalize_crlf=True)))

    def test_derived_output_is_new_and_retains_exact_inputs(self):
        answer=dict(reuse_decision='RE_CONFIRM',evidence=[dict(source='source.py',quote=self.quote)])
        with tempfile.TemporaryDirectory() as temp:
            first=v.write_derived(temp,answer,self.sources,self.oracle)
            path=Path(temp)/first['path'];raw=path.read_bytes()
            second=v.write_derived(temp,answer,self.sources,self.oracle)
            self.assertNotEqual(first['path'],second['path']);self.assertEqual(path.read_bytes(),raw)
            bundle=json.loads(raw)
            self.assertEqual(bundle['sources'],self.sources)
            self.assertEqual(bundle['schema'],v.schema(self.sources))
            self.assertTrue(first['path'].startswith('.harness-runtime/derived/'))


if __name__=='__main__':unittest.main()
