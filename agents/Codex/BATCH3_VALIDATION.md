# 第3バッチと今回の到達点 — 2026-10-31

**M1のローカル実装・機械検証は一区切り。M2の実作業での効果確認とM3の採用判断は未完了。**
継続改修全体を終える意味ではない。[GOALS.md](GOALS.md)で今回の完了条件を定義した。
主目的はCodex環境整備。TRINITY単体の機能開発や本番移行は行っていない。

## 今回の3件

1. GOALSで、M1運用基盤・M2効果確認・M3採用判断を分離。各バッチを閉じる条件も明文化。
2. reportは標準20試行/最大100試行の表示へ変更。全試行の集計を維持し、hash固定で続行。
3. 選択した検証入力の実体をcontent-addressed objectへ保存。未commit bytesと明示的な
   外部依存を、元ファイルへrestoreせず閲覧可能にした。manifestと実行入力の差はSTALE。

保存提案との比較・採否は[ADOPTION.md](ADOPTION.md)の第3バッチ。
同目的の新DBや新サービス、TRINITY protocol変更は導入していない。

## 検証結果

| 対象 | 結果 |
|---|---|
| 全体回帰 | 93件中92成功・1skip。Windows symlink権限に依存する1件は未実施 |
| 既存receipt | 9/9成功。developmentのchecker/schema/testsは変更なし |
| 生成した最終receipt 2件 | 既存checkerで両方OK |
| 別プロセスのCLI再入場 | 同一運用IDを再利用、重要制約を復元、CURRENTと両チェックPASSを確認 |
| reportの2ページ取得 | 各1件表示、全2試行の集計を維持、同一hashで続行 |
| snapshotの2ページ取得 | 表示上限とmanifest hash固定を確認 |
| snapshot-file | 実際のtools/codex_environment.pyの保存bytesと表示先頭100文字が一致 |
| 保護領域 | HARNESS/Core/既存TRINITY/評価成果物/保存提案/他projectにtracked差分なし |

新規12テストには、元ファイル変更後の原文取得、同内容の再利用、破損objectの上書き拒否、
manifest破損、snapshot保存失敗時の古いPASS無効化、保存と実行の間の入力変更、binary保持、
明示外部依存の固定、path逸脱防止、全件集計と表示の分離、観測変更時のcursor失効を含む。

## 実証できた範囲

M1の条件に対応する証拠:

- 再入場・重要条件の復元: 第1/2バッチと今回の実CLI。
- 古い入力/環境・失敗の識別: 既存の負例群と今回のsnapshot失敗/途中変更の追加試験。
- 入力実体の保持: 今回のobject/manifest、原文取得テストと実CLI。
- 原文ログと版固定取得: 第1/2バッチと今回のreport/snapshot cursor。
- 観測と欠測の分離: reportのPARTIAL/null、全件集計を維持するページ試験。
- 許可範囲と保護領域: branch確認、差分確認、公開/本番操作なし。

これはローカルの機械動作と今回の限定した操作の証拠。
モデルが圧縮後も一般タスクで必ず目的を保持する、総合性能が向上した、実tokenが減った、
という証明ではない。M2/M3を機械PASSで代替しない。

## 運用と証跡

branch `codex/environment-upgrade-batch1`、基準development `7ae57c2`。
作業ツリーの変更は未commitのまま保持。既存の変更・過去証跡は消していない。
タスク`environment-batch3`、checkpoint版2、運用ID
`ec149315524e44fcbd5d1a1b389b1c66`、OPEN/CURRENT。

unit attempt `bf1ee8e66ed34a448f56fc4252878fee`、receipt attempt
`aa0732e273894eadb66a5bda31e168ce`。両チェックPASS、受入はREVIEW_REQUIRED。
詳細はignored `.harness-runtime/batch3-cli-smoke.json` と `batch3-operation-report.json`。

今回の2試行は合計58ファイル参照を35個のobjectで保持し、原bytesは306,038 bytes。
manifest/receipt等のmetadata容量は別。保存にはIOと容量の追加コストがある。
選択したwatch/source/外部依存だけを保存し、全環境の再現や全会話の保存は行わない。
この数値を速度・実token・総費用の削減率へ読み替えない。

次回の入口:

```powershell
python -B tools/codex_environment.py begin environment-batch3
```

## 次はM2

実案件の同条件比較を先に設計し、品質・重要制約・誤停止・再試行・人の負担・
wall-clock・保存IO/容量・取得可能な実usageを確認する。
新しい機能は、その比較で確認できた不足に優先して追加する。
品質が下がる候補や効果が不明な候補は採用しない。
公開/push、main統合、本番移行、既存証跡やデータの削除は引き続きHuman事前承認。
