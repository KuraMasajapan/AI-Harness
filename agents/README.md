# AI Agents
# AIエージェント

## 1. Purpose
## 1. 目的

This directory defines AI-specific operating configurations for the AI-Harness.

このディレクトリでは、AI-Harnessを利用する各AI固有の運用設定を定義する。

The shared Harness provides common principles, while each AI may have different capabilities, limitations, tools, and appropriate context.

共通Harnessが基本原則を提供し、各AIは能力、制約、利用可能なツール、適切なコンテキストなどが異なる。


## 2. Shared and AI-Specific Structure
## 2. 共通部分とAI固有部分

The Harness is divided into:

Harnessは以下に分けて管理する。

- Shared — 複数のAIで共有する情報
- AI-Specific — 特定のAIに固有の情報
- Private — 原則として外部AIへ共有しない情報

AI-specific configurations should reference shared information rather than duplicate it.

AI固有の設定では、共通情報を重複してコピーするのではなく、共有情報を参照する。


## 3. AI Agent Directory
## 3. AIエージェントディレクトリ

Each supported AI may have its own directory.

対応するAIごとに独自のディレクトリを持つ。

Example:

例：

agents/
├── README.md
├── GPT/
│   └── HARNESS.md
├── Claude/
│   └── HARNESS.md
├── Gemini/
│   └── HARNESS.md
└── Local/
    └── HARNESS.md

The directory name identifies the AI environment, not necessarily a specific model version.

ディレクトリ名はAIの実行環境を識別するものであり、必ずしも特定のモデルバージョンを意味しない。


## 4. AI-Specific Configuration
## 4. AI固有設定

An AI-specific Harness may define:

AI固有Harnessでは、以下を定義できる。

- Model information — モデル情報
- Available tools — 利用可能なツール
- Strengths — 得意分野
- Limitations — 制約
- Preferred Skills — 推奨Skill
- Allowed Projects — 利用可能なプロジェクト
- Memory access — Memoryへのアクセス範囲
- Evaluation characteristics — 評価上の特徴
- Write permissions — 書き込み権限

Only information useful for operating that AI should be included.

そのAIの運用に必要な情報だけを記載する。


## 5. Access Control
## 5. アクセス制御

AI-specific configuration must follow `core/ACCESS.md`.

AI固有設定は `core/ACCESS.md` のアクセス方針に従う。

An AI should not automatically receive access to all Harness information.

AIはHarness内のすべての情報へ自動的にアクセスできるものとはしない。

Access should be determined by the current task and the AI's assigned permissions.

アクセス範囲は現在の作業内容と、そのAIに設定された権限によって決定する。


## 6. Evaluation
## 6. 評価

Each AI may produce different results when evaluating the same task.

同じ作業でも、AIによって評価結果が異なる場合がある。

AI-specific evaluation results should be preserved rather than treating one AI as universally correct.

AI固有の評価結果は保持し、特定のAIを常に正しいものとして扱わない。

Differences between AI systems may provide useful information for improving the Harness.

AI間の違いそのものが、Harnessを改善するための有用な情報になる場合がある。


## 7. Authority
## 7. 権限

An AI may:

AIは以下を行える。

- Read permitted information
- Perform assigned tasks
- Evaluate results
- Create Lessons
- Propose changes
- Propose new Skills

- 許可された情報を読む
- 割り当てられた作業を実行する
- 結果を評価する
- Lessonを作成する
- 変更を提案する
- 新しいSkillを提案する

An AI must not silently change Core rules or approve its own changes.

AIはCore Ruleを無断で変更したり、自分自身の変更を承認したりしてはならない。

Human approval remains the final authority.

最終的な承認権限は人間が持つ。


## 8. Adding a New AI
## 8. 新しいAIを追加する場合

When a new AI system is introduced:

新しいAIを追加するときは、

1. Create an AI-specific directory.
2. Create its `HARNESS.md`.
3. Define its available capabilities.
4. Define its access permissions.
5. Define relevant evaluation methods.
6. Test it against the common Harness.
7. Record meaningful differences in `memory/LESSONS.md`.

1. AI固有ディレクトリを作成する。
2. `HARNESS.md` を作成する。
3. 利用可能な能力を定義する。
4. アクセス権限を定義する。
5. 適切な評価方法を定義する。
6. 共通Harnessに対してテストする。
7. 重要な違いを `memory/LESSONS.md` に記録する。


## 9. Core Principle
## 9. 基本原則

One Harness does not require one AI.

1つのHarnessが1つのAIだけに依存する必要はない。

The Harness should preserve the user's intended way of working while allowing different AI systems to contribute according to their capabilities.

Harnessはユーザーが意図した作業方法を維持しながら、それぞれのAIが能力に応じて貢献できる構造を目指す。

AI systems are replaceable components.

AIは交換可能な構成要素として扱う。
