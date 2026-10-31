# 外部レビュー・リレーの再開チェックポイント

2026-10-31。最新のユーザー確認に基づく記録。
保存状態は過去の記録であり、再開時のユーザー指示や権限を上書きしない。

## 停止位置（確定）

- Sakana AIとの往復は**資料07への回答受領まで完了**。
- 資料07への回答を踏まえたCodex側の軽微な補強と検証は完了し、資料08へ収録済み。
- **資料08はSakana AIへ渡したが、回答は未受領**。週間リミットに達して停止。
- 再開は**資料08をもう一度渡すところから**。処理済み・承認済みとみなさない。
- 資料09は準備済み・未送付。再開の最初に09を渡さない。
- 追加モデル試行・外部API切替・追加課金を行っていない。

## 再開時の受け渡し

1. Codex側でこの記録と現在の依頼・branch・実ファイルを照合する。
   作業ディレクトリは `AI-Harness-development`。
   `python -B tools/codex_environment.py begin environment-m2-pilot` で保存状態を確認する。
   CURRENTなら不要な再検証・refreshをしない。差異があれば内容を確認してから対応する。
2. Sakana AIの同じ会話へ、次の**資料08を再送**する。
   `agents/Codex/FUGU_IMPLEMENTATION_REVIEW_08_2026-10-31.md`
3. 回答ファイル `SAKANA_REVIEW_08_RESPONSE.md` を受領したらCodexへ渡す。
   対象資料08と末尾 `SAKANA-08-END` を確認する。
   対象や末尾マーカーは転記確認用であり、内容の正しさの証明ではない。
4. ユーザーの固定ループに従い、08の回答受領と同時に、用意済みの資料09をSakana AIへ渡せる。
   `agents/Codex/FUGU_EVALUATION_PLAN_09_2026-10-31.md`
   09は次の評価計画の検討で、08の修正完了を仮定しない。重大指摘は実試行前に対応する。
5. 次の返信でCodexは08の指摘を実証・照合し、必要な差分と検証結果を記録する。
   リレーを続ける場合は、実質的に独立した次作業があるときだけ次のファイルを準備する。

08と同一の依頼文を回答として受領した場合は採点・採用せず、取り違えを指摘する。
同一内容の再回答も既存原文を上書きせず、受領版を区別する。

## 現在のローカル実装と証拠

- branch: `codex/environment-upgrade-batch1`（development起点）
- HEAD: `7ae57c2a089f82e5e232690d8ecb8c257f51ac51`
- 変更は未commit。`.gitignore`変更と、AGENTS/agents/Codex/tests/toolsの追加を保持。
- 明示contract+refreshによる旧activation欠落からの復帰を実装・回帰確認済み。
- 出典検証は独立offlineの `citation-v2.2`。形式・literal・reuse_decisionの限定診断。
  位置/提示範囲/意味/全体品質を機械PASSへ混ぜない。新しいモデル比較runnerには未接続。
- 直近全体回帰124件中123成功・1skip、旧parser9/9、receipt互換9/9、FINAL receipt3/3正常。
- 保存時のbeginはCURRENT、現行gateの3項目はPASS、acceptanceはREVIEW_REQUIRED。
- 元M2 trial62ファイル、v1、既存のv2.0/v2.1保存結果は保持。
- 生ログ・入力snapshot・受領原文・照合記録はignored `.harness-runtime/` に保存。

上記はローカル機械検証。一般作業の品質・速度・文脈保持・実token効率の改善は未確認。
M2実効果確認/M3Human採用は未完了。元の8回を再実行・再採点しない。

## 維持する権限・目的

主目的はCodex環境整備。TRINITYは必要な評価補助。品質・重要制約・必須検証を落とさない。
未commit変更・無関係なファイル・元の証跡を保護する。
公開/push/main統合/本番移行/既存証跡やデータの削除は、内容を示したうえでHuman事前承認。
外部レビューの賛同や保存hashは、その承認の代わりにならない。
