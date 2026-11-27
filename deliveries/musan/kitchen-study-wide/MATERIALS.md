# kitchen-study 素材感改修版

今回の推奨ファイルは `Musan_Kitchen_Study_Materials_2026-11-27.zip` です。
部屋だけを改修しました。**むーさんは元の軽量v12のまま**です。
却下されたv13キャラ改修はPRから追加コミットで取り消しており、このZIPには含みません。
元のSummary ZIPと最初のWide ZIPは変更していません。

## 取り込み

1. ZIP内の `models/kitchen-study.glb` で部屋だけを置き換えます。
2. `models/musan-butler-detail-v12.glb` は元ZIPとSHA-256一致。既存v12の差し替えは不要です。
3. `muse/scene-placement.json` は最初の横長版と同じ位置・倍率です。
4. PBRのbase color、roughness、metallic、normal mapを有効にします。
   ノーマル画像とmetallic/roughness画像は非カラー、base colorはsRGBです。
   金属には環境光の反射が必要です。白い環境光一灯だけでは素材が平坦に見えます。
5. 部屋GLBには `KHR_lights_punctual` で**4灯**を同梱しています。
   電球列を左右2灯で近似し、卓上灯1灯と丸窓からの夕日1灯を追加しています。
   対応ビューアなら同梱照明を使用し、非対応なら `muse/lighting-evening.json` の
   Y-up位置・色・GLBと同じcandela値で作ります。**両方を重ねて二重点灯しないでください。**
6. 影は夕日の1灯だけを推奨し、遅い端末では全部切ります。影の有無はglTF標準に
   含まれないため、ノードの `runtime_cast_shadow` と照明JSONで別途渡しています。
   暗めの暖色環境光と金属用の弱い環境反射を残してください。
   レビューはAgX・露出+0.45EVと補助面光源を使っています。面光源はglTF標準対象外で、
   GLBに照明・影を焼き込んだものでもないため、Museで同じ見え方とは未確認です。

## 素材と形状

- **木材:** 壁、床、ハニーオーク、濃い家具で色を分離。導管・不規則な繊維・節と、
  木目に対応したroughness/normalを用意。UVで木目方向と密度を設定しています。
- **床:** 元の引き伸ばした横板を、奥へ走る千鳥継ぎの板へ変更。
  横幅8.4・奥行き4.6と床面高さ、中央動線の予約は維持しています。
- **布:** アイボリー・プラム・セージで染色を分離。織りと繊維のばらつきを
  base color/roughness/normalへ入れ、光沢のある木材と反応を分けています。
  ベッド足元のスローには別の太い編み目を設定しています。
- **寝具:** 直方体の掛け布団を、側面の垂れ・裾・折り皺のある薄い布面へ置換。
  枕とクッションも膨らみのある形に変更しています。キャラ側には変更していません。
- **石・金属:** 石天板は微細な粒と粗さ。ステンレスと真鍮はmetallic値を分け、
  共通の微細なブラッシュ面を設定しています。
- **塗装・器:** アイボリー塗装、エナメル、釉薬陶器、素焼き、紙、窓面を
  個別の色・反射粗さへ分離。丸窓は薄い透明反射面と、奥の夕景面を分離しました。
  夕景は生成した簡素な背景画像で、屋外の3D空間・写真・屈折ガラスではありません。

画像はこのスクリプトで生成したオリジナルのタイルテクスチャです。
完成イメージを板に貼ったものではなく、部屋全体は実際の3D形状です。
外部生成API・画像アップロード・有料素材・追加課金は使っていません。

## 軽量化・確認

木材は最大1024px、布・石・金属は512px。繰り返しUVと画像共有を利用し、
視差マッピング、実行時の手続きノイズ、布シミュレーションは不要です。
静止形状は素材・配置区画ごとにまとめ、細い床板や本が一つずつ描画されるのを避けています。
照明は電球ごとの14灯ではなく4灯にまとめています。影の実行時設定はホスト側で行います。
正確な容量・三角形数・画像展開後のRGBA概算容量は `verification-materials.json` に記録します。
これはGLB内の画像だけの概算であり、GPU全体のメモリ消費量ではありません。

GLB再取り込み、中央動線、v12のSHA-256、埋め込み画像の解像度、
metallic/roughnessの実際の画像チャンネル、全manifestハッシュとZIP CRCを検証しています。
比較画像は同じカメラ・同じ照明です。画像の変化には床・寝具の形状変更も含みます。
`lighting-comparison.png` だけは同じGLBを異なる照明で比較しています。

**未確認:** Museへの反映、iPhoneでの表示・読み込み・FPS・GPUメモリ。
小型画像と静止形状に抑えていますが、実機で軽いと確認したものではありません。
リグ、アニメーション、当たり判定、navmeshはありません。

## 再制作

元Summary ZIPを一つ上のディレクトリに置き、スクリプトのある場所で実行します。

```sh
python3.11 -m pip install -r requirements-build.txt
python3.11 build_room.py
python3.11 texture_room.py
python3.11 render_review.py --view interior
python3.11 render_review.py --materials
python3.11 render_review.py --materials --view interior --neutral-lighting
python3.11 verify_materials.py
python3.11 compose_materials.py
python3.11 package_materials.py
```

ZIPの `source/` にも同じスクリプトと配置JSONを同梱しています。
生成画像は `textures/` にも収録し、GLB内にもすべて埋め込んでいます。
