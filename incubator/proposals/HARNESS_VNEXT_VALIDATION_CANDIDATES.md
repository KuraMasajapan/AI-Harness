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



---

## Update 2026-10-04 — Design Principles Extracted from Claude Code Setup Article

この節は、ユーザーが共有した記事本文から、AI-Harnessへ転用価値がある「設計思想」だけを抽出して保存する。
Claude Code固有の設定値・バージョン依存仕様・コマンド・ファイル配置を、そのままHarness標準として採用するものではない。
記事内の個別仕様は実装時に公式一次情報で再確認する。

### Principle N: Instruction Budget / Progressive Loading

常時読み込ませる指示を増やし続けない。
入口となる共通指示は短く保ち、詳細資料は用途と参照先を明示して必要時に読む。

狙い:
- Context肥大化の抑制
- 重要Ruleの埋没防止
- モデル変更時の移植性向上
- 長時間作業での指示欠落を減らす

考え方:
- 常時: 目的 / 境界 / 完了条件 / 参照先
- 必要時: 背景 / 長い手順 / 過去事例 / 詳細資料

既存Candidate D Retrieval Layerと接続して評価する。

### Principle O: Executable Validation Before AI Judgment

機械で判定できる項目を、AIの自己評価だけに任せない。

例:
- JSON / YAML等の構文
- 必須ファイルの存在
- import / 参照先
- 重複
- 循環
- build / test / diff check
- 設定整合

考え方:
AI review
≠
deterministic check

機械的検査で確認できるものは先に自動判定し、
意味・妥当性・根拠の質など、機械判定できない部分をAI / Trinityへ渡す。

Candidate C Definition of DoneとCandidate G/Hの安全機構を補強する候補。

### Principle P: Capability-Separated Reviewer

作成役と確認役を役割だけで分けるのではなく、可能なら権限も分ける。

基本形:
- Builder: 必要なWrite / Execute権限
- Reviewer: Read中心
- Human: 最終承認

Reviewerに不要な編集・公開・送信・外部変更権限を持たせない。

狙い:
- Reviewerが指摘と同時に勝手に修正するのを防ぐ
- 独立性をPromptだけでなくAccessで補強する
- Trinity等の独立検証とAccess Separationを接続する

既存Candidate B Rule / Access Separationとの統合候補。

### Principle Q: Failure → Durable Improvement

失敗をその場の注意で終わらせない。
再発した失敗は、原因に応じて適切な層へ反映する。

反映先の例:
- Rule不足 → Rule候補
- 手順不足 → Skill / Workflow候補
- 機械的見落とし → Check / Validator候補
- 資料不足 → Retrieval / Reference候補
- 権限事故 → Access候補

重要:
失敗を検出したAIが自動でCore Ruleを書き換えるのではない。
Proposal
→ Validation
→ Human判断
→ Promotion
の流れを維持する。

これはHarnessを「経験を蓄積する仕組み」にするが、
自己変更の暴走は防ぐ。

### Principle R: Idempotent Harness Configuration

Harness自身のセットアップ・設定更新にも冪等性を要求する。

同じセットアップや修正指示を複数回実行しても、
- Ruleが重複しない
- Hookが重複しない
- Folderが増殖しない
- 同じ設定項目が二重登録されない
- 既存の意味を壊さない

ことを目標にする。

Candidate G Idempotencyを外部Actionだけでなく、
Harness configuration / migrationへ拡張する。

### Principle S: Reversible Changes / Local Rollback

AIが設定を変更する場合、今回の差分だけを復元可能にする。

狙い:
- 大きな破壊的Rollbackを避ける
- 未コミット変更を巻き込まない
- Humanが変更単位を理解できる
- Pilot / Experimentを安全に戻せる

禁止方向:
- reset --hardのような広域破壊
- 無関係な既存設定の上書き
- 原本の勝手な移動

Experiment系Candidateの共通安全要件として扱う。

### Principle T: Model-Neutral Core + Model-Specific Adapter

共通の設計思想と、特定AI製品の機能を分離する。

共通Coreの候補:
- Rule
- Access
- DoD
- State
- Evidence
- Memory / Retrieval
- Validation
- Handoff

製品固有Adapterの候補:
- Claude CodeのRules / Skills / Hooks / Subagents
- Codex固有設定
- ChatGPT / Work固有機能
- Local AI固有設定

原則:
HarnessをClaude Code化しない。
Claude CodeをHarnessに接続する。

