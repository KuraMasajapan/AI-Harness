---
id: DEV-STORY-001
type: development-story
status: captured
created: 2026-09-22
project: AI-Harness
tags:
  - harness
  - runtime
  - context
  - image-generation
  - trinity
  - failure-analysis
related_lessons:
  - LESSON-013
related_tests:
  - TEST-020
related_proposals:
  - 2026-09-20-harness-content-flywheel
---

# ハーネスの落とし穴

## Content hook

**AIにルールを書けば、守ってくれると思っていた。**

しかし実運用では、

> Ruleが存在すること  
> と  
> Ruleが実行時に使われること

は別だった。

---

## 起点

Source of Truthに重要な仕様が存在していたにもかかわらず、Source of Truthから画像生成へ進む途中の抽象化・handoffで、数量・配置・関係性などの重要属性が失われる問題が観察された。

同時期に、Context Freshnessの仕組みについても似た構造が見えた。

- Feather Triggerは `[activity_gap: ...]` を届けられる
- Harnessには再開・Freshness CheckのRuleがある
- START / BOOTSTRAPにも再入場経路がある

それでも、**AIがそのRuleを必要な瞬間に実際に運用すること自体は別問題**だった。

## 当初の理解

最初は単純に、

> AIが忘れた

という問題に見えた。

しかし、この説明だけでは複数のFailure modeを区別できない。

## 問題の分解

現時点では、少なくとも以下を分離して考える必要がある。

1. **Memory loss**
   - 情報自体がContextから失われた
2. **Retrieval failure**
   - 情報は外部にあるが必要な時に再取得されなかった
3. **Representation loss**
   - 情報は読まれたが、要約・抽象化で重要属性が落ちた
4. **Execution-control failure**
   - Ruleは存在するが、順序・Gate・必須確認として強制されなかった
5. **Model reasoning failure**
   - 必要情報が揃っていてもAIの判断自体が誤った

単なる「忘却」とまとめると、原因ごとに異なる対策を一つに混ぜてしまう。

## 現時点の推論

**Inferred / not yet fully isolated**

大元の候補として強く見えているのは、

> AIの確率的な注意・抽象化能力を、Harnessの実行制御にも使ってしまっている

という構造。

AIにとって、

- 重要そうな情報を選ぶ
- 長文を圧縮する
- 抽象化する
- 次に必要なRuleを思い出す

ことは推論上は有用だが、順序保証や必須条件の保持を担う制御装置としては不安定になり得る。

## 認識が変わった瞬間

重要だったのは、

> 「Ruleが足りない」のではなく  
> 「Ruleがあっても実行される保証が弱い」

と切り替わったこと。

追加の指示文だけで修正し続けると、同じFailure modeの上にさらにRuleを積む可能性がある。

## 二つの対策思想

議論から、対策は二択ではなく組み合わせになると整理された。

### 1. 忘れても戻れる

回復型。

- Source of Truth再取得
- Current State
- checkpoint
- durable state
- re-entry / resume

Contextが飛んでも復元可能にする。

### 2. 忘れたまま進めない

予防型。

- must-preserve
- preflight
- gate
- state machine
- deterministic check
- release condition

重要条件が欠けた状態では次工程へ進めない。

### 中心メッセージ

> **忘れることは許す。  
> でも、重要なものを忘れたまま先へ進むことは許さない。**

## 今回の対策

Harnessには `Harness Runtime Enforcement Review Trigger` を追加。

Harness / Context / TRINITY / automation等の改修時に、

- Declarative vs Enforced
- execution ownership
- bypass path
- state durability
- constraint preservation
- runtime gate / checkpointの必要性
- Evidence of execution

を再検討するようにした。

また `TEST-020` で、

> Ruleが存在するだけではPASSにしない

という回帰観点を追加した。

## 未解決

**Unresolved**

根本原因が、

- Context容量
- retrieval運用
- representation
- runtime architecture
- model特性

のどこに、どの比率で存在するかはまだ切り分け切れていない。

将来の検証候補：

- 短いContextでも欠落するか
- 同じ条件で外部Gateだけ追加すると改善するか
- proseとstructured `must_preserve[]`で差が出るか
- Current Stateからの復元だけで継続可能か
- 全情報が揃っていてもAI判断が誤るか

## コンテンツ化候補

### タイトル

- ハーネスの落とし穴
- AIにルールを書けば、守ってくれると思っていた
- PromptからRuntimeへ
- AIは忘れる。問題は忘れたまま進めることだ

### 強いフレーズ

> **AIは忘れる。問題は、忘れることではない。忘れたまま次へ進めてしまうことだ。**

> **Ruleの存在は、Ruleの実行を証明しない。**

> **知性はAIに任せる。順序保証は別の仕組みに任せる。**

## 将来使える形式

- X短文シリーズ
- note / 技術ブログ
- 「HARNESS開発失敗談」シリーズ
- Agent設計のケーススタディ
- 動画台本
- 図解「Memory / Retrieval / Representation / Control / Reasoning」

## Evidence links

- [[../../memory/LESSONS|LESSON-013 Declarative Rules Need Runtime Enforcement Review]]
- [[../../evaluation/TEST_CASES|TEST-020 Runtime Enforcement vs Declarative Rule]]
- [[../proposals/2026-09-20-harness-content-flywheel|HARNESS Content Flywheel]]
- [[../../experiments/feather-trigger/V0.1|Feather Trigger V0.1]]

## Evidence status

- **Proven:** relevant rules and mechanisms existed; runtime activation is not guaranteed merely by repository presence.
- **Observed:** source-locked generation and continuity handling exposed related operational gaps.
- **Inferred:** the shared root may be over-reliance on AI attention/abstraction for execution control.
- **Unresolved:** exact causal contribution of memory, retrieval, representation, control, and model reasoning.
