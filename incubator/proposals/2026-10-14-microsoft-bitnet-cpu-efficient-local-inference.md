---
status: proposal
created: 2026-10-14
origin: Human-provided X screenshot and https://github.com/microsoft/BitNet
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A++
stage_2_rank: A+
evidence_status: CONFIRMED (official repository and documentation) / UNVERIFIED (independent performance reproduction, project fit)
tags:
  - local-ai
  - bitnet
  - cpu-inference
  - ternary-llm
  - embedding
  - speech-recognition
  - energy-efficiency
  - candidate
trigger_topics:
  - BitNet
  - bitnet.cpp
  - 1.58bit
  - 1-bit LLM
  - CPU-only LLM
  - 100B CPU
  - BitNet embedding 270M
  - PLaMo comparison
  - VibeASR
---

# Microsoft BitNet / bitnet.cpp — 省メモリCPU推論の検証候補

## Human decision (2026-10-14)

- **研究知識・将来の検証候補としてGitHubへ保存することをHuman承認済み。**
- 採用・インストール・ベンチマーク実行・モデルダウンロード・Core/Workflow/既存Project変更は**未承認・未実施**。
- Decision: **CANDIDATE** / Implementation: **HOLD**。
- 最初から100Bモデルや新たな常駐基盤を導入しない。実機と用途が定まった時点で、最小・可逆の比較試験を検討する。

## 原典と日付

- Microsoft公式GitHub: https://github.com/microsoft/BitNet
- 推論基盤・100Bに関する技術報告: https://arxiv.org/abs/2410.16144 （2024年）
- 公式BitNet-b1.58-2B-4T: https://huggingface.co/microsoft/BitNet-b1.58-2B-4T （公式READMEで2025-04-14公開と説明）
- 公式BitNet Embedding 270M: https://huggingface.co/microsoft/BitNet-embedding-270M （公式READMEで2026-07-20公開と説明）
- Embedding用I2_S実装・測定手順: https://github.com/microsoft/BitNet/blob/main/docs/bitnet-embeddings-i2s-guide.md
- 関連音声認識OSS（別リポジトリ）: https://github.com/microsoft/VibeASR.cpp （公式READMEで2026-07-23紹介）

**新規リリースの報告ではない。** 今回の発見はHuman提供のXスクリーンショットを入口とした既存OSSの再評価である。投稿の原URL・投稿日時は未取得。

## 1. 主張の分解と証拠の境界

### 公式資料から確認できたこと（CONFIRMED: 公式側の記載）

- `bitnet.cpp` はMicrosoftによる1.58-bit（三値重み {-1,0,+1}）系LLM向け推論フレームワーク。CPU最適化実装があり、GPUカーネルも公開されている。フレームワークはMITライセンス表記。
- 公式READMEの報告値では、比較対象・測定環境を限定したx86 CPUで最大6.17倍の高速化、最大82.2%のエネルギー削減、ARMで最大5.07倍・最大70%削減。
- 100Bパラメータを単一CPUで5〜7 tokens/sという主張は公式READMEにある。ただし技術報告の研究用・合成モデルでのスケーリング測定を、学習済み100B会話モデルの一般家庭PC上での実用性と同一視しない。CPUだけで動くことは、少RAMで高速・高品質な日本語会話が成立することを保証しない。
- 会話生成向け公式モデル `BitNet-b1.58-2B-4T`（約2.4Bパラメータ）が実際に公開されている。ただし日本語の実運用適性は未検証。
- 検索・類似度計算向け `BitNet-embedding-270M` と `BitNet-embedding-0.6B` が公開されている。公式I2_Sガイドでは多言語対応、x86 CPU最適化、実測ベンチマークが説明されている。**日本語のHarness文書検索品質は別途測定が必要**。
- Microsoftは関連プロジェクトとして、CPU上で動く音声認識 `VibeASR.cpp` も紹介している。BitNetの会話LLMやEmbeddingと同じ役割ではない。

### 採用判断に使ってはいけない解釈（UNVERIFIED / MISLEADING）

- 「普通のCPU一つで、学習済み100Bモデルが誰でも快適に使える」との一般化。
- 「すべての既存LLMを後から1.58bitに変換すれば同様の速度と精度になる」との一般化。BitNet向けに学習されたモデル・対応カーネルが重要。
- 「スターやforkが多いので実ユーザー数・本番運用実績が多い」とする推定。fork数は利用実態の証明ではない。
- 公表ベンチマークを、現有CPU・RAM・日本語入力・実際のHarness検索負荷に対する性能保証とすること。
- 公式資料で確認できた事実と、独立して実機で再現できた性能を混同しない。

