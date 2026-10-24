---
document_type: external_research_evaluation
created: 2026-10-24
project: BBB
source_post: "https://x.com/carm1nee/status/2113765239674032262"
upstream: "https://github.com/HKUDS/Vibe-Trading"
upstream_org: HKUDS
stage_1_rank: A++
stage_2_rank: A+
decision: CANDIDATE
role: INDEPENDENT_RESEARCH_COMPARATOR
implementation: HOLD
status: RESEARCH_ONLY / NOT_IN_CURRENT_SPEC
human_preference: "2026-10-24: comparison target; save same as previous BBB research"
evidence_status: "X POST & OFFICIAL GITHUB README EXAMINED; BBB COMPARISON NOT RUN"
trigger_topics:
  - ハーネスを確認して
  - ハーネス確認
  - BBB研究候補
  - Vibe-Trading
  - vibe-trading-ai
  - HKUDS
  - 香港大学
  - 独立比較
  - BBB比較
  - TradingAgents
  - Alpha Zoo
  - 478因子
  - ストラテジー研究
  - Backtest
  - Walk-Forward
  - Monte Carlo
  - Bootstrap
  - Shadow Account
  - Paper Trading
  - Pine Script
  - MT5
  - 金融AI
  - ヘッジファンド
  - 取引コスト
  - Forward Gate
---

# Vibe-Trading — BBBの独立した研究・検証基盤としての比較候補

> **一読要約**
>
> HKUDS/Vibe-Tradingは自然言語で金融調査、データ収集、戦略コード生成、Backtest、頑健性テスト、Multi-Agent研究、Paper運用、レポート・TradingView等への出力を行うOSS。BBBにも類似機能が多いが、**478 Alpha因子の探索、研究ラン・数値根拠の検証、異なるエンジンによる結果の突合**には比較価値がある。
>
> 2026-10-24のHuman判断は**「比較対象」**。BBBの置換・自動注文システムとして採用しない。将来、**別環境・同一データ・同一コスト前提で、独立に検証できるか**を見極める。
>
> **Stage 1 A++ → Stage 2 A+ / CANDIDATE / 実装HOLD。** 今回は実装・配布・認証・実売買には進まない。

## 1. 発見とHumanの意図

