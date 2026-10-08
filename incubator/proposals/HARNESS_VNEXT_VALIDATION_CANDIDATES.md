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


---

## Update 2026-10-04 — Event-driven X Push Sensor Candidate

### Candidate: Angelic Angel / Event-driven External Observer

Source:
- https://github.com/sh1ma/Angelic-Angel
- Rust / MIT
- Repository description: browser Web Push emulation for streaming X/Twitter notifications

Observed architecture:
- emulate a browser Web Push client
- register a push subscription with Mozilla AutoPush
- register that endpoint with X/Twitter notification settings
- receive notifications over WebSocket
- decrypt Web Push payloads
- forward decrypted payloads to a configured Webhook

Potential Harness role:

`External Event -> Trigger -> Condition -> Job -> Human / AI-Harness`

This differs from the current Grok observer pattern:

`Temporal signal (18:00) -> Grok searches X -> Airtable -> ChatGPT -> Human`

Angelic Angel suggests an additional event-driven path:

`followed / notification-enabled X account posts -> Web Push -> Angelic Angel -> Webhook -> Harness event`

Important distinction:
- Grok remains useful for broad discovery across X, including unknown people, ideas, and anomalies.
- Angelic Angel would be suitable only for a curated watchlist of accounts already followed with X post notifications enabled.
- Therefore this is not a direct Grok replacement candidate.

Potential value:
- near-real-time detection instead of scheduled polling
- natural fit with Event / Trigger / Condition design
- low-latency observation of high-priority accounts or projects
- could complement Temporal Layer with a true external Event source

Potential role split:
- Grok = broad X discovery / unknown-signal search
- Angelic Angel = curated real-time push sensor
- Airtable = structured Inbox / Human review boundary
- ChatGPT = downstream verification
- Human = final authority

Risks / trade-offs:
- requires X session credentials (`auth_token` and `ct0`) stored locally
- uses X internal notification API behavior rather than an official developer streaming API
- may break if X changes browser notification internals
- account / security / terms-of-service implications must be reviewed before any live use
- event volume and duplicate handling require explicit limits
- Webhook endpoint becomes a new trust boundary
- Event-driven immediacy may increase noise and Human notification pressure

Validation questions:
- Does it still work reliably with current X behavior?
- Can it operate from an isolated local environment with least privilege?
- What exact data is contained in the push payload?
- Can Webhook intake be authenticated and rate-limited?
- Can Event IDs be made idempotent?
- How should duplicate posts / reconnect replay be handled?
- What is the real account-security risk of holding `auth_token` / `ct0`?
- Does the real-time benefit justify the operational and policy risk?
- Would a simpler official source or periodic Grok run be sufficient?

Suggested action:
EXPERIMENT / HOLD.

Do not deploy now.
Keep as a future Event Layer validation candidate.

Architectural significance:
This is a concrete implementation example for the emerging distinction:

- Temporal Layer = "time arrived, so evaluate"
- Event Layer = "external world changed, so evaluate"

The combination could eventually support:

`Temporal + Event -> Trigger -> Condition -> Job -> Human Approval -> Harness`

Status:
PROPOSAL / NOT ACTIVE


---

## Update 2026-10-04 — External Collection / Retrieval Stack Candidates

This section records three OSS candidates as future comparison targets for the Observer / Retrieval layer.
They are not approved for deployment and should not all be installed by default.

### Candidate: Agent-Reach / Sensor & Retrieval Router

Source:
- https://github.com/Panniantong/Agent-Reach

Observed role:
- capability layer above individual collection tools
- selects, installs, diagnoses, and routes to platform-specific backends
- supports Web, YouTube, RSS, GitHub, X, Reddit and other sources
- uses ordered primary / fallback backends per platform
- provides `agent-reach doctor` for reachability and configuration checks

Potential Harness role:
- Sensor Adapter / Retrieval Router
- abstract platform-specific collectors behind a swappable routing layer
- reduce direct coupling between Harness and one specific scraper / CLI / API

Potential value:
- backend replacement without redesigning the whole Harness
- multi-source collection with graceful fallback
- explicit health checks for each source path
- strong fit with Model-neutral Core + Adapter and Multi-Sensor Observer concepts

Risks / trade-offs:
- some channels require cookies or existing browser login state
- account-ban / platform-policy risk exists for scripted access
- dependency chain is broad and may increase operational complexity
- upstream tools can change independently
- should not become a mandatory monolithic dependency

