# Google AI Studio
# Google AI Studio 運用ガイド

## 1. Purpose
## 1. 目的

This file records observed operating characteristics and practical guardrails for using Google AI Studio as an implementation agent.

このファイルは、Google AI Studioを実装エージェントとして利用するときの観測結果と実用的なガードレールを記録する。

It is not a general judgment of the product. Behaviors may change as models and the service evolve.

これは製品全体の評価ではない。モデルやサービスの更新によって挙動は変化し得る。

## 2. Primary Role
## 2. 主な役割

Use Google AI Studio primarily for implementation, prototyping, and code changes within an already-defined scope.

Google AI Studioは主に、定義済みの範囲における実装、PoC、コード変更を担当する。

Architecture decisions, UX decisions, acceptance decisions, and promotion of Lessons to Rules remain outside the implementation agent unless explicitly delegated.

アーキテクチャ判断、UX判断、採否判断、LessonからRuleへの昇格は、明示的に委任されない限り実装エージェントへ任せない。

## 3. Observed Lessons
## 3. 観測されたLesson

During iterative app development, broad or ambiguous instructions sometimes led to locally convenient fixes, unrequested additions, or UX changes that addressed symptoms rather than the underlying cause.

反復的なアプリ開発では、広すぎる指示や曖昧な指示に対し、局所的に便利な修正、未依頼機能の追加、根本原因ではなく症状だけを解消するUX変更が提案・実装される場合があった。

Therefore, implementation prompts should constrain both the objective and the allowed solution space.

そのため、実装プロンプトでは目的だけでなく、変更可能な範囲も制約する。

## 4. Prompt Guardrails
## 4. プロンプトのガードレール

For implementation tasks, specify as applicable:

- Objective — 今回の目的
- Allowed changes — 変更してよい範囲
- Forbidden changes — 変更してはいけない範囲
- Existing behavior to preserve — 維持すべき既存挙動
- Success criteria — 成功条件
- Verification method — 検証方法
- Required implementation report — 実装後に報告すべき内容

Prefer one primary objective per iteration when debugging or validating uncertain behavior.

不具合調査や不確実な挙動の検証では、1回の作業につき主目的を原則1つに絞る。

## 5. Root Cause Before Patch
## 5. パッチより原因特定

When a problem appears:

1. Reproduce or observe the problem.
2. Identify the responsible layer.
3. Expose raw/intermediate state when useful.
4. Determine the root cause.
5. Change only the responsible behavior.
6. Verify that existing behavior remains intact.

問題が発生した場合：

1. 問題を再現または観測する。
2. 責任を持つレイヤーを特定する。
3. 必要なら生データや中間状態を可視化する。
4. 根本原因を特定する。
5. 原因となる挙動だけを修正する。
6. 既存挙動が維持されていることを確認する。

Do not hide a failure with an unrelated fallback, mask, UI rearrangement, or substitute behavior unless explicitly requested.

明示的な指示がない限り、無関係なFallback、マスク、UI再配置、代替挙動によって失敗を隠さない。

## 6. UX Protection
## 6. UX保護

Do not change interaction priority, control placement, layer behavior, gestures, workflow steps, or existing user-visible behavior merely because it makes implementation easier.

実装を容易にする目的だけで、操作優先順位、コントロール配置、レイヤー挙動、ジェスチャー、操作手順、既存のユーザー向け挙動を変更しない。

Separate rendering order from interaction/hit-test priority when those concerns differ.

描画順と操作・Hit Testの優先順位は、目的が異なる場合は分離して設計する。

## 7. Verification States
## 7. 検証状態

Keep these states distinct:

- Assumption / hypothesis — 仮説
- Implementation complete — 実装完了
- Browser or development-environment test — 開発環境での確認
- Real-device observation — 実機観測
- Human UX evaluation — 人間によるUX評価
- Verified result — 検証済み結果

Do not report estimates, expected performance, or simulated results as real-device measurements.

推定値、期待性能、シミュレーション結果を実機測定値として報告しない。

## 8. Debugging and Observability
## 8. デバッグと可観測性

For browser, WASM, media, model, or device-dependent pipelines, prefer staged diagnostics over a single generic error.

ブラウザ、WASM、メディア、モデル、端末依存のパイプラインでは、単一の一般的エラーより段階別診断を優先する。

Useful diagnostics may include:

- initialization step
- asset URL and HTTP status
- asset size
- model handoff state
- backend/runtime
- raw output
- intermediate transformation
- final output
- timing per stage
- original error name/message/stack

Debug UI should remain separable from production UI.

デバッグUIは本番UIから分離可能な構造にする。

## 9. Mobile Real-Device Testing
## 9. スマートフォン実機検証

Desktop/browser success does not prove iPhone Safari or Android Chrome behavior.

デスクトップや開発ブラウザでの成功は、iPhone SafariやAndroid Chromeでの成功を保証しない。

Record both technical measurements and human observations such as:

- controls obscured by browser chrome or safe areas
- perceived animation strength and duration
- touch target usability
- output quality
- sharing behavior
- device-specific failures

Technical correctness and good UX are separate acceptance criteria.

技術的に正しいことと、UXとして良いことは別々の採用条件として扱う。

## 10. Scope Discipline
## 10. スコープ管理

Do not add features that were not requested, even when they appear useful.

依頼されていない機能は、有用に見えても勝手に追加しない。

When a secondary feature begins consuming disproportionate effort, define a PoC stopping condition and return to the product's core path after the question under test is answered.

副次機能の検証が過大になった場合はPoCの打ち切り条件を定義し、検証したい問いに答えが出たらコア開発へ戻る。

## 11. Reporting After Implementation
## 11. 実装後の報告

A useful implementation report should state:

- files changed
- exact reason for each change
- behavior preserved
- assumptions
- measured results
- unverified claims
- remaining uncertainty
- real-device checks still required

Avoid words such as "perfect", "100%", "fully solved", or "optimal" unless the stated scope and evidence actually justify them.

証拠が十分でない状態で「完璧」「100%」「完全解決」「最適」と断定しない。

## 12. Promotion to Shared Rules
## 12. 共通Ruleへの昇格

This file contains AI-specific operating guidance and observed Lessons.

このファイルはAI固有の運用ガイドと観測Lessonを扱う。

If a lesson proves useful across multiple implementation agents, propose it for review as a shared Harness Rule or Skill. Do not silently promote it.

複数の実装エージェントで有効だと確認されたLessonは、共通Harness RuleまたはSkillへの昇格を提案する。自動昇格はしない。
