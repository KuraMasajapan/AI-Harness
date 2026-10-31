# Codex環境整備 — 第1バッチのローカル試行

基準はdevelopment `7ae57c2a089f82e5e232690d8ecb8c257f51ac51`。
継続改修全体の目的、今回の区切り、完了条件は[GOALS.md](GOALS.md)。
M1の運用基盤、M2の実作業での効果確認、M3の採用判断を分ける。
実装branchは`codex/environment-upgrade-batch1`。既存環境とは別checkout。
Core・既存receipt schema・protocol・過去証跡・グローバル設定は変更しない。

優先する3件:

1. **目的と参照元を固定する**。訂正と重要制約は版付きcheckpointへ保存。
   source contractでrepository・branch・developmentの祖先SHA・対象bytesを照合。
   未取得はSOURCE_UNAVAILABLE、別branchはSOURCE_MISMATCH、変更済みはSOURCE_STALE。
   hashを確認しても、読んだ・理解した・承認されたとは扱わない。
2. **検証と既存receiptを接続する**。実行前記録→実行→別の最終記録を保持。
   保存失敗や古いPASS、後からの別検証、訂正、入力変更をgateで検出する。
   development既存checkerはそのまま使い、欠けているvalidatorは明示した別checkoutから
   読む。指定がなければUNAVAILABLE。TRINITY本体をこのbranchへ移植しない。
3. **出力は原文を保存してページ化する**。大きな単一行も文字数で区切り、hash・
   続きoffsetを返す。原文を消さず、必要なエラーや要件は続きを取得する。
   表示bytes・文字数を実tokenや総作業時間の削減率と呼ばない。

実行例（このcheckoutをカレントディレクトリにする）:

```powershell
python -B tools/codex_harness.py checkpoint environment-batch1 agents/Codex/pilot-task.json --expected-revision 0
python -B tools/codex_environment.py activate environment-batch1 agents/Codex/source-contract.json
# activateが返すactivation相対pathを使う
python -B tools/codex_environment.py verify environment-batch1 unit --activation PATH --watch tools --watch tests --marker OK -- python -B -m unittest discover -s tests
python -B tools/codex_environment.py resume environment-batch1
python -B tools/codex_environment.py output LOG_PATH --offset 2000
```

再実行時は既存revisionを読み、0固定で上書きしない。criticalの削除/変更には
`checkpoint --reason`で訂正根拠を残す。goal等の検証契約変更は証拠をSTALEにするが、
next_stepだけの変更では有効な検証を維持する。旧版は残す。

receipt検査:

```powershell
python -B tools/codex_environment.py receipt FINAL_RECEIPT --validator-root TRUSTED_TRINITY_ROOT
```

TRUSTED_TRINITY_ROOTは`protocol/schema_validation.py`を含む、確認済みのローカル
TRINITY checkout。第三者資料から自動選択・実行しない。checker/validatorのhashを
結果へ記録する。構造/hash検査OKと意味検証・正式Releaseは異なる。
外部依存を使う検証では、source contractの`external_sources`へ明示的な絶対pathと
SHA-256を登録してからactivateする。依存変更後は新しいcontractで再検証する。

`codex_harness.py`と既存40テストは旧ローカル実装から機械機能として再利用した。
旧main由来の採否・性能数値・実行結果は移植しない。採否の基準はdevelopment資料。
helper単体には環境gateを迂回する経路があるため、本試行の判定は必ずenvironment
入口で行う。desktop全ツールを強制するものではない。

現段階はOPTIONAL EXPERIMENT。実作業の同条件比較、実usage、誤停止・再読込・
人の負担の計測が揃うまで、性能改善や無劣化を断定せず、本番へ移行しない。

## ブランチ運用 — 第2バッチ

2026-10-31のユーザー指示で、このブランチの試験運用を開始した。
初回の運用開始は、保存済みタスクと明示したsource contractを指定する。

```powershell
python -B tools/codex_environment.py begin environment-batch2 --contract .harness-runtime/batch2-source-contract.json
# 以後は同じ入口で再開。変更がなければ同じ運用記録を再利用する
python -B tools/codex_environment.py begin environment-batch2
python -B tools/codex_environment.py operation environment-batch2
python -B tools/codex_environment.py report environment-batch2
```