Suggested action:
EXPERIMENT / HOLD.

Use primarily as an architectural reference for a pluggable Sensor / Retrieval Router before considering installation.

### Candidate: Scrapling / General Extraction & Crawl Engine

Source:
- https://github.com/D4Vinci/Scrapling

Observed role:
- adaptive scraping framework from single-page fetch to full crawling
- HTTP and browser-based fetchers
- dynamic-page support, sessions, concurrent crawling, pause/resume
- proxy rotation and blocking detection
- adaptive element relocation when site structure changes
- `capture_xhr` support for capturing matching XHR / fetch responses
- MCP server and Agent Skill support

Potential Harness role:
- Extraction Engine behind the Retrieval layer
- structured collection from dynamic pages and site-internal API responses
- candidate engine when simple Web / official API / connector retrieval is insufficient

Potential value:
- one engine can cover page extraction, crawl, browser, and XHR capture
- useful for evidence collection from sources without clean APIs
- can feed structured data into downstream verification instead of raw browser pages

Risks / trade-offs:
- anti-bot / stealth features increase policy, account, and operational risk
- heavier than simple HTTP / connector retrieval
- browser and proxy operation can add cost and maintenance
- overlap exists with other collectors; avoid duplicate stacks

Suggested action:
EXPERIMENT / HOLD.

Prefer simpler official APIs, connectors, Jina-style readers, or direct retrieval first. Consider Scrapling only when those are insufficient.

### Candidate: Patchright Enhanced / Browser Fallback

Source:
- https://github.com/whaleyxbt/patchright-enhanced

Observed role:
- lightweight wrapper around Patchright
- creates stealth-oriented Chrome sessions
- intended for sites with WAF / anti-bot friction
- relies mainly on Patchright's built-in stealth patches rather than providing a separate extraction framework

Potential Harness role:
- last-resort Browser Transport / Fallback
- support collection flows where ordinary browser automation or direct HTTP access fails

Important distinction:
- this is not the preferred general extraction engine
- network interception / data extraction can be built on browser automation, but this repository's primary value is stealth browser session setup

Risks / trade-offs:
- highest policy / account / anti-bot risk among these three candidates
- brittle against site-defense changes
- easy to overuse when a simpler retrieval method would work
- should remain isolated from core Harness logic

Suggested action:
HOLD.

Do not standardize this path. Keep only as a fallback candidate for tightly scoped experiments.

### Provisional role split

`Agent-Reach = source routing / backend selection`

`Scrapling = extraction / crawling / XHR capture`

`Patchright Enhanced = stealth browser fallback`

Combined with the previously recorded Angelic Angel candidate:

`Angelic Angel = curated X real-time Event Sensor`

`Grok = broad X discovery`

`Agent-Reach = multi-source Retrieval Router`

`Scrapling = generalized Extraction Engine`

`Patchright Enhanced = difficult-site Browser Fallback`

Architectural principle:
Do not install every collector simply because it is available.
Prefer the simplest reliable path, keep adapters replaceable, and escalate only when a lower-complexity route fails.

Validation questions:
- Which capabilities are actually missing from current Web / GitHub / connectors?
- Can Agent-Reach's routing design be reused without adopting its whole dependency stack?
- Does Scrapling materially improve evidence quality versus simpler retrieval?
- What failure / maintenance burden appears after site changes?
- Can credentials and browser state be isolated with least privilege?
- Are terms-of-service / account risks acceptable for each target source?
- Can each collector be removed without changing Core Harness logic?

Status:
PROPOSAL / NOT ACTIVE


---

## Update 2026-10-05 — Durable Agent Recovery / State Survival Candidates

This section records the architectural lesson extracted from a 10-project durable-agent OSS roundup.
The projects are comparison targets, not approved dependencies.
Before adoption, current licensing, maintenance status, security posture, and official documentation must be rechecked.

### Core lesson: Design for recovery, not perfect execution

The useful principle is not "prevent every failure."
Long-running AI work should assume that tool calls, workers, browsers, networks, APIs, and models can fail.

Target recovery loop:

`Task -> Execute -> Failure -> Inspect -> Restore State -> Idempotency Check -> Retry / Compensate / Escalate Human -> Validate -> Continue`

Important:
- durable execution, persistent memory, failure isolation, and observability are different layers
- do not solve all four by adding one large framework
- completed work should not be repeated after restart
- external side effects must be checked for idempotency before retry
- Human escalation remains available when automatic retry is unsafe

