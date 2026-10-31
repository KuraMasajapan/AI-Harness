# Fugu Maxへの外部レビュー依頼 — 2026-10-31

このファイル全体を、新しいFugu Maxの会話へ渡してください。
回答は編集せず、そのままCodex側へ戻せる形式でお願いします。

---

あなたはCodex環境整備の外部レビュアーです。以下の資料から、評価設計・原因切分け・
最小修正の妥当性を検討してください。Codexの暫定結論への反証も歓迎します。
今回は推論・提案までを依頼します。追加のモデルAPI呼出し、公開、実環境変更は不要です。
資料にないコード・ログ・実効モデル構成を確認したとは言わず、必要な追加資料を指定してください。

## 目的と制約

- 主目的はCodexの安定性、検証精度、速度、重要コンテキストの保持、token効率の改善。
- 現在の品質を落とす削減策は採用しない。改善は3件ずつ比較・検証する。
- TRINITYは必要な評価・検証の補助。TRINITY単体開発を主目的へ置き換えない。
- ローカルの試行ブランチで運用中。公開、main統合、本番移行、既存証跡削除はHuman事前承認。
- 元の試行結果は保持する。後から基準を変えて元のFAILをPASSへ書き換えない。

## 今回お願いしたい3点

1. 出典の表記と採点契約に関する不備の、再発防止と次回の評価設計。
2. tokensが減ったのに応答時間が延びた観測の、原因候補と切り分け順。
3. 有効な証拠の再確認と検査の再実行を区別し、余分な再検証を抑える条件。

## 実験の事実

実際の未commitコードを凍結し、2つの読み取り監査を比較した。

- checked-reentry: begin→verify→finish→beginの再開不具合を、隔離fixtureで再現して診断。
- runtime-drift: 保存済みPASSに対し、隔離プロセス内だけでPYTHONPATHを変え、
  gateのNOT_CURRENT / Runtime changedを作った負例の診断。

比較対象:

- baselineは関連7ファイル全体。candidateは事前に選んだ関数のAST原文と必須資料。
- 同じ元ソース・質問・schema・観測・重要条件。関数選択は実験者が事前定義した。
- これは自動探索の能力比較ではなく、ソースの提示範囲を変えたtext-only診断。
- CLIバージョン、binary、要求モデルgpt-6.1-sol、推論強度highを固定。
- read-only、ephemeral。shell/exec/multi-agent/apps/plugins/memory機能は呼出し単位で無効。
- ツール使用はeventsに検出されなかった。実装作業や実際のcontext compactionは測っていない。
- ケースごと2反復、計8回。順序を交互にし、自動再試行なし。
- 要求したモデル/effortのbackend実効値は独立認証できない。
- 下の秒数はCLI起動・待機を含む。packetの選択・準備時間や全作業時間は含まない。

| 順序 | ケース | 方式 | 反復 | input | cached input（内数） | output | input+output | 秒 | 元grader |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | checked-reentry | baseline | 1 | 33539 | 0 | 874 | 34413 | 16.841 | PASS |
| 2 | checked-reentry | candidate | 1 | 18040 | 0 | 927 | 18967 | 21.282 | PASS |
| 3 | checked-reentry | candidate | 2 | 18040 | 0 | 1200 | 19240 | 32.495 | PASS |
| 4 | checked-reentry | baseline | 2 | 33539 | 0 | 1041 | 34580 | 24.827 | FAIL |
| 5 | runtime-drift | candidate | 1 | 18170 | 0 | 551 | 18721 | 13.226 | FAIL |
| 6 | runtime-drift | baseline | 1 | 33543 | 11520 | 668 | 34211 | 16.428 | FAIL |
| 7 | runtime-drift | baseline | 2 | 33543 | 0 | 594 | 34137 | 14.815 | FAIL |
| 8 | runtime-drift | candidate | 2 | 18170 | 0 | 564 | 18734 | 13.596 | FAIL |

各方式4回答の合計はbaseline 137,341 tokens / 72.91秒、candidate 75,662 tokens / 80.60秒。
tokensは44.91%減、時間は10.55%増。ただし小標本で、ケース別の速度差の方向も異なる。
cached inputとreasoning outputを合計へ再加算していない。料金・quotaは測っていない。
全8回で共通のPowerShell shell snapshot非対応警告があった。機能失敗は起きていない。

## 問題1: 出典契約と採点

実行前のschemaは次の形式で、sourceを任意文字列としていた。

```json
{"source": {"type": "string"}, "quote": {"type": "string"}}
```

