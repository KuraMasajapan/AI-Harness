# ジャービスUIデザインサンプル
_JARVIS / Soul UI — VFX Design Reference Collection_

- 作成日: 2026-10-21
- 保存先: `KuraMasajapan/AI-Harness` → `development/projects/JARVIS_Soul_UI/docs/`
- 用途: 子どもが製作しているローカルAIのJARVIS風Soul UIに向けた**映像表現・描画技術の参考資料**
- 方針: **方向性は変えない。質感・表現力を向上**する。外部作品をそのまま複製せず、透明感、柔らかい発光、粒子の密度、流動性、負荷管理を学ぶ。
- 収録範囲: 既出の2件＋追加の4件（**6サイト／主要7デモ以上**）。Hologram Particles VFX — Cortiz は今回**除外**。
- 状態: 参考資料として保存。各サイトの全動作・全環境での性能を検証済みという意味ではない。ライセンスは利用前に都度再確認する。

## すぐに見られるリンク一覧

| # | 作品・サイト | デモ・ギャラリー | ソース | Soul UIへの参考点 |
|---|---|---|---|---|
| 01 | **Born of Data / Techartist (VoXelo)** | [動くデモ](https://codepen.io/VoXelo/full/VYexvqY) | [CodePen編集画面](https://codepen.io/VoXelo/pen/VYexvqY) | 柔らかい粒子、加算合成、光の密度、映画的な仕上げ |
| 02 | **Jarvis AI Orb / cyber1443** | [ライブデモ](https://cyber1443.github.io/jarvis-ai-orb-web-animation/) | [GitHub](https://github.com/cyber1443/jarvis-ai-orb-web-animation) | 思考・待機などの状態変化、軽量化、停止制御 |
| 03 | **Dreamy Particles / Dominik Fojcik — Codrops** | [ライブデモと複数Variation](https://tympanus.net/Tutorials/DreamyParticles/) | [GitHub](https://github.com/DGFX/codrops-dreamy-particles) | GPGPU粒子、柔らかい輝き、有機的な集合／解散 |
| 04a | **React Bits — Orb** | [Orbデモ](https://reactbits.dev/backgrounds/orb) | [React Bits GitHub](https://github.com/DavidHDev/react-bits) | 呼吸する発光リング、光の流れ、インタラクション |
| 04b | **React Bits — Liquid Ether** | [Liquid Etherデモ](https://reactbits.dev/backgrounds/liquid-ether) | [React Bits GitHub](https://github.com/DavidHDev/react-bits) | 光の膜、液体状の流れ、有機的な揺らぎ |
| 05 | **WebGL Shader Lab / PSCactux** | [14種類のVFXギャラリー](https://pscactux.github.io/webgl-shader-lab/) | [GitHub](https://github.com/PSCactux/webgl-shader-lab) | Curl Swarm、Aurora、Portal、Constellation等の描画技術の比較 |
| 06 | **Morphing Particle Swarm / wonjyou** | [GitHub内のデモ説明・コード](https://github.com/wonjyou/morphing-particle-swarm) | [GitHub](https://github.com/wonjyou/morphing-particle-swarm) | 1,000〜40,000粒子の密度比較、形状モーフィング |

> **特に見ておきたい多バリエーションのサイト**:  
> [WebGL Shader Lab](https://pscactux.github.io/webgl-shader-lab/) は**14種類**の個別VFXを比較できる。  
> [React Bitsの背景ギャラリー](https://reactbits.dev/c/backgrounds) はOrb・Liquid Ether以外にも多数の効果を一覧できる。  
> [Dreamy Particles](https://tympanus.net/Tutorials/DreamyParticles/) には **Leader / Venecia / Samurai / Cyborg** など形状のVariation切替がある。

---

## 01 — Born of Data

- 作者: Techartist（CodePen: VoXelo）
- 主な構成: Three.jsによる多層粒子、柔らかな発光粒子、動く形態、加算合成、ポストプロセス。
- 観察ポイント: **粒子が個別の点に見えず、全体で光の場に見える理由**。中心／外周の密度差、粒子のサイズ差、トレイル、Bloomと色階調のバランス。
- 留意事項: 作品全体の粒子数や負荷をそのまま模倣しない。CodePen上のコードの再利用許諾条件は本資料作成時点で未確定のため、**参考・研究のみ**とする。

## 02 — Jarvis AI Orb

- 作者: cyber1443
- 主な構成: React + Three.js。 `idle` / `thinking` / `success` / `alert` 等の状態遷移、色・品質プリセット。
- 観察ポイント: **状態変化を視覚へ接続する設計**、描画を画面外／非表示で止める工夫、自動品質調整と reduced-motion。
- Soul UIへの適用: 状態API・描画ループ・負荷管理の設計を参考にする。既存HTML UIをReactに置き換える必要はない。
- ライセンス: リポジトリに **MIT**。コードを利用する場合は条件・著作権表示を維持。

## 03 — Dreamy Particles

- 作者: Dominik Fojcik（Codrops）
- 主な構成: Three.js、GPGPU、シェーダーによる粒子表現。
- 観察ポイント: **雲のような粒子密度、緩やかな集合／離散、輪郭の柔らかさ**。
- デモのポイント: 複数のマスク／形状に切り替えられる。形状そのものより粒子の集まり方、光の見え方を観察する。
- 留意事項: 配布リポジトリの明示的なLICENSEを今回確認できていない。デモに使われた3Dモデル等の権利も個別に注意。**第三者コードやアセットの移植は許諾条件を確認するまで行わない。**

## 04 — React Bits（Orb / Liquid Ether）

- 運営: DavidHDev / React Bits
- [背景VFXの一覧（Orb・Liquid Ether以外も掲載）](https://reactbits.dev/c/backgrounds)
- **Orb**: 発光する渦・リング、呼吸感、滑らかな色の流れ。
- **Liquid Ether**: 流体のように連続する光の流れ。粒子表現に重ねる「光の膜」「空気感」の着想。
- Soul UIへの適用: 実装の丸ごと移植より**表現設計の研究**を優先。React導入は前提としない。
- ライセンス: **MIT + Commons Clause**（単体コンポーネントの販売・再配布に制約）。`MITのみ` と取り違えないこと。[ライセンス原文](https://github.com/DavidHDev/react-bits/blob/main/LICENSE.md)。

## 05 — WebGL Shader Lab（14種類のVFX）

- 作者: PSCactux
- **特に注目**: [ギャラリー](https://pscactux.github.io/webgl-shader-lab/)から効果を個別に開き、動きや操作を比較できる。
- 全14種類: **Liquid Metal / Curl Swarm / Particle Morph / Wireframe Terrain / Glass / Tunnel / Portal / Topographic Contours / Aurora Gradient / VHS Tape / Warp Speed / Wave Field / Gear Train / Constellation**。
- Soul UIへの有望候補:
  - **Curl Swarm**: curl-noiseを用いた有機的な粒子の流れ。元作品は高密度だが、流れ場の考え方を研究する。
  - **Aurora Gradient**: 柔らかく連続する色・光の層。
  - **Portal**: 立体的な渦と流入・流出の表現。
  - **Constellation**: 粒子間の関係を感じさせる穏やかな動き。
  - **Wave Field**: 流れと局所的な変化の設計。
- 構成: Three.js / React Three Fiber / WebGL2。すべてのデモが軽量という意味ではない。
- ライセンス: **MIT**。使用部分の依存関係・表示条件も確認する。

## 06 — Morphing Particle Swarm

- 作者: wonjyou
- 主な構成: Three.js、WebGL、ソフトな粒子、形状間モーフィング。
- 形状: Sphere / Cube / Pyramid / Donut。
- 特に有用: 粒子数を**1,000〜40,000個**の範囲で変更できるため、**多い状態から減らす粒子密度の比較実験**に向く。
- Soul UIへの適用: 実装をコピーするより、形状モーフィング・粒子密度比較・段階的な間引き方を参考にする。
- ライセンス: リポジトリ直下に明示的なLICENSEを今回確認できていない。**利用許諾を確認するまで参考のみにとどめる。**

---

## Soul UIへの適用ルール

1. **優先するのは質感**: 透明感、輝度差、前後の重なり、柔らかな粒子、連続的な光の流れ。
2. **光るワイヤーを主役にしない**: 粒子の密度分布で大きな光の構造を作り、フィラメントは補助にする。
3. **粒子数は上限から間引いて探す**: 高密度の見た目を先に確認し、同一条件で段階的に減らして「見た目の改善が頭打ちになる帯域」を検証する。粒子数だけで画質を評価しない。
4. **GPU使用を許可**: Three.js / WebGL2 / GLSLで良い。内蔵GPUも対象とし、Eco / Balanced / Highを実測で調整する。
5. **Bloomは手段**: OFFと弱いONを比較し、強い白飛びで質感を誤魔化さない。
6. **正式v0.2やv0.3実験を保護**: 外部作品を自動導入・上書きしない。採用前に小さい独立試作を作り、GitHub上の画像・短い動画で比較する。
7. **ライセンス・安全性**: 外部デモのコード／画像／3Dモデルを無断で同梱しない。ソース配布条件・使用ライブラリ・第三者アセットの権利を別途確認する。
8. **公開用と研究用を分ける**: X等では作者と原典に誘導する。画像・動画を再投稿する場合は別途利用条件を確認する。

## 今後の使い方

- CodexへSoul VFX改善を依頼する際、この資料を**デザイン参照カタログ**として提示する。
- 実装の採用優先順位ではなく、比較のための引き出し。固定の1作品を完全模倣する設計にはしない。
- リンク切れ・ライセンス変更・新発見は追記更新する。
- 自分たちのSoul UI本体は別途 `experiments/v0.3/` や正式UIで管理する。

---

**除外（今回の収録対象外）**: Hologram Particles VFX — Cortiz。