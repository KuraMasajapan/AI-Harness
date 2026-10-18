# RTK (Rust Token Killer) — Codexコマンド出力の圧縮によるコンテキスト節約

- Date: 2026-10-18
- Status: HOLD / NOT IMPLEMENTED
- Stage 1 (provisional): A+
- Stage 2 (research rank): A
- Evidence: CONFIRMED (ツールの存在・公式記載の機能) / UNVERIFIED (投稿の93.1%という一般化された削減効果)
- Scope: AI-Harness / Codex / Developer Tools / Evaluation
- Dedup: RELATED EXISTING — Airtable「Token Harness v0.1.31」(2026-10-10) がRTK統合を言及。RTK単体の過去評価は未確認。
- Recall Triggers: RTK, Rust Token Killer, Codex, token optimization, output compression, Token Harness, logs, git diff

## 入力情報・主張

2026-10-18にX投稿が共有された。「Codex 6.1のトークン消費を最大93.1%削減」「Git操作・テスト・ビルド・エラーログの出力を自動圧縮」「Codexに導入を任せられる」と主張。共有文中のXリンクは省略形のため、投稿本文全体や93.1%の測定条件は独立確認できていない。

## Stage 1 — 一次評価（暫定 A+）

コマンド実行結果によるコンテキスト圧迫への対策として、AI-HarnessのCodex利用に関連性が高い。調査優先度A+。この段階では効果・安全性を未確定とする。

## 詳細調査 — 一次資料

公式候補: https://github.com/rtk-ai/rtk

公式README（2026-10-18確認）により、以下の機能説明を確認：
- Rust製CLIがシェルコマンド出力をフィルタ・集約・切り詰め・重複排除する。
- `git status`, `git diff`, `git log`, テスト結果、検索結果等を短縮する。
- Codex向け初期化 `rtk init -g --codex` が記載されている。ただし**未実行**。
- READMEはbash出力の圧縮を最大90%程度と説明し、**セッション全体のトークン数や請求額が同率で減るとは主張していない**。絶対トークン数は `bytes / 4` による概算と記載。
- シェルフックが対象であり、すべての組み込みツール呼び出しが自動で圧縮されるわけではない。
- ライセンスは配布形態によってApache-2.0とBUSL-1.1が関係する。導入前に利用形態を確認する。

**注意**: READMEの説明が存在することと、独立した実測による効果の確認は別。93.1%という数値の測定条件、Codex 6.1での再現性、品質維持は未検証。

## 既存研究との重複

Airtable Harness Inboxに「Token Harness v0.1.31 OSS for Codex/Claude rate limit maximization」（2026-10-10、記録ID `recj48MB78ZJcq9vr`）があり、RTK等の統合に言及している。RTKの採用・単独評価が完了していたという証拠ではない。GitHubのデフォルトブランチに対する `rtk` コード検索は一致なしだが、`development` 全体を網羅した検索ではないため「新規確定」とはしない。

## Stage 2 — 二次評価（A / HOLD）

**期待効果**: ログやテスト出力のコンテキスト使用量削減。長時間のCodex作業で有益な可能性。

**重複・代替**: Token Harnessが既にRTK統合候補として存在。まず単体RTKの必要性と既存ツールとの差を確認する。

**主要リスク**:
- 省略されたエラー行、差分、テスト出力が原因究明・検証証拠・Trinity等の比較に必要な場合、判断品質を損なう。
- フックやコマンド書換えが既存のCodex運用・セキュリティ境界に干渉する可能性。
- 配布形態・ライセンス・更新運用の確認が必要。

**評価**: 実在性と用途は確認できるが、投稿の「最大93.1%削減」をCodex全体の消費量に適用する根拠は不足。安全な再現テストまで **HOLD / NOT IMPLEMENTED**。

## 将来の最小検証案（未承認・未実施）

1. 既存のCodex環境を変更しない隔離環境で、同一のGit操作、テスト、ビルド、意図的なエラーをRTKあり／なしで比較。
2. コマンド出力の文字数・概算トークン数と、可能ならセッション全体の実測トークン数を**別々に**測る。
3. エラー原因特定、失敗テスト特定、重要差分の保持、復元手順、ログ完全性を比較。
4. Token Harnessを含む既存候補との重複と追加価値を判断。
5. Humanの明示承認なしにインストール、フック変更、Core変更、正式採用はしない。

## 保存境界

本ファイルは研究記録。GitHubへの保存は導入・自動実行・Codex設定変更・Coreへの昇格を意味しない。