promptは「原文の12文字以上のsubstringを引用」と指示したが、sourceに関数名・行番号・
JSON位置を添えることを明示的には禁止していなかった。graderの関連部分は以下。

```python
if not citations or not any(c.get('source') == oracle['required_source'] for c in citations):
    problems.append('required_source')
for citation in citations:
    quote = citation.get('quote', '')
    name = citation.get('source')
    if not isinstance(quote, str) or len(quote.strip()) < 12 or name not in sources or quote not in sources[name]:
        problems.append('fabricated_or_incomplete_evidence')
```

期待sourceが`tools/codex_operations.py`のとき、例えば以下の回答もFAILになった。

```json
{
  "source": "tools/codex_operations.py: begin",
  "quote": "if prior and prior['state'] == 'OPEN':"
}
```

このquoteは凍結原文に存在する。関数名/JSON位置を添えた参照を別途解決した事後auditでは、
全8回答の全quoteがそれぞれの原文中に存在した。診断・主目的・承認境界のコードも期待と一致。
ただし、これは自由記述全体や意味の正しさの認証ではない。元の採点は変更していない。

現時点の対応は、今後用のschemaでsourceを正確なファイル名のenumにし、
promptにもsuffix禁止を明記すること。修正版で追加のモデル試行は行っていない。

検討してほしいこと:

- モデルの事実誤り、引用場所の表記揺れ、評価契約の不一致をどう別々に判定するべきか。
- exact source enumと、source_path/locator/quoteを分離する設計のどちらが適切か。
- literal一致でも無関係な箇所を引用できる。意味・位置・必要sourceとの関係をどう検証するか。
- 元結果を保持したまま、派生する検査結果と将来の新評価をどう版管理するか。
- 正例と負例を少数で挙げてほしい。出典の曖昧な自動補正で誤引用を正当化しないこと。

## 問題2: 速度の原因は未特定

Codexの現在の結論は「token数だけでは採用できない。速度悪化と品質判定不足があるため保留」。
cache差、待機、推論/出力量、source提示の違い等は原因候補であり、確定原因ではない。

検討してほしいこと:

- 上の実測から言えること/言えないこと、原因候補の優先順位。
- 原因を区別できる、最小の追加計測と比較条件。まず既存ログでできる分析を優先すること。
- 次回必要な計測値と、取得できないときの扱い。今回の値から推定した事実を捏造しないこと。
- 正しさや速度を落とさずtoken効率を判断する、限定採用/保留/不採用の条件。

## 問題3: gateの再確認と検査の再実行

この環境の考え方は以下。

- source、task契約、runtime、出力log、receiptが同一で有効なら、既存証拠をgateで再確認できる。
- next_stepだけの変更は検証契約を変えない。目的や重要制約の変更は別扱い。
- stale/missing/corruptな証拠を使い回さない。機械PASSと意味の正しさ/Human承認も区別する。
- 新しいユーザー指示と保存状態の照合は必要。hash一致だけで現依頼を理解したとはしない。

candidateのcall 2には、次の記述があった。

> Rerun current verification and retain human review; do not carry forward the old PASS.

有効な証拠まで常に再実行するなら効率を落とす。今回のSUTは推奨を返しただけで、
実際に余分な再検証を実行した回数や人の負担は測っていない。

関連する実不具合は修正済み: 旧beginはOPEN時だけ保存contractを取得していたため、
finishによるCHECKEDの後にbegin(task)が未指定エラーになった。
修正では、保存contract取得とsource/task照合をCHECKEDにも適用し、OPENの再利用だけを分岐した。
source/目的の変更は引き続き明示refreshを要求する。4回帰は修正前失敗→修正後成功。
全体は97件中96成功・1skip、評価parser9成功、receipt9成功。意味検証の代用にはしない。

検討してほしいこと:

- 再確認だけでよい条件と、再実行が必要な条件の具体的な判定表。
- 新依頼・目的変更・環境変化・中断・進捗メモのみの更新に対する正例/負例。
- 不要な再検証を減らしても、古いPASSを流用しない仕組みの不足がないか。

## 返答形式

まず3点の結論を短く示し、その後、次の表で回答してください。

| 対象 | 確認できる事実 | 仮説/未確定 | 推奨する最小修正 | 正例/負例テスト | 残るリスク |
|---|---|---|---|---|---|

最後に、優先する変更を3件以内で挙げ、各変更に「なぜ先か」「どの証拠で合格とするか」を付けてください。
追加資料が必要なら最大3点に絞り、ファイル名/必要な関数やログ範囲/確認目的を指定してください。
外部モデルの回答や多数決を、正しさや採用承認の証拠として扱わないでください。
