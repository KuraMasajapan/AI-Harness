# 出典検証v2と次回比較の境界

2026-10-31。v1のrun_m2.py、元trial、採点を変更せず、独立したoffline評価器を追加した。
本書はローカル試行用の契約であり、次回モデル試行の実行許可や正式採用ではない。

## 今回の実装

`evaluation/citation_v2.py` は `evidence` と `reuse_decision` の2項目だけを評価する。
v1のcase/diagnosis/action/主目的/権限/approvals全体を置き換える採点器ではない。
新しいモデル比較runnerへは未接続。providerのstructured output対応も未検証。

- `mechanical_quality` は形式・必要source・引用含有・reuse_decisionだけのPASS/FAIL。
- `position_check` はNOT_PERFORMED / UNRESOLVED / PERFORMED_MATCH / PERFORMED_CONFLICT。
  位置の問題は独立した診断として返し、mechanical_qualityに混ぜない。
- `presented_scope` は実際の提示packetを明示した場合だけ確認する。
- 意味検証は常にNOT_PERFORMED、acceptanceは常にREVIEW_REQUIRED。
  mechanical_quality=PASSを全体合格・位置合格・採用と呼ばない。
- source名の補正・ファジー照合・全角半角変換・末尾rstripは行わない。
  CRLF→LFのみ明示opt-inで、raw一致と変換後一致を別記録する。offsetも別の座標系。
- symbolはAST内で名前が一意のfunction/async function/classのみ。曖昧な同名はUNRESOLVED。
  行spanは1始まりの両端を含む原文行。symbolとspanが両方あれば共通範囲で照合。
- 未知sourceや不正型/短すぎるquoteはliteral未検査として分母から除外。
  unsupported率には検査数と未検査数を必ず併記する。
- schemaのsource enumは入力sourcesの実キーから生成する。oracleのrequired_sourceと
  reuse_decisionを評価前に検査し、契約不備は回答の失敗と区別して例外にする。

CLIは明示したv2 answer/sources/oracleのJSONを読み、追加モデル呼出しをせず、
`.harness-runtime/derived/citation-v2.2/<unique>/evaluation.json`へ新規保存する。
schema・正確な入力text・oracle・options・評価器hash・結果を同梱し、既存結果は上書きしない。
現行fixtureはsyntheticで、元の8回答をv2で再採点していない。

v2.1ではlocatorの型・正整数制約も形式層で検査する。型違反はCITATION_TYPE_INVALIDで
mechanical FAIL、未解決symbolや範囲矛盾は独立した位置結果として扱う。
Pythonの物理行境界はCRLF/CR/LFのみとし、form feedやUnicode separatorを行数へ加えない。
v2.0の保存結果は上書きしない。

v2.2ではlocator形式違反があってもsource/quoteの独立した診断を続け、位置検査だけを
NOT_PERFORMEDとする。型違反の形式FAILは維持する。JSON Schemaより厳しく、linesは
小数表記の整数（2.0）も拒否し、quote長はstrip後で判定する。schema適合だけで評価器の
合格は保証しない。v2.0/v2.1の保存結果は変更しない。

## 次回比較の事前条件（未実行）

1. 修正済みバグを未解決ケースとして使わず、新しい実案件と不変入力を決める。
2. 文脈保持・権限境界・成果物の正しさ・不要な再実行を含む期待結果を事前に定める。
   v2の形式検査だけで品質の無劣化を認定しない。
3. source全文と提示packetの両manifest、schema、oracle、runner、モデル要求値・CLIを凍結。
   壊れたfixture/契約はモデル呼出し前に停止する。
4. ケース別のペア差を主に、全件・順序・cache・実usage・総時間・欠測を保存する。
   パケット準備や再実行の負担も別計測し、固定Sの推定減算や事後除外を主評価にしない。
5. 呼出し回数・予算・停止条件を新しい計画で明記する。今回の8回の再試行はしない。
6. 正の速度劣化や品質退行の許容率を外部提案から自動採用しない。現在の性能を落とさない。
   標本不足・交絡・実効backend未認証・欠測等で判断できなければ保留。
7. 有効な証拠ならRE_CONFIRM、検証条件変更後の必要検査はRE_EXECUTE、
   破損/欠落/記録不一致はDIAGNOSEを基本とする。新依頼の意味照合は別途行う。
   宣言していない依存の変化はhash一致から検知できない、という限界を維持する。

実装の回帰PASS、実作業での効果、Humanの採用判断は別々に報告する。M2/M3は未完了。

品質確認は新ケースごとに対象成果物・重要制約・検証すべき振舞いを先に記述し、同じ入力の
baseline/candidateを機械テストと原文レビューで比較する。必要に応じてHumanが意味と
運用適合性を確認する。比較対象・入力・判定基準が一致しない場合、重大な差異が未解決、
または標本が限定的で対象範囲の効果を判断できない場合は保留する。全反復の機械PASSや
外部モデルの賛同だけでは無劣化を認定せず、結論の対象を確認したケースに限定する。
