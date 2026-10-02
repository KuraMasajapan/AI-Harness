# Harness vNext Validation Candidates

## Status
PROPOSAL / NOT ACTIVE

この文書は、現行AI-Harnessの運用ルールを変更するものではない。
追加で得られた知見を、次回のHarness運用見直し時に実証・検証するための候補として保持する。

作成日: 2026-10-02

## Purpose
AI-Harness運用開始後に蓄積した新しい知見を、思いつきで即導入せず、現行Harnessを基準として比較検証する。

特にTrinity実行と組み合わせ、
- 本当に品質が上がるか
- 欠落が減るか
- 誤判断や手戻りが減るか
- Human確認負荷が減るか
- トークン・時間・複雑性に見合うか

を確認してから、Rule / Workflow / Access等への昇格を判断する。

## Candidate A: Persistence Class
重要情報を「重要度」だけでなく「どの程度、欠落してはいけないか」で分類する。

暫定例:
- P0: 絶対に失ってはいけない
- P1: 作業中ずっと必要
- P2: 必要時に再取得できればよい
- P3: 履歴・参照用

検証したい点:
- 長時間作業や文脈圧縮後の欠落率
- P0/P1情報の配置先が妥当か
- 欠落発生時にTrinityが検出できるか
- 意図的な欠落注入テストが有効か

注意:
分類名・段階数・配置先は未確定。実証後に決める。

## Candidate B: Rule / Access Separation
「守ってほしい指示」と「実際に実行できない強制境界」を分離する。

考え方:
- Rule: 意図、方針、判断基準
- Access: 権限、禁止、読み書き可能範囲

検証したい点:
- Ruleだけの場合とAccess制御を加えた場合の逸脱率
- 誤操作防止効果
- 権限制限による作業停止・過剰制約の増加
- Human承認が必要な境界の適切さ

## Candidate C: Definition of Done
AIの「終わりました」という自己申告ではなく、外部から確認可能な完了条件をTask開始時に定義する。

例:
- build PASS
- tests PASS
- diff check PASS
- 必須成果物が存在
- 禁止された次Layerへ進んでいない

検証したい点:
- 未完了の誤完了報告が減るか
- Checkpointとの重複・統合可能性
- Human確認回数が減るか
- 完了条件が過剰にならないか

## Candidate D: Retrieval Layer / External Connectors
「全部をAIに覚えさせる」だけでなく、「必要なときに信頼できる情報源から取得する」構造を検証する。

候補となる情報源の例:
- 論文・研究: alphaXiv等の研究Connector / MCP
- コード: GitHub
- 個人・チーム資料: Drive等
- 個人知識: Obsidian
- 最新公開情報: Web

基本仮説:
Memory中心だけでなく、
Memory + Retrieval
の役割分担にすると、記憶欠落を補いながらコンテキスト量を減らせる可能性がある。

検証したい点:
- Memoryだけの場合との正答率・根拠品質差
- 必要情報の取得漏れ
- Retrieval結果の信頼性
- 取得元の優先順位
- Connector追加による複雑性・権限リスク
- トークン量と処理時間
- 重要結論だけをHarness / Obsidianへ昇格する運用の有効性

### Connector Policy Candidate
大量導入を前提にしない。

まずは以下を分けて評価する。
1. Read-oriented Connector
   - 検索、参照、取得中心
   - 比較的積極的に試験可能
2. Write / Action Connector
   - 編集、削除、送信、決済、外部変更
   - Access設計とHuman承認を先に検証する

alphaXivは特定サービスへの依存を意味せず、「専門情報源へ直接Retrievalする方式」の代表例として扱う。

## Trinity Validation Plan
現行HarnessをBaselineとし、候補を一度に本番導入しない。

推奨比較:
- Baseline: 現行Harness
- Variant A: Persistence Class追加
- Variant B: Rule / Access分離強化
- Variant C: Definition of Done明示
- Variant D: Retrieval Layer追加
- Combined: 効果が確認できた候補のみ組み合わせる

Trinityでは通常の成果物比較に加え、以下を観測する。
- 欠落した情報
- 欠落を検出できたか
- 誤判断
- 根拠の質
- 手戻り
- Human介入回数
- Task完了までのターン数
- トークン / 時間
- 外部情報取得回数
- Access逸脱・停止
- 検証自体の負荷

## Missing-Information Injection Test
Persistence Class検証時には、意図的に重要情報を1つ抜いたTask Packageを用意する案を検討する。

確認項目:
- Analystが欠落に気づくか
- Comparatorが差異として検出するか
- 誤った補完をしないか
- P0/P1として配置していれば防げた欠落か

既存Trinityのsealed boundaryや現行結論は変更せず、独立した検証Runとして扱う。

## Promotion Policy
候補は、実証結果なしにCoreへ昇格しない。

想定フロー:
Proposal
→ Focused Validation
→ Trinity比較
→ Review
→ 採用 / 棄却 / 保留
→ 必要な場合のみRule / Workflow / Accessへ反映

## Current Decision
- 今すぐ現行Harnessを再設計しない。
- 追加知見が十分に蓄積した段階でHarness全体を棚卸しする。
- その際、この文書をvNext検証候補一覧として使用する。
- Plugin / Connector / Retrievalも、便利そうという理由だけでは採用せず、実証してから判断する。
