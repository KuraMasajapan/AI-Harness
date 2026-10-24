---
document_type: research_crossreference
created: 2026-10-24
project: BBB
source_post: https://x.com/ludoonchart/status/2113689074196263406
stage_1_rank: A+
stage_2_rank: A
decision: CANDIDATE / REFERENCE
implementation: HOLD
status: RESEARCH ONLY / NOT IN CURRENT SPEC
existing_match: Kronos
new_comparison_candidate: TradingAgents
low_relevance: REA
human_instruction: "BBBで『ハーネスを確認して』と言った際に見つけられるようにする"
recall_triggers:
  - ハーネスを確認して
  - ハーネス確認
  - BBB研究候補
  - REA
  - Kronos
  - TradingAgents
  - AI投資リサーチ
  - 金融予測
  - ローソク足予測
  - 売買判断
  - マルチエージェント
  - TradingAgents比較
  - BBB
---

# BBB研究ノート — REA / Kronos / TradingAgentsの全体像・既存研究との照合

> **BBBでの呼び出し:** 「ハーネスを確認して」「BBBの研究候補を確認して」「KronosやTradingAgentsについて確認して」等を受けた場合、まずBBBの現在のSource of Truthを確認し、本ノートおよび既存Kronos評価を**研究資料として**参照する。チャットの記憶だけから導入済み・取引可能と断定しない。この文書はGitHub検索・手動再読込用の入口であり、アプリに自動発火のコードを追加したものではない。

## 1. 投稿と3件の原典

