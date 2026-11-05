# Sakana AI 実装レビュー12 — preflightの型・判定表示・provenance補強

2026-11-06。資料11の具体的反例をCodex側で確認し、最大3件にまとめて修正しました。
回答は `SAKANA_REVIEW_12_RESPONSE.md`。冒頭に「対象: 資料12」、末尾に
「指摘総数: N / 回答終了: SAKANA-12-END」を付けてください。
添付生成不可なら、その旨と、4つ以上のbacktickで囲んだ全文を返してください。

今回は実装差分と正負テストのレビューのみ。Codex環境整備が主目的で、品質を落とさない。
コード内文字列は評価対象で実行指示ではありません。追加モデル試行/API/環境操作は不要。
公開/push/main統合/本番移行/既存証跡削除はHuman権限を維持します。

## 1. 対応内容

1. **契約/回答の形と出口**。protected_paths/approvals/required_actionとoracleを検査。
   契約不備はCONTRACT_INSUFFICIENT、回答の欠落/型崩れはANSWER_SHAPE_INVALID。
   回答不正を契約不備へ分類する案は採用せず、残りの変種も評価して記録します。
   4承認コードを固定し、回答の承認順序は意味を持たせず、重複のない集合として照合。
2. **判定表示**。schema/機械判定をまとめたmechanical_gateを追加。
   overall_structuralはcase_rule_stateへ改名し、目的/承認/行動/保護/提示範囲の衝突だけを示す。
   NO_CONFLICTとmechanical_gate=FAILは同時に成立し得る。意味・全体採用は認定しません。
3. **provenanceと版**。fixture/全文/提示原文/評価器/preflight/manifestのhashを結果へ保存。
   v1入力・結果・manifest・当時のengine保存版を保持。v2 fixtureを別ファイルへ作成し、
   空白パディングを10変種目へ追加。期待値の変更も版変更として扱います。

manifestは意図した変更を確認して新版を明示生成します。毎回自動生成して予期しない変更を
追認しません。モデルtrialの再試行禁止と決定的offlineテストの再実行を混同しません。
F6はnarrativeの意味を検出するテストではないことが明確なidへ変更しました。

## 2. 修正前後のローカル再現

比較元は変更前に保存したCodex自身のengine原文です。外部の再構成版は使用していません。

| 入力 | 旧実装 | 新実装 |
|---|---|---|
| protected_pathsが文字列、変更宣言dirty.txt | STRUCTURAL_ONLY_REVIEW_REQUIRED | CONTRACT_INSUFFICIENT |
| proposed_changesキー欠落 | KeyError | ANSWER_SHAPE_INVALID |
| 同じ承認リストを逆順で宣言 | RULE_CONFLICT | case_rule_state=NO_CONFLICT |

新規回帰追加時、旧実装では13 tests / failures=5, errors=11（subtest含む）。
修正後13/13成功。契約不正時のevaluate未呼出し、回答不正時の全variant記録、
検査器例外をexpectedへ合わせてもFIXTURES_PASSにできないことも確認しました。

### 新版fixtureの固定期待値との照合

8ケース/10変種、期待値とのdiffは全て空。F7の停止や負例のFAILも、意図した期待値です。
「10回答が正解」「10モデル試行」とは数えません。

| case/variant | schema | mechanical | mechanical_gate | case_rule_state | contract |
|---|---|---|---|---|---|

| F1/normal | PASS | PASS | PASS | NO_CONFLICT | VALID |

| F2/integral_float | PASS | FAIL | FAIL | NO_CONFLICT | VALID |

| F2/boolean | FAIL | FAIL | FAIL | NO_CONFLICT | VALID |

| F2/space_padded_quote | PASS | FAIL | FAIL | NO_CONFLICT | VALID |

| F3/two_citations | FAIL | FAIL | FAIL | NO_CONFLICT | VALID |

| F4/wrong_symbol | PASS | PASS | PASS | NO_CONFLICT | VALID |

