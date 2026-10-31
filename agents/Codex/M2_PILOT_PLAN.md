# M2初回比較 — 実ソースの読み取り診断

2026-10-31。実装の追加より、まず実usageと診断品質を観測する。

対象trial: `.harness-runtime/m2-pilot/de2c3845e526423b815fcd4836eed423/`。
plan、oracle、入力、grader/runner、ソースhashはモデル呼出し前に保存した。
準備済み旧trial `c0fb6ae43e2241f99166df17b5d8292f` は未実行。評価コードの固定を加えたため新trialを使用する。

## 今回の3作業

1. 実際に確認した2つの監査を同条件で比較し、品質と実usageを取得する。
2. 各ペアの値・欠測・ばらつきを評価し、採用と追加評価を区別する。
3. 再現したfinish後のbegin不具合を、凍結した比較が終わってから最小修正・回帰検証する。

## 凍結した比較条件

- CLI `0.165.0-alpha.1.2`、binary SHA固定。
- 要求モデル `gpt-6.1-sol`、推論強度high。ローカルbundled catalogでサポートを確認。
- 2ケース×baseline/candidate×2反復、最大8回。ケースごとに順序を交互にする。
- baselineは関連7ファイル全体、candidateは必要関数をASTで選択した原文。
  元のソース版・質問・schema・重要制約・観測ログは同一。
- 明示的なユーザーの重要条件は両方式とも原文で保持する。
- 分析対象はCodexというsystem-under-test。実装担当のsubagentは起動しない。
  shell/exec/multi-agent/apps/plugins/memory機能を呼出し単位で無効化し、ツール使用が
  eventsに現れた場合は試験を無効化して停止する。
- read-only sandbox、ephemeral、user configを読まない試験プロセス。
  project_doc_max_bytes=0として、試験用に渡したpacket以外のAGENTS注入を抑える。
  hostのsandbox/承認やglobal設定は変更しない。規則ファイルを無視するflagは使わない。
- 既存ChatGPT認証を使用。API key環境変数は子へ渡さない。既存Codex利用枠を使用する。
- 1呼出し180秒。基盤失敗・不正なevents・重大な権限誤判断では停止し、自動再試行しない。

入力bytes（表示量であり実tokensではない）:

| ケース | baseline | candidate |
|---|---:|---:|
| checked-reentry | 82,568 | 17,203 |
| runtime-drift | 82,584 | 17,896 |

## ケースと先に固定した判定

**checked-reentry**: 実コードを隔離fixtureでbegin→verify→finish→beginと実行し、
`First begin requires an explicit --contract`を確認した。
期待診断はREENTRY_CONTRACT_GAP、対応は保存済みcontractの再利用と鮮度/目的の再確認。
現行コードを無断変更した状態で比較しない。

**runtime-drift**: 現行のPASSに対して、隔離プロセス内だけでPYTHONPATHを変えた
負例を作り、gateのNOT_CURRENT / Runtime changedを確認した。
期待診断はRUNTIME_DRIFT、対応は現環境での再検証。
恒久的な環境変更や実データ破損は起こさない。

両ケースでCodex環境整備という主目的、4つのHuman承認境界、正式採用・一般性能向上を
主張できないことを確認する。証拠引用は凍結した原文とliteral一致を検査する。
自由記述全体の正しさや一般開発能力を自動認証する判定ではない。

## 計測と判断

turn.completedの実input/output tokensを保存し、合計はinput+output。
cached inputとreasoning outputは内数なので再加算しない。料金やquotaとは区別する。
wall-clockはCLI起動/待ち時間も含む。生JSONL・stderr・回答を保存する。
要求モデル/effortは固定するが、backendの実効identityは独立認証できない。

2反復のtext-only監査でM2全体やM3を完了にしない。実装・長時間継続・実際のcontext
compaction・複雑な開発品質を測る試験ではない。candidateの品質後退や時間悪化を平均に隠さない。
モデル不調・不正出力・欠測も結果として保持する。失敗しても別条件へ黙って差し替えない。

実行方法は[公式Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)と
[公式設定リファレンス](https://learn.chatgpt.com/docs/config-file/config-reference)、ローカルCLI helpで確認した。
これらの仕様は本試行の効果や将来性能を保証しない。
