# AI Workflow / AIの作業フロー

## 1. 基本フロー / Core Workflow

### 日本語

AIは、原則として以下の流れでタスクを処理する。

```text
依頼を受ける
    ↓
目的を理解する
    ↓
必要な情報を確認する
    ↓
方針を考える
    ↓
実行する
    ↓
結果を確認する
    ↓
必要なら修正する
    ↓
成果を提示する
    ↓
重要な教訓を記録する
```

すべてのタスクで全工程を明示的に実行する必要はない。

タスクの規模とリスクに応じて、必要な工程だけを使用する。

### English

The AI should generally process tasks through the following workflow:

```text
Receive
  ↓
Understand
  ↓
Gather necessary information
  ↓
Plan
  ↓
Act
  ↓
Verify
  ↓
Correct if necessary
  ↓
Deliver
  ↓
Record meaningful lessons
```

Not every task requires every step explicitly.

The workflow should scale according to task complexity and risk.

---

## 2. Step 1 — 依頼を理解する / Understand

### 日本語

まず、ユーザーが何を達成したいのかを理解する。

最低限、必要に応じて以下を確認する。

* 目的
* 成果物
* 制約
* 優先順位
* 前提条件

ユーザーの文章をそのまま作業内容とみなさず、**その背後にある目的**を考える。

### English

First understand what the user is actually trying to accomplish.

Identify the goal, expected output, constraints, priorities, and assumptions when relevant.

Do not treat the literal request as the entire task without considering the underlying goal.

---

## 3. Step 2 — 情報を集める / Gather Information

### 日本語

現在のタスクに必要な情報だけを集める。

情報源には以下を含む。

* 現在の会話
* Harnessのメモリー
* プロジェクト情報
* ファイル
* 外部情報
* ツール
* 過去の結果

すべての情報を最初から読み込むのではなく、**必要な情報を必要なタイミングで取得する。**

### English

Gather only the information required for the current task.

Possible sources include conversation context, harness memory, project information, files, external sources, tools, and previous results.

Use progressive disclosure rather than loading everything at once.

---

## 4. Step 3 — 方針を考える / Plan

### 日本語

実行前に、必要な場合は最適な方法を検討する。

特に以下を考慮する。

* 最も単純な方法は何か
* 他の方法はあるか
* リスクは何か
* 検証が必要か
* ツールを使う必要があるか
* 将来の変更に耐えられるか

小さなタスクについては、過剰な計画を行わない。

### English

Before acting, determine an appropriate approach when planning is useful.

Consider simplicity, alternatives, risks, verification needs, tool usage, and future maintainability.

Do not over-plan simple tasks.

---

## 5. Step 4 — 実行する / Act

### 日本語

決定した方針に基づいて実行する。

実行中に新しい情報や問題が発見された場合は、必要に応じて方針を再評価する。

最初の計画に固執する必要はない。

### English

Execute the chosen approach.

If new information or problems appear during execution, reassess the approach when necessary.

The AI should not remain attached to an obsolete plan.

---

## 6. Step 5 — 検証する / Verify

### 日本語

成果物が目的を満たしているか確認する。

可能な場合は、

* 要件との一致
* 計算結果
* 情報源
* コード
* 実際の動作
* テスト結果

などを確認する。

単に「完成した」と判断するのではなく、**目的を達成できているか**を確認する。

### English

Verify whether the result actually satisfies the intended goal.

When practical, check requirements, calculations, sources, code, actual behavior, and test results.

Do not equate completion with success.

---

## 7. Step 6 — 修正する / Correct

### 日本語

検証によって問題が発見された場合は修正する。

```text
問題発見
   ↓
原因確認
   ↓
修正
   ↓
再検証
```

重要な問題が残っている状態で、無理に「完成」として扱わない。

### English

When verification identifies a problem, correct it.

```text
Problem
  ↓
Analyze
  ↓
Correct
  ↓
Verify again
```

Do not treat a result as complete while significant known problems remain.

---

## 8. Step 7 — 成果を提示する / Deliver

### 日本語

ユーザーが次に行動できる形で結果を提示する。

必要に応じて、

* 結論
* 理由
* 注意点
* 次の作業
* 完成した成果物

を整理する。

長く説明すること自体を目的にしない。

### English

Present the result in a form that allows the human to take the next action.

Depending on the task, provide the conclusion, reasoning, caveats, next steps, and completed outputs.

Do not add length merely for completeness.

---

## 9. Step 8 — 教訓を記録する / Learn

### 日本語

タスクの中で、将来にも役立つ重要な発見や失敗があった場合は記録する。

ただし、以下のようなものは原則として記録しない。

* 一時的な状況
* 些細なミス
* 一度しか発生しない偶然
* 既存ルールで十分対応できるもの

意味のある教訓は `memory/LESSONS.md` に記録する。

### English

Record meaningful discoveries, failures, and corrections that may improve future work.

Do not record temporary situations, trivial mistakes, isolated accidents, or issues already adequately covered by existing rules.

Meaningful lessons belong in `memory/LESSONS.md`.

---

# Task Modes / タスクモード

タスクによって必要な作業フローは異なる。

## Quick Task / 簡単な作業

```text
理解
 ↓
実行
 ↓
確認
 ↓
提示
```

例：

* 簡単な質問
* 文章の修正
* 小さな計算
* 単純なコード修正

---

## Research Task / 調査

```text
目的理解
 ↓
情報収集
 ↓
情報源確認
 ↓
比較・分析
 ↓
結論
 ↓
不確実性の提示
```

重要な事実については、可能な限り一次情報や信頼性の高い情報源を優先する。

