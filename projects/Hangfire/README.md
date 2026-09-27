# Hangfire Codex Form

Hangfireゲーム開発で、毎回のCodex指示を同じ形式で作るための常設フォーム。

## 開くファイル

`CODEX_TASK_FORM.html`

ブラウザで開く。

## 役割

固定仕様はフォーム内に保持し、毎回変更する項目だけ入力する。

- CURRENT_LAYER
- TARGET
- ALLOWED_FILES
- DO_NOT_TOUCH
- ACCEPTANCE
- STATUS

「Markdown生成」でCodex用の指示全文を生成する。

## 出力

- 画面表示
- クリップボードへコピー
- `HANGFIRE_TASK.md` として保存

## 注意

このHTML自体はゲームコードを実行・変更しない。
Codexへ渡すMarkdownを生成するだけ。

Source of Truthとなる固定仕様を変更する場合は、フォーム内の固定仕様も明示的に更新する。


## ASTRA実行入口

Codex ASTRAでHangfire開発を開始・再開する場合は、

`ASTRA_START.md`

を最初のProject実行指示として使用する。

ASTRAは各Layerで、

`PRE-FLIGHT → PLAN → IMPLEMENT → VALIDATE → OMISSION CHECK → CHECKPOINT → PROJECT更新 → STOP`

の順で進める。

各Layer完了時の記録は `checkpoints/` に保存する。


## Server Architecture

無料枠または極低コストの小規模Serverを前提とする構成方針は、

`SERVER_ARCHITECTURE.md`

を参照する。

ASTRAはBackend / Infrastructure変更前にこのファイルを確認する。


## Gear Collision

機体への当たり判定の正式ルールは、

`GEAR_COLLISION.md`

を参照する。

見た目と被弾判定を分離し、Hit Point + Direct Hit Radius方式を採用する。


## Tuning

Balance値の集中管理と将来のHuman Playtest調整方針は、

`TUNING_POLICY.md`

を参照する。

本格的なEditorは後回しにし、各Layerで必要なTuning値だけを追加する。

## Layer 3 Playground（Layer 1・2を継承）

Node.js 22以上。外部package不要、npm install不要。
このディレクトリ（projects/Hangfire）で実行する。

~~~powershell
npm run build
npm test
npm start
~~~

Browserで http://127.0.0.1:3000 を開くとClientが起動する。
Serverが静的Clientも配信するため、Client用の別processは不要。
配布用buildは dist/ に生成され、node dist/server/index.js でも起動できる。
停止は起動terminalでCtrl+C。

Angle / Powerを入力してFireを押す。Serverから受信した点列をCanvasで
補間表示し、Server着弾座標を表示する。表示倍率は軌道全体に自動調整する。
接続失敗時はServerを確認して再読み込みする。

### 風の確認

風の変更はServer起動時のみ。Clientに風変更APIやTuning UIはない。
PowerShellの別terminalで以下を実行すると3条件を比較できる。

~~~powershell
# 無風（標準）
$env:WIND='0'; $env:PORT='3000'; npm start
# 右風（別terminal）
$env:WIND='12'; $env:PORT='3001'; npm start
# 左風（別terminal）
$env:WIND='-12'; $env:PORT='3002'; npm start
~~~

それぞれのportをBrowserで開く。初期位置のPlayer A、Angle=45 / Power=55で着弾Xは
左風128.500 / 無風196.750 / 右風265.000。同じ位置・入力・風なら結果は同じ。発射には現在手番とResourceが必要。

### Authority / tuning / cost

- GET /api/state: Serverのwind、tuning、turnTuning、hitTuning、players、currentPlayer、logicalTime、revision、lastAction、latestShot、matchState、winnerを取得。
- POST /api/fire: playerId、expectedRevision、angle、powerだけを受理。移動APIと同じ手番・Resource検証を通す。旧入力だけでは発射できない。
- Serverだけが初期位置・速度・風・着弾・pathを決定し、最新結果をmemoryに保持。
- pathは時刻順の {t,x,y} 点列。隣接点を将来の線分判定へ渡せるがGear判定は未実装。
- server/tuning.js がGameplay値の唯一の定義。値は独自の暫定値。
- 最大風力を70%にする場合、WIND_MAXを12から8.4へ変更。
  WIND_MINは-WIND_MAXなので対称に追従する。再起動し、build/testも再実行する。
  既存のWIND=±12起動例は新しい範囲の±8.4へ変える。他のBalance値は変更しない。
- 重力は下向き、風は水平方向加速度。単位はworld unitと秒。
- 計算は発射時のみ。path上限1024点、body上限1024 bytes、保持結果は最新1件。
- Clientは描画中だけrequestAnimationFrameを使い、終了後は常時loopを回さない。
- デフォルトはloopbackのみ。hostingは未選定・未公開。必要時HOST/PORTでbindを設定可能。
- 無料枠の実測、10年前の実機性能は未検証。構成は1 process / Canvas / dependencyなし。
- 認証・rate limit・Room・履歴永続化はない。共有Playgroundであり対戦Serverではない。

最新の検証記録: checkpoints/LAYER_03_2026-09-27.md（Layer 1・2記録も保持）

### Layer 2の操作とルール

固定Player A / Bの共通Playground。操作対象selectは試作用hotseat入力で、
ログイン・認証ではない。受理後はServerのcurrentPlayerへselectが追従する。
別Playerを選んで操作すればServerの手番拒否を確認できる。

