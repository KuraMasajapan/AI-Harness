# むーさん v13: 輪郭と執事パーツの精細化プロトタイプ

あるじの追加依頼と、ヘッドセット・蝶ネクタイ・執事服・白タオルの参照シート4枚を基準に、
v12をローカルのBlender処理で改修しました。画像を貼った板ではなく、実際のGLB形状です。
参照画像の外部送信、生成API、追加課金は使っていません。

## 差し替え

`Musan_Kitchen_Study_Refined_2026-11-27.zip` を展開します。

1. `models/musan-butler-refined-v13.glb` を、既存のv12と**置き換える**。両方を同時に表示しない。
2. `models/kitchen-study.glb` は最初のWide版と同一です。すでにWide版なら部屋の再交換は不要。
3. `muse/scene-placement.json` を使用する。位置・倍率はWide版を維持しています。
   GLB全体の根元へ変換を適用し、部品ごとに中心合わせしないでください。
4. 縦画面では横が切れないよう、元READMEの画面比率対応を適用してください。

元ZIPと最初のWide版ZIPは変更せずに保持しています。v13からv12へ戻せます。

## 改修点

| パーツ | 改修内容 |
| --- | --- |
| 頭・胴・手足 | 頭頂の丸いドームを緩めて角丸寄りの輪郭へ。肩幅・腹部・奥行きを絞り、サービス側の前腕を上げた姿勢へ |
| 顔 | 元の顔領域を維持し、黒目を滑らかに再生成。頬の淡い赤みと小さなU字の口へ |
| 毛並み | 暖色寄りに調整。短いテーパー状の毛24,000本と既存の毛並み法線マップを併用 |
| ヘッドセット | 片耳の丸角カプセル、黒い小孔、一体型マイクブームと先端を別グループで再制作。露出したヘッドバンドなし |
| 蝶ネクタイ | 中央で絞った翼と角丸の結び目。襟元へ合わせて衣装に統合 |
| 執事服 | 黒い燕尾服、サテン襟、柄入りベスト、白シャツ、胸チーフ、金ボタンを一体メッシュ化。前裾を斜めに伸ばし、背面の柄パネル・襟の曲線・ボタン縁を追加 |
| 白タオル | 腕の上を連続して折り返す別メッシュ。2枚に見える垂れ、厚み、角丸の縁、裾の短い縫い目、布地法線を追加 |

`Butler outfit - one piece` はマテリアルごとの重なりを残した**1メッシュ**です。
物理的に全頂点が接続した防水メッシュや、布シミュレーション用の縫合済みトポロジーではありません。
`White service towel - separate` は衣装へ結合していません。
本体・毛・衣装・タオル・ヘッドセット・左右の目・口の8メッシュに整理しています。

## 確認と限界

- 書き出したGLBを再読み込みし、8メッシュ・衣装1点・独立タオル1点・外部URIなしを検証。
- `avatar-verification.json` に実際のサイズ、三角形数、部品数、SHA-256を記録。
- `room-verification.json` で中央の予約動線へ家具が入らないことを再確認。
- `manifest.json` とZIPのCRCで、全納品ファイルの破損とチェックサムを確認。
- `preview/` は実GLBのオフラインレンダー。同じカメラ・照明のv12対v13正面比較、三面図、パーツ詳細、新キャラ入りの部屋全景を含みます。

**残る点:** 参照画像の高密度な長い毛、繊維単位の布、細かな縫製や完全一致までは再現していません。
特に腕と胴のつながり、服の重なり・ドレープは手作業スカルプトではなくプロトタイプ形状です。
リグ・アニメーション・歩行・物理布・当たり判定は未実装です。
Museへの反映と、iPhone実機での表示・読込時間・FPSは未確認です。
照明と影はGLBへ焼き込んでいないため、実環境では見え方が変わります。

## 再制作

このディレクトリで、Python 3.11とBlender 4.5 LTSのPythonモジュールを使用します。

```sh
python3.11 -m pip install -r requirements-build.txt
python3.11 build_room.py
python3.11 render_review.py
python3.11 package_delivery.py
python3.11 build_avatar.py
python3.11 render_avatar.py
python3.11 render_avatar.py --original --view front
python3.11 render_review.py --refined-avatar --view wide-room
python3.11 compose_previews.py
python3.11 package_refined.py
```

確認だけなら `python3.11 render_avatar.py --check-only` と
`python3.11 render_review.py --refined-avatar --check-only`。
入力は一つ上の元ZIPです。元v12のSHA-256を固定値と照合してから改修します。
配布ZIPの `source/` からも、元ZIPをその一つ上へ置いて同じ手順で再制作できます。
最初にWide版も再パッケージし、v13同梱ルームとのバイト一致を確認します。
乱数は固定していますが、GLBのバイナリ同一性ではなく形状・部品・サイズ・SHAの再検証を基準とします。
