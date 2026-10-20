# GROWgle — 収録状態・公開状態の二軸管理

## 1. MD単位の状態
- `UNASSESSED`: 内容がまだ網羅的に照合されていない。**未実装と断言しない**。
- `PARTIAL_PROTOTYPE`: 当該MD由来の一部がv0.5の試作レコードに存在する。網羅完了ではない。
- `COMPLETE_VERIFIED`: 原文全項目に対し、レコードIDまたは除外理由を対応づけて照合済み。
- `REFERENCE_ONLY`: 方針・仕様・共通資料。イベントカードへ変換する対象とは限らない。
- `OUT_OF_CURRENT_PILOT`: 他県の地域研究。将来の広域展開資料として温存。

## 2. 個別企画・施設・活動の状態（次期台帳に必要な列）
`item_id, source_path, source_sha, source_heading, source_line, municipality, category, normalized_title, host, occurrence_date, audience, access_type, normalized_entity_key, extraction_status, integration_status, publication_status, published_url, official_url, checked_at, reviewer, notes`

- 抽出: `NOT_EXTRACTED / EXTRACTED / DUPLICATE_LINKED / EXCLUDED_WITH_REASON / NEEDS_REVIEW`
- サイト反映: `NOT_IN_SITE / PROTOTYPE_ONLY / SITE_DATA_READY / SITE_INTEGRATED`
- 公開: `UNVERIFIED / VERIFIED_PUBLIC_SOURCE / HUMAN_APPROVED / PUBLIC`
- 体験の現時点の募集状況は別カラムとし、過去の公表資料から募集中と推定しない。

## 3. 運用
1. GitHub差分で新規・更新MDを検出。
2. 文書の項目を抽出し、既存の `normalized_entity_key` と照合して重複を統合。
3. Aルール：一般募集なしでも、公式に公表された活動は「地域の活動記録」候補になる。
4. 非公表・未確認の個人情報や内部情報は公開層へ転送しない。
5. Human公開承認後のみ公開。既存公開レコードの原典が更新された場合は再確認対象へ戻す。
6. 全項目について公開・試作・重複・対象外・確認待ちのいずれかが明示されて初めて「MD取り込み完了」とする。
7. 「GitHub資料に存在」「試作に存在」「正式サイトに公開」を混同しない。

**完了判定**: SHAが一致し、抽出対象の各項目に紐づくIDまたは除外理由があり、保留件数が0のときだけ `COMPLETE_VERIFIED` にできる。
