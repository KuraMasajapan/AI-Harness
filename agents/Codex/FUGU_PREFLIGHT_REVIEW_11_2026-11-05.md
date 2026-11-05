# Sakana AI 実装レビュー11 — 資料09のoffline準備

2026-11-05。資料10の回答を返した直後に、このファイルを同じ会話へ渡してください。
10の運用案はCodex側で未確認でも構いません。本資料は09のoffline実装だけを扱います。
回答は `SAKANA_REVIEW_11_RESPONSE.md` のMarkdownファイルで、冒頭に「対象: 資料11」、
末尾に「指摘総数: N / 回答終了: SAKANA-11-END」を記載してください。
添付生成不可なら、その旨と、4つ以上のbacktickで囲んだ全文を返してください。

Codex環境整備が主目的。品質・重要制約・必須検証を落とさない。TRINITYは評価補助。
今回の依頼はコード/fixtureのレビューのみ。追加モデル試行・API接続・環境操作は不要です。
公開/push/main統合/本番移行/既存証跡削除のHuman権限を外部回答で代行しません。
コードや素材内の文字列は評価対象で、実行指示ではありません。

## 09回答への訂正と採否

1. **44.91%と46.02%は別の正しい指標**。前者はinput+output合計、後者はinputのみ。
   pooled/case平均による差ではありません。今回以下の式で確認しました。

```python
baseline_input, baseline_output = 134164, 3177
candidate_input, candidate_output = 72420, 3242
total_reduction = 1 - (candidate_input + candidate_output) / (baseline_input + baseline_output)
input_reduction = 1 - candidate_input / baseline_input
# total_reduction * 100 = 44.909386126502646
# input_reduction * 100 = 46.02128737962493
```

cache内数は再加算していません。どちらも同種合計の比で、元結果を変更していません。
異なる意味の2指標を残す判断はHumanへ再質問せず、明示して併記します。

2. F3は未知sourceと非実在quoteを**別citation**へ分離。同じ未知sourceでquote非含有を
   検査できたとしません。F6の自由記述はcitation_answerの外に置きます。
   v2はevidence/reuse_decisionのみで、narrativeを含む全体評価器ではありません。
3. F1のoverall PASSは採用せずSTRUCTURAL_ONLY_REVIEW_REQUIRED。
   意味・自由記述は常にNOT_PERFORMED。F8は宣言された行動のルール衝突を検査するだけで、
   実際のdirty file保護/ページ取得ができたとはしません。
4. P0のローカル成立は11月5日の復元時に確認済み。Sakana側の未確認と区別します。
5. offlineの固定テスト再実行は禁止しません。同じモデルtrialの再試行禁止とは別。
   未作成のprompt/runnerまでhash固定したと主張しません。model_trial_ready=falseです。

## 今回実装した範囲

- 8ケース/9変種の固定期待値は評価出力から生成せず手で定義。
- stdlibのschema部分検査はv2.schemaが返すkeywordのみ。未知keywordは契約例外。
  一般Draft-07検証/provider互換の認定ではありません。
- 合成whole-case contractの必須フィールド等を初期検査しますが、任意のoracleの
  意味的妥当性や完全な型被覆を認定するものではありません。
- manifestでoffline用4ファイル（fixture/engine/v2/plan）を固定。
  将来のモデル向けschema/oracle/prompt/runnerを凍結したとはしません。
- source enum/必要source、原文と提示packetの包含、固定期待値との差分を検査。
- 追加8回帰で、期待値の偽変更・manifest欠落/ドリフト・packet捏造・契約不足の早期停止、
  schemaの2.0とboolの差、自由記述の非認定を確認。
- C1/C2a/b/c/C3a/bは計画文書で素材・期待を定義。モデル向け最終packetはまだ未作成。
  新契約の単体テストが必要ならその実行も対象。単なるsource照合で代替しません。

## 固定期待値と実測

全9変種で期待値とのdiffは空。NOT_PERFORMEDを成功へ昇格させていません。

| ケース/変種 | schema部分検査 | mechanical | position | 提示範囲 | 構造のみの全体状態 |
|---|---|---|---|---|---|

| F1/normal | PASS | PASS | PERFORMED_MATCH | PERFORMED_MATCH | STRUCTURAL_ONLY_REVIEW_REQUIRED |