同様に、他モデルでもCoreを変えずAdapterだけ差し替えられる構造を目指す。

Candidate E Externalized Memory / Model-Swappable Architectureと強く関連する。

### Principle U: Separate Content Quality from Configuration Integrity

「設定が壊れていないこと」と「成果物の内容が良いこと」を同じ検査にしない。

例:
- Configuration integrity:
  構文、参照、重複、Hook登録、ファイル存在
- Content quality:
  根拠、正確性、完成条件、可読性、依頼適合

前者は軽量な自動検査、
後者はAI review / Trinity / Human reviewへ分離する。

これによりStop Hook等の機械チェックが、
成果物品質の誤った代理指標になるのを防ぐ。

### Principle V: Minimal Change / Preserve Existing Structure

AIによる環境整備では、「理想構成へ全面移行」より既存構成を尊重する。

原則:
- 同等構成が既にあれば再利用
- 原本を勝手に移動しない
- 未知の設定キーを削除しない
- 既存Hookや配列を丸ごと置換しない
- 小さな変更に大規模再編を持ち込まない

Harness導入コストと既存運用破壊を減らすための共通原則として候補化する。

## Article-derived Design Decision

この記事から採用候補とするのは、Claude Code固有の「神設定」そのものではない。

保存する中核思想は以下:
1. 短い入口 + 必要時Retrieval
2. 機械判定可能な項目はExecutable Validationへ
3. Reviewerは役割だけでなくAccessも分離
4. 失敗を再利用可能な改善候補へ変換
5. Harness自身の設定変更も冪等・可逆にする
6. Model-neutral CoreとModel-specific Adapterを分ける
7. Configuration integrityとContent qualityを別検査にする
8. 既存構成を尊重し最小変更で統合する

Status:
PROPOSAL / NOT ACTIVE

これらは既存Candidate B / C / D / E / G / Hと重なる部分が多いため、
新しいCoreを増やす前に統合可能性を確認する。


---

## Update 2026-10-04 — Human Interface / Action-First Output

この節は、ユーザーが共有した `i-have-adhd` Skillの紹介文から、AI-Harnessへ転用価値がある設計思想だけを抽出して保存する。
ADHD向けという名称・対象ユーザー分類そのものは採用せず、Human Interface設計として一般化する。

### Principle W: Action-First Output

AIの内部処理量とHumanへ見せる情報量を分離する。

基本順序:
1. 結論
2. 次にやること
3. 必要な手順
4. 必要な場合だけ詳細・根拠

狙い:
- Humanが次の判断をすぐ行える
- 長文説明による判断遅延を減らす
- 「どこまで進んだか」「次に何をするか」を見失いにくくする
- Human-in-the-loopを実運用しやすくする

重要:
短くすること自体を目的にしない。
詳細が必要なTaskではEvidenceやRiskを省略しない。

### Principle X: Progressive Disclosure for Human Review

Humanへ最初から全情報を出さず、判断に必要な情報を優先して提示する。

候補UI:
- Summary: 結論 / Current State / Next Action
- Expand: Evidence / Risk / Alternatives / Full Details

仮説:
AIは深く処理してよいが、Humanの認知負荷は必要最小限に保つ。

これはCandidate J Operational Visibility / Fleet Status UIと接続して評価する。

### Principle Y: Output Mode by Task Type

すべてのTaskを同じ出力形式に固定しない。

暫定モード:
- Action Mode:
  結論 → 次Action → 必要手順
- Evidence Mode:
  結論 → Evidence → 不確実性 → 次Action
- Decision Mode:
  選択肢 → 推奨 → Risk → Human承認点
- Review Mode:
  問題 → 対象箇所 → 理由 → 修正候補

Harness側でTask種別またはHumanの目的に応じて出力Contractを切り替える。

### Human Interface Design Decision

保存する中核思想:
- AIの思考量とHumanへの表示量は別物
- Humanには「次に押すハンコ」が分かる形で出す
- 詳細は必要時に展開する
- 重要Taskでは短さのためにEvidence / Riskを削らない
- UI / Output Contractとして扱い、Core reasoningやValidationを弱めない

Status:
PROPOSAL / NOT ACTIVE

候補位置づけ:
- Candidate J Operational VisibilityのHuman-facing output版
- Human-in-the-loopの負荷削減策
- Trinity / Validation結果の提示形式としても検証可能
