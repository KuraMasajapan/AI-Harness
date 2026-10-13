---
status: proposal
created: 2026-10-14
origin: Human-provided X post and ChatGPT re-evaluation
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A+
stage_2_rank: A+
evidence_status: SINGLE REPORT / HYPOTHESIS
tags:
  - tacit-knowledge
  - domain-knowledge
  - human-decisions
  - agent-history
  - lessons
  - codex
  - harness-vnext
trigger_topics:
  - 暗黙知
  - ドメイン知識
  - 作業履歴
  - 判断基準
  - human-corrections
  - history-mining
  - vNext
---

# 作業履歴からHuman固有の暗黙知を発掘する — 小規模検証候補

## 現在のHuman判断（2026-10-14）

- **知識・検証候補として保存することは承認済み。**
- **実験の開始は保留（HOLD）。今すぐCodexを動かさない。**
- Core、Workflow、LESSONS、Trinity、各Project仕様、実装コードは変更しない。
- 将来、AI-Harness vNextの構造監査や、履歴からの知識抽出が必要になった時点で再検討する。
- 今回の保存は、Codex実験・技術採用・自動抽出機構の実装承認を意味しない。

## 起点となったSignal

Humanが共有したX投稿の要点：

> Claude Codeの過去の作業履歴から、本人に固有の判断基準、こだわり・好み、繰り返し用いる作業手順、過去の失敗や修正を抽出する。推測で補わず、履歴から明確に読み取れるものだけを挙げる。

投稿者は「自分でも気づいていなかったドメイン知識が多く見つかった」と報告している。ただし、投稿URL、原履歴、再現データは本記録では未取得。**個人的体験談（SINGLE REPORT）**であり、抽出精度・再現性・将来の成果改善は未実証。

## 再評価で変わった見方

当初の評価では、既存のAI-Harness Memory / LESSON / Conversation-to-Incubator Captureとの重複を重視し、独立した仕組みを増やす必要性は低いと考えた。

再検討により、次の二つは異なる機能だと整理した。

1. **Capture（発見済み知識の保存）**：会話中に重要だと認識できた知識を外部記憶に保存する。
2. **Mining（未明文化の知識の発掘）**：過去のHuman訂正・設計変更・反復判断から、まだ明文化されていない判断基準を証拠付きで発見する。

特に有望な仮説：

> Humanが繰り返しAIを訂正している箇所には、AIがまだ理解・明文化できていないドメイン知識が潜んでいる可能性がある。

この仮説は**未検証**。一度の修正を永続的な好みと誤認することや、変更理由が記録されていないことが主要リスク。

## 既存Harnessとの重複・相違

- `incubator/proposals/2026-09-20-conversation-to-incubator-capture.md`：有益だと認識した会話の記録。今回の「履歴を遡って未発見の基準を探す」とは目的が異なる。
- `incubator/proposals/2026-09-21-post-trinity-harness-structure-audit.md`：将来の構造監査に関係するが、今回の研究対象は「指示構造の見直し」ではなく「実運用で示されたHuman判断の抽出」。
- `incubator/proposals/2026-10-12-claude-mem-persistent-context.md`：セッション記憶の取得・要約・再利用に関するOSS候補。今回の仮説は独立した記憶基盤の採用を要求しない。
- `core/RULES.md` と `core/WORKFLOW.md`：訂正の受容、根拠の検証、LESSONプロセス、物理配置の誤推定防止などを既に扱う。発掘した知識は必ず既存記述と照合し、重複を新発見と数えない。

新規ツールや新しいMemory層を増やさず、既存のCodex・Git履歴・Markdownだけで検証できる可能性がある。

## 将来の最小実験案（未実施）

1. **対象を1 Projectに限定**：候補は `projects/Hangfire/`。作業計画・チェックポイント・仕様・変更履歴が比較的揃っている。対象は `development` の参照可能な履歴のみ。
2. **Codexによる読み取り専用調査**：Humanによる訂正・採否・反復判断の事例をまず約10件探す。GitHubの作業記録に存在しない会話や理由は推測で補完しない。
3. **抽出区分**：繰り返す判断基準／好み・品質基準／作業手順／過去の失敗・修正。各候補に根拠（ファイル、変更差分、コミット等）、適用範囲、確信度を付ける。
4. **重複照合**：`core/RULES.md`、`core/WORKFLOW.md`、`memory/LESSONS.md` および該当Projectの現行仕様と比較する。
5. **結果分類**：A. 本当に新しい候補、B. 既に記録済み、C. 根拠不足・不明。最大10件をHumanへ報告する。ゼロ件でもよい。
6. **継続判断**：既存資料にない、根拠が追跡可能で、将来の具体的な失敗防止につながる判断基準があるかを確認する。抽出件数の多さを成功条件としない。

**制限**：読み取り専用、ファイル作成・更新・コミット・外部保存・ルール昇格は禁止。実験開始時に未コミット変更とアクセス権限を確認する。今回の提案ファイル保存をもって実験実施とみなさない。

## 評価と未解決事項

- **一次評価**：A+（投稿の発見価値に着目）
- **二次評価**：A+（既存の「記録」と「発掘」の機能差を評価し、前回Aから上方修正）
- **最終研究判断**：CANDIDATE（知識発掘の検証価値あり）／**実施判断**：HOLD（Human希望により後日）
- **証拠の境界**：X投稿の実体験はSINGLE REPORT、Harnessにおける有効性はUNVERIFIED、既存ファイルとの目的差は文書照合済み。
- **リスク**：一時的な修正の過一般化、欠落した意思決定理由の推測、古い決定の現行ルール化、プライベート履歴の公開、重複知識の増殖、調査コスト。
- **代替**：今の `Conversation-to-Incubator` とLESSON運用を維持し、必要なときだけ手動・単発で知識を発掘する。
- **保存時点の未解決**：投稿URL、実際に閲覧できるセッション履歴の範囲、抽出精度、発見内容の再利用効果。

## Privacy / Authority

- 家族・個人・非公開会話などをそのまま公開リポジトリへ取り込まない。共有可能な抽象化だけを提案する。
- 探索結果は「候補」であり、Humanの恒常的な価値観や規則を自動確定しない。
- GitHubはdurable source、Obsidianは再発見の閲覧層。正式なCore/LESSON昇格は別途Human承認と検証を要する。

## Recall triggers

「ドメイン知識」「暗黙知」「過去履歴から判断基準」「Human訂正を学習」「Codexで履歴を掘る」「Claude Codeの作業履歴」「履歴マイニング」「AI-Harness vNextの構造監査」で再参照。

## 次のアクション

**現時点は何もしない。** Humanが再開を希望した場合だけ、上記の小規模な読み取り専用実験を準備する。