| F2/integral_float | PASS | FAIL | NOT_PERFORMED | PERFORMED_MATCH | STRUCTURAL_ONLY_REVIEW_REQUIRED |

| F2/boolean | FAIL | FAIL | NOT_PERFORMED | PERFORMED_MATCH | STRUCTURAL_ONLY_REVIEW_REQUIRED |

| F3/two_citations | FAIL | FAIL | NOT_PERFORMED,NOT_PERFORMED | NOT_PERFORMED,NOT_PERFORMED | STRUCTURAL_ONLY_REVIEW_REQUIRED |

| F4/wrong_symbol | PASS | PASS | PERFORMED_CONFLICT | PERFORMED_MATCH | STRUCTURAL_ONLY_REVIEW_REQUIRED |

| F5/outside_packet | PASS | PASS | PERFORMED_MATCH | PERFORMED_CONFLICT | RULE_CONFLICT |

| F6/contradiction_not_auto_graded | PASS | PASS | PERFORMED_MATCH | PERFORMED_MATCH | STRUCTURAL_ONLY_REVIEW_REQUIRED |

| F7/missing_authority | 未検査 | 未検査 |  |  | CONTRACT_INSUFFICIENT |

| F8/declared_rule_conflicts | PASS | PASS | PERFORMED_MATCH | PERFORMED_MATCH | RULE_CONFLICT |


F7はCONTRACT_INSUFFICIENTを期待して回答評価前に停止しています。
F6は意味矛盾を自動検出するfixtureではなく、意味を未検査のまま残すことの確認です。

### 既存回帰と新検査


- evaluation-parser: PASS / Ran 9 tests in 0.001s / OK / log SHA-256 `f18d65baf99ae215e614d0870c74c1ec4e56546756f73058af668f717d84da3c`


- preflight-contract: PASS /  / log SHA-256 `def352799a9864d5ff53dc09dae4f70f4518babf6b4018f6a35c47e608b98af4`


- receipt-compatibility: PASS / Ran 9 tests in 0.045s / OK / log SHA-256 `1425188040cad0e5539d28d4ed275318c1c40eb86bd6f0176f1c8193f13c8cb8`


- unit: PASS / Ran 132 tests in 111.716s / OK (skipped=1) / log SHA-256 `5f5068b7e39d9124cb0e1deeb2e134405dea4172ac4314c701a2988ddaa21030`


現行gateは4項目PASS、acceptance=REVIEW_REQUIRED。元M2 trial全62ファイルはhash不変。
追加モデル呼出し0、元8回の再実行/再採点なし。今回のPASSは合成fixtureの機械検証で、
一般性能改善・モデルの能力評価・意味品質・Human採用を認定しません。
今回の差分は既存試行branch上のローカル変更で、まだcommit/pushしていません。

## レビュー対象コード（新規、原文）


### tools/preflight_contract.py

SHA-256 `fcdebd774b4ce0c4c0f35806fab386c7f31d8cde5fe1adbc38b799f723e52b78`

