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

### Security
- API Key / SecretをChatGPTへ貼らない。
- API Key / SecretをGitHub / AI-Harnessへ保存しない。
- 将来Live時はPC側の環境変数またはSecret Storeで保持。
- BBB用APIには出金権限を与えない方針。
- 実注文開始前にLive Trading Gateを設ける。

### Logging policy
- BBBの重要決定・仕様変更・検証状態をAI-Harness内にも継続記録する。
- 秘密情報と大量の実取引生ログはHarnessへ直接保存せず、要約・Checkpoint・検証結果を記録する。
