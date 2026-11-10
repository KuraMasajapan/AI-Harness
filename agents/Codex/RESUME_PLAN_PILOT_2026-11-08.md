# Codex再開表示の試行結果 — 2026-11-08 JST

対象: `codex/environment-upgrade-batch1`、HEAD `2431c09`、ローカル変更を含む試行。
目的: 再開時に重要な制約と判断を保持し、何を取り直すべきかを短く伝える。

```powershell
python -B tools/codex_views.py resume-plan environment-m2-pilot
```

既存の `operation` とenvironment gateを読み取る任意の表示経路。
版付き記録の目的・次工程・重要制約・判断・レビュー項目を原文のまま含める。
新規の検証機構、権限付与、検証の自動再実行は行わない。

| 表示 | 読み方 |
|---|---|
| RECONCILE | source/taskなどを照合し直す。現在の指示と実ファイルを確認し、必要な場合に明示refresh |
| VERIFY_REQUIRED | 証拠が不足または失効。実行中かどうかと失効理由を確認して、必要な検証だけ取り直す |
| RECONFIRM | 現行証拠は揃っている。現在の依頼・必要なHuman判断を確認して再利用できる |

終了コード0は表示生成の成功。検証PASSや採用判定はaction/checks/acceptanceで別に読む。
従来の詳細確認は既存 `operation`、検証は既存environment入口を使う。
使わなくなった場合は旧入口へ戻るだけでよく、過去証跡は削除しない。

## 観測

- 再起動後の実記録で、sourceはCURRENT、4チェックはRuntime changedでNOT_CURRENT。
- この改修でsource差分がある間はRECONCILE、確認後の明示refresh直後はVERIFY_REQUIRED。
- 4チェック取り直し後はRECONFIRM。149件中148成功・既存skip 1件、FINAL receipt4件OK。
- 同一revision 35を対象に、既存B/候補Cを事前固定順 B C C B B C で各3回実行。
  目的・次工程・重要制約7件・判断2件・レビュー項目・検証状態・acceptanceが一致。
- stdoutは5,073→3,982 bytes（約21.5%減）。CLIの中央値は3.94→3.17秒。
- Windowsの日本語JSONを既存CLIと同じUTF-8で出力。集計中にcheckpoint revisionが変われば停止。

この観測は1つの実チェックポイントに対するCLI出力比較。モデル呼出し0。
表示bytesをtoken削減とみなさない。反復数が少なく、総作業時間、実token、人の負担、
コンテキスト圧縮後の理解・品質、全タスクでの速度非劣性は未確認。
一般採用せず、再開時の任意コマンドとして試行する。モデル8回の元試行は保持。

根拠はignored `.harness-runtime/resume-plan-pilot/dfc7e7180393470a806a41861e94f7a6/`。
plan、check結果、receipt照合、各stdout、観測値を保存。

## V2への接続

この範囲の再開・検証・証拠保存が揃い、V2の設計を始める目処が立った。
[V2移行草案](../../incubator/proposals/2026-11-08-harness-v2-transition.md)に、
再開、証跡、共有文脈の3境界と既存6層への対応を整理した。
V2の実行経路への切替や正式採用は別工程。M2の一般効果とM3の採否は未完了。