This directly connects to existing Candidates C, E, G, H, I and J.

### Category A: Durable Execution / Workflow Recovery

#### Temporal
Source:
- https://github.com/temporalio/temporal

Role:
- durable workflow execution
- reconstruct workflow state from persisted execution history after process / worker failure
- strong reference architecture for long-running execution

Harness position:
REFERENCE / EXPERIMENT.

Use primarily as a benchmark for what "durable execution" should guarantee.
Likely heavier than needed for the current personal Harness unless runtime complexity grows substantially.

#### Inngest
Source:
- https://github.com/inngest/inngest

Role:
- step-oriented durable execution
- event / schedule / API triggers
- retries, waits, and long-running workflows
- useful conceptual fit for Human approval waits and resumable agent steps

Harness position:
HIGH-PRIORITY EXPERIMENT candidate.

Why important:
Its execution model maps closely to the emerging Harness flow:

`Event / Temporal -> Trigger -> Job -> Step -> Wait Human -> Resume -> Validate`

Also relevant to Candidate G because retries around external side effects require idempotency protection.

Caution:
Server / CLI licensing should be reviewed separately from SDK licensing before any self-hosted adoption.

#### Hatchet
Source:
- https://github.com/hatchet-dev/hatchet

Role:
- orchestration for long-running tasks
- retries, schedules, event / webhook triggers, pause / resume, monitoring
- Postgres-backed durability

Harness position:
HIGH-PRIORITY EXPERIMENT candidate.

Potential comparison:
Inngest vs Hatchet as a lighter-weight practical runtime layer before considering Temporal-scale infrastructure.

#### LangGraph
Source:
- https://github.com/langchain-ai/langgraph

Role:
- checkpoint / resume for graph-based agent workflows
- persistence around graph super-steps
- can preserve completed progress across interruptions

Harness position:
REFERENCE / EXPERIMENT.

Important:
Do not rebuild the Harness around graph orchestration just to gain checkpointing.
First evaluate whether checkpoint / pending-write / resume patterns can be absorbed independently.

#### Prefect
Source:
- https://github.com/PrefectHQ/prefect

Role:
- retries, scheduling, workflow state, observability and recovery for Python workflows

Harness position:
LOWER-PRIORITY REFERENCE.

Useful as a mature workflow-recovery comparison, but less directly agent-specific than Inngest / Hatchet / LangGraph.

### Category B: Persistent Memory / Cross-session State

#### Letta
Source:
- https://github.com/letta-ai/letta
- active source location should be rechecked before future testing

Role:
- stateful agents with persistent memory across sessions
- memory architecture worth studying separately from runtime durability
- Git-backed / file-oriented memory ideas are especially relevant to Externalized Memory

Harness position:
MEMORY RESEARCH / EXPERIMENT.

Potential value:
- explicit durable memory artifacts
- versioned state / rollback concepts
- separation from ephemeral chat context

Important:
Persistent memory is not the same as execution checkpoint state.

#### Mem0
Source:
- https://github.com/mem0ai/mem0

Role:
- extracted / retrieved persistent memory across runs and sessions

Harness position:
LOWER-PRIORITY MEMORY REFERENCE.

Caution:
Automatic memory extraction can still omit important facts.
It should not be assumed to solve the known "handoff summary dropped a critical decision" problem by itself.

### Category C: Failure Isolation

#### E2B
Source:
- https://github.com/e2b-dev/E2B

Role:
- disposable / isolated execution sandboxes for agent-generated code

Harness interpretation:
`Failure Containment != Failure Recovery`

Harness position:
EXISTING RELEVANT CANDIDATE / REFERENCE.

Potential value:
A broken execution step damages an isolated sandbox rather than the main environment.
This is complementary to durable execution, not a substitute for it.

### Category D: Observability / Failure Inspection

#### Langfuse
Source:
- https://github.com/langfuse/langfuse

Role:
- traces model calls, tool calls, retrieval, latency, cost and evaluation data

Harness interpretation:
`Observability = find what broke`

Harness position:
EXISTING OBSERVABILITY CANDIDATE / REFERENCE.

It helps diagnose failures but does not by itself restore or resume execution.

#### AgentOps
Source:
- https://github.com/AgentOps-AI/agentops

Role:
- inspect, trace and replay agent sessions

