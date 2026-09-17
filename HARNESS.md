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

## 5. Task Routing / タスク別の読み込み経路

Progressive disclosure must not cause a relevant workflow to be skipped.
When a task matches one of the following patterns, load the indicated core context before making an important recommendation or design decision.

段階的読み込みによって、必要なワークフロー自体を読み飛ばしてはいけない。
以下に該当するタスクでは、重要な推奨や設計判断を行う前に、対応する中核コンテキストを読み込む。

### Technical research, component selection, architecture comparison

対象例：

- 電子部品・IC・MCUの選定
- 回路方式やアーキテクチャ比較
- 価格・在庫・JLCPCB / LCSC実装性を含む選定
- 「最適解」「代替候補」「見落としがないか」の検証
- 採用後の再設計コストが大きい技術判断

Required context / 必須参照：

- `core/RULES.md`
- `core/WORKFLOW.md`
  - `Research Task`
  - `Component Research Task`
  - `Search Breadth Check`
  - `Reasoning / Verification Depth Check`
- Relevant project file(s) only after identifying the current task scope.

この種のタスクでは、既知の型番や最初の候補から検索を始めて早期に固定せず、**要件から検索空間を作り、横方向に探索してから絞り込む。**

### Reasoning depth trigger / 思考量の提案条件

If the task is technically complex, spans multiple candidate categories, requires an optimum rather than a merely workable solution, or a wrong choice would cause meaningful redesign cost, assess whether deeper reasoning or verification would materially improve confidence.

次のような場合は、より高い思考量または追加検証が有効かを判断する。

- 複数カテゴリを横断する探索
- 複数の電気的・製造的条件が絡む
- 「動くもの」ではなく「より良い候補」を探している
- 見落とし検証が重要
- 採用後の変更コストが大きい

より深い思考が有効と判断できる場合は、ユーザーへ簡潔に提案する。
原因が思考量か、検索範囲・情報源・外部データ不足か判別できない場合は断定せず、**精度に不満がある場合の再検証手段の一つとして思考レベルを上げる案を提示する。**

高い思考量は正確さを保証しない。思考量と証拠の質は別に評価する。

### Re-evaluation trigger / 再検証の発火条件

When the user indicates that the result feels incomplete, asks why a candidate was missed, requests a deeper review, or challenges the search quality, do not merely refine the current shortlist.

ユーザーが、

- 精度に不満を示す
- 候補の見落としを指摘する
- 「もう一度しっかり調べて」と求める
- なぜ最初に候補へ出なかったかを問う

場合は、現在の候補リストだけを磨き直すのではなく、必要に応じて**要件定義まで戻って候補生成をやり直す。**

再検証では、思考量、検索範囲、検索カテゴリ、一次資料、ライブ在庫・価格のどこに不足があったかを分けて確認する。

---

## 6. Current Structure / 現在の構成

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

Some directories may not exist yet.
They will be added as the Harness develops.

一部のディレクトリはまだ存在しません。
Harnessの発展に応じて追加します。

```

---

## 7. Authority / 優先順位

The Harness should respect the following priority:

1. System and safety constraints
2. Current explicit user instructions
3. Current project requirements
4. Approved Harness rules
5. Stable memory and context
6. Previous lessons
7. General assumptions

Harnessは以下の優先順位を基本とします。

1. システムおよび安全上の制約
2. 現在の明示的なユーザー指示
3. 現在のプロジェクト要件
4. 承認済みのHarnessルール
5. 安定したメモリ・コンテキスト
6. 過去の教訓
7. 一般的な仮定

---

## 8. Evolution / 発展

AI-Harness should evolve through actual use.

AI-Harnessは実際の利用を通じて発展させます。

The basic cycle is:

Design → Use → Evaluate → Learn → Improve

設計 → 利用 → 評価 → 学習 → 改善

New rules should not be added merely because they seem useful.
They should be justified by actual problems, failures, or recurring needs.

新しいルールは「役立ちそうだから」という理由だけで追加せず、
実際の問題・失敗・繰り返し発生する課題を根拠として追加します。

```text
HARNESS.md
   ↓
「必要なものはどこ？」
   ↓
ROLE / RULES / WORKFLOW
   ↓
必要なら memory / skills / evaluation / projects

```
