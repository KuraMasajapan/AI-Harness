# 要素の採否と適用境界

基準: development `7ae57c2`。原案の正式採用状態は変えない。
今回の選択はCodex環境整備向けのOPTIONAL EXPERIMENT。

| 優先 | 参照した既存情報 | 重複の扱いと取り込む要素 | 今回の実装 |
|---|---|---|---|
| 1 | HARNESS Runtime Activation、Workflow Runtime Enforcement Review、Context Vault reference、TRINITY companion Persistence候補 | 組合せ。既存Coreを正本とし、追加の憲法・新DB・全量注入を作らない。重要条件は原文ID付き、sourceはbranch/base/bytes別に記録 | checkpoint/resumeとsource contract。最新ユーザー訂正も保持 |
| 2 | 既存DoD、operator receipt、companion Rule/AccessとCompletion、Hermit fixed/adapter分離 | 既存receipt形式へ一本化し、Codex固有の状態はsidecar。hash/構造、機能、意味、受入を分離。TRINITY protocol再実装は見送り | 事前/最終receipt、入力鮮度・保存失敗・別検証流用のgate、明示validator依存 |
| 3 | RTK、Token Harness、Jev、Resource Hygieneの保存研究 | 良い要素だけ組合せ。原文保持・段階取得・欠測をゼロ扱いしない。製品本体、外部分類器、global hookの導入は見送り | raw log保持、hash付き文字offsetページ、未知tokensはnull |

原案の本文と既存の比較台帳はワークスペースの
`development-review/CODEX_UPGRADE_DESIGN.md` / `SOURCE_REGISTER.md` にある。
今回の実装ではContext Vault、companion、Hermit、RTKの関連本文を再確認した。
115提案すべてを今回もう一度精査したとはしない。

## Runtime Enforcement Review

1. **宣言と実行**: AGENTSは入口。source_guardとgateはこのCLI経路で実行。
2. **記憶なし**: exact criticalと訂正理由を版付きJSONから再取得。自動注入・理解の保証はしない。
3. **所有者**: ローカルadapterが事前保存・検証・最終保存の順を所有。公開・本番判断はHuman。
4. **迂回**: helper単体やnative toolは迂回可能。environment gateで別検証の流用を拒否するが、desktop全体を遮断しない。
5. **耐久性**: atomic保存、revision競合、RUNNINGを先行保存。失敗時は古いPASSへ戻さない。
6. **保持**: ID付き原文・出典・目的・未完了・訂正を保持。ログページと重要制約を同じ圧縮対象にしない。
7. **最小制御**: 既存の機械的補助コードを再利用し、sourceとreceipt接続だけを追加。
8. **発火証拠**: activation、command argv、入力hash、全出力、receipt、負例試験を保存。読了/理解の認証とは区別。
9. **費用**: hashと原文保存のIO負担は増える。小タスクではこの経路を必須化しない。実usage/時間の利得は未測定。
10. **Human**: 提案を昇格させず、承認・publish・本番・既存証跡削除を自動化しない。

旧ローカルhelperのソースhashは
`d2dd30889215c17de215d02c44fa689a37be4dab6607e32973485aff7be03db9`。
その機械機能と40テストを再利用したが、旧baselineや削減率は持ち込まない。
同条件の実作業比較で品質・負担・時間・実usageを確認してから限定採用を判断する。

## TRINITYに関して今回確認できた範囲

別の既存checkout `work/trinity-orchestrator-v0.1` / `8f6263e` にvalidator実装が存在する。
developmentの不足依存を解決する参照先として明示的に利用できる。
UI文字列のJavaScript構文不良と6ファイルのCRLFは別checkout側で修正・検証した。
そこでの81/41/9件とSynthetic Run成功は、そのcheckoutの証拠。
development自体のTRINITY実装済み・実AI能力向上・本番準備完了の証明ではない。

## 第2バッチ — 運用開始時の不足を優先

ユーザーのブランチ運用指示を受け、以下の3件を追加した。

| 順位 | 保存情報と実際の不足 | 重複の選択 | 実装 |
|---|---|---|---|
| 1 | HARNESS再有効化・Feather Phase0。初版ではcheckpoint/resume/activateを毎回手で組み合わせていた | 既存原則へ一本化。時間固定の全再読込や新workflow engineは見送り | beginによる再入場、訂正時の明示refresh、版付き運用イベント、finishの現行証拠確認 |
| 2 | Rule/Access分離・DoD・Hermit固定領域。初版はPython/platformとwatch中心で、実行ファイルや選択環境の変化を捕捉しなかった | 既存gateと組合せ。新しい権限管理システムは作らない | runtime fingerprint、実行前後とgateでの照合、環境値を保存しないhash記録 |
| 3 | Efficiency Telemetry・Resource Hygiene・RTK原文保持。初版は計測入口がなく、出力ページの異版混在と巨大ログ全量読込が残った | 良い要素を組合せ。外部製品導入・全会話収集・cache自動削除は見送り | 観測レポート、PARTIAL/null、hash固定ページ。chunk読込は速度改善が安定せず標準採用を見送り、--stream試験に限定 |

再確認した保存資料は`incubator/proposals/2026-09-20-efficiency-telemetry-public-metrics.md`、
`incubator/proposals/2026-10-12-resource-hygiene-runtime-cleanup.md`、
`experiments/feather-trigger/PHASE0.md`の関連部分。既存原案を正式Coreへ昇格させない。
小タスクの常時記録は必須化せず、実際に使った範囲で観測する。

## 第3バッチ — ゴールと証拠の不足を補う

| 順位 | 実際の不足・保存情報 | 重複の選択 | 今回の対応 |
|---|---|---|---|
| 1 | ユーザーのゴール確認。既存DoDとTRINITY companion Completion候補 | 既存原則に一本化。新しい憲法や自動採用gateは増やさない | GOALSでM1運用基盤/M2効果確認/M3採否を分け、各バッチの閉じる条件を記録 |
| 2 | reportが全履歴をそのまま表示し、長期運用で出力が増える | RTK/Token Harnessの段階取得だけを既存reportへ組合せ | 表示20件を標準に、全件集計を維持。hash固定のcursorで異版混在を拒否 |
| 3 | 初版のhash中心の証拠だけでは、未commit bytesが変わった後に再構成できない | PersistenceとHaluMemの保存/取得/使用の分離を組合せ。新memory DBや全会話importは見送り | 選択入力をcontent-addressed objectへ保存し、同内容を再利用。壊れた証拠の自動修復や自動restoreはしない |

今回再確認したのはcompanionのDefinition of Done/Freeze節、HaluMemの操作段階別評価節。
原案の正式採用やTRINITY protocol変更ではなく、Codexのブランチ試行への要素抽出である。
入力実体の保存にはIO/容量コストがあるため、必要な入力だけを対象にし、効果比較で負担も測る。
