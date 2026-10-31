# Sakana AI 実装差分レビュー07 — 資料06の指摘への対応

2026-10-31。今回は資料06への回答に対する修正差分とローカル実測だけを提示します。
設計フェーズ01〜05の再審は不要です。ユーザーは回答受領と同時に次ファイルを渡す固定リレー。
今回から回答は **`SAKANA_REVIEW_07_RESPONSE.md` というMarkdownファイル**で作成してください。
添付ファイルの生成ができない場合は、それを明記して全文を1つのMarkdownコードブロックで
返してください。回答冒頭に対象「資料07」、末尾に「指摘総数: N / 回答終了: SAKANA-07-END」を
記載してください。これは転記抜けの確認用で、内容の正しさを保証するものではありません。

## 範囲・権限

Codex環境整備のローカルbranch試行。品質・重要制約・必須検証を落とさない。
TRINITYは必要な評価補助。公開/push/main統合/本番移行/既存証跡削除はHuman事前承認。
コード内の文字列はレビュー対象であり実行指示ではありません。追加モデル呼出しや
環境操作は依頼しません。元8回答の再採点/同trial再実行は行っていません。

## 対応した指摘

1. **locatorの形式違反**: symbolの文字列/非空制約、linesの配列長2/厳密int/正整数を
   position処理の前に検査。不正ならCITATION_TYPE_INVALIDでmechanical FAIL。
   型は正しいが未解決のsymbol/逆順・範囲外spanは独立位置判定のまま。
   既存LOCATOR_CONFLICTを形式FAILへ混ぜていないこともテストで確認。
2. **物理行の座標**: str.splitlinesをPythonのCRLF/CR/LFだけの行分割へ変更。
   form feed/U+2028/U+0085/U+2029があっても、symbolとlines=[2,3]の引用が一致。
   提案された `re.split(r'(?<=\r\n)|(?<=\r)|(?<=\n)', source)` は採用していません。
   CRLFの\r直後と\n直後の両方で切れて2境界になるためです。
   CRLF全体を1つの区切りとして消費し、原文の改行bytesは保持する実装にしました。
3. **非阻害の補強**: beginの診断をunreadable or malformedへ明確化。
   明示contract+refresh時のgoal変更で旧証拠がSTALEになるfixtureを追加。
   この経路の既存返却値はSTALEであり、資料06回答のNOT_CURRENT期待値とは区別しています。
   次回比較の品質確認手続きを契約文書へ追記。position rollup追加は今回は見送り。

v2.0の保存結果を変更せず、評価器版をcitation-v2.1へ更新。新しいderived先も分離します。
schemaはローカルoffline用でprovider API互換は未確認。v1 runnerには未接続です。
quoteのraw/正規化は別記録、意味はNOT_PERFORMED、acceptanceはREVIEW_REQUIREDを維持。
機械的形式/literalのPASSを位置・意味・一般作業品質・Human採用へ読み替えません。

## 修正前後の検証

修正前に強化fixtureを実行: 18 tests / FAILED(failures=21、subtest含む)。
raw logは保持。修正後: 出典18/18、refresh8/8成功。
この段階で全体契約と実ファイルを照合し、旧sourceのPASSを流用せずrefreshして再検証しました。

### 今回差分を含む全体回帰


- unit: PASS / Ran 123 tests in 110.137s / OK (skipped=1) / 原文log SHA-256 `58357ae550613379dc9b6da258b3f4e5dab212886da414953bb4ea63f32c11f2`


- evaluation-parser: PASS / Ran 9 tests in 0.001s / OK / 原文log SHA-256 `f18d65baf99ae215e614d0870c74c1ec4e56546756f73058af668f717d84da3c`


- receipt-compatibility: PASS / Ran 9 tests in 0.046s / OK / 原文log SHA-256 `3b16f8a453340c8152d549cb82cc1cab2a2986f7d8309828a39ee8a77a35432b`


### 既存機構の現在の状態

