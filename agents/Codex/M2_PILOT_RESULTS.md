# M2初回結果 — 2026-10-31

**限定した読み取り診断の実usageは取得できたが、文脈選択方式の一般採用は保留。M2/M3は未完了。**
対象は2種類の実ソース監査×2方式×2反復、合計8回。コード実装・長時間継続・実際の
context compactionや一般開発能力を測った試験ではない。
計画は[M2_PILOT_PLAN.md](M2_PILOT_PLAN.md)。実装担当subagentやモデルによるツール操作は使用していない。

## 1. 実測結果

| 項目（各方式4回答の合計） | baseline: 関連ソース全体 | candidate: 関連関数を選択 |
|---|---:|---:|
| input tokens | 134,164 | 72,420 |
| cached input（上記の内数） | 11,520 | 0 |
| output tokens | 3,177 | 3,242 |
| input + output | 137,341 | 75,662 |
| CLI起動・待機を含む応答時間 | 72.91秒 | 80.60秒 |
| 事前graderの形式合格数 | 1/4 | 2/4 |

この小さい比較では合計tokensは44.91%少ない一方、時間は10.55%増えた。
cached/reasoningの内数を再加算していない。両方式を実行した今回の試験自体の合計は
213,003 tokensであり、運用全体で61,679 tokensを節約した実績という意味ではない。
料金・利用枠の換算や、本文bytesによる推計はしていない。

| ペア | candidateのtoken差 | candidateの時間差 |
|---|---:|---:|
| checked-reentry 1 | -15,446 | +4.44秒 |
| checked-reentry 2 | -15,340 | +7.67秒 |
| runtime-drift 1 | -15,490 | -3.20秒 |
| runtime-drift 2 | -15,403 | -1.22秒 |

再開診断では2回とも遅くなり、環境差異診断では2回とも短くなった。
平均だけで悪化を隠さない。cacheの偏り、待機、推論のばらつきがあり、速度差の原因や
将来の改善率は断定しない。packetの手動選択/準備や全作業時間もこの時間には含まない。

## 2. 品質比較で判明した評価契約の不足

事前schemaはevidence.sourceを任意文字列としていたが、graderはファイル名の完全一致を
要求していた。関数名やJSON位置を添えた正常な引用参照もFAILに数えてしまった。
この指定不足は評価側の問題であり、上の形式合格数をモデルの一般品質と解釈しない。

元のplan・grader・全回答・一次採点は上書きしていない。
後から参照位置のsuffixを解決して凍結原文と照合した診断用auditでは、全8回答の全引用が
原文中に存在した。これは事後の原因切分けであり、元のFAILをPASSへ変更していない。
診断/action/主目的/承認境界のコードも期待と一致したが、自由記述全体を認証するものではない。

自由記述の確認ではcandidateのcall 2に、証拠が有効な場合にも再検証を勧める記述があった。
実際に再検証を実行させた試験ではないため、人の負担や追加実行回数は未測定。
次回は「有効な証拠のgate再確認」と「検査の再実行」を区別する判定を事前に設ける。

今後用のschemaはsourceをenumで限定し、promptにもsuffix禁止を明記した。評価コードの
変更後に追加のモデル呼出しや同trialの再実行は行っていない。上限8回を維持した。

## 3. 確認できた実不具合の修正

`finish`でCHECKEDになった後、`begin TASK`が保存済みcontractを取得せず
`First begin requires an explicit --contract`で止まる問題を再現した。
保存済みcontractの取得とsource/目的の照合を、OPENだけでなくCHECKEDにも適用した。
最小修正で、以下の4回帰を修正前FAILから修正後PASSへ変更した。

- CHECKED後、contractを再指定せず新しいOPEN運用を開始できる。
- source変更は黙って受け入れずSOURCE_STALEで停止する。
- 目的変更は照合・明示refreshを要求し、以前の検査を現在のPASSへ流用しない。
- next_stepだけの更新で不要なcontract再指定を要求しない。

実運用タスクでもfinish→beginを実行し、新しい運用ID・CURRENT・現行PASSを確認した。
元の運用イベントは保持。自動文脈選択や新サービスを標準導入していない。

## 現行コードの検証

| 検査 | 結果 |
|---|---|
| 全体回帰 | 97件中96成功・1skip。Windows symlink権限による1件は未実施 |
| 今後用の評価parser/schema | 9/9成功 |
| 既存receipt互換性 | 9/9成功 |
| 生成した最終receipt 3件 | 既存checkerで全件OK |
| 保護領域 | HARNESS/Core/既存TRINITY/評価成果物/保存提案/他projectにtracked差分なし |

モデル試行の一次採点と、現行コードに対するこの回帰検査は別物。
回帰PASSを、品質比較の判定保留の解消やM3承認の代わりにしない。

## 証跡と現在の状態

元trial `.harness-runtime/m2-pilot/de2c3845e526423b815fcd4836eed423/`。
plan hash `3bf9fb84b43bd03c9be7738c895e0b3d7e33993eb067c51c359dde0b31cda3a5`。
凍結したplan対象ファイルと保存済みgraderのhash一致を、修正後にも確認した。
生JSONL、stderr、回答、実usage、一次結果、comparison、citation-contract-audit、reviewを保存。
同一trialは再実行を拒否し、liveのコード修正で過去の入力を差し替えない。
全呼出しに共通してPowerShell shell snapshot非対応の警告があったが、モデルのツール使用は検出されなかった。

現行タスク`environment-m2-pilot`、ブランチ`codex/environment-upgrade-batch1`。
再開不具合修正後の新運用ID `8a8b1628f22f45938025d46243d2d141` はOPEN/CURRENT。
unit/receipt-compatibility/evaluation-parserはPASS、受入はREVIEW_REQUIRED。
変更は未commit。push・公開・main統合・本番移行・既存証跡の削除はしていない。

## 次のM2

新しいケース計画で出典表記と余分な再検証の扱いを先に定義する。
同じtrialをやり直してよい結果だけを採用しない。
実装や継続作業に範囲を広げ、品質・時間・実usage・確認負担の同条件比較を行う。
今回の文脈選択方式は、速度悪化と品質判定の不足があるため一般採用しない。
M3のHuman判断・公開等の承認境界も維持する。