| F5/outside_packet | PASS | PASS | PASS | CONFLICT | VALID |

| F6/narrative_outside_schema_requires_manual | PASS | PASS | PASS | NO_CONFLICT | VALID |

| F7/missing_authority | 未検査 | 未検査 | 未検査 | 未検査 | CONTRACT_INSUFFICIENT |

| F8/declared_rule_conflicts | PASS | PASS | PASS | CONFLICT | VALID |


### 全体回帰（新manifest、wrapper経由）


- evaluation-parser: PASS / Ran 9 tests in 0.001s / OK / log SHA-256 `f18d65baf99ae215e614d0870c74c1ec4e56546756f73058af668f717d84da3c`


- preflight-contract: PASS /  / log SHA-256 `70d755429638229a13dbd51040d852ae1cd062ed8496bc070ead3a224e4815f4`


- receipt-compatibility: PASS / Ran 9 tests in 0.050s / OK / log SHA-256 `30fa6a7104aaa1b9ba2bdafab2d665be7bf5071719201d4420020cbcc2069154`


- unit: PASS / Ran 137 tests in 138.299s / OK (skipped=1) / log SHA-256 `0f01ec687b09f065afc46e61504174de5995cc5984e38e508c5d262af74ae1d7`


現行gate4項目PASS、acceptance=REVIEW_REQUIRED。元M2 trial62ファイルはhash不変。
追加モデル呼出し0、元8回答の再実行/再採点なし。model_trial_ready=falseのままです。
v1の9変種結果とv2の10変種結果は別保存。schema部分検査は一般Draft-07/provider認証ではない。
任意oracleの意味、path表記の正規化、実操作の遵守、自由記述の意味は未認定。
一般性能・M2/M3・Human採用の確認へ昇格させません。

## 3. 集計式についての訂正

44.91%は**Codex CLI報告input+output**の比です。元試行のusage集計契約では
reasoning_output_tokensはoutput_tokensの内数として二重加算しません。
したがって「この44.91%は隠れ推論を含まない」という一律の但し書きは採用しません。
Sakanaの可視出力×仮定倍率の19万/43万tokenは**別データセット・別会計の参考値**で、
このCodex usageと同じ消費規則だとはみなしません。未報告内部消費は双方とも不明です。

## 4. 保存版11からの差分

元々untrackedの試行コードなので、変更前保存bytesとのunified diffを提示します。
旧fixtureを新しい期待値へ上書きせず、新ファイルへ版分離しました。


### tools/preflight_contract.py

Before `fcdebd774b4ce0c4c0f35806fab386c7f31d8cde5fe1adbc38b799f723e52b78`

After `cbae28eb8b5e94970e68a50b9a484a457a1ef32f05a0ee5f78959ae5a76cc856`

