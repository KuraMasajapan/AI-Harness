# GROWgle 岡山県パイロット — 実装状況ボード
作成日: 2026-10-20 / 対象: `main` / UI参照: **v0.5試作**（GitHub未配備）

## 現時点の集計
| 種類 | 件数 | 注記 |
|---|---:|---|
| 岡山パイロット対象MD | 10 | 調査・チェックポイント・引継ぎを含む |
| 一部試作へ抽出 | 4 MD | **完了ではない** |
| 未精査 | 6 MD | 既存体験カードを含む全面照合は未実施 |
| 仕様/方針/AI別モジュール | 6 MD | 体験カード収録対象と分離 |
| 他県のMD | 49 | 岡山対象外（将来の地域拡張用） |
| v0.5地域活動の試作カード | 28 | 4 MD由来、正式公開承認0 |
| v0.5体験参考カード | 27 | 原典逆引きが未完成、公開検証済みではない |

## 岡山対象MD
| MD | 文書処理状態 | v0.5活動記録への抜粋 |
|---|---|---:|
| [岡山北再調査](../CROSS_CATEGORY/OKAYAMA_NORTH_RESCAN_V0_1.md) | 一部試作抽出 | 5 |
| [岡山南再調査](../CROSS_CATEGORY/OKAYAMA_SOUTH_RESCAN_V0_1.md) | 一部試作抽出 | 10 |
| [北部ENTRE](../ENTRE/OKAYAMA_NORTH_RESEARCH_V0_1.md) | 一部試作抽出 | 1 |
| [倉敷企業教育詳細](../KURASHIKI/KURASHIKI_ENTERPRISE_EDUCATION_PILOT_V0_1.md) | 一部試作抽出 | 12 |
| [南部ENTRE](../ENTRE/OKAYAMA_SOUTH_RESEARCH_V0_1.md) | 未精査 | 0 |
| [岡山北部候補](../CROSS_CATEGORY/OKAYAMA_NORTH_SEEDS_V0_1.md) | 未精査 | 0 |
| [県内初回チェックポイント](../CHECKPOINT_OKAYAMA_V1_2026-10-04.md) | 未精査 | 0 |
| [カテゴリ再走査チェックポイント](../CHECKPOINT_CROSS_CATEGORY_RESCAN_2026-10-04.md) | 未精査 | 0 |
| [深度校正・追加調査](../SECOND_PASS_CALIBRATION_2026-10-07.md) | 未精査 | 0 |
| [倉敷企業調査引き継ぎ](../KURASHIKI/ENTERPRISE_RESEARCH_HANDOFF.md) | 未精査 | 0 |

*注：0件は「未掲載の情報が0件」の意味ではなく、今回の原典パスで追跡した28件の試作活動記録に紐付く件数が0という意味。*

## 次回作業時
1. `python3 projects/GROWgle/implementation_tracking/check_sources.py` で新規・更新MDを検出
2. 更新箇所を既存レコードIDと突合
3. 企画別にサイト反映・公開可否・重複・対象外を記録
4. このボードを更新し、差分が消えた時点でスナップショットSHA更新を検討

※ 本ボードは**固定スナップショット**。MD差分の検出はGitHub Actionsが自動実行しますが、未実装・実装済みの確定とボードの書き換えはレビュー後に行います。

## 自動チェックの確認先

**[GitHub Actions：GROWgle MD 取り込みチェック](https://github.com/KuraMasajapan/AI-Harness/actions/workflows/growgle-md-intake.yml)**

各実行の Summary に追加・更新されたMDや未精査資料が表示されます。
このボードは人による照合状況を記す**固定スナップショット**であり、Actionsで自動的に「実装済み」へ変わることはありません。
Actionsの成功は**検出処理が成功した**という意味です。