Harness position:
LOWER-PRIORITY OBSERVABILITY REFERENCE.

Potential value:
session-level inspection / replay for debugging, but compare against Langfuse and lightweight custom tracing before adding another observability stack.

### Provisional priority for future comparison

High priority:
1. Inngest
2. Hatchet

Reference architectures:
3. Temporal
4. LangGraph

Memory research:
5. Letta

Existing / adjacent candidate examples:
6. E2B
7. Langfuse

Lower priority:
8. Prefect
9. Mem0
10. AgentOps

### Architectural decision to preserve

Do not evaluate these ten projects as ten interchangeable "agent frameworks."

Separate the problem:

`Durable Execution`
- save execution progress
- resume after failure
- avoid replaying completed steps

`Persistent Memory`
- preserve user / project knowledge across sessions

`Failure Isolation`
- contain risky execution

`Observability`
- inspect why the run failed

Then choose the smallest component necessary for the missing capability.

### Future validation questions

- Can the current Harness gain durable resume without adopting a large orchestration framework?
- What is the minimal checkpoint unit: Task, Job, Step, Tool call, or external side effect?
- How are completed steps distinguished from externally committed actions?
- Can retries always carry an Operation ID / Idempotency Key?
- When should retry become compensation or Human escalation?
- Can Human approval pause survive process restart?
- How should durable execution connect to Airtable state without making Airtable the execution engine?
- Can GitHub remain architecture / config history rather than runtime state?
- Does Inngest or Hatchet reduce custom runtime code enough to justify dependency and operational cost?
- What is the smallest observability layer required to reconstruct a failure?

Status:
PROPOSAL / NOT ACTIVE


---

## Update 2026-10-07 — OpenAI Decisions API / Bounded Decision Layer

Source:
- OpenAI API Changelog, 2026-10-06
- https://developers.openai.com/api/docs/changelog
- Decisions API reference
- https://developers.openai.com/api/reference/resources/decisions/methods/create
- User-supplied OpenAI Developers post:
  https://x.com/openaidevs/status/2107573382229188645

Status:
PUBLIC BETA / PROPOSAL / NOT ACTIVE

### What changed

OpenAI released the Decisions API in public beta using `gpt-6-luna`.

The endpoint is:

`POST /v1/decisions`

Officially supported answer forms:
- Predicate: probability that a statement is true
- Choice: select from predefined options
- Score: evaluate against ordered levels / rubric

The API accepts shared text evidence and user messages containing text and inline images.
For image input, the Decisions API reference currently requires inline base64 data URLs; external URLs and file IDs are not supported.

OpenAI states that the Decisions API can return typed answers up to approximately 10x faster than using GPT-6 Luna through the Responses API.

### Architectural significance

This is a concrete implementation of a bounded-decision layer:

```
Input / Event / Observation
        ↓
Bounded Decision
        ↓
Route / Classify / Score
        ↓
Normal path / Reviewer / Strong model / Human
```

The key distinction is:

`Bounded Decision != Open-ended Reasoning`

Use the cheapest narrow decision primitive that can safely answer the question.
Escalate to a reasoning model or Human when the task is ambiguous, high-impact, destructive, or outside the fixed decision contract.

### Potential AI-Harness roles

Candidate uses:
- route a task to model / tool / agent
- classify Grok / Airtable observer signals
- rank or score evidence
- choose a narrow next action from predefined options
- triage UI / image states
- pre-screen risky tool calls
- decide whether a task should escalate to a more capable model
- reduce expensive LLM calls on repetitive classification tasks

Possible flow:

```
Sensor / Human Input
        ↓
Decisions API
        ↓
LOW RISK       AMBIGUOUS       HIGH IMPACT
   ↓               ↓                ↓
auto path       reviewer        Human approval
```

### Relationship to existing candidates

This overlaps with the previously recorded idea of lightweight / bounded decision models such as Cloudflare Clef and Jev-style interfaces.

Do not delete local / open alternatives.

Provisional distinction:

```
OpenAI Decisions API
- cloud
- OpenAI-native
- typed probabilistic outputs
- fast integration with existing OpenAI API workflows

Clef / local bounded model
- potentially local / self-hosted
- lower provider coupling
- useful for offline or privacy-sensitive routing
```

The architectural candidate should therefore remain provider-neutral:

`Bounded Decision Adapter`

Possible implementations can be swapped underneath it.

### Human approval boundary

