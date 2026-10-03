# Crypto Bot Event-Driven Trigger Handoff

## Purpose
仮想通貨取引Botで、AIを常時動かさず、イベント発生時だけ必要な処理を起動するための設計メモ。

## Core Idea
通常時はコードで監視し、条件成立時だけTriggerを発火させる。

```
Market / News / Schedule
        ↓
      Event
        ↓
     Trigger
        ↓
    Condition
        ↓
   Pending Job
        ↓
  Human Approval
        ↓
 AI Analysis / Action
```

## Recommended Initial Use
最初は自動売買ではなく「上申型」にする。

例:
- 価格が一定幅以上変動
- 出来高急増
- 決算・重要ニュース
- 経済指標発表
- Bot内部の異常
- 売買条件候補の成立

Trigger発火後は、AIがすぐ売買するのではなく、
「何が起きたか」「なぜ重要か」「推奨する次の処理」をJobとしてまとめる。

Humanが以下を選ぶ:
- 承認
- 保留
- 却下

## Cost Policy
OpenAI APIを常時呼ばない。
通常監視はPython等の通常コードで行い、重要イベント時だけAIを使う。

ChatGPT Plus内で処理できる範囲はPlusを優先し、追加API課金は最小化する。

## Future Extension
将来的には以下を段階的に追加可能。

1. Event / Trigger
2. Pending Job
3. Human Approval
4. AI一次分析
5. Trinity / Evaluator
6. 安全性が確認できた処理だけ自動実行

## Important Principle
最初に自動化するのは「売買」ではなく、
**仕事を見つけて、整理して、Humanへ上申するところ**。

完全自動化は、実証・検証後に限定範囲から行う。
