# Soul v0.3 — 独立したA/B描画実験

正式v0.2は変更していません。これは採用判断のための研究用プロトタイプであり、映画的な品質の最終合格・正式採用を宣言するものではありません。

- [比較結果・実測・残課題](RESULTS.md)
- [PC／iPhone相当の画像と6秒動画](../../docs/previews/v0.3/README.md)
- [実装前に確認した研究計画](RESEARCH_PLAN.md)
- 基準コミット: `bdd2225403bd9ba3d582a35bd82809f978caa0e7`
- 実行・計測: Human承認済みのWindowsローカル。Codex Cloudではありません。

## 起動

このディレクトリでNode.jsを使います。検証時はNode.js 22.18.0でした。

```powershell
node scripts/serve.mjs
```

ブラウザで `http://127.0.0.1:8034/experiments/v0.3/` を開きます。サーバーは127.0.0.1にのみバインドし、ソースの取り違えを避けるためキャッシュを無効にします。ポート変更は環境変数 `SOUL_PORT`。終了はCtrl+Cです。正式UIは同じサーバーの `/index.html` から確認できます。

実行時のインストールや外部CDNは不要です。Three.jsの必要な2モジュールとMITライセンスを `vendor/` に同梱しています。`file://` ではなくHTTP経由で開いてください。

依存を再生成する場合のみ:

```powershell
npm ci --ignore-scripts
npm run vendor
npm test
```

`node_modules`、ログ、作業キャプチャはコミット対象外です。既存UIのCSSと描画コードを相対参照するため、この実験フォルダだけを切り離さずSoulプロジェクトの構造を維持してください。

## A / B

**A: Canvas 2D + clear**

正式v0.2の `js/soul-renderer.js` の `draw2d` をそのまま呼び出し、直前に透明な `clearRect` を1回追加します。元の描画内容、グラデーション、粒子・曲線・シードは変更しません。コンストラクターの旧ループは起動せず、実験用アダプターで計測・停止・リサイズを管理します。元の状態表現の限界も残してあり、Listening以外の描画は同一です。

`accumulation.html` は、同一時計で「消去なし」と「消去あり」を描画し、初回・5秒・15秒の画像と全Canvasのアルファ値を取得します。

**B: Three.js r180 / WebGL2**

独自GLSLの非対称な3D流れ場を、柔らかい粒子・開いた細い光の筋・低密度の光の膜・内部の短い流線で共有します。中心を埋める球メッシュはありません。属性を生成時に固定し、時間／状態／入力レベルをuniformで更新します。

- `THREE.Points`: 円形の指数減衰、奥行き別の大きさ・輝度・色。
- フィラメント: まとめたリボンメッシュ。柔らかい断面、途切れた輝度、異なる高さ・奥行き。
- 加算合成、透明マテリアル、深度書き込みなし。通常3 draw calls。
- RGBA16Fが使えなければRGBA8。これは体積レイマーチングや物理的な散乱シミュレーションではありません。
- Bloomは標準OFF。ON時は幅・高さ各1/4の分離ぼかし2パスを追加し、合計5 draw calls。Ecoでは無効。
- WebGLが使えない／コンテキスト喪失時は、別の新しいCanvasを作ってAへ切替。

## 操作と状態API

上部で方式／品質／Bloom／静止画／一時停止を切替できます。`Still · t=8s` は同じシード・同じ時刻で比較する静止画モードです。`Measure 10s` は2秒ウォームアップ後、実際に描画したフレーム間隔を10秒間収集します。タブが非表示になると計測を中止します。

入力部品以外にフォーカスがあるとき、1–5キーで状態切替、Spaceで停止／再開。状態ボタンにはテキストと `aria-pressed` があり、色だけに依存しません。OSの `prefers-reduced-motion` または検証用Reduce motionではイベント時のみ静止画を描きます。OS設定そのものは変更しません。

```javascript
renderer.setInput({ state: 'listening', audioLevel: 0.35 });
renderer.setQuality('Balanced');
renderer.setBloom(false); // Bのみ。Ecoでは常にfalse
renderer.resize(cssWidth, cssHeight);
renderer.render(timeSeconds, deltaSeconds, { still: false });
renderer.dispose();
```

| 状態 | Bの表現 |
| --- | --- |
| Ready | 遅い呼吸、循環、微小な姿勢変化 |
| Listening | 外側が広がる。模擬入力レベルが外層に反映 |
| Processing | 内側へ収束し、循環が少し速くなる |
| Speaking | 不均一な明滅と、流線に沿って移動する膨張 |
| Attention | 細く引き締まり、速度が大きく落ちる |

`idle`→`ready`、`error`→`attention` の互換名を受け付けます。入力レベルは0–1へ制限します。状態は約0.4秒の時定数で補間します。AI、マイク、STT、TTSは未接続。サイドバー等は明示した見た目だけのプレースホルダーです。

## 品質予算

| B設定 | 粒子 | 主フィラメント | セグメント/本 | DPR上限 | 最大画素 | 目標fps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Eco | 600 | 7 | 112 | 0.75 | 300,000 | 24 |
| Balanced | 1,200 | 12 | 192 | 1.0 | 600,000 | 30 |
| High | 1,800 | 16 | 224 | 1.35 | 1,000,000 | 60 |

全設定に低密度の膜5本＋内部流線4本を追加。画素上限はSoulの描画バッファに適用し、UI文字の解像度は下げません。実際のDPRが上限より小さければそれを使用します。上表は予算であり、性能の保証ではありません。

AはEco/Balanced/Highで80/150/230粒子、6/10/14曲線、CSS寸法に対する描画倍率0.42/0.58/0.76です。

## 動画と計測の注意

`Record 6s` はSoul部分のみをMP4（利用できなければWebM）で録画します。MP4はアルファを持たないため、描画直後に別の不透明な2D Canvasへ合成してから記録します。録画は計測と同時に行わないでください。GPU時間は非同期タイマークエリーで測り、GPU使用率とは区別します。CanvasのGPU時間・CPU/GPU使用率は未計測です。

`measurements.json` が最終計測、`measurements-exploratory.json` は初期の参考記録です。両者を混ぜて平均しません。後者には原因未確定の長いフレームも残しています。

## ライセンス

[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) と同梱の [Three.js MIT LICENSE](vendor/THREE-LICENSE.txt) を参照。参考作品のコード・アセットはコピーしていません。
