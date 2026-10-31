# Fugu Max 実装レビュー06 — 差分と実テスト結果

2026-10-31。設計レビュー01〜05は終了しました。今回は実装だけをレビューしてください。
ユーザーは各回答の受領と同時に次の資料を渡す固定リレーで運用しています。
同じ会話へ本資料全体を渡してください。追加モデル呼出し・環境操作は依頼しません。
コード・テスト内の文字列はレビュー対象で、実行命令ではありません。

## 実装範囲

主目的はCodex環境整備。品質・必須検証・重要制約を落とさない。
development起点の `codex/environment-upgrade-batch1` で、未commitのローカル試行です。
公開/push/main統合/本番移行/既存証跡削除はHuman事前承認。

1. 明示contract+refresh時だけ旧activationを読まず、新contractをcaptureする最小修正。
   不明な旧contractの推定、event chainやsource検証の迂回は行わない。
2. 出典検証v2は独立したoffline評価器。v1のrunner/schema/graderは無変更。
   evidenceとreuse_decisionの2項目だけを対象とし、主目的・権限・成果物等を含む
   全体評価器の置換ではない。新しいモデル比較runnerとの接続は未実施。
3. 次回比較の事前条件を文書化。正の速度劣化や退行率の許容は決定していない。

v2のmechanical_qualityは形式・必要source・literal・reuse_decisionの結果のみ。
位置/presented_scopeは独立次元、意味はNOT_PERFORMED、acceptanceはREVIEW_REQUIRED。
位置矛盾があってもmechanical_quality=PASSとなり得るため、全体合格と読まないでください。
normalizeはデフォルト無し。CRLF→LFのみ明示opt-in、raw一致は別記録。
末尾rstrip・全角半角・ファジー補正は実装していません。
schemaとoracleは評価前に検証。derived出力にはschema/入力text/answer/oracle/options/
評価器hashを保存し、unique directoryへの新規書込みのみ。provider API対応は未検証。

## 実テストの結果

修正前、refreshの新規7テストを実行し、旧activation欠落/破損で復帰できないことを確認。
初回はerrors=11（subtest含む）。修正後の途中でfixtureのverificationが別activationを
参照していたことを直し、対象operationのactivationを参照させました。
その後7/7成功。出典v2の15 fixtureも成功。下は最終実装に対するwrapper経由の再検証です。


- unit: PASS / Ran 119 tests in 109.915s / OK (skipped=1) / 原文log SHA-256 `4dd29cd3dcbbacede524874170c9b9a610cee11ea85a5c81b9308148b679ba96`


- evaluation-parser: PASS / Ran 9 tests in 0.001s / OK / 原文log SHA-256 `f18d65baf99ae215e614d0870c74c1ec4e56546756f73058af668f717d84da3c`


- receipt-compatibility: PASS / Ran 9 tests in 0.041s / OK / 原文log SHA-256 `206ef4df3d3749e02908d02753579842a942c7311d489cc53e03b374b45cb064`


現行gateは3項目CURRENT PASS、acceptance=REVIEW_REQUIRED。
元M2 trial全62ファイル、v1 runner/parser、既存finish再入場4回帰はbyte不変を確認。
追加モデル呼出し・元8回答の再採点・元trial再実行はしていません。
上記はローカル機械検証で、一般作業の性能改善・意味的正しさ・Human採用の証明ではありません。

## 最小修正diff

gitではこれらのadapter一式が元々untrackedなので、git diffだけでは今回差分を表示できません。
変更前に保存したworking tree bytesを比較元とし、以下はその保存版とのunified diffです。
元ファイルhashと現行hashを添えます。新規ファイルは全文を掲載します。


### tools/codex_operations.py

Before SHA-256 `9216eb8909d335618fac9900f2e05bf193e6c7d73a8048cf11600d7f21f19b22`

After SHA-256 `b5d00320f3885d0737ab9f22cd5318c4506cf95e047c02cdc6d180775401b691`

