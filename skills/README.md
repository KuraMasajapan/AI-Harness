# Skills
# スキル

## 1. Purpose
## 1. 目的

Skills are reusable capabilities that extend what the AI-Harness can do.

Skillsは、AI-Harnessが実行できる作業や能力を拡張するための再利用可能な機能単位である。

A Skill should describe how to perform a specific type of task reliably and repeatedly.

Skillには、特定の種類の作業を安定して繰り返し実行するための方法を定義する。


## 2. Role of Skills
## 2. Skillの役割

Skills are different from Core Rules.

SkillsとCore Ruleは役割が異なる。

Core Rules define how the AI should behave.

Core Rulesは、AIがどのように振る舞うべきかを定義する。

Skills define how the AI can perform specific tasks.

Skillsは、AIが特定の作業をどのように実行できるかを定義する。

Examples include:

例：

- Research Skill — 調査・情報収集
- Coding Skill — コーディング
- Data Analysis Skill — データ分析
- Document Skill — 文書作成・編集
- Image Analysis Skill — 画像分析
- Testing Skill — テスト・検証


## 3. Skill Design Principles
## 3. Skill設計原則

A Skill should be:

Skillは以下を満たすことが望ましい。

- Specific — 目的が明確である
- Reusable — 複数の作業で再利用できる
- Verifiable — 結果を確認できる
- Maintainable — 修正・更新しやすい
- Minimal — 必要以上に複雑にしない

A Skill should not duplicate Core Rules.

Skillの中にCore Rulesを重複して記述しない。

A Skill should use the existing Harness rules and workflow.

Skillは既存のHarnessのルールとWorkflowを利用する。


## 4. Skill Structure
## 4. Skillの構成

Each Skill should normally have its own directory.

各Skillは原則として独自のディレクトリを持つ。

Example:

例：

skills/
├── README.md
├── research/
│   └── SKILL.md
├── coding/
│   └── SKILL.md
└── data-analysis/
    └── SKILL.md

The directory name should clearly describe the capability.

ディレクトリ名は、そのSkillの能力を明確に表すものとする。


## 5. Skill Content
## 5. Skillに含める内容

A Skill may contain:

Skillには必要に応じて以下を含める。

- Purpose — 目的
- When to Use — 使用条件
- Inputs — 入力
- Process — 実行手順
- Verification — 検証方法
- Output — 出力
- Limitations — 制約
- Examples — 使用例
- Related Files — 関連ファイル

Only information necessary for reliable execution should be included.

安定した実行に必要な情報だけを記載する。


## 6. Skill Selection
## 6. Skillの選択

The AI should use a Skill when the current task clearly matches its purpose.

現在の作業がSkillの目的に明確に一致する場合、AIはそのSkillを利用する。

Do not load or use unnecessary Skills.

不要なSkillを無条件に読み込んだり使用したりしない。

Prefer the smallest set of Skills required to complete the task.

作業を完了するために必要な最小限のSkillを優先する。


## 7. Skill Evolution
## 7. Skillの進化

Skills should evolve through actual use.

Skillsは実際の利用を通じて改善する。

When repeated problems or useful patterns are discovered, record them in `memory/LESSONS.md`.

繰り返し発生する問題や有用なパターンを発見した場合は、`memory/LESSONS.md` に記録する。

A Lesson may eventually lead to the creation or modification of a Skill.

Lessonは、最終的にSkillの新規作成や変更につながる場合がある。


## 8. Core Principle
## 8. 基本原則

Skills extend capability without weakening the Core.

Skillは、Coreを弱めることなく能力を拡張する。

Core defines how the AI works.

CoreはAIの動作原則を定義する。

Skills define what specialized work the AI can perform.

SkillsはAIが実行できる専門的な作業を定義する。
