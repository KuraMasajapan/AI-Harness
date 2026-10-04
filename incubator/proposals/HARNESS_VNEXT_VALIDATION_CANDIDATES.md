# Harness vNext Validation Candidates

## Status
PROPOSAL / NOT ACTIVE

この文書は、現行AI-Harnessの運用ルールを変更するものではない。
追加で得られた知見を、次回のHarness運用見直し時に実証・検証するための候補として保持する。

作成日: 2026-10-02
最終更新: 2026-10-04

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


---

## Update 2026-10-04 — New Candidate Set

本節は2026-10-04に得られた知見を、Coreへ即導入せず、vNextの追加検証候補として保存する。
個別OSS・サービスの提供状況や仕様は変化し得るため、採用判断時には最新の公式一次情報を再確認する。

### Candidate E: Externalized Memory / Model-Swappable Architecture

Memory / Contextを特定モデル内部へ閉じ込めず、外部の永続ストアを正本として扱う。

仮説:
- モデルをClaude / Codex / ChatGPT / Local等へ差し替えても作業継続しやすい
- モデル停止・利用制限・サービス変更時のロックインを減らせる
- Humanが「どこに正本があるか」を追跡しやすい

候補となる配置先:
- GitHub: 仕様・コード・変更履歴
- Obsidian等: 個人知識
- Airtable等: 構造化された状態・承認待ち
- 必要に応じた文書ストア

検証したい点:
- モデル内部Memory中心と比べた継続性
- 外部Memory更新漏れ
- 正本の競合
- Retrieval負荷
- Humanの運用負荷

判定:
ABSORB候補。既存Candidate D Retrieval Layerと合わせて検証する。

### Candidate F: Transport / Handoff Layer

複数AI間の「人間によるコピペ運搬」を専用Transportへ分離する。

想定形:
AI A
→ Job / Message
→ Relay / Transport
→ AI B
→ Result

参考候補:
- Agent TincanのようなRelay方式
- HarnessRouter型の単一入口
- 将来のLocal AI / Cloud AI間Handoff

重要:
TransportはHarness全体の代替とは見なさない。
原則として Rule / Access / Validation / Memory / Human Approval とは別層として評価する。

検証したい点:
- Humanの運搬作業削減
- コンテキスト欠落
- 誤配送
- 権限伝播
- Prompt Injectionの横展開
- Relay停止時の復旧
- Audit可能性

判定:
EXPERIMENT候補。

### Candidate G: Idempotency / Duplicate-Execution Guard

AIが一度だけ指示したつもりでも、通信失敗・再試行・MCP障害等により外部Actionが重複実行される可能性を前提にする。

候補対策:
- Operation ID / Job ID
- 同一IDの二重実行拒否
- in-progress / completed状態
- 再試行回数上限
- 外部Action前後の状態確認
- Human承認後のActionでも冪等性を要求

重要:
「AIが二度命令しない」ことではなく「実世界で二度実行されない」ことを保証対象にする。

検証したい点:
- 二重発火シミュレーション
- Network retry
- MCP retry
- タイムアウト後の再実行
- 決済・送信・編集等の不可逆Action

判定:
ABSORB候補。Rule / Access / Validationへ跨る安全機構として独立検証する。

### Candidate H: Loop Guard / Escalation

Agentが失敗を再試行理由と誤認し、同一状態・同一Actionを繰り返す事故を防ぐ。

暫定候補:
- 同一状態へ短いステップ数で戻った場合に検知
- 同一Tool / APIの連続呼出し上限
- Cost / Token / Time上限
- 一定条件でHumanへEscalate
- 自動停止後に原因・最終状態を保存

「同一状態3ステップ」等の具体閾値は未確定であり、実証前にCore Rule化しない。

検証したい点:
- 正常な反復処理の誤停止
- 本当のLoop検出率
- Human介入タイミング
- コスト事故の抑制

判定:
ABSORB候補。

### Candidate I: Temporal Layer

AI-Harnessに時間軸を独立レイヤとして持たせる。

対象:
- Scheduled Task
- Deadline
- Reminder
- Escalation
- Re-evaluation
- Recertification
- 情報鮮度
- activity gap等の時間信号
- EventとScheduleの統合

基本仮説:
Eventは「何かが変わったから起こす」。
Temporalは「時間が来たから起こす」。

Harnessは外部Schedulerそのものを必ずしも内製せず、
外部の時刻信号を受けて何をするかを決定する層を持つ。

検証したい点:
- 外部Scheduler依存時の移植性
- 時間経過による状態遷移
- missed run
- stale情報の再検証
- Human通知過多

判定:
EXPERIMENT候補。

### Candidate J: Operational Visibility / Fleet Status UI