- Playerごとにposition、resource、nextActionTimeをServerが保持。
- FIRE: Resource 20、Action Cost 30。angle/powerでLayer 1弾道を使用。
- MOVE: left/right、整数amount 1..20。Resourceはamount × 2、Action Cost 10。
- 初期Resource 100、AのX=0、BのX=60。移動後のFIREはそのServer位置から発射。
- 行動後にnextActionTime = 行動開始時のlogicalTime + Action Cost。
- 次PlayerはnextActionTime最小、同値ならID昇順（A→B）。
- logicalTimeは次PlayerのnextActionTimeへ進む論理値。実時間待機・Timerなし。
- A FIRE後、BがMOVEを3回行うと、予定時刻A=30/B=30となりAの手番。
  単純交互ではなく、Action Costの差が行動順に反映される。
- lastActionにServerが適用したResource / Action Cost / 次回時刻を表示。
- 他のBrowserから操作した後は「Server状態を更新」で取得する。常時pollingなし。
- Resource回復・PASS・自動skipは指示範囲外のため未実装。枯渇すると進行できない
  場合がある。Playtestをやり直すにはServerを再起動する（Browser再読込では回復しない）。

POST /api/moveはplayerId、expectedRevision、direction、amountのみ。
expectedRevisionは直前に取得したServer revisionを返す前提条件で、状態を書き換える値
ではない。非手番、Resource不足、古いrevisionは409。入力不正・追加fieldは400。
拒否ではresource / position / 時刻 / shot / revisionを含む全Stateが不変。
Serverは検証と弾道計算の成功後に一度だけStateをcommitする。
同じrevisionの同時要求は最大1つだけ受理される。通信失敗時に自動再送しない。

Layer 2値はserver/tuning.jsのTURN_TUNINGへ集中。例えば移動Resourceコストを70%に
するならMOVE_RESOURCE_COST_PER_UNITを2→1.4、射撃後遅延を30%増やすなら
FIRE_ACTION_COSTを30→39へ変更してbuild/test/再起動する。
現在値はAI-selected / Provisional。Layer 1値は変更していない。

検証コマンド: npm run check / npm run build / npm test。
Layer 1の純粋弾道テストは維持。HTTP回帰テストはactor/revision付き要求と
State応答へ適応し、弾道とAuthorityの元の検証を維持している。
Layer 2では非手番拒否、Resource消費/不足、State不変、行動順、左右移動、
移動後発射、改変field拒否、同時要求を追加検証する。

### Layer 3: Hit / Damage / Victory

Serverの各PlayerはHP、eliminated、visualOrigin / hitPoint / groundContactPointを持つ。
MOVEで各基準をServer側で更新する。見た目のサイズや描画位置は当たり判定の正本ではない。
FIREの自由飛行pathはLayer 1の式をそのまま使い、各線分とhitPoint円の最初の交差、
または平地到達で打ち切る。Gear同時接触はID順、Terrainとの完全同時接触はTerrain優先。

- hitPoint = position + (0,4)、Direct Hit Radius=2、HP_MAX=100（暫定）。
- 最初のcollision pointがExplosion Center。直撃対象にはDirect Damage=60。
- 他の生存Playerは発射者も含め、hitPointまでの距離でSplash判定。
- 距離がBlast Radius=18未満なら ceil(40 × (1 - distance/18)^1)。
  半径境界・外側はDamage 0。直撃対象へSplashを二重加算しない。
- 一つのExplosionの全Damageを計算後、一括でHPへ適用。HP下限0、HP0でeliminated。
- 生存者1人ならそのIDをwinner、0人ならwinner=null（Draw）。matchState=finished。
- eliminatedは手番対象外。finishedでは追加FIRE/MOVEをServerが拒否しState不変。
- hp/damage/winner/directHit/explosionCenter等をClientから注入する要求は拒否。
- Resource / Action Costは命中成否に関係なくLayer 2の値を維持。
  Resource不足では衝突処理前に拒否。回復/PASSは引き続き未実装。
- UIはHP・脱落・Direct/Splash/Miss・Damage・Winnerを表示。
  DEVチェック時のみHit Point/RadiusとExplosion Center/Blast Radiusを重ねる。
  描画toggleはServer Stateを変更しない。地形破壊やGear差ではない。

Human Playtest例（無風、再起動直後、初期位置）:
1. A: Angle45 / Power28 → BにSplash28、HP72。
2. B: Angle45 / Power55 → Miss、HP変化なし。
3. A: Angle45 / Power30 → BにDirect60、HP12。
4. B: Angle90 / Power10 → 自爆でB HP0、Winner A、finished。
敵を直撃で倒す例はA(45/30)、B(45/55)、A(45/30)。
再プレイはServer再起動。勝敗後のBrowser再読込でもfinishedは保持する。

Layer 3値はserver/tuning.jsのHIT_TUNINGのみで調整する。
例: DIRECT_HIT_RADIUSを2→1.7（85%）、BLAST_RADIUSを18→21.6（20%拡大）、
HIT_POINT_Yを4→-2（6単位下げる）。変更後はbuild/testとServer再起動。
DIRECT_HIT_DAMAGEとBLAST_DAMAGE_MAXは別々に調整できる。
数値は正式Balanceではなく独自の暫定値。Layer 1・2の値は変更していない。
地形破壊、落下、15秒Timer、Room/Team/Item等のLayer 4以降は未実装。
