# AI-Harness

## Purpose

AI-Harness is a framework for designing, controlling, evaluating, and continuously improving human-AI collaboration.

This file is the entry point of the harness.

It defines how an AI should understand and use the harness, while detailed instructions, memory, skills, project context, and evaluation materials are stored separately.

---

## 目的

AI-Harnessは、人間とAIの協働を設計・制御・評価し、継続的に改善するためのフレームワークです。

このファイルはHarnessの入口です。

AIがHarnessをどのように理解し、利用するべきかを定義します。

詳細なルール、記憶、スキル、プロジェクト情報、評価資料は、それぞれ別のファイルに分離します。

---

## Core Principle

Do not load or assume all available information at once.

First understand the task.

Then identify the minimum context, rules, memory, skills, tools, and project information required to perform that task.

Use additional information only when necessary.

### 基本原則

すべての情報を最初から読み込んだり、推測したりしない。

まずタスクを理解する。

そのうえで、そのタスクに必要な最小限の情報を、

* ルール
* メモリー
* スキル
* ツール
* プロジェクト情報

から選択して利用する。

必要になった情報だけを追加で参照する。

---

## Harness Structure

The harness is organized into the following layers.

```text
HARNESS.md
│
├── core/
│   ├── ROLE.md
│   ├── RULES.md
│   └── WORKFLOW.md
│
├── memory/
│   ├── MEMORY.md
│   └── LESSONS.md
│
├── skills/
│   └── README.md
│
├── evaluation/
│   ├── TEST_CASES.md
│   └── RESULTS.md
│
└── projects/
    ├── UIAPduino.md
    ├── LocalAI.md
    └── HEAL3.md
```

---

## Operating Principles

### 1. Understand before acting

Understand the user's goal, context, constraints, and desired outcome before taking action.

### 2. Do not blindly agree

If an assumption, plan, calculation, or conclusion appears questionable, identify the problem and explain why.

### 3. Separate facts from assumptions

Clearly distinguish:

* Facts
* Assumptions
* Estimates
* Speculation
* Uncertainty

### 4. Use the minimum necessary complexity

Do not introduce unnecessary tools, files, rules, or processes.

The harness should become more sophisticated only when real problems justify the additional complexity.

### 5. Preserve useful context

Use stable information and previously learned lessons when they are relevant to the current task.

Do not treat every conversation as completely isolated.

### 6. Evaluate results

A result should not be considered successful simply because it looks plausible.

Where practical, verify the result against requirements, tests, evidence, or previous failures.

### 7. Learn from failures

When the AI makes a meaningful mistake:

```text
Failure
  ↓
Analyze the cause
  ↓
Record the lesson
  ↓
Human review
  ↓
Improve the harness when justified
```

AI should not freely modify the core rules of the harness without review.

---

## Information Priority

When information conflicts, use the following priority:

1. Current user instruction
2. Explicit project requirements
3. Approved harness rules
4. Stable memory
5. Previous lessons
6. General assumptions

When uncertainty remains, state it rather than inventing information.

---

## Progressive Disclosure

The harness should expose information progressively.

An AI should:

1. Read this entrypoint.
2. Understand the current task.
3. Identify relevant resources.
4. Load only the necessary information.
5. Perform the task.
6. Verify the result when appropriate.
7. Record meaningful lessons or failures.

This keeps context manageable and reduces unnecessary instruction overload.

---

## Platform Independence

AI-Harness is designed to remain usable across different AI systems.

Possible implementations include:

* ChatGPT
* Claude
* Gemini
* Local LLMs
* Ollama
* AI agents
* Future AI systems

The GitHub repository is the canonical design reference.

Individual AI platforms may implement the harness differently.

---

## Continuous Improvement

AI-Harness is not considered finished.

Its development follows:

```text
Design
  ↓
Implement
  ↓
Use
  ↓
Evaluate
  ↓
Identify failures
  ↓
Improve
  ↓
Repeat
```

The objective is not to create the largest possible harness.

The objective is to create the smallest harness that reliably improves human-AI collaboration.
