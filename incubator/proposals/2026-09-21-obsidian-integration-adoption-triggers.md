---
status: proposal
created: 2026-09-21
origin: Obsidian integration review
tags:
  - obsidian
  - plugin-adoption
  - proposal-trigger
  - trigger-based-adoption
trigger_topics:
  - dashboard
  - human-approval
  - advanced-query
  - templating
  - task-management
  - mcp
  - local-api
  - launcher
  - idea-capture
  - web-clipping
---

# Obsidian Integration Adoption Triggers

## Purpose

Do not install every useful Obsidian plugin in advance.

Preserve explicit **adoption triggers** so future HARNESS conversations, Proposal Recall, Smart Connections, or Human friction can surface the right tool when a real need appears.

The operating rule is:

```text
need appears
→ trigger matches
→ recall candidate
→ confirm current gap
→ minimal test
→ adopt only if measured value is positive
```

This note is intentionally phrased with concrete future-problem language so semantic recall can surface it when similar friction appears later.

---

## P0 — use / evaluate now

### Obsidian CLI

Recall when discussion includes ideas such as:

- "HARNESSからObsidianを直接操作したい"
- "GitHub経由の反映待ちをなくしたい"
- "ObsidianをLauncherから起動・操作したい"
- "local agent should read or write the Vault"
- "Propertiesを自動更新したい"
- "Obsidian commandをscriptから実行したい"

Action:
Evaluate official CLI first.

Do not jump directly to Local REST API / MCP unless an HTTP or MCP-native interface is actually required.

### Bases + Properties

Recall when:

- Proposal数が増えて一覧性が落ちる
- Role / Tool / UI component registryが必要
- compatible_with / requires / verified / status を一覧で見たい
- Human approval queueをObsidianで見たい
- card / table / kanban表示が欲しい

Action:
Use native Properties as the structured metadata layer and Bases as the first registry/dashboard layer.

### Web Clipper

Recall when:

- browserで面白い記事やGitHub projectを頻繁に見つける
- URLを後から探し直すことが増える
- 公開アイデアの収集をHARNESS研究へ流したい
- "これ面白い、保存したい" が繰り返される

Action:
Create a HARNESS Idea Capture template with source URL, capture date, status=raw, possible_use, and source type.

### Web Clipper Interpreter

Recall when:

- captured pages require repetitive summarization
- external ideas must be converted into mechanism / benefit / risk / HARNESS-use fields
- Ollama becomes available locally
- clipping long pages creates too much manual cleanup

Action:
Test local Interpreter with bounded context and explicit extraction fields.

---

## P1 — early Human UX

### Homepage

Recall when:

- Obsidian起動時に毎回同じHARNESS画面を開きたい
- Launcher / Control Room / Agent Inboxを作り始める
- startup状態を一画面で確認したい
- Usage Monitor / Git sync / approval pendingをまとめたい

Action:
Use a Base, note, Canvas, or workspace as HARNESS Home.

### QuickAdd

Recall when:

- the Human repeatedly creates the same kind of note
- manual filename / path / Properties entry becomes annoying
- "面白い" を1操作でIncubatorへ残したい
- approval receipt or idea capture is repetitive

Action:
Start with only one or two high-frequency captures.
Avoid macro sprawl.

---

## P2 — interactive Obsidian UI

### Meta Bind

Recall when:

- Human approval should become a button or toggle
- editing frontmatter directly feels cumbersome
- status / priority / verified changes need a simple UI
- Obsidian is becoming a control surface rather than only a browser

Action:
Use Meta Bind for UI convenience only.

Important:
A UI button does not replace HARNESS permission, audit, receipt, or authority checks.

---

## P3 — query complexity

### Dataview

Recall when:

- "Basesではこのqueryを表現できない"
- cross-note aggregation becomes necessary
- efficiency metrics need dynamic aggregation
- Agent / Role / Component usage history must be grouped or calculated
- computed dashboards exceed native Bases capability

Action:
Confirm the concrete query that Bases cannot express.
Only then add Dataview.

---

## P4 — deferred until a real gap exists

### Local REST API + MCP

Recall when:

- another process needs HTTP access to the Vault
- an MCP-native agent needs direct Obsidian tools
- CLI cannot satisfy required integration
- remote/local service architecture needs a persistent API
- section-level patching over HTTP is required

Before adoption:
- define trust boundary
- confirm loopback-only vs remote use
- review API key handling
- review TLS / plain HTTP setting
- define allowed read/write scope
- test with a disposable vault first

### Templater

Recall when:

- QuickAdd + native Templates cannot express required note generation
- conditional logic is repeatedly needed
- JavaScript-generated metadata is needed
- system-command execution would eliminate repeated manual work

Before adoption:
Treat templates as executable code.
Never import and run unreviewed external templates.

### Tasks

Recall when:

- simple checkbox / status is no longer enough
- Human Action Queue needs due dates
- recurring tasks are required
- task queries need scheduling or done-date semantics
- Agent Inbox grows into real work management

Action:
First test whether Bases + checkbox + official CLI task operations are enough.

---

## Existing foundation

Keep:

- Smart Connections = semantic candidate discovery
- Obsidian Git = GitHub → local Vault synchronization and durable workflow support

Current known local setting:
- Obsidian Git auto-pull interval: 5 minutes
- automatic push: intentionally not part of the current design

---

## Adoption rule

A trigger is not permission to install automatically.

It means:

```text
relevant friction detected
→ surface this proposal
→ verify current tool gap
→ Human approval when installation or consequential change is required
→ minimal experiment
→ keep / remove / defer
```

The objective is to keep the Vault and HARNESS simple while preserving future options.
