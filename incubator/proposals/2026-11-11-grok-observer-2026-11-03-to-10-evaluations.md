---
document_type: research_evaluation_batch
date: 2026-11-11
timezone: Asia/Tokyo
title: "Grok Observer 2026-11-03〜11-10: 19 intake records / 18 themes"
branch_target: development
source: Airtable / AI-Harness / Harness Inbox
intake_records: 19
unique_topics: 18
decision_counts: {CANDIDATE: 8, HOLD: 7, REJECT: 3}
evaluation_scope: current AI-Harness environment only
evidence_level: "Grok Observer secondary summaries; original sources not fully independently rechecked in this batch"
implementation: NOT_IMPLEMENTED
status_note: "Candidate labels reconstructed from preceding review; HOLD/REJECT are current provisional triage, not historic Human-confirmed dispositions"
---

# Grok Observer 2026-11-03〜11-10 — 未処理分のまとめて評価

## 保存の趣旨と制約
- **対象は個別技術18テーマ、元のAirtable19レコード。** Anthropic記憶研究は同じ一次資料を扱う2件を1テーマに統合。元IDを両方記載して取りこぼさない。
- 既存のAI-Harness（Core/Memory/Skills/Evaluation/各Project）に照らし、**技術・概念の参考価値と導入可否を分ける**。現行環境でのREJECTは技術一般の否定ではない。
- CANDIDATEの8テーマは前回評価で候補と確認できたもの。残り10テーマの**以前の個別HOLD/REJECT対応は履歴から完全には再現できなかったため、今回の暫定判断として明記**した。評価作業の履歴を捏造しない。
- 初期資料はGrok Observerの報告とリンク先。Observer側の「CONFIRMED」は第三者メモの評価であり、**今回の独立検証完了を意味しない**。数値・モデル性能・ライセンスは再検証が必要。
- **CANDIDATEは実装承認ではない。** 正式仕様、TRINITY sealed、プロジェクト本体、外部権限設定を変更しない。すべて研究待機。
- 同じ日付のKaggle研究: [Kaggle無料GPU研究](./2026-11-11-kaggle-free-gpu-benchmarks.md)。既存の記憶/権限/ブラウザ提案との重複は個別に精査する。

