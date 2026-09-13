これは２０２６_０９_１３日時点での備忘録である。
どのフィルがどんな役割をするのかここで確認できるとおもう。

# AI-Harness 手引書

## 1. この手引書について

このファイルは、AI-Harnessを構成する各ファイルの役割と、
それぞれの関係を人間向けに説明するための手引書である。

AI-Harnessそのものを動作させるためのルールではない。

「このファイルは何のためにあるのか」
「どのファイルを変更すればよいのか」
「AIと人間の権限はどう分かれているのか」

を理解するための設計メモとして使用する。


## 2. AI-Harnessとは

AI-Harnessは、AIそのものを作るものではない。

AIがより適切に、

- 考える
- 情報を選ぶ
- 行動する
- 検証する
- 失敗から学ぶ
- 改善を提案する

ための「運用基盤」である。

AIモデルが変わっても、
蓄積したルール・知識・経験・評価方法をできるだけ引き継げることを目指す。

つまり、

AIモデル
+
AI-Harness
=
運用されるAIシステム

という考え方を基本とする。


## 3. 全体構造

現在の基本構造は以下の通り。

<img width="162" height="545" alt="image" src="https://github.com/user-attachments/assets/7f936dbc-7114-4c14-8a8a-648c7ded6131" />
AI-Harness/
│
├── README.md
├── HARNESS.md
├── HANDBOOK.md
│
├── core/
│   ├── ROLE.md
│   ├── RULES.md
│   ├── WORKFLOW.md
│   └── ACCESS.md
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
├── projects/
│   ├── UIAPduino.md
│   ├── LocalAI.md
│   └── HEAL3.md
│
└── agents/
    ├── README.md
    └── ChatGPT/
        ├── HARNESS.md
        └── BOOTSTRAP.md


## 4. 各ファイルの役割

### README.md

**役割：AI-Harnessの表紙・概要**

GitHubリポジトリを初めて見た人が、

- 何を作っているのか
- 何を目的としているのか
- どのような考え方なのか

を短時間で理解するためのファイル。

詳細な運用ルールはここに集めない。


---

### HARNESS.md

**役割：AI-Harness全体の入口**

AIがAI-Harnessを利用するときの最初の案内役。

ここでは、

- Harnessの目的
- 基本構造
- Coreの位置づけ
- 情報を段階的に読み込む考え方
- 権限の優先順位
- 改善サイクル

などを示す。

HARNESS.mdそのものに全てのルールを書くのではなく、
必要な情報がどこにあるかを示す「入口」として使用する。


---

### HANDBOOK.md

**役割：人間向けのAI-Harness説明書**

このファイル。

各ファイルの役割、
ファイル同士の関係、
変更するときの考え方などを記録する。

AIが動作するためのルールではなく、
人間がHarnessを理解・管理するための設計メモ。

将来、自分自身が数か月後に見ても理解できることを目的とする。


# Core

## core/ROLE.md

**役割：AIの「どういう存在として振る舞うか」**

AIの基本的な姿勢を定義する。

例えば、

- 単なる命令実行者ではなく思考パートナーになる
- 必要ならユーザーの考えに反対する
- 事実と推測を分ける
- 不確実性を隠さない
- 具体的な成果へ変換する
- 人間の最終判断を尊重する

など。

簡単に言えば、

**ROLE.md = AIの人格・基本姿勢**

である。


---

## core/RULES.md

**役割：AIが守る基本ルール**

ROLE.mdより具体的な行動原則を定義する。

例えば、

- ユーザーの本当の目的を優先する
- 事実を捏造しない
- 重要な情報を検証する
- 不要な複雑化を避ける
- Coreを勝手に変更しない

など。

簡単に言えば、

**RULES.md = AIが守る基本ルール**

である。


---

## core/WORKFLOW.md

**役割：AIが仕事を進める手順**

基本的な流れを定義する。

依頼
→ 目的理解
→ 情報確認
→ 方針
→ 実行
→ 検証
→ 修正
→ 成果提示
→ 教訓記録

というように、

「何をどの順番で行うか」

を定義する。

簡単に言えば、

**WORKFLOW.md = AIの仕事の進め方**

である。


---

## core/ACCESS.md

**役割：AIが「何を見てよいか・何を変更できるか」を管理する**

AI-Harnessにおいて重要な情報管理ルール。

情報を、

- Shared
- AI-Specific
- Private

という考え方で分離し、
必要以上に情報を共有しない。

