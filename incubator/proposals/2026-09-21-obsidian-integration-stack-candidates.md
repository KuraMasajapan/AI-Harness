---
status: proposal
created: 2026-09-21
origin: Obsidian plugin / integration research
---

# Obsidian Integration Stack Candidates

## Signal

Recent HARNESS discussions identified possible uses for Obsidian beyond note storage:

- compatibility graph
- component / role / workflow registry
- Human approval surface
- launcher / dashboard
- web idea capture
- local-first agent integration
- dynamic UI support

A review of current Obsidian capabilities suggests that much of this can be built with official core features plus a small number of community plugins.

## Strong current candidates

### Obsidian CLI — official, core-adjacent capability

Potentially the most important finding.

Current official CLI can:

- create/read/append/move/delete vault files
- inspect/set/remove Properties
- list backlinks/outgoing links
- search vault content
- query Bases
- manage tasks
- use templates
- list/install/enable/disable plugins
- execute registered Obsidian commands

The desktop app must be running, but the first CLI command can launch it.

Reference:
https://obsidian.md/help/cli

HARNESS implication:
Prefer testing official CLI before adding a custom REST/MCP control layer.

### Bases + Properties — official core plugins

Use as the first structured registry/dashboard layer.

Potential uses:

- component registry
- role registry
- compatibility metadata
- proposal status
- Human approval queue
- verified/unverified views
- table/card/kanban views

References:
https://obsidian.md/help/bases
https://obsidian.md/help/properties

### Obsidian Web Clipper — official browser extension

Useful for harvesting public ideas and implementation patterns into the Vault.

Features relevant to HARNESS:

- highlights
- structured templates
- metadata extraction
- page-specific template triggers
- Interpreter for extraction/summarization
- local model support including Ollama

References:
https://obsidian.md/help/web-clipper
https://obsidian.md/help/web-clipper/interpreter

### Homepage

Potential HARNESS control-room landing page.

Can open a note, Canvas, Base, or workspace at startup and can run an Obsidian command when opening.

Reference:
https://github.com/mirnovov/obsidian-homepage

### QuickAdd

Useful for rapid Human capture and repeatable note creation.

Supports:

- templates
- captures
- macros
- chained workflows

Reference:
https://github.com/chhoumann/quickadd

### Meta Bind

Useful when HARNESS needs interactive controls inside notes.

Can bind inline inputs/buttons to frontmatter properties.

Potential uses:

- Human approval toggles
- status controls
- simple local control panels

Reference:
https://github.com/mProjectsCode/obsidian-meta-bind-plugin

## Later / conditional candidates

### Dataview

Powerful metadata query/index engine.

Useful if native Bases becomes insufficient for registry queries or dynamic aggregation.

Reference:
https://github.com/blacksmithgu/obsidian-dataview

### Local REST API with MCP

Provides authenticated REST and MCP access for scripts and AI agents.

High future value, but overlaps with the now-capable official Obsidian CLI and expands the local attack surface.

Test only after deciding what the CLI cannot provide.

Reference:
https://github.com/coddingtonbear/obsidian-local-rest-api

### Templater

Useful for advanced note generation and scripted templates.

Can execute JavaScript and system commands, so only use trusted templates and add it when advanced automation is actually required.

Reference:
https://github.com/SilentVoid13/Templater

### Tasks

Actively maintained task-management layer.

May become useful for a richer Agent Inbox / Human approval queue, but basic task operations are already available through Obsidian and the official CLI.

Reference:
https://github.com/obsidian-tasks-group/obsidian-tasks

## Candidates to avoid as primary dependencies for now

- Obsidian Projects: discontinued and removed from the community plugin list.
- Kanban community plugin: maintainer has requested new maintainers; native Bases now includes a Kanban view.
- Metadata Menu: useful, but its maintainer states limited availability; native Properties/Bases plus Meta Bind may cover the immediate need with less dependency risk.

## Minimal-first stack

Current direction:

```text
Existing:
Smart Connections
Obsidian Git

Add / enable first:
Obsidian CLI
Bases
Properties
Web Clipper

Then only as needed:
Homepage
QuickAdd
Meta Bind
Dataview

Later after security/design review:
Local REST API / MCP
Templater
Tasks
```

## Why preserve this proposal

This stack supports the existing simple-is-best philosophy:

Use official/local mechanisms first, then add community plugins only when a measured gap appears.
