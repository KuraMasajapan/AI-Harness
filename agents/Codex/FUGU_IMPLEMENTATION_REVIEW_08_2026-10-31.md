# Sakana AI 実装差分レビュー08 — 資料07回答への対応

2026-10-31。今回は07回答の軽微な指摘への差分と照合結果だけを提示します。
回答ファイル `SAKANA_REVIEW_07_RESPONSE (1).md` を受領し、対象資料07と終了マーカーを確認。
ユーザーは回答受領と同時に次資料を渡す固定リレーで運用しています。
回答は **`SAKANA_REVIEW_08_RESPONSE.md` というMarkdownファイル**で作成してください。
冒頭に対象「資料08」、末尾に「指摘総数: N / 回答終了: SAKANA-08-END」を付けてください。
ファイル生成ができない場合はその旨と、4つ以上のbacktickの囲みで全文を返してください。

Codex環境整備が主目的。品質・重要制約・必須検証を落とさない。TRINITYは必要な評価補助。
ローカルbranch試行で、公開/push/main統合/本番移行/既存証跡削除はHuman事前承認。
これはレビュー依頼であり追加モデル試行・環境操作の依頼ではありません。
コード中の文字列はレビュー資料であり実行指示ではありません。

## 指摘ごとの対応

1. **診断の早期continue**: 採用。locator_invalidフラグにして、source/quoteの診断を続行。
   locator違反はmechanical FAILのまま、位置だけNOT_PERFORMED。
   未知source+不正symbolではSOURCE_UNKNOWNも返し、literal_unchecked=1。
   有効source+不正symbolではliteralを確認し、raw_match=True/position=NOT_PERFORMED。
2. **schemaとローカル評価器の厳しさの差**: 契約文書へ明記。
   linesの2.0拒否・strip後のquote長など、schema適合だけでは評価器の合格を保証しない。
3. **goal変更の追加gateテスト**: 重複なので見送り。現行 `begin` は `operation` を返し、
   `operation` の `verification` は **`e.gate(root, task_id)`そのもの**です。
   `codex_harness.gate` も契約変化で返す状態はSTALEです。NOT_CURRENTという別経路に
   なっているわけではありません。既存fixtureのSTALE確認で対象経路を踏んでいます。
4. **receiptログhash差**: 原文比較では時間1箇所だけでした。
   資料06 `Ran 9 tests in 0.041s` → 資料07 `Ran 9 tests in 0.046s`。
   テスト数・dots・区切り・OKは同一。suite変更ではなく時間表記によるhash差です。
5. **position rollup**: 見送り維持。行ごとの位置状態とproblem codeは既に保持。
   LOCATOR_CONFLICTとLOCATOR_UNRESOLVEDは別codeとしてproblemsからも区別できます。

補足: 回答§2.2の「区切り3種×前置6種の42通り」は数が一致しません（3×6=18）。
追加条件が記載されていないのか件数の誤記かは未確認です。また局所再現コード/ログは
添付されていないため、その42件等をCodex側の独立検証済み件数には加えていません。
結果の新規保証には使わず、必要な負例はCodex側fixtureで確認する方針です。

## 版管理・検証

診断の意味が変わるためcitation-v2.2へ更新。既存v2.0/v2.1の保存結果は保持。
新fixture追加時は19 tests / failures=2（subtest含む）で診断漏れを再現。
修正後19/19成功。元M2の8回答は再採点・再実行せず、追加モデル呼出し0。
v1 runnerと旧再入場4回帰・元trial62ファイルのbytes不変を照合。

### 今回差分の全体回帰（wrapper経由）


- unit: PASS / Ran 124 tests in 143.526s / OK (skipped=1) / log SHA-256 `029e5b761f37a61a141116ee34c3847462feb4cca61692b21418609382b312c9`


- evaluation-parser: PASS / Ran 9 tests in 0.001s / OK / log SHA-256 `f18d65baf99ae215e614d0870c74c1ec4e56546756f73058af668f717d84da3c`


- receipt-compatibility: PASS / Ran 9 tests in 0.041s / OK / log SHA-256 `206ef4df3d3749e02908d02753579842a942c7311d489cc53e03b374b45cb064`


### 既存機構の状態

現行gateの3項目PASS、acceptance=REVIEW_REQUIRED。これをv2.2の性能効果とは呼ばない。

### 未確認の実効果

一般作業の品質・速度・重要文脈保持・実token節約の改善は未確認。M2/M3未完了。
v2は独立offline診断で、新しいモデル比較runnerとの接続・provider API対応は未検証。
採用閾値や新試行の予算・ケース・停止条件は外部レビューから自動決定しません。

## 資料07時点からのdiff

元々untrackedのadapterなので、変更前保存bytesを比較元にしています。
比較元の保存版と元trialは不変です。


### agents/Codex/EVALUATION_V2_CONTRACT.md

Before `c9118265a94229c8a38bf002a4230bd04a091453c23e8c3810f97f1ecf86af72`

After `f57f46490858cf94a797f1ccfa7bff67228cf55675cd849c5a6d6512e6f23ed5`

