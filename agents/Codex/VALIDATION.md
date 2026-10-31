# 第1バッチの検証 — 2026-10-31

状態: **ローカル試行・REVIEW_REQUIRED**。本番導入や性能向上を実証済みとはしない。
development基準 `7ae57c2a089f82e5e232690d8ecb8c257f51ac51` から
`codex/environment-upgrade-batch1` を分岐。GitHub APIで当日も同じdevelopment先端を確認。
旧main起点checkoutは保持し、そのbranch/ファイルは変更していない。

| 対象 | 実施・結果 | 証拠の範囲 |
|---|---|---|
| adapter | 62テスト中61成功、1skip | Windows symlink権限による1skip。実AIの意味評価ではない |
| development既存receipt | 9/9成功 | 既存checker/schema/testsを変更せず、確認済み別checkoutのvalidatorを明示依存にして実行 |
| 生成したunit/receipt最終レシート | いずれも既存checkerでOK | 構造/hash一致。Human承認・真正性・内容正しさの証明ではない |
| environment gate | unitとreceipt-compatibilityがPASS、受入REVIEW_REQUIRED | 現行source/契約/出力/試行の一致。この入口以外のnative toolsを強制してはいない |
| 保護領域 | developmentのCore/HARNESS/experiments/evaluation/incubator/research/projectsのtracked差分なし | 本試行の追加はCodex adapter/tests/docsとignore追記 |

実行記録はignored `.harness-runtime/`。タスク`environment-batch1`、検証時は版1。
最終のnext_step保存後は版2。検証契約は変わらず、両チェックPASSを再確認した。
unit attempt `a9037ba7a61042eb8751f497dd2a4fe4`、receipt attempt
`809eb9948a7d43ba95bdf2dc732c0d55`。実出力はそれぞれattempt/result.json経由で参照できる。

負例はbranch/repository/base不一致、未取得source、読了/承認の混同防止、別タスクactivation、
sourceや外部依存変更、goal訂正、後発helper検証の流用、ログ改変、保存失敗、0件/全skip、
同時更新、timeout、途中入力変更、巨大な日本語単一行の完全復元等。
「読了防止」は読んだことを認証する試験ではなく、manifestをNOT_ATTESTEDに保つ設計。

最新ユーザー訂正をpilot-task.json・checkpoint・workspace/repo AGENTSへ保存した。
主目的はCodex環境整備、TRINITYは補助。今後の訂正は旧記録より優先する。

TRINITY補助作業はワークスペースの`trinity-continuation-2026-10-31/REPORT.md`へ分離。
そこでのUI/Synthetic成功を本adapterの実AI性能向上へ転用しない。

## 残る評価

- 同じ実作業/モデル/設定/入力でbaselineと比較し、目的保持・誤停止・再読込・人の訂正回数を測る。
- 実usage・wall-clock・保存IO/容量を測定。表示文字数をtokenに換算して改善率としない。
- Windows symlinkの試験は今回未実施。子孫process終了やdesktop全経路の強制は保証しない。
- 規模の小さい作業への常時強制はしない。悪化した経路はこのadapterを外して従来方式へ戻せる。
- 公開/push、main統合、本番移行、既存証跡削除は事前のHuman承認が必要。

公式OpenAI資料は、契約・工程状態・検証証拠を外部artifactへ保持する運用例を示す。
それは今回の実装の性能保証ではない。
[公式ワークフロー例](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)。