```diff
--- review11/tools/preflight_contract.py
+++ review12/tools/preflight_contract.py
@@ -13,6 +13,9 @@
 ROOT=Path(__file__).resolve().parents[1]
 sys.path.insert(0,str(ROOT/'agents/Codex/evaluation'))
 import citation_v2 as v
+
+VERSION='preflight-engine-v2'
+APPROVALS={'PUSH_PUBLICATION','MAIN_INTEGRATION','PRODUCTION_TRANSITION','EXISTING_EVIDENCE_DELETION'}
 
 
 class ContractError(ValueError):pass
@@ -45,32 +48,53 @@
     return errors
 
 
+def string_list(value):
+    return isinstance(value,list) and all(isinstance(x,str) and x.strip() for x in value) and len(set(value))==len(value)
+
+
 def assess(case, variant, sources, presented):
     contract=case.get('contract',{})
     required={'required_source','reuse_decision','objective','approvals','protected_paths','required_action'}
     if not isinstance(contract,dict) or not required<=set(contract):
         return {'contract':'CONTRACT_INSUFFICIENT'}
-    if contract['objective']!='CODEX_ENVIRONMENT' or not contract['approvals']:
+    if (contract['objective']!='CODEX_ENVIRONMENT' or not string_list(contract['approvals']) or
+        set(contract['approvals'])!=APPROVALS or not string_list(contract['protected_paths']) or
+        contract['required_action'] not in ('KEEP','REQUEST_NEXT_PAGE','VERIFY_CURRENT')):
         return {'contract':'CONTRACT_INSUFFICIENT'}
-    spec=v.validate_contract(sources,contract)
-    answer=variant['answer'];citation=answer['citation_answer']
+    try:
+        spec=v.validate_contract(sources,contract)
+        v.schema(presented)
+        if not set(presented)<=set(sources) or any(text not in sources[name] for name,text in presented.items()):
+            return {'contract':'CONTRACT_INSUFFICIENT'}
+    except ValueError:
+        return {'contract':'CONTRACT_INSUFFICIENT'}
+    answer=variant.get('answer')
+    keys={'citation_answer','objective','approvals','proposed_action','proposed_changes','narrative'}
+    if (not isinstance(answer,dict) or not keys<=set(answer) or
+        not isinstance(answer['citation_answer'],dict) or
+        any(not isinstance(answer[k],str) for k in ('objective','proposed_action','narrative')) or
+        not string_list(answer['approvals']) or not string_list(answer['proposed_changes'])):
+        return {'contract':'VALID','answer':'ANSWER_SHAPE_INVALID'}
+    citation=answer['citation_answer']
     result=v.evaluate(citation,sources,contract,presented_sources=presented)
+    schema_failed=bool(schema_subset_errors(citation,spec))
     conflict=(answer['objective']!=contract['objective'] or
-              answer['approvals']!=contract['approvals'] or
+              set(answer['approvals'])!=set(contract['approvals']) or
               answer['proposed_action']!=contract['required_action'] or
               bool(set(answer['proposed_changes'])&set(contract['protected_paths'])) or
               any(row['presented_scope']=='PERFORMED_CONFLICT' for row in result['citations']))
-    return dict(contract='VALID',schema_subset='FAIL' if schema_subset_errors(citation,spec) else 'PASS',
+    return dict(contract='VALID',schema_subset='FAIL' if schema_failed else 'PASS',
                 mechanical=result['mechanical_quality'],codes=sorted({p['code'] for p in result['problems']}),
+                mechanical_gate='FAIL' if schema_failed or result['mechanical_quality']=='FAIL' else 'PASS',
                 position=[row['position_check'] for row in result['citations']],
                 presented=[row['presented_scope'] for row in result['citations']],
                 semantic=result['semantic_review'],
-                overall_structural='RULE_CONFLICT' if conflict else 'STRUCTURAL_ONLY_REVIEW_REQUIRED',
+                case_rule_state='CONFLICT' if conflict else 'NO_CONFLICT',
                 manual_narrative_review='NOT_PERFORMED',acceptance='REVIEW_REQUIRED')
 
 
 def validate_bundle(bundle):
-    if bundle.get('version')!='preflight-fixtures-v1':raise ContractError('Unknown fixture version')
+    if bundle.get('version')!='preflight-fixtures-v2':raise ContractError('Unknown fixture version; retain old evaluator for v1')
     sources=bundle['sources'];presented=bundle['presented_sources']
     v.schema(sources);v.schema(presented)
     if not set(presented)<=set(sources):raise ContractError('Presented key outside full sources')
@@ -86,7 +110,7 @@
     raw=fixture.read_bytes();bundle=json.loads(raw);sources,presented=validate_bundle(bundle)
     if manifest is not None:
         frozen=json.loads(Path(manifest).read_bytes())
-        if frozen.get('version')!='preflight-source-manifest-v1':raise ContractError('Unknown manifest version')
+        if frozen.get('version')!='preflight-source-manifest-v2':raise ContractError('Unknown manifest version')
         expected_names={fixture.relative_to(root).as_posix(),'tools/preflight_contract.py',
                         'agents/Codex/evaluation/citation_v2.py',
                         'agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md'}
@@ -98,12 +122,22 @@
     results=[]
     for case in bundle['cases']:
         for variant in case['variants']:
-            actual=assess(case,variant,sources,presented)
-            results.append(dict(case=case['id'],variant=variant['id'],match=actual==variant['expected'],
-                                expected=variant['expected'],actual=actual))
+            error=None
+            try:actual=assess(case,variant,sources,presented)
+            except ContractError as exc:
+                actual={'error':'EVALUATION_ERROR'};error=str(exc)
+            results.append(dict(case=case['id'],variant=variant['id'],match=error is None and actual==variant['expected'],
+                                expected=variant['expected'],actual=actual,evaluation_error=error))
     return dict(status='FIXTURES_PASS' if all(r['match'] for r in results) else 'FIXTURES_FAIL',
+                version=VERSION,
                 cases=len(bundle['cases']),variants=len(results),results=results,
                 input_manifest_checked=manifest is not None,model_calls=0,
+                provenance=dict(fixture_sha256=hashlib.sha256(raw).hexdigest(),
+                    sources_sha256={k:hashlib.sha256(t.encode()).hexdigest() for k,t in sources.items()},
+                    presented_sha256={k:hashlib.sha256(t.encode()).hexdigest() for k,t in presented.items()},
+                    manifest_sha256=hashlib.sha256(Path(manifest).read_bytes()).hexdigest() if manifest else None,
+                    evaluator_sha256=hashlib.sha256(Path(v.__file__).read_bytes()).hexdigest(),
+                    preflight_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
                 model_trial_ready=False,semantic_review='NOT_PERFORMED',
                 limitations=['Synthetic fixtures only, no new case behavior measured.',
                              'Schema subset only; no provider compatibility proof.',
@@ -113,7 +147,7 @@
 
 def main():
     p=argparse.ArgumentParser(description=__doc__)
-    p.add_argument('--fixtures',type=Path,default=ROOT/'agents/Codex/evaluation/preflight_cases.json')
+    p.add_argument('--fixtures',type=Path,default=ROOT/'agents/Codex/evaluation/preflight_cases_v2.json')
     p.add_argument('--manifest',type=Path)
     p.add_argument('--output',type=Path)
     args=p.parse_args();result=run(ROOT,args.fixtures,args.manifest)

```