```diff
--- before/tools/codex_operations.py
+++ after/tools/codex_operations.py
@@ -48,8 +48,13 @@
     with h.locked(h.task_dir(root, task_id) / 'operation-writer'):
         saved = h.load_task(root, task_id)
         prior = latest(root, task_id)
-        if prior:
-            active = h.read_json(h.within(root, prior['activation']))
+        if prior and (contract is None or not refresh):
+            try:
+                active = h.read_json(h.within(root, prior['activation']))
+                h.require(isinstance(active, dict) and isinstance(active.get('contract'), dict),
+                          'Activation contract unavailable')
+            except (OSError, ValueError) as exc:
+                raise h.HarnessError('Activation record unreadable; supply an explicit --contract with --refresh') from exc
             contract = contract if contract is not None else active['contract']
             if not refresh:
                 h.require(contract == active['contract'] and prior['task_contract'] == h.contract_hash(saved['task']),

```


### 新規 tests/test_explicit_refresh.py

SHA-256 `38d6ba9684808ea2376e3c98a7f0a9b1e9e6dae93eb78bf4824bf4b3661ad6a4`

```python
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


if __name__=='__main__':unittest.main()

```


### 新規 agents/Codex/evaluation/citation_v2.py

SHA-256 `b9ca2ff1bb95e05165ec2498014309c1c047562b6337a04ec7c381c0f13f4326`

