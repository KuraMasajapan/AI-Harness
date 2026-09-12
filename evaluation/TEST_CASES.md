# Evaluation Test Cases / 評価テストケース

## 1. Purpose / 目的

This file defines test cases for evaluating the behavior and effectiveness
of the AI-Harness.

このファイルでは、AI-Harnessの動作と有効性を評価するための
テストケースを定義します。

The purpose is not to test whether the AI can answer correctly in general.
The purpose is to test whether the Harness improves the quality of
human-AI collaboration.

目的は、AIそのものの一般的な回答能力を測定することではありません。

Harnessによって、人間とAIの協働品質が向上しているかを評価します。

---

## 2. Evaluation Principles / 評価原則

Evaluation should focus on observable behavior.

評価は、実際に観察できるAIの行動を中心に行います。

Important evaluation criteria include:

- Goal understanding
  / 目的理解

- Appropriate use of context
  / 適切なコンテキスト利用

- Distinction between facts and assumptions
  / 事実と推測の区別

- Appropriate disagreement and critical thinking
  / 必要な反論・批判的検討

- Verification of important information
  / 重要情報の検証

- Avoidance of unnecessary complexity
  / 不必要な複雑化の回避

- Quality of concrete deliverables
  / 具体的な成果物の品質

- Honest handling of uncertainty
  / 不確実性の適切な扱い

- Learning from previous failures
  / 過去の失敗からの学習

---

## 3. Test Case Format / テストケース形式

Each test case should contain:

各テストケースには以下を含めます。

```text
### TEST-XXX: Title

- Purpose:
- Scenario:
- Input:
- Expected Behavior:
- Failure Conditions:
- Notes:
