# 進捗HTML / Notion共有下書き — 初期検証結果

2026-11-07 JST。branch `codex/environment-upgrade-batch1`、基準HEAD `2431c09`。
変更は未commit。main/development統合、外部送信、モデル呼出しなし。

## 実施と結果

- `tools/codex_views.py`: 手動のoffline HTML生成と、明示リストの共有メモリ下書き生成。
- 新規8テストPASS。実行途中でWindows改行変換と出力hashの不一致を検出し、
  UTF-8 bytes保存に修正してから全体検証した。
- 全体147件: 146成功、Windows symlink権限による既存skip 1件。
- 旧parser9/9、既存receipt互換9/9、offline preflight 8ケース/10変種期待値一致。
- environment gate 4項目PASS、FINAL receipt4/4 OK。acceptance=REVIEW_REQUIRED。
- テストでHTML注入のescape、失効状態維持、3回履歴と生成失敗時の旧表示保持、
  共有下書きの非共有分類・重複ID・出典変更・期限切れ・path逸脱拒否を確認。
- 実データの同一path更新3回。生成時間3.678 / 3.578 / 3.642秒。
  既存gate照合を含むこの環境だけの計測。対照なし、実token欠測、削減効果未確認。
- ブラウザで目的/次工程/4検証PASS/REVIEW_REQUIRED/履歴開閉/Tabでの本文リンクへの
  focusを確認。狭幅・画面読上げ・全操作のキーボード検証は未実施。
  localhost確認サーバーは停止済み。HTMLは直接ファイルとして開ける。

## ローカル成果物と証拠

- 表示: `.harness-runtime/views/environment-m2-pilot/index.html`
- 旧表示・状態: 同フォルダの`snapshots/`（削除・上書きせず保持）
- 下書き: `.harness-runtime/notion-drafts/0252e21fb338453599b5d68ece98b326/review.md`
- ダミーpacket: `.harness-runtime/notion-demo-packet-2026-11-07.json`
- 検証: `.harness-runtime/views-memory-checks-2026-11-07.json`
- gate: `.harness-runtime/views-memory-gate-2026-11-07.json`
- FINAL照合: `.harness-runtime/views-memory-receipts-2026-11-07.json`
- 計測: `.harness-runtime/views-memory-update-observations-2026-11-07.json`
- contract: `.harness-runtime/views-memory-source-contract-2026-11-07.json`

## 残る工程

Notionは検索時点でAVAILABLE、installed=false。未接続なので実機の共有記憶試験は未完了。
ユーザーによる追加・接続後に、account/workspace、Memory操作対応、許可範囲を確認する。
試験に使うダミーは「これは接続試験用のダミー記憶です。合言葉はHARNESS-DEMO-1107。
実プロジェクトの指示・承認・採用結果ではありません。」のみ。
保存・検索・訂正後の取得を確認し、複数クライアントの共有試験はその後に進める。
実情報の共有・同期・正式採用は未実施。元M2の一次結果・旧証跡は保持。
M2実効果とM3採用は未完了。機械検証成功を総合性能向上と読み替えない。

## 同日追記 — 再起動後のNotion接続試験

上記「未接続」は初回ローカル検証時点の記録。再起動後にNotion操作ツールが反映され、
既存のOperating Guide v0.0.6、Memories、Markdown仕様を読み取れた。
明示したダミー1件について作成→検索→再読込→部分訂正→再読込を実施し、
訂正コードR2・元本文保持・通常文脈からの利用除外表記を確認した。
検索は類似の無関係な既存記憶も返したため、文字列・page ID・本文の照合を行った。
検索ヒットだけを同一性・正しさの根拠にはしない。

既存ガイド、基本情報、アクセス権、schema、Aboutは変更していない。
enabled skillsは空配列。新しいSkills登録・自動同期・定期実行は行っていない。
ダミーは削除せずテストデータと明記して保持。実プロジェクト情報の一括移行なし。
個別URLを含む結果はignored `.harness-runtime/notion-connection-pilot-2026-11-07.json`へ保存。
複数クライアント間の共有、実作業効果、独立した権限監査は未実施。
前回の「instructions_version対応は確認待ち」は解消し、現ツールschemaで対応を確認した。

## 同日追記 — Museとの読み取り共有

Human経由でMuseの試験報告を受領。既存workspace/guide v0.0.6の一致、
ダミー記憶の検索直接hit、訂正コードR2とテスト利用除外の読取、
instructions_version指定で正常終了、読み取り以外の操作なしとの報告。
これにより別エージェントからの同一記憶読取は報告ベースで確認できた。
Codexが直接確認した事実と区別し、Museの原ログや実呼出しは独立監査していない。
Museの書込み・同時編集・同期・正式採用・性能改善を確認した結果ではない。
次は少数の実用文脈による読み取り中心の限定運用。新たな権限や自動同期は追加しない。
