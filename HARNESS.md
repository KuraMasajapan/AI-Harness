# AI-Harness

AI-Harness is a framework for designing, controlling, evaluating,
and continuously improving human-AI collaboration.

AI-Harnessは、人間とAIの協働を設計・制御・評価し、
継続的に改善するためのフレームワークです。

---

## 1. Purpose / 目的

This file is the entry point of the AI-Harness.

このファイルはAI-Harnessの入口です。

The Harness should not load every file automatically.
It should discover and use only the context necessary for the current task.

Harnessはすべてのファイルを常に読み込むのではなく、
現在のタスクに必要な情報を選択して利用します。

---

## 2. Core Components / 中核構成

### Role / 役割

`core/ROLE.md`

Defines what the AI should be and how it should behave as a thinking partner.

AIがどのような役割を担い、どのように行動するべきかを定義します。

### Rules / ルール

`core/RULES.md`

Defines the fundamental behavioral rules of the Harness.

Harnessが守る基本的な行動原則を定義します。

### Workflow / ワークフロー

`core/WORKFLOW.md`

Defines the general process for handling tasks.

タスクを理解し、実行し、検証し、改善するための基本的な流れを定義します。

---

## 3. Context Loading / コンテキストの読み込み

At the beginning of a task:

1. Understand the user's goal.
2. Identify relevant constraints.
3. Load the minimum necessary context.
4. Select additional files only when required.
5. Execute and verify the task.

タスク開始時には、

1. ユーザーの目的を理解する
2. 制約を確認する
3. 必要最小限のコンテキストを読み込む
4. 必要に応じて追加情報を読み込む
5. 実行して検証する

という流れを基本とします。

---

## 4. Progressive Disclosure / 段階的読み込み

The Harness should prefer progressive disclosure.

Harnessは「必要になったら読む」を基本とします。

Do not load large amounts of unrelated information
when the current task does not require it.

現在のタスクに関係のない大量の情報を、
最初から読み込むことは避けます。

---

## 5. Current Structure / 現在の構成

```text
AI-Harness/
├── README.md
├── HARNESS.md
│
├── core/
│   ├── ROLE.md
│   ├── RULES.md
│   └── WORKFLOW.md
│
├── memory/
├── skills/
├── evaluation/
└── projects/
