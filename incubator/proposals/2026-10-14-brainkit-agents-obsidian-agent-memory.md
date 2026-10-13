---
status: proposal
created: 2026-10-14
origin: Human shared https://www.npmjs.com/package/brainkit-agents and its README
stage_1_rank: A+
stage_2_rank: A
evidence_status: CONFIRMED (repository, source implementation) / UNVERIFIED (production reliability, incremental advantage)
decision: CANDIDATE
implementation: HOLD
tags:
  - memory
  - obsidian
  - claude-code
  - hooks
  - context-recovery
  - agent-handoff
  - human-approval
trigger_topics:
  - brainkit-agents
  - brain-kit
  - Obsidian Vault memory
  - Claude Code SessionEnd
  - context compaction
  - core reread
  - runtime context recovery
  - agent memory persistence
  - multi-persona
---

# brainkit-agents — Obsidian Vaultを使うAgent記憶の継続性

## Human decision and scope
- 2026-10-14、Humanが「ここまでの優良なものを保存」と指示。研究候補としての保存を承認。
- **導入・実装・Core変更・既存Vaultの編集は未承認。HOLD**。
- 記憶システムを増やすこと自体は目的ではない。既存GitHub/Obsidian/AI-Harnessで不足が測定された場合だけ参考にする。

## Source / provenance
- npm: https://www.npmjs.com/package/brainkit-agents
- GitHub: https://github.com/chocochocopipip/brain-kit
- 確認時のリポジトリの `package.json`: `brainkit-agents`, 12.0.0, MIT (2026-10-14閲覧)。
- 重要: `@2brain/brainkit` (https://github.com/oribarilan/brainkit) は**名前の似た別OSS**。混同しない。
- 原典READMEおよび `claude/hooks/session-end-brain.sh`, `claude/hooks/brain-digest.js`, `claude/hooks/brain-kit-core-reread.py`, `claude/skills/partner/SKILL.md` のコードを確認した。実機導入や独立動作検証は未実施。

## Confirmed mechanism (公式実装として確認)
1. Claude Codeの四役: Partner（Vault記憶・相談）、Dev（Issue→PR）、Review（版管理された基準で審査）、Release（明示的なラベル＋指示を条件にmerge/deploy）。Git worktreeとGitHubラベルで役割間を受け渡す。
2. **SessionEnd hook**: トランスクリプトをダイジェスト化し、標準ではHaikuの `claude -p` に「やったこと／決定事項／未解決事項」を要約させ、Vaultの `daily/YYYY-MM-DD.md` に追記・Git commit。要約が失敗したら依頼一覧を記すフォールバック。
3. **起動時の再読込**: Partnerは基本方針・辞書・関係・最近の日誌・対象Project状態を読み込むようSkillに規定。
4. **文脈圧縮後の再読込**: `SessionStart(compact)` hook が担当人格の `00_核.md` 等をその時点のVaultから読み、現在のコンテキストへ渡す。ファイル単位32KiB、合計64KiBの上限などをコードで確認。
5. **承認境界**: `agent-ready`ラベルや権限ダイアログはHuman側に保持。リリースには別途条件を設ける。ただし記憶ノートの自動追記・自動コミットまで常時Human確認される仕組みではない。
6. README記載のWindows利用はWSL経由。Claude Code CLIが前提。任意のOrca/Tailscale常駐・Codex統合はコア記憶機能とは別。

## Important limits and risks
- **記憶の完全性は保証されない**: digestは最大60,000文字等の上限を持ち、過大な履歴は中間省略。要約の誤り・重要判断の欠落・後日の検索失敗はあり得る。
- **自動コミットの副作用**: `session-end-brain.sh` に `git add -A` があり、Vault内にある他の未コミットファイルも含め得る。秘密情報・プライベートVaultへの適用前にスコープと承認境界を精査する必要。
- **計算コスト**: セッション終了ごとの要約モデル呼出しはゼロコストを保証しない。Haikuが標準だが実利用課金・認証・CLI制限等は環境次第。
- **運用負荷**: 四人格・worktree・hooks・Git/Claude CLI・オプション母艦は既存Harnessの機構と広く重複。外部コード実行と権限昇格に伴う攻撃面を増やす。
- **実証の境界**: リポジトリの説明、コード、テストの存在はCONFIRMED。一方、毎回の要約正確性、リカバリ成功率、既存Harnessより高品質であることはUNVERIFIED。

## AI-Harness existing assets and overlap
- `HARNESS.md`: Bootstrap / Revalidation、宣言的ルールと実行時読込の区別が既に存在。
- `core/ACCESS.md`: Shared/AI-specific/Private分離、最小権限、Human最終承認。
- `incubator/proposals/2026-09-21-obsidian-integration-stack-candidates.md`: Obsidian CLI等を優先する既存方針。
- `incubator/proposals/2026-09-21-obsidian-integration-adoption-triggers.md`: 実際の必要が生じたら小さく評価する採用トリガー。
- `incubator/proposals/2026-10-12-claude-mem-persistent-context.md`: 会話記録・永続コンテキストの重複候補。
- `incubator/proposals/2026-09-20-role-pattern-library.md`: 外部の四役構造は原則の部品として比較し、全面移植しない。
- `incubator/proposals/2026-10-14-tacit-domain-knowledge-history-mining.md`: 履歴から暗黙知を発見する研究と関連するが、単なるSessionEnd要約では代替できない。
- **独自性として保存する点**は「セッション終了時の実行トリガー」「compaction直後の明示的なコンテキスト再注入」を結ぶ**具体的なコード実例**。

## Future minimal evaluation (NOT STARTED)
1. 本当に「記憶を保存したのに再開後のAIに反映されなかった」という再現例が発生した場合に限る。
2. Core/現行プロジェクトを変更せず、公開ダミー資料を使う隔離Vaultで記憶の正確性・欠落・誤記を測定。
3. compaction前後に重要ルールの再取得有無・正しい適用・プロセス終了後の復元を照合。
4. Hookによるモデル呼出し・token・時間、書込み範囲、意図しないコミット、Human承認負荷を計測。
5. Obsidian CLIや既存GitHub/Bootstrapの最小構成でも同じ課題を解決できないか比較する。
6. 成果があれば必要な小機能だけ独立提案し、Humanの別承認を経て採否判断。自動commitや人格のフル導入は既定で拒否。

## Assessment / recall
- Stage 1: **A+** / Stage 2: **A**。
- Evidence: **CONFIRMED** (official code supports described hooks and organization) / **UNVERIFIED** (independent effect and benefit to Harness)。
- Decision **CANDIDATE**, Implementation **HOLD**。
- Recall when: Vaultの記憶欠落、再開時の不整合、compaction後のルール忘却、セッション間引継ぎ、保存済み記憶の実行時有効化、Codex/Claudeを跨ぐ記憶比較。