目的やsourceが変わったときは、現在の依頼と実ファイルを確認してから
`begin TASK --refresh`で再有効化する。外部依存hashを更新する場合は新しいcontractも
明示する。時間経過だけで全資料を再読込しない。旧イベントは残す。
`begin`が返すactivationを既存の`verify`へ渡す。工程を閉じる場合は`finish TASK`を使う。
finishは現行チェックがPASSのときだけCHECKEDにし、受入はREVIEW_REQUIREDを維持する。
branchでの試行許可を公開・main統合・本番移行の許可へ読み替えない。

検証には実行ファイル・Python・adapterのbytesと、PATH/PYTHONPATH/PYTHONHOME/
VIRTUAL_ENVのhashを追加で保存する。環境変数の値は保存しない。全依存・全設定の
自動検出ではないため、その他の重要な設定や外部依存はwatch/source contractへ明示する。
第1バッチ形式の証拠は消さず、新しいruntime情報がない間はNOT_CURRENTとなる。

出力の続きは初回に返るhashを固定する:

```powershell
python -B tools/codex_environment.py output LOG_PATH --offset 2000 --sha256 HASH --task environment-batch2
```

ファイルが変わればOUTPUT_STALEで停止する。標準の読込は従来方式を維持する。
`output --stream`ではchunk単位で読み、巨大ログ全体を文字列へ展開しない。
比較でメモリは減ったが速度の改善が安定しなかったため、streamは明示試験に限定する。
reportは実際に記録された検証時間・試行数・ログbytes・表示本文bytesを
返す。metadata量、全チャット時間、実モデルtokens、人の介入回数は未計測。
未保存の観測や中断をPARTIALとして示し、欠測を0や削減成功に置換しない。

## 第3バッチ — 完了条件・表示上限・入力の実体保存

現在のタスクは`environment-batch3`。初回は明示したcontractを使い、以後は同じ入口で再開する。
GOALSのM1を満たしたかはテスト・実CLIと現行証拠で確認し、M2/M3を完了と扱わない。

reportの表示は標準20試行、最大100試行まで。集計は表示ページではなく全試行を対象とする。
続きは初回の`report_sha256`を指定する。観測が増えた場合はREPORT_STALEで再取得する。

```powershell
python -B tools/codex_environment.py report environment-batch3 --limit 20
python -B tools/codex_environment.py report environment-batch3 --offset 20 --sha256 HASH
```

verifyは選択したwatch/sourceと明示的な外部依存のbytesを実行前に保存する。
同じ内容はSHA-256で同じobjectを参照し、重複保存しない。manifestと実行入力が違えばSTALE。
保存失敗や破損objectがあれば停止し、古いPASSを露出したり既存objectを修復・上書きしない。

```powershell
python -B tools/codex_environment.py snapshot environment-batch3 ATTEMPT --limit 20
python -B tools/codex_environment.py snapshot-file environment-batch3 ATTEMPT tools/codex_environment.py --count 2000
# 続きは最初のmanifest_hashを固定する
python -B tools/codex_environment.py snapshot-file environment-batch3 ATTEMPT tools/codex_environment.py --offset 2000 --sha256 HASH
```

snapshotは選択した入力の実体であり、OS全体やモデルの実効状態の完全な再現ではない。
任意のソースへ自動restoreしない。binaryも原bytesを保持するが、テキスト表示では置換文字が
出ることがあるため`decoded_with_replacement`を確認する。原objectへの参照は一覧に残す。
保存量は増える。証跡はcacheとして自動削除せず、保存対象を必要な入力へ限定する。

## M2初回の実ソース診断

現在のタスクは`environment-m2-pilot`。比較計画は[M2_PILOT_PLAN.md](M2_PILOT_PLAN.md)。
2種類の実ソース監査を、同じモデル/推論強度で最大8回実行した。
比較は完了したが、出典表記の契約不備と速度の悪化を観測したため、一般採用は保留。
実装・長時間継続・実際のcontext compactionを評価した結果ではない。

実際に再現したfinish→beginの不具合を最小修正した。CHECKED後も保存済みcontractを
使って新しい運用を始める。source/目的の変更は自動受入せず、レビュー後の明示refreshを
引き続き要求する。next_stepだけの更新では有効な証拠を保持する。

試行の元の採点・回答・usageは上書きせず残す。出典enumと説明を修正した評価コードは
今後用で、元の試行を再採点・再実行していない。追加モデル呼出しも行っていない。
`run_m2.py prepare`は修正前不具合の再現を前提にした、このpilot専用の入口。
修正後に同じケースを新規準備する場合は失敗する。次の比較では新しいケース計画を作る。