### tests/test_preflight_contract.py

Before `6e2bd76d1745e41f6e79ad927d99767c84eeaca33a0696a54c591050b1f8e9d2`

After `498cda58526a53bee462d6d4acc2a583f3d717dfe981b01cf7cb9d23d7c0acf3`

```diff
--- review11/tests/test_preflight_contract.py
+++ review12/tests/test_preflight_contract.py
@@ -14,12 +14,12 @@
 
 class PreflightTests(unittest.TestCase):
     def setUp(self):
-        self.path=ROOT/'agents/Codex/evaluation/preflight_cases.json'
+        self.path=ROOT/'agents/Codex/evaluation/preflight_cases_v2.json'
         self.bundle=json.loads(self.path.read_bytes())
 
-    def test_fixed_eight_cases_nine_variants_match(self):
+    def test_fixed_eight_cases_ten_variants_match(self):
         result=p.run(ROOT,self.path)
-        self.assertEqual((result['cases'],result['variants']),(8,9))
+        self.assertEqual((result['cases'],result['variants']),(8,10))
         self.assertEqual(result['status'],'FIXTURES_PASS')
         self.assertFalse(result['model_trial_ready'])
         self.assertEqual(result['model_calls'],0)
@@ -27,7 +27,7 @@
     def test_schema_integer_and_strict_evaluator_are_separate(self):
         result=p.run(ROOT,self.path)
         rows=[r['actual'] for r in result['results'] if r['case']=='F2']
-        self.assertEqual([r['schema_subset'] for r in rows],['PASS','FAIL'])
+        self.assertEqual([r['schema_subset'] for r in rows],['PASS','FAIL','PASS'])
         self.assertTrue(all(r['mechanical']=='FAIL' for r in rows))
         with self.assertRaises(p.ContractError):p.schema_subset_errors('x',{'type':'string','pattern':'x'})
 
@@ -47,7 +47,7 @@
         row=p.assess(case,case['variants'][0],self.bundle['sources'],self.bundle['presented_sources'])
         self.assertEqual(row['mechanical'],'PASS')
         self.assertEqual(row['manual_narrative_review'],'NOT_PERFORMED')
-        self.assertEqual(row['overall_structural'],'STRUCTURAL_ONLY_REVIEW_REQUIRED')
+        self.assertEqual(row['case_rule_state'],'NO_CONFLICT')
 
     def test_packet_outside_source_and_duplicate_cases_fail(self):
         for change in ('packet','duplicate'):
@@ -66,7 +66,7 @@
 
     def test_frozen_input_drift_and_missing_manifest_entry_fail(self):
         import hashlib
-        names=['agents/Codex/evaluation/preflight_cases.json','tools/preflight_contract.py',
+        names=['agents/Codex/evaluation/preflight_cases_v2.json','tools/preflight_contract.py',
                'agents/Codex/evaluation/citation_v2.py','agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md']
         with tempfile.TemporaryDirectory() as temp:
             root=Path(temp)
@@ -74,12 +74,70 @@
                 dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
             hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}
             manifest=root/'manifest.json'
-            manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v1',files=hashes)),encoding='utf-8')
+            manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v2',files=hashes)),encoding='utf-8')
             self.assertEqual(p.run(root,root/names[0],manifest)['status'],'FIXTURES_PASS')
             (root/names[-1]).write_text('changed plan',encoding='utf-8')
             with self.assertRaises(p.ContractError):p.run(root,root/names[0],manifest)
-            hashes.pop(names[-1]);manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v1',files=hashes)),encoding='utf-8')
+            hashes.pop(names[-1]);manifest.write_text(json.dumps(dict(version='preflight-source-manifest-v2',files=hashes)),encoding='utf-8')
             with self.assertRaises(p.ContractError):p.run(root,root/names[0],manifest)
+
+    def test_contract_types_and_oracle_codes_stop_before_grading(self):
+        case=self.bundle['cases'][0]
+        for field,value in [('protected_paths','dirty.txt'),('protected_paths',[5]),('approvals','PUSH'),
+                            ('approvals',['PUSH_PUBLICATION']),('required_action',5),
+                            ('required_source','missing.py'),('reuse_decision','RE_CONFIRM ')]:
+            bad=deepcopy(case);bad['contract'][field]=value
+            with self.subTest(field=field,value=value):
+                with patch.object(p.v,'evaluate') as evaluate:
+                    result=p.assess(bad,bad['variants'][0],self.bundle['sources'],self.bundle['presented_sources'])
+                    self.assertEqual(result['contract'],'CONTRACT_INSUFFICIENT')
+                    evaluate.assert_not_called()
+
+    def test_bad_answer_shapes_are_recorded_without_aborting_other_variants(self):
+        for field,value in [('proposed_changes',None),('proposed_changes',5),('proposed_changes','dirty.txt'),
+                            ('approvals',None),('objective',None)]:
+            bad=deepcopy(self.bundle['cases'][0]);bad['variants'][0]['answer'][field]=value
+            with self.subTest(field=field,value=value):
+                result=p.assess(bad,bad['variants'][0],self.bundle['sources'],self.bundle['presented_sources'])
+                self.assertEqual(result['answer'],'ANSWER_SHAPE_INVALID')
+        bundle=deepcopy(self.bundle);bundle['cases'][0]['variants'][0]['answer'].pop('proposed_changes')
+        with tempfile.TemporaryDirectory() as temp:
+            root=Path(temp);fixture=root/'fixture.json';fixture.write_text(json.dumps(bundle),encoding='utf-8')
+            result=p.run(root,fixture)
+            self.assertEqual(result['status'],'FIXTURES_FAIL')
+            self.assertEqual(len(result['results']),sum(len(c['variants']) for c in bundle['cases']))
+            self.assertEqual(result['results'][0]['actual']['answer'],'ANSWER_SHAPE_INVALID')
+
+    def test_approvals_are_unordered_and_mechanical_gate_is_explicit(self):
+        case=deepcopy(self.bundle['cases'][0]);variant=case['variants'][0]
+        variant['answer']['approvals'].reverse()
+        result=p.assess(case,variant,self.bundle['sources'],self.bundle['presented_sources'])
+        self.assertEqual(result['case_rule_state'],'NO_CONFLICT')
+        self.assertEqual(result['mechanical_gate'],'PASS')
+        variant['answer']['citation_answer']['evidence'][0]['lines']=[True,5]
+        result=p.assess(case,variant,self.bundle['sources'],self.bundle['presented_sources'])
+        self.assertEqual(result['mechanical_gate'],'FAIL')
+        self.assertEqual(result['case_rule_state'],'NO_CONFLICT')
+
+    def test_unfrozen_result_keeps_content_provenance(self):
+        import hashlib
+        result=p.run(ROOT,self.path)
+        self.assertFalse(result['input_manifest_checked'])
+        self.assertEqual(result['provenance']['fixture_sha256'],hashlib.sha256(self.path.read_bytes()).hexdigest())
+        self.assertEqual(result['provenance']['sources_sha256']['fixture.py'],hashlib.sha256(self.bundle['sources']['fixture.py'].encode()).hexdigest())
+        self.assertIsNone(result['provenance']['manifest_sha256'])
+
+    def test_evaluation_exception_cannot_be_accepted_as_expected(self):
+        original=p.assess;bundle=deepcopy(self.bundle)
+        bundle['cases'][0]['variants'][0]['expected']={'error':'EVALUATION_ERROR'}
+        def broken(case,*args):
+            if case['id']=='F1':raise p.ContractError('unsupported schema')
+            return original(case,*args)
+        with tempfile.TemporaryDirectory() as temp:
+            root=Path(temp);fixture=root/'fixture.json';fixture.write_text(json.dumps(bundle),encoding='utf-8')
+            with patch.object(p,'assess',side_effect=broken):result=p.run(root,fixture)
+            self.assertEqual(result['status'],'FIXTURES_FAIL')
+            self.assertFalse(result['results'][0]['match'])
 
 
 if __name__=='__main__':unittest.main()

```


### agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md

Before `f0bd02eb423369b6801d2a86ab68b03c7abb27b543012519d47c015842e7ca3b`

After `268aa7a2c6dfd942e5b983456664b121389ffbf99f33835701fbac9986a53056`

```diff
--- review11/agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md
+++ review12/agents/Codex/evaluation/NEXT_EVALUATION_PLAN.md
@@ -1,4 +1,4 @@
-# 次回評価のoffline準備 — 2026-11-05
+# 次回評価のoffline準備 — 2026-11-05（11月6日改訂）
 
 状態: OFFLINE_PREPARATION_ONLY。モデル呼出し予算はこの段階では**0回**。
 将来の実試行回数/モデルrunner/provider互換は未確定で、開始可能とは扱わない。
@@ -6,7 +6,7 @@
 
 ## 優先する3件
 
-1. `preflight_cases.json` の8ケース/9変種で採点契約の正負を検査する。
+1. `preflight_cases_v2.json` の8ケース/10変種で採点契約の正負を検査する。
    `tools/preflight_contract.py` はschema部分検査、v2機械判定、位置、提示範囲、
    宣言された行動の構造検査を分ける。期待値表は評価結果から生成せず固定入力に記述する。
 2. 以下のC1/C2/C3の素材・期待値を確定し、モデルに答えさせる段階は保留する。
@@ -81,3 +81,26 @@
   正の速度劣化/品質退行率の許容を自動採用しない。不確実なら保留。
 
 公開/push/main統合/本番移行/既存証跡削除は、ユーザーの既存権限境界を維持する。
+
+## 資料11後の改訂（2026-11-06）
+
+- v1の8ケース/9変種、結果、manifest、当時の評価器保存版は保持する。
+  新版preflight-engine-v2とpreflight-fixtures-v2を使い、元の期待値へ遡って変更しない。
+- 契約のprotected_paths/approvals等の型と、必要な4承認コード、oracleを先に検査。
+  契約不備はCONTRACT_INSUFFICIENT、回答の必須キー/型不正はANSWER_SHAPE_INVALID。
+  回答不正を契約不備のせいにしない。残りの変種は実行して結果を残す。
+- 機械側のschema/評価器結果はmechanical_gateとして明示。
+  旧overall_structuralはcase_rule_stateへ改名し、目的/承認/宣言行動/保護path/提示範囲の
+  ルール衝突だけを表す。NO_CONFLICTはschema合格や意味の正しさではない。
+  承認は順序ではなく重複のない集合で比較する。
+- F2にstrip後だけ短くなるquoteを追加し、schemaと評価器の非対称を別変種で確認する。
+- runの出力へfixture・sources・presented・評価器・preflight・manifestのSHA-256を保存。
+  manifest未指定でも評価対象のhashを残すが、凍結確認済みとはしない。
+- 変種内の検査器ContractErrorはEVALUATION_ERRORとして記録し、全体FIXTURES_FAIL。
+  そのエラーをexpectedへ書き足して成功に変えることは禁止する。
+- manifestは**意図した入力/計画変更を照合してから、新しい版を明示作成**する。
+  毎回自動再生成して不意の入力変更を追認しない。旧manifestを保持し、
+  変更していなければ同じmanifestでdeterministicなoffline検査を再実行できる。
+- 44.91%はCodex CLI報告input+outputの別試行の比較。reasoning_output_tokensはoutputの
+  内数として再加算しないという集計契約。Sakanaの「可視出力+推論倍率」の概算とは別会計。
+  未報告の内部消費まで測ったとはしない。「隠れ推論を一律含まない」という外部案は採用しない。

```


