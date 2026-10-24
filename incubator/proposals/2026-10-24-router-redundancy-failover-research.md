---
document_type: architecture_research_candidate
date: 2026-10-24
timezone: Asia/Tokyo
title: "AI-Harness Router Redundancy — 2ルーター冗長化・振り分け・障害時フェイルオーバー研究"
origin: "Human discussion following Experiential Labs / GLM-5.3 Uncensored free API investigation"
status: "FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED"
stage_1_rank: A+
stage_2_rank: A
decision: CANDIDATE
implementation: HOLD
evidence_status: "IDEA / architectural hypothesis; current implementation and benefit UNVERIFIED"
human_approval: "2026-10-24: preserve as a research candidate for the next update planning; no implementation authorization"
branch: development
tags: [router, routing, model-routing, gateway, harnessrouter, redundancy, failover, fallback, multi-provider, resilience, availability, reliability, api-gateway, privacy, cost-control, human-gate]
trigger_topics:
  - ルーター
  - ルーター冗長化
  - 二重ルーター
  - 振り分け
  - モデル振り分け
  - ルーティング
  - ルーター切替
  - フェイルオーバー
  - フォールバック
  - 障害時切替
  - 障害対策
  - HarnessRouter
  - Router Redundancy
  - Router Failover
  - Model Routing
  - Gateway Failover
  - multi-provider routing
  - 次期Harnessアップデートのルーティング設計
---

# AI-Harness Router Redundancy — 2ルーター構成による障害耐性の研究候補

> **要約**
> 次回アップデートはこれから構想する段階。ルーターやモデル振り分けを検討するときに、単一ルーターの機能拡張だけでなく、**Primary/Backupの独立した2経路**を比較候補として思い出せるようにする。現時点の結論は**研究候補として保存**であり、設計確定・導入・自動切替の承認ではない。

## 1. 提案の発生経緯・原資料

- 2026-10-24、Human提供のX投稿でGLM-5.3 Uncensoredの無料APIを調査。
- 発見元: https://x.com/painn_x/status/2113761550091899310
- 提供元候補: https://platform.experientiallabs.ai/models/glm-5.3-uncensored
- 提供元のAPI Gateway: https://platform.experientiallabs.ai/docs
- 調査では、Experiential LabsがOpenAI互換APIで複数モデルを仲介するGatewayであると確認。無料表示や経路、利用条件は将来変更可能で、無料枠の永続性・品質・実運用の効果は未実証。
- Humanの新しい着想: **『バグ発生時のヘッジに二つのルーターを使うのは無しではない』**。
- Humanの保存指示: **『次のアップデート内容はまだこれから作る段階なので、研究候補として保存。ルーターや振り分けのキーワードをトリガーにして、構想時に再検討できるようにする』**。
- 本提案は**上記の着想と再検索要件の記録**。特定製品を2つ採用するという意思決定ではない。

## 2. 解決したい問題を分ける

### A. すでに扱われていた問題

- **モデル/プロバイダーの振り分け**: タスクに合うモデル・費用・利用枠でルートを選ぶ。
- **プロバイダー障害時のfallback**: 選んだルート先のAPI/モデルが応答しない場合に別モデルへ送る。
- **ツールの代替**: Web取得等のツールが動作しない場合に別ツールを試す。

### B. 今回の追加着想

- **ルーター自身の障害**: 主ルーターのプロセス、設定、依存ライブラリ、認証、更新不具合などで振り分け機構自体が動かなくなったときに、*主ルーターを通らない*第二経路で復旧できるか。
- **共通原因障害**: 2つのルーターが同じ資格情報、同一Gateway、同じSDK、同じホスト、同一クラウドAPI、共通設定/ポリシー、電源に依存すると、形式上2本でも同時停止する。
- **切替の安全性**: 故障と判断して転送した結果、重複呼出し、費用超過、Private内容の外部送信、許可範囲逸脱、タスク状態の分岐が起きないか。

**差別化**: 既存の『モデルが失敗したら別モデルへ』と、『ルーターが失敗したらルーターを使わず別経路へ』を分離する。

## 3. 比較対象となる候補構成（未採用）

### 案S: 単一Router + プロバイダーfallback

```text
Human / Harness policy
        ↓
     Router A ─────→ Model / Provider 1
        └──────────→ Model / Provider 2
```

- 最も単純で保守負荷が小さい。
- Router A自身が停止したときは共通障害点が残る。

### 案M: 2ルーター + 手動切替（最初の研究比較候補）

