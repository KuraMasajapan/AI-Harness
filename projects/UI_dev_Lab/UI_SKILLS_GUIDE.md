# UI_dev_Lab — UI Skills Guide

更新: 2026-10-04

## 目的

UI_dev_Lab に導入した9個のUI Skillsを「全部毎回使う」のではなく、課題に応じてLuna/Codexが適切なSkillを選べるようにするための選定ガイド。

基本原則:
- HumanはSkill名を指定しなくてよい。
- Luna/Codexは対象UIと課題を先に読み、必要なSkillだけ選ぶ。
- Skillは判断補助。既存仕様・データ・安全分類を勝手に変更する権限にはしない。
- UI変更は「情報を消す」より「優先順位・階層・見せ方を変える」を優先する。
- 大胆な別案が必要な場合はMagicPathとの併用を検討する。

## 9 Skills

### 1. information-architecture-navigation
**役割:** 情報設計・分類・導線。

使う場面:
- 情報量が多く全体像が分からない
- カテゴリが混在している
- ナビゲーションや探索経路を再設計する
- 一覧 / 詳細 / フィルタ / 検索の関係を整理する

GROWgleでの代表例:
- 「能力」「利用経路」「特典」「地域」が同列に並ぶ問題の整理
- 発見層と全体像層の役割分離

### 2. interaction-patterns-components
**役割:** ボタン、カード、選択、展開、モード切替などの操作設計。

使う場面:
- 押せる場所が分かりにくい
- 選択状態が伝わらない
- 複数選択、解除、リセットが必要
- モバイルでフィルタや詳細表示を改善したい

GROWgleでの代表例:
- 「やりたいこと」の複数選択
- 発見モード / 保護者モード
- details/summaryや探索カードの操作

### 3. ui-visual-composition
**役割:** 視覚階層、余白、色、タイポグラフィ、カード構成。

使う場面:
- 機能は良いが見た目が弱い
- 情報密度が高すぎる
- 色が多すぎる / 単調
- 第一印象や視線誘導を改善したい

GROWgleでの代表例:
- ダーク/ネオンから明るい信頼感ある配色への実験
- カテゴリごとのイメージカラー設計

### 4. ux-usability-foundations
**役割:** 基本的な使いやすさ、認知負荷、迷いの削減。

使う場面:
- 「最初に何をすればいい？」となる
- 情報が多く疲れる
- 操作後の結果が分かりにくい
- UIが設計者都合になっていないか確認したい

GROWgleでの代表例:
- 最初の行動を「やりたいこと」から始める
- 子どもが発見 → 大人が確認、という流れの評価

### 5. accessibility-inclusive-design
**役割:** アクセシビリティと多様な利用者への配慮。

使う場面:
- 色だけで状態を表している
- キーボード操作やfocusが弱い
- 動的更新がスクリーンリーダーへ伝わらない
- 小さいタップ領域や読みにくいコントラストがある

GROWgleでの代表例:
- 信号色 + テキストラベル
- aria-pressed / aria-live
- focus表示、reduced-motion

### 6. ux-writing-content-design
**役割:** UI文言、ラベル、説明の理解しやすさ。

使う場面:
- 技術用語が多い
- 子ども向けと大人向けの説明が混ざる
- ボタン文言が曖昧
- 安全情報を怖がらせず正確に伝えたい

GROWgleでの代表例:
- 「チェックをすべて外す」→「すべての絞り込みを解除」
- 技術分類を子どもにも分かる表示名へ変換

### 7. design-systems-frontend-architecture
**役割:** UIの一貫性と再利用可能な設計。

使う場面:
- 複数ページ/モジュールへ展開する
- 色・余白・角丸・カード・ボタンがバラバラ
- 共通コンポーネント化したい
- 将来のGROWgle ENTRE / WORKS / STEAMまで見据える

GROWgleでの代表例:
- GROWgle全体の共通デザイン言語
- モジュール別カラーと共通UIルールの分離

### 8. ux-research-discovery-testing
**役割:** 仮説、利用者視点、比較、テスト設計。

使う場面:
- A/Bどちらが良いかHuman確認したい
- UI変更の狙いを明確にしたい
- 「なんとなく良い」で終わらせたくない
- 実際の利用フローで問題を見つけたい

GROWgleでの代表例:
- Luna案とMagicPath案の比較
- 子ども発見→大人確認の実利用シナリオ検証

### 9. forms-inputs-checkout
**役割:** フォーム、入力、選択、エラー、完了フロー。

使う場面:
- 検索フォーム
- 登録・応募・問い合わせ
- 条件入力や複雑な選択UI
- 将来GROWgleでイベント応募等を扱う場合

現時点のGROWgle AIでは優先度は低め。フォームを本格導入した時に使用する。

## 課題 → 推奨Skillセット

### 情報が多く全体像が見えない
主: information-architecture-navigation
補助: ux-usability-foundations, ui-visual-composition

### 見た目が物足りない
主: ui-visual-composition
補助: design-systems-frontend-architecture
大胆な別案が必要ならMagicPathへ。

### ボタンや選択が分かりにくい
主: interaction-patterns-components
補助: accessibility-inclusive-design, ux-usability-foundations

### 子どもにも分かる言葉へ直したい
主: ux-writing-content-design
補助: ux-usability-foundations, accessibility-inclusive-design

### モバイルで使いにくい
主: interaction-patterns-components
補助: ux-usability-foundations, accessibility-inclusive-design

### GROWgle全体でUIを統一したい
主: design-systems-frontend-architecture
補助: ui-visual-composition, information-architecture-navigation

### Human評価前の最終レビュー
主: ux-usability-foundations
補助: accessibility-inclusive-design, ux-research-discovery-testing

## 標準選定フロー

1. 対象UIを読む。
2. Humanが感じている問題を1〜3個に分解する。
3. 問題ごとに主Skillを1個選ぶ。
4. 必要なら補助Skillを1〜2個追加する。
5. 変更前に「何を改善するか」を短く言語化する。
6. 実装またはレビューする。
7. 実ブラウザで操作・モバイル・アクセシビリティを確認する。
8. Humanが見て採否判断する。

原則として5個以上を機械的に同時使用しない。多数Skillを呼ぶこと自体を品質とみなさない。

## Luna Low と上位モデルの役割

Luna Low + Skillsを日常UI作業の第一選択とする。

上位モデルへのエスカレーション候補:
- 情報設計そのものに複数の重大なトレードオフがある
- Lunaが同じ問題を繰り返し解決できない
- 正式公開前に独立レビューしたい
- 大規模な設計変更が他プロジェクトへ波及する

上位モデルは自動的に「改善」させず、まずLuna成果物のレビュー役として使う。Humanが満足している案を上位モデルの好みだけで変更しない。

## MagicPathとの境界

Skillsは「考え方と実装品質を高める」ために使う。
MagicPathは「現在の前提を外して別の形を見せる」ために使う。

目安:
- 改善 → Skills
- 再構成 → Skills + Human
- 大胆な別案探索 → MagicPath
- 採用案の磨き込み → Skills
- 正式実装 → Luna/Codex + Skills
