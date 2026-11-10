---
document_type: research_evaluation
date: 2026-11-11
evaluated_at: 2026-11-10
timezone: Asia/Tokyo
title: "Kaggle free GPU Notebooks and Benchmarks — Colab complement"
branch_target: development
stage_1_rank: A+
stage_2_rank: A+
decision: CANDIDATE
evidence: "OFFICIAL DOCUMENTATION CONFIRMED; USER ACCOUNT QUOTA AND RUNTIME UNTESTED"
implementation: HOLD / NOT_IMPLEMENTED
dedup: "NEW topic by filename review; broad full-text overlap unconfirmed"
tags: [kaggle, free-gpu, colab, model-evaluation, notebooks, privacy, trinity, research-only]
---

# Kaggle無料GPU / Benchmarks — 研究候補

## 判定
- **A+ / CANDIDATE**（2026-11-10の暫定評価を保存）。導入・認証・API利用・TRINITY変更は**HOLD**。
- Kaggleは2017年にGoogle Cloudが買収したAI/データサイエンスのサービス。2026年公開案内では登録ユーザー3,400万人超。Kaggle Inc.は独立した個人情報管理主体として登録されている。
- **評価の中心は「GPU計算資源の無料利用」**。無料GPT/ChatGPT/OpenAI API権利の提供と混同しない。

## 公式で確認できた要点
| 機能 | 公開条件と範囲 | 注意点 |
| --- | --- | --- |
| Kaggle Notebooks無料GPU | P100、T4×2などを提供。GPU利用枠は原則**週30時間**、需給により増減し得る | 実際のGPU配分と空きはアカウント/需給次第。利用可能な時間を常時保証するものではない |
| Notebook実行 | 公式Notebooks文書にGPU/CPUセッション**最大12時間**と記載 | 旧GPU Tipsには9時間の記載も残る。現実の上限は実画面で確認 |
| 登録条件 | GPUの有効化には電話番号認証が要求されるとKaggleスタッフが説明 | 電話番号提供は人間判断。代理で認証しない |
| Kaggle Benchmarks | 専用の**AI推論クォータ**でGemini、Claude、Qwen、DeepSeekなどを比較可能 | 一般Community Benchmarksは当時OpenAIモデル非対応。研究助成採択者は例外あり |
| 推論クォータ金額 | kaggle benchmarks quota で実アカウントの残量を表示できる | 公式CLIのドル額は**表示例**であり、全員への固定付与額ではない |

T4×2は2枚の独立GPUであり、プログラムが自動的に1枚の大容量GPUとして扱えるわけではない。無料枠を外部常駐APIサーバーとして使えると推定しない。

## 既存案との比較 / AI-Harnessへの価値
- **Google Colab無料枠との違い**：Colab公式はGPU種別・時間を動的とし、具体的な固定上限を公表していない。Kaggleは公式に週単位の目安を示すため、短時間の再現可能なGPU研究計画を立てやすい。
- **Harnessでの候補用途**：GPUが必要なローカルLLM/音声AIの短期実験、小型モデル比較、評価用バッチ処理、Kaggle BenchmarksとTRINITYの評価手法比較。
- **既存環境との重複**：Colab、ローカルGPU計画、TRINITY評価機構。単純な無料枠追加で管理負担が増えないかを比較する。
- **利用しない用途**：秘密情報の持ち込み、無許可の常時サーバー化、OpenAI GPTの無料API代替という誤認。

## 未検証と最小検証案
1. 電話認証前にKaggle利用規約とプライバシーポリシーを確認。ユーザーの同意なしにアカウント接続しない。
2. 人間の希望があれば、認証後に割当GPU・残時間・利用条件を画面で確認し、機密を含まない短い計算のみ試す。
3. 同じ公開ベンチをColabとKaggleで実行し、GPU待ち時間、実測速度、セッション安定性、準備負荷を記録。
4. Benchmarks機能はTRINITYの sealed artifacts / Human Authority を置き換えず、比較対象としてのみ扱う。

## 一次資料
- Kaggle GPU利用枠：https://www.kaggle.com/docs/efficient-gpu-usage
- Kaggle Notebook仕様：https://www.kaggle.com/docs/notebooks
- Community Benchmarks公式発表：https://www.kaggle.com/discussions/product-announcements/667898
- Kaggle Benchmarks公式仕様：https://www.kaggle.com/docs/benchmarks
- Kaggle CLI quota文書：https://github.com/Kaggle/kaggle-cli/blob/main/docs/benchmarks.md
- Google Colab無料制限：https://research.google.com/colaboratory/faq.html
- Googleの買収発表：https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/100-announcements-google-cloud-next-17/
- Kaggle利用者数：https://www.kaggle.com/c/about/featured
- 電話認証要件（Kaggleスタッフ）：https://www.kaggle.com/product-feedback/268333
- 個人情報方針：https://www.kaggle.com/privacy

**Authority boundary**: 研究記録の保存のみ。無料枠登録、電話番号提供、サービス連携、GPU起動、Core/Trinity/Skills変更は含まない。
