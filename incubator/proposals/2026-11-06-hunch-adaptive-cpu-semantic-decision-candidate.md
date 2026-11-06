---
document_type: research_evaluation
date: 2026-11-06
timezone: Asia/Tokyo
title: "hunch — CPU-local adaptive semantic decision layer using EmbeddingGemma 2"
source_social: "https://x.com/aigclink/status/2118237906716516496"
source_upstream: "https://github.com/undrgrnd-labs/hunch"
branch_target: development
stage_1_rank: A+
stage_2_rank: A-
decision: CANDIDATE
implementation: HOLD / NOT_IMPLEMENTED
evidence: "Public code, upstream technical documentation and Google model card checked; target-device benchmark, independent security evaluation and financial savings not reproduced"
relationship: "REINFORCE_EXISTING_JEV_CONTEXT_FILTER_AND_EFFICIENCY_TELEMETRY_PROPOSALS"
priority_note: "HIGH_VISIBILITY_RESEARCH_CANDIDATE; NOT_PRODUCTION_PRIORITY"
tags: [hunch, embeddinggemma2, cpu, local-ai, semantic-classification, teacher-student, model-distillation, online-learning, confidence-routing, observability, agent-traces, cost-efficiency, human-authority, hermes, trinity, jev, research-only]
---

# 注目候補：hunch — 高頻度の意味判定をCPUに引き継ぐ適応型ゲート

## 1. 判定と扱い

- **一次評価：A+** — AI-Harness Core/Execution Observation、TRINITYログ監視、Hermes Local Agent Phase 0の「GPUなし・軽量判定」という長期方針と合致。
- **二次評価：A−** — GitHubの実装、ベンチマーク方法、適用できない質問、精度確認・監査・降格の設計が公開されている。ただし実機計測・教師の精度・運用費用は未検証。
- **Disposition：CANDIDATE / IMPLEMENTATION HOLD**。研究優先度は高いが、即時実装の優先度ではない。AI-Harness v1.5 / Codex環境改善を阻害しない。
- **保存の性質**：公開情報に基づく検証候補の記録。既存のTRINITY sealed artifacts、writer lock、Human Disposition、正式レビューとRelease権限を変更しない。
- GitHubの調査資料として目立つ場所から見つけられるよう、`incubator/README.md`から本記録へリンクする。

## 2. 原情報・一次情報

- 中国語の紹介投稿（2026-11-05 UTC）: https://x.com/aigclink/status/2118237906716516496
- 同投稿内の開発元リンク: https://x.com/aigclink/status/2118237911758131708
- 開発元GitHub（MITまたはApache-2.0の選択式）: https://github.com/undrgrnd-labs/hunch
- hunch本体の設計・API・閾値・ベンチマーク: https://github.com/undrgrnd-labs/hunch/blob/main/hunch/README.md
- 様々な質問の適性・実証結果・事前テスト: https://github.com/undrgrnd-labs/hunch/blob/main/docs/question-design.md
- CPUバックエンド性能測定: https://github.com/undrgrnd-labs/hunch/blob/main/docs/performance.md
- Google公式 EmbeddingGemma 2モデルカード: https://ai.google.dev/gemma/docs/embeddinggemma/model_card_2
- Google公式発表: https://developers.googleblog.com/en/google-ai-edge-with-embeddinggemma-2/

**証拠区分**：ソースコードとドキュメントの存在・記載は確認済み。開発元による性能測定と「教師以上の精度」等の自己評価は、BOSS環境で再現しておらず主張として扱う。

## 3. 仕組み — 何を省力化するのか

同じ構造の短いAgentイベントに繰り返し問う「失敗したか」「どの種類の結果か」「秘密情報の兆候か」などの**固定した選択肢への判断**が対象。

1. **Exact cache**：過去と同じ状態・質問なら保存済みの回答を返す。
2. **Local student**：EmbeddingGemma 2の中間表現（既定で第8層）をCPUで求め、質問単位の小さな分類器で判定。学習済み範囲か、確信度が高いかを確認。
3. **Teacher fallback**：未学習・新規・曖昧・未合格の質問を高性能モデルまたは意思決定モデルへ送る。回答を訓練データにする。
4. **Graduation**：交差検証で教師回答との一致率等が十分な項目のみ、小型判定器へ移行。
5. **Audit / demotion**：小型側へ移行した後も既定で10%の判定を非同期で教師に照合。基準を割った質問は教師へ戻す。保持済みの学習結果と監査履歴で再起動後も継続する。
6. **Human ground truth**：教師に誤りがある場合、Human/検証済みラベルを与え、教師自身の偏り・盲点を分析できる。教師に似せるだけでは正解精度の保証にならない。

対応する判定型は`noul`（Yes/No）、`choice`（選択肢）、`score`（順序のある段階）。自由文生成・広範な因果推論・外部状態を伴う計画の代わりではない。

