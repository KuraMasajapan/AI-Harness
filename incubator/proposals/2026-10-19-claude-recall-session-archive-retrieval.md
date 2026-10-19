---
document_type: research_evaluation
date: 2026-10-19
title: "claude-recall — Claude Codeセッション原文の保存・検索"
origin: "Human-shared Zenn article; official GitHub README, architecture and ADR reviewed"
source_article: "https://zenn.dev/babarot/articles/claude-code-session-recall"
source_repository: "https://github.com/babarot/claude-recall"
decision: CANDIDATE
implementation: HOLD
human_priority: LOW
current_adoption_priority: C
stage_1_rank: A++
stage_2_rank: A+
relationship: "REINFORCE + EXPAND (Checkpoint / Memory / evidence retrieval)"
evidence_status: "OFFICIAL DOCUMENTATION CONFIRMED / LOCAL TEST UNVERIFIED"
tags:
  - session-recall
  - claude-code
  - original-transcript
  - checkpoint
  - sqlite
  - fts5
  - mcp
  - memory
  - human-decisions
  - low-priority
trigger_topics:
  - claude-recall
  - Claude Codeセッション検索
  - 過去会話原文
  - Checkpoint記録漏れ
  - 人間の過去判断の確認
  - セッション履歴消失
---

# claude-recall — 原文検索をCheckpointの補助候補として保持

## Human decision (2026-10-19)

- Humanの判断: **「今のチェックポイントの使い方と大きくは変わらないよね。これは優先度低いかな」→「それでは念のため保存しておこう」**。
- この発言に基づき、**将来参照できる研究候補としての記録のみを承認**。導入・ダウンロード・実験・MCP接続・フック登録・設定変更は未承認。
- 技術研究評価 **Stage 1 A++ / Stage 2 A+** と、現在の**導入優先度 LOW (C)** は別指標として保持する。
- Decision: **CANDIDATE / Implementation: HOLD**。独立したMemory基盤の増設を今すぐ行わない。既存Checkpointの運用を優先。
- 本記録は既存Core/Workflow/LESSONS/プロジェクト仕様を変更しない。

## 1. Source and confirmed mechanics

Sources:
- Human-shared article: https://zenn.dev/babarot/articles/claude-code-session-recall
- Official README: https://github.com/babarot/claude-recall
- Official architecture: https://github.com/babarot/claude-recall/blob/main/docs/architecture.md
- Official decision record: https://github.com/babarot/claude-recall/blob/main/docs/adr/001-recall-not-memory-extension.md

Upstream documentation explains:

- `claude-recall` imports Claude Code JSONL session transcripts into **local SQLite/FTS5** archive (usually `~/.claude/vault.db`).
- Past sessions can be searched/retrieved with **MCP**, browsed in a terminal **TUI** or browser **Web UI**, and exported.
- Session transcripts imported before their original JSONL disappears remain in the archive; the archive therefore requires its own backup and protection.
- Indexing and full-text search do **not require LLM calls**. An explicit separate 'ask Claude' workflow can invoke Claude.
- This is **pull-based recall**, not automatic memory injection. It is primarily a **Claude Code** workflow; no direct integration with ChatGPT history is established.
- The program can run without a permanent indexing daemon, but imports/watchers run while Web UI/MCP are active and via a session-end hook when configured. Installation modes have different side effects.
- The indexed material can include messages, thinking content, tool calls and results, not only Human-authored prose.
- The project's ADR explicitly distinguishes raw-text retrieval from summarized memory extension.

**Evidence boundary**: These are claims described in published upstream docs/code. This record does not claim a successful local test, a complete security audit, or validated Japanese search accuracy.

## 2. Distinguish from the existing Checkpoint

| Aspect | Current AI-Harness Checkpoint | claude-recall |
| --- | --- | --- |
| Purpose | Hand off important decisions, progress, and next actions | Retrieve earlier conversations and evidence verbatim |
| Content | Selected, structured essentials | Indexed raw session transcripts (noise filtered) |
| Strength | Lightweight, directed resumption and authority-aware records | Finding a detail omitted from a summary/checkpoint |
| Limitation | Material not captured cannot be recalled from the checkpoint | Finding the right text and interpreting whether it is current remains necessary |
| Source coverage | Harness project artifacts and specified records | Claude Code local session logs; not all AI chat services |
| Authority | Human-approved decisions and project Source of Truth govern | Original words are evidence, not automatically current policy |