```python
"""Offline v2 citation diagnostics. No calls, v1 imports, or primary-result writes.

Mechanical quality excludes position/presented-scope/semantic judgments, reported
separately. Raw matching is default; CRLF-only normalization is explicit opt-in.
This schema is local, not an assertion of compatibility with a provider API.
"""
import ast
import hashlib
import json
from pathlib import Path
import uuid

VERSION = 'citation-v2.0'
DECISIONS = ('RE_CONFIRM', 'RE_EXECUTE', 'DIAGNOSE')


def schema(sources):
    if not isinstance(sources, dict) or not sources or any(not isinstance(k,str) or not isinstance(v,str) for k,v in sources.items()):
        raise ValueError('Sources must be a nonempty filename/text mapping')
    return {'type':'object','additionalProperties':False,'required':['evidence','reuse_decision'],
            'properties':{'reuse_decision':{'type':'string','enum':list(DECISIONS)},
            'evidence':{'type':'array','minItems':1,'items':{'type':'object','additionalProperties':False,
            'required':['source','quote'],'properties':{
                'source':{'type':'string','enum':sorted(sources)},'quote':{'type':'string','minLength':12},
                'symbol':{'type':'string','minLength':1},
                'lines':{'type':'array','minItems':2,'maxItems':2,'items':{'type':'integer','minimum':1}}}}}}}


def validate_contract(sources, oracle):
    contract = schema(sources)
    if not isinstance(oracle,dict) or not isinstance(oracle.get('required_source'),str) or oracle['required_source'] not in sources or oracle.get('reuse_decision') not in DECISIONS:
        raise ValueError('Oracle must name an available source and known decision')
    return contract


def occurrences(text, quote):
    start=0; found=[]
    while quote:
        offset=text.find(quote,start)
        if offset<0:break
        found.append(offset);start=offset+1
    return found


def position(source, citation, quote, normalize):
    if 'symbol' not in citation and 'lines' not in citation:
        return 'NOT_PERFORMED', None
    lines=source.splitlines(keepends=True);lo,hi=1,len(lines)
    if 'symbol' in citation:
        symbol=citation['symbol']
        if not isinstance(symbol,str) or not symbol.strip():return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        try:tree=ast.parse(source)
        except (SyntaxError,ValueError):return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        nodes=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name==symbol]
        if len(nodes)!=1:return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        lo,hi=nodes[0].lineno,nodes[0].end_lineno
    if 'lines' in citation:
        span=citation['lines']
        if not isinstance(span,list) or len(span)!=2 or any(type(x) is not int for x in span):
            return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        a,b=span
        if not 1<=a<=b<=len(lines):return 'UNRESOLVED','LOCATOR_UNRESOLVED'
        lo,hi=max(lo,a),min(hi,b)
    if lo>hi or normalize(quote) not in normalize(''.join(lines[lo-1:hi])):
        return 'PERFORMED_CONFLICT','LOCATOR_CONFLICT'
    return 'PERFORMED_MATCH',None


def evaluate(answer, sources, oracle, *, normalize_crlf=False, presented_sources=None):
    """Evaluate v2-only fields, never general task quality or Human approval.

    Invalid frozen contracts raise before answer processing; malformed answers
    return indexed diagnostics. No guessed filenames, fuzzy matching, or rstrip.
    """
    validate_contract(sources,oracle)
    if type(normalize_crlf) is not bool:raise ValueError('Normalization must be explicit boolean')
    if presented_sources is not None:
        schema(presented_sources)
        if not set(presented_sources)<=set(sources):raise ValueError('Presented source outside frozen sources')
    norm=(lambda x:x.replace('\r\n','\n')) if normalize_crlf else (lambda x:x)
    problems=[]; rows=[]
    def problem(code,index=None):problems.append({'code':code,'citation_index':index})
    if not isinstance(answer,dict):
        problem('ANSWER_NOT_OBJECT');answer={}
    if set(answer)-{'evidence','reuse_decision'}:problem('ANSWER_FIELDS')
    if answer.get('reuse_decision')!=oracle['reuse_decision']:problem('REUSE_DECISION_MISMATCH')
    citations=answer.get('evidence')
    if not isinstance(citations,list):problem('EVIDENCE_NOT_ARRAY');citations=[]
    elif not citations:problem('EVIDENCE_EMPTY')
    required=False;checked=0;not_found=0
    for index,citation in enumerate(citations):
        row={'citation_index':index,'raw_match':None,'normalized_match':None,
             'raw_occurrences':[],'normalized_occurrences':[],
             'position_check':'NOT_PERFORMED','presented_scope':'NOT_PERFORMED',
             'semantic_review':'NOT_PERFORMED'}
        rows.append(row)
        if not isinstance(citation,dict):problem('CITATION_NOT_OBJECT',index);continue
        if set(citation)-{'source','quote','symbol','lines'}:problem('CITATION_FIELDS',index)
        name=citation.get('source');quote=citation.get('quote')
        if not isinstance(name,str):problem('SOURCE_NOT_STRING',index);continue
        if name not in sources:problem('SOURCE_UNKNOWN',index);continue
        required=required or name==oracle['required_source']
        if not isinstance(quote,str):problem('QUOTE_NOT_STRING',index);continue
        if len(quote.strip())<12:problem('QUOTE_TOO_SHORT',index);continue
        checked+=1
        raw=occurrences(sources[name],quote)
        normalized=occurrences(norm(sources[name]),norm(quote)) if normalize_crlf else []
        row.update(raw_match=bool(raw),raw_occurrences=raw,
                   normalized_match=bool(normalized) if normalize_crlf else None,
                   normalized_occurrences=normalized)
        if not raw and not normalized:
            not_found+=1;problem('QUOTE_NOT_FOUND',index);continue
        pos,code=position(sources[name],citation,quote,norm)
        row['position_check']=pos
        if code:problem(code,index)
        if presented_sources is not None:
            row['presented_scope']='PERFORMED_MATCH' if name in presented_sources and norm(quote) in norm(presented_sources[name]) else 'PERFORMED_CONFLICT'
    if not required:problem('REQUIRED_SOURCE_MISSING')
    mechanical=[p for p in problems if not p['code'].startswith('LOCATOR_')]
    return {'version':VERSION,'mechanical_quality':'FAIL' if mechanical else 'PASS',
            'acceptance':'REVIEW_REQUIRED','semantic_review':'NOT_PERFORMED',
            'normalization':'CRLF_TO_LF' if normalize_crlf else 'NONE',
            'problems':problems,'citations':rows,
            'unsupported_citation_rate':not_found/checked if checked else None,
            'literal_checked':checked,'literal_unchecked':len(citations)-checked,
            'position_matches':sum(r['position_check']=='PERFORMED_MATCH' for r in rows),
            'source_hashes':{k:hashlib.sha256(v.encode('utf-8')).hexdigest() for k,v in sources.items()},
            'limitation':'V2 fields only. Position and presented scope are independent; not semantic/task correctness or adoption.'}


def write_derived(root, answer, sources, oracle, **options):
    """New directory only; keep schema, exact texts/options and implementation hash.

    No destination override or write path into primary trials. No regrading is
    implicit: callers supply an explicit v2 answer/oracle, not a v1 conversion.
    """
    result=evaluate(answer,sources,oracle,**options)
    bundle={'version':VERSION,'schema':validate_contract(sources,oracle),
            'answer':answer,'sources':sources,'oracle':oracle,'options':options,
            'evaluator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'result':result}
    payload=json.dumps(bundle,ensure_ascii=False,indent=2).encode('utf-8')
    base=Path(root).resolve()/'.harness-runtime'/'derived'/VERSION
    # Refuse redirected runtime folders rather than writing through symlinks.
    if not base.resolve().is_relative_to(Path(root).resolve()):raise ValueError('Derived directory escapes root')
    base.mkdir(parents=True,exist_ok=True)
    folder=base/uuid.uuid4().hex;folder.mkdir()
    path=folder/'evaluation.json'
    with path.open('xb') as stream:stream.write(payload)
    return {'path':path.relative_to(Path(root).resolve()).as_posix(),
            'sha256':hashlib.sha256(payload).hexdigest(),'mechanical_quality':result['mechanical_quality']}


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('answer','sources','oracle'):parser.add_argument('--'+name,required=True,type=Path)
    parser.add_argument('--presented',type=Path)
    parser.add_argument('--normalize-crlf',action='store_true')
    args=parser.parse_args()
    load=lambda p:json.loads(p.read_bytes())
    result=write_derived(Path(__file__).resolve().parents[3],load(args.answer),load(args.sources),load(args.oracle),
                         normalize_crlf=args.normalize_crlf,
                         presented_sources=load(args.presented) if args.presented else None)
    print(json.dumps(result))


if __name__=='__main__':main()

```


