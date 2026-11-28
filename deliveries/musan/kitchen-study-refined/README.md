# Kitchen-study — material and furniture refinement

## 差し替えるもの

`models/kitchen-study.glb` は部屋だけです。既存の部屋GLBと置き換えてください。
むーさん本体・服なしモデル・着せ替え服は変更していません。本ZIPにキャラクターは含めません。
表示に使うのは引き続き元の `musan-butler-detail-v12.glb` です。

元v12のSHA-256:
`a656295b226adb614281acfc2e6f61faeba9f1b66abe28dd6b9cdbd4dd11b84d`

横長の部屋、壁際の家具配置、中央の空き領域、既存4灯の夕方照明は保持しました。
`muse/scene-placement.json` の配置・縮尺を使い、キャラクターの参照は既存のv12に向けてください。
中央の空き領域は配置上の予約であり、歩行用navmeshや衝突判定ではありません。

## 今回の変更

- **本棚:** 27冊それぞれに独立した表紙・紙の束・丸い背表紙を作り、布装丁、箔色のタイトル、紙の小口を追加しました。
- **家具:** 木の写真素材をUV方向に合わせ、木目のスケール・艶・凹凸を控えめに調整。デスクは丸い縁、細く絞った脚、引き出しと真鍮の取っ手に変更しました。
- **布:** リネンの写真由来の織りと粗さを使い、ランプシェードは薄い中空形状に、椅子と枕には縫い目や縁取りを追加しました。
- **キッチン:** 枠組み式の扉、石の天板、実際に穴が開いた深いシンク、曲線の水栓、オーブンガラス、4口コンロ、釉薬の鍋、タイルを作り直しました。
- **窓の外:** 丸窓のイラストと台所窓の暗い板を、同じ夕景パノラマから切り出した写真に変更。湖・遠景の稜線・夕日のある風景にしています。

金属・釉薬・塗装の艶と、木・布・紙の粗さを分けています。
元の小物と床・部屋構造は再利用しており、写真そのものの完全再現や全面的な高密度モデル化ではありません。

## 容量と検証

| 項目 | 値 |
| --- | --- |
| 部屋GLB | 約7.4 MB |
| 部屋のみの三角形 | 98,429 |
| 材質 | 34 |
| メッシュ / 描画プリミティブ | 48 / 48 |
| テクスチャ最大辺 | 1,024 px |
| 展開したRGBA画像の合計 | 48 MiB |
| mipmapを加えた画像のみの概算 | 約64 MiB |

画像はGLBに内包し、外部ファイルを参照しません。同じ木・布のnormalとroughness画像を共有しています。
上記の画像メモリはピクセル数からの概算で、GPU実測値やキャラクター込みの総メモリではありません。

実GLBの再取り込み、中央床への家具のはみ出しなし、元v12のバイト一致、材質と画像の内包、4灯の一致を確認しました。
シンク中心へ実メッシュにレイを当て、天板ではなく底へ届くことも確認しました。
詳細は `verification-refined.json`、ZIP内のファイル一覧とSHA-256は `manifest.json` にあります。

**Museへの反映、iPhoneでの表示・FPS・GPUメモリは未確認です。**
画像は納品GLBを再取り込んだオフラインのCyclesレンダーで、Museのスクリーンショットではありません。
レンダーには既存の面光源フィルも使っています。取り込み先の環境光・反射・トーンマッピングで見え方は変わります。
4灯はGLBの `KHR_lights_punctual` に含みます。`muse/lighting-evening.json` から別途作る場合、重複配置しないでください。

窓の風景は共有の1,024×512画像による静止背景です。外の地形を3Dで追加したものではなく、視点を動かしたときの外景の視差はありません。

## 写真素材とライセンス

Poly Havenの公開APIから選んだCC0素材です。元画像の色調・コントラスト・粗さを部屋用に調整しています。
石材は目地を避けて単一スラブとして切り出しています。本の装丁と紙の画像は独自生成です。

| 元素材 | 使用先 |
| --- | --- |
| [Dark Wood](https://polyhaven.com/a/dark_wood) | 壁・床・家具の木目 |
| [Fine Grained Wood](https://polyhaven.com/a/fine_grained_wood) | まな板 |
| [Rough Linen](https://polyhaven.com/a/rough_linen) | 布・ランプシェード |
| [Marble 01](https://polyhaven.com/a/marble_01) | 明るい石の天板 |
| [Qwantani Sunset](https://polyhaven.com/a/qwantani_sunset) | 丸窓・台所窓の外景 |

ライセンス: https://polyhaven.com/license

元画像、APIの取得URLとSHA-256は `source/kitchen-study-refined/work/sources/` と
`source/kitchen-study-refined/work/material-sources.json` に保存しています。

## 再制作

Python 3.11と `source/kitchen-study-wide/requirements-build.txt` の依存を使います。
`source/` は元の2ディレクトリの相対関係を維持しています。

1. 既存の元v12を `source/kitchen-study-wide/work/musan-butler-detail-v12.glb` に置きます。
2. `source/kitchen-study-refined/` で `python build_refined.py` を実行します。
3. `python verify.py` で実GLBの材質・画像・中央動線・シンクを検査します。
4. `python review.py` で全景と寄りのレンダーを作れます。

元の無加工部屋GLBは `source/kitchen-study-wide/work/kitchen-study.glb` に含めています。
元画像があれば再ダウンロード不要です。欠けている場合のみ `python fetch_materials.py` を使います。
比較・再梱包は元のリポジトリ上で実行する制作補助で、以前のレンダーと元ZIPも参照します。

GitHubへの保存と、Muse等への取り込み・表示確認は別作業です。
この成果物を保存しただけでは、既存スペースは更新されません。
