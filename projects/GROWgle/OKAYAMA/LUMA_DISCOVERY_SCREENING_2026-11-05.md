# GROWgle — Luma公開イベント収集・判定記録 (2026-11-05)

State: RESEARCH_CAPTURE_COMPLETE / PUBLIC_IMPORT_0 / HUMAN_REVIEW_2  
Scope: 岡山県パイロット / 公開イベント / 2026-11-05以降に開始するもの  
Recorded: 2026-11-05 (Asia/Tokyo)

## 目的と既存ルール

LumaをGROWgleの**補助的な発見源**として調査する。既存の自治体・学校・企業・施設等からの収集を置き換えない。

準拠:
- `projects/GROWgle/RESEARCH_RULES.md`: 情報源と活動、発見情報と掲載根拠、HUMAN_REVIEW、Cross-Category Capture、調査層と公開層の分離
- `projects/GROWgle/PUBLICATION_SCORING.md`: Access Gate先行、通常掲載基準
- `projects/GROWgle/CHECKPOINT_V1_REGIONAL_SCOPE_2026-10-05.md`: 12府県調査のうち、今回の公開パイロットは岡山県を優先

## 収集方法・検索範囲

- ツール: Luma連携の公開イベント検索 `search_events` と個別詳細 `get_event`
- 日付: 2026-11-05以降の開催
- 検索地: 「岡山県」「倉敷市, 岡山県」「津山市, 岡山県」
- 岡山県の検索語: ワークショップ / 子ども / AI / 自然体験 / 学生 / プログラミング / 親子 体験 / ロボット STEAM / 起業 こども / キッズ / 小学生 / 高校生 / 体験教室 / ものづくり / アート
- 倉敷市: ワークショップ / 親子
- 津山市: 教育
- Luma検索は**順位付きの単一ページ**を返す。全件照会ではないため、未発見を「開催がない」と解釈しない。
- 地域フィルターに香川県高松市のイベントが混入したため、**実際の都道府県を追加検証して**対象外判定する。

## SOURCE

