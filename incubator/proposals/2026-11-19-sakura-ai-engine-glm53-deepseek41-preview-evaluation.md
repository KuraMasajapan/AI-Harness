---
document_type: external_service_research
status: research_candidate
created: 2026-11-19
origin: "https://cloud.sakura.ad.jp/news/2026/11/18/glm-5-3-flash_deepseek-v4-1-flash-1017_pubpreview/"
subject: "Sakura AI Engine GLM-5.3-Flash + DeepSeek-V4.1-Flash-1017 public preview"
stage_1_rank: A+
stage_2_rank: A+_PROVISIONAL
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
verified_at: 2026-11-19
tags: [sakura-ai-engine, glm, deepseek, cloud-llm, japan, free-tier, inference-api, model-routing, security, cost, ai-harness]
---

# さくらのAI Engine — 2モデル追加・AI-HARNESSでの評価（2026-11-19）

## 要約 / 評価の境界
- さくらインターネットの国内クラウド推論API「さくらのAI Engine」が2026-11-18に `preview/GLM-5.3-Flash` と `preview/DeepSeek-V4.1-Flash-1017` のパブリックプレビューを開始した。各モデルへのAPI切替はリクエストの `model` 指定。
- Stage 1 A+ / Stage 2 A+ (provisional) / **CANDIDATE / Implementation HOLD**。無料枠、国内推論、OpenAI互換 API、長大コンテキストは魅力だが、モデルの実品質、遅延、ツール呼び出し信頼性、レート制限の実効値、コストは**独立実測していない**。A+は収益性・モデル性能の保証ではない。
- この候補は **Sakura提供の推論APIサービス** であって、モデルの新規発明・DeepSeek Harness本体の導入提案ではない。
- 本レポート保存は研究記録のみ。サービスへの登録、電話認証、カード登録、APIキー発行、課金、HARNESS/CORE/Skills/Router/BBBの設定変更は含まない。

## 1. 公式発表で確認した追加モデル
| 項目 | GLM | DeepSeek |
|---|---|---|
| 正式API model ID | `preview/GLM-5.3-Flash` | `preview/DeepSeek-V4.1-Flash-1017` |
| 発表日 | 2026-11-18 | 2026-11-18 |
| Endpoint | OpenAI-compatible Chat Completions | 同左 |
| Context window（APIマニュアル） | 1,048,575 tokens | 1,048,575 tokens |
| `max_tokens` cap | 32,000 | 32,000 |
| Vision / Tool Call / Reasoning | Yes / Yes / Yes | Yes / Yes / Yes |
| Input types（サービス料金表） | Text/Image/Video | Text/Image |
| Response/output | Text | Text |
| License（さくらのモデルライセンス表示） | Z.ai / MIT | DeepSeek-AI / MIT |
| Paid price incl. tax | input ¥0.4 / 10k tokens; output ¥4.0 / 10k tokens | Same |

**注意:** 最大コンテキスト長は有効理解品質を保証しない。出力は32k tokens上限、約5分/リクエストの時間上限あり。Reasoning tokensも出力枠を消費する。Tool Calling/Reasoning/Visionの「対応」は、各ユースケースでの実品質を示さない。画像認識対応は画像生成と異なる。

## 2. サービスの利用方法・無料枠・費用
- Chat Completions endpoint: `https://api.ai.sakura.ad.jp/v1/chat/completions`; Bearer account token（発行時に見えるUUID:secret形式）を使用する。
- 月 **3,000 Chat Completions requests** の無料枠は**各モデル別ではなくChat Completions全体で共有**。無料枠は毎月更新。無料プランも従量課金プランも無料枠があり、無料プランは超過後レート制御、課金プランは超過後トークン従量課金。プラン自動移行はない。
- 契約・利用開始には、さくら会員ID、さくらのクラウドプロジェクト、**電話認証、クレジットカード登録**が必要。無償プラン新規受付数には上限あり。
- 3,000回未満でも混雑時に HTTP 429 となる場合がある。SLAなし。
- API serviceは embeddings 10,000回/月、音声文字起こし50回/月、TTS50回/月の別無料枠を掲げる。
- RAG/document storageは無料枠外。文書アップロード後、削除まで別費用が発生。料金ページでは**100チャンクあたり税込¥3**と説明。無料でモデル推論を試すケースではRAGを不用意に有効化しないこと。
- OpenAI-compatible `/v1/responses`とAnthropic-compatible `/v1/messages`エンドポイントがサービス全体に存在するが、**今回の2モデルに対する正式発表の提供形態はChat Completions**。すべてのClaude Code/Responses機能への完全互換を推定しない。APIは全てのOpenAI Chat Completionsパラメータをサポートしない。未対応フィールドを無視する場合あり。
- Playgroundはブラウザ試用画面。プラン契約が必要、試用はAPI同様無料枠/課金へ計上される。PlaygroundはFunction Callingに非対応。

