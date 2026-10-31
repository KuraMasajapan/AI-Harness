# ブランチ運用開始と第2バッチ — 2026-10-31

**ブランチ試験運用を開始し、第2バッチの3件を実装・検証した。**
対象はdevelopment `7ae57c2`から分岐した`codex/environment-upgrade-batch1`。
ローカル作業ツリーの運用。変更は未commitのまま保持し、push・公開・main統合はしていない。
主目的はCodex環境整備。TRINITYは既存receiptの検査依存先としてのみ参照した。

## 今回の3件

| 優先 | 実装と運用 | 採否 |
|---|---|---|
| 1 | beginによる開始/再入場、訂正・source変更時の明示refresh、保存済み重要制約の復元、追記型イベントとfinish条件 | 既存の再有効化原則と組み合わせ、ブランチ運用で使用開始 |
| 2 | 実行ファイル・Python・adapter・選択環境のfingerprintを実行前後/gateで照合。機能FAILと証拠の陳腐化を区別 | 既存gateを拡張。環境値はhashのみ保存。全依存自動検出とはしない |
| 3 | reportによる実測項目、欠測PARTIAL/null、hash固定の出力続行、実際に返した本文量の記録 | 計測と異版混在防止を使用開始。stream読込の標準採用は見送り、明示オプションのみ |

元資料の選択・重複比較は[ADOPTION.md](ADOPTION.md)の第2バッチ。
第1バッチの機械機能を置き換えて作り直さず、既存入口・記録へ接続した。

## 確認結果

- 全体81件中 **80成功・1skip**。Windowsでsymlinkを作成できない1件を未実施として保持。
- development既存receipt検査 **9/9成功**。checker/schema/testは変更していない。
- 新しく生成したunit/receiptの最終レシートも、既存checkerで両方OK。
- 別プロセスのCLI beginで、同じ運用ID・CURRENT・重要制約・現行PASSを復元。
- CLI outputのhash固定・20文字の正確な継続取得・表示観測保存を確認。
- next_stepだけの更新後も、両チェックPASSを維持。
- Core/HARNESS/既存TRINITY/評価成果物/保存提案/他projectにtracked差分なし。

新しい負例には、訂正後の無断再開、運用イベント改変、event保存後のpointer保存失敗、
環境やadapter変更、実行中のruntime変化、ログの異版混在、UTF-8 chunk境界、
未完了attemptと計測保存失敗を含めた。

第1バッチの旧証跡は削除していない。新しいruntime項目がない旧形式はNOT_CURRENTとし、
第2バッチの現行実装で再検証した。機能PASSと計測失敗も分離し、計測失敗はPARTIALとする。

## 運用記録

現在のタスクは`environment-batch2`、checkpoint版2。
運用ID `171f0ae914624013a780c8320ef5f174` はOPEN、source CURRENT。
unit attempt `ad90b376c7754b069cfa6f27b004f700`、receipt attempt
`3e4261e8c3754a269062abc3df4d3c5e`。いずれもgate PASS、受入はREVIEW_REQUIRED。

```powershell
python -B tools/codex_environment.py begin environment-batch2
python -B tools/codex_environment.py report environment-batch2
```

観測時点で検証2試行、検証コマンド合計65.47秒、raw log 310 bytes、記録された表示3回・
本文330 bytes。再閲覧分も数えるので、表示量がraw log量を超えることがある。
これは今回adapterを経由した検証・表示だけ。チャット全体の時間/使用量ではない。
実モデルtokens・人の介入回数・一般品質の改善は未測定で、0に置換しない。
ローカルの詳細はignored `.harness-runtime/batch2-operation-report.json`。

## 速度とメモリの比較、標準採用を見送った要素

初期のstream試作は小ログのメモリ負担を増やし、速度の改善も安定しなかった。
さらに同一入力・交互実行で比較したところ、低メモリと速度の利得は同一ではなかった。
そのため標準は第1バッチの読込方式を維持し、`output --stream`を明示試験に限定した。
原文/過去比較記録は削除していない。

最終実装で7反復、同じraw bytes・offset/countを使用し、全戻り値の一致を確認した。

| 合成入力 | baseline中央値 | 現行標準中央値 | stream中央値 | Python allocation peak中央値 baseline / 標準 / stream |
|---|---:|---:|---:|---:|
| 1,400 bytes | 1.898ms | 1.863ms | 1.793ms | 11,455 / 11,455 / 79,501 bytes |
| 1,310,720 bytes | 8.447ms | 7.673ms | 8.623ms | 5,244,441 / 5,244,546 / 434,225 bytes |

ファイルcacheが温まった局所比較で、tracemallocの負担も含む。RSS、Codex全体の速度、
実token削減、将来の無劣化を証明する数値ではない。標準経路の性能改善も一般化しない。
最終比較はplan・入力・全反復値・baseline/candidateソースを保存した:
`.harness-runtime/io-benchmark/72ae2bfd5d244da49cdd00a078e660df/`。

## 残る作業

次の実案件で、目的保持・再入場・古い証拠の防止・誤停止・再検証負担を観測する。
同条件の実作業比較と実usage取得が揃うまでは、総合性能やtoken削減率を断定しない。
今の運用はこのworkspace/入口の範囲。global設定やCodexの全native toolを強制するものではない。
Coreへの昇格・公開・main統合・本番移行・既存証跡削除は別のHuman承認を要する。
