# BBB Fundamental Sentinel Concept

Date: 2026-09-29
Status: CONCEPT / NOT IMPLEMENTED
Project: BITBANK-BOT (BBB)

## 1. Purpose
BBBへファンダメンタルズ要因を取り込むため、GPUを搭載していない現在のWindows PC上で動作する小型Local AIを「専属エージェント」として利用する構想。

ただしLocal AIへ直接売買判断を任せない。
役割は、API等で取得した文章情報の文脈整理・分類・要約に限定し、その出力をBBB側の決定論的アルゴリズムが取引上の指示へ変換する。

## 2. Basic responsibility split

External APIs / structured feeds
-> Collector
-> deterministic normalization / simple numeric judgment
-> Local AI Fundamental Sentinel
-> structured context signal
-> Fundamental Policy Engine
-> BBB Risk Manager / Strategy
-> Paper (future Live only through Live Gate)

### API / deterministic code
担当:
- 経済指標のActual / Forecast / Previous取得
- 発表時刻
- 数値差分計算
- 重複除去
- 時刻・単位統一
- 明確な閾値判定
- ニュース本文・見出し取得

構造化数値だけで判断可能なものはAIへ渡さない。

### Local AI
担当:
- ニュース・声明文の分類
- 短い要約
- 文脈理解
- monetary_policy / inflation / geopolitical / crypto 等のカテゴリ分類
- hawkish / dovish / neutral / unknown
- risk_on / risk_off / neutral / unknown
- BTC関連度
- USD/JPY関連度
- 重要度
- confidence / uncertainty
- 有効時間(TTL)候補

Local AIは「BUY / SELL」を直接出さない。
判断不能時にUNKNOWN / no_overrideを正式な正常出力として許可する。

## 3. Fundamental Policy Engine
Local AIの曖昧な自然言語出力をそのままStrategyへ渡さない。
JSON等の固定Schemaで受け取り、BBB側の決定論的ルールへ変換する。

例:
- high-impact event + high uncertainty -> 新規Entry一時停止
- high risk + sufficient confidence -> order size縮小
- low confidence / unknown -> no override
- event終了 / TTL超過 -> 通常状態へ復帰

Risk ManagerとLive Gateが最終権限を保持する。

## 4. GPU-less operating policy
現在のPCにはGPUがないため、Local AIは常時推論させない。

方針:
- 小型量子化LLMをCPU実行候補とする
- 1B〜数B級程度を初期候補とする
- Event-drivenで必要時のみ起動
- 複数記事をまとめて分類可能にする
- 推論後は待機
- 長文生成や複雑な市場予測は担当させない

Local AIを高度な経済評論家ではなく、「文章をBBB向け構造化信号へ変換するセンサー」として扱う。

## 5. Three-level processing model

### Level 0: Deterministic
数値・時刻・既知イベントは通常コードで処理。
AI不要。

### Level 1: Local AI
文章の意味整理、分類、関連性判定。
原則ここまでをローカルPCで処理。

### Level 2: Cloud AI (future)
複数要因が矛盾する、地政学的に複雑、Local AI confidenceが低い等の難しい案件だけ必要時にCloud AIへエスカレーション。

Cloud AIは常時利用しない。
将来BBBの利益が確認できた場合、利益の一部を高度なAI利用費へ回す Self-Funding AI 構想を検討する。

## 6. Safety boundary
- Local AI停止時もBBB本体は動作可能にする
- AIなしFallbackを持つ
- AI出力を直接注文へ接続しない
- Local AIからLiveへの直接経路は禁止
- Research ChampionからLiveへの自動昇格禁止を維持
- Human承認とLive Trading Gateを維持
- API Secret等はAIへ渡さない

## 7. Fundamental AI Sandbox
初期導入ではLocal AI判定を売買へ反映しない。

Phase A:
ニュース分類・要約のみ
-> 保存
-> Human確認
-> 実際のその後の相場と比較

十分な履歴を蓄積後に、分類精度・用途別有効性を評価してからRisk調整へ接続する。

## 8. Fundamental Confidence Ledger
Local AIの判断と、その後の実相場を記録する。

例:
- event category
- AI classification
- importance
- confidence
- timestamp
- BTC/JPY subsequent move
- USD/JPY subsequent move
- volatility response
- useful / false alarm / unknown

目的:
モデル名や印象でAIを信用せず、BBB内部の実績から
「どの種類のニュース分類ならどの程度信用できるか」
を評価する。

将来:
- CPIには強い
- FOMC声明分類には強い
- 地政学ニュースには弱い
等、カテゴリ別の信頼度をPolicy Engineへ反映可能にする。

## 9. UI concept: Fundamental Desk / Watch
Dashboard候補:

- Local AI status: ONLINE / SLEEP / OFFLINE
- Current Fundamental Risk: NORMAL / CAUTION / HIGH
- Next major event
- Last analysis time
- Local AI summary
- BBB action / override
- TTL / next re-evaluation
- Cloud escalation: NONE / REQUESTED / COMPLETED

重要なのは「なぜBBBが慎重になっているのか」をHumanが見て理解できること。

## 10. Development principle
BBBの機能進化と実資金運用信頼性は別軸で扱う。

Fundamental Sentinelは面白い機能として積極的に研究するが、
Live利用可否はPrivate API、reconciliation、安全機構、長期検証、独立監査等のOperational Readinessで別途判定する。

## 11. Current conclusion
採用する基本構想:
- 情報取得 = API / deterministic collector
- 単純指標 = deterministic algorithm
- 文脈理解 = Local AI
- 取引上の変換 = deterministic Fundamental Policy Engine
- 最終安全判断 = BBB Risk Manager / Live Gate
- Cloud AI = 将来の難案件だけ
- Local AI = 専属だが権限の限定された Fundamental Sentinel

Status remains CONCEPT. No current v0.7.1 live/paper behavior is changed by this document.
