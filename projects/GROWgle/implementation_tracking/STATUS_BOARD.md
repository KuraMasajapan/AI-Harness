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

## パイロットページの実装状況（2026-10-21 / v0.6）

> 試作ZIPに反映した内容の進捗。GitHub内の**正式公開サイトへ反映済み**という意味ではありません。

| 判定 | 現状 |
|---|---|
| 地域活動記録の試作収録 | **87件**（v0.5の28件＋59件） |
| 体験参考カード | **27件**（今回変更なし） |
| 活動記録に候補がある市町村 | **24 / 27** |
| 活動候補が未収録の市町村 | 和気町、久米南町、新庄村（活動がない意味ではない） |
| 完了審査 | **全件未完了**：一次情報の再照合とHuman正式公開判定が必要 |
| v0.6に一部が含まれた原資料 | 岡山南部ENTRE、岡山北部ENTRE、岡山南部CROSS_CATEGORY、岡山北部CROSS_CATEGORY、倉敷企業教育詳細の計5MD |
| 追加検出した新規資料 | `KURASHIKI/CHECKPOINT_ENTERPRISE_PILOT_2026-10-14.md`（個別レコード抽出は未完了） |
| 追加検出した更新資料 | `KURASHIKI/ENTERPRISE_RESEARCH_HANDOFF.md`（差分確認待ち） |

新規・更新の検出は [GitHub Actions](https://github.com/KuraMasajapan/AI-Harness/actions/workflows/growgle-md-intake.yml) が担当。
**検出＝実装ではありません**。試作版への反映は、個々の活動の出典・重複・募集状況を確認したうえで行います。

v0.6の活動レコードは会話内のZIPとして出力済みですが、現段階ではGitHubの公開サイトにはデプロイしていません。リンク先に最新の募集があるとは限りません。

