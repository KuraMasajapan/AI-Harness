# UI_dev_Lab — UI設計ツール運用メモ

更新: 2026-10-04

## 目的

UI_dev_Lab は、各プロジェクトの正式実装を直接変更する前に、UI/UXのレビュー・大胆な別案・比較・試作を行う実験場所として扱う。

基本フロー:

1. Luna Low + UI Skills で日常的なレビュー・改善・試作
2. 現行案に物足りなさ、構造上の行き詰まり、別方向を見たい場面で MagicPath を投入
3. Human が実際に見て・触って採否判断
4. 採用案を Luna/Codex で正式HTMLへ実装
5. GitHub Pages 等の正式公開先へ反映

MagicPath は微修正を繰り返す用途より、「構成そのものを変える」「別の世界観を試す」など大胆な探索に優先して使う。

## Luna Low + UI Skills

主用途:
- 通常のUI改善
- 情報設計の整理
- アクセシビリティ確認
- モバイル対応
- 選択状態・導線・カード密度などの改善
- 小〜中規模の実装

現在導入済みのUI Skills:
- accessibility-inclusive-design
- design-systems-frontend-architecture
- forms-inputs-checkout
- information-architecture-navigation
- interaction-patterns-components
- ui-visual-composition
- ux-research-discovery-testing
- ux-usability-foundations
- ux-writing-content-design

## MagicPath

位置づけ:
- UIの大胆な別案を出す「発想を飛ばす」用途
- 触れるReact/TypeScriptベースのプロトタイプを作り、Humanが比較できる
- MagicPath上の試作は正式公開物ではない
- 採用した考え方を正式実装側へ持ち帰る

初回 GROWgle AI 実験:
- コンセプト: Discovery Atlas / AI発見航海
- 興味を複数選択 → 発見候補 → 現在地 → AI世界地図
- 保護者モードを維持
- MagicPathホスト上で操作可能なプロトタイプを生成
- 現行GROWgleを直接変更していない

### Call運用ルール

MagicPath は週次call上限があるため、使用するたびに利用量を可視化する。

MagicPathを使用したターンの最後に原則として次を表示する:

> MagicPath使用量: X calls | 推定残り: Y / 50 | 次回リセット: YYYY-MM-DD

ルール:
- そのターンで実行したMagicPath call数を数える
- 残量確認API自体も1 call消費するため、毎回の残量照会はしない
- 通常は前回確認値から使用callを差し引いた「推定残り」を表示する
- 残量に疑義がある時、節目、またはHumanが求めた時だけ実残量を照会する
- call枠を微修正ループで浪費しない
- 可能なら1回の依頼で複数方向の大胆な案を比較する
- MagicPath以外のPluginには同じcall制度を自動適用しない。各Pluginの課金・quota仕様を確認して個別管理する

2026-10-04 初回実験:
- 週上限: 50 calls
- 実験開始時の残量確認後: 49 calls
- GROWgle試作〜共有URL取得: 5 calls
- 残量確認を含む総消費: 6 calls
- 実験終了時の推定残り: 44 / 50

## 使い分け判断

通常改善 → Luna Low + Skills
大胆な別案探索 → MagicPath
採用判断 → Human
正式実装 → Luna/Codex
公開 → GitHub Pages

MagicPathを使う目安:
- UIは悪くないが「何か物足りない」
- 現在の構造を前提にした改善では伸びない
- まったく違う情報設計・画面構成を比較したい
- コードを書き直す前に、触れる試作品でHuman判断したい

使わない目安:
- ボタン色・余白・文言などの微修正
- 明確な不具合修正
- 既に方向性が決まっている通常実装
- Luna Low + Skillsで十分解ける問題

## 今後のGROWgle UI課題

現在の探索型UIは「全体像」と「発見」の二段構成まで成立。
次の主要課題は、カテゴリ軸の整理とグループごとの視覚言語。

現在は以下の異なる軸が同列に混在している:
- 能力/用途: 会話・学習、画像・作品、音声、コード・開発
- 実行環境/利用経路: ローカル等
- 特典/制度: 学生・教育特典
- 地域/言語: 日本語・国内系

次回は先に情報分類を整理し、その後にグループ別のイメージカラーを決める。MagicPathはこの段階で大胆な複数案を比較する候補。