## 3. データ・ライセンス・運用上の注意
- さくら公式によれば、AI Engine対象LLMはさくらがホストし、推論のリクエストは**国内データセンター**で処理。チャット等の入力・出力は保存せず、モデル学習にも使われない方針。**RAG文書はユーザーが削除するまで保管**。企業内部データ利用には機密区分、契約・責任分界を別途評価。
- `preview/` models は予告なしに仕様・品質・提供を変更/終了し得る。パブリックプレビュー終了後の価格変更もあり得る。API稼働の保証（SLA）なし。
- 新しいモデルの商用利用はプロバイダ固有条件を含めライセンスを利用時に再確認。公式さくらモデル表示では両モデルMIT。
- LLM側の自己申告するモデル名/仕様は信用せず、APIレスポンスとモデル一覧・請求ログをSource of Truthとする。

## 4. 既存プロポーザルとの重複と違い
1. `incubator/proposals/2026-10-17-deepseek-harness-v041-flash-evaluation.md`: **同系モデル** DeepSeek-V4.1-Flash-1017 とDeepSeek Harnessを研究済み。旧研究はモデルおよびHarnessの性能・構造・大きさ/自己ホスティング障壁を中心にA/HOLD。**今回の増分はさくら国内APIホスティング、現行無料枠・具体価格・マルチモーダルAPI仕様**。旧研究を上書き・採否変更しない。
2. `incubator/proposals/2026-10-21-magpie-deepseek-routing.md`: DeepSeekを既存router/gateway経由で使用する設計研究あり。今回のAPIは**新たなプロバイダ接続候補**として将来比較可能であり、Magpie採用の理由にはならない。
3. HarnessのLocalAI/Hermes/Ollama/ModelRouter検討は別。API利用は既存Core/Access権限体系を上書きしない。

## 5. A/B研究プラン（未承認・未実施）
- まず同一プロンプト/JSON/tool-call課題を5〜20件の固定セットとして、GLM vs DeepSeek vs 現行参考モデルを匿名化評価。成功率、出力正確性、JSON/ToolCall信頼性、日本語品質、TTFT/全応答遅延、スループット、Token/Requestと請求費用、429、タイムアウトを採取。
- ロングコンテキストの検証は小・中・大入力サイズ別に実施。最大windowが利用可能でも長文正確性を別試験する。
- **No live trading**。BBB金融系用途はResearch/Sandbox限定。
- **No automatic install/API access/registration**。Humanの別承認を条件にする。

## 6. 一次資料
- 発表 https://cloud.sakura.ad.jp/news/2026/11/18/glm-5-3-flash_deepseek-v4-1-flash-1017_pubpreview/
- モデルごとのAPI仕様 https://manual.sakura.ad.jp/cloud/ai-engine/chat-models.html
- サービス概要/国内データ/保存 https://manual.sakura.ad.jp/cloud/ai-engine/01-basics.html
- 利用手順/API https://manual.sakura.ad.jp/cloud/ai-engine/02-howto.html
- Playground https://manual.sakura.ad.jp/cloud/ai-engine/playground.html
- モデルライセンス https://manual.sakura.ad.jp/cloud/ai-license.html
- 料金・各モデル https://ai.sakura.ad.jp/sakura-ai/ai-engine/
