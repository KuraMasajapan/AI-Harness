# Access Policy
# 情報アクセス方針

## 1. Purpose
## 1. 目的

This file defines how information is separated and accessed within the AI-Harness.

このファイルは、AI-Harness内の情報をどのように分離し、AIがどこまでアクセスできるかを定義する。

The purpose is to protect privacy while allowing each AI to receive the context necessary for its task.

目的は、プライバシーを保護しながら、それぞれのAIが作業に必要なコンテキストだけを利用できるようにすることである。


## 2. Three Information Layers
## 2. 3つの情報レイヤー

The Harness separates information into three primary layers.

Harnessでは情報を基本的に3つのレイヤーに分離する。

### Shared
### Shared / 共通情報

Information that may be shared among multiple AI systems.

複数のAIで共有してよい情報。

Examples:

例：

- Core principles
- General workflow
- Approved project information
- General skills
- Evaluation methods

- Core原則
- 基本Workflow
- 共有が承認されたプロジェクト情報
- 一般的なSkill
- 評価方法


### AI-Specific
### AI-Specific / AI固有情報

Information specific to a particular AI system.

特定のAIに固有の情報。

Examples:

例：

- AI-specific instructions
- AI-specific strengths and weaknesses
- AI-specific tool configuration
- AI-specific evaluation results
- AI-specific lessons

- AI固有の指示
- AI固有の得意・不得意
- AI固有のツール設定
- AI固有の評価結果
- AI固有のLesson


### Private
### Private / 非共有情報

Information that should not be shared with external AI systems unless explicitly authorized.

明示的な許可がない限り、外部AIシステムへ共有しない情報。

Examples:

例：

- Personal information
- Family information
- Private conversations
- Sensitive documents
- Private credentials or secrets

- 個人情報
- 家族に関する情報
- 非公開の会話
- 機密性の高い文書
- 認証情報や秘密情報


## 3. Access Principle
## 3. アクセス原則

An AI should receive the minimum information necessary to perform the current task.

AIには、現在の作業を実行するために必要な最小限の情報だけを提供する。

More access is not automatically better.

アクセスできる情報が多いほど良いとは限らない。

Context should be loaded progressively according to the task.

コンテキストは作業内容に応じて段階的に読み込む。


## 4. Default Access
## 4. デフォルトアクセス

The default access policy is:

基本的なアクセス方針は以下とする。

| Information | Shared AI | AI-Specific | Private |
|---|---|---|---|
| Core | Allowed | Allowed | Not Required |
| General Skills | Allowed | Allowed | Not Required |
| Approved Projects | Allowed | Allowed | Not Required |
| General Memory | Allowed | Allowed | Not Required |
| AI-Specific Memory | Not Required | Allowed | Not Required |
| Private Memory | Denied | Denied by default | Allowed only when authorized |
| Secrets | Denied | Denied | Restricted |

Access should be granted explicitly when information requires special handling.

特別な扱いが必要な情報については、明示的にアクセスを許可する。


## 5. Project Access
## 5. プロジェクトアクセス

Project information should also be treated according to its sensitivity.

プロジェクト情報についても、機密性に応じて扱う。

A project may contain:

プロジェクトには以下のような情報が含まれる場合がある。

- Public information
- Shared information
- Private information
- AI-specific working information

- 公開情報
- 共有情報
- 非公開情報
- AI固有の作業情報

Do not assume that all information inside a project is shareable.

プロジェクト内のすべての情報が共有可能とは限らない。


## 6. AI Permissions
## 6. AI権限

AI permissions should be separated into at least the following capabilities.

AIの権限は、少なくとも以下の能力に分けて考える。

- Read — 読み取り
- Propose — 改善案の提案
- Evaluate — 検証・評価
- Write — 情報の追加・編集
- Promote — LessonをRuleやMemoryへ昇格
- Approve — 変更の承認

By default, an AI may read and propose, but should not approve its own Core changes.

デフォルトでは、AIは読み取りと提案を行えるが、自分自身のCore変更を承認してはならない。


## 7. Human Authority
## 7. 人間による最終権限

The human remains the final authority over the Harness.

Harnessに対する最終的な権限は人間が持つ。

AI may:

AIは以下を行ってよい。

- Identify problems
- Suggest changes
- Create Lessons
- Evaluate behavior
- Propose new Skills
- Propose Memory updates

- 問題を発見する
- 変更を提案する
- Lessonを作成する
- 動作を評価する
- 新しいSkillを提案する
- Memoryの更新を提案する

AI should not silently change Core rules.

AIはCore Ruleを無断で変更してはならない。


## 8. AI-Specific Evaluation
## 8. AI固有の評価

Different AI systems may evaluate the same task differently.

異なるAIシステムは、同じ作業に対して異なる評価を行う場合がある。

These differences should be preserved rather than immediately normalized.

この違いは、すぐに一つの判断へ統合するのではなく、可能な限り保持する。

Evaluation should record:

評価では以下を記録する。

- AI identity
- Model version
- Context used
- Result
- Evidence
- Reasoning summary
- Confidence
- Limitations

- AI識別情報
- モデルバージョン
- 使用したコンテキスト
- 結果
- 根拠
- 判断理由の要約
- 確信度
- 制約


## 9. Conflict Handling
## 9. 意見が一致しない場合

Disagreement between AI systems is not automatically a failure.

AI同士の意見の不一致は、それだけで失敗とはみなさない。

A disagreement may reveal:

意見の違いは、以下を発見する手がかりになる。

- Missing information
- Different assumptions
- Different evaluation criteria
- Model-specific limitations
- A genuine uncertainty

- 情報不足
- 前提条件の違い
- 評価基準の違い
- モデル固有の制約
- 本当の不確実性

Important disagreements should be preserved for human review.

重要な意見の相違は、人間による確認のために記録する。


## 10. Core Principle
## 10. 基本原則

Share enough information to be useful.

役に立つために必要な情報は共有する。

Do not share information merely because it is available.

利用可能だからという理由だけで情報を共有しない。

Separate capability from authority.

能力と権限を分離する。

Allow AI to learn and propose improvements, while keeping final control with the human.

AIには学習と改善提案を許可するが、最終的な管理権限は人間が保持する。