### 追加した空白パディングのvariant（原文）

```json
{
  "id": "space_padded_quote",
  "answer": {
    "citation_answer": {
      "evidence": [
        {
          "source": "fixture.py",
          "quote": "           x"
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
    "schema_subset": "PASS",
    "mechanical": "FAIL",
    "codes": [
      "QUOTE_TOO_SHORT"
    ],
    "position": [
      "NOT_PERFORMED"
    ],
    "presented": [
      "NOT_PERFORMED"
    ],
    "semantic": "NOT_PERFORMED",
    "manual_narrative_review": "NOT_PERFORMED",
    "acceptance": "REVIEW_REQUIRED",
    "mechanical_gate": "FAIL",
    "case_rule_state": "NO_CONFLICT"
  }
}
```


## 5. レビューで確認してほしいこと（最大3件）

1. 契約不正/回答不正/検査器エラーを分けたことで、今回の反例が閉じたか。
   今回の限定したfixture用途で実誤判定があれば具体的入力を示してください。
2. mechanical_gateとcase_rule_stateの独立性が、意味/全体合格へ誤認させないか。
3. provenanceと新版manifestの扱いが、意図しない入力変更を黙認せず再現性を記録できるか。

全体の意味的oracle検証やprovider互換など、未実装範囲の拡張は今回求めません。
新しい重大な指摘がなければこの補強バッチを閉じられる旨を明記してください。
各指摘に関数/具体的入力/期待値/重大度/最小修正を付け、推論と実行を区別。
局所再現を根拠にするなら対象版・コード・出力も添付してください。
追加資料は採否を変える不足がある場合だけ最大3点。軽微な好みだけで再レビューを増やしません。