Do not use a probability score as a direct replacement for Human approval on destructive, irreversible, financial, credential, security, or other high-impact actions.

A safer interpretation is:

```
Decision score
    ↓
routing / escalation policy
    ↓
Human remains final authority where required
```

This keeps the decision model as a pre-filter or router rather than a self-authorizing actor.

### Pricing note — NEEDS VERIFICATION

The user-supplied report states:
- $0.10 / 1M input tokens
- no output / cache-read / cache-write charges
- regional and long-context multipliers apply

The first-party public materials checked on 2026-10-07 confirm the Decisions endpoint, model, speed claim, supported outputs, and input constraints.

However, the general GPT-6 Luna pricing page separately lists normal input, cached-input, cache-write, and output rates.

Therefore:
- do not encode the user-supplied Decisions-specific pricing as a permanent fact yet
- re-check the dedicated Decisions guide / pricing documentation before cost modeling or implementation

### Suggested experiment

Do not wire this into production immediately.

First experiment against one low-risk repetitive classification task, for example:
- Harness Inbox importance / route classification
- tool-risk pre-screening
- simple model-routing decision

Measure:
- accuracy against Human labels
- false-negative rate on risky cases
- latency
- cost
- calibration of returned probabilities
- escalation rate
- behavior under ambiguous inputs
- image-input usefulness if applicable

### Current decision

KEEP AS HIGH-PRIORITY VALIDATION CANDIDATE.

Do not make it a new core dependency yet.

The reusable architectural idea is more important than the vendor endpoint:

```
Cheap bounded decision
        ↓
Escalate only when needed
        ↓
Reasoning model / Reviewer / Human
```

This directly supports:
- Rule / Access separation
- Model-neutral Core + Adapter
- Human approval fatigue reduction
- retrieval / observer triage
- cost-aware model routing
- capability-separated review


---

## Update 2026-10-08 — EmbeddingGemma 2 / Local Semantic Warehouse Candidate

Status:
HIGH-VALUE EXPERIMENT CANDIDATE / NOT ACTIVE

Source context:
- User-provided summary of Google DeepMind's EmbeddingGemma 2 announcement (2026-10-06).
- Verify the current official model card / documentation again before implementation.

### Core idea

Treat EmbeddingGemma 2 not as a chatbot, but as a local semantic "warehouse keeper" for AI-Harness.

The model's job is not to answer the Human directly.
Its job is to understand the semantic contents of stored information, identify what is relevant to the current need, and return where the authoritative source lives.

```
Human / AI query
      ↓
Local semantic warehouse keeper
      ↓
Find semantically relevant items
      ↓
Return source locations / IDs
      ↓
Human or AI fetches the authoritative originals
      ↓
Reason / act
```

### Important distinction

The warehouse keeper does not become the Source of Truth.

Authoritative data remains in systems such as:
- GitHub
- Airtable
- Obsidian
- Google Drive or other external storage
- local files

The semantic index is disposable and rebuildable.

```
Original stores = authoritative
Semantic index = searchable map / catalog
```

If the embedding model changes, the index can be regenerated from the originals.

### What the warehouse keeper should know

Not only storage addresses or labels.

It should use semantic embeddings to understand the contents well enough to answer questions such as:

- "Where is the material about the Task Fork idea?"
- "Find the design note most related to this UI screenshot."
- "Which previous rule / decision is relevant to this new request?"
- "Find the code, notes, image, audio or video most semantically related to this query."

The retrieval result should ideally contain:
- source system
- file / record / object identifier
- path or address
- relevance score
- updated timestamp
- data type
- access class / policy metadata if available

### Proposed architecture

```
Airtable ─────┐
GitHub ───────┤
Obsidian ─────┤
Drive ────────┤
Local files ──┘
       ↓
Storage Adapters
       ↓
Local Semantic Index
EmbeddingGemma 2
       ↓
Retrieval Gateway
       ↓
Access / Policy Filter
       ↓
Return source locations
       ↓
Fetch only required originals
       ↓
ChatGPT / Hermes / Local LLM / Human
```

### Model-neutral advantage

The retrieval layer should not belong to Gemini or any single reasoning model.

```
                Local Retrieval Gateway
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       ChatGPT       Hermes      Local LLM
```

The same semantic index can serve different reasoning models.
This supports Model-Neutral Core + Model-Specific Adapter.

### Multimodal value

A major reason to track EmbeddingGemma 2 is the possibility of mapping multiple content types into one semantic space:

- text
- code
- images
- audio
- video

Potential future queries:
- text -> related image
- audio note -> related design document
- screenshot -> related code / requirement
- natural language -> related codebase location
- image -> related prior conversation notes

This could make the Retrieval Gateway a common information entrance for the Harness rather than a text-only RAG layer.

### Possible lightweight routing role

Semantic similarity may also support low-cost, local pre-routing for narrow cases such as:
- task category
- likely source
- likely relevant Skill / Rule / Memory
- zero-shot intent grouping

Do not use embedding similarity alone to authorize destructive or high-impact actions.

```
Embedding / similarity
       ↓
candidate / route
       ↓
Validator / LLM / policy
       ↓
Human where required
```

### Why this fits current cost constraints

The attraction is specifically local execution.

Target:
- no per-query API charge for the warehouse keeper
- local/private indexing
- only fetch originals and call cloud AI when needed
- reduce unnecessary cloud retrieval / context loading

Cloud-hosted inference is not required for the intended experiment.

### First experiment

Keep the experiment small.

Phase 1:
- index only AI-Harness Markdown / text artifacts
- ask natural-language queries
- compare retrieval quality against current filename / keyword / repository search
- return source paths only; do not let the index become authoritative

Phase 2, only if Phase 1 is useful:
- add Airtable records
- then code
- then images / audio / video

Measure:
- retrieval precision
- missed critical records
- stale-index behavior
- index rebuild time
- storage size
- latency on available local hardware
- usefulness of lower-dimensional embeddings
- operational simplicity versus current retrieval paths

### Safety / design constraints

- Original storage remains authoritative.
- Access rules must be checked before returning or fetching sensitive content.
- Embedding similarity is not proof of correctness.
- Human approval boundaries remain unchanged.
- Index corruption must never damage source data.
- Prefer rebuild over complex index repair.
- Do not expose all storage credentials directly to every reasoning model if the Retrieval Gateway can mediate access.

### Current decision

KEEP AS HIGH-VALUE EXPERIMENT CANDIDATE.

The architectural idea to preserve is:

```
External Stores
      ↓
Local semantic warehouse keeper
      ↓
Best source locations
      ↓
Fetch only what is needed
      ↓
Any reasoning model / Human
```

Potential Harness role:
`Retrieval Gateway / Local Semantic Warehouse`


---

## Update 2026-10-08 — Tailscale / Local Semantic Broker Bridge

Status:
HIGH-VALUE ARCHITECTURE IDEA / NOT ACTIVE

Source:
- https://tailscale.com/blog/codex-cloud-tailscale

### Why this matters

The previously identified Local Semantic Warehouse architecture had one unresolved gap:

```
Cloud AI
   ↓
???
   ↓
Local Agent
   ↓
EmbeddingGemma 2
   ↓
Local / External Information
```

Tailscale can potentially fill that network-transport gap for Codex Cloud by providing a private path into a local tailnet without exposing the local service directly to the public Internet.

### Proposed combined architecture

```
Codex Cloud
    ↓
Tailscale
    ↓
Local Agent / Hermes
    ↓
EmbeddingGemma 2
    ↓
Local files / Obsidian / Git / selected external stores
    ↓
Relevant source locations or minimal extracted context
    ↓
Back through Local Agent
    ↓
Codex Cloud
```

### Role split

```
Tailscale
= private transport / "secret road"

Local Agent / Hermes
= execution and handoff worker

EmbeddingGemma 2
= semantic warehouse keeper

Codex Cloud
= remote reasoning / coding brain
```

The local Agent does not need to be a powerful local LLM in the first phase.
It may start as a lightweight service that:
- receives a scoped retrieval request
- queries the semantic index
- reads only permitted originals
- returns source locations or minimal context

### Important security property

Do not expose the local machine broadly to the Internet.

Instead:
- expose only a narrow local service on the tailnet
- use least-privilege Tailscale grants / tags
- keep storage credentials local when possible
- apply Harness Access rules before returning content
- return only the minimum necessary information
- preserve Human approval for sensitive / destructive actions

The model should not receive unrestricted desktop access merely because the network path exists.

### Why this connects to the GPU-less local agent idea

The local side can remain lightweight:

```
Local CPU machine
 ├─ Local Agent / small API
 ├─ EmbeddingGemma 2
 ├─ local semantic index
 └─ source adapters
```