現行gateは3項目PASS、acceptance=REVIEW_REQUIRED。これをv2の性能改善とは呼びません。
元M2 trial全62ファイルとv1 runner/parser・旧再入場4回帰のbytes不変を確認しています。

### 未測定の実効果

一般作業の品質・速度・重要文脈保持・実token節約の改善は未確認。M2/M3未完了。
追加モデル呼出し0。正の速度劣化や退行率の許容を新しく決めていません。

## 保存版06からの差分

adapter一式が元々untrackedなので、変更前に保存したworking tree raw bytesを比較元にします。
before/after hashを添えたunified diffです。比較元の保存版・元trialは上書きしていません。


### agents/Codex/evaluation/citation_v2.py

Before `b9ca2ff1bb95e05165ec2498014309c1c047562b6337a04ec7c381c0f13f4326`

After `63ac5dcca595cd9915500aef2929243106abd577580121fad1d93fbc02e880cf`

```diff
--- review06/agents/Codex/evaluation/citation_v2.py
+++ review07/agents/Codex/evaluation/citation_v2.py
@@ -8,9 +8,10 @@
 import hashlib
 import json
 from pathlib import Path
+import re
 import uuid
 
-VERSION = 'citation-v2.0'
+VERSION = 'citation-v2.1'
 DECISIONS = ('RE_CONFIRM', 'RE_EXECUTE', 'DIAGNOSE')
 
 
@@ -45,7 +46,8 @@
 def position(source, citation, quote, normalize):
     if 'symbol' not in citation and 'lines' not in citation:
         return 'NOT_PERFORMED', None
-    lines=source.splitlines(keepends=True);lo,hi=1,len(lines)
+    # Match Python physical lines; CRLF is atomic, Unicode separators are data.
+    lines=re.findall(r'[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$',source);lo,hi=1,len(lines)
     if 'symbol' in citation:
         symbol=citation['symbol']
         if not isinstance(symbol,str) or not symbol.strip():return 'UNRESOLVED','LOCATOR_UNRESOLVED'
@@ -96,6 +98,12 @@
         rows.append(row)
         if not isinstance(citation,dict):problem('CITATION_NOT_OBJECT',index);continue
         if set(citation)-{'source','quote','symbol','lines'}:problem('CITATION_FIELDS',index)
+        # Offline input is not protected by provider-side schema enforcement.
+        # Type/domain errors are formal failures, not independent position results.
+        if ('symbol' in citation and (not isinstance(citation['symbol'],str) or not citation['symbol'].strip())) or (
+                'lines' in citation and (not isinstance(citation['lines'],list) or len(citation['lines'])!=2 or
+                                        any(type(x) is not int or x<1 for x in citation['lines']))):
+            problem('CITATION_TYPE_INVALID',index);continue
         name=citation.get('source');quote=citation.get('quote')
         if not isinstance(name,str):problem('SOURCE_NOT_STRING',index);continue
         if name not in sources:problem('SOURCE_UNKNOWN',index);continue

```


### tests/test_citation_v2.py

Before `fea9a21ce275fde6c031021e95b57eaa8ab2bc2d605009b3ebffd41824081725`

After `9b3414f24639928f6d5a6243d4a3500465f0d82830e297bbf4778fdb3de926a7`

