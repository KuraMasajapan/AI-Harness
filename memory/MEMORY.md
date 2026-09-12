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
