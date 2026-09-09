# AI-Harness
Create own AI harness
<img width="601" height="447" alt="image" src="https://github.com/user-attachments/assets/24fb4f84-cf7a-41b5-842c-6137668422a5" />
# AI-Harness

**Create your own AI harness.**
**自分自身のAIハーネスを構築する。**

---

## Purpose / 目的

AI-Harness is a framework for designing, controlling, evaluating, and continuously improving collaboration between humans and AI.

AI-Harnessは、人間とAIの協働を設計・制御・評価し、継続的に改善するためのフレームワークです。

The goal is not simply to create better prompts.

単に「良いプロンプト」を作ることが目的ではありません。

The goal is to build a reusable system that helps AI become a more reliable and effective thinking partner.

AIを、より信頼でき、より効果的な思考パートナーとして機能させるための、再利用可能な仕組みを構築することを目的とします。

---

## Philosophy / 基本思想

A good AI harness should not make AI blindly obedient.

優れたAIハーネスは、AIを盲目的に従わせるものではありません。

It should help AI:

* understand the user's goals and context
* understand the user's goals and context
* challenge questionable assumptions
* distinguish facts, assumptions, and speculation
* use appropriate tools when necessary
* explain uncertainty
* learn from feedback
* maintain useful context
* evaluate its own results
* improve continuously

AIは次のことができる状態を目指します。

* ユーザーの目的と文脈を理解する
* 疑わしい前提には疑問を投げかける
* 事実・前提・推測を区別する
* 必要に応じて適切なツールを使う
* 不確実性を明示する
* フィードバックから学ぶ
* 有用な文脈を維持する
* 自分の結果を評価する
* 継続的に改善する

---

## Design Principles / 設計原則

### 1. Human-centered / 人間中心

The harness exists to improve human-AI collaboration, not to replace human judgment.

ハーネスは人間の判断を置き換えるためではなく、人間とAIの協働を改善するために存在します。

### 2. Challenge, don't blindly agree / 盲目的に同意しない

AI should identify problems, contradictions, risks, and alternative perspectives when appropriate.

AIは必要に応じて、問題点・矛盾・リスク・別の視点を提示します。

### 3. Evidence over confidence / 自信より根拠

AI should distinguish verified information from inference, speculation, and uncertainty.

AIは確認された情報、推論、推測、不確実な情報を区別します。

### 4. Minimal complexity / 必要最小限の複雑さ

The harness should remain as simple as possible while providing meaningful improvements.

意味のある改善を維持しながら、ハーネスは可能な限りシンプルに保ちます。

### 5. Portable by design / 移植可能な設計

The core rules should be stored in human-readable formats and remain adaptable to different AI systems.

中核となるルールは人間が読める形式で保存し、異なるAIシステムにも適応できるようにします。

### 6. Continuous improvement / 継続的改善

The harness is not a finished product.

ハーネスは完成品ではありません。

Real-world use, feedback, failures, and evaluation should continuously improve the system.

実際の利用、フィードバック、失敗、評価を通じて継続的に改善します。

---

## Architecture / 構造

The initial architecture consists of the following layers.

初期構造は以下のレイヤーで構成します。

```text
AI-Harness
│
├── Role
│   └── What the AI is expected to be
│
├── Rules
│   └── What the AI should follow
│
├── Context & Memory
│   └── What the AI should know and remember
│
├── Skills & Tools
│   └── What the AI can use
│
├── Workflow
│   └── How the AI should work
│
├── Evaluation
│   └── How the AI's behavior is tested
│
├── Feedback
│   └── How failures and improvements are recorded
│
└── Maintenance
    └── How the harness itself evolves
```

---

## Platform Independence / プラットフォーム非依存

AI-Harness is designed to be independent from a single AI provider.

AI-Harnessは、特定のAIサービスだけに依存しない設計を目指します。

Potential target platforms include:

* ChatGPT
* Claude
* Gemini
* Local LLMs
* Ollama
* AI agents

対象となり得るプラットフォームには以下が含まれます。

* ChatGPT
* Claude
* Gemini
* ローカルLLM
* Ollama
* AIエージェント

The same core principles should be reusable across different environments whenever practical.

可能な限り、同じ中核原則を異なる環境で再利用できることを目指します。

---

## Development Approach / 開発方針

AI-Harness will be developed iteratively.

AI-Harnessは段階的に開発します。

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

設計して終わりではなく、実際にAIとの対話で使用し、その結果を評価して改善します。

---

## Repository Status / 開発状況

**Version: v0.1 — Initial design**

This repository is currently in the early design phase.

現在は初期設計段階です。

The architecture and rules are expected to change through experimentation and evaluation.

実験と評価を通じて、構造やルールは変更される可能性があります。

---

## License

To be determined.

ライセンスは今後決定します。
