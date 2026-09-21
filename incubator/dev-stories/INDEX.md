---
type: dev-story-index
status: active
updated: 2026-09-22
---

# Development Stories / 開発ストーリー

このフォルダは、AI-Harness開発中に生まれた**苦労話・失敗・認識転換・重要発見**を、後から人間向けコンテンツへ再構成するための素材置き場です。

これは Source of Truth や Core Rule ではありません。

- システム改善 → `memory/LESSONS.md`
- 実行検証 → `evaluation/`
- 将来のコンテンツ素材 → このフォルダ

## Lifecycle

```text
captured → curated → ready → published
```

## Capture rule

保存価値が高いのは特に、

> 最初はAだと思っていた → EvidenceでBだと分かった

という認識転換を含む出来事です。

単なる進捗ログや些細なミスは保存しません。

## Stories

| ID | Title | Status | Date | Related |
|---|---|---|---|---|
| DEV-STORY-001 | [[2026-09-22-harness-pitfall|ハーネスの落とし穴]] | captured | 2026-09-22 | LESSON-013 / TEST-020 |

## Obsidian usage

このrepository自体をObsidian Vaultとして使用するため、GitHubへ保存したnoteはObsidian Gitのauto-pull後にそのまま表示されます。

Smart Connectionsは関連候補の発見に使えますが、semantic similarityだけで記事化・公開・事実認定は行いません。

## Publication boundary

公開用コンテンツへ変換する際は、

- Proven / Inferred / Unresolvedを分離
- Evidenceを再確認
- Privacy確認
- 過剰主張を除去
- Human approval

を行います。