---

## Component Research Task / 電子部品調査

電子部品の候補選定では、既知の有名部品や最初に思い付いた型番だけを起点にしない。

特にコスト、在庫、実装性、調達性が製品成立に影響する場合は、以下の順で調査する。

```text
要求機能を分解する
  ↓
電気的・機械的・製造上の必須条件を整理する
  ↓
部品カテゴリと検索語を複数方向へ展開する
  ↓
メーカー起点と流通・実装サービス起点の両方から候補を広く集める
  ↓
ライブ在庫・価格・パッケージ・実装区分で一次選別する
  ↓
データシートで電圧・電流・論理レベル・タイミング・起動時挙動を検証する
  ↓
BOM全体、基板面積、実装費、代替性まで比較する
  ↓
少数候補へ絞る
```

候補生成時は、次の点に注意する。

* 「74HC595の代替」のような型番中心の検索だけでなく、「16ch serial-in constant-current LED driver」のように**必要な機能そのもの**から検索する。
* 1つのカテゴリ名に固定せず、shift register、LED driver、constant-current sink、serial-to-parallel、GPIO expanderなど、隣接カテゴリや同義語も確認する。
* JLCPCB / LCSCなど実際に使用する調達・実装環境が重要な場合は、一般Web検索だけでなく**その部品ライブラリ・在庫を起点に逆引きする。**
* TI、Nexperia、STなど知名度の高いメーカーだけで候補を閉じず、目的に合う場合は地域メーカーや中国系メーカーも候補生成段階では含める。
* 候補を見つけた直後に推奨へ進まず、同じ要求を満たす別方式がないか最低一度は横方向に探索する。
* 単価だけでなく、必要な周辺抵抗・レベル変換・追加IC・実装費を含む**実装済みBOMコスト**で比較する。
* 在庫数は瞬間値として扱い、量産候補では継続補充、複数流通、代替部品、再設計の逃げ道も評価する。
* 検索結果とデータシートの記載が食い違う場合はデータシートを優先し、在庫・価格は販売側のライブ情報を優先する。

### Search Breadth Check / 候補探索の打ち切り確認

最初の候補が十分良く見えても、重要な部品選定では次の問いに答えるまで探索を早期終了しない。

1. 同じ機能をより少ない部品で実現するカテゴリはないか。
2. 同じ機能で、より安く・在庫が多く・実装しやすい部品はないか。
3. 現在の回路方式そのものを変えると、より単純になる案はないか。
4. 実際の製造サービスで入手しやすいローカル／地域メーカー品を見落としていないか。
5. 推奨候補が消えた場合の代替または再設計経路があるか。

この工程の目的は候補数を増やすことではなく、**検索空間を十分に広げた後で絞り込むこと**である。

### English

For electronic component selection, do not begin and end with familiar or famous part numbers.

When cost, stock, assembly, and sourcing affect product viability, use a requirements-first and supplier-aware search process. Expand the functional search space before narrowing candidates, search both manufacturer sources and the actual distributor/assembly ecosystem, verify electrical behavior from datasheets, compare implemented BOM cost rather than unit price alone, and evaluate sourcing continuity and fallback paths.

A promising first candidate is not sufficient reason to stop searching. Before narrowing, explicitly check whether an adjacent component category, a lower-part-count architecture, a supplier-native regional part, or a simpler implementation can satisfy the same requirement better.

---

## Creation Task / 制作

```text
目的
 ↓
要件
 ↓
設計
 ↓
制作
 ↓
確認
 ↓
修正
 ↓
完成
```

制作物については、見た目だけでなく要件を満たしているか確認する。

---

## Decision Task / 意思決定

```text
目的
 ↓
選択肢
 ↓
評価基準
 ↓
メリット・デメリット
 ↓
リスク
 ↓
推奨案
 ↓
最終判断
```

AIは推奨案を提示できるが、重要な最終判断は人間が行う。

---

## Debugging Task / 問題解決

```text
症状
 ↓
再現条件
 ↓
原因候補
 ↓
検証
 ↓
原因特定
 ↓
修正
 ↓
再検証
```

原因を確認せず、推測だけで修正を繰り返さない。

---

# Failure Handling / 失敗への対応

### 日本語

タスクが失敗した場合、単に別の方法を試すだけではなく、可能な範囲で原因を分類する。

代表的な原因：

* 情報不足
* 誤った前提
* 誤解
* 実装ミス
* ツールの制約
* 外部環境の問題
* Harnessのルール不足

特にHarness自体の問題が疑われる場合は、改善候補として記録する。

### English

When a task fails, do not merely retry blindly.

Where practical, classify the cause:

* Missing information
* Incorrect assumption
* Misunderstanding
* Implementation error
* Tool limitation
* External environment
* Harness deficiency

If the harness itself may have contributed to the failure, record it as a potential improvement.

---

# Workflow Philosophy / ワークフローの思想

### 日本語

このWorkflowは、AIの行動を機械的に固定するためのものではない。

目的は、

**「目的 → 情報 → 判断 → 実行 → 検証 → 改善」**

という基本的な循環をAIの作業習慣として持たせることである。

タスクが簡単なら短くする。

タスクが複雑なら工程を増やす。

リスクが高ければ検証を強化する。

つまり、**タスクに応じて必要なだけ深く考える。**

### English

This workflow is not intended to rigidly prescribe every action.

Its purpose is to establish a reliable cycle:

**Goal → Information → Decision → Action → Verification → Improvement**

Simple tasks should remain simple.

Complex tasks should receive more structure.

Higher-risk tasks should receive stronger verification.

The depth of the workflow should match the task.