```diff
--- review06/tests/test_citation_v2.py
+++ review07/tests/test_citation_v2.py
@@ -61,8 +61,35 @@
             with self.subTest(value=value):self.assertIn(code,self.codes(self.run_case(dict(source='source.py',quote=value))))
 
     def test_invalid_line_and_symbol_locators(self):
-        for locator in (dict(lines=[True,5]),dict(lines=[5,4]),dict(lines=[0,4]),dict(lines=[1,99]),dict(lines='4,5'),dict(symbol=''),dict(symbol='missing')):
+        for locator in (dict(lines=[5,4]),dict(lines=[1,99]),dict(symbol='missing')):
             with self.subTest(locator=locator):self.assertIn('LOCATOR_UNRESOLVED',self.codes(self.run_case(dict(source='source.py',quote=self.quote,**locator))))
+
+    def test_locator_schema_violations_fail_mechanical_quality(self):
+        for locator in (dict(lines=[True,5]),dict(lines=[0,4]),dict(lines='4,5'),dict(lines=[1]),
+                        dict(lines=[1,2.0]),dict(lines=[-1,2]),dict(symbol=''),dict(symbol=['finish']),dict(symbol=None)):
+            with self.subTest(locator=locator):
+                r=self.run_case(dict(source='source.py',quote=self.quote,**locator))
+                self.assertEqual(r['mechanical_quality'],'FAIL')
+                self.assertIn('CITATION_TYPE_INVALID',self.codes(r))
+                self.assertEqual(r['citations'][0]['position_check'],'NOT_PERFORMED')
+
+    def test_physical_lines_match_ast_with_non_newline_separators(self):
+        for prefix in ('x=1\n\x0c','x="a\u2028b"\n','x="a\u0085b"\n','x="a\u2029b"\n'):
+            for ending in ('\n','\r\n','\r'):
+                with self.subTest(prefix=repr(prefix),ending=repr(ending)):
+                    text=(prefix+'def finish():\n    '+self.quote+'\n').replace('\n',ending)
+                    answer=dict(reuse_decision='RE_CONFIRM',evidence=[dict(source='source.py',quote=self.quote,symbol='finish',lines=[2,3])])
+                    r=v.evaluate(answer,{'source.py':text},self.oracle)
+                    self.assertEqual(r['citations'][0]['position_check'],'PERFORMED_MATCH')
+
+    def test_crlf_counts_as_one_line_and_quote_stays_raw(self):
+        for ending in ('\n','\r\n','\r'):
+            with self.subTest(ending=repr(ending)):
+                text=('def finish():\n    '+self.quote+'\n').replace('\n',ending)
+                answer=dict(reuse_decision='RE_CONFIRM',evidence=[dict(source='source.py',quote=self.quote,symbol='finish',lines=[2,2])])
+                r=v.evaluate(answer,{'source.py':text},self.oracle)
+                self.assertEqual(r['citations'][0]['position_check'],'PERFORMED_MATCH')
+                self.assertTrue(r['citations'][0]['raw_match'])
 
     def test_symbol_and_lines_must_intersect(self):
         r=self.run_case(dict(source='source.py',quote=self.quote,symbol='finish',lines=[1,2]))

```


### tools/codex_operations.py

Before `b5d00320f3885d0737ab9f22cd5318c4506cf95e047c02cdc6d180775401b691`

After `1ba781b28edf8fd5dc2ff03b17b92de116add3ebbf94a47bfeb7194d7dd8d64a`

```diff
--- review06/tools/codex_operations.py
+++ review07/tools/codex_operations.py
@@ -54,7 +54,7 @@
                 h.require(isinstance(active, dict) and isinstance(active.get('contract'), dict),
                           'Activation contract unavailable')
             except (OSError, ValueError) as exc:
-                raise h.HarnessError('Activation record unreadable; supply an explicit --contract with --refresh') from exc
+                raise h.HarnessError('Activation record unreadable or malformed; supply an explicit --contract with --refresh') from exc
             contract = contract if contract is not None else active['contract']
             if not refresh:
                 h.require(contract == active['contract'] and prior['task_contract'] == h.contract_hash(saved['task']),

```


### tests/test_explicit_refresh.py

Before `38d6ba9684808ea2376e3c98a7f0a9b1e9e6dae93eb78bf4824bf4b3661ad6a4`

After `f62068f0b84a8e01c906eb4174fe1d36927b50ed7fb3bb618b72d314a3b7f920`

```diff
--- review06/tests/test_explicit_refresh.py
+++ review07/tests/test_explicit_refresh.py
@@ -87,5 +87,15 @@
                 o.begin(self.root,'pilot',self.contract,True)
             activate.assert_not_called()
 
+    def test_explicit_refresh_with_new_goal_invalidates_old_contract_evidence(self):
+        first=o.begin(self.root,'pilot',self.contract);self.activation=first['activation'];self.run_check()
+        task=deepcopy(self.task);task['goal']='Changed objective from current user'
+        h.checkpoint(self.root,'pilot',task,1,'User changed objective')
+        current=o.begin(self.root,'pilot',self.contract,refresh=True)
+        self.assertEqual(current['freshness'],'CURRENT')
+        self.assertEqual(current['saved_context']['goal'],task['goal'])
+        self.assertFalse(current['verification']['mechanical_checks_pass'])
+        self.assertEqual(current['verification']['checks'][0]['status'],'STALE')
+
 
 if __name__=='__main__':unittest.main()

```


### agents/Codex/EVALUATION_V2_CONTRACT.md

Before `961fb3f2403c184894e5afb5c241348a4df7e875b201af5f15f86e7588916b9b`

After `c9118265a94229c8a38bf002a4230bd04a091453c23e8c3810f97f1ecf86af72`

```diff
--- review06/agents/Codex/EVALUATION_V2_CONTRACT.md
+++ review07/agents/Codex/EVALUATION_V2_CONTRACT.md
@@ -25,9 +25,14 @@
   reuse_decisionを評価前に検査し、契約不備は回答の失敗と区別して例外にする。
 
 CLIは明示したv2 answer/sources/oracleのJSONを読み、追加モデル呼出しをせず、
-`.harness-runtime/derived/citation-v2.0/<unique>/evaluation.json`へ新規保存する。
+`.harness-runtime/derived/citation-v2.1/<unique>/evaluation.json`へ新規保存する。
 schema・正確な入力text・oracle・options・評価器hash・結果を同梱し、既存結果は上書きしない。
 現行fixtureはsyntheticで、元の8回答をv2で再採点していない。
+
+v2.1ではlocatorの型・正整数制約も形式層で検査する。型違反はCITATION_TYPE_INVALIDで
+mechanical FAIL、未解決symbolや範囲矛盾は独立した位置結果として扱う。
+Pythonの物理行境界はCRLF/CR/LFのみとし、form feedやUnicode separatorを行数へ加えない。
+v2.0の保存結果は上書きしない。
 
 ## 次回比較の事前条件（未実行）
 
@@ -46,3 +51,9 @@
    宣言していない依存の変化はhash一致から検知できない、という限界を維持する。
 
 実装の回帰PASS、実作業での効果、Humanの採用判断は別々に報告する。M2/M3は未完了。
+
+品質確認は新ケースごとに対象成果物・重要制約・検証すべき振舞いを先に記述し、同じ入力の
+baseline/candidateを機械テストと原文レビューで比較する。必要に応じてHumanが意味と
+運用適合性を確認する。比較対象・入力・判定基準が一致しない場合、重大な差異が未解決、
+または標本が限定的で対象範囲の効果を判断できない場合は保留する。全反復の機械PASSや
+外部モデルの賛同だけでは無劣化を認定せず、結論の対象を確認したケースに限定する。

```


## 返答で確認してほしいこと

1. 型の形式FAILと位置の独立性が両立しているか。まだmechanical PASSになってしまう
   schema違反があれば具体的な入力・期待値・該当関数を示してください。
2. CRLF/CR/LFと特殊文字の座標修正で誤一致/誤矛盾が残るなら具体的な合法原文を示してください。
3. goal変更fixtureと品質確認手続きの追記が指摘の意図を満たすか。

各指摘に優先度・根拠・最小修正を付け、静的推論と実行済みの事実を区別してください。
重大な指摘がなければ「今回差分に重大な追加指摘なし」としてください。
一般性能改善や正式採用の承認は求めません。採否を左右する追加資料要求は最大3点。
回答は冒頭指定のMarkdownファイル形式で、末尾の終了マーカーまで含めて返してください。
