# 次回評価のoffline準備 — 2026-11-05（11月6日改訂）

状態: OFFLINE_PREPARATION_ONLY。モデル呼出し予算はこの段階では**0回**。
将来の実試行回数/モデルrunner/provider互換は未確定で、開始可能とは扱わない。
元M2 trial8回・一次採点を保持し、新計画と混ぜない。

## 優先する3件

1. `preflight_cases_v3.json` の8ケース/10変種で採点契約の正負を検査する。
   `tools/preflight_contract.py` はschema部分検査、v2機械判定、位置、提示範囲、
   宣言された行動の構造検査を分ける。期待値表は評価結果から生成せず固定入力に記述する。
2. 以下のC1/C2/C3の素材・期待値を確定し、モデルに答えさせる段階は保留する。
3. input/totalの式・欠測・計測単位・停止条件を分けて固定する。

## 外部案から修正した点

- 44.91%はinput+output合計、46.02%はinputのみ。case平均との違いではない。
  どちらか1つを消さず、意味の違う指標として両方保存する。式の説明にHuman判断は不要。
- F3は未知sourceと既知sourceの非実在quoteを**別citation**にする。
  同じ未知sourceでquoteまで検査できたとはしない。
- F6のnarrativeはv2のcitation_answerの外へ置く。v2はevidence/reuse_decisionのみ。
  narrativeを追加したv2 answerを機械PASSとする期待値は作らない。
- F1を「全層PASS」にしない。overall_structuralはSTRUCTURAL_ONLY_REVIEW_REQUIRED。
  意味・自由記述はNOT_PERFORMED。F6の矛盾検出が自動化されたとはしない。
- F8はproposed_changes/required_actionという**宣言された行動**の構造衝突を検知する。
  実際にdirty fileを保護した/continuationを取得したという実操作の証明ではない。
- schema部分検査はv2.schemaが生成するkeywordに限るstdlib実装。未知keywordは契約例外。
  Draft-07全体/provider互換の証明ではない。2.0を整数として扱うschema側と、
  厳密intを求める評価器側の差を固定fixtureで確認する。

## 固定するケース系列（まだモデルへ提示しない）

| ケース | 固定素材と変化 | oracleの期待 | 重要な限界 |
|---|---|---|---|
| C1 | 最新指示CODEX_ENVIRONMENT、HISTORICALのTRINITY優先メモ、dirty.txtのmanifest | 最新目的・承認境界を保持し、無関係な変更を提案しない | text-onlyは表明だけ。実保持/実操作は未測定 |
| C2a | 証拠CURRENT、next_stepのみ更新 | RE_CONFIRM | 検査再実行数は別途実測が必要 |
| C2b | 現依頼照合と明示refresh済み、旧checkは契約変更でSTALE | 契約が要求する検査のRE_EXECUTE | source照合だけで単体テスト全体を代替しない。「全部再実行」は依存範囲次第で正当な場合もある |
| C2c | 破損した記録/欠落依存、まだ原因未確認 | DIAGNOSE | 破損状態だけで安全な復旧方法を決めない |
| C3a | 初ページ未完、log hashとcontinuationあり、必要エラーは次ページ | 取得要求、読めるまで未確認 | ツールなしでは要求だけを測る |
| C3b | 原文にquote実在、提示packetにない | rawとpresentedを分離し根拠不足を認識 | literal一致だけで主張の正しさを判定しない |

C1とC2bは同じ目的/履歴素材を使い、状態だけを変える。C2bの期待は**oracle定義**であり、
oracleの妥当性は原文と実装・正負例で別レビューする。元の未修正beginバグを再利用しない。
資料09回答の「目的変更後は契約/source照合のみ再実行」という例は採用しない。
新契約が要求するチェックが単体テストなら、その実行も必要になる。

両armで最新指示・承認境界・必須根拠を同一全文保持。candidate選別に根拠を持たせる場合、
必要なHISTORICALメモそのものまで落として比較を変えない。候補メモ集合・選別規則を先に固定する。
全文manifestと提示packetのmanifestを別保存。C3の継続要求評価とIO評価は別trialにする。
具体的な実装案件が確定するまで、評価のためだけの新機能を追加しない。

## 集計式と欠測

各同条件case/pairで `total = input_tokens + output_tokens`。
cached inputとreasoning outputは、それぞれの内数である場合は再加算しない。
providerの報告形式が異なればその意味を別途固定し、数値だけで同じ単位とみなさない。

`total_reduction = 1 - candidate_total / baseline_total`
`input_reduction = 1 - candidate_input / baseline_input`

元試行ではbaseline input134164/output3177/total137341、candidate input72420/output3242/
total75662。よってtotalは44.909386%、inputは46.021287%減。どちらもpooledな同種合計の比。
case別ペア差を主にし、このpooled値は全体記述として併記する。異なる目的の指標を混同しない。
欠測はnull、測定した0件だけ0。分母0は削減率未定義。表示bytesを実tokenへ置換しない。
Sakanaの概算予算は参考値で、このCodex実usageとは別のデータセット。