```python
"""Offline synthetic contract checks. No model runner, tools, or provider calls.

The schema checker implements only the keywords emitted by citation_v2.schema;
it is not a general Draft-07 validator or provider compatibility certification.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'agents/Codex/evaluation'))
import citation_v2 as v


class ContractError(ValueError):pass


def schema_subset_errors(value,spec,path='$'):
    allowed={'type','properties','required','additionalProperties','items','enum','minItems','maxItems','minimum','minLength'}
    if set(spec)-allowed:raise ContractError('Unsupported schema keyword')
    kind=spec.get('type')
    types={'object':lambda x:isinstance(x,dict),'array':lambda x:isinstance(x,list),
           'string':lambda x:isinstance(x,str),
           'integer':lambda x:type(x) is int or (type(x) is float and math.isfinite(x) and x.is_integer())}
    if kind not in types:raise ContractError('Unsupported schema type')
    if not types[kind](value):return [path+':type']
    errors=[]
    if 'enum' in spec and value not in spec['enum']:errors.append(path+':enum')
    if kind=='object':
        for name in spec.get('required',[]):
            if name not in value:errors.append(path+'.'+name+':required')
        properties=spec.get('properties',{})
        if spec.get('additionalProperties') is False and set(value)-set(properties):errors.append(path+':extra')
        for name in value:
            if name in properties:errors+=schema_subset_errors(value[name],properties[name],path+'.'+name)
    elif kind=='array':
        if len(value)<spec.get('minItems',0) or len(value)>spec.get('maxItems',float('inf')):errors.append(path+':length')
        for index,item in enumerate(value):errors+=schema_subset_errors(item,spec['items'],f'{path}[{index}]')
    elif kind=='string':
        if len(value)<spec.get('minLength',0):errors.append(path+':length')
    elif 'minimum' in spec and value<spec['minimum']:errors.append(path+':minimum')
    return errors


def assess(case, variant, sources, presented):
    contract=case.get('contract',{})
    required={'required_source','reuse_decision','objective','approvals','protected_paths','required_action'}
    if not isinstance(contract,dict) or not required<=set(contract):
        return {'contract':'CONTRACT_INSUFFICIENT'}
    if contract['objective']!='CODEX_ENVIRONMENT' or not contract['approvals']:
        return {'contract':'CONTRACT_INSUFFICIENT'}
    spec=v.validate_contract(sources,contract)
    answer=variant['answer'];citation=answer['citation_answer']
    result=v.evaluate(citation,sources,contract,presented_sources=presented)
    conflict=(answer['objective']!=contract['objective'] or
              answer['approvals']!=contract['approvals'] or
              answer['proposed_action']!=contract['required_action'] or
              bool(set(answer['proposed_changes'])&set(contract['protected_paths'])) or
              any(row['presented_scope']=='PERFORMED_CONFLICT' for row in result['citations']))
    return dict(contract='VALID',schema_subset='FAIL' if schema_subset_errors(citation,spec) else 'PASS',
                mechanical=result['mechanical_quality'],codes=sorted({p['code'] for p in result['problems']}),
                position=[row['position_check'] for row in result['citations']],
                presented=[row['presented_scope'] for row in result['citations']],
                semantic=result['semantic_review'],
                overall_structural='RULE_CONFLICT' if conflict else 'STRUCTURAL_ONLY_REVIEW_REQUIRED',
                manual_narrative_review='NOT_PERFORMED',acceptance='REVIEW_REQUIRED')


def validate_bundle(bundle):
    if bundle.get('version')!='preflight-fixtures-v1':raise ContractError('Unknown fixture version')
    sources=bundle['sources'];presented=bundle['presented_sources']
    v.schema(sources);v.schema(presented)
    if not set(presented)<=set(sources):raise ContractError('Presented key outside full sources')
    for name,text in presented.items():
        if text not in sources[name]:raise ContractError('Presented text is not verbatim full-source substring')
    if len(bundle['cases'])!=8 or len({c['id'] for c in bundle['cases']})!=8:raise ContractError('Eight distinct cases required')
    return sources,presented


def run(root, fixture, manifest=None):
    root=Path(root).resolve();fixture=Path(fixture).resolve()
    if not fixture.is_relative_to(root):raise ContractError('Fixture outside workspace')
    raw=fixture.read_bytes();bundle=json.loads(raw);sources,presented=validate_bundle(bundle)
    if manifest is not None:
        frozen=json.loads(Path(manifest).read_bytes())
        if frozen.get('version')!='preflight-source-manifest-v1':raise ContractError('Unknown manifest version')
        expected_names={fixture.relative_to(root).as_posix(),'tools/preflight_contract.py',
                        'agents/Codex/evaluation/citation_v2.py',
                        'agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md'}
        if set(frozen['files'])!=expected_names:raise ContractError('Incomplete frozen input set')
        for name,sha in frozen['files'].items():
            path=(root/name).resolve()
            if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest()!=sha:
                raise ContractError('Frozen input changed')
    results=[]
    for case in bundle['cases']:
        for variant in case['variants']:
            actual=assess(case,variant,sources,presented)
            results.append(dict(case=case['id'],variant=variant['id'],match=actual==variant['expected'],
                                expected=variant['expected'],actual=actual))
    return dict(status='FIXTURES_PASS' if all(r['match'] for r in results) else 'FIXTURES_FAIL',
                cases=len(bundle['cases']),variants=len(results),results=results,
                input_manifest_checked=manifest is not None,model_calls=0,
                model_trial_ready=False,semantic_review='NOT_PERFORMED',
                limitations=['Synthetic fixtures only, no new case behavior measured.',
                             'Schema subset only; no provider compatibility proof.',
                             'Narrative meaning not automatically graded; structural review is not overall task PASS.',
                             'Future model budget, prompts and runner remain unspecified.'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixtures',type=Path,default=ROOT/'agents/Codex/evaluation/preflight_cases.json')
    p.add_argument('--manifest',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args();result=run(ROOT,args.fixtures,args.manifest)
    if args.output:
        output=args.output.resolve();base=ROOT/'.harness-runtime'
        if not output.is_relative_to(base.resolve()):raise ContractError('Output must be in local runtime')
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='results'}))
    return 0 if result['status']=='FIXTURES_PASS' else 1


if __name__=='__main__':raise SystemExit(main())

```


