# BBB v0.8.8 Fundamental Confidence Dashboard — Checkpoint
Date: 2026-10-02

## Goal
100件Historical Replayの結果からSokudanのカテゴリ別傾向をすぐ見えるようにする。

## Implemented
- Existing historical confidence ledgerを追加推論なしで再分析。
- Overall:
  - Scored Cases
  - 24H Alignment
  - Avg |Move|
  - Evidence Stage
- By Category:
  - events
  - scored
  - alignment rate
  - average absolute 24h move
  - average model minimum confidence
  - sample stage
- Largest Aligned Cases: 最大5件
- Largest Misses: 最大5件
- moved install pathに対するledger fallback lookup。

## Interpretation boundary
24H AlignmentはHuman labelによるAI classification accuracyではない。
risk_on/risk_offと24時間後BTC/JPY return signの一致率のみ。
今後Human case labelsを追加して、文章分類精度と市場方向一致を分離評価する。

## Validation
- pytest: 60 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- flat ZIP root: PASS
- packaged ZIP extraction + pytest: 60 passed
- package: BBB_v0.8.8_Fundamental_Confidence_Dashboard.zip
- SHA-256: aeae977c337d315f0a749710df72619d76a63c10dee83d690a199b506f8fdb93

## Safety
Read-only analytics only.
No Paper / Risk / Live behavior change.
