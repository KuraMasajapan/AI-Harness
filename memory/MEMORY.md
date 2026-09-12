# Memory / メモリ

## 1. Purpose / 目的

Memory stores stable and reusable context that improves future
human-AI collaboration.

メモリは、将来のAIとの協働を改善するために、
長期的に再利用する価値のある情報を保存します。

Memory is not a transcript of conversations.
It is a curated collection of useful context.

メモリは会話ログではありません。
再利用する価値がある情報を整理して保存する場所です。

---

## 2. What Should Be Remembered / 記憶するもの

The following types of information may be stored:

以下の情報を記憶対象とします。

- Stable user preferences
  / 長期的に有効なユーザーの好み

- Project decisions
  / プロジェクト上の決定事項

- Important constraints
  / 重要な制約条件

- Established terminology
  / プロジェクト固有の用語・定義

- Architecture decisions
  / システム構成・設計上の決定

- Recurring requirements
  / 繰り返し発生する要件

- User-approved background information
  / ユーザーが保存を認めた重要な背景情報

---

## 3. What Should Not Be Remembered / 記憶しないもの

Do not store information merely because it appeared in a conversation.

会話に登場したという理由だけで情報を保存してはいけません。

Avoid storing:

- Temporary task status
  / 一時的な作業状況

- One-off details with no future value
  / 将来の利用価値がない一時的な情報

- Raw conversation logs
  / 会話そのものの記録

- Secrets, passwords, API keys, or credentials
  / パスワード、APIキー、認証情報など

- Sensitive personal information unless explicitly approved
  / 明示的な許可がないセンシティブな個人情報

- Information that is likely to become obsolete quickly
  / 短期間で古くなる情報

---

## 4. Memory Types / メモリの種類

Each memory should have a clear type.

各メモリには種類を設定します。

### Preference / 好み

A stable preference that affects future interactions.

将来の回答や作業に継続的に影響する好み。

### Decision / 決定

A decision that has already been made.

すでに決定された事項。

### Constraint / 制約

A condition that must be respected.

守る必要がある条件。

### Terminology / 用語

An established meaning for a project-specific term.

プロジェクト内で定義された用語。

### Fact / 事実

A stable fact relevant to future work.

将来の作業に必要な安定した事実。

---

## 5. Memory Entry Format / 記録形式

Use a concise and structured format.

以下の形式で簡潔に記録します。

```text
## [Memory ID] Title

- Type:
- Topic:
- Content:
- Source:
- Confidence:
- Last Updated:
- Status:

```

## 6. Conflict Resolution / 矛盾の処理

When memories conflict, do not silently keep both.

メモリ同士が矛盾した場合、
古い情報と新しい情報をそのまま併存させてはいけません。

Priority should generally be:

1. Current explicit instruction
2. Newer confirmed decision
3. Older confirmed decision
4. Older memory
5. Assumption

優先順位は基本的に、

1. 現在の明示的な指示
2. 新しい確定済み決定
3. 過去の確定済み決定
4. 古いメモリ
5. 推測

とします。

When uncertainty exists, ask for clarification rather than
creating a false certainty.

不確実な場合は、勝手に確定せず確認します。

## 7. Memory Maintenance / メモリのメンテナンス

Memory should remain small, useful, and current.

メモリは小さく、役立ち、最新の状態を維持します。

Periodically:

- Remove obsolete information
  / 古くなった情報を整理する
- Merge duplicates
  / 重複情報を統合する
- Resolve contradictions
  / 矛盾を解消する
- Promote important lessons when appropriate
  / 必要に応じて重要な教訓を反映する
- Avoid unnecessary growth
  / 不要な肥大化を防ぐ

## 8. Memory vs Lessons / MemoryとLessonsの違い

Memory stores reusable context.

Memoryは「今後も使う情報」を保存します。

Lessons stores discoveries about how the Harness should improve.

Lessonsは「Harnessをどう改善すべきか」という発見を保存します。

A lesson does not automatically become a rule or memory.

教訓は自動的にルールやメモリへ昇格させません。

Human review should be used when a lesson would change
the behavior of the Harness.

Harnessの動作を変更する場合は、
人間による確認を経て反映します。

## 9. Core Principle / 基本原則

Remember what helps.

Forget what does not.

記憶するのは、将来役立つもの。

役立たないものは記憶しない。

```text
会話
 ↓
失敗・発見
 ↓
LESSONS.md
 ↓
人間が確認
 ↓
必要ならRULES / ROLE / MEMORYへ反映

```

という学習ループになります。