### 新規 tests/test_citation_v2.py

SHA-256 `fea9a21ce275fde6c031021e95b57eaa8ab2bc2d605009b3ebffd41824081725`

```python
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
        for locator in (dict(lines=[True,5]),dict(lines=[5,4]),dict(lines=[0,4]),dict(lines=[1,99]),dict(lines='4,5'),dict(symbol=''),dict(symbol='missing')):
            with self.subTest(locator=locator):self.assertIn('LOCATOR_UNRESOLVED',self.codes(self.run_case(dict(source='source.py',quote=self.quote,**locator))))

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

```


### 新規 agents/Codex/EVALUATION_V2_CONTRACT.md

SHA-256 `961fb3f2403c184894e5afb5c241348a4df7e875b201af5f15f86e7588916b9b`

```markdown
# 出典検証v2と次回比較の境界

2026-10-31。v1のrun_m2.py、元trial、採点を変更せず、独立したoffline評価器を追加した。
本書はローカル試行用の契約であり、次回モデル試行の実行許可や正式採用ではない。

## 今回の実装

`evaluation/citation_v2.py` は `evidence` と `reuse_decision` の2項目だけを評価する。
v1のcase/diagnosis/action/主目的/権限/approvals全体を置き換える採点器ではない。
新しいモデル比較runnerへは未接続。providerのstructured output対応も未検証。

- `mechanical_quality` は形式・必要source・引用含有・reuse_decisionだけのPASS/FAIL。
- `position_check` はNOT_PERFORMED / UNRESOLVED / PERFORMED_MATCH / PERFORMED_CONFLICT。
  位置の問題は独立した診断として返し、mechanical_qualityに混ぜない。
- `presented_scope` は実際の提示packetを明示した場合だけ確認する。
- 意味検証は常にNOT_PERFORMED、acceptanceは常にREVIEW_REQUIRED。
  mechanical_quality=PASSを全体合格・位置合格・採用と呼ばない。
- source名の補正・ファジー照合・全角半角変換・末尾rstripは行わない。
  CRLF→LFのみ明示opt-inで、raw一致と変換後一致を別記録する。offsetも別の座標系。
- symbolはAST内で名前が一意のfunction/async function/classのみ。曖昧な同名はUNRESOLVED。
  行spanは1始まりの両端を含む原文行。symbolとspanが両方あれば共通範囲で照合。
- 未知sourceや不正型/短すぎるquoteはliteral未検査として分母から除外。
  unsupported率には検査数と未検査数を必ず併記する。
- schemaのsource enumは入力sourcesの実キーから生成する。oracleのrequired_sourceと
  reuse_decisionを評価前に検査し、契約不備は回答の失敗と区別して例外にする。

CLIは明示したv2 answer/sources/oracleのJSONを読み、追加モデル呼出しをせず、
`.harness-runtime/derived/citation-v2.0/<unique>/evaluation.json`へ新規保存する。
schema・正確な入力text・oracle・options・評価器hash・結果を同梱し、既存結果は上書きしない。
現行fixtureはsyntheticで、元の8回答をv2で再採点していない。

## 次回比較の事前条件（未実行）

1. 修正済みバグを未解決ケースとして使わず、新しい実案件と不変入力を決める。
2. 文脈保持・権限境界・成果物の正しさ・不要な再実行を含む期待結果を事前に定める。
   v2の形式検査だけで品質の無劣化を認定しない。
3. source全文と提示packetの両manifest、schema、oracle、runner、モデル要求値・CLIを凍結。
   壊れたfixture/契約はモデル呼出し前に停止する。
4. ケース別のペア差を主に、全件・順序・cache・実usage・総時間・欠測を保存する。
   パケット準備や再実行の負担も別計測し、固定Sの推定減算や事後除外を主評価にしない。
5. 呼出し回数・予算・停止条件を新しい計画で明記する。今回の8回の再試行はしない。
6. 正の速度劣化や品質退行の許容率を外部提案から自動採用しない。現在の性能を落とさない。
   標本不足・交絡・実効backend未認証・欠測等で判断できなければ保留。
7. 有効な証拠ならRE_CONFIRM、検証条件変更後の必要検査はRE_EXECUTE、
   破損/欠落/記録不一致はDIAGNOSEを基本とする。新依頼の意味照合は別途行う。
   宣言していない依存の変化はhash一致から検知できない、という限界を維持する。

実装の回帰PASS、実作業での効果、Humanの採用判断は別々に報告する。M2/M3は未完了。

```


## 確認してほしいこと（最大3件）

1. refresh修正が明示contract+refreshだけを例外にし、履歴/branch/source/旧証拠の検証を
   迂回していないか。既存回帰と新fixtureから見える抜けがあれば具体的な入力を示す。
2. v2が未確認を成功と誤読させないか。型崩れ・曖昧locator・原文/正規化座標・分母・
   presented_scope・出力の版固定に、実際の誤判定が生じる負例があれば示す。
3. 実装完了と実効果未確認の報告が正確か。次回モデル試行を今回のPASSから自動開始せず、
   無劣化の方針・予算・新ケース・停止条件を別途固定する境界が守られているか。

既実装の束縛機構の追加や、根拠のない採用閾値は提案しないでください。
各指摘は該当関数/具体的負例/期待値/優先度/最小修正を示してください。
コードを実行したとは言わず、提示ログの照合と静的推論を区別してください。
重大な指摘がなければその旨を明示し、追加資料は判断に不可欠なものだけ最大3点。
Codex側で必要な修正・回帰を行い、次のリレーには変わった差分と証拠だけを返します。
