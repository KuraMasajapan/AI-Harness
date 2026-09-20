---
status: provisional-spec
created: 2026-09-21
project: reference-first-spatial-file-notebook
version: 0.1
---

# Spatial Notebook UI / UX Decision Snapshot V0.1

This file records decisions that are sufficiently mature to treat as the current default for the first prototype.
They remain reversible until implementation begins.

## Product concept

- Do not reorganize the filesystem.
- Organize references to files and folders.
- Source files remain in their current locations.
- The same source item can appear in multiple boards.
- The tool acts as a spatial/visual organization layer over the PC.

## Desktop entry

- Use a dedicated HARNESS visual launcher/shell.
- Entry tiles use curated artwork images for a visually unified desktop.
- Default tile family uses one consistent aspect ratio.
- App/tool names are hidden by default and appear on hover/focus.
- One tile maps to one persistent tool/shell window by default.

## Open / close motion

Open:
1. artwork tile is activated
2. tile lifts to foreground
3. tile position and size morph toward remembered window bounds
4. artwork fades out during expansion
5. familiar application window fades in
6. normal window remains after transition completes

Close:
- use the reverse transition back to the source tile

Default motion target:
- about 350–500 ms
- ease-out on opening
- ease-in-out on closing
- no bounce
- reduced-motion mode uses short crossfade / no large zoom

## Window background

Selected direction:
**Ivory Canvas**

Visual rules:
- warm ivory / off-white base
- very subtle canvas weave
- no simulated depth
- no bevels
- no glossy highlights
- no heavy shadows
- 1 px hairline dividers
- generous whitespace
- panels feel drawn onto the canvas rather than floating
- selection/focus uses outline contrast, not drop shadows
- texture must remain subtle enough for long work sessions
- texture layer can be disabled independently

## Main layout

Default first prototype layout:

- Left 15%: Inbox / board list
- Center 70%: free spatial canvas
- Right 15%: selected-item inspector

Responsive behavior may collapse the right panel when space is limited.

## Core content model

Initial item types:
- file reference
- folder reference
- image reference / thumbnail
- text note
- URL

Principles:
- reference-only by default
- no automatic file moves
- no source duplication unless explicitly requested
- one source item may appear in multiple boards
- cards can be freely positioned
- boards are multiple, not one mandatory giant canvas
- one large Inbox acts as an unsorted intake area

## Storage

Preferred authoritative local store:
- one SQLite database

Store:
- item ID
- last known path
- filename
- source type
- file size
- modified time
- optional hash
- board membership
- x/y position
- card dimensions
- tags
- notes
- relationships
- last window bounds

Thumbnails are disposable cache, not authoritative data.

## Broken-link behavior

If a source file cannot be found:
- mark link as broken
- search may propose likely matches using path/name/size/mtime/hash hints
- never silently relink
- Human confirms the replacement

## Prototype V0.1 scope

The first implementation should prove only the essential experience:

1. artwork tile launcher
2. morph-open transition
3. Ivory Canvas window
4. 15/70/15 shell
5. drag/drop one local file or image
6. card appears on canvas
7. click card to open original source
8. persist card/reference/position in SQLite
9. close using reverse transition

Do not add search, semantic linking, Obsidian integration, automatic relinking, advanced board relations, or AI features until this basic interaction feels good.

## Later candidates

Deferred until a trigger appears:
- richer search
- semantic association
- Obsidian export/import
- Smart Connections integration
- AI-assisted grouping
- automatic relationship suggestions
- board-to-Markdown export
- alternate launcher themes
- more complex multi-window behavior


## File / folder link creation

User-facing behavior:

- Dragging a file or folder from Explorer into the app creates a reference card.
- Dropping a folder creates a folder reference that behaves as a folder entry point; it opens the original folder and can optionally expose its contents in the app later.
- When drag-and-drop is inconvenient, a standard file/folder picker can be used.
- Selecting a file or folder from the picker creates the same kind of reference card.
- In both cases, the original source remains in place.
- The app creates a link/reference only; it does not move, rename, or duplicate the original unless the user explicitly requests a different operation.

Preferred plain-language description:

> ファイルやフォルダをドラッグ＆ドロップすると、その場所をそのまま参照するリンクカードとして登録されます。フォルダは元のフォルダを開ける入口として機能します。ドラッグ操作が面倒な場合は、ファイル選択画面から目的のファイルやフォルダを指定するだけで、元データを移動せず同じリンクカードを作成できます。

