# 資料11回答の照合とpreflight v2への補強

2026-11-06に受領。本文の日付は2026-11-05。原文/hashはignored領域に保存。
対象11・SAKANA-11-ENDを確認。外部回答の実行申告をローカルの検証件数へ加えない。

## 採用した最大3件

1. **契約/回答の型と出口**。protected_pathsがstrだと文字集合へ化ける偽陰性/偽陽性を
   実コードで確認。契約の型・4承認コード・oracleを検証してCONTRACT_INSUFFICIENTへ。
   回答のキー不足・型崩れはANSWER_SHAPE_INVALIDへ分け、残りの変種を続けて記録する。
2. **層の読み違い防止**。schema/機械判定の合流をmechanical_gateへ明示。
   overall_structuralはcase_rule_stateへ改名し、宣言された行動等のルールだけを示す。
   承認リストの順序は意味を持たせず、重複のない集合で比較する。
3. **版とprovenance**。run出力にfixture、全文/提示原文、評価器、preflight、manifestの
   hashを保存。manifest未指定でも対象を特定できるようにする。v1の素材・結果を保持し、
   新版fixtureへ空白パディングの変種を追加して8ケース/10変種とする。

13件の局所回帰へ増やし、事前実行では旧実装の不備を検出した。
誤った型の契約や回答を採点前に止めること、異常回答でも全変種の結果が残ること、
検査器例外をexpectedへ合わせて成功にできないことを確認する。

## 外部案をそのまま採用しなかった点

- answer.proposed_changes不正をCONTRACT_INSUFFICIENTにしない。契約側と回答側の責任を分離。
- mechanical FAILとcase_rule_state=NO_CONFLICTは共存可能。後者は全体合格ではない。
  値の名前とmechanical_gateで区別する。意味/一般品質/採用は依然REVIEW_REQUIRED。
- expectedのフィールド追加も版変更である。「1行追加だから旧期待値は未変更」としない。
  preflight_cases.jsonは保持し、新しいpreflight_cases_v2.jsonへ独立した期待値を置く。
- manifestを毎回無条件で再生成しない。不意の変更を承認してしまうため、意図した変更を
  照合してから理由付きの新版manifestを作り、旧版を保持する。
- 44.91%を「隠れ推論を含まない」と断定しない。これはCodex CLI報告input+outputの比。
  元試行はreasoning_outputをoutputの内数として集計する契約。Sakana可視出力×倍率の
  概算は別データセット。双方を同じ消費会計として比較しない。未報告内部消費は不明。
- 「fixtureを1件足すと必ず問題化する」「数行で足りる」は採用判断の根拠にしない。
  観測できた入力・対象範囲と実際の差分・回帰で判断する。

## 検証と次工程

v2 fixtureは結果から期待値を生成していない。元v1の9変種と新v2の10変種を別に保持する。
model_trial_ready=false、モデル呼出し0。新しいモデルrunnerやprovider互換を認定しない。
この段階でも、合成データの構造確認は実作業の安全性・一般性能の証明ではない。

次の外部資料12には、修正前後の再現、最小差分、全体回帰、新版fixture/manifest結果を収録する。
新規文書とコードはブランチ上のローカル差分。GitHubへの次の共有更新へまとめる。