## 2. 技術的な特徴と使いどころ

- 三値重みの低ビット表現と専用の高速推論カーネルによって、CPU推論の計算量・メモリ帯域・消費電力を抑える構想。
- **優先検討: BitNet Embedding 270M**。大量のMarkdownを対象とした類似文書検索、過去の失敗・判断の再発見、Incubator提案の類似候補探索、ローカルRAGの入口として有望。
- **補助検討: BitNet Embedding 0.6B**。270Mより精度改善が期待できるか、必要RAM/CPU負荷と対比する。
- **参考比較: BitNet-b1.58-2B-4T**。小型日本語生成モデルとの会話品質・応答速度比較対象になり得るが、日本語適合性・特定用途の精度が未確認。
- **別候補: VibeASR.cpp**。将来のSTT用途として参照するに留め、BitNet導入と抱き合わせない。

## 3. 既存AI-Harness候補との比較

基準: `development` の `agents/Local-AI/README.md`（2026-10-14時点）。

| 既存の候補 | 今回の関係 | 判断 |
| --- | --- | --- |
| `agents/Local-AI/PLaMo-Embedding-1B.md` | 日本語検索・重複検出の同用途で比較できる | 270Mとの検索精度・速度・RAM比較が最優先 |
| `agents/Local-AI/TinySwallow-1.5B-Instruct.md` | 日本語生成LLMの比較対象 | BitNet 2Bの日本語性能が確認できる場合のみ限定比較 |
| `agents/Local-AI/sokudan-ja-310m.md` | 型付き判定・分類が主用途 | 用途違い。代替とみなさず、原則維持 |
| `incubator/proposals/2026-10-14-tacit-domain-knowledge-history-mining.md` | 過去履歴から暗黙知を発掘する研究 | 文書検索を助ける可能性はあるが、推論・知識抽出の検証を代替しない |

**位置づけ**: 新しいMemory基盤や独立した常駐Agentの採用案ではなく、既存Local-AIカタログに対する**CPU効率のよい推論・Embeddingモデルの比較研究**。今回は候補の保存だけとし、既存カタログに新たな「採用済みモデル」を追加しない。

## 4. 期待効果・費用・限界・安全性

- GPUなしのPCでも特定用途を処理し、クラウド呼出しと継続費用を減らせる可能性。
- モデルはローカル処理可能だが、セットアップ・変換・推論基盤の保守が必要。実機性能、メモリ使用量、電力、待ち時間、品質を比較する。
- 1.58-bitは全処理・全ファイルのビット数が常に1.58である意味ではない。I2_Sの実体やEmbedding表を含むRAMの実使用量を計測する。
- 日本語検索の適合、長文処理、モデルごとのライセンス、依存関係・配布物の安全性は採用前に確認する。
- 保存対象を公開リポジトリに置けない個人・家庭データまで広げない。ローカル処理と公開GitHubへの記録は分離する。

## 5. 将来の最小検証（NOT STARTED）

1. 実際に利用するCPU・RAM・OSと、比較対象となる日本語Markdown文書群を確定。
2. `BitNet Embedding 270M` と既存候補 `PLaMo-Embedding-1B` を同じ入力・検索正解セットで比較（必要に応じて0.6Bも）。
3. Top-k検索の有効性、類似提案の見逃し、誤一致、日本語固有表現、索引速度、検索速度、最大RAM、導入コストを実測。
4. 既存の文字列検索・単純な検索方法にも勝つか確かめる。高性能なAIを無条件に採用しない。
5. 優位性が再現でき、保守負荷に見合う場合のみ採用提案としてHumanへ戻す。Core/Memory/既存Projectへの反映は別途承認。

## 6. 評価・次のアクション

- **Stage 1: A++**（GPU不要のローカルAI基盤への関連性が高く一次資料調査価値が大きい）
- **Stage 2: A+**（公式公開モデルとCPU効率への実証資料はあるが、100Bの実用性・日本語特化の精度・既存候補との優劣は未検証）
- **Evidence**: プロジェクト・公開モデル・著者による測定値はCONFIRMED (official-source claims)。独立再現・AI-Harness上の効果はUNVERIFIED。
- **Decision**: CANDIDATE / Implementation HOLD。
- **Trigger to revisit**: ローカルAI機材の選定、Embedding比較、日本語RAG、Markdown大量検索、過去履歴の類似事例照合、GPUレスSTT、AI-Harness vNextのメモリ検索構造監査。
- **Next action now**: なし。知識・検証案の保存のみ。