## 個別評価（簡潔な根拠と判断）
| テーマ | 当環境の判断 | 主要根拠 / 未確認事項 | 出典 / 元の取り込み記録 |
| --- | --- | --- | --- |
| **MS Agent Framework 1.25.0 adds MCP discovery approval policies** | **HOLD** (今回暫定) | Microsoft既存スタックに対するMCP承認ポリシーの参考にはなるが、現行TRINITYへの移植・回帰検証費用が未算定。 | [一次資料](https://github.com/microsoft/agent-framework/releases/tag/python-1.25.0) / [rec01AFfNBggmD0pW](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/rec01AFfNBggmD0pW) |
| **olcli MCP: server-side HITL confirmation via elicitation for all writes** | **CANDIDATE** (前回候補を引継ぎ) | 書込み直前に差分とHuman承認を要求し、拒否・タイムアウト時は無変更とする設計がHuman Authorityの強化に直結。Overleaf専用実装なので概念移植を対象。 | [一次資料](https://github.com/aloth/olcli/blob/main/docs/MCP.md) / [rec1Qnk5O4J9m0zTP](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/rec1Qnk5O4J9m0zTP) |
| **Engraphis bi-temporal grounded local memory for agents** | **CANDIDATE** (前回候補を引継ぎ) | 二時点管理・出典付き記憶・棄権はMemoryの誤記や履歴の混同対策に有益。作者報告の定量改善は未追試。 | [一次資料](https://github.com/Coding-Dev-Tools/engraphis) / [rec38sWSx4lecA36B](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/rec38sWSx4lecA36B) |
| **ha-mcp: MCP for Home Assistant with read-only, per-tool controls, edit backups** | **CANDIDATE** (前回候補を引継ぎ) | 読み取り専用・ツール個別制御・編集前バックアップを組み合わせる安全なMCP実例。Home Assistant機能の導入を意味しない。 | [一次資料](https://github.com/homeassistant-ai/ha-mcp) / [rec5oSfjnKiB9AqD6](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/rec5oSfjnKiB9AqD6) |
| **LocalHarness 0.27.6: OSS local LLM agent harness with permission gate** | **REJECT** (今回暫定) | 既存TRINITY/Orchestratorと広範に重複。移行・認証・権限検証の追加負担に対する実証済み優位性がない。 | [一次資料](https://pypi.org/project/localharness/) / [recJqUL6c7YoOUM3P](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recJqUL6c7YoOUM3P) |
| **strutil-core Ruby gem poisons AI agent MCP configs** | **HOLD** (今回暫定) | 依存パッケージ経由でエージェントのMCP設定と起動フックを改ざんする事例として有用。自環境での被害は未確認。 | [一次資料](https://socket.dev/blog/shai-hulud-descendant-malicious-ruby-gem) / [recKeWLJH1GDKwy2R](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recKeWLJH1GDKwy2R) |
| **Anthropic FlashProve: zk proofs of which model generated a response** | **REJECT** (今回暫定) | 生成元の暗号学的証明は研究価値があるが、現行家庭環境のGPU/運用目的と乖離し導入負担が大きい。 | [一次資料](https://github.com/anthropics/FlashProve) / [recMSunjpXmsuILbd](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recMSunjpXmsuILbd) |
| **Lucy Memory MCP: governed propose-only durable memory** | **HOLD** (今回暫定) | 記憶への直接書込みを禁じ、提案→審査→承認で永続化する発想は既存Human Authorityと重複。 | [一次資料](https://github.com/Lucy-AI-Inc/lucy-memory-mcp) / [recPJ3ayneZsXb7lD](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recPJ3ayneZsXb7lD) |
| **MCP tool bloat: prefer fewer tools and tool search** | **HOLD** (今回暫定) | MCPツール定義の増殖によるコンテキスト・選択誤差の注意喚起。ハーネスの既存Skillsオンデマンド設計と方向性が近い。 | [一次資料](https://x.com/HimanshuRawal05/status/2117533980006203461) / [recRJodmfsLSprvLk](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recRJodmfsLSprvLk) |
| **Anthropic agent memory components + dreaming correction** | **CANDIDATE** (前回候補を引継ぎ) | 生ログ・要約メモ・索引・注入文脈の役割分離と、原記録に照らして修正するオフライン整理がMemoryの堅牢化に寄与。 | [一次資料](https://www.anthropic.com/research/components-of-agent-memory) / `reccxYK9dq7gUxOyP`, `recsuCQsWdBVY3lXx` |
| **OmniMem: self-hosted semantic memory MCP with experience scoring & failure graveyard** | **CANDIDATE** (前回候補を引継ぎ) | 失敗事例の保持、反証・競合の扱い、経験を技能候補に変換する手法が『不採用も残す』方針に合致。ベンチ値は未検証。 | [一次資料](https://omnimem.org/) / [recdh1xHCU0PSbK7I](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recdh1xHCU0PSbK7I) |
| **AgentCap: Capability-based runtime authorization for LLM agents via MCP** | **CANDIDATE** (前回候補を引継ぎ) | 短命・予算上限付き能力トークンをモデル外で検証する手法がツール権限の安全強化候補。論文の再現性は未確認。 | [一次資料](https://arxiv.org/abs/2611.00729) / [recfqGWbEwM9x2YRA](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recfqGWbEwM9x2YRA) |
| **Murmury: OSS local Mac meeting assistant with Ollama** | **REJECT** (今回暫定) | Mac会議支援の個別用途で、AI-Harness Core/BBB等の現在要件との直接関係が薄い。 | [一次資料](https://github.com/GianlucaBave/murmury) / [recjPSJlWU9mI5Loj](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recjPSJlWU9mI5Loj) |
| **krusch-context-mcp: 5-verb local SQLite memory MCP** | **CANDIDATE** (前回候補を引継ぎ) | 5操作に絞る低トークンMCPと時系列の失効管理は小規模Memory検証向き。発表された高ベンチマークは独立未確認。 | [一次資料](https://github.com/kruschdev/krusch-context-mcp) / [recjp84zv7OmqNddF](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recjp84zv7OmqNddF) |
| **OpenCode Browse: MCP real-browser control with HITL handoff** | **HOLD** (今回暫定) | 既存ブラウザとログインを扱えるが、認証セッション・閲覧権限の露出面が増える。既存操作経路と比較が必要。 | [一次資料](https://opencode.ai/product/browse) / [recn0ckL4HzHEIUKb](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recn0ckL4HzHEIUKb) |
| **Vercel agent-desktop: a11y-tree computer use CLI + MCP** | **HOLD** (今回暫定) | アクセシビリティツリー方式は画面操作の低トークン化候補。OS別権限、UIへの誤操作、既存環境との差は未実証。 | [一次資料](https://github.com/vercel-labs/agent-desktop) / [reco0YKlThJI3gQWD](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/reco0YKlThJI3gQWD) |
| **MCPHallu: Benchmark for MCP Agent Hallucinations** | **CANDIDATE** (前回候補を引継ぎ) | MCP失敗・到達不能な目標・偽成功を測る評価セット。TRINITYの完了判定とfail-closed試験の強化候補。 | [一次資料](https://arxiv.org/abs/2611.07689) / [recpy7y3vkLvYBy0y](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/recpy7y3vkLvYBy0y) |
| **Mainplane: OSS multi-PC agent harness with retrieval over compaction** | **HOLD** (今回暫定) | 圧縮より原履歴検索を優先する設計は有益だが、常駐サーバー・複数端末管理と現行TRINITYが重複。 | [一次資料](https://github.com/mainplane-ai/mainplane) / [rectHcJpkLz125eeN](https://airtable.com/appfyC1xCHDTCsz7V/tbl887BSk3xoO2QQQ/rectHcJpkLz125eeN) |

## 再評価する条件
- **MS Agent Framework 1.25.0 adds MCP discovery approval policies**（HOLD）：既存承認ゲートと機能差を実装・テストで確認できたとき。
- **olcli MCP: server-side HITL confirmation via elicitation for all writes**（CANDIDATE）：独立の権限制約テストとfail-closed検証。
- **Engraphis bi-temporal grounded local memory for agents**（CANDIDATE）：既存Memoryとの検索精度/更新履歴/小規模運用比較。
- **ha-mcp: MCP for Home Assistant with read-only, per-tool controls, edit backups**（CANDIDATE）：権限境界とバックアップ復旧の小規模再現試験。
- **LocalHarness 0.27.6: OSS local LLM agent harness with permission gate**（REJECT）：隔離比較で明確な安全性・効率優位が出た場合。
- **strutil-core Ruby gem poisons AI agent MCP configs**（HOLD）：監査ルールや実際の影響範囲の確認が必要なとき。
- **Anthropic FlashProve: zk proofs of which model generated a response**（REJECT）：軽量CPU検証や実用OSSが整備された場合。
- **Lucy Memory MCP: governed propose-only durable memory**（HOLD）：既存Memory管理にない監査可能性が立証された場合。
- **MCP tool bloat: prefer fewer tools and tool search**（HOLD）：自環境でトークン・成功率の実測差が出た場合。
- **Anthropic agent memory components + dreaming correction**（CANDIDATE）：sealed原本不変のまま夢見処理の検証。
- **OmniMem: self-hosted semantic memory MCP with experience scoring & failure graveyard**（CANDIDATE）：権限管理と記憶肥大化を抑えた局所ベンチ。
- **AgentCap: Capability-based runtime authorization for LLM agents via MCP**（CANDIDATE）：現在のHuman承認・writer lockとの境界比較。
- **Murmury: OSS local Mac meeting assistant with Ollama**（REJECT）：家族・仕事向けオフライン会議補助の具体要件が発生した場合。
- **krusch-context-mcp: 5-verb local SQLite memory MCP**（CANDIDATE）：自環境で精度と実測トークンの比較。
- **OpenCode Browse: MCP real-browser control with HITL handoff**（HOLD）：最小権限・Human handoff・セッション隔離が検証できた場合。
- **Vercel agent-desktop: a11y-tree computer use CLI + MCP**（HOLD）：Windows/Macで読み取り専用試験と安全ゲートを整備した場合。
- **MCPHallu: Benchmark for MCP Agent Hallucinations**（CANDIDATE）：ライセンス・課題再現性確認後に限定したテストを実施。
- **Mainplane: OSS multi-PC agent harness with retrieval over compaction**（HOLD）：運用管理負担と長期記憶精度で定量優位が得られた場合。

## 保存・反映ルール
- CANDIDATE 8件: この統合研究ノートを当面の正本とする。独立検証で優位性が出たものだけ個別proposalへ昇格する。
- HOLD 7件: 採用せず、上表の出典/保留理由/再評価条件を検索可能に保存。
- REJECT 3件: 再検討に必要な最小事項のみ `research/TECHNOLOGY_DECISIONS.md` に登録。この表を詳細な不採用レビューとして拡充しない。
- 重複: Anthropic memory 2記録を1件に統合。その他の機能重複は既存提案と照合し、実装前に重複検証を必須にする。
- Airtableは取り込み・確認状況に限定し、上表の評価本文を転載しない。

*Research only / no code, permission, policy, or runtime implementation changes.*
