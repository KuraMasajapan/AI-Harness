# むーさん3D — 最新成果物

服なしモデル、着せ替え用の執事服、素材と造形を詰めた部屋をまとめています。
GLBの直接ダウンロード用は [`latest/models/`](latest/models/)、確認画像は [`latest/previews/`](latest/previews/) にあります。

| 成果物 | GLB | ZIP・再制作コード |
| --- | --- | --- |
| 服なしモデル（クリーム色・肌色調整済み） | [musan-bare-shape.glb](latest/models/musan-bare-shape.glb) | [ZIP](bare-shape/Musan_Bare_Shape_2026-11-28.zip) / [詳細](bare-shape/README.md) |
| 執事服一式（フィット・丈・素材の調整版） | [musan-butler-outfit.glb](latest/models/musan-butler-outfit.glb) | [ZIP](butler-outfit/Musan_Butler_Outfit_Refined_2026-11-28.zip) / [詳細](butler-outfit/README.md) |
| 書斎・台所の部屋（窓の夕景を含む） | [kitchen-study.glb](latest/models/kitchen-study.glb) | [ZIP](kitchen-study-refined/Musan_Kitchen_Study_Refined_2026-11-28.zip) / [詳細](kitchen-study-refined/README.md) |
| 元の軽量執事むーさん v12（変更なし） | [musan-butler-detail-v12.glb](latest/models/musan-butler-detail-v12.glb) | 元のSummary ZIPと同じバイト列 |

## 組み合わせ

- 既存の部屋表示を維持する場合: 部屋と元のv12を使います。[scene-placement.json](latest/scene-placement.json) の配置・縮尺を参照してください。
- 着せ替える場合: 服なしモデルと執事服を同じ親・同じ変換で重ねます。[wardrobe.json](latest/wardrobe.json) を参照してください。
- 執事服は `ButlerOutfit` という単一メッシュで、一式単位で表示切替できます。素体とタオルは含みません。

部屋の横長配置・中央動線・既存4灯は維持しています。窓の外はCC0写真から作った静止背景で、外景の3D化・視差はありません。
服なしモデルと服は静止姿勢用です。歩行リグと変形追従は未実装、Muse・iPhoneでの表示・速度は未確認です。
GitHubへの保存だけでは既存スペースは差し替わりません。

各ZIPは送付済み成果物の原本として保持しています。ZIP内READMEのGitHub保存状況は制作当時の記録です。
旧版の服ZIP・元のSummary ZIP・以前の部屋は履歴・比較用で、最新版は上の表を使用してください。
[`latest/manifest.json`](latest/manifest.json) に配布ファイルのSHA-256と、モデルが納品ZIPと一致することの検証結果があります。