さらに、

- Read
- Propose
- Evaluate
- Write
- Promote
- Approve

などの権限を区別する。

簡単に言えば、

**ACCESS.md = AIの情報アクセスと権限のルール**

である。


# Memory

## memory/MEMORY.md

**役割：長期間使える安定した記憶**

会話ログそのものを保存する場所ではない。

将来も役に立つ、

- ユーザーの安定した好み
- プロジェクトの決定事項
- 継続的な制約
- 独自用語
- 重要な背景情報

などを保存する。

簡単に言えば、

**MEMORY.md = AI-Harnessの長期記憶**

である。


---

## memory/LESSONS.md

**役割：経験から得た教訓**

実際にHarnessを使って、

- 失敗した
- 思ったよりうまくいった
- 非効率な方法が分かった
- 新しい問題を発見した

といった経験を記録する。

重要なのは、

**Lesson = すぐにRuleではない**

という点。

AIはLessonを提案できるが、
Core Ruleへの昇格は人間が判断する。

簡単に言えば、

**LESSONS.md = AI-Harnessの経験・学習記録**

である。


# Skills

## skills/README.md

**役割：AIに追加する再利用可能な能力の管理方法**

Coreは基本原則。

Skillは特定の仕事を上手く行うための追加能力。

例えば将来的には、

- Research Skill
- Coding Skill
- Data Analysis Skill
- GitHub Skill
- Evaluation Skill

などを作る。

簡単に言えば、

**Skills = AIに追加する専門能力**

である。


# Evaluation

## evaluation/TEST_CASES.md

**役割：Harnessが正しく機能しているか確認するためのテスト**

AI-Harnessの品質を評価するためのテストケースを定義する。

例えば、

- 目的を正しく理解できるか
- 事実と推測を分けられるか
- 必要なときに反対意見を出せるか
- 情報を検証できるか
- 不確実性を扱えるか
- 失敗から学べるか

など。

簡単に言えば、

**TEST_CASES.md = Harnessのテスト項目**

である。


---

## evaluation/RESULTS.md

**役割：テスト結果の記録**

TEST_CASES.mdで定義したテストを実施した結果を記録する。

例えば、

- Pass
- Partial
- Fail
- Not Tested

などで評価する。

さらに、

- 問題がHarnessにあるのか
- AIにあるのか
- 情報不足なのか
- Workflowの問題なのか

を分析するために使用する。

簡単に言えば、

**RESULTS.md = Harnessの評価記録**

である。


# Projects

## projects/<project>.md

**役割：プロジェクトごとの安定した知識・条件**

AI-Harnessそのもののルールではなく、
個別プロジェクトの情報を保存する。

現在は、

- UIAPduino
- LocalAI
- HEAL3

など。

プロジェクトごとに、

- 目的
- 方針
- 制約
- 用語
- 設計判断
- 注意点

などを記録する。

簡単に言えば、

**Projects = AIが仕事をするためのプロジェクト別知識**

である。


# Agents

## agents/README.md

**役割：AIごとのHarnessを管理するための共通説明**

AI-Harnessを複数のAIで利用するための設計思想を定義する。

例えば、

- ChatGPT
- Claude
- Gemini
- Local AI

などを、それぞれ独立したAIコンポーネントとして扱う。

全AI共通のCoreを持ちながら、
AIごとの特性・権限・評価結果を分離する。


---

## agents/ChatGPT/HARNESS.md

**役割：ChatGPTの「どういうAIとしてAI-Harnessを使うか」**

CoreのROLE.mdがHarness全体の基本姿勢なのに対して、
こちらはChatGPT専用。

例えば、

- ChatGPTがどの情報を読むか
- どの順番でContextを選ぶか
- ChatGPT固有の強み・弱点をどう記録するか
- どこまで変更を提案できるか
- どのように評価・学習するか

などを定義する。

簡単に言えば、

**agents/ChatGPT/HARNESS.md = ChatGPT専用の運用ルール**

である。


---

## agents/ChatGPT/BOOTSTRAP.md

**役割：ChatGPTがAI-Harnessを「どう起動・利用するか」**

ChatGPTがHarnessを使用するときの、

- 最初に読むファイル
- タスク判定
- 必要なContextの選択
- 検証
- Lesson作成
- 権限確認

などの起動手順を定義する。

簡単に言えば、

**BOOTSTRAP.md = ChatGPTがHarnessを使い始めるための起動手順**