```text
Human / Harness policy / approval
          │
   [手動で経路を選択]
        ↙       ↘
  Router A    Router B
        ↘       ↙
     許可されたモデル/API
```

- Router Bに入るためにRouter Aの稼働を要求しない。
- 切替手段が単純であり、運用者が障害原因を見て選べる。
- 切替の手間、保守・設定の二重管理、誤切替は発生し得る。
- 独立性を確保する前に、同じモデル・同じ外部Gatewayを両方で使用しても実質的な冗長化にならない点を監査する。

### 案A: 2ルーター + 自動フェイルオーバー

```text
Human / Harness policy / approval
          ↓
  小さな独立した切替・監視機構
       ↙           ↘
  Router A       Router B
```

- 早い復旧の可能性はあるが、監視/切替機構自身が**単一障害点**になり得る。
- 判定誤り、ループ、split-brain、二重処理、追加の設定や費用が懸念。
- 『自動化したほうが良い』とは現時点で決めない。案Mで実用上十分なら案Aは不要。

**設計原則候補**: Routerは接続先選択と接続処理を担当。AI-HarnessのRule/Access/承認はルーターの外側で維持する。どの経路でも同一の最低安全条件を強制し、復旧用の経路でアクセス制限が緩くならないことを確認する。

## 4. 実装製品と設計の区別

| 要素 | 過去の研究位置づけ | 今回の扱い |
|---|---|---|
| HarnessRouter | プライベート/一般/コード等の分類と振り分けを担う構想 | 権限・ルート判断の責務を再点検する対象。稼働・実装状態は最新のSource of Truthで確認 |
| Magpie | ローカルGateway、複数モデル・プロバイダー切替/フェイルオーバーの候補 | Router A等の例。採用決定ではない |
| Experiential Labs | 外部OpenAI互換Gateway、特定モデルの一時的無料表示を確認 | Router B等の例。データ保持・料金・対応機能・制限の審査が必須 |
| FreeLLMAPI | 複数の無料プロバイダーをつなぐOSS候補 | 代替比較対象。保証された利用可能量とは扱わない |
| S.H.I.E.L.D. control plane | AI-Harnessにおけるモデル振り分け・費用・権限・fallbackの概念 | 冗長化の置き場所を考える上位概念。正式仕様ではない |

なお**二重化は外部サービスを増やさなくても実現し得る**。単純なバックアップ設定、既存GatewayのProvider failover、直接接続等も比較する。構成例のA/Bは製品名ではない。

## 5. 既存Proposalとの重複判定

- `incubator/proposals/2026-09-21-shield-low-cost-multi-ai-control-plane.md`: 低コストな複数AIへの振り分けとfallback、権限制御。**機能的に重なるが、主ルーター自体の故障への独立経路という論点は未整理**。
- `incubator/proposals/2026-09-21-ai-harness-reference-architecture.md`: S.H.I.E.L.D.層にモデルroutingとfallbackを配置した全体像。**今回の文書はその信頼性に関する派生仮説**。
- `incubator/proposals/2026-10-21-magpie-deepseek-routing.md`: Magpieのmodel routingとprovider fallbackを確認済み。**同じ製品の再評価ではなく、2ルーター採否の比較**。
- `incubator/proposals/2026-10-12-freellmapi-free-provider-routing.md`: 無料API・多Provider経路の利用。**共通依存・持続性を注意点として再利用**。
- `incubator/proposals/2026-10-18-autonomous-tool-fallback.md`: Web閲覧失敗時の代替ツール選択。**Tool fallbackとRouter failoverは別の障害レイヤー**。
- `incubator/proposals/2026-10-16-harness-minimalism-counterhypothesis.md`: 機能を増やすコストの反証。**二重化の必要性を測定して初めて複雑化を許す**。

**重複判定**: 既存ProposalはRouting/Provider fallbackの広い構想を持つ。今回はその重複を明示した上で、**Routerそのものの可用性と独立した退避経路**を一つの比較可能な研究課題として独立保存する追加価値がある。

## 6. 安全性・費用・障害モデル（設計前の確認事項）