Heavy generation / reasoning can remain in Codex Cloud.

Therefore a GPU is not a prerequisite for the first version.

Possible staged path:

```
Phase 1
Codex Cloud
+ Tailscale
+ simple local retrieval API
+ EmbeddingGemma 2
+ Markdown / local-file search

Phase 2
+ Airtable / Obsidian / Git adapters
+ Access policy
+ richer source handoff

Phase 3
+ Hermes or another local agent
+ optional local LLM
+ richer local actions

Phase 4
+ GPU only if local reasoning becomes necessary
```

### Architectural significance

This forms a candidate answer to the broader problem:

"How can a cloud AI use private local knowledge without giving it unrestricted direct access to the desktop?"

Candidate pattern:

```
Remote AI
   ↓
Private transport
   ↓
Local policy boundary
   ↓
Local semantic broker
   ↓
Authoritative local sources
```

The local side decides what can leave the machine.

This is safer and more modular than granting the remote AI broad direct filesystem or desktop access.

### Scope limitation

The Tailscale article specifically concerns Codex Cloud integration.

Do not generalize this into:
"Tailscale gives every ChatGPT conversation direct local-PC access."

Other ChatGPT surfaces would still need an appropriate supported bridge / gateway / connector.

### Relationship to existing Harness candidates

Strongly related to:
- Candidate D: Retrieval Layer / External Connectors
- Candidate E: Externalized Memory / Model-Swappable
- Candidate F: Transport / Handoff
- Candidate B: Rule / Access Separation
- Candidate T: Model-Neutral Core + Model-Specific Adapter
- EmbeddingGemma 2 / Local Semantic Warehouse Candidate
- Hermes Local Agent project

### Current decision

KEEP AS HIGH-VALUE ARCHITECTURE IDEA.

Do not deploy yet.

The key reusable structure is:

```
Cloud reasoning
      ↓
Private transport
      ↓
Local Agent
      ↓
Semantic warehouse keeper
      ↓
Local authoritative information
```

This may allow the local agent project to begin before GPU acquisition.


---

## Update 2026-10-08 — Local Agent Safety Stack / Cross-Reference Map

Status:
HIGH-VALUE ARCHITECTURE MAP / NOT ACTIVE

Purpose:
Link the recent Local Agent discoveries into one coherent, cross-referenced architecture instead of keeping them as isolated notes.

Primary sources / signals:
- Tailscale / Codex Cloud bridge: https://tailscale.com/blog/codex-cloud-tailscale
- Microsoft Execution Containers article: https://forest.watch.impress.co.jp/docs/news/2146735.html
- AECP paper: https://arxiv.org/abs/2610.06481
- MCP tool-list cache behavior: OpenAI Agents SDK docs / repository
- Evidence-before-write: Grok Inbox signal from 2026-10-08; treat as idea / anomaly until independently reproduced
- EmbeddingGemma 2 / Local Semantic Warehouse: see the dedicated candidate in this file
- Hermes Local Agent: see projects/Hermes_Local_Agent/

### Combined architecture

```
Codex Cloud / Remote AI
        ↓
Tailscale
Private Transport
        ↓
Hermes / Local Agent
Local Worker / Handoff
        ↓
Microsoft Execution Containers (MXC)
OS-enforced Execution Boundary
        ↓
EmbeddingGemma 2
Local Semantic Warehouse Keeper
        ↓
Local authoritative sources
Git / Obsidian / files / selected stores
        ↓
Evidence / source IDs
        ↓
AECP-style structured artifact
+ Evidence-before-write gate
        ↓
Tool schema freshness check
        ↓
Action
        ↓
Validation / Trace
        ↓
Human approval where required
```

### Role of each component

#### Tailscale
Role:
Private transport between cloud execution and the local environment.

Architectural meaning:
The remote side should not require public exposure of the local service.

Related Harness areas:
- Transport / Handoff
- Access
- Model-neutral adapters

#### Hermes / Local Agent
Role:
Local worker that receives scoped requests, retrieves or acts locally, and returns bounded results.

Initial target:
Do not require a large local LLM.
A first version may be mostly deterministic orchestration plus retrieval.

Related Harness areas:
- Local execution
- Handoff
- Task Fork
- Human boundary

#### Microsoft Execution Containers (MXC)
Role:
OS-enforced containment for local agent execution.

Architectural meaning:
Do not rely only on prompt instructions such as "do not read this folder".
Where practical, enforce filesystem / process / network boundaries below the model layer.