**境界**：通常のhunch proxyは短いテキスト状態を対象とする。`hunch.live`では画像・テキストの連続入力も扱うが、通常proxyがそのまま画像を汎用処理できるわけではない。

## 4. 性能の取り扱い

開発元の数値:
- **テキスト判定22 ms（p50）**：Apple M5 Pro、約190 tokensの実ツール結果を逐次入力した測定。p95は51 ms、p99は76 ms。
- **32並列時86 requests/s**：このときp50は382 ms、p99は466 ms。単発22 msと並列遅延を混同しない。
- **約1.5GBのプロセスメモリ**（モデル込み）、単一要求エンコード時は約7 CPUコアが忙しくなると記載。
- `hunch.live`による画像フレーム処理例はApple M5 Proで約110 ms（70 soft tokens）。
- X投稿の「100万tokensで3セント未満」は、今回確認した同条件の公式ベンチマークで裏付けられていない。**費用対効果未確認**とする。ローカル電力/メモリ/CPU占有、教師APIの初期学習・監査費用を含める。
- Windows i7-11700やGPUなし既存PCでの遅延、RAM占有、日本語ログへの精度は未測定。モデルの日本語能力とhunchの質問別適合性は別評価。

Google公式カードはEmbeddingGemma 2を740Mパラメータのマルチモーダル埋め込みモデルとして公開。hunchはモデル全体を毎回生成用途に使うのではなく、分類に有効な中間表現と軽量な分類器を利用する。

## 5. AI-Harnessへの適用順位

| 対象 | 望ましい用途 | 避ける用途 |
| --- | --- | --- |
| Harness Observability / Execution | 単純なツール結果のタグ付け、繰り返すログ分類、異常候補の一次抽出 | エージェントの最終評価、権限付与 |
| TRINITY | sealed事実に影響しない派生ログの注意喚起・監視補助 | A/B/C比較の正式結論、Human Disposition、Releaseの代行 |
| Hermes Local Agent Phase 0 | GPUなしの低遅延分類、用途別Teacher escalationの研究 | 既存Phase 0制約を越えて無断常駐・自律化 |
| BBB | 機械的なログ分類・補助監視 | 発注、リスク判断、金融結果の正当性判定 |
| Harness Router / Context Filter | 使い捨て文脈の分類、難しい案件だけ上位モデルへ委譲する可否のベンチマーク | RULES、Source of Truth、sealed evidence等の削除判断 |

**安全境界**：安全性に関わる稀少なYes（危険あり）を見落としやすいことを公式ドキュメント自身が警告している。one-sided判定（安全そうなものだけ小型側で通し、疑わしいものは教師へ回す）は比較候補だが、絶対的な安全保証ではない。外部モデル判断で情報破棄・権限拡大・承認を自動化しない。

## 6. 既存資料との重複・新規性

- **`incubator/proposals/2026-09-21-jev-context-filter-adoption-model.md`**：交換可能なContext Filter（none/deterministic/local/Jev）、保護文脈非委任、導入見送りの原則が先行。hunchはその候補実装になり得るが、Jevや既存ルールを無条件に置換しない。
- **`incubator/proposals/2026-09-20-efficiency-telemetry-public-metrics.md`**：速度やToken削減を単なる宣伝値でなく固定メトリクスで比較する方針が先行。
- **TRINITY Orchestrator**：監査とHuman権限は既設。hunch固有の研究価値は、*ラベルを蓄積して高速・低費用の「軽い判断」だけに教師の仕事を移譲する仕組み*と、教師への自動復帰設計。
- **既存のJev/Ollama/Sokudan候補**：同じ入力、同じルーブリック、同じ教師ラベル・真値で評価。新規性は「軽量な継続学習+卒業/監査/降格を含むProxy」であり「CPU分類の発明」ではない。

## 7. 後日検証するなら（まだ実行しない）

1. 現行の実装を変更せず、個人情報・機密情報・鍵を含まない**合成ツールログ150〜300件**と、Human確認済みの少数の正解ラベルを用意。
2. 決定的ルール、Jev/Ollama/Sokudan、hunch+教師を同一基準で比較。対象は失敗/成功、出力種別などの限定質問。少数派の「失敗」を十分に採録。
3. 公式pre-flight（層4/8/12/最終、交差検証、稀少クラスの検出、未学習判定）の条件を理解し、誤検知・見逃し・校正・教師呼び出し率・監査結果を比較。セッションをまたいだデータ漏洩を防止。
4. CPUコア占有、RAM、初期学習コスト、逐次/並列遅延を測定。高価なモデルを呼ばない単純ルールで十分なら採用しない。
5. 導入是非を別途Human判断。Harness v1.5、TRINITY sealed運用、Runtime設定、権限の変更は自動で行わない。

## 保存操作の境界

この研究記録とIncubator索引の案内のみを追加。hunchのインストール、モデルダウンロード、API設定、試験実行、既存コードやCoreルールへの変更は本件では行わない。
