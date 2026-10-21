# GROWgle — MD取り込み追跡台帳（岡山県パイロット）

目的：GitHubに増え続けるMD資料と、サイトへの掲載状態を混同せず追跡する。

- `source_inventory.json`：GitHub `main` のファイルSHAを持つ初回スナップショット。岡山対象・他県（将来）・方針資料を区分。
- `check_sources.py`：GitHubの最新ツリーとスナップショットを比較し、追加・変更・削除を表示。**読むだけ**で自動掲載や自動承認はしない。
- `SOURCE_STATUS_RULES.md`：対象資料の精査から一般公開までの判定規則。

## 手順
```bash
python3 projects/GROWgle/implementation_tracking/check_sources.py
```

`main` に新規MDが追加・更新された場合、GitHub Actionsが差分検出を実行。必要に応じて手元からもチェック可能。
新規・変更MDは、内容を精査して重複を取り除いた上でレコード単位の台帳へ登録する。
**この初期スナップショットは自動更新しない**（ベースラインを書き換えると未対応を見逃す）。
レビュー担当が差分処理済みを確認した場合のみSHAを更新。

## 現状の意味
- v0.5の地域活動記録**28件**は試作掲載候補であり、正式公開済みは**0件**。
- 岡山県対象資料で `PARTIAL_PROTOTYPE` になったMDは、**一部レコードが試作に存在するだけ**。原文全件の処理完了を意味しない。
- 体験参考カード27件は、現状source_pathで一意に逆引きできないため、資料単位の処理完了判定に使わない。
- 他県のMDは `OUT_OF_CURRENT_PILOT` であり、「岡山パイロット未実装」ではない。
- 仕様/AI別モジュールは `REFERENCE_ONLY` として体験レコードの掲載状況と区別。

**注意**：GitHubのツリーはファイル追加・更新だけを確実に検出する。MD内での個別企画の追加・変更・取消・重複統合を判定するには、人またはAIによる内容比較とレコード台帳が必要。GitHub同期だけで公開承認にはならない。

## 自動検出（GitHub Actions）

- [GROWgle MD 取り込みチェック](https://github.com/KuraMasajapan/AI-Harness/actions/workflows/growgle-md-intake.yml) に実行履歴を表示。
- `main` にある `projects/GROWgle/` 配下が変更された際に自動実行（MD以外のファイル変更でも再検査）。
- 毎週月曜日19:35頃（日本時間）にも再点検（GitHub側の混雑で遅延する場合あり）。
- Actions画面の `Run workflow` から手動でも実行可能。
- 各実行の **Summary** に新規・更新・削除・未精査の一覧を表示。
- `growgle-md-audit` という成果物に閲覧用Markdownと機械読み取り用JSONを30日間保存。

### 自動実行されないこと（重要）
- 活動内容の抽出や一般公開判定の自動承認
- 新規MDを既存の掲載済みとみなすこと
- `source_inventory.json` の差分ベースラインSHAを勝手に更新すること
- `STATUS_BOARD.md` を勝手に書き換えること
- v0.5試作品や本番サイトへの自動公開

スナップショットとの差分は、人またはAIが個別案件を照合して処理するまで残る設計です。GitHub Actionsの緑色の成功マークは**検査プログラムの実行成功**であり、全資料実装済みを意味しません。