AIやJobを増やす場合、「何が動いているか分からない」状態を防ぐ可視化レイヤを検討する。

最低限見たい状態:
- Pending
- Waiting Human
- Running
- Failed
- Retry
- Done
- Stale / Needs Review

候補:
- Airtable Status Board
- 将来の専用Dashboard
- 既存SaaSのUIをHarnessの前面に使う

重要:
UIのためにAgent数や構造を増やさない。
可視化は実際の状態を表示するだけにする。

判定:
ABSORB候補。まずAirtable等の既存UIで十分か検証する。

### Candidate K: Adapter / Translation Layer

Harnessが全SaaSを置き換えるのではなく、人間やチームが既に使っているUI間の翻訳・同期層として振る舞う設計。

例:
Personal UI
↔ Harness Adapter
↔ Team / Required UI

仮説:
- 人間に新UIを強制しない
- 既存業務への導入障壁を下げる
- Harnessを「中央アプリ」ではなく「橋」にできる

検証したい点:
- 双方向同期Conflict
- Source of Truth
- 削除・更新権限
- 遅延・重複
- Humanがどちらを正本と理解するか

判定:
EXPERIMENT候補。

### Candidate L: Research / Evidence Layer

調査タスクを単なるWeb検索ではなく、Evidenceを組み立てる独立Pipelineとして扱う。

候補フロー:
Question
→ Split
→ Search
→ Extract
→ Link Claims
→ Cross-check
→ Cite
→ Report

目的:
「大量のSourceを集める」より、
Source間で主張が衝突したときに、どのClaimが生き残るかを検証する。

評価対象となり得るOSS群:
- GPT Researcher
- STORM
- Perplexica
- Crawl4AI
- PaperQA2
- Docling
- GraphRAG
- LightRAG

注意:
上記OSSは採用済みではない。
各Repository・Maintainer・更新状況・License・Security・Local運用可否を別途確認する。
候補群として比較する。

検証したい点:
- Source discovery精度
- Primary source優先
- Claim単位のEvidence紐付け
- Conflicting evidence処理
- Citation correctness
- PDF / Table / Long document抽出
- Graph化の実益
- Local / low-cost運用
- Trinityとの役割重複

判定:
Focused Validation候補。
Retrieval Layerより一段上の「Evidence construction」として独立評価する。

### Candidate M: Multi-Sensor Observer Architecture

情報収集元を同一役割で競わせず、媒体特性に合わせて役割分担する。

暫定分担:
- X / Grok: 技術速報、OSS、開発者報告、障害、API、新機能
- Meta系 / Meta AI: 実利用、Workflow、非エンジニア運用、普及、失敗例
- GitHub: 実物、Repository、Issue、Release
- Official Docs / Blog: 現在仕様の確認
- Reddit / Hacker News等: 実運用の反応・失敗・反論

重要:
SNSはSignalでありEvidenceではない。
採用判断前に最新のPrimary sourceへ遡る。

Observer outputの候補分類:
- KEEP
- ABSORB
- REPLACE
- EXPERIMENT
- IGNORE

REPLACE判定では、
- Harness全体
- Transport
- Memory
- Scheduler
- Rule
- Access
- Validation
- UI
等、どのLayerを置き換えるのかを必ず明記する。

判定:
現在はPILOT継続。
Observer自体をCore Ruleへ昇格しない。

## vNext Design Principle Update

AI-Harnessという名称・現在構造を守ることを目的にしない。

評価対象が、
- 現行Harnessを補強する
- 一部Layerを置き換える
- 複雑性を下げる
- Harness全体を不要にする

いずれの場合でも、実証結果が良ければ採用候補とする。

最終目的は「Harnessを完成させること」ではなく、
安全・持続・低コスト・検証可能で、Humanが最終判断を保持できるAI運用構造を見つけること。

## Prioritization After 2026-10-04

優先度 High:
1. Candidate G: Idempotency / Duplicate-Execution Guard
2. Candidate H: Loop Guard / Escalation
3. Candidate F: Transport / Handoff Layer
4. Candidate L: Research / Evidence Layer
5. Candidate E: Externalized Memory

優先度 Medium:
6. Candidate I: Temporal Layer
7. Candidate J: Operational Visibility
8. Candidate K: Adapter / Translation Layer
9. Candidate M: Multi-Sensor Observer Architecture

既存候補 A-Dは継続し、上記と統合可能かを後で棚卸しする。

## Promotion Policy Addendum

新しい候補は以下を満たすまでCoreへ昇格しない。
- Current statusを最新一次情報で確認
- 何を置き換えるCandidateかをLayer単位で明示
- Security / Access境界を確認
- Failure modeを1つ以上列挙
- Focused testまたはTrinity比較を実施
- Humanが採用 / 保留 / 棄却を判断

