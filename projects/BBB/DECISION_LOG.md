# BBB Decision Log

## 2026-09-29

### Project start
- 正式名称を **BITBANK-BOT** と決定。
- 略称を **BBB** と決定。
- 取引所を **bitbank** と決定。

### Core philosophy
- 最初はAI取引の検証を目的とする。
- 常時多数のAIエージェントを動かさない。
- 古典的なBotを常時稼働の土台とし、将来AIは必要時のみ利用する省エネ構成を目指す。
- Humanとの常時ホットラインなしでも、将来的に記録・評価・改善を自動化する。

### Development ownership
- 初期構築はSOLで進める。
- Codexはゲーム開発が落ち着いた後、BBB完成版の独立監査役として利用予定。

### Exchange integration
- bitbankとの接続の基本層は **CCXT** を採用。
- 販売所経由ではなく、取引所の現物板取引を前提とする。
- bitbank公式APIドキュメントをAPI仕様のSource of Truthとする。

### Phase 1
- エージェントなしBotから開発開始。
- BTC/JPYを初期対象とする。
- 現物のみ。
- 空売りなし。
- レバレッジなし。
- Paper Tradeを先行。
- EMA + RSI を基準戦略とする。
- 基準戦略は最終戦略ではなく、将来の改善効果を測るBaselineとして扱う。

### Validation
- Backtestを導入。
- Live Paper Tradeを導入。
- Historical Replayを導入。
- 過去相場は未来情報を見せず時系列に再生する。
- Buy & HoldをBaseline比較対象にする。
- 手数料・スリッページ・最大ドローダウン・勝率・Profit Factor等を評価対象にする。

### Improvement loop
- Agentless Learning Loopを導入。
- EMA/RSIパラメータ候補を自動探索する。
- 時系列Fold + unseen Holdoutを使う。
- Research Championの更新は自動化可能とする。
- リスク上限は自動最適化対象にしない。
- 同一データセット再利用による安易な昇格を抑止するためDataset SHA-256を記録する。
- Research Championから実資金Liveへの自動昇格は禁止。

### JPY / FX issue
- BTC/JPYにはUSD/JPYの為替影響が混ざることを重要課題として採用。
- 判断用にBTC/JPY ÷ USD/JPYを利用できるFX-aware構造を実装。
- 実際の損益評価はJPY建てで維持する。
- 異なるSignal Basisで学習したChampionを、同じ参照データ無しにPaperへ流用しない。

### Security
- API Key / SecretをChatGPTへ貼らない。
- API Key / SecretをGitHub / AI-Harnessへ保存しない。
- 将来Live時はPC側の環境変数またはSecret Storeで保持。
- BBB用APIには出金権限を与えない方針。
- 実注文開始前にLive Trading Gateを設ける。

### Logging policy
- BBBの重要決定・仕様変更・検証状態をAI-Harness内にも継続記録する。
- 秘密情報と大量の実取引生ログはHarnessへ直接保存せず、要約・Checkpoint・検証結果を記録する。

### v0.6 immediate-use direction
- 「すぐ使えるものに仕上げて渡し、そこから学習を続ける」方針を採用。
- Windows向けDesktop Research Consoleを追加。
- BBB_START.batから初回環境構築と起動を行う。
- Desktop shortcut installerを追加。
- native shellが使えない場合はlocalhost browser consoleへfallbackする。
- 継続学習をアプリ起動中に定期実行できるようにする。
- 新しいトレード手法を一つずつ手作業で差し替えるのではなく、複数Strategy Familyを同じ検証Gateで競わせるStrategy Labを採用。
- 初期Strategy Family: EMA+RSI / EMA Cross / Breakout / Mean Reversion / Momentum。
- Strategy Lab ChampionはPaperへ自動反映可能。ただしLiveへは自動反映しない。

### v0.7 UI / UX Lab
- Human決定: 過剰でもよいので便利機能とUI/UXを積極的に試す。
- Desktop Research ConsoleをTrading Research Cockpitへ拡張。
- 4画面構成: Dashboard / Training Lab / History / Risk & System。
- bitbank Public OHLCVのローソク足表示を追加。
- Paper資産曲線、Return、Max Drawdown、判断回数、Fill、Error等の可視化を追加。
- Strategy Familyカード、Research Jobタイムライン、Operational Readinessを追加。
- Ctrl+Kコマンドパレット、Toast通知、キーボード画面切替を追加。
- 監査Snapshot JSON書き出しを追加。
- UIの便利さを積極的に追求する一方、Live安全境界は別管理し固定する。

### Fundamental Sentinel concept
- GPUなしPCで動く小型Local AIを、BBB専属のファンダメンタルズ文脈整理エージェントとして検討する。
- 情報取得はAPI / deterministic collectorで行い、Local AIへWeb探索そのものを主担当させない。
- Actual / Forecast / Previous等の単純な数値判定はアルゴリズムで処理する。
- Local AIはニュース・声明文の要約、カテゴリ分類、hawkish/dovish、risk-on/risk-off、BTC/JPY関連度、重要度、不確実性等の文脈処理を担当する。
- Local AIはBUY / SELLを直接命令しない。固定Schemaの構造化信号だけを返し、BBB側のFundamental Policy EngineがRisk調整等へ変換する。
- 判断不能時のUNKNOWN / no_overrideを正式な正常系として扱う。
- Local AI停止時もBBB本体を継続可能にし、AIなしFallbackを持たせる。
- 初期はFundamental AI Sandboxとして観測専用運用し、売買へ反映しない。
- Local AI判断とその後のBTC/JPY・USD/JPY等をFundamental Confidence Ledgerへ蓄積し、カテゴリ別にAIの有効性を検証する。
- 将来Cloud AIを利用する場合も常時稼働させず、Local AIで処理困難な案件のみエスカレーションする。
- BBBの利益が確認できた場合、利益の一部を高度なCloud AI利用費へ回すSelf-Funding AI構想を検討する。
- 機能進化と実資金運用信頼性は引き続き別軸で評価する。

