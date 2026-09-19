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


## Runtime Activation & Revalidation / 実行時の有効化と再検証

Harness files are declarative context, not self-executing runtime code.

Harnessファイルはルールや知識を保存する宣言的Contextであり、ファイルが存在するだけでAIの動作へ自動適用されるわけではない。

したがって、Harnessの利用は「アプリ起動時の一回限りのBootstrap」ではなく、**必要に応じて同一チャット内でも再検証できる仕組み**として扱う。

各AI integrationは以下を満たすことを目標とする。

1. 明示的なSTART / BOOTSTRAP経路を持つ。
2. Fresh sessionだけでなく、meaningful interruption後やContext freshnessに疑いがある場合に再Bootstrapできる。
3. 継続Projectでは、会話Memoryだけでなく現在のProject Source of Truthを必要に応じて再取得する。
4. 重要な継続作業の前には、必要なCore / Workflow / Project Contextが現在のRunで有効か確認する。
5. 評価では以下を分ける。
   - Ruleがrepositoryに存在する
   - START / BOOTSTRAP経路がRuleを参照する
   - 現在のRunで実際にContextが読み込まれた
   - 実タスクで期待動作が観察された

利用可能なmessage timestampはResume Boundary判定の有力なシグナルとして使えるが、timestampが常に利用可能とは限らないため、時刻だけを唯一の判定条件にしてはならない。

The practical target is **verifiable activation and revalidation**, not an unsupported claim of universal runtime guarantee.

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
The depth of research should match the purpose of the component search.

段階的読み込みによって必要なワークフローを読み飛ばしてはいけない。
ただし、電子部品の検索をすべて同じ深さで扱わず、**用途に応じて調査深度を切り替える。**

### A. Standard Component Lookup / 通常の電子部品検索

対象例：

- DIY、学習、修理、単発の試作
- 一般的なセンサー、抵抗、トランジスタ、リレー、DC-DCなどを探す
- Amazon、秋月電子、マルツ等から少量購入する
- 特殊な最適化より、すぐ入手できて安心して使えることが重要

この場合は、過度な候補探索を行わず、次を優先する。

- 市場に広く流通している
- 複数販売店で容易に入手できる
- 価格帯が長期的に大きく崩れにくい
- 使用実績が多く情報を得やすい
- 必要十分な信頼性・堅牢性がある
- 用途に対して十分なコストパフォーマンスがある

通常は2〜5候補程度で十分とし、未知の地域メーカーまで網羅した探索、JLCPCB実装費比較、BOM最適化、全カテゴリ横断検索などは行わない。

通常検索では、必要に応じて `core/RULES.md` と `core/WORKFLOW.md` の一般的な `Research Task` を使う。高度な `Component Research Task` は原則として発火させない。

### B. Product-Grade Component Research / 製品開発向け高度部品調査

対象例：

- JLCPCB / LCSC等を利用したPCB・PCBA設計
- 数十〜量産を想定した製品
- BOMコスト、実装費、基板面積、供給性が製品成立に影響する
- 既存市場にない価値や独自コンセプトを作る製品
- 複数の回路方式からアーキテクチャ自体を選ぶ必要がある
- 「最適解」「代替候補」「見落としがないか」の検証
- 採用後の再設計コストが大きい技術判断

この場合は重要な推奨や設計判断を行う前に以下を参照する。

- `core/RULES.md`
- `core/WORKFLOW.md`
  - `Research Task`
  - `Component Research Task`
  - `Search Breadth Check`
  - `Reasoning / Verification Depth Check`
- Relevant project file(s) only after identifying the current task scope.

この種のタスクでは、既知の型番や最初の候補から検索を始めて早期に固定せず、**要件から検索空間を作り、横方向に探索してから絞り込む。**

### Escalation / 通常検索から高度調査への切替

通常の部品検索として開始しても、調査中に以下が判明した場合は高度調査へ切り替えることを検討する。

- 一般的な部品では要求を満たせない
- 数円〜数十円の差が製品コストに大きく効く
- 部品点数削減が重要
- JLCPCB等の実装可否・在庫が設計を左右する
- 独自機能の実現方法そのものを比較している
- 代替性や長期供給が重要
- ユーザーがより高精度な探索を求めた

切替が有効な場合は、必要に応じてユーザーへ簡潔に説明する。

### Reasoning depth trigger / 思考量の提案条件

高度調査に該当し、タスクが技術的に複雑、複数カテゴリにまたがる、最適解を求めている、または誤選定による再設計コストが大きい場合は、より深い思考や追加検証が有効かを判断する。

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

場合は、必要に応じて通常検索から高度調査へ昇格し、現在の候補リストだけを磨き直すのではなく、**要件定義まで戻って候補生成をやり直す。**

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