- X投稿：[@carm1nee](https://x.com/carm1nee/status/2113765239674032262)、2026-10-23 UTC。Vibe-Tradingを「一文でQuant Desk」「478因子」「Monte Carlo / Bootstrap / Walk-Forward」「Pine Script / MT5」「Paper Trade」と紹介。
- 公式ソース：[HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading)、[PyPI配布パッケージ](https://pypi.org/project/vibe-trading-ai/)、[Docs](https://vibetrading.wiki/docs/)。
- 2026-10-24時点のREADME・GitHub metadataを確認。約36,438 stars、MIT license、Python 3.11+、FastAPI/React UI。Starsは性能・安全性・収益性の実証ではない。
- 公式READMEは2026-10-22にv0.1.18リリース、10/23-24にも未リリースの修正を説明。**mainと実際のPyPI releaseを混同しない**。
- Humanコメント「香港といえばアジアの金融拠点の一つ」「比較対象だね」。**大学系組織という背景は関心の根拠であって、金融機関の審査済み・儲かる保証ではない**。
- Humanは前のBBB研究と同じ形式での保存を承認。BBB field-notesに1件保存し、BBB READMEの「ハーネスを確認して」入口から参照できるようにする。

## 2. Vibe-Tradingは何をするか

公式READMEは自然言語の指示を金融Tool、API/MCP、Run Artifactと結びつけるResearch Workspaceと説明。

| 領域 | READMEで確認した機能・説明 | 注意事項 |
|---|---|---|
| 自然言語研究 | Strategy draft、Market Data取得、バックテスト、報告書生成 | 生成内容は検証が必要 |
| Alpha Zoo | **478因子**をIC、Alive/Reversed/Dead等で評価 | 株式向け因子も含み、BTC/JPY 5分足に全適用可能とは限らない |
| リスク検証 | Monte Carlo、Bootstrap、Walk-Forward、時点付きRun Cards | 信頼性・採点手順の独立監査なし |
| Multi-Agent | Investment / Quant / Crypto / Macro / RiskのSwarm分析 | 多数のAgentが利益を生むとは限らず、LLM費用増の可能性 |
| 市場データ | 株式・Crypto・FX等のLoaderとProvider Fallback、独自OHLCV導入の説明 | bitbank BTC/JPYの同じデータと取引条件を保証しない |
| Paper / Shadow | 日足等を用いたPaper Account、ジャーナルに基づくShadow比較 | **BBBの独立した5分足・凍結後Forward Gateとは別の概念** |
| Artifact | Pine Script v6、MT5/MQL5、Reports、API/MCP | Export可能でも実戦で有効とは限らない |
| Agent/LLM | Claude Code CLIや複数Provider、OpenAI互換Gateway | OSS無料とAPI/サブスク無料は違う |
| Safety | 非ローカルAPI認証、Shell Tool既定制限、Broker連携ガード等 | 作者の説明でありBBB環境の安全性は未検証 |

**誇張の切り分け**：「個人でもヘッジファンド級」「無料」「一文でAlphaを発見」は投稿側の宣伝。収益性、計算・情報・保守費用、取引可能性は確認されていない。

## 3. 既存BBBとの重複と増分

[BBB CURRENT_SPEC](../../CURRENT_SPEC.md) の2026-10-20時点の検証済み版は**v0.9.39**。Source codeは配布済みZIPとGitHubで未同期なので、将来の比較前に最新の実機/ZIPを再確認する。

| 比較軸 | BBBの既存機能・状態 | Vibe-Trading側の増分仮説 |
|---|---|---|
| Strategy | Mean Reversion等のStrategy Lab / Champion | Alpha Zoo、自然言語による戦略草案と広域探索 |
| Backtest | Replay、時系列Fold、Holdout、Active/Shadow Forward | 別エンジンでの独立評価、Look-ahead・評価窓の検証 |
| 統計 | Matched Control、Robustness Check / Bootstrap等 | Monte Carlo・Bootstrapの計算方式比較 |
| 取引実態 | Execution Parity、手数料・Slippage想定 | 同一条件のNet return、DD、PF、Turnoverの独立再計算 |
| 証拠 | Dataset Hash、Run Report、Journal、Evidence Readiness | Numeric Grounding、undefined/null、ProvenanceとArtifactの監査 |
| Research AI | Sokudan Sandbox、Macro Research | Swarmの分析・反証過程、ただし売買へ自動影響させない |
| UI/Paper | BBB Desktop CockpitとPaper、Freeze付きForward | 参考UIと日足Paper。BBBの機能をそのまま置き換えない |

**採用を決めるべき理由ではなく、比較価値**：自前BBBとは別方式で計算することにより、BBBの見落とし・計算定義差・データの問題を発見できる可能性がある。

「独立検証」には同一Dataset・タイムゾーン・時点・手数料・ルールに加え、検証対象の選別バイアスとコードの独立性も記録すること。片方の結果を見て最適化すると未見とは言えない。

## 4. 他の既存研究との関係

- [2026-10-20 Kronos調査](2026-10-20-kronos-candlestick-model-evaluation.md)：OHLCVの将来予測というモデル。Vibe-Tradingの戦略研究・検証ツールとは役割が違い、連携は未決定。
- [2026-10-24 REA/Kronos/TradingAgents](2026-10-24-rea-kronos-tradingagents-bbb-crossreference.md)：TradingAgentsは多Agent金融判断、Vibe-Tradingは重なる部分があるがAlpha Zoo・Backtest Tool群の比較余地が広い。
- [BBB field-notes運用](README.md)：Research CandidateはCURRENT_SPECやLiveへ自動昇格しない。
- [TradingView API研究](../../../..//incubator/proposals/2026-10-23-tradingview-api-bbb-safe-extraction-guide.md)：Pine出力とTradingViewデータの取得経路・規約を混同しない。

**総合**：機能重複はHIGH / 部分的な具体的新規性あり。Vibe-TradingとTradingAgentsを同時導入せず、まず個別の比較増分を確かめる。

## 5. 将来の最小比較実験（今回未実施）

1. **現状を保護**：Active Mean Reversion / Active Freeze（2026-10-08 17:20 JST）/ Shadow Freeze（2026-10-20 20:32:52 JST）/ Paper / Source of Truthを変更しない。Freezeを再設定しない。
2. **環境分離**：Vibe-Tradingの導入・生成Python実行は使い捨て環境で実施し、BBB本体Python、Secret、Private API、注文処理にはアクセスさせない。
3. **共通データ**：事前固定したbitbank BTC/JPY 5分足の読み取り専用Dataと時刻を使い、Loader差は明示。OHLCV formatが非対応なら適正な変換を検証する。
4. **比較Baseline**：Mean Reversionの固定条件、Buy/Hold、No-trade等。同一情報・期間・通貨・現物・取引回数を守る。
5. **コスト**：bitbankでのMaker/Taker、Spread、Slippage、最小注文額、Precision、約定不可、Partial Fill等を同条件に。**実際のLive約定が再現できたと誤認しない**。
6. **指標**：Net Return、DD、PF、Turnover、時間、CPU/RAM、LLM費用、Log trace、Future information leakage、変更しないHoldout。
7. **採否基準**：再現可能な検証上の発見、現行BBBと異なる障害検知、安全な独立算定、費用対効果などに明白な改善がある場合だけ次段階を検討。成果がなければ不採用も可。

## 6. 費用・安全・誤認の注意

- **AI生成コード実行**：Local Python subprocessによるStrategy BacktestはShell/Network/File accessの実質的な権限を検査する必要がある。狭めた環境変数だけで完全なsandboxと見なさない。
- **取引権限**：READMEにはTAPの認証ProxyやHuman approval、Broker Mandate等の説明があるが、bitbankへの対応を意味しない。BBBのPrivate API Key・実資金取引権限を付与しない。
- **Claude Code CLI**：既存のCLI Loginに依存する方式が記載されているが、別途ライセンス・プラン・利用上限・提供規約の確認を要する。「追加API key不要」でも無料無制限ではない。
- **公式なりすまし警告**：公式READMEはVibe-Tradingを装ったXアカウント・Token/Wallet関連の詐称について警告している。OSS利用のためのToken購入・Wallet署名はしない。
- **バージョン依存**：main READMEには10/23-24の未リリース修正が含まれ、v0.1.18との整合は要確認。比較する際はRelease TagとCommitを固定。
- **金融研究**：478因子のAlive/Deadは市場・期間・多重比較・取引コストに依存。ForwardやWalk-Forwardだけで利益の保証はできない。

## 7. 二次評価の保存

| 項目 | 結論 |
|---|---|
| Stage 1 | **A++**：BBBとの関連性が非常に高い |
| Stage 2 | **A+**：重複は大きいが独立した検証方法・Alpha評価・研究証跡に比較価値 |
| Overlap | **PARTIAL / HIGH FUNCTIONAL OVERLAP** |
| Decision | **CANDIDATE — INDEPENDENT RESEARCH COMPARATOR** |
| Implementation | **HOLD** |
| Verified | X投稿の内容、公式repo、作者READMEによる機能・構成・リリース説明 |
| Unverified | BBB互換性・比較優位・金融効果・OS/CPU負荷・実運用セキュリティ |
| Human | 「比較対象」：まだ採用決定ではない |

## 8. BBBでの再発見：「ハーネスを確認して」

BBBの[README](../../README.md)に本ノートへのリンクを追加する。次の語でも研究候補を検索・照合する：**ハーネスを確認して / BBB / Vibe-Trading / HKUDS / 香港大学 / Alpha Zoo / 478因子 / 独立比較 / TradingAgents / Monte Carlo / Bootstrap / Walk-Forward / Shadow Account / 取引コスト**。

再読込順：最新のBBB CURRENT_SPEC → field-notes README → この調査 → 必要に応じてTradingAgents/Kronosの既存研究。Markdownの導線は宣言的であり、BBBアプリが自動的にGitHubを監視する機能は作らない。別チャットでGitHubへアクセスできない場合は自動参照を保証しない。

## 9. 変更権限

Humanが承認したのは**研究候補としての保存と前回と同じREADME導線**。Core、CURRENT_SPEC、DECISION_LOG、BBBコード、Model/Risk/Paper/Forward/Live設定、Freeze、API Key、外部認証は変更しない。実験や実装は別途Human承認。