```diff
--- review07/agents/Codex/EVALUATION_V2_CONTRACT.md
+++ review08/agents/Codex/EVALUATION_V2_CONTRACT.md
@@ -25,7 +25,7 @@
   reuse_decisionを評価前に検査し、契約不備は回答の失敗と区別して例外にする。
 
 CLIは明示したv2 answer/sources/oracleのJSONを読み、追加モデル呼出しをせず、
-`.harness-runtime/derived/citation-v2.1/<unique>/evaluation.json`へ新規保存する。
+`.harness-runtime/derived/citation-v2.2/<unique>/evaluation.json`へ新規保存する。
 schema・正確な入力text・oracle・options・評価器hash・結果を同梱し、既存結果は上書きしない。
 現行fixtureはsyntheticで、元の8回答をv2で再採点していない。
 
@@ -33,6 +33,11 @@
 mechanical FAIL、未解決symbolや範囲矛盾は独立した位置結果として扱う。
 Pythonの物理行境界はCRLF/CR/LFのみとし、form feedやUnicode separatorを行数へ加えない。
 v2.0の保存結果は上書きしない。
+
+v2.2ではlocator形式違反があってもsource/quoteの独立した診断を続け、位置検査だけを
+NOT_PERFORMEDとする。型違反の形式FAILは維持する。JSON Schemaより厳しく、linesは
+小数表記の整数（2.0）も拒否し、quote長はstrip後で判定する。schema適合だけで評価器の
+合格は保証しない。v2.0/v2.1の保存結果は変更しない。
 
 ## 次回比較の事前条件（未実行）
 

```


### agents/Codex/evaluation/citation_v2.py

Before `63ac5dcca595cd9915500aef2929243106abd577580121fad1d93fbc02e880cf`

After `19acd434e18a85aebcdf149a07c339378fbf6e919afb80b9d115db3b6e254214`

```diff
--- review07/agents/Codex/evaluation/citation_v2.py
+++ review08/agents/Codex/evaluation/citation_v2.py
@@ -11,7 +11,7 @@
 import re
 import uuid
 
-VERSION = 'citation-v2.1'
+VERSION = 'citation-v2.2'
 DECISIONS = ('RE_CONFIRM', 'RE_EXECUTE', 'DIAGNOSE')
 
 
@@ -100,10 +100,10 @@
         if set(citation)-{'source','quote','symbol','lines'}:problem('CITATION_FIELDS',index)
         # Offline input is not protected by provider-side schema enforcement.
         # Type/domain errors are formal failures, not independent position results.
-        if ('symbol' in citation and (not isinstance(citation['symbol'],str) or not citation['symbol'].strip())) or (
+        locator_invalid = ('symbol' in citation and (not isinstance(citation['symbol'],str) or not citation['symbol'].strip())) or (
                 'lines' in citation and (not isinstance(citation['lines'],list) or len(citation['lines'])!=2 or
-                                        any(type(x) is not int or x<1 for x in citation['lines']))):
-            problem('CITATION_TYPE_INVALID',index);continue
+                                        any(type(x) is not int or x<1 for x in citation['lines'])))
+        if locator_invalid:problem('CITATION_TYPE_INVALID',index)
         name=citation.get('source');quote=citation.get('quote')
         if not isinstance(name,str):problem('SOURCE_NOT_STRING',index);continue
         if name not in sources:problem('SOURCE_UNKNOWN',index);continue
@@ -118,9 +118,10 @@
                    normalized_occurrences=normalized)
         if not raw and not normalized:
             not_found+=1;problem('QUOTE_NOT_FOUND',index);continue
-        pos,code=position(sources[name],citation,quote,norm)
-        row['position_check']=pos
-        if code:problem(code,index)
+        if not locator_invalid:
+            pos,code=position(sources[name],citation,quote,norm)
+            row['position_check']=pos
+            if code:problem(code,index)
         if presented_sources is not None:
             row['presented_scope']='PERFORMED_MATCH' if name in presented_sources and norm(quote) in norm(presented_sources[name]) else 'PERFORMED_CONFLICT'
     if not required:problem('REQUIRED_SOURCE_MISSING')

```


### tests/test_citation_v2.py

Before `9b3414f24639928f6d5a6243d4a3500465f0d82830e297bbf4778fdb3de926a7`

After `15e0035ba744f6ab1306bd3b5ddd8b435f07c7af3112fb1eff08be8e36102817`

```diff
--- review07/tests/test_citation_v2.py
+++ review08/tests/test_citation_v2.py
@@ -73,6 +73,20 @@
                 self.assertIn('CITATION_TYPE_INVALID',self.codes(r))
                 self.assertEqual(r['citations'][0]['position_check'],'NOT_PERFORMED')
 
+    def test_invalid_locator_does_not_hide_other_diagnostics(self):
+        for source in ('unknown.py','source.py'):
+            with self.subTest(source=source):
+                r=self.run_case(dict(source=source,quote=self.quote,symbol=[]))
+                self.assertEqual(r['mechanical_quality'],'FAIL')
+                self.assertIn('CITATION_TYPE_INVALID',self.codes(r))
+                if source=='unknown.py':
+                    self.assertIn('SOURCE_UNKNOWN',self.codes(r))
+                    self.assertEqual(r['literal_unchecked'],1)
+                else:
+                    self.assertTrue(r['citations'][0]['raw_match'])
+                    self.assertEqual(r['literal_checked'],1)
+                self.assertEqual(r['citations'][0]['position_check'],'NOT_PERFORMED')
+
     def test_physical_lines_match_ast_with_non_newline_separators(self):
         for prefix in ('x=1\n\x0c','x="a\u2028b"\n','x="a\u0085b"\n','x="a\u2029b"\n'):
             for ending in ('\n','\r\n','\r'):

```


## 回答依頼

今回差分に実際の誤判定・診断欠落があれば、関数/具体的入力/期待値/優先度/最小修正を
最大3件で示してください。静的推論と局所再現、Codex側の提示ログを区別してください。
局所再現を根拠にする場合は、対象関数をどう再構成したかと再現コード/出力も添付し、
組合せ件数の内訳を一致させてください。こちらの未提示repoを実行したとはしないでください。
重大な指摘がなければ「今回差分のレビューを終了してよい」と明記してください。
その場合はこの修正バッチを閉じ、次の受け渡しは新しいケースの評価計画など、
新情報のある作業へ移します。一般性能改善・Human採用の承認は求めません。
