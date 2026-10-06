# Meltype Reference — 2026-10-06

Status: REFERENCE / NOT INTEGRATED

Source:
- Repository: https://github.com/yksr-melt/Meltype
- Release checked: v1.0.1
- Release date: 2026-10-06
- Release: https://github.com/yksr-melt/Meltype/releases/tag/v1.0.1

## What it is

Meltype is a local Japanese input tool that reduces the half-width/full-width mode-switching burden.

Core behavior:
- Type romanized input continuously and automatically mix Japanese and English.
- Example from the project: `kyouhagoogledekensaku` -> `今日はgoogleで検索`.
- Japanese text is converted through a conversion box while English words can remain in Latin characters.
- English sentences can also be typed directly.
- VS Code and terminals are generally treated as alphanumeric input, with Japanese enabled in comments/strings.
- Judgment/conversion is performed locally on the PC; typed text is not sent to a network service.

Platforms:
- Windows 10/11: main supported release.
- macOS: preview.
- Linux/IBus: preview.

## Why this is interesting

The important idea is not only the IME itself but the interaction model:

> Remove explicit mode switching and infer the user's intended input mode from context.

This is relevant to local-AI / Human-AI interfaces because it reduces friction at the input boundary without requiring cloud inference.

Potential reference areas:
- Local AI text input UX.
- Coding workflows that frequently mix Japanese instructions with English identifiers, commands, Git terms, APIs, and filenames.
- Family/local PC environments where privacy and offline processing matter.
- Future voice/text hybrid input where explicit mode selection should be minimized.

## v1.0.1 notes worth preserving

The v1.0.1 release fixed several practical mixed-language cases, including:
- `commitして`, `pushして`, `commitする`.
- English handling for words such as `feature`, `future`, `remote`, and `online`.
- Optional half-width spaces around English words, e.g. `今日は GitHub に push した`.
- Windows input-context fixes across multiple applications.
- Privacy fix so learned words / typed characters do not remain in logs when input logging is disabled.
- Crash logging added for startup failures.

## Constraints / caution

- GPL-3.0-or-later.
- Using it as-is is straightforward, but product embedding / redistribution must respect GPL terms.
- The project is young; macOS and Linux are explicitly preview versions.
- Because it handles keyboard input, security and privacy review matter before adopting it in a permanent AI-Harness runtime.

## Current decision

KEEP AS REFERENCE.

Do not integrate into AI-Harness now.
Revisit if we design:
1. a local family AI input layer,
2. a coding-oriented Japanese/English text interface,
3. a low-friction Human input adapter.

The reusable design idea is:

```
Raw Human Input
      ↓
Local Context / Language Judgment
      ↓
Japanese / English mixed text
      ↓
AI / App
```

This is a useful example of moving intelligence toward the input layer while keeping processing local and reversible.
