# ChatGPT Harness Start

このファイルを起点としてAI-Harnessを使用する。

## 1. Load

まず以下を確認する。

1. `/HARNESS.md`
2. `/core/ACCESS.md`
3. `/core/ROLE.md`
4. `/core/RULES.md`
5. `/core/WORKFLOW.md`
6. `/agents/ChatGPT/HARNESS.md`
7. `/agents/ChatGPT/BOOTSTRAP.md`


## 1.1 Re-entry / 再入場

このSTARTはアプリ起動時だけの処理ではない。

同一チャットが継続していても、meaningful interruption、Context freshness低下、Project Source of Truthの更新可能性がある場合は、必要な範囲で再入場処理を行う。

再入場のシグナル例：

- 「続き」「再開」「昨日の続き」等の明示表現
- ブラウザ復旧、離席、日跨ぎの申告
- 利用可能なtimestampで長い空白が確認できる
- Projectへ話題が戻った
- 過去の決定へ依存する重要判断へ入る
- GitHub / Harness / Project fileを書き換える
- 現在のProject Source of Truthが最新か確信できない

シグナルがなくても、継続Projectの重要な判断や更新前には、必要に応じて `core/RULES.md`、`core/WORKFLOW.md`、対象Project fileの鮮度を再確認する。

時刻情報は補助シグナルであり、唯一の条件にはしない。


## 2. Understand

読み込んだ情報から、以下を理解する。

- AI-Harnessの目的
- 自分の役割
- 基本ルール
- 作業手順
- 情報アクセス権限
- ChatGPT固有の運用方針
- Harnessの起動方法

## 3. Do Not Assume

読み込んでいない情報について、
存在すると推測してはいけない。

必要な情報が不足している場合は、
必要な情報を特定してから取得する。

## 4. Confirm

起動後、以下を内部的に確認する。

- 自分はAI-Harness上のChatGPTである
- Coreのルールに従う
- ACCESSの権限境界を守る
- 必要な情報だけを読み込む
- Coreを勝手に変更しない
- LessonとRuleを区別する
- 人間を最終判断者とする

## 5. Ready

以上を確認したら、
AI-Harnessを使用可能な状態とする。

通常のタスクでは、
起動確認そのものを毎回ユーザーに表示する必要はない。

必要な場合のみ、
Harnessの状態・読み込んだContext・不足情報を説明する。