Target principle:

```
Rule
= define what must not happen

Access
= make forbidden actions technically unavailable

Validation
= verify what actually happened
```

Safety posture:
- deny by default
- least privilege
- narrow mounted / visible resources
- explicit network policy
- Human approval remains for high-impact actions

Re-verify current Microsoft documentation and platform constraints before implementation.

#### EmbeddingGemma 2
Role:
Local semantic warehouse keeper.

Architectural meaning:
Find the best source locations from meaning, then hand back source IDs / paths rather than becoming the Source of Truth.

Related Harness areas:
- Retrieval Gateway
- Externalized Memory
- Evidence discovery
- Model-neutral context

#### Evidence-before-write
Role:
Require support for a write / mutation before considering it safe.

Candidate pattern:

```
Retrieve evidence
      ↓
record source / evidence IDs
      ↓
pre-write predicate
      ↓
write
      ↓
post-write validation
```

Do not treat "the tool call succeeded" as sufficient evidence that the write was justified.

Possible lightweight implementation:
Require evidence IDs in mutation tool arguments or in the task artifact.
Reject or escalate if missing.

Caution:
The current 2026-10-08 signal is a single report and is not independently reproduced.
Preserve the principle; do not preserve benchmark claims as fact.

#### AECP-style structured artifact
Role:
Replace fragile free-form inter-agent relay with structured, inspectable handoff artifacts where the commitment matters.

Candidate use:
- requested scope
- allowed sources
- required output
- source / evidence IDs
- assumptions
- access class
- result
- validation status

Harness should be able to fail closed when a required interface / contract is missing or inconsistent.

Do not replace all conversational coordination with rigid schemas.
Apply first to high-impact handoffs and durable commitments.

#### MCP tool-schema freshness
Role:
Prevent agents from acting against stale tool definitions.

Known OpenAI Agents SDK behavior:
Tool lists may be cached with `cache_tools_list=True`; the SDK exposes `invalidate_tools_cache()` for refresh.

Candidate Harness principle:
A task must not treat an old tool contract as authoritative after the tool surface changes.

Possible lightweight implementation:

```
session start
   ↓
tool schema hash
   ↓
before mutation
   ↓
schema unchanged?
  YES → continue
  NO  → refresh / revalidate / stop
```

This belongs primarily in implementation / Transport / Access checks, not as a new major subsystem.

### Cross-link matrix

```
Tailscale
  ↔ Hermes
  private transport for local work

Hermes
  ↔ MXC
  local worker constrained by OS boundary

Hermes
  ↔ EmbeddingGemma 2
  worker asks warehouse keeper where relevant originals live

EmbeddingGemma 2
  ↔ Evidence-before-write
  retrieval produces candidate evidence / source IDs

Evidence-before-write
  ↔ AECP artifact
  evidence and scope travel in structured handoff

AECP artifact
  ↔ MCP schema freshness
  action contract must match the current tool contract

MXC
  ↔ Access rules
  policy should be backed by technical enforcement

Validation / Human
  ↔ all layers
  final escalation remains available when confidence, authority, or reversibility is insufficient
```

### Why this matters to the GPU-less path

The architecture deliberately separates:
- heavy reasoning
- private transport
- local retrieval
- local execution
- safety boundaries

Therefore the first useful version can target a CPU-only local machine:

```
Remote reasoning
      ↓
Tailscale
      ↓
Hermes / lightweight local service
      ↓
MXC
      ↓
EmbeddingGemma 2 + local index
      ↓
local sources
```

A GPU becomes an optional future upgrade for more local reasoning, not a prerequisite for the retrieval / handoff / containment architecture.

### Current decision

KEEP AS A LINKING ARCHITECTURE MAP.

Do not activate all components at once.

Preferred order for future experiments:
1. Local semantic retrieval on text / Markdown.
2. Narrow local retrieval API.
3. Private transport.
4. OS-level containment.
5. Evidence-before-write on reversible mutations.
6. Structured artifacts for high-impact handoffs.
7. Tool-schema freshness checks.
8. Add local reasoning only if it produces measurable value.

The reusable principle is:

```
Remote intelligence
   ↓
private path
   ↓
local worker
   ↓
enforced local boundary
   ↓
semantic evidence retrieval
   ↓
structured, evidence-backed action
   ↓
validation
   ↓
Human when required
```