- `SOURCE_ID: LUMA_PUBLIC_EVENTS`
- `SOURCE_TYPE: EVENT_PLATFORM / DISCOVERY_SOURCE`
- URL: https://luma.com/
- 用途: イベント発見、主催者・カレンダーの逆引き、開催日時・会場・申込条件の確認
- 掲載判断: Lumaのイベントページが主催者による募集ページなら募集一次情報として扱えるが、参加条件等は個別イベント詳細で確認する
- 今回発見したSOURCE: [Claude Community Events](https://luma.com/claudecommunity) (`cal-TOpA5LAFfuDeFpu`)
- SOURCE評価: AIイベントの発見源。ただし今回の岡山県内の確認分は18歳以上対象で、子ども向けSOURCEと断定しない。

## ACTIVITY候補（同一イベントIDを検索語間で統合）

### LUMA-OKAYAMA-20261107-001

- `LUMA_EVENT_ID: evt-HvoOW3qM9vVeTU2`
- 名称: Okayama | Claude for Business Hackathon | Opus 5.5 Build Day
- URL（募集元）: https://luma.com/claude-0jmy
- 日時: 2026-11-07 18:00–21:00 JST
- 会場: ももスタ / MOMOTARO STARTUP CAFE、岡山市北区駅前町1丁目8-18 2階
- 主催系統: Claude Community Events / 公開ホスト 平川知秀・柳翔・宮崎翼
- 内容: 社内課題を題材にClaude Codeを使って実際に制作・発表するハッカソン
- 対象: **18歳以上と明記**。小学生・中学生・18歳未満の高校生は不可。18歳の高校生が対象となるかは学校・募集趣旨上の扱いを未確認。
- 参加費: Luma上のチケットは無料、承認制。Claude個人アカウントが必要でPro以上のプランでの参加を案内（実質負担に注意）
- 想定カテゴリ: AI / STEAM / WORKS（横断タグ、公開レコードは未作成）
- `ACCESS_MODE: AGE_RESTRICTED_18_PLUS`
- `DIRECT_APPLICATION: YES_WITH_APPROVAL`
- `ACCESS_GATE: CONDITIONAL_OR_FAIL_FOR_GROWGLE_AGE`
- `DECISION: HUMAN_REVIEW`（18歳の高校生という境界事例）
- `PUBLIC_STATUS: RESEARCH_ONLY`（確認まで公開掲載しない）
- 根拠: 主催者のLumaイベント詳細「18歳以上の方が対象です」

### LUMA-OKAYAMA-20261208-002

- `LUMA_EVENT_ID: evt-8yGFMC9w7WjKjh7`
- 名称: Okayama | Claude Workshop — Claudeと未来を考える思考整理ワークショップ【AI初心者向け】
- URL（募集元）: https://luma.com/claude-b7iu
- 日時: 2026-12-08 18:00–19:30 JST
- 会場: Wonderwall / TSUTAYA BOOKSTORE 岡山駅前、岡山市北区駅前町1丁目8-18 2階
- 主催系統: Claude Community Events / 公開ホスト 柳翔
- 内容: Claudeを使い、仕事の中でAIに任せることと人が行うことを整理するワークショップ
- 対象: **18歳未満は参加不可と明記**。18歳の高校生を含むかは未確認。
- 参加費: Luma上のチケットは無料、承認制。Claude無料プランでも参加可能、有料プランを推奨
- 想定カテゴリ: AI / WORKS（横断タグ、公開レコードは未作成）
- `ACCESS_MODE: AGE_RESTRICTED_18_PLUS`
- `DIRECT_APPLICATION: YES_WITH_APPROVAL`
- `ACCESS_GATE: CONDITIONAL_OR_FAIL_FOR_GROWGLE_AGE`
- `DECISION: HUMAN_REVIEW`（18歳の高校生という境界事例）
- `PUBLIC_STATUS: RESEARCH_ONLY`
- 根拠: 主催者のLumaイベント詳細「18未満の方のご参加できません」

## 対象外の検索ヒット

- `evt-Mme6W9dIhQZMRwC` / [takesakuメソッドセミナー@高松](https://luma.com/fz3ezmkx): 検索フィルター「岡山県」に混入したが、開催地は**香川県高松市**。岡山県パイロットには取り込まない（香川県の将来調査対象になり得るが、本記録では参加条件未精査）。

## 取り込み結果と重複判定

| 項目 | 件数 |
| --- | ---: |
| 岡山県内で詳細確認したユニークイベント | 2 |
| 小中高生向けとして参加適格性が確認できたイベント | 0 |
| GROWgle公開掲載へ反映 | 0 |
| Research LayerのHUMAN_REVIEWへ記録 | 2 |
| 県外混入として保留・未取り込み | 1 |

- 同一LumaイベントID・正規URLで検索語間の重複を統合した。**新規公開レコードを生成していない**ため、既存の公開データと二重掲載は発生しない。
- 既存GROWgle調査資料の代表的な岡山AI/STEAM案件と名称を照合したが、外部本番データベースとの完全な突合は**未実施**。
- 子ども向け正式掲載を伴わないため、`PUBLIC_VALUE_SCORE` は未採点。18歳高校生の扱いをHumanが判断するまでは公開しない。
- これはLumaの初回探索記録であり、岡山27自治体・全開催イベントの完全走査や自動同期の完了を意味しない。

## 次回の差分探索

1. `LUMA_EVENT_ID` と正規URLで二重取り込み防止。更新された開催日時・対象年齢・募集条件をチェック。
2. 子ども・親子・小中高生・地域教育団体のカレンダーが発見された時にSOURCEとして優先登録し、その主催者・一次資料を逆引きする。
3. AI/Harnessの既存収集と合流させる際は、1イベント=1レコード、複数カテゴリタグを守る。
4. GROWgleの公開パイロットは岡山県の参加可能イベントのみ。県外は広域Research Layerで別扱い。

