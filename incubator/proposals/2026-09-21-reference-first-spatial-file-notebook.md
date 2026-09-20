---
status: proposal
created: 2026-09-21
origin: desktop file-organization / evolved-notepad discussion
---

# Reference-First Spatial File Notebook

## Signal

Local files are often scattered across many folders, drives, and projects. Physically reorganizing them is expensive because it requires moving or renaming files and can break existing workflows.

The desired experience is closer to an evolved notepad or pinboard:

- files stay where they are
- arbitrary files/folders/images can be referenced from anywhere on the PC
- references can be grouped visually by topic
- the same source can appear in multiple boards without duplication
- notes and relationships can be added without editing code
- one local metadata store can describe the whole organization layer

## Core principle

```text
Do not organize the filesystem.
Organize references to the filesystem.
```

The application becomes a semantic/spatial overlay on top of the existing PC.

## Candidate UX

### Capture / Inbox
- drag files or folders from Explorer
- paste copied files/paths
- create a quick text note
- optionally paste a screenshot/image
- everything first lands in an unstructured Inbox

### Spatial Board
- free placement of cards
- image thumbnails
- file/folder cards
- text notes
- grouping / frames
- links/arrows
- tags / labels
- same source can be placed in several boards

### Open / Navigate
- click a card to open the original file
- open containing folder
- copy original path
- reveal broken links

### Search
- filename/path/tag/note search
- board search
- later semantic search through Obsidian/HARNESS if useful

## Storage model

Prefer one authoritative local metadata store, such as a single SQLite database or equivalent project file.

Store references rather than file contents:

- stable item ID
- original absolute path
- filename
- source type
- optional size / modified time / content hash
- board membership
- x/y position and size
- tags
- notes
- relationships
- optional external metadata

Thumbnails can be regenerated and may live in a disposable local cache rather than becoming authoritative data.

## Link resilience

Absolute paths alone are fragile when files move.

Store enough hints to support recovery:

- last known path
- filename
- file size
- modified time
- optional partial/full hash

If a source is missing:

```text
BROKEN LINK
→ search likely locations
→ propose matches
→ Human relink
```

Do not silently relink to an uncertain file.

## Obsidian relation

Possible future integration:

- export selected boards or relationships to Markdown
- link board items to Obsidian notes
- use Obsidian Properties/Smart Connections for semantic relationships
- keep the spatial notebook as the local file-reference UI
- keep Git/Obsidian as knowledge/audit layers where appropriate

Do not assume Obsidian Canvas alone can provide arbitrary-PC file access without testing its external-file behavior.

## Implementation direction

A browser-only app is constrained by browser filesystem permissions.

A local desktop shell is more suitable if the tool must freely open/read arbitrary local paths and accept Explorer drag/drop.

Possible lightweight implementation families:

- Tauri + local web UI
- Python local service + desktop shell
- Electron only if its heavier footprint is justified

Implementation is intentionally deferred until the UX and storage contract are agreed.

## Important limits

- moving files outside the tool may break references
- removable/network drives need explicit handling
- sensitive file paths should remain local
- no automatic upload/cloud dependency by default
- avoid copying originals unless the user explicitly requests duplication
- preserve the rule: organization metadata can change without modifying source files

## Why preserve this proposal

This can turn an unorganized filesystem into a navigable visual knowledge layer without forcing the user to first reorganize the underlying files.