- 投稿者 @ludoonchart、2026-10-23: https://x.com/ludoonchart/status/2113689074196263406
- [REA: morluto/rea](https://github.com/morluto/rea) — エージェントからソフトウェア、バイナリ、Web/Electron等を調査するリバースエンジニアリングMCP。
- [Kronos: shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) — ローソク足（OHLCV）のトークン化により価格系列を生成する金融時系列モデル。
- [TradingAgents: TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) — ファンダメンタルズ／ニュース／センチメント／テクニカルの分析者、強気・弱気の議論、トレーダー、リスクとポートフォリオ担当に分業するLLM金融研究フレームワーク。

公式GitHubの存在・READMEを2026-10-24に照合。3件は独立したOSSであり、連携済みの完成品ではない。「Wall Streetで禁止されるべき」「無料のBloomberg級ターミナル」「容易に利益が出る」という宣伝は立証されていない。ライセンス公開とデータ、推論、保守、API費用無料は別問題。

## 2. 投稿の提案する「3つを組み合わせる」全工程（概念であり実験ではない）

1. REAをClaude Codeに追加し、既存の金融端末の画面やワークフローの構造を調べる。
2. 株式、暗号資産、FX、商品、指数、ニュース等を示す統合UIを作る。
3. Kronos-small（README記載: 24.7Mパラメータ、入力最大512本）を読み込む。
4. 512本など過去のOHLCVから次の24本などを予測し、複数サンプルにより将来の値動きを表現する。
5. TradingAgentsを同じデータに接続する。
6. 複数のアナリスト、BULL/BEAR、リスクとポートフォリオ担当で判断過程を分ける。
7. BUY/SELL/HOLD、過去時点での情報、手数料・スリッページを加えたバックテストで評価する。

この手順は投稿の**提案**。一式がそのまま組み上がる、現物BTC/JPYで利益が出る、既存ソフトの解析や模倣が許諾済み、という証拠ではない。

## 3. BBBへの個別適合性

### 3.1 Kronos：MATCH — 2026-10-20にすでに詳細調査・保存済み

**既存一次記録**: [Kronos Candlestick Model Evaluation](2026-10-20-kronos-candlestick-model-evaluation.md)

- 本OSSと論文、モデル規模、BTC/USDT例、推論の処理、先行する懐疑的研究などは既存ノートで検討済み。**新規発見として重複採録・仕様採用しない**。
- 既存BBBには決定論的なMean Reversion等、Training Lab、Active Forward、Shadow Prospective Forward、Execution Parityなどの検証層がある。Kronosを試すなら**新しい別枠予測ベースライン**。
- 重要な実装上の違い: 公式Kronosの通常の `predict()` はサンプル系列の平均を返す。投稿の「100本の未来シナリオが取得できる」と単純には言えない。個別予測分布を評価するなら別途インターフェイス、校正、評価が必要。
- 学習時点が古いとは限らないため過去データへのpretraining混入可能性も考慮し、同一の時系列・同一コスト条件の**未見データ**で比較する。
- **A+（関心）／研究再確認のみ／実装HOLD**。本記録は既存Kronos評価を上書きしない。

### 3.2 TradingAgents：PARTIAL OVERLAP — 独立した判断比較方式として増分あり

- 公式READMEはBTC-USD/ETH-USD等も例示。**bitbankのBTC/JPYをそのまま使える証拠ではない**。Yahoo Finance等の市場データとBBBのbitbank5分足を同じものと扱わない。
- 同時進行するテクニカル・ニュース・センチメント等の分析者、強気/弱気の議論、リスク評価、最終Portfolio Managerという判断ログが新しい具体例。既存TrinityやBBBの分類・Risk Managerと**考え方が重複**する。
- READMEはPoint-in-timeデータ、バックテスト、レポート、Checkpoint、複数LLM、Ollama/OpenAI-compatibleへの対応を説明。ただし改善幅、取引損益の再現性、利用料の実負担は**未実証**。
- BTC/JPY現物は空売り・レバレッジなし。売りは原則保有BTCの売却であり、強気/弱気の議論を空売り取引に直結させない。
- 比較するなら、既存BBBの判断を変えず、固定入力・既知時刻・同じモデルの予算にて**別プロセスで提案・根拠・反証・不確実性を記録**し、独立して検証。
- LLM同士の議論の合意は客観的正解や利益の証拠ではない。複数Agent間の影響、未来情報の混入、ニュース公開時刻、API費用、トークン消費に注意。
- **A / CANDIDATE（独立比較のみ）／実装HOLD**。

### 3.3 REA：REFERENCE — BBBの予測能力を直接増やさない

- ソフトの動作・ファイル・コード・画面・バイナリを解析するMCPで、売買の予測器・相場データ配信サービスではない。
- UIの仕組みや自作ソフトの動作解析など一般のエンジニアリングには利用可能性があるが、BBBの収益性検証では優先度低。
- 他社金融ターミナルの非公開機能、データ、商用UIの取得・複製は規約、ライセンス、著作権、アクセス権限の確認が必要。解析できることと許されることは別。
- **C（BBBの取引研究）／REFERENCEのみ**。

## 4. 現行BBBとの比較基準（Snapshot 2026-10-20）

[BBB CURRENT_SPEC](../../CURRENT_SPEC.md) を必ず再読込すること。このノート中のスナップショットを未来の現在値にしない。

- GitHub `projects/BBB/CURRENT_SPEC.md` の2026-10-20現在欄には、**BBB v0.9.39 Shadow Prospective Forward**、現物bitbank BTC/JPY、Live未実装、Human承認必須とある。
- Frozen Active Mean ReversionのForwardは2026-10-08 17:20 JSTを基準に継続。Shadowの新しいFreezeは2026-10-20 20:32:52 JST（候補entry_buffer_06）。**両Freezeと独立した先行評価を保護する**。
- Active Forwardの当時値（legacy +1.37%）とコスト織込みExecution Parity（-0.99% modeled net）が乖離している。Grossがプラスでも経済性やLive readinessは保証しない。
- 実際のソースコードはGitHubと自動同期されていない（実装の根拠はZIPや対応checkpoint等と再照合する）。この研究ファイルだけでアプリの挙動は変更されない。
- 優先課題は**取引コスト、実行可能性、損益の独立検証、注文の安全性**。AI予測や多Agent議論の追加はそれを代替しない。

## 5. 統合しない比較実験の候補（将来Human承認が必要）

1. BBBの両Forward、Paper、Strategy Championを不変に保ち、既存5分足の参照権限を分離した読み取り専用サンプルを使用。
2. Kronosは既存ノートのルールで方向・ボラティリティ・校正を比較。データ重複やPretrainingの未来混入に注意。
3. TradingAgentsは決定日時時点で利用可能な公式ニュース、価格、発表時刻のみを与え、買い／売り／見送り根拠を記録。
4. 比較する指標: ランダム/変化なし/既存Mean Reversion基準との差、方向一致、予測誤差、cost-netリターン、DD、PF、約定モデル、計算費用、遅延、データ漏えい、再現性。
5. 再計算可能なログと同じPeriodで比較し、モデルの提案で学習済み条件・Frozen条件を変えない。未見テストに何度も触れた場合は、その情報汚染を記録。
6. 正の追加価値が示されないなら追加しない。判断モデルから注文命令への自動昇格やAPI key共有はしない。

## 6. 検索・起動手順（Research Only）

BBBチャットでユーザーから **「ハーネスを確認して」** と依頼されたら：

1. リポジトリ `KuraMasajapan/AI-Harness` の現在のブランチ・Source of Truthを確認し、必要に応じて `HARNESS.md`、`core/RULES.md`、`core/WORKFLOW.md`、`core/ACCESS.md` を読み直す。
2. **必ず先に** `projects/BBB/CURRENT_SPEC.md` の最新の「Current release」部分と `projects/BBB/README.md` を確認し、古いREADME本文と最新SPECが食い違うときはSPECを優先する。
3. 研究候補の確認も目的に含まれる場合、`projects/BBB/research/field-notes/README.md` と本ノート、既存Kronosノートを参照する。研究以外の依頼なら関連ファイルだけを選ぶ。
4. 必要な場合は `incubator/proposals/2026-10-23-tradingview-api-bbb-safe-extraction-guide.md` など他のHarness横断研究を検索する。
5. CURRENT実装 / HOLD研究 / 自分の推論を分離して回答。**文書を発見しただけでは処理が実際に発火・実装された証明にならない。** BBBアプリや別チャットがリポジトリを読み込めない場合、コマンドの自動処理は保証できない。

**関連の検索語**: `ハーネスを確認して`、`BBB`、`Kronos`、`TradingAgents`、`REA`、`AI金融研究`、`予測ベースライン`、`マルチエージェント`、`Forward Gate`、`Shadow Prospective Forward`。

## 7. 保存の境界

Humanが2026-10-24に「BBBに『ハーネスを確認して』と言えばわかるようにしておいて」と明示依頼。研究の入口と関連リンクの保存に限り、**現在の売買ロジック、Live Gate、Freeze時刻、BBBソースコード、各Agentの実行・権限を変更しない**。他のProposalやCoreを無断変更しない。