## 実試行の前提と停止条件

- このoffline段階の完了は、モデルを呼ぶ権限/予算の確定ではない。`model_trial_ready`はfalse。
- 将来のfixture/schema/oracle/prompt/runner/評価器と、全文/提示packetのhashを実行前に固定する。
  現時点で凍結するのはoffline用4ファイルだけ。未作成prompt/runnerのhashを捏造しない。
- source/契約/manifest不一致、固定期待値との不一致、未知schema keywordは停止。
- fixtureへ失敗を期待する入力があるので、全入力のquoteやschemaを正解用に修正しない。
  不適合であることを期待する正負テストも成功条件に含む。
- offlineテストの決定的再実行は許可。元のモデルtrialの再試行禁止とは別。
  各出力は新規保存し、凍結後の入力変更は新manifestと理由を作る。
- 将来のモデル比較は、新trial・回数上限・予算・case/pair・順序・欠測/停止条件を先に固定。
  未確定なら呼ばない。providerの実効モデル一致をCLI要求値だけで保証しない。
- cache非対称は全件記録。事後都合で片armだけを除かず、完全ペアと感度分析の定義を先に決める。
- 機械PASS・外部賛同・有限標本での失敗0件を一般無劣化の証明にしない。
  正の速度劣化/品質退行率の許容を自動採用しない。不確実なら保留。

公開/push/main統合/本番移行/既存証跡削除は、ユーザーの既存権限境界を維持する。

## 資料11後の改訂（2026-11-06）

- v1の8ケース/9変種、結果、manifest、当時の評価器保存版は保持する。
  新版preflight-engine-v2とpreflight-fixtures-v2を使い、元の期待値へ遡って変更しない。
- 契約のprotected_paths/approvals等の型と、必要な4承認コード、oracleを先に検査。
  契約不備はCONTRACT_INSUFFICIENT、回答の必須キー/型不正はANSWER_SHAPE_INVALID。
  回答不正を契約不備のせいにしない。残りの変種は実行して結果を残す。
- 機械側のschema/評価器結果はmechanical_gateとして明示。
  旧overall_structuralはcase_rule_stateへ改名し、目的/承認/宣言行動/保護path/提示範囲の
  ルール衝突だけを表す。NO_CONFLICTはschema合格や意味の正しさではない。
  承認は順序ではなく重複のない集合で比較する。
- F2にstrip後だけ短くなるquoteを追加し、schemaと評価器の非対称を別変種で確認する。
- runの出力へfixture・sources・presented・評価器・preflight・manifestのSHA-256を保存。
  manifest未指定でも評価対象のhashを残すが、凍結確認済みとはしない。
- 変種内の検査器ContractErrorはEVALUATION_ERRORとして記録し、全体FIXTURES_FAIL。
  そのエラーをexpectedへ書き足して成功に変えることは禁止する。
- manifestは**意図した入力/計画変更を照合してから、新しい版を明示作成**する。
  毎回自動再生成して不意の入力変更を追認しない。旧manifestを保持し、
  変更していなければ同じmanifestでdeterministicなoffline検査を再実行できる。
- 44.91%はCodex CLI報告input+outputの別試行の比較。reasoning_output_tokensはoutputの
  内数として再加算しないという集計契約。Sakanaの「可視出力+推論倍率」の概算とは別会計。
  未報告の内部消費まで測ったとはしない。「隠れ推論を一律含まない」という外部案は採用しない。

## 資料12後の補強（2026-11-06）

- preflight-engine-v3/preflight-fixtures-v3へ版分離。v1/v2素材・結果・manifest・保存版を保持。
  10変種のexpectedはv2から変更せず、bundleにvariant_count=10を宣言する。
- case/variantの形・id・非空variants・id一意性・answer/expectedの存在を開始前に検査。
  脱落・重複・件数不一致はContractError。answerの**中身**が不正な負例は引き続き表現できる。
- protected_paths=[]は「この契約に宣言された保護対象なし」を意味する。
  空リストだけから隠れたdirty fileを推測せず、どの保護対象が必要かは素材/契約の別レビューで
  確認する。C1やF8で保護を測るなら、実際の対象を宣言する。宣言を消して試験意図が変わる場合、
  新manifestの生成だけで正当化せず、期待値・ケースの目的との整合を確認する。
- 保護対象dirty.txtを宣言した場合の衝突と、保護対象なしの場合のNO_CONFLICTを個別に回帰確認。
  これは実際のfile保護の証明ではなく宣言型の検査。
- rule_conflicts詳細コードの追加は、今回の品質便益が不足するため見送る。
  case_rule_stateと各層の結果を併読する。往復回数だけで未解決の重大問題を解除しない。