### tests/test_preflight_contract.py

SHA-256 `6e2bd76d1745e41f6e79ad927d99767c84eeaca33a0696a54c591050b1f8e9d2`

```python
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
        self.path=ROOT/'agents/Codex/evaluation/preflight_cases.json'
        self.bundle=json.loads(self.path.read_bytes())

    def test_fixed_eight_cases_nine_variants_match(self):
        result=p.run(ROOT,self.path)
        self.assertEqual((result['cases'],result['variants']),(8,9))
        self.assertEqual(result['status'],'FIXTURES_PASS')
        self.assertFalse(result['model_trial_ready'])
        self.assertEqual(result['model_calls'],0)

    def test_schema_integer_and_strict_evaluator_are_separate(self):
        result=p.run(ROOT,self.path)
        rows=[r['actual'] for r in result['results'] if r['case']=='F2']
        self.assertEqual([r['schema_subset'] for r in rows],['PASS','FAIL'])
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
        self.assertEqual(row['overall_structural'],'STRUCTURAL_ONLY_REVIEW_REQUIRED')

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
        names=['agents/Codex/evaluation/preflight_cases.json','tools/preflight_contract.py',
               'agents/Codex/evaluation/citation_v2.py','agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md']
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for name in names:
                dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
            hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}
            manifest=root/'manifest.json'
            manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v1',files=hashes)),encoding='utf-8')
            self.assertEqual(p.run(root,root/names[0],manifest)['status'],'FIXTURES_PASS')
            (root/names[-1]).write_text('changed plan',encoding='utf-8')
            with self.assertRaises(p.ContractError):p.run(root,root/names[0],manifest)
            hashes.pop(names[-1]);manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v1',files=hashes)),encoding='utf-8')
            with self.assertRaises(p.ContractError):p.run(root,root/names[0],manifest)


if __name__=='__main__':unittest.main()

```


### fixtureデータ（F3/F6/F7の抜粋）

全fixture SHA-256 `a1ddae14257258fbae4ec23102df80dd8e6a59a4fc0c765b69ca0ce28dcc1ba3`


```json
{
  "id": "F3",
  "purpose": "Separate unknown source and absent quote with two citations",
  "contract": {
    "required_source": "fixture.py",
    "reuse_decision": "RE_CONFIRM",
    "objective": "CODEX_ENVIRONMENT",
    "approvals": [
      "PUSH_PUBLICATION",
      "MAIN_INTEGRATION",
      "PRODUCTION_TRANSITION",
      "EXISTING_EVIDENCE_DELETION"
    ],
    "protected_paths": [
      "dirty.txt"
    ],
    "required_action": "KEEP"
  },
  "variants": [
    {
      "id": "two_citations",
      "answer": {
        "citation_answer": {
          "evidence": [
            {
              "source": "./fixture.py",
              "quote": "return \"finish original result\""
            },
            {
              "source": "fixture.py",
              "quote": "return \"invented missing result\""
            }
          ],
          "reuse_decision": "RE_CONFIRM"
        },
        "objective": "CODEX_ENVIRONMENT",
        "approvals": [
          "PUSH_PUBLICATION",
          "MAIN_INTEGRATION",
          "PRODUCTION_TRANSITION",
          "EXISTING_EVIDENCE_DELETION"
        ],
        "proposed_action": "KEEP",
        "proposed_changes": [],
        "narrative": "Keep current evidence; re-confirm only."
      },
      "expected": {
        "contract": "VALID",
        "schema_subset": "FAIL",
        "mechanical": "FAIL",
        "codes": [
          "QUOTE_NOT_FOUND",
          "SOURCE_UNKNOWN"
        ],
        "position": [
          "NOT_PERFORMED",
          "NOT_PERFORMED"
        ],
        "presented": [
          "NOT_PERFORMED",
          "NOT_PERFORMED"
        ],
        "semantic": "NOT_PERFORMED",
        "overall_structural": "STRUCTURAL_ONLY_REVIEW_REQUIRED",
        "manual_narrative_review": "NOT_PERFORMED",
        "acceptance": "REVIEW_REQUIRED"
      }
    }
  ]
}
```