1. **個人情報/Private保護**: あるGatewayで許可した情報を、退避先で同じように扱えるとは限らない。提供者のログ/保持期間・ZDR・利用規約・リクエスト内容を検査。特に無料プロモーションはPrivate許諾の根拠ではない。
2. **Human承認**: GitHub write、Shell、課金、個人情報の外部送信、BBBの判断・注文などは、通信成功とは別の権限問題。Router Bが承認を迂回してはならない。
3. **二重実行**: 発行済みか不明な処理を無条件にBへ再投入しない。リクエストID、結果確認、冪等性、同一操作の二重実行防止が必要。注文・書込みは自動切替しないのを初期条件とする。
4. **障害の分類**: ルーター停止、provider 5xx、429レート制限、401権限問題、timeout、PC電源OFF、共通依存、データ保護方針の不一致。全エラーで自動切替する設計は危険。
5. **コスト**: API利用料・有料プラン・通信・モニタリング・設定更新・保守時間・Human介入を含む総費用。無料枠や提供条件が変わる前提で考える。
6. **複雑さ**: 2経路化で可用性が実際に増えたか。設定ズレや依存関係の追加でむしろ信頼性が低下していないか。
7. **秘密情報/キー**: できるだけ別スコープの鍵、権限分離、漏えい時の停止、ルートごとの機密データ送信可否を確認。認証情報を非公式OSSへ安易に渡さない。

## 7. 将来の最小検証（今は実行しない）

**前提**: Humanが次回アップデート構想を始めたときに取り出す。現在のルーター実装状態と利用可能なサービス・権限・コストを再確認する。

1. **現行基準S**: まず単一ルーターと既存fallbackだけで、どの故障まで回復できるかを書き出す。
2. **案M（手動）**: ダミーの入力、権限のないテストプロジェクト、低額または無料の正規APIで、Router Aのプロセスを停止してもRouter B経由の読み取りタスクを実行できるか試す。
3. **独立性**: 片方の資格情報・設定・外部Gateway・ネットワーク・PC停止を模擬し、共通要因で両方落ちないかを確認。片方が無料上限に達した状況も観察。
4. **比較指標**: 復旧の成否、Recovery Time、切替操作数、変更・確認にかかった時間、リクエスト重複、失敗ログ、追加コスト、Private情報の逸脱、必要な権限の増加。
5. **自動化の必要性判定**: 案Mで十分かを先に確認。自動切替を作る場合も「有害な再試行を止められる」「操作・課金の承認を維持」「容易に元へ戻せる」ことを必須条件とする。
6. **No adoption option**: 単一ルーター + 手動直接接続のほうが軽く、安全で故障にも十分耐えるなら二重化しない。

## 8. 研究評価

- **Stage 1: A+** — AI-Harness全体で可用性・障害復旧の問題に関係し、次のルーティング設計検討時に思い出す価値が高い。
- **Stage 2: A（暫定）** — 既存のrouting/fallback構想と重なるが、Router単体障害への独立退避経路という別の検証仮説がある。現行Harnessでの改善効果・費用対効果は未検証。
- **Evidence**: FACT（既存Proposalにrouting/fallback関連構想の記載あり）、IDEA（Humanの2ルーター冗長化案）、UNVERIFIED（改善幅・必要性・実装可否）。
- **Decision**: CANDIDATE / FUTURE VALIDATION / IMPLEMENTATION HOLD。
- **保存価値**: 実装の確定を急がず、次期更新で『ルーターを増やす必要が本当にあるか』を再検討できる根拠と比較手順を残すこと。

## 9. Recall triggers / 将来の検索用キーワード

特に次の言葉が今後の会話・設計資料に現れた場合、このProposalを**検索候補として想起・提示**し、既存のMagpie・FreeLLMAPI・S.H.I.E.L.D.と照合する。

- 中核: **ルーター / 振り分け / ルーティング / HarnessRouter / モデル選択**。
- 高一致: **2ルーター / ルーター冗長化 / Router Redundancy / Router Failover / 代替ルーター / Gateway Failover / デュアルルーター**。
- 関連: **フォールバック / バックアップ経路 / 障害復旧 / 切替 / APIゲートウェイ / provider routing / 無料モデルの振り分け / 次期アップデート**。

これはGitHub/Obsidian/AIの検索や将来の設計レビューに使う**検索メタデータ**であり、会話を監視して自動実行するトリガー機構を新設するものではない。自動検索・通知・Coreへの常時注入は未実装であり、保証しない。

## 10. 権限と次のアクション

- **保存の承認のみ**。Humanが次期アップデートを構想する際に、このProposalを取り出して比較する。
- 現時点でRouter A/B、Magpie、Experiential Labs、FreeLLMAPI、APIキー、料金設定、契約、サービス接続は新規に導入・変更しない。
- AI-HarnessのCore、Access、Workflow、Trinity、Hermes、BBBや実装コード、他のProposalは変更しない。
- 将来の技術選定・試験・採用・実装は、その時点の実態とHuman承認を前提とする。
