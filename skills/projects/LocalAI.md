# LocalAI

## 1. Purpose / 目的

This file stores stable context and important decisions for the LocalAI project.

このファイルは、ローカルAIプロジェクトに関する安定したコンテキストと重要な決定事項を記録する。

The project explores a local-first AI environment that can provide useful AI capabilities while keeping appropriate information and processing local.

このプロジェクトでは、必要な情報や処理を適切にローカルに保持しながら、AIを活用できるローカルファーストな環境を検討する。


## 2. Project Principles / プロジェクト原則

- Prefer local processing when practical.
- Consider privacy before sending information to external services.
- Use cloud AI when it provides meaningful advantages.
- Do not assume that local processing is always superior.
- Prioritize practical usefulness over technical complexity.
- Keep the system expandable.

- 実用的な場合はローカル処理を優先する。
- 外部サービスへ情報を送る前にプライバシーを考慮する。
- 明確なメリットがある場合はクラウドAIを利用する。
- ローカル処理が常に優れているとは考えない。
- 技術的な複雑さより実用性を優先する。
- 将来の拡張性を確保する。


## 3. Current Direction / 現在の方向性

The project is exploring a local AI environment that can operate as part of a broader AI-Harness.

現在は、AI-Harnessの一部として機能するローカルAI環境を検討している。

Possible roles include:

想定される役割：

- Local gateway — ローカルAIゲートウェイ
- Information classification — 情報の分類
- Context preparation — コンテキストの整理
- Privacy-aware routing — プライバシーを考慮した振り分け
- Local inference — ローカル推論
- Family or shared AI infrastructure — 家族・共有AI基盤

These roles are exploratory and should not be treated as fixed architecture until validated.

これらは検討中の役割であり、検証されるまでは確定したアーキテクチャとして扱わない。


## 4. Architecture Principles / アーキテクチャ原則

The system should separate:

システムは以下を分離して考える。

- AI behavior — AIの振る舞い
- Routing — 処理先の判断
- Local processing — ローカル処理
- Cloud processing — クラウド処理
- Memory — 記憶
- User interface — ユーザーインターフェース
- Security and privacy — セキュリティとプライバシー

A local LLM should not automatically be treated as the only possible gateway or decision-maker.

ローカルLLMを必ずしも唯一のゲートウェイや判断主体として扱わない。


## 5. Hardware Considerations / ハードウェア上の考慮事項

Hardware decisions should consider:

ハードウェアを選定するときは、以下を考慮する。

- VRAM — VRAM容量
- RAM — メモリ容量
- Power consumption — 消費電力
- Thermal characteristics — 発熱・冷却
- Reliability — 信頼性
- Expandability — 拡張性
- Cost — コスト
- Availability — 入手性

The hardware should be selected according to the actual workload rather than specifications alone.

ハードウェアはスペックだけで判断せず、実際の処理内容に応じて選定する。


## 6. Privacy and Security / プライバシーとセキュリティ

Information should be classified before external processing when practical.

実用上可能な場合、外部処理へ送る前に情報を分類する。

Potentially private information should not be sent to external services without an appropriate reason and user authorization.

プライベートな可能性がある情報は、適切な理由とユーザーの許可なしに外部サービスへ送らない。

Security decisions should be based on actual threat models rather than assumptions.

セキュリティ上の判断は、単なる思い込みではなく実際の脅威モデルに基づいて行う。


## 7. Decision Policy / 判断方針

Evaluate local and cloud approaches according to:

ローカルとクラウドの方式を以下の観点から比較する。

- Privacy — プライバシー
- Capability — 能力
- Cost — コスト
- Latency — 応答速度
- Reliability — 信頼性
- Maintenance — 保守性
- Scalability — 拡張性
- User experience — ユーザー体験

Avoid building infrastructure merely because it is technically interesting.

技術的に面白いという理由だけでインフラを構築しない。

Build only what provides a meaningful practical benefit.

実用上の明確なメリットがあるものを構築する。


## 8. Related Harness Files / 関連Harnessファイル

- `HARNESS.md`
- `core/ROLE.md`
- `core/RULES.md`
- `core/WORKFLOW.md`
- `memory/MEMORY.md`
- `memory/LESSONS.md`
- `evaluation/TEST_CASES.md`
- `evaluation/RESULTS.md`
