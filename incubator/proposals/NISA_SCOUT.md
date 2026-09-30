# NISA Scout Proposal

## Purpose
NISA向けの長期投資支援Bot。仮想通貨Botとは分離し、頻繁な売買ではなく、成長テーマの発掘・企業分析・監視・買い場待ちを主目的とする。

## Core Operating Model
1. 成長業界・構造変化を探索
2. 関連する国内上場企業を抽出
3. 財務、受注、シェア、競争優位、バリュエーション、リスクを確認
4. 投資仮説を作成
5. WATCH / WAIT / BUY CANDIDATE / HOLD / REVIEW で状態管理
6. 買い条件成立時にHumanへ通知
7. 初期版ではHumanが最終承認して発注
8. 決算・適時開示ごとに当初の投資仮説を再検証

## Execution Policy
- 初期版は完全自動発注しない。
- AIは探索、分析、監視、購入候補金額の算出まで担当。
- 最終発注はHumanが行う。
- 将来、API対応証券をExecution口座として追加する余地を残す。

## PayPay Securities Fit
PayPay証券の「100円以上・1円単位の金額指定買付」を活用する。

例:
- 最有力: 150,000円
- 有力: 80,000円
- 試し: 20,000円
- 観察: 5,000円

AIの確信度・評価を、株数ではなく投資金額へ変換する設計とする。

現時点では一般向け公開取引APIを前提にせず、PayPay証券ではHuman発注を基本とする。

## Evaluation Axes
- Theme
- Growth
- Orders / Backlog
- Moat
- Valuation
- Catalyst
- Risk
- Price
- Evidence quality

## AI Call Policy
常時AIを動かさない。
通常時は価格・出来高・指標をコードで監視し、以下のようなイベント時のみAIを起動する。
- 大幅下落
- 決算発表
- 適時開示
- 受注急増
- 新テーマ発生
- 投資仮説に関わる重要ニュース

## Record Separation
- AI-Harness: 判断ルール、検証方法、失敗事例、運用設計
- Obsidian: 銘柄、テーマ、投資仮説、調査メモ、結果、振り返り

## Key Principle
「良い会社を見つける」だけではなく、「良い会社を高値で買わない」ことを重視する。
NISA Scoutは売買Botではなく、長期の発掘・監視・仮説検証システムとして扱う。