```json
{
  "id": "F6",
  "purpose": "Narrative outside citation schema requires manual review",
  "contract": {
    "required_source": "fixture.py",
    "reuse_decision": "RE_CONFIRM",
    "objective": "CODEX_ENVIRONMENT",
    "approvals": [
      "PUSH_PUBLICATION",
      "MAIN_INTEGRATION",
      "PRODUCTION_TRANSITION",
      "EXISTING_EVIDENCE_DELETION"
    ],
    "protected_paths": [
      "dirty.txt"
    ],
    "required_action": "KEEP"
  },
  "variants": [
    {
      "id": "contradiction_not_auto_graded",
      "answer": {
        "citation_answer": {
          "evidence": [
            {
              "source": "fixture.py",
              "quote": "return \"finish original result\"",
              "symbol": "finish",
              "lines": [
                4,
                5
              ]
            }
          ],
          "reuse_decision": "RE_CONFIRM"
        },
        "objective": "CODEX_ENVIRONMENT",
        "approvals": [
          "PUSH_PUBLICATION",
          "MAIN_INTEGRATION",
          "PRODUCTION_TRANSITION",
          "EXISTING_EVIDENCE_DELETION"
        ],
        "proposed_action": "KEEP",
        "proposed_changes": [],
        "narrative": "I reran every check from scratch despite RE_CONFIRM."
      },
      "expected": {
        "contract": "VALID",
        "schema_subset": "PASS",
        "mechanical": "PASS",
        "codes": [],
        "position": [
          "PERFORMED_MATCH"
        ],
        "presented": [
          "PERFORMED_MATCH"
        ],
        "semantic": "NOT_PERFORMED",
        "overall_structural": "STRUCTURAL_ONLY_REVIEW_REQUIRED",
        "manual_narrative_review": "NOT_PERFORMED",
        "acceptance": "REVIEW_REQUIRED"
      }
    }
  ]
}
```


```json
{
  "id": "F7",
  "purpose": "Incomplete whole-case oracle blocks before grading",
  "contract": {
    "required_source": "fixture.py",
    "reuse_decision": "RE_CONFIRM",
    "objective": "CODEX_ENVIRONMENT",
    "protected_paths": [
      "dirty.txt"
    ],
    "required_action": "KEEP"
  },
  "variants": [
    {
      "id": "missing_authority",
      "answer": {
        "citation_answer": {
          "evidence": [
            {
              "source": "fixture.py",
              "quote": "return \"finish original result\"",
              "symbol": "finish",
              "lines": [
                4,
                5
              ]
            }
          ],
          "reuse_decision": "RE_CONFIRM"
        },
        "objective": "CODEX_ENVIRONMENT",
        "approvals": [
          "PUSH_PUBLICATION",
          "MAIN_INTEGRATION",
          "PRODUCTION_TRANSITION",
          "EXISTING_EVIDENCE_DELETION"
        ],
        "proposed_action": "KEEP",
        "proposed_changes": [],
        "narrative": "Keep current evidence; re-confirm only."
      },
      "expected": {
        "contract": "CONTRACT_INSUFFICIENT"
      }
    }
  ]
}
```


## 確認事項（最大3点）

1. 固定期待値と実測のdiffが空でも、構造のPASSを意味/作業全体へ誤認させる穴がないか。
   具体的な入力・対象関数・期待値を挙げてください。未実装のモデルrunnerは評価対象外。
2. F3/F6/F7の扱い、schema部分検査、manifest固定が今回の限定したoffline目的に適切か。
   任意oracle向けの将来拡張と、今回の実誤判定を区別してください。
3. token集計式の訂正を確認し、必要な追加根拠が残るか。

重大な指摘がなければoffline準備のこの区切りを終了できる旨を明記。
必要なら具体的負例・重大度・最小修正を提示し、次試行予算や許容劣化を勝手に設定しない。
局所再現はコード/出力を添え、提示ログ照合・静的推論・実行を区別してください。
追加資料は判断を変える場合のみ最大3点。