である。


# 5. ファイル同士の関係

全体としては以下のように考える。

                    AI-Harness
                         │
                  ┌──────┴──────┐
                  │   HARNESS   │
                  │   全体入口   │
                  └──────┬──────┘
                         │
                     core/
                         │
        ┌────────┬───────┼───────┐
        │        │       │       │
      ROLE     RULES  WORKFLOW ACCESS
        │        │       │       │
        └────────┴───────┴───────┘
                         │
             AI共通の基本ルール
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     memory/          skills/        evaluation/
        │                │                │
   記憶・教訓         能力追加          検証
        │                │                │
        └────────────────┼────────────────┘
                         │
                     projects/
                         │
                   プロジェクト知識
                         │
                         ↓
                     agents/
                         │
              ┌──────────┼──────────┐
              │          │          │
           ChatGPT     Claude      Gemini
              │
        ChatGPT専用設定
              │
       ┌──────┴──────┐
       │             │
    HARNESS       BOOTSTRAP
       │             │
   運用ルール       起動手順


# 6. 変更するときの判断

何か問題が起きた場合、
「とりあえずRULES.mdを書き換える」
とはしない。

まず原因を考える。

### AIの基本姿勢の問題

→ `core/ROLE.md`

### AIが守るべきルールの問題

→ `core/RULES.md`

### 作業手順の問題

→ `core/WORKFLOW.md`

### 情報アクセスの問題

→ `core/ACCESS.md`

### 安定した知識の問題

→ `memory/MEMORY.md`

### 過去の経験・失敗

→ `memory/LESSONS.md`

### 特定の作業能力が不足

→ `skills/`

### Harnessの品質を確認したい

→ `evaluation/`

### 特定プロジェクトの情報

→ `projects/`

### 特定AIだけの問題

→ `agents/<AI>/`

というように、原因に応じて変更場所を分ける。


# 7. AIと人間の役割

AI-Harnessでは、
AIにすべての変更権限を与えない。

基本的な考え方は、

AI
↓
問題・改善点を発見
↓
Lesson / Proposal
↓
評価
↓
人間が判断
↓
Harnessへ反映

である。

AIはHarnessを改善するための重要な参加者だが、
Harnessの最終管理者ではない。


# 8. AIごとの分離

AI-Harnessは、

「1つの巨大なHarnessを全AIにそのまま渡す」

ことを目指さない。

基本構造は、

Shared Core
+
AI-Specific Harness
+
必要なProject / Skill / Memory
+
Private Information

とする。

AIごとに必要な情報だけを渡す。

これにより、

- プライバシー保護
- AIごとの特性の保存
- AIごとの評価
- AIごとの改善
- AIの交換可能性

を確保する。


# 9. Harnessの基本サイクル

AI-Harnessは完成品ではない。

基本的な改善サイクルは、

Observe
↓
Evaluate
↓
Learn
↓
Propose
↓
Human Review
↓
Improve
↓
Re-evaluate

とする。

つまり、

**使う → 観察する → 評価する → 学ぶ → 改善する → また使う**

という循環によって成長する。


# 10. 最も重要な考え方

AI-Harnessの目的は、
ファイルを大量に作ることではない。

AIに大量の情報を与えることでもない。

重要なのは、

**必要な情報を、
必要なAIに、
必要なときだけ渡し、
適切な権限の中で使わせ、
結果を検証し、
経験を次の改善につなげること。**

そのために、

- Core
- Memory
- Skills
- Evaluation
- Projects
- Agents
- Access

を分離している。


# 11. 現在の設計思想

現在のAI-Harnessは、

「AIに命令するための巨大なプロンプト」

ではなく、

**AIが利用するための小さなOSのような運用基盤**

を目指している。

AIモデルが変わっても、
プロジェクトや経験、ルール、評価方法を可能な限り維持する。

そして複数のAIが同じ基盤を共有しながら、
それぞれ異なる能力・評価・経験を持てる構造を目指す。


# 12. 今後の発展

今後必要になる可能性があるもの：

- Harnessの自動Context構築
- AIごとの実行環境
- Private領域の分離
- 自動評価
- AI間比較
- Lessonの整理・統合
- Ruleへの昇格管理
- GitHubとの連携
- Local AIとの接続
- MCPや外部ツールとの接続
- Harness自身の健全性チェック

ただし、必要性が確認されるまでは追加しない。

**最小構成から始め、実際の問題に応じて拡張する。**
