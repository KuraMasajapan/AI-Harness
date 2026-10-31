# Proposal — Fugu Max / 無料AIリソースの評価と段階利用

- Date: 2026-10-31
- Status: PROPOSED / NOT IMPLEMENTED
- Scope: AI-Harness横断（Codex、TRINITY、BBB、GROWGLE）
- Decision: 調査候補として保存。API課金・自動連携・本番採用は未承認。

## 目的
Codexの限られた利用枠を実装・テストに優先配分し、Fugu Maxを独立レビュー・複雑な推論の候補として検証する。Fugu Max内部で複数モデルを協調させる層と、AI-Harnessが外部AIを振り分ける層は補完関係。性能向上は推測せず実測する。

## 暫定評価
| 観点 | 評価 | 根拠・懸念 |
|---|---|---|
| 設計レビュー | 有望 | Sakanaがコード・推論等のベンチマークで好成績を公表。ただし独立検証は未実施 |
| 外部連携 | 技術的に可能 | OpenAI互換API、Function Calling、Structured Output。MCPはCodex等ホスト側が橋渡し |
| コスト | 試用に好条件 | 公式チャット無料。公式APIは入力$2/百万token、出力$6/百万token。外部API枠は条件付き |
| 安全・運用 | 要検証 | 規約、学習利用設定、第三者へのデータ転送、上限変更、費用超過対策 |
| 総合 | **検証推奨・本番保留** | Codex利用枠の節約とセカンドオピニオン候補として価値あり |

## 利用ルート（2026-10-31時点）
| ルート | 利用枠・評価 |
|---|---|
| Sakana Chat | 公式無料ブラウザチャット。ログインで上限緩和。APIとは独立 |
| Rewind.ai | 匿名2,500 token/日、無料登録5,000 token/日と案内。APIは別料金 |
| Puter.js | 無料試用枠あり。User-Pays方式のため「開発者の統合費ゼロ」≠「利用者のAI費ゼロ」 |
| teai.io | 登録100クレジットの案内。Fugu Maxの利用回数は文章量と単価で変動 |
| FastMetal | Fugu Max APIを提供。無料モデルはあるがFugu Max自体が無料対象か未確認。新規登録無料クレジットなし |
| Sakana公式API | 有料。従量課金または月額プラン。チャット無料枠と別 |

## 検証計画
1. **Phase A（無料チャット）**：公開可能または機密除去済みのAI-Harness設計資料をFugu MaxとChatGPTに同一条件で渡す。指摘の正確性、根拠、具体性、新規性、誤りを比較して記録。
2. **Phase B（小規模API）**：必要と判断した場合だけ、Puter.jsやteai.ioの条件を確認し、JSON出力・ツール呼び出し・速度・失敗率・消費枠を測定。
3. **Phase C（Harness統合）**：Codex=実装、Fugu Max=独立評価、ChatGPT=設計対話、Sarasina AI=日本語処理候補。連携の費用・監査・復旧策を確認して別途採否判断。

## 非採用事項・ガードレール
- 無料チャットを非公式自動操作してAPI代替にしない。
- 無料枠を永続・無制限とみなさない。
- 社外秘、個人情報、認証情報を第三者サービスに無断送信しない。
- TRINITY sealed構成や既存権限を変更しない。
- 書込み・発注などの実行操作には人の承認を設ける。
- 今回のProposalだけで新規契約・課金・実装は行わない。

## 出典
- https://chat.sakana.ai/faq
- https://sakana.ai/chat-fugumax/
- https://sakana.ai/fugu-max-release/
- https://console.sakana.ai/models
- https://console.sakana.ai/get-started
- https://console.sakana.ai/pricing
- https://rewind.ai/apps/sakana-fugu-max/
- https://developer.puter.com/ai/sakana/fugu-max/
- https://developer.puter.com/pricing/
- https://teai.io/pricing
- https://fastmetal.jp/docs/faq
- https://fastmetal.jp/models/sakana/fugu-max

**結論**：PROPOSED / VALIDATION CANDIDATE。無料チャットによる独立レビューから開始する案を保存。実装・課金は保留。