**Conclusion:** Similarity in use case is high, but they are **not identical**. Checkpoint = compact handoff document; claude-recall = searchable historical primary transcript. Neither one alone proves which past instruction is still in force.

Practical example: when a Human's prior preference to proceed early was omitted from later summary (as happened in discussions of Vercel Drives), a raw transcript search could help confirm its wording—provided the original relevant conversation was captured, searchable, and accessible. It cannot search ChatGPT chats automatically.

## 3. Relation to existing AI-Harness studies

- `incubator/proposals/2026-10-12-claude-mem-persistent-context.md`: adjacent alternative. claude-mem extends agent context with summarized/semantic observations; claude-recall keeps a searchable raw history and avoids automatic injection. Do not install both by default.
- `incubator/proposals/2026-10-14-temporal-runtime-discussion-checkpoint.md`: original messages and timestamps may help reconstruct conversation history. However original archived utterances do not replace Source of Truth authority, supersession tracking, or verified timing.
- `incubator/proposals/2026-10-14-tacit-domain-knowledge-history-mining.md`: raw logs may serve as evidence of Human corrections or decisions when such mining is separately approved.
- `incubator/proposals/2026-09-21-tars-parse-finder-constellation-discovery.md`: a possible future evidence source for checking candidate relationships, not an adopted integration.
- `experiments/latent-risk-scan/cases/04-unread-source-false-absence.md`: absence from search results is not proof that a past statement did not exist.

No new always-on Memory layer, autonomous agent, or Project structure is required by this research.

## 4. Benefits, risks, and limits

**Potential benefit**: When a checkpoint fails to preserve exact Human wording, obtain the underlying session text with date/session reference instead of inferring past decisions.

**Limits and risks**:
1. Target is Claude Code; ChatGPT, Codex and other session formats are **not confirmed** compatible without a separate lawful access/export method.
2. FTS5 lexical matching can miss synonyms and paraphrases, especially for Japanese; recall success must be measured rather than assumed.
3. Preserved transcripts can include secrets, private discussions, tool outputs, and sensitive reasoning traces. Local storage does not eliminate device access/MCP and backup risks. Avoid committing raw chat archives to a public GitHub repository.
4. The archive can become the only remaining copy when original logs are deleted; backups, retention, permission boundaries and data deletion need policy.
5. Raw historical statements may have been superseded. The latest timestamp alone does not make an older statement current or authoritative.
6. The installer/plugin may register MCP or hooks and import existing logs; inspect side effects before any trial.

## 5. Revisit triggers (HOLD until a concrete need)

Reconsider only when one or more occur:
- Critical omissions in existing Checkpoints recur and the original source cannot otherwise be located.
- Claude Code session history becomes important for a practical active project and the logs are accessible.
- A read-only audit needs exact prior Human instructions or correction evidence beyond what GitHub records.
- Existing lightweight files/Checkpoint tools measurably fail the task.

If triggered, first compare **manual/source-file search**, **current Checkpoint**, and **claude-recall** on a disposable/local test corpus. Assess true-positive recall, false matches, Japanese search, provenance, latency, setup/maintenance, privacy and export. Start without exposing private logs, writing Hooks, or changing production configurations.

## 6. Final evaluation

- **Novelty**: moderate. It offers a distinct *raw-source recall* mechanism but overlaps operationally with existing resume/checkpoint tasks.
- **Research value**: Stage 1 **A++**; Stage 2 provisional **A+** (official implementation described, project-specific performance not tested).
- **Human implementation priority**: **LOW / C** (explicit decision on 2026-10-19).
- **Disposition**: **CANDIDATE / HOLD / knowledge-only archive**.
- **Current next action**: **None**. Continue current Checkpoint workflow; retrieve this record only when the named problem returns.

**Boundary:** Saving this research note authorizes no installation, no experiment, no MCP access to histories, no credential transfer, and no modification of Core, Workflow, Memory, or existing project behavior.
