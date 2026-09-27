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

## Layer 4 Playground（Layer 1〜3を継承）

Node.js 22以上。外部package / npm install不要。
projects/Hangfireで実行:

~~~powershell
node scripts/build.js
node --test
node dist/server/index.js
~~~

Browserで http://127.0.0.1:3000/ を開く。Clientも同じServerが配信する。
PORTでport、WINDで風を指定可能。今回の確認用Serverはport3004。
Ctrl+Cで停止、再起動で状態初期化。Browser再読み込みでは初期化されない。

### 操作

- A / D: 長押しの連続移動、離すと停止。
- ↑ / ↓: 長押しAim（180°を5秒）。移動と同時使用可能。
- 現在Gearを左クリックしたままdrag: pointer方向へ即時Aim。
- Space: 0から等速充電。離すと発射、5秒MAXで自動発射。
- 20秒で強制Turn End。期限前に始めた充電だけは継続し、以後移動/Aim禁止。
- 発射→飛翔→着弾Damage→短いeffect完了後、Serverが次手番/勝敗を確定。
- DEVチェック: 全関連tuning、Server時計・入力・Resource・移動距離・HP・衝突結果を表示。
- 固定2人hotseat。認証された対戦ではない。入力はServer選択のcurrentPlayerに送る。

### Authority / tuning

GET /api/state はtuningとServer stateを取得。
POST /api/input はplayerId / turnId / sequence / typeとtype固有入力だけを受理する。
HOLD(move,aim: -1/0/1)、AIM(angle)、CHARGE、RELEASE。
Clientの時刻・power・position・damageは受理しない。
旧POST /api/fire、/api/moveは通常runtimeでは404（テスト専用内部legacyTestModeのみ）。

server/tuning.jsがGameplay値の集中管理箇所。
INPUT_TUNINGに20秒、5秒充電、5秒Aim、共通move速度、境界、effect時間を定義。
Power0..100、Aim0..180へ採用仕様どおり拡張。旧範囲の弾道式は変更なし。
風は起動時のみ（WIND=-12 / 0 / 12）。同じ位置・入力・風なら同じ結果。

Resourceは実移動距離×2、FIRE20。充電中はFIRE資源を予約。
Layer2のnextActionTime選択とID tie-breakを維持し、移動のlogical costは旧5距離/10costを比例適用。
timeout base10、FIRE base30。これは暫定互換境界であり、本格的Turn Load式ではない。
Elapsed/distance/resourceUsedは記録するが、4要素負荷、回復、Weapon/Item/Gear差は未実装。

### 検証 / 制限

node --test: 39件（Layer1〜3の25回帰＋Layer4の14）。
旧HTTPテストは内部legacyTestMode、Layer4は通常HTTPとfake-clock境界も検証。
Evidence: checkpoints/LAYER_04_2026-09-27.md。
Browserで移動/Aim/Space発射、drag、DEV表示を確認。
長押し時間の厳密検証は自動テスト。Humanによる操作感確認は継続する。

一process/in-memory、Node標準HTTP + Canvas。追加dependencyなし。
Resource回復・manual Skip・Room・Team・Gear差・地形破壊・latency compensationは未実装。
Clientは100ms間隔でstateを取得。切断時もServer deadline/MAXは進行する。
Serverはeffectの固定時間を待つが、非表示/停止したBrowserの描画完了通知は待たない。
hosting実測・10年前の実機性能は未検証。Layer5へ自動で進まない。

## Layer 5 Lobby / Room / Communication

通常起動はLobbyモードです。外部package・DB・Redis不要。

- Guest Loginでdisplay nameを送るとServerが一時session ID / Player IDを発行します。
- Create Roomで1v1/2v2/3v3/4v4を選択し、invite codeで参加します。
- 入室順でTeam A/Bを交互割当。正確な人数・同数TeamだけhostがBattle開始できます。
- Roomは最大8人。Battle中の任意退出・途中参加・Team変更は不可です。
- Host退出／切断時は最古の残存参加者へhost権限を移譲します。再ログイン復帰はありません。

CommunicationはRoomから独立したServer routingです。LOBBY、ROOM、BATTLE_GLOBAL、
BATTLE_TEAM、WHISPERを使用し、BATTLE_TEAMは同Teamだけへ配信します。
WhisperはPlayer ID指定で所在に依存しません。短期memory履歴、500文字制限、
10秒あたり5件のrate limitがあります。Voice、NPC takeover、永続profileは未実装です。
Themeのdefault色はclient表示属性として定義し、channel判定には使用しません。

Layer 5 evidence: `checkpoints/LAYER_05_2026-09-28.md`。
