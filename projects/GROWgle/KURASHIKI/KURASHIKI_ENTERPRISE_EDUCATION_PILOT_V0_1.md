# GROWgle — 倉敷市 企業・地域教育資源 Pilot v0.1

Status: ACTIVE_RESEARCH
Date: 2026-10-05
Scope: 倉敷市
Purpose: 地域企業・大学・医療・NPO・自治体等が子ども／学生／地域住民へ提供する体験型教育機会を、通常のイベント検索では落ちるものまで含めて構造化する。

## 1. Pilotの狙い

倉敷市を小地域Pilotとして、1市を深く探索した場合の母集団・有効SOURCE数・有効活動数・探索コストを測る。

既知の精度基準:
- JFEフェスタ
- 三菱自動車 水島製作所の地域・教育活動

これらだけを再発見するのではなく、以下を含む未知案件を探索する。

- 企業祭／工場祭／一般開放
- 工場見学／施設見学
- 親子ワークショップ
- ものづくり／科学／STEAM
- 職業体験／出前授業
- CSR／地域貢献
- 企業スポーツ
- 大学・病院・専門教育機関の地域開放
- 企業×学生
- 企業×大学
- 企業×自治体
- 企業×NPO
- 大学×地域住民
- 企業×学校×行政
- 複数組織による地域課題PBL

## 2. Data model

### SOURCE
企業・大学・病院・NPO・自治体・商工団体など、継続して体験機会を生む主体。

### ACTIVITY
SOURCEが提供する個別の見学・祭り・講座・ワークショップ・PBL等。

### Participation
- OPEN_PUBLIC: 個人／家族で一般応募可能
- GROUP_BOOKING: 団体予約
- SCHOOL_ONLY: 学校経由
- STUDENT_ONLY: 対象学校種・学生限定
- RESIDENT_ONLY: 地域居住条件あり
- PARTNER_ONLY: 連携組織経由
- WATCH: 現在募集なし／次回確認対象

### Continuity
- CONSTANT: 常設
- RECURRING: 毎年／定期開催が確認できる
- REPEAT_LIKELY: 複数年等から再開催期待
- ONE_OFF: 単発
- UNKNOWN: 未確認

## 3. 2026年度 企業学び楽舎 — 公的母集団

倉敷市公式「企業学び楽舎講座」2026年度版で、倉敷市内に事業所を持つ協力企業・組織64件を確認。
制度自体が「地元企業が学校へ出向き、生徒が仕事の話を聞き、製品・道具に触れ、実際の作業を体験する」キャリア教育。

### 64組織（公式パンフレット順）
1. 倉敷中央病院
2. 川崎医科大学附属病院
3. 水島協同病院
4. コープリハビリテーション病院
5. 倉敷スイートホスピタル
6. 創心會
7. 亀龍会 特別養護老人ホームくらしき
8. しおかぜ
9. ますみ会 ますみ荘
10. 郁青会 サンバードナーシングホーム
11. 温故知新会 ひかりの里
12. クムレ
13. 富田ケアセンター
14. 倉敷福徳会 小谷かなりや認定こども園
15. 松園福祉会 八幡認定こども園
16. 愛育福祉会 めばえ保育園
17. ドルフィン・メイトこども園 新倉敷
18. くすの木福祉会 中山保育園
19. ふるいち
20. 行雲
21. よしゐ屋BASE
22. 玉島信用金庫
23. 広島銀行 倉敷支店
24. 住友生命 倉敷匠支部
25. ディー・エス笹沖（オートバックス）
26. 江口電機
27. カザケン
28. 目黒建設
29. 中央建設
30. ナイカイアーキット
31. ヤマダ
32. エムイーシーテクノ 中国事業所
33. イシダ工務店
34. 岡山県瓦工事協同組合
35. 中央設備
36. 大同設備工業
37. 松永創作事務所
38. 日本非破壊検査 水島事業所
39. JFE物流
40. 下津井電鉄
41. ENGI倉敷スタジオ
42. ピープルソフトウェア
43. 中国電力 玉島発電所
44. 中国電力ネットワークセンター
45. テオリ
46. JFEスチール 西日本製鉄所
47. シンニチロ
48. 三菱ケミカル 岡山事業所
49. 萩原工業
50. 倉敷化工
51. 新来島サノヤス造船
52. 水島鋼板工業
53. 西鉄
54. アキオカ
55. ベティスミス
56. 松井織物
57. 菅公学生服
58. 坂本織物
59. 廣珍
60. 倉敷市管事業協会
61. ENEOS 水島製油所
62. M.S.E.
63. 岡山県警察
64. 起業ラボ（倉敷市商工課presents）

## 4. 企業学び楽舎内で確認した高体験性講座

単なる企業説明ではなく、実作業／機器／製品に触れるものを優先。

- 医療: 医療職実習、多職種連携
- 倉敷スイートホスピタル: 心臓マッサージ、採血、松葉杖、低周波
- 医療・介護: AED、車椅子、体力測定等
- 福祉: 車椅子、高齢者疑似体験
- 金融: マネープランゲーム、銀行員／顧客体験
- オートバックス: 商品・簡単な整備作業
- 江口電機: FA・最新製造技術体験
- 建設: 現場機器操作
- ヤマダ: クレーン試乗・簡単操作
- エムイーシーテクノ: 工具・測定・重量物操作
- イシダ工務店: 地域課題／未来の街ワークショップ
- アキオカ: 鋳造・砂型づくり等
- 水島鋼板工業: 測定器等
- 製造・繊維・エネルギー等: 個別逆引き継続

## 5. 企業学び楽舎外で確認済みの重要SOURCE / ACTIVITY

### JFEスチール 西日本製鉄所（倉敷地区）
- 夏休み工場見学 2026: 小学生以上、保護者同伴
- 団体工場見学: 10名以上、予約制
- JFEフェスタ: 工場／船上見学等を含む地域開放型
- Classification: OPEN_PUBLIC / GROUP_BOOKING / RECURRING
- Learning: 鉄、巨大製造設備、仕事、物流、環境技術

### 三菱自動車 水島製作所
- 2026年度工場見学: 小学校限定、90分、各時間帯最大160名（引率含む）
- 出前授業「人と環境にやさしいクルマづくり（SDGs）編」: 小4〜6、EV試乗等
- 「クルマづくり編」: 小5、安全保護具・ネジ締め等
- Classification: SCHOOL_ONLY / RECURRING
- Learning: 自動車、一貫生産、ロボット、安全、EV、環境

### テオリ（真備）
- 竹家具の製造工程見学
- 団体向け工作: 器、鍋敷き、飾り台等
- 親子にも適する
- Classification: GROUP_BOOKING / CONSTANT
- Learning: 竹→素材→加工→家具→デザイン

### 中国電力（玉島／水島）
- 発電所見学（小学生からの受入確認）
- Classification: GROUP_BOOKING / CONSTANT
- Learning: 発電、エネルギー、設備、地域インフラ

### 水島臨海鉄道
- 2026夏休み「こども運転体験教室」
- 4歳〜小学生が倉敷貨物ターミナルで運転体験
- Classification: OPEN_PUBLIC / CHILD
- Learning: 鉄道、運転士、物流、地域交通

### 倉敷中央病院
- Open Hospital 2026
- 地域の小中学生向け施設見学・医療仕事体験
- Classification: OPEN_PUBLIC / RECURRING_CANDIDATE

### 倉敷中央病院リバーサイド
- Open Hospital 2026
- 地域の小中学生向け施設見学・仕事体験
- Classification: OPEN_PUBLIC

### 倉敷市立市民病院
- Open Hospital 2026
- 一般参加、一部ブース抽選
- Classification: OPEN_PUBLIC
- Region: 児島

### 中国銀行 / ちゅうぎんFG × 倉敷成人病センター
- 2026「ちゅうぎん☆キッズドリーミースクール」
- 病院の仕事体験
- 他地域企業／大学との職業体験ネットワークの一部
- Classification: OPEN_PUBLIC / COMPANY_X_MEDICAL

### みずしま財団 × 倉敷市環境学習センター × JFE
- 2026 水島コンビナート環境学習ツアー
- 親子24名（子ども13名）
- 公害史→製鉄所→水循環・環境技術
- 主催側が翌年度継続意向を明記
- Classification: OPEN_PUBLIC / COMPANY_X_NPO_X_MUNICIPALITY / WATCH_2027

### 岡山県企業局 × 小学校 × JFE
- 2026 水島・連島地区小4対象
- 浄水場座学→水処理実験→施設見学→環境学習→JFE見学
- Classification: SCHOOL_ONLY / GOVERNMENT_X_SCHOOL_X_COMPANY

### 玉島商工会議所「玉島歩きプラン」
- 年間平日、100年以上続く味噌醤油・酒蔵・紙問屋3店を見学
- 子ども向け特典あり
- Classification: GROUP_BOOKING / CONSTANT / LOCAL_INDUSTRY_NETWORK
- Learning: 港町、商業史、食品、紙、ものづくり

### みずしま滞在型環境学習コンソーシアム
- 水島の公害、環境、産業、歴史、文化、地域生活を教育資源化
- 2026に複数大学合同ゼミ受入等
- Classification: REGIONAL_NETWORK / COMPANY_X_UNIVERSITY_X_NPO_X_COMMUNITY
- Important: 個別イベントではなくSOURCE NETWORKとして保持

## 6. 地域別の学習ルート仮説

### 水島
鉄 / 自動車 / 化学 / 石油 / 発電 / 物流 / 公害史 / 環境再生
→ JFE / 三菱自動車 / 三菱ケミカル / ENEOS / 旭化成等
→ 工場・職業・環境・エネルギー・地域史

### 児島
繊維 / デニム / 制服 / 染色 / 縫製 / 港
→ 菅公学生服 / ベティスミス / 染色企業等
→ 素材・デザイン・染色・製造・エシカル

### 玉島
発電 / 鋳造 / 港 / 食品 / 商業史 / リサイクル
→ 中国電力 / アキオカ / 老舗企業群等
→ エネルギー・金属・食品・循環・地域史

### 真備
竹 / 家具 / 地域資源
→ テオリ
→ 自然素材・加工・デザイン・持続可能性

### 倉敷中心〜中庄
医療 / 福祉 / 大学 / 金融 / 観光
→ 病院群 / 川崎学園 / 大学 / 金融機関等
→ 医療職・ライフサイエンス・福祉・金融・地域サービス

## 7. 構造上の発見

1. 「イベント検索」だけではSCHOOL_ONLYやGROUP_BOOKINGを大量に落とす。
2. 大企業だけではなく中小企業の方が手作業密度の高い体験を持つ場合がある。
3. SOURCEとACTIVITYを分離しないと、継続活動を毎年別イベントとして重複管理する。
4. 地域内に年齢別成長ルートを構成できる可能性がある。
   小学生見学 → 中学生職業体験 → 高校PBL → 大学連携／インターン。
5. 企業×NPO×自治体の複合企画は、産業だけでなく地域史・環境問題まで学べるため教育密度が高い。
6. 倉敷は市全体を一括表示するより、水島・児島・玉島・真備・中心部等のLOCAL_SUBAREAを持つ方が地域色を保持できる。

## 8. Next research queue

Priority A:
- 企業学び楽舎64組織を全件SOURCE化
- 64組織それぞれについて学び楽舎外の一般公開／学校連携／CSRを逆引き
- 水島コンビナート主要企業を全社逆引き
- 児島繊維・染色企業群を逆引き
- 玉島の中小製造・老舗企業を逆引き

Priority B:
- 大学／高専／専門教育機関
- 病院／医療法人
- NPO／財団
- 商工会議所／業界団体
- 企業スポーツ
- 地域祭・企業祭

Priority C:
- 2024〜2026の過去開催を遡り、RECURRING / WATCH候補化
- 年齢別GROWTH_PATHの抽出
- OPEN_PUBLIC案件の開催月カレンダー化

## 9. Pilot completion criteria

倉敷Pilotは以下を満たした時点でv1 checkpointとする。
- 公的母集団64件の全件分類
- 主要産業企業の追加母集団作成
- 大学／病院／NPO／自治体連携SOURCEを追加
- 有効ACTIVITY重複排除
- 参加形態と継続性付与
- 地域別密度と探索コストの測定
- 他自治体へ展開可能な探索手順を確定


## 10. Discovery expansion — 2026-10-05

### 倉敷市「教育旅行」公式ルートを第二母集団として追加

企業学び楽舎64社とは別に、倉敷市修学旅行誘致委員会／倉敷観光コンベンションビューローが公開する教育旅行向け体験網を第二母集団として扱う。

#### 児島ものづくり体験
公式ページは児島を「日本一の繊維のまち」と位置づけ、本物のものづくり体験を将来の進路を考える契機としている。

確認SOURCE:
- 旧野﨑家住宅・野﨑家塩業歴史館
  - 塩づくり体験
  - 小中高の授業利用は入館料免除条件あり
  - 最大60名、要予約
- ベティスミス・ジーンズミュージアム
  - ジーンズ史／製造工程
  - 平日は工場を窓越し見学
  - ボタン・リベット打ち、オリジナルジーンズ制作
  - 最大100名
- BIG JOHN 児島本店
  - デニム雑貨のボタン・リベット打ち
  - インディゴ染め等
  - 小中高生料金設定あり、最大120名
- 倉敷どんぐり工房（浦上染料店）
  - 染色系体験SOURCE候補
- 坂本織物
  - 真田紐、力織機、児島の綿・繊維史
- 倉敷市児島産業振興センター
  - 綿繰り〜糸紡ぎ無料体験
  - ものづくりワークショップ
- 髙田織物
  - 畳縁国内シェア40%以上
  - 準備・製造工程／織機見学
- 菅公学生服 倉敷工場
  - 小中学校等の学校団体限定工場見学
  - SCHOOL_ONLY / CONSTANT_CANDIDATE

児島では「企業学び楽舎」と「教育旅行」の母集団が一部重複するため、SOURCE統合しACTIVITYを別管理する。

### 玉島・水島・真備 産業環境学習

倉敷市側が「鉄鋼・石油化学コンビナート、公害経験、リサイクル」をSDGs教育資源として公式にパッケージ化している。

追加確認:
- ヒラキン リサイクルステージ玉島
  - 小学生高学年以上
  - 最大40名
  - 1〜2時間
  - 無料、要予約
  - 自動車／家電／鉄道レール等が再資源化される工程
  - GROUP_BOOKING / CONSTANT
  - Learning: リサイクル / サーキュラーエコノミー / カーボンニュートラル / 産業設備
- JFEスチール
  - 教育旅行公式SOURCEとしても確認
  - 高炉・圧延工程・鉄の学び館
- みずしま滞在型環境学習コンソーシアム
  - 公害史、環境再生、平和、人権、まちづくりを統合
  - NPO単体ではなく地域教育ネットワークとして保持

### 水島臨海鉄道 — RECURRINGへ昇格

2026年:
- こどもの日: 子ども向け運転／車掌体験、フォークリフト荷役見学
- 7月31日 夏休みこども運転体験教室
  - 4歳〜小学生
  - 定員28名
  - 旅客車両100m運転
  - 機関車との綱引き
  - 大型フォークリフト見学
  - 車両クラフト
- 10月25日 鉄道の日記念フェスタ予定

Classification:
OPEN_PUBLIC / RECURRING / TRANSPORT / WORKS / COMMUNITY

### カモ井加工紙 — GROWTH_PATH SOURCE

公式SDGsページで以下を明記:
- 近隣小学生の工場（社会科）見学
- 中学生・高校生・大学生のインターンシップ受入
- ファクトリーツアー、展示会

2026 mt factory tour vol.15:
- 年1回
- 2012年開始
- 2026年は約1万人枠に約4万人応募との地域媒体報道
- mt製造工程、歴史、工場、アート等

Classification:
SCHOOL_ONLY + STUDENT + OPEN_PUBLIC / RECURRING
Growth path:
小学生社会科見学 → 中高生インターン → 大学生インターン

### 三菱自動車 水島製作所 — 2026 current state確認

- 工場見学可能期間: 2026-04〜2027-03
- 2026年度は小学校のみ
- 最大160名（引率含む）
- 90分
- プレス／溶接／車体組立
- 出前授業:
  - SDGs編 小4〜6、EV試乗等
  - クルマづくり編 小5、工具／ネジ締め／安全保護具
- 毎年実施時期が公式に明記されているため RECURRING

### 岡山県企業局 × 小学校 × JFE

2026-06-25:
- 連島東小4年 45名
- 浄水場座学
- 薬品による水処理実験
- 浄水施設見学
- 環境学習
- その後JFE倉敷地区見学

企業×学校×行政を拾う必要性を裏付ける代表ケース。

## 11. Search-method update

倉敷Pilotで有効だった探索経路を以下に更新。

1. 自治体の企業教育制度から公的企業母集団を取得
2. 自治体／観光側の教育旅行・産業体験リストを第二母集団化
3. 各SOURCE公式サイトのCSR／SDGs／工場見学／NEWSを逆引き
4. 過去3年程度の地域媒体から企業祭・年1回開放を発見
5. 学校側の「社会見学」「探究」「PBL」から企業名を逆引き
6. NPO／財団から企業×環境×地域史の複合案件を探索
7. イベントカレンダーから同一SOURCEの年内複数開催を確認
8. 年齢段階をまたぐ活動があればGROWTH_PATHを付与

重要:
- 「企業名 + 子ども」だけでは不足。
- 「企業名 + 社会見学 / 探究 / CSR / SDGs / 地域貢献 / 出前授業 / インターン / 工場祭 / ファクトリーツアー」を横断する。
- 一般公開されないSCHOOL_ONLYをGROWgle上で捨てない。
- 教育旅行向けGROUP_BOOKINGも、個人イベントと分けて保持する。

## 12. New structural finding

倉敷には少なくとも3種類の「教育供給網」が重なっている。

A. 市のキャリア教育網
企業学び楽舎（2026: 64社）

B. 市・観光側の地域産業教育網
児島ものづくり体験 / 水島・玉島・真備産業環境学習

C. 各企業・NPO独自網
企業祭、ファクトリーツアー、夏休み企画、環境学習、インターン等

したがって完全性を高めるには、A/B/Cの和集合をSOURCEマスター化してから重複排除する必要がある。


## 13. Heatmap-ready data model — approved

Human decision: GROWgleの企業・地域教育資源を将来ヒートマップ化する。
目的は企業ランキングではなく、地域に存在する次世代育成資源の密度・偏り・空白を可視化すること。

### SOURCEに追加する地理属性
- municipality
- local_subarea
- address
- latitude
- longitude
- geocode_precision
- location_type: SOURCE_SITE / ACTIVITY_SITE / SERVICE_AREA

### ACTIVITYに追加する可視化属性
- target_age: PRESCHOOL / ELEMENTARY_LOW / ELEMENTARY_HIGH / JUNIOR_HIGH / HIGH_SCHOOL / UNIVERSITY / FAMILY / GENERAL
- access: OPEN_PUBLIC / GROUP_BOOKING / SCHOOL_ONLY / STUDENT_ONLY / RESIDENT_ONLY / PARTNER_ONLY
- category: AI / ENTRE / WORKS / STEAM / CREATIVE / NATURE / SPORTS / COMMUNITY
- regional_asset: LOCAL_INDUSTRY / NATURE_ASSET / CULTURAL_ASSET / EDUCATION_ASSET / MEDICAL / INFRASTRUCTURE / OTHER
- continuity: CONSTANT / RECURRING / REPEAT_LIKELY / ONE_OFF / UNKNOWN
- collaboration: COMPANY_X_STUDENT / COMPANY_X_UNIVERSITY / COMPANY_X_MUNICIPALITY / COMPANY_X_NPO / UNIVERSITY_X_RESIDENT / COMPANY_X_SCHOOL_X_GOVERNMENT / OTHER
- hands_on_level: 0-3
  - 0 information only
  - 1 observation / tour
  - 2 guided hands-on
  - 3 real tools / production / professional task simulation
- recurrence_years
- last_verified_date
- next_watch_date
- source_confidence

### Derived heatmap layers
1. EXPERIENCE_DENSITY
   - 子ども・若者向けACTIVITYの地理密度
2. OPEN_ACCESS_DENSITY
   - 個人・家族がアクセスできるOPEN_PUBLIC密度
3. HANDS_ON_DENSITY
   - hands_on_level 2-3を重視した体験密度
4. AGE_COVERAGE
   - 年齢層別の機会密度
5. CATEGORY_DENSITY
   - STEAM / WORKS / AI / MEDICAL / NATURE等の分野別密度
6. REGIONAL_OPENNESS
   - 企業・大学等が地域へ継続的に開いている度合い
7. COLLABORATION_DENSITY
   - 企業×学校×大学×自治体×NPO等の連携密度
8. CONTINUITY_DENSITY
   - CONSTANT / RECURRINGを重視した持続的教育資源
9. OPPORTUNITY_GAP
   - 人口・学校・企業等に対して体験機会が相対的に少ない地域／年齢／カテゴリ
10. YEAR_OVER_YEAR_CHANGE
   - 年次で教育資源が増加／減少している地域

### Important scoring policy
- 「掲載されていない企業 = 悪い企業」とは判定しない。
- 未発見と活動不存在を区別する。
- 件数だけで企業価値を順位付けしない。
- 大規模イベント1件と、小規模でも毎月継続する活動を同一扱いしない。
- SCHOOL_ONLYも地域教育資源として保持するが、OPEN_PUBLICとは別レイヤーにする。
- 活動場所と本社所在地を混同しない。
- 点データが少ない段階ではヒートマップを断定的な「評価地図」として公開しない。

### Heatmap design principle
可視化の主語は「企業評価」ではなく「地域の次世代育成環境」。
地図から以下を発見できることを目標とする。
- 強い地域資産
- 子どもがアクセスできる機会
- 年齢の谷
- 分野の谷
- 地理的空白
- 連携の強い地域
- 新しいCSR／教育施策を置くと効果が高い場所

### Future policy / CSR use
十分なデータ量と検証期間を得た後は、自治体・学校・企業・NPOが
「どの地域／年齢／分野に次の教育機会を追加すれば空白を埋められるか」
を判断する基盤として利用可能にする。

### Data collection rule from this point
今後追加するSOURCE / ACTIVITYは、可能な範囲で上記heatmap-ready属性を同時取得する。
過去取得分はKurashiki Pilot完了時にbackfillする。


## 14. Enterprise reverse-search batch 1 — 2026-10-05

企業学び楽舎64組織のうち、外部活動・学校連携・一般公開・学生向け活動を企業公式情報中心に逆引き。

### 萩原工業
Official sustainability pageで以下を確認。
- 地元小学生等の工場見学受入れ
- 防災イベントへの参加。製品展示・体験を通じ、防災時の用途を学ぶ
- 津山工業高等専門学校と包括連携・協力協定。研究・教育面で連携
- BRIDGE SETOUCHI: 製造工程で出るブルーシート等を再利用し、防災・減災活動基金へ
Classification:
- SCHOOL / GROUP_VISIT
- COMPANY_X_HIGHER_EDUCATION
- COMMUNITY / DISASTER_EDUCATION
- RECURRING_SOURCE
GROWgle note:
製造業体験と防災・資源循環を接続できるSOURCE。企業学び楽舎外にも教育的活動あり。

### ENEOS 水島製油所
Current official site:
- 岡山県内の水島製油所近隣の学校関係・官公庁等を原則対象に見学受入
- 火・水・木、70分程度、5〜40名、DVD・概要説明・構内見学
- 3か月前までに申込
Community / next-generation activities:
- 2024年度: 近隣小学校で出前サッカースクール
- ENEOS児童文化賞受賞者によるアウトリーチ公演を水島拠点でも実施
- 2025-12-13: 倉敷市で地元中学生48名向けENEOS野球教室
- 2024年度にも水島製油所連携で中学生向け野球教室
Classification:
- SCHOOL / GOVERNMENT_GROUP_BOOKING
- SPORTS / COMMUNITY
- RECURRING
GROWgle note:
「石油・エネルギー」だけでなく企業スポーツが独立教育ルートになっている。

### JFE物流
Official sustainability page:
- 毎年開催されるJFEフェスタで、倉敷の船上見学会運営に参加
- 地域来訪者向けの体験機会をJFEスチールと共同で支える
Student route:
- 2026年7〜9月に倉敷で複数回のオープン・カンパニー
- 製鉄所内の物流現場体験、社員解説、オフィス見学、座談会
Classification:
- COMPANY_X_COMPANY / COMMUNITY
- UNIVERSITY_STUDENT / CAREER
- RECURRING
GROWgle note:
同じJFEフェスタでもJFEスチール単独イベントとせず、物流会社も教育機会の供給主体として紐づける。

### カザケン
Official site:
- 専門学生インターンを随時受入。現場で測量、出来形管理、鉄筋組立検査、朝礼・KY等を実習
- 2021年、真備陵南高校生の3日間インターン。重機乗車、測量、施工現場見学等
- 小田川堤防強化工事では岡田小4年32名、川辺小6年生を現場見学会へ招待
Classification:
- COMPANY_X_HIGH_SCHOOL
- COMPANY_X_VOCATIONAL_STUDENT
- COMPANY_X_ELEMENTARY_SCHOOL
- WORKS / INFRASTRUCTURE / DISASTER_RECOVERY
GROWgle note:
真備の復旧・治水工事そのものを学習資源化している。地域史・防災教育との接続候補。

### ピープルソフトウェア
Official site:
- 2025「OICおしごと体験 ～みんなの『好き』が未来をつくる！～」への出展実績
- 大学生向けインターンシップ・仕事体験を継続受付
Classification:
- WORKS / IT
- CAREER_EDUCATION
- UNIVERSITY_STUDENT
Status:
- 子ども向け出展の詳細内容を次段階で要確認
- 倉敷での継続性・対象年齢を追加確認

### 菅公学生服 / カンコー学生服 倉敷工場
Official company information:
- 倉敷工場のセーラー服製造工程を題材にした工場見学動画を公開
- 全国の小学生の社会科見学・家庭科教材として利用可能
- 全国の中高向けオンライン工場見学プログラムを開始
- 映像とライブ配信、制服に込めた思い、工場社員とのトークセッションを組み合わせる
Classification:
- SCHOOL_ONLY / ONLINE
- ELEMENTARY / JUNIOR_HIGH / HIGH_SCHOOL
- LOCAL_INDUSTRY / TEXTILE
GROWgle note:
現地見学だけでなくONLINE_ACTIVITYもSOURCEモデルに保持すべき事例。

### ベティスミス
Official site:
- 日本最古のジーンズ工場を平日に窓越し見学可能
- ジーンズミュージアムで国産ジーンズ史を学べる
- ジーンズ作り体験あり
- 小さな子どものいる家族向け貸切体験室も用意
- 敷地内ガーデンを一般開放。不定期で農作物収穫イベントもあり
Classification:
- OPEN_PUBLIC / CONSTANT
- FAMILY
- LOCAL_INDUSTRY / TEXTILE / CREATIVE
GROWgle note:
工場見学 + ミュージアム + 制作体験を一か所で完結できる児島の強い常設SOURCE。

### 株式会社ヤマダ
Official site news:
- 2024、2025と連続して「企業学び楽舎」参加を確認
- 高校生向け就職応援メディア掲載、応募前職場見学も実施
Classification:
- SCHOOL_ONLY / RECURRING confirmed for 企业学び楽舎
- HIGH_SCHOOL_CAREER
Next:
- 学び楽舎のクレーン試乗・簡単操作内容と公式ニュース詳細を紐づける

### 日本非破壊検査 水島事業所
Official siteで水島事業所・技術センターの所在を確認。
企業学び楽舎では非破壊検査を教育題材として採用。
Status:
- 学び楽舎外の一般公開／学校見学は未確認
- HIGH_VALUE_WATCH: 技術自体がSTEAM / SAFETY学習に適するため継続探索

### 三菱ケミカル 岡山事業所
Official siteで岡山事業所の製品・製造拠点を確認。
企業学び楽舎参加は確認済み。
Status:
- 独自の子ども／学校向け一般公開活動は今回の公式検索では未確定
- 次回、岡山事業所RCレポート・地域交流資料・過去NEWSを遡る

### ENEOS historic continuity note
旧JX時代の水島製油所では、1976年から2014年まで小4〜6対象サッカースクールを38年間継続した記録あり。
現在は形式を変え、学校への出前サッカーや野球教室等へ次世代育成活動が継続している。
GROWgleではイベント名の継続だけではなく、「企業スポーツを通じた地域児童育成」というSOURCE-level continuityとして扱う。

## 15. Batch 1 findings

- 企業学び楽舎参加企業を逆引きすると、制度内の1講座だけでは見えない別活動が複数出る。
- 特に萩原工業、ENEOS、JFE物流、カザケンは外部教育・地域活動が明確。
- 水島は製造見学だけでなくSPORTS、環境、防災、物流へ枝分かれする。
- 真備では建設会社が豪雨復旧・治水工事を児童・高校生の学びへ接続している。
- 児島では工場を「見せる」だけでなく、歴史展示・制作体験・オンライン教材まで多層化している。
- SOURCEごとに一般公開、学校限定、学生キャリアを分離して持つ必要性が再確認された。

## 16. Next reverse-search batch

優先:
- 江口電機
- ENGI倉敷スタジオ
- 下津井電鉄
- 玉島信用金庫
- 広島銀行 倉敷支店
- 住友生命 倉敷匠支部
- ナイカイアーキット
- 目黒建設
- 中央建設
- エムイーシーテクノ中国事業所
- 新来島サノヤス造船
- 倉敷化工
- 水島鋼板工業
- アキオカ
- 松井織物 / 坂本織物
- 廣珍
- 倉敷市管事業協会


## 17. Enterprise reverse-search batch 2 — 2026-10-05

### 中央建設 — HIGH_VALUE / RECURRING
Official newsで2025〜2026に複数の子ども・学生向け活動を確認。

- 2025-01-29 倉敷市立旭丘小学校6年生2クラス向けドローン体験会
  - ドローンの歴史・種類・法律・建設業での活用を座学
  - 児童が一人ずつ操縦
  - 仕事との接続まで説明
- 2025年11月にも旭丘小学校6年生2クラスで再度ドローン体験
  - 2025年内2回目。児童の要望から再開催
- 2026 高校生インターン
  - 入札ゲーム
  - 安全巡視
  - CAD
  - 測量
  - 施工事例
- 2026 玉島笠岡道路工事で高校生の現場見学、産業教育共通研修を受入
- 2026-10 倉敷商工会議所の「はたらく車」子ども向け建設イベントに参加

Classification:
SCHOOL_ONLY / ELEMENTARY / HIGH_SCHOOL / RECURRING
WORKS / STEAM / INFRASTRUCTURE
COMPANY_X_SCHOOL / COMPANY_X_CHAMBER
hands_on: HIGH

GROWgle note:
単発の企業学び楽舎参加ではなく、ドローン・測量・CAD・入札・現場見学まで年齢別に複数の教育接点を持つ強いSOURCE。

Evidence:
https://chuo-kensetsu.co.jp/
https://chuo-kensetsu.co.jp/news/

### 目黒建設 — HIGH_VALUE / RECURRING
Official「社会貢献」で中学生職場体験を定期受入と明記。

- 毎年、倉敷市立中学校の職場体験を受入
- 建設現場見学
- 測量
- 簡単な現場作業
- BIMソフト操作
- ドローン操作
- 企業学び楽舎にも初年度から参加
- 学校経由のインターンは日数・時期を相談可能
- 2022/2023 倉敷チャレンジ・ワーク14実績確認

Classification:
SCHOOL_ONLY / GROUP_OR_SCHOOL_REQUEST
JUNIOR_HIGH / STUDENT
CONSTANT_OR_RECURRING
WORKS / STEAM / INFRASTRUCTURE

Evidence:
https://www.meguro-kensetu.co.jp/contributions

### ナイカイアーキット — RECURRING_CANDIDATE
2024 企業学び楽舎で中1向け出前授業。
体験:
- ドローン操縦チーム戦
- 建設業でのドローン活用説明
- 入札の仕組み説明
- 模擬入札ゲーム

過去には高校生3日間インターン:
- 杭打ち施工管理
- 浄水場耐震補強
- 浚渫船、水質監視
- 潮位観測
- 測量実習

Classification:
SCHOOL_ONLY
JUNIOR_HIGH / HIGH_SCHOOL
WORKS / STEAM / INFRASTRUCTURE
hands_on: HIGH

Evidence:
https://www.naikai-archit.jp/information/1514

### アキオカ — HIGH_VALUE
2026 企業学び楽舎:
- 生徒が鋳造工程を実体験
- 砂を固めた型づくり
- 金属を型に流し込む作業

高校生向け:
- 2026新社屋
- 高卒候補者の職場見学を随時受付
- 砂型、1,500℃溶解・注湯、研磨、塗装、検査などの工程を紹介

Classification:
SCHOOL_ONLY + HIGH_SCHOOL_CAREER_VISIT
JUNIOR_HIGH / HIGH_SCHOOL
WORKS / STEAM / LOCAL_INDUSTRY
hands_on: VERY_HIGH
Region: 玉島

Evidence:
https://akioka1966.co.jp/
https://akioka1966.co.jp/recruit/highschool/

### 新来島サノヤス造船 水島製造所 — HIGH_VALUE
学校側記録で企業学び楽舎の体験内容を確認。
- 中学生が船の構造を紙で作り、強度を出す体験
- 船体構造・造船工学を簡易模型で理解

大学・高専等学生向け:
- 2026夏期インターン募集
- 水島製造所で2日間就業体験
- 溶接・ガス切断・設計実習
- 工場見学、社員座談会

Classification:
SCHOOL_ONLY / UNIVERSITY_STUDENT
JUNIOR_HIGH / UNIVERSITY
WORKS / STEAM / SHIPBUILDING
hands_on: HIGH
Region: 児島塩生 / 水島製造所

Evidence:
https://www.sanoyas.skdy.co.jp/
https://www.sanoyas.skdy.co.jp/recruit/

### 坂本織物 — OPEN / CONSTANT
倉敷教育旅行公式SOURCE。

- 倉敷真田紐の解説
- 真田紐＋ラインストーンのキーホルダー制作
- 小学生 / 中学生 / 高校生 800円
- 約20分
- 最大20名
- 2日前まで要予約
- 倉敷市自然の家のファミリーキャンプにも講師派遣実績
- 一般向けにはキーホルダー、コースター等のワークショップも実施

Classification:
OPEN_OR_GROUP_BOOKING / CONSTANT
ELEMENTARY / JUNIOR_HIGH / HIGH_SCHOOL / FAMILY
CREATIVE / LOCAL_INDUSTRY / CULTURAL_ASSET
Region: 児島

Evidence:
https://kankou-kurashiki.jp/kyouiku_ryokou/theme/monodukuri/1921/
https://www.sanadahimo.info

### ENGI 倉敷スタジオ — STRATEGIC_SOURCE
倉敷市と包括連携。
市公式が以下を明記:
- 企業学び楽舎で中高向け出前講座
- 教育現場へのプロの知見導入
- アニメ人材育成
- 育成人材の市内就業先として連携
- 官民学一体のデジタルコンテンツ産業育成

企業公式:
- 倉敷スタジオは若手作画スタッフ育成拠点
- 2026 学生向けアニメーター説明会
- ポートフォリオ講習・講評
- 倉敷スタジオ見学
学校側:
- 2024 倉敷高校でスタジオ所長がアニメーター職業講話

Classification:
COMPANY_X_MUNICIPALITY / COMPANY_X_SCHOOL
JUNIOR_HIGH / HIGH_SCHOOL / STUDENT
CREATIVE / DIGITAL_CONTENT / CAREER
RECURRING / STRATEGIC_NETWORK

Evidence:
https://www.city.kurashiki.okayama.jp/business/employment/1005580/1005581.html
https://engi-st.net/studio/kurashiki/

GROWgle note:
倉敷の企業教育では珍しい「アニメ・デジタルコンテンツ産業」。製造業偏重を補完する重要カテゴリ。

### 江口電機 — CAREER + SCHOOL_SOURCE
- 企業学び楽舎2026参加
- FA（Factory Automation）を題材とする企業
- 大学・大学院生向け採用直結型インターンを本社（倉敷市中島）で実施
- 座学＋現場体験

Classification:
SCHOOL_ONLY + UNIVERSITY_STUDENT
STEAM / WORKS / AUTOMATION
Status:
企業学び楽舎での具体的ハンズオン内容はパンフレット情報と突合継続。

Evidence:
https://eguchi-denki.co.jp/

### 玉島信用金庫 — VERY_HIGH_VALUE / OPEN_PUBLIC
今回の逆引きで大きな発見。

2026:
- 「キッズマネースクール2026」を開催
- 本店営業部で夏休みワークショップ「マグネット黒板づくり」
- 子ども向けマジックショー
- 「子育て応援project〜未来を担う子どもの力でより良い街に〜」

継続プログラム:
- ジュニア倶楽部
- 主催キッズ・マネースクールや子ども向け企画情報
- 2023 キッズサマースクール
- 2024 キッズサマースクール
- 2024 お金の○×クイズ / キッズフリーマーケット
- 2024 空飛ぶクルマ見学＆体験ツアー
- 2025 English Technology Camp
- 2026 キッズマネースクール

Classification:
OPEN_PUBLIC_OR_MEMBER_EVENT / RECURRING
ELEMENTARY / FAMILY
ENTRE / FINANCIAL_LITERACY / STEAM / COMMUNITY
Region: 玉島

GROWgle note:
金融機関が単なる金融教育を超え、テクノロジー・空飛ぶクルマ・工作等の子ども体験SOURCEになっている。企業中心探索で特に価値が高い。

Evidence:
https://www.shinkin.co.jp/tamashima-sk/
https://www.shinkin.co.jp/tamashima-sk/jrclub/

### 広島銀行 倉敷支店 — GROUP_LEVEL_SOURCE, LOCALITY_UNVERIFIED
広島銀行全体では公式に:
- 小学生向けキッズ・マネースクール
- 中高生向け職場体験学習
- 大学への出張講座
を継続。

倉敷市内には倉敷・児島・水島・玉島支店あり。
ただし今回、上記教育活動が倉敷支店で直近実施された一次情報までは確認できず。

Classification:
FINANCIAL_EDUCATION_SOURCE
LOCAL_ACTIVITY_STATUS: VERIFY
Do not count as Kurashiki active ACTIVITY until locality confirmed.

Evidence:
https://www.hirogin.co.jp/company/csr/social/

### 住友生命 倉敷匠支部 — GROUP_LEVEL_SOURCE, LOCALITY_UNVERIFIED
住友生命全体:
- 小学校〜大学へ金融教育等の出前授業
- 中高向け金融、キャリア、コミュニケーション、がん教育、課題解決型授業
- 2024年度末まで累計200回超
- 小学校高学年向け金融教育も開始

企業学び楽舎64社に倉敷匠支部が登録されているため、倉敷では制度経由の教育接点あり。
ただし独自の倉敷地域開催実績は継続確認。

Evidence:
https://www.sumitomolife.co.jp/about/sustainability/important/stakeholder/fr.html

## 18. Batch 2 structural findings

1. 建設会社群が予想以上に強い。
   - ドローン
   - BIM / CAD
   - 測量
   - 模擬入札
   - 工事現場
   - 防災・インフラ
   が学校教育へ直接接続されている。

2. 玉島信用金庫は金融教育だけでなく、継続的な「子ども体験プロデューサー」に近い。
   地域金融機関を単に FINANCE とせず EVENT_SOURCE として逆引きする。

3. ENGIは倉敷における新産業育成政策と教育が直結した例。
   「既存地場産業」だけでなく「地域が新たに育てようとしている産業」をGROWgleで別タグ化する価値あり。
   Candidate tag: EMERGING_LOCAL_INDUSTRY

4. 新来島サノヤス造船、アキオカ、中央建設等は、中学生の簡易体験から高校・大学の実務体験まで段階的接続が可能。

5. 金融・保険の全国企業は、全国施策が存在しても倉敷実施を確認できない限りKurashiki ACTIVITYとして数えない。
   SOURCE候補とLOCAL VERIFIED ACTIVITYを分離する。

## 19. Next queue

Unfinished / deeper verification:
- 玉島信用金庫 2026キッズマネースクール詳細
- 下津井電鉄: バス職業体験・学校受入の有無
- 松井織物
- 廣珍
- 倉敷市管事業協会
- 中央設備 / 大同設備工業
- エムイーシーテクノ中国事業所
- 日本非破壊検査 水島事業所
- シンニチロ
- 三菱ケミカル岡山事業所
- ENEOS水島製油所の学校見学・企業スポーツ追加確認
- JFE物流
- 医療 / 福祉64社群の独自Open Hospital・職場体験
- 保育園群の地域向け活動


## 20. Enterprise reverse-search batch 3 — 2026-10-05

### M.S.E. — VERY_HIGH_VALUE / OPEN + SCHOOL + PBL
2026年の公式・準公式情報で、企業学び楽舎外の活動を複数確認。

- 高梁川流域未来人材育成事業の連携可能企業
  - 技術指導
  - 会社・工場見学
- 地元小学校でワークショップ
- 高校生の工場見学を積極受入
- 製造過程で出る廃電線を使う「デンセンストラップ」
- 2026年「本物の電線に触れよう。デンセンストラップ ワークショップ」
- 倉敷観光コンベンションビューローでも工場見学＋ストラップ製作体験を紹介
  - 制御盤の役割
  - ものづくり現場
  - 実際の電線に触れる制作体験

Classification:
OPEN_OR_GROUP_BOOKING / SCHOOL_ONLY / HIGH_SCHOOL / PBL
ELEMENTARY / HIGH_SCHOOL
STEAM / WORKS / UPCYCLING / LOCAL_INDUSTRY
hands_on: HIGH
Region: 玉島

Evidence:
https://mse1026.co.jp/2026/06/24/2326/
https://mse1026.co.jp/company/
https://kankou-kurashiki.jp/2026/05/%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E3%80%80m-s-e/
https://www.city.kurashiki.okayama.jp/business/employment/1013051/1017009.html

GROWgle note:
従業員10人規模の町工場でも、工場見学・小学校WS・高校見学・アップサイクル教材まで持つ。企業規模で探索優先度を下げるべきでない代表例。

### 下津井電鉄 — COMPANY_X_HIGH_SCHOOL_X_UNIVERSITY / PRODUCT_DEVELOPMENT
倉敷市の2026未来人材育成事業で連携可能企業。
- 商品開発
- 会社・工場見学

実例:
- 倉敷鷲羽高校ビジネス研究部
- 環太平洋大学 現代経営学科
- 下津井電鉄
が共同し、鴻ノ池SAの新メニュー「児島塩3Cサンデー」を開発。
高校生・大学生が地域観光資源を使った商品企画、試作、協議、販売PRを経験。

Classification:
COMPANY_X_HIGH_SCHOOL_X_UNIVERSITY
HIGH_SCHOOL / UNIVERSITY
ENTRE / LOCAL_INDUSTRY / TOURISM / FOOD
hands_on: HIGH
Region connection: 児島

Evidence:
https://www.city.kurashiki.okayama.jp/business/employment/1013051/1017009.html
https://www.u-presscenter.jp/article/6059
https://digitalpr.jp/r/118667

GROWgle note:
「企業×学生」だけでなく、高校＋大学＋企業による世代混合PBLの好例。

### 廣珍 — HIGH_VALUE / WORK_EXPERIENCE + PBL
2026未来人材育成事業で連携可能企業:
- 商品開発
- 技術指導
- 会社・工場見学

地域実績:
- 中学生の職場体験を受入
- 特別支援学校の現場実習を受入
- 実際の店舗業務と同じ達成リストを使い、接客等を段階的に体験
- 地元玉島の食材を積極利用

Classification:
SCHOOL_ONLY / PBL
JUNIOR_HIGH / SPECIAL_NEEDS_STUDENT / HIGH_SCHOOL_CANDIDATE
WORKS / ENTRE / FOOD / COMMUNITY
hands_on: HIGH
Region: 玉島

Evidence:
https://www.city.kurashiki.okayama.jp/business/employment/1013051/1017009.html
https://kouchin.jp/
https://article.yahoo.co.jp/detail/0aafc3ebfe8015d2ea4fb4fbcdf3e868819e4bf8

### 中央設備 — PBL / COMPANY_VISIT
2026未来人材育成事業の連携可能企業として会社・工場見学を提供可能。
企業学び楽舎では大同設備工業と共同し、中学生へ:
- 水道・ガス配管
- 空調設備
- 生活インフラの仕事
- 現場作業服・ハーネス試着
を提供。

Classification:
SCHOOL_ONLY / HIGH_SCHOOL_PBL_AVAILABLE
JUNIOR_HIGH / HIGH_SCHOOL
WORKS / INFRASTRUCTURE
hands_on: MEDIUM-HIGH

Evidence:
https://www.city.kurashiki.okayama.jp/business/employment/1013051/1017009.html
https://kuratoco.com/kigyomanabigakusya/

### 大同設備工業 — RECURRING_CANDIDATE
中央設備との企業学び楽舎共同講座で、中学生に配管・空調等の生活インフラと実物安全装備を体験させる。
2026年時点で倉敷創業60周年の地域密着設備会社。

Classification:
SCHOOL_ONLY
JUNIOR_HIGH
WORKS / INFRASTRUCTURE
hands_on: MEDIUM-HIGH

Evidence:
https://kuratoco.com/kigyomanabigakusya/
https://daido-s.jp/

### 日本非破壊検査 水島 — RECURRING / HIGH_STEAM
企業公式ブログで2023企業学び楽舎参加を確認。
新田中2年向けに:
- 渦電流探傷試験
- 赤外線サーモグラフィー試験
- ドローン
を体験。

さらに2025年、水島中で水島鋼板工業と企業学び楽舎を実施。
安全防護具等を用いた体験も確認。

Classification:
SCHOOL_ONLY / RECURRING_CONFIRMED
JUNIOR_HIGH
STEAM / WORKS / SAFETY / INSPECTION_TECH
hands_on: VERY_HIGH
Region: 水島

Evidence:
https://www.jndi.com/blog/
https://www.kurashiki-oky.ed.jp/mizushima-j/2025-1manabi.html

GROWgle note:
非破壊検査は、物理・センサー・熱画像・ドローンを仕事として統合して見せられる高密度STEAM案件。

### 松井織物 — SCHOOL_SOURCE / TEXTILE
水島中で2024年度の企業学び楽舎参加を確認。
- 仕事の内容
- 働く意義
- コミュニケーション
- 体験学習
また郷内中でも企業学び楽舎としてテオリ・水島鋼板工業と並び実体験型講座を実施。

Classification:
SCHOOL_ONLY / RECURRING_CANDIDATE
JUNIOR_HIGH
LOCAL_INDUSTRY / TEXTILE
Region: 児島
Status:
一般向けワークショップ／工場見学の恒常提供は今回未確定。追加確認。

Evidence:
https://www.herikoubou.co.jp/
https://www.kurashiki-oky.ed.jp/mizushima-j/2024manabi.html

### シンニチロ — PBL / FACTORY_VISIT
2026高梁川流域未来人材育成事業で会社・工場見学の連携可能企業。
水島事業所、南畝工場、松江工場を持ち、JFE製鉄関連、製造請負、機械整備等を行う。

Classification:
HIGH_SCHOOL_PBL_AVAILABLE
WORKS / LOCAL_INDUSTRY
Region: 水島
Status:
小中学生向け独自プログラムは未確認。企業学び楽舎との接続を継続調査。

Evidence:
https://www.city.kurashiki.okayama.jp/business/employment/1013051/1017009.html
https://shinnichiro.co.jp/company/

### 三菱ケミカル 岡山事業所 — SCHOOL_VISIT / CHEMISTRY
岡山県公式「おかやま子育て応援宣言企業」ページで:
- 子どもたちに化学の楽しさを知ってもらうため
- 事業所見学
- 体験教育学習への参加
を実施方針として明記。

岡山事業所は倉敷市潮通の水島コンビナート拠点。

Classification:
SCHOOL_OR_GROUP_VISIT
STEAM / CHEMISTRY / LOCAL_INDUSTRY
Region: 水島
Status:
2026直近の具体開催日・対象校・一般公募性は追加確認。

Evidence:
https://www.pref.okayama.jp/page/detail-92324.html
https://www.mcgc.com/group/outline/mcc/location/plant.html

## 21. Batch 3 structural findings

1. 町工場を軽視すると重要案件を落とす。
   M.S.E.は従業員10名規模でも、工場見学・学校WS・高校見学・アップサイクル制作を持つ。

2. PBLを独立検索すると「イベント検索」では出にくい企業が見つかる。
   2026未来人材育成事業だけで、シンニチロ、廣珍、中央設備、下津井電鉄、M.S.E.等が連携可能企業として表出。

3. 下津井電鉄の事例は、高校・大学・企業が同一商品を共同開発するため、GROWTH_PATHではなく CROSS_AGE_PBL として扱う価値がある。

4. 日本非破壊検査の講座は、渦電流・赤外線・ドローンを含み、製造業系の中でもSTEAM密度が非常に高い。

5. 食品・飲食企業も「調理体験」だけではなく、接客・店舗運営・商品開発・地域食材を通じたキャリア教育SOURCEになり得る。

## 22. Search-status note

今回までで、企業学び楽舎64社のうち製造・建設・金融・交通・デジタル・食品系の重要SOURCEはかなり輪郭が出てきた。
次段階では未深掘りの医療・福祉系をまとめて逆引きし、Open Hospital、職場体験、地域講座、学校出前の独自活動を確認する。


## 23. Medical / welfare reverse-search batch — 2026-10-05

### 倉敷中央病院 — OPEN_PUBLIC / VERY_HIGH_VALUE
2026-06-06「オープンホスピタル2026」。
地域の小中学生を主対象に病院施設見学・仕事体験を実施。
予約制プログラム例:
- 超音波検査体験
- 手術室探検
- こども薬剤師
- 放射線部門体験
- 救急・レスキュー体験
- 歯科材料実験
小さな子どもも参加可能な一般向け企画あり。

Classification:
OPEN_PUBLIC / FAMILY / RECURRING_CANDIDATE
ELEMENTARY / JUNIOR_HIGH
MEDICAL / STEAM / WORKS
hands_on: VERY_HIGH

Evidence:
https://www.kchnet.or.jp/about_us/open-hospital-2026/

### 倉敷中央病院リバーサイド — OPEN_PUBLIC
2026-08-08 Open Hospital。
小中学生向けに:
- こども薬剤師
- 顕微鏡
- 歯科材料工作
- 放射線部門
- 高齢者疑似体験
- 病院食
等。

Classification:
OPEN_PUBLIC / FAMILY
ELEMENTARY / JUNIOR_HIGH
MEDICAL / STEAM / WELFARE
hands_on: HIGH

Evidence:
https://www.kchnet.or.jp/krh/about_us/open-hospital-2026/

### 水島協同病院 — HIGH_VALUE / RECURRING_CANDIDATE
2026広報で複数の若者向け接点を確認。
- 2026-03-11 古城池高校生の看護体験
- 2026年夏〜秋に高校生向け医療体験・地元高校生への健康教育を継続
- 広報紙に「リアルな医療業界を体感」等を掲載

Classification:
SCHOOL_OR_STUDENT_PROGRAM
HIGH_SCHOOL
MEDICAL / CAREER
RECURRING_CANDIDATE

Evidence:
https://mizukyo.jp/letter/letter-4428/
https://mizukyo.jp/letter/

### コープリハビリテーション病院 — RECURRING
病院広報で:
- 2025年も中学生職場体験（倉敷チャレンジ・ワーク14）
- 夏の高校生医療体験
を確認。

Classification:
SCHOOL_ONLY / STUDENT_PROGRAM
JUNIOR_HIGH / HIGH_SCHOOL
MEDICAL / REHABILITATION / CAREER
RECURRING

Evidence:
https://coopreha.jp/tayori

### 創心會 — HIGH_VALUE / MULTI-AGE
2026企業学び楽舎:
- 車いすに乗る／押す
- ビジョントレーニング
- 作業療法士の仕事
を中高生へ提供。

2026-09:
- 倉敷市高校のキャリア教育へ作業療法士が参加
- 実際の道具に触れながら仕事説明

学生向け:
- 倉敷本社で施設見学付き会社説明会
- 1DAYオープンカンパニーでサービス現場体験

Classification:
SCHOOL_ONLY / HIGH_SCHOOL / UNIVERSITY_STUDENT
JUNIOR_HIGH / HIGH_SCHOOL / STUDENT
WELFARE / MEDICAL / CAREER
RECURRING_CANDIDATE
hands_on: HIGH

Evidence:
https://www.soushinkai.com/news/4676
https://www.soushinkai.com/news/4280

### 亀龍会 — HIGH_VALUE / PBL_AVAILABLE
企業学び楽舎で:
- 車いす試乗
- 車いす操作
- 段差移動
- 介護職の責任・役割
を体験。

2026高梁川流域未来人材育成事業では:
- 技術指導
- 会社・施設見学
の連携可能法人。

Classification:
SCHOOL_ONLY / HIGH_SCHOOL_PBL_AVAILABLE
JUNIOR_HIGH / HIGH_SCHOOL
WELFARE / COMMUNITY
hands_on: HIGH

Evidence:
https://kuratoco.com/kigyomanabigakusya/
https://www.city.kurashiki.okayama.jp/business/employment/1013051/1017009.html

### クムレ — COMMUNITY_INFRASTRUCTURE / CAREER
法人自体が地域子育て支援・障がい児支援・親子通園等を継続提供。
教育・キャリア面:
- 施設見学を随時受付
- ボランティアを広く受入
- 保育士・児童指導員志望者向け「お仕事体験」を随時実施
- 保育園、乳児保育、児童発達支援等の複数拠点で現場体験

地域親子向け:
- 園庭・サロン無料開放
- 親子教室
- 保育園体験
- 子育て相談

Classification:
COMMUNITY / STUDENT_CAREER / FAMILY
PRESCHOOL / FAMILY / STUDENT
WELFARE / CHILDCARE / COMMUNITY
CONSTANT

Evidence:
https://cumre.or.jp/
https://www.cumre-recruit.com/gathercat/new-graduate/
https://cumre.or.jp/qa/

GROWgle note:
クムレは「体験イベントSOURCE」だけでなく、地域の子育て・福祉インフラとして別種の恒常SOURCE。GROWgleに含める場合はイベントDBと支援施設DBを混同しない。

### 富田ケアセンター — STUDENT / COMMUNITY
- 新卒者向け就業体験を随時受付
- 個別事業所見学に対応
- 2026現在、地域貢献事業・子育て事業も運営
- 企業学び楽舎参加済み

Classification:
STUDENT_CAREER / SCHOOL_SOURCE
WELFARE
Status:
小中高生向け独自一般イベントは追加確認。

Evidence:
https://www.tomicare.com/recruit/index.cgi?c=faq-1
https://www.tomicare.com/

### 倉敷スイートホスピタル — STUDENT / SCHOOL_SOURCE
2026:
- インターンシップ案内
- 企業学び楽舎では心臓マッサージ、採血、松葉杖、低周波等の実体験講座を提供

Classification:
SCHOOL_ONLY + STUDENT
MEDICAL / CAREER
hands_on: VERY_HIGH

Evidence:
https://sweet-town.jp/
https://sweet-town.jp/hospital/

## 24. Medical / welfare structural findings

1. 医療・福祉は「見る」より「やる」比率が高い。
   薬剤師、超音波、救急、放射線、車いす、作業療法等、職業体験密度が非常に高い。

2. Open Hospital型は一般家庭から直接アクセスできるため、SCHOOL_ONLY中心の企業学び楽舎を補完する。

3. 医療機関は中学生職場体験、高校生医療体験、大学生インターンまで年齢連続性が強い。

4. 福祉法人は地域支援サービスそのものを持つため、「イベントSOURCE」と「地域支援インフラ」を分離管理する必要がある。

5. 倉敷の企業・地域教育資源は製造業だけでなく、医療・福祉が第二の大きな柱として成立している。


## 25. Enterprise reverse-search batch 4 — 2026-10-05

### 三菱自動車 水島製作所 — benchmark resolved / RECURRING
ユーザーが既知例として挙げていた「三菱自動車のお祭り」の正体を一次情報で確認。

2024-10-20:
- 三菱自動車水島製作所感謝祭
- 水島製作所構内
- 入場無料
- 三菱車展示
- ショー
- 福引き
- 模擬店
- 水島警察署、西日本三菱自動車販売等と協働した「クルマの学校」
  - マイパイロットパーキング同乗体験
  - パトカー・白バイ・消防車展示等

2026:
- 三菱自動車公式イベントカレンダーで2026-10-18 10:00〜15:00
- イベント名「三菱感謝祭」
- 会場: 三菱自動車 水島製作所構内
を確認。
- 同会場で新型パジェロ先行展示会も実施予定。

Past continuity:
- 2018にも「三菱自動車感謝祭」開催記録あり
- 2023には水島製作所で水島警察署と「クルマの学校」を実施、約120名来場
- 2024感謝祭でも「クルマの学校」を実施

Classification:
OPEN_PUBLIC / FAMILY / RECURRING
WORKS / COMMUNITY / TRAFFIC_SAFETY / AUTOMOTIVE
Region: 水島
hands_on: MEDIUM-HIGH

Evidence:
https://www.mitsubishi-motors.co.jp/carlife/calendar/2026/pajero/okayama.html
https://www.mitsubishi-motors.com/jp/sustainability/society/contribution/report/2024/11/29.html
https://west-mitsubishi-motor-sales.com/
https://www.mitsubishi-motors.com/jp/sustainability/society/contribution/report/2023/09/04.html

GROWgle note:
既知の基準イベントを正式に再発見。学校限定工場見学とは別ACTIVITYとして保持する。
「工場見学SOURCE」「出前授業SOURCE」「地域感謝祭SOURCE」が同一企業内に併存する代表例。

### 倉敷化工 — HIGH_VALUE / SCHOOL_ONLY / RECURRING_CANDIDATE
2026企業学び楽舎で体験内容を具体確認。
- 紙・ペットボトルキャップ等で4種類の構造模型を制作
- 制震・免震・耐震の違いを、実際に模型を揺らして比較
- 身近な建物の耐震構造と企業技術を接続

別ルート:
- 倉敷観光WEBが、近隣小学校の要望を受けた社会科工場見学を紹介
- 本社工場で機械設備と部品→製品工程を学習
- 一般向け工場見学は不可

Classification:
SCHOOL_ONLY / RECURRING_CANDIDATE
ELEMENTARY / JUNIOR_HIGH
STEAM / WORKS / DISASTER_PREVENTION / MECHANICAL_ENGINEERING
hands_on: HIGH
Region: 水島・連島

Evidence:
https://kuratoco.com/article-178068/
https://www.kurashiki-tabi.jp/rm_experience/rm-experience49/
https://www.kuraka.co.jp/

GROWgle note:
防振・免震を工作で理解させるため、建設系とは異なる「材料・機械・防災STEAM」SOURCE。

### 水島鋼板工業 — RECURRING confirmed
企業公式で複数年継続を確認。

2023:
- 黒崎中1・2年
- マイクロメータ／ノギスで鋼板の厚さ・幅を測定

2024:
- 福田南中・南中
- 鉄の厚さ・長さ測定
- 鉄を曲げる体験

2025:
- 水島中で日本非破壊検査と企業学び楽舎
- 安全防護具着用等
- 真備陵南高校でも職業講座

Classification:
SCHOOL_ONLY / RECURRING_CONFIRMED
JUNIOR_HIGH / HIGH_SCHOOL
WORKS / STEAM / METROLOGY / STEEL
hands_on: VERY_HIGH
Region: 水島

Evidence:
https://www.mizuko.co.jp/information/detail.php?id=33&page=3
https://www.mizuko.co.jp/information/detail.php?id=40
https://www.mizuko.co.jp/information/
https://www.kurashiki-oky.ed.jp/mizushima-j/2025-1manabi.html

GROWgle note:
「測る」「曲げる」「安全装備」という非常に具体的な製造技能体験。製造系Hands-on比較の基準SOURCE候補。

### 川崎学園 — VERY_HIGH_VALUE / OPEN_PUBLIC / LONG_RUNNING
「かわさき夏の子ども体験教室」は2009年から開催履歴を確認。
2026:
- 8月18・19日
- 小1〜4: 午前
- 小5〜中学生: 午後
- 各日65名
- 無料、抽選
- 災害救助体験
- 医師体験
- 看護師体験
- ドクターヘリ見学
- ライフサイエンスへの関心と将来の学びの動機づけが目的

Classification:
OPEN_PUBLIC / FAMILY / LONG_RUNNING_RECURRING
ELEMENTARY / JUNIOR_HIGH
MEDICAL / STEAM / EMERGENCY / CAREER
hands_on: VERY_HIGH
Region: 中庄 / 松島

Evidence:
https://k.kawasaki-m.ac.jp/data/summer/
https://k.kawasaki-m.ac.jp/data/summer2026/summer_dtl/
https://www.city.kurashiki.okayama.jp/cityinfo/publicity/1001929/1001937/1022190/1025520/1025522.html

### 川崎リハビリテーション学院 — OPEN_PUBLIC / HIGH_VALUE
2026夏休み:
- 小4〜6: 24名
- 中学生: 12名
- 無料
- リハビリ検査体験
- 治療器具作成

Classification:
OPEN_PUBLIC
ELEMENTARY_HIGH / JUNIOR_HIGH
MEDICAL / REHABILITATION / STEAM / WORKS
hands_on: VERY_HIGH
Region: 中庄 / 松島

Evidence:
https://www.city.kurashiki.okayama.jp/cityinfo/publicity/1001929/1001937/1022190/1025520/1025522.html

### ふるいち — VERY_HIGH_VALUE / MULTI-AGE / RECURRING
2026企業学び楽舎:
- 中高生向け職業体験授業
- 代表による「働くとは何か」「働く楽しさ」の講話
- 倉敷名物ぶっかけうどんの盛り付け体験
- 2026-09-11 連島中
- 2026-09-25 玉島西中

別活動「キッズうどん教室」:
- 地元幼稚園・保育園対象
- 2024開始
- 2024〜2026の3年間で6回
- 園児延べ210名
- 2026年11月にも新たに2園予定
- 地域の食文化を体験で継承

Classification:
SCHOOL_ONLY / PRESCHOOL / JUNIOR_HIGH / HIGH_SCHOOL / RECURRING
FOOD / LOCAL_CULTURE / CAREER / COMMUNITY
hands_on: HIGH

Evidence:
https://www.atpress.ne.jp/news/619851
https://www.atpress.ne.jp/news/631300
https://kuratoco.com/kigyomanabigakusya/

GROWgle note:
幼児→中高生まで同じ企業が年齢別活動を持つ。地域食文化SOURCEとしても強い。

### ドルフィン・エイド — SCHOOL_ONLY / CHILDCARE_CAREER
企業学び楽舎で保育の仕事を題材に:
- スライム作り
- 感触遊び
- 子どもの遊びを通したコミュニケーション
を中学生が体験。

Classification:
SCHOOL_ONLY
JUNIOR_HIGH
CHILDCARE / WORKS / CREATIVE
hands_on: HIGH

Evidence:
https://kuratoco.com/kigyomanabigakusya/

### 玉島信用金庫 — OPEN_PUBLIC / CURRENT_2026 confirmed
2026公式サイトで複数の子ども向け企画を確認。
- 7月「キッズマネースクール2026」
- 7月 本店営業部 夏休みワークショップ「マグネット黒板づくり」
- 8月「たましんpresents マジックショー」
- 「子育て応援project〜未来を担う子どもの力でより良い街に〜」
- 「こどものみらい古本募金」
- 過年度にもジュニア倶楽部サマースクール等

Classification:
OPEN_PUBLIC_OR_MEMBER / RECURRING
ELEMENTARY / FAMILY
FINANCIAL_LITERACY / CREATIVE / COMMUNITY
Region: 玉島

Evidence:
https://www.shinkin.co.jp/tamashima-sk/
https://www.shinkin.co.jp/tamashima-sk/info/

### 行雲 — SOURCE_CANDIDATE / LOCALITY_STRONG, ACTIVITY_VERIFY
企業学び楽舎64社に参加。
企業公式では倉敷美観地区を拠点に:
- 古民家飲食
- 地域商社
- 岡山・倉敷資源の商品企画
- 岡山くだものミュージアム
- 地域への還元を企業方針として明記

Classification:
LOCAL_INDUSTRY / TOURISM / FOOD / ENTRE
Status:
企業学び楽舎内の具体的体験内容、子ども向け独自企画は次回確認。
「地域商社」「商品企画」系PBL候補としてHIGH_WATCH。

Evidence:
https://ko-un.jp/
https://ko-un.jp/about-us/
https://ko-un.jp/regional_trade/

## 26. Batch 4 structural findings

1. 三菱自動車感謝祭を正式に再発見できたため、既知benchmark 2件（JFE / 三菱）の再現性を確保。
2. 企業学び楽舎の逆引きでは「同一企業に複数の教育入口」があることが繰り返し確認される。
3. 水島鋼板工業のような中小製造企業でも複数年継続が明確。大企業だけをRECURRING SOURCEとみなすべきではない。
4. ふるいちは幼児〜高校生まで年齢階層を跨ぐ地域食文化・キャリアSOURCE。
5. 川崎学園は2009年からの開催履歴があり、医療系OPEN_PUBLICの長期継続SOURCEとして最重要級。
6. 倉敷化工の免震工作は、防災×ものづくり×STEAMの交差領域。
7. OPEN_PUBLIC / SCHOOL_ONLY / GROUP_BOOKINGの区別は必須。一般家庭が直接参加できる機会と学校経由のみの機会を混ぜない。

## 27. Next exploration route

次は、企業学び楽舎64社の未深掘りを継続しつつ、企業名起点だけでなく以下の逆方向探索へ進む。

- 倉敷商工会議所 / 玉島商工会議所 / 児島商工会議所等の子ども・学生向け事業
- 水島コンビナート協議体
- 児島繊維業界団体
- 企業スポーツチーム
- 企業博物館 / PR館
- 学校サイトの社会見学・探究・職場体験から企業名を抽出
- 大学PBL成果物から企業名を抽出
- 2024〜2026の「夏休み」「感謝祭」「フェスタ」「工場祭」を企業横断検索



## 28. Network / chamber / emerging-source batch — 2026-10-05

企業単体の逆引きから、商工会議所・学校・地域産業網側からの逆引きへ拡張。

### 倉敷商工会議所 建設委員会 × 岡山県建設業協会倉敷支部 — RECURRING / OPEN_PUBLIC
2025と2026の連続開催を確認。
イベント:
- 「見てさわって学べる！はたらく車 乗車体験イベント」
- 小4〜6と保護者
- 無料
- 重機見学・乗車
- 木工制作
- 2026はショベルカー、ダンプ、高所作業車等11台
- 2026で2回目

Classification:
OPEN_PUBLIC / FAMILY / RECURRING
ELEMENTARY_HIGH
WORKS / INFRASTRUCTURE / CAREER / CREATIVE
COLLABORATION: CHAMBER_X_INDUSTRY_ASSOCIATION_X_EDUCATION
hands_on: VERY_HIGH

Evidence:
https://www.kura-cci.or.jp/event/event-24351/
https://www.jcci.or.jp/news/news/2026/0910164726.html
https://www.kura-cci.or.jp/event/event-20046/

GROWgle note:
個社ではなく業界団体が複数企業の仕事をまとめて子どもへ開く「INDUSTRY_GATEWAY SOURCE」。

### 玉島商工会議所 × 金光学園 — 職業クエスト / PBL
2026「職業クエスト」:
- 中等部14歳
- 5〜10名程度で地域事業所を訪問
- 現場見学
- 企業が抱える課題を持ち帰る
- 生徒グループが解決策を考える
- 商工会議所が参加企業を募集

Classification:
SCHOOL_ONLY / PBL
JUNIOR_HIGH
ENTRE / WORKS / COMMUNITY
COLLABORATION: CHAMBER_X_SCHOOL_X_COMPANY
hands_on: HIGH
Status: SOURCE_NETWORK / 参加企業は実施後に追跡

Evidence:
https://www.tamashima-cci.or.jp/news/o-828.html

GROWgle note:
「職場を見る」から「企業課題を解く」へ一段深い。企業×中学生PBLの標準モデル候補。

### 玉島商工会議所 — 地域文化体験SOURCE
2025・2026の連続開催を確認:
- 西爽亭「お抹茶点て方体験」
- 小学生以上
- 2026年度は5月〜翌3月に複数回
- 和菓子製作体験付き回あり

Classification:
OPEN_PUBLIC / RECURRING
ELEMENTARY_PLUS / FAMILY / GENERAL
CULTURAL_ASSET / COMMUNITY
Region: 玉島

Evidence:
https://www.tamashima-cci.or.jp/news/i-97.html
https://www.tamashima-cci.or.jp/news/i-92.html

### 児島商工会議所 × 倉敷市立短期大学 — RECURRING
児島繊維産業未来Vision委員会が倉敷市立短期大学との連携強化として合同企業説明会を継続。
- 2024
- 2025
- 2026
と3年継続を確認。
目的:
- 学生に児島の事業所を知ってもらう
- 地元企業への就職関心を高める
- 企業と学生の交流

Classification:
STUDENT_ONLY / RECURRING
UNIVERSITY / JUNIOR_COLLEGE
LOCAL_INDUSTRY / TEXTILE / CAREER
COLLABORATION: CHAMBER_X_UNIVERSITY_X_COMPANY

Evidence:
https://www.kojima-cci.or.jp/info/20260116-kuratangoudoukigyousetsumeikai.html

### 児島商工会議所 — ものづくり体験ハブ
公式「体験する」ページから、企業学び楽舎とは別の常設・予約型SOURCE群を再確認。
- 髙田織物: 畳縁製造工程、ミニ畳づくり。小学生以上、団体最大48名
- BIG JOHN: 藍染め・デニム加工
- ベティスミス: リベット打ち
- 浦上染料店 / どんぐり工房: 藍染め
- 児島学生服資料館: 学生服・セーラー服試着
- 野﨑家塩業歴史館: 塩づくり

Classification:
GROUP_BOOKING / OPEN_PUBLIC_MIXED / CONSTANT
ELEMENTARY_PLUS / FAMILY / SCHOOL
LOCAL_INDUSTRY / TEXTILE / CREATIVE / CULTURE

Evidence:
https://www.kojima-cci.or.jp/sightseeing/experience

### クラレ 倉敷事業所 — LONG_RUNNING / MULTI-ACTIVITY
公式CSRで強く確認。

少年少女化学教室:
- 1992年開始
- 毎年開催
- 小学生対象
- 2025年に国内累計参加者1万人超
- 倉敷事業所では「おもしろかがく館」
- 社員ボランティアが講師・アシスタント

倉敷事業所の地域交流:
- クラレ杯子ども会球技大会
- サマーフェスタ
- クリスマスファンタジー
- 地域小学校・こども園への支援
- 「小鳥の森」による環境・生物多様性教育資源候補

2025クリスマスファンタジー:
- 1990年開始、2025年で通算34回
- 地域一般来場可能

Classification:
SCHOOL / OPEN_PUBLIC / RECURRING_LONG_RUNNING
ELEMENTARY / FAMILY / COMMUNITY
STEAM / CHEMISTRY / SPORTS / COMMUNITY / NATURE
Region: 玉島乙島

Evidence:
https://www.kuraray.com/jp-ja/sustainability/3p/relationship_with_society/
https://www.kuraray.com/jp-ja/news/2025/1215_2/
https://100th.kuraray.com/ja/

GROWgle note:
一企業で「化学」「スポーツ」「地域祭」「自然」「イルミネーション」の複数入口を持つため、SOURCE→ACTIVITY分離の代表例。

### 旭化成 水島製造所 — FACTORY + SPORTS + SCIENCE
工場見学:
- 小学生高学年以上
- 10〜40人程度
- 45分
- 製造所紹介、概要、車窓プラント見学
- 1か月前予約

地域教育:
- 水島製造所が岡山県で旭化成柔道教室を企画
- 世界レベルの柔道部員が地域の子どもへ直接指導
- 製造所は以前から地元中学生へのスポーツ活動支援
- 環境保全や化学の楽しさを伝える出前授業も実施

Classification:
GROUP_BOOKING + SCHOOL / RECURRING_SOURCE
ELEMENTARY_HIGH / JUNIOR_HIGH / CHILD
STEAM / CHEMISTRY / SPORTS / LOCAL_INDUSTRY
hands_on: MEDIUM-HIGH

Evidence:
https://www.kurashiki-tabi.jp/rm_experience/rm-experience46/
https://www.asahi-kasei.com/jp/asahikasei-brands/stories/judo

### JFEスチール — SPORTS layer追加
公式社会貢献活動:
- 各製鉄所・製造所で福利厚生施設を地域へ開放
- 陸上、サッカー、野球、バレー、バスケ等の地域大会
- 2025年度: 22大会、約9,100人参加（全社）
- 硬式野球部等が子ども向け教室
- 中高生向け指導も実施
- 倉敷地区発の「アクティブ体操」「安全体力」も教育現場へ展開

Kurashiki-specific activity countsは個別確認継続。

Classification:
SPORTS / HEALTH / COMMUNITY / EDUCATION
SOURCE_LEVEL_CONFIRMED
LOCAL_ACTIVITY_COUNT: VERIFY

Evidence:
https://www.jfe-steel.co.jp/company/csr.html

### 水島港みなと親子学習会 — PORT / LOGISTICS NETWORK
2026-10-24:
- 水島港玉島ハーバーアイランド周辺
- 小学生＋保護者
- 24人
- 無料
- 船で港を探検
- 港湾について学習
- 中国地方整備局 宇野港湾事務所

Classification:
OPEN_PUBLIC / FAMILY
ELEMENTARY
WORKS / LOGISTICS / INFRASTRUCTURE / PORT
Region: 玉島ハーバーアイランド
Note:
企業主催ではないが、港湾企業群への入口となるNETWORK SOURCE。

Evidence:
https://www.city.kurashiki.okayama.jp/cityinfo/publicity/1001929/1001937/1022190/1027202/1027203.html

### 日本エアロフォージ — NEW VERY_HIGH_VALUE SOURCE
学校・企業双方から2026活動を確認。

2026-07-31 倉敷市民講座:
- 小5・6
- 20名
- 無料
- 玉島ハーバーアイランド工場
- 世界有数の5万トン大型鍛造プレス
- 航空機パーツの製造工場を見学

企業公式:
- 2026-06 笠岡工業高校工場見学
- 学生向け工場見学を随時受付
- 1日インターン、長期インターン相談可
- 2025-11 従業員家族向け工場見学会を2日開催

Classification:
OPEN_PUBLIC_LIMITED + STUDENT + SCHOOL + FAMILY_INTERNAL
ELEMENTARY_HIGH / HIGH_SCHOOL / UNIVERSITY_STUDENT
STEAM / WORKS / AEROSPACE / MATERIALS / FORGING
hands_on: OBSERVATION_HIGH
Region: 玉島ハーバーアイランド

Evidence:
https://www.kurashiki-oky.ed.jp/tamashima-ph/natu_kouza2016_2.html
https://japan-aeroforge.com/
https://japan-aeroforge.com/recruit/
https://japan-aeroforge.com/2025/11/24/2714/

GROWgle note:
玉島に「航空宇宙・大型鍛造」という新しい地域学習カテゴリが存在。非常に強いLOCAL_INDUSTRY資源。

### 岐阜プラスチック工業 倉敷工場 — NEW SOURCE
2026:
- 倉敷市立工業高校1年生が工場見学

過去:
- 倉敷工業高校電子機械科2年生が工場見学
- 最先端デジタル技術を導入した工場設備、原料、製品、環境対応を学習
- 同校卒業生が就職し、仕事内容・社会人生活を説明
- 同社高卒採用サイトにも「高校2年時の倉敷工場見学が入社のきっかけ」とする社員例

Classification:
SCHOOL_ONLY / HIGH_SCHOOL
WORKS / STEAM / PLASTICS / DIGITAL_MANUFACTURING
RECURRING_CANDIDATE
Region: 倉敷

Evidence:
https://www.kurashiki-oky.ed.jp/kogyo-h/news.html
https://www.kurako.okayama-c.ed.jp/wordpress/?p=65410
https://www.risu.co.jp/recruit/high-school/

### ニッパツ水島 — NEW SOURCE / HIGH_SCHOOL_OPEN_COMPANY
2026:
- 倉敷市立工業高校2年生が工場見学

2024企業公式:
- 岡山県内高校1〜3年と保護者向けオープンカンパニー
- 工場見学＋質問会
- 1回4名
- 複数日開催

Classification:
HIGH_SCHOOL / FAMILY_COMPANION
WORKS / AUTOMOTIVE_PARTS / CAREER
RECURRING_CANDIDATE
Region: 水島

Evidence:
https://www.kurashiki-oky.ed.jp/kogyo-h/news.html
https://nhkseating-mizushima.co.jp/info/%E3%82%AA%E3%83%BC%E3%83%97%E3%83%B3%E3%82%AB%E3%83%B3%E3%83%91%E3%83%8B%E3%83%BC%E3%81%B8%E3%81%AE%E5%8F%82%E5%8A%A0%E3%81%AE%E3%81%8A%E7%9F%A5%E3%82%89%E3%81%9B/

### 田中商会 — NEW RECYCLING SOURCE
2026:
- 公式NEWSで「くらしき市民講座」で工場見学受入を確認
- 玉島工場を含む複数拠点で資源リサイクル
- 市民学習センターでは過去にも水島エコワークス＋田中商会玉島工場のリサイクル工場見学ツアーを実施

Classification:
GROUP / MUNICIPAL_PROGRAM
GENERAL / FAMILY_CANDIDATE
NATURE / STEAM / CIRCULAR_ECONOMY / WORKS
Region: 玉島 / 水島 / 中島
REPEAT_LIKELY

Evidence:
https://tanaka-rc.co.jp/
https://www.kurashiki-oky.ed.jp/lpk-shimin-gakushu-c/documents/izanai62.pdf

## 29. School-side reverse discovery findings

学校側サイトから企業を探索すると、企業学び楽舎64社に含まれないSOURCEが新たに出ることを確認。

2026 倉敷市立工業高校:
- 岐阜プラスチック工業 倉敷工場
- ニッパツ水島
- 洋服の青山 倉敷総本店（着こなし・社会人マナー）

2026 倉敷翔南高校:
- シモハナ物流
- 倉敷芸術科学大学
- 倉敷アイビースクエアで進路ガイダンス

過年度学校実績:
- 大阪富士工業 水島支店
- ENEOS水島による小学校観劇支援

これらはすべて「企業学び楽舎母集団外から見つかる企業教育接点」。
今後、学校サイトを企業発見センサーとして定常利用する。

Evidence:
https://www.kurashiki-oky.ed.jp/kogyo-h/news.html
https://www.kurashiki-oky.ed.jp/kurashiki-shonan-h/blog.html
https://www.kurashiki-oky.ed.jp/kogyo-h/news-r7.html
https://www.kurashiki-oky.ed.jp/mizushima-e/r0_00.html

## 30. Batch 5 structural findings

1. 商工会議所はイベント告知媒体ではなく、複数企業を束ねる教育SOURCEとして扱うべき。
2. INDUSTRY_GATEWAY（建設業界、児島繊維等）を設定すると企業単体検索より効率よく裾野を広げられる。
3. 玉島に航空宇宙・大型鍛造という強い学習資産を追加。
4. 学校Webサイトは、64社リスト外の企業教育活動を見つける高精度な逆引き元。
5. 企業スポーツは製造業の地域接点として独立カテゴリ価値がある。
6. 市・商工会議所が企業の工場見学を一般親子向けに変換している例があり、企業自身の募集ページだけでは拾えない。
7. 「企業×子ども」探索は、企業公式・学校・自治体・商工会議所の4面照合が必要。

## 31. Next route

- 企業学び楽舎64社の残り未精査
- 水島コンビナート8社: 三菱ガス化学を追加深掘り
- 64社外の学校発見SOURCE: 洋服の青山 / シモハナ物流 / 大阪富士工業 / 岐阜プラスチック / ニッパツ水島
- 玉島ハーバーアイランド立地企業を企業リスト化
- 児島商工会議所の繊維産業未来Vision参加企業を抽出
- 倉敷・児島・玉島商工会議所の過去3年イベントアーカイブ横断
- 「企業博物館 / PRセンター / ミュージアム / 資料館」の常設SOURCE探索
- 学校サイトから2024〜2026の工場見学・職場体験先企業を抽出


## 32. Industrial-cluster / permanent-source batch — 2026-10-05

### 児島「こじまファクトリー」 — INDUSTRY_MASTER / VERY_HIGH_VALUE
児島商工会議所 児島繊維産業未来Vision委員会が、児島の繊維関連事業所を技術工程単位で体系化した企業マスターを公開。

2026時点で公式一覧に少なくとも39事業所を確認。
掲載例:
- 明石被服興業
- 菅公学生服
- 浦上染料店
- 髙田織物
- ジャパンブルー
- ショーワ
- 豊和
- 児島
- 日本被服
- セロリー
- ドミンゴ
- COTTLE
- ACID HOUSE
- 桑和
- 晃立
- 荻野製織
- 池田製紐所
- 小倉屋
- マルイ
- マルトク
等。

工程・技術タグ:
- 商品企画
- パターン
- 裁断
- 縫製
- 染色・加工
- 製織
- 仕上げ・アイロン
- 副資材
- 卸売
等。

2026-06-25には「児島地区のインターンシップ受入企業」情報を公開。

Classification:
INDUSTRY_MASTER / COMPANY_NETWORK
TEXTILE / DESIGN / MANUFACTURING / CAREER
Region: 児島

Evidence:
https://www.kojima-cci.or.jp/kojima-factory/
https://www.kojima-cci.or.jp/kojima-factory/company
https://www.kojima-cci.or.jp/kojima-factory/company_cat/industries

GROWgle note:
企業学び楽舎64社とは独立した第三の企業母集団。
児島については「イベントを探す」より先に、この39社を逆引きする方が高再現性。
全39社を一律ACTIVITY扱いせず、教育・見学・インターン等の実績が確認できた企業のみ昇格させる。

### 玉島ハーバーアイランド — INDUSTRIAL_CLUSTER MASTER
倉敷市公式で245ha規模の企業団地として確認。
地域の産業教育上、単一企業ではなく以下のテーマが集積:
- 港湾・国際物流
- 航空宇宙鍛造
- リサイクル
- 食料コンビナート
- 大型製造

既確認SOURCE:
- 日本エアロフォージ
- ヒラキン リサイクルステージ玉島
- 田中商会 玉島工場
- 水島港国際物流センター
- JA西日本くみあい飼料
- J-オイルミルズ
- 全農サイロ

2017以降、JA西日本くみあい飼料・J-オイルミルズ・全農サイロの3社が食料コンビナートを形成。

Classification:
INDUSTRIAL_CLUSTER / LOCAL_SUBAREA
WORKS / LOGISTICS / FOOD / STEAM / CIRCULAR_ECONOMY / AEROSPACE
Region: 玉島

Evidence:
https://www.city.kurashiki.okayama.jp/business/industry/1012624/1011031.html
https://www.pref.okayama.jp/site/chijikaiken/397622.html
https://www.callcenter-kurashiki-city.jp/faq/detail.aspx?id=999

Next:
立地企業を企業マスター化し、工場見学・学校連携・地域イベントを逆引き。

### 水島港国際物流センター — VIEWPOINT / LOGISTICS SOURCE
倉敷市FAQ:
- 事前連絡により屋上から玉島ハーバーアイランド見学可能
- 立地企業・港湾を俯瞰できる

Classification:
GROUP_BOOKING_CANDIDATE / INFRASTRUCTURE
LOGISTICS / PORT
Region: 玉島
Status:
子ども・学校向けプログラムとしての運用条件は要確認。

Evidence:
https://www.callcenter-kurashiki-city.jp/faq/detail.aspx?id=999

### 日本エアロフォージ — continuity strengthened
追加確認:
- 2026-06 岡山県立笠岡工業高校が工場見学
- 企業公式採用ページ: 学生の工場見学を随時受付
- 1日インターン＋長期インターン相談可
- 2025従業員家族工場見学会
- 2026倉敷市民講座: 小5・6対象工場見学

よってSOURCE continuity:
ELEMENTARY → HIGH_SCHOOL → UNIVERSITY/STUDENT
の段階接続が成立。

Evidence:
https://japan-aeroforge.com/
https://japan-aeroforge.com/recruit/
https://www.kasako.okayama-c.ed.jp/wordpress/?p=47809
https://www.kurashiki-oky.ed.jp/tamashima-ph/natu_kouza2016_2.html

### 田中商会 — municipal learning conversion confirmed
2026-07-29 企業公式NEWS:
- 「くらしき市民講座」で工場見学受入

市民学習側では過去に:
- 水島エコワークス
- 田中商会 玉島工場
を組み合わせたリサイクル工場見学ツアーを実施。

Classification:
MUNICIPAL_PROGRAM_X_COMPANY
GROUP_BOOKING / REPEAT_LIKELY
CIRCULAR_ECONOMY / WORKS / NATURE
hands_on: OBSERVATION

Evidence:
https://tanaka-rc.co.jp/
https://www.kurashiki-oky.ed.jp/lpk-shimin-gakushu-c/documents/izanai62.pdf

### ヒラキン リサイクルステージ玉島 — adult route also confirmed
2026-11-13:
- 倉敷市市民学習センターと商工課水島港振興室連携
- 15歳以上20名
- 無料
- 破砕・選別工程見学

既に小学校高学年以上の工場見学SOURCEとして確認済み。
子ども向け／成人向け双方に地域学習資源として開かれている。

Evidence:
https://www.pal.pref.okayama.jp/pal/search/searchdtl.aspx?stdycd=14141

### 三菱ガス化学 水島工場 — SOURCE_CANDIDATE / EDUCATION_UNVERIFIED
水島コンビナート活性化検討会構成企業。
倉敷市水島海岸通3-10の化学製造拠点。
主要製品分野:
- キシレン異性体
- メタキシレン誘導品
- 特殊芳香族製品
- 多価アルコール類

今回の一次情報検索では、2024〜2026の子ども・学生向け工場見学や出前授業の具体的ローカル実績を確認できず。

Classification:
INDUSTRIAL_SOURCE_CANDIDATE
CHEMISTRY / LOCAL_INDUSTRY
ACTIVITY_STATUS: UNVERIFIED
Do not count as active GROWgle activity yet.

Evidence:
https://www.mgc.co.jp/corporate/access/mf.html

GROWgle note:
「見つからない」と「実施していない」を区別する運用例として保持。

## 33. Permanent / museum-style source findings

### ベティスミス ジーンズミュージアム＆ヴィレッジ
既確認に加え、2026公式サイトで常設性を再確認:
- ジーンズミュージアム
- 日本最古のジーンズ工場
- ジーンズ作り体験
- 家族で利用できる施設群
- 団体・修学旅行対応

Classification:
OPEN_PUBLIC / CONSTANT / MUSEUM_X_FACTORY_X_WORKSHOP
LOCAL_INDUSTRY / TEXTILE / CREATIVE / HISTORY

Evidence:
https://betty.co.jp/

### 三菱自動車 水島製作所 PRセンター
工場見学入口としてPRセンターを常設。
学校見学と出前授業の起点。

Classification:
SCHOOL_ONLY / CONSTANT_INFRASTRUCTURE
AUTOMOTIVE / WORKS / STEAM

Evidence:
https://www.mitsubishi-motors.com/jp/sustainability/society/contribution/factory/mizushima.html

### 児島学生服資料館
児島商工会議所「体験する」公式リストに常設体験SOURCEとして掲載。
- 学生服・セーラー服試着体験
- 児島の学生服産業史への入口

Classification:
OPEN_PUBLIC_OR_GROUP / CONSTANT
TEXTILE / CULTURE / LOCAL_INDUSTRY

Evidence:
https://www.kojima-cci.or.jp/sightseeing/experience

## 34. School-side new SOURCE candidates

### 岐阜プラスチック工業 倉敷工場
2026倉敷市立工業高校、過去倉敷工業高校の複数年見学実績。
高卒採用公式ページでも、倉敷工場見学が就職動機になった社員事例を確認。

Status:
RECURRING_CANDIDATE → strong

Evidence:
https://www.kurashiki-oky.ed.jp/kogyo-h/news.html
https://www.risu.co.jp/recruit/high-school/

### ニッパツ水島
2026倉敷市立工業高校見学。
企業公式では高校生1〜3年＋保護者対象のオープンカンパニー実績:
- 工場見学
- 質問会
- 複数日
- 少人数

Classification:
HIGH_SCHOOL / OPEN_COMPANY / FAMILY_COMPANION
CAREER / WORKS / AUTOMOTIVE_PARTS

Evidence:
https://nhkseating-mizushima.co.jp/info/%E3%82%AA%E3%83%BC%E3%83%97%E3%83%B3%E3%82%AB%E3%83%B3%E3%83%91%E3%83%8B%E3%83%BC%E3%81%B8%E3%81%AE%E5%8F%82%E5%8A%A0%E3%81%AE%E3%81%8A%E7%9F%A5%E3%82%89%E3%81%9B/
https://www.kurashiki-oky.ed.jp/kogyo-h/news.html

### 洋服の青山 倉敷総本店
2026倉敷市立工業高校4年:
- スーツ着こなし
- 社会人マナー
の出前講座。

Classification:
SCHOOL_ONLY
HIGH_SCHOOL
CAREER / LIFE_SKILLS / RETAIL_SERVICE

Evidence:
https://www.kurashiki-oky.ed.jp/kogyo-h/news.html

### シモハナ物流
2026倉敷翔南高校2年:
- 企業・大学見学で訪問
- キャリア学習

Classification:
SCHOOL_ONLY
HIGH_SCHOOL
LOGISTICS / CAREER
Status:
倉敷拠点での独自教育プログラムは要確認。

Evidence:
https://www.kurashiki-oky.ed.jp/kurashiki-shonan-h/blog.html

## 35. Enterprise-master strategy update

倉敷Pilotの企業母集団は、少なくとも以下の独立リストを統合する。

A. 企業学び楽舎 64組織
B. 水島コンビナート活性化検討会 主要8主体
C. 児島こじまファクトリー 約39繊維事業所
D. 玉島ハーバーアイランド立地企業
E. 学校側から発見した見学・講座受入企業
F. 商工会議所・業界団体経由の参加企業
G. 一般向け産業観光・教育旅行掲載企業

重複を考慮しても、倉敷の企業系探索母集団は100組織規模に達する可能性が高い。
ただし「母集団企業数」と「GROWgle適合ACTIVITYを持つ企業数」は厳密に分けて集計する。

## 36. Next route

- こじまファクトリー39社のうち、工場見学・WS・インターン公開企業を優先抽出
- 玉島ハーバーアイランド企業の全リスト化
- 食料コンビナート3社の学校／親子見学探索
- 水島コンビナート主要企業で未確認の三菱ガス化学をWATCH
- 倉敷クリエイティブパーク、船穂産業団地、市場工業団地も企業マスター化
- 企業博物館／資料館／PRセンターを常設SOURCEとして独立抽出
- 学校側の2024〜2026企業見学先をさらに横断抽出


## 37. Kojima textile deep-dive / current public routes — 2026-10-05

### ジャパンブルー — HIGH_VALUE / CONSTANT_SOURCE
Current corporate CSR page explicitly states:
- 国内外からのデザイン・製造研修受入
- 学校・企業からの職業体験
- 岡山・児島地域での地域貢献活動
- 見学・研修問い合わせ窓口を常設

Factory-tour history:
- 児島製織所の一般・学校・団体向け見学を継続
- 2024年時点で月2回程度の完全予約制見学枠を案内
- 製織工場を中心に、旧式力織機とデニム生地製造を見学
- 大学・専門学校等の見学、国内外インターン受入実績あり

Classification:
GROUP_BOOKING / SCHOOL / STUDENT / WORK_EXPERIENCE
JUNIOR_HIGH+ / UNIVERSITY / GENERAL_GROUP
TEXTILE / DESIGN / WORKS / LOCAL_INDUSTRY
CONSTANT_SOURCE / RECURRING_ACTIVITY
Region: 児島

Evidence:
https://www.japanblue.co.jp/csr.html
https://www.japanblue.co.jp/topics/2760.html
https://www.japanblue.co.jp/topics/393.html
https://www.japanblue.co.jp/contact.html

GROWgle note:
「産地ブランド」だけではなく、製織・縫製・店舗・デザイン・販売まで学べる多工程SOURCE。

### 髙田織物 — VERY_HIGH_VALUE / CONSTANT
Official factory-tour page:
- 営業日の見学可能日に実施
- 団体10〜48名程度
- 小学生以上
- 工場見学のみ無料
- ミニ畳制作を含む体験コースあり
- 整経→製造→艶付け→展示→制作まで一連で見学可能

児島商工会議所も教育・観光体験SOURCEとして掲載。
過去には夏休み時期に小学生参加可の工場見学＋ミニ畳制作ワークショップも開催。

Classification:
GROUP_BOOKING / CONSTANT
ELEMENTARY+ / SCHOOL / FAMILY_GROUP
TEXTILE / CREATIVE / LOCAL_INDUSTRY / CULTURAL_ASSET
hands_on: VERY_HIGH
Region: 児島唐琴

Evidence:
https://ohmiyaberi.co.jp/factorytour/
https://www.kojima-cci.or.jp/sightseeing/experience/tatami.html
https://flat-kojimaberi.com/event/flat_workshop_7_8/

### セロリー — SCHOOL + STUDENT / STRONG CONTINUITY
Current official corporate / social contribution pages:
- 地元小・中学校、高校の会社見学を受入
- 中学生から大学生まで職場体験・インターンシップを受入
- 学校へ残り布を提供
- 地域スポーツイベントのボランティア等

Classification:
SCHOOL_ONLY / STUDENT
ELEMENTARY / JUNIOR_HIGH / HIGH_SCHOOL / UNIVERSITY
TEXTILE / CAREER / COMMUNITY / CIRCULAR_RESOURCE
CONSTANT_SOURCE
Region: 児島

Evidence:
https://www.selery.co.jp/corporate/info/
https://www.selery.co.jp/activity/social_activity.html

GROWgle note:
小学生見学→中高職場体験→大学インターンの年齢連続性が明確な繊維企業。

### BIG JOHN — OPEN + SCHOOL / RECURRING
School / group:
- 小学校・中学校・高校・大学・企業団体のデニム雑貨制作体験を受入
- 修学旅行・校外学習実績あり
- ボタン・リベット打ち、ストラップ、トート等

General public:
- 児島本店で体験系プログラム
- 2024、2025と年末のBIG JOHN感謝祭を連続確認
- 2025感謝祭: しめ縄編み込み、ボタン打ち、塗り絵、Tシャツプリント等
- 2020記事では「毎年年末恒例」と明記
- 2026年開催は2026-10-05時点では公式告知未確認 → WATCH_DECEMBER

Classification:
OPEN_PUBLIC + GROUP_BOOKING / RECURRING
ELEMENTARY / JUNIOR_HIGH / HIGH_SCHOOL / UNIVERSITY / FAMILY
TEXTILE / CREATIVE / LOCAL_INDUSTRY
hands_on: VERY_HIGH
Region: 児島

Evidence:
https://bigjohn.co.jp/blogs/blog/big-john-%E5%85%90%E5%B3%B6%E6%9C%AC%E5%BA%97%E3%81%A7%E3%81%AF%E5%9B%A3%E4%BD%93%E6%A7%98%E3%82%82%E6%89%BF%E3%82%8A%E3%81%BE%E3%81%99
https://bigjohn.co.jp/blogs/blog/big-john%E6%84%9F%E8%AC%9D%E7%A5%ADin-%E5%85%90%E5%B3%B6%E6%9C%AC%E5%BA%97-12%E6%9C%886%E6%97%A5%E9%96%8B%E5%82%AC
https://bigjohn.co.jp/blogs/blog/%E6%84%9F%E8%AC%9D%E7%A5%AD%E4%B8%AD%E6%AD%A2-%E3%81%A8-%E3%81%97%E3%82%81%E7%B8%84%E3%82%AD%E3%83%83%E3%83%88%E7%84%A1%E6%96%99%E9%85%8D%E5%B8%83-%E3%81%AE%E3%81%8A%E7%9F%A5%E3%82%89%E3%81%9B

### 明石被服興業 / AKASHI S.U.C. — PERMANENT SHOWROOM + STUDENT_EVENT
Current official school-facing page:
- 倉敷本社内に学校制服・体育服・作業服・介護服等を年間常設展示
- 学校関係者向け見学案内あり

Past educational event:
- 岡山大学留学生を招き、裁断工場・制服展示場見学
- 各国制服事情ディスカッション
- 学生服着用による地域文化体験

Classification:
GROUP_BOOKING / SCHOOL_RELATION
STUDENT / SCHOOL_STAFF
TEXTILE / CULTURE / DESIGN / LOCAL_INDUSTRY
CONSTANT_SHOWROOM
Region: 児島

Evidence:
https://akashi-suc.jp/school/showroom/index.html
https://akashi-suc.jp/company/newsrelease/webdir/76.html

## 38. New 2026 parent-child industrial visit

### 住友重機械工業 岡山製造所 — OPEN_PUBLIC_LIMITED / PARENT_CHILD
2026-08-04 倉敷市・玉島公民館「くらしき市民講座」:
- 「親子工場見学 ～住友重機械工業㈱ 岡山製造所編～」
- 小学5・6年生＋保護者
- 20組
- 無料
- ギヤボックス製造工場を見学
- 玉島支所産業課連携
- 社員が講師

Classification:
OPEN_PUBLIC_LIMITED / FAMILY
ELEMENTARY_HIGH
WORKS / STEAM / MECHANICAL_ENGINEERING / LOCAL_INDUSTRY
COLLABORATION: COMPANY_X_MUNICIPALITY
Region: 玉島乙島

Evidence:
https://www.kurashiki-oky.ed.jp/tamashima-ph/natu_kouza2016_2.html

GROWgle note:
住友重機械工業は企業学び楽舎64社外だが、市民講座側から発見。自治体講座を企業発見センサーとして使う有効例。

## 39. Current event — 瀬戸内産業芸術祭2026 / 児島

2026-10-03〜10-31:
「瀬戸内産業芸術祭2026」が岡山・愛媛の産業現場を舞台に初開催。
倉敷会場:
- 児島ジーンズストリート協同組合
- 旧野﨑家住宅
- 児島ジーンズストリートの工場・ショップを巡るスタンプラリー型体験
- デニムの原料である綿花→糸→布→縫製→ジーンズという地域産業史をアートとともに体験
- 限定ガイドブック「MADE IN KOJIMA, JAPAN.」
- 全作品事前予約制
- 年齢制限は今回確認できず → GENERAL / AGE_UNVERIFIED

Classification:
OPEN_PUBLIC_ADVANCE_RESERVATION / CURRENT_2026
GENERAL / FAMILY_CANDIDATE
LOCAL_INDUSTRY / TEXTILE / CREATIVE / CULTURAL_ASSET
COLLABORATION: INDUSTRY_ASSOCIATION_X_ART_FOUNDATION
Region: 児島

Evidence:
https://www.sai-art.jp/
https://prtimes.jp/main/html/rd/p/000000012.000186934.html
https://www.okayama-kanko.jp/event/detail_1002827.html

GROWgle note:
「工場・産業現場そのものを文化体験化する」新しいタイプ。
企業教育イベントと観光・芸術祭の境界にあり、地域産業への入口として保持。

## 40. Tamashima Harbor Island master expansion

岡山県公式の立地記録から、既存マスターに追加すべき企業を確認。

2014 food complex:
- JA西日本くみあい飼料
- J-オイルミルズ
- 全農サイロ

2017 newly located:
- 明治
- 岐阜プラスチック工業
- シーアール物流
- アイム
- 上組

Existing / historical industrial assets:
- 日本エアロフォージ
- ナカシマプロペラ 玉島工場
- ヒラキン リサイクルステージ玉島
- 田中商会 玉島工場
- 水島港国際物流センター
- 住友重機械工業 岡山製造所（隣接E地区）

Classification:
INDUSTRIAL_CLUSTER_MASTER
Region: 玉島乙島 / ハーバーアイランド

Evidence:
https://www.pref.okayama.jp/site/160/409663.html
https://www.pref.okayama.jp/site/160/540711.html
https://www.city.kurashiki.okayama.jp/culture/tourism/1001881/1008126/1008137/1008145.html

### 水島港国際物流センター — facility-tour status strengthened
岡山県港湾課公式:
- 玉島ハーバーアイランド国際コンテナターミナルの施設見学を受付
- 水島港国際物流センターへ事前連絡

Classification:
GROUP_BOOKING / CONSTANT
GENERAL_GROUP / SCHOOL_CANDIDATE
PORT / LOGISTICS / INFRASTRUCTURE
Region: 玉島

Evidence:
https://www.pref.okayama.jp/page/detail-43059.html

Status:
学校・子ども向け専用プログラムの有無は未確認。GENERAL_GROUPとして保持。

## 41. Master count / methodology update

こじまファクトリー「業種」ページで、現在の対象事業所数39件を再確認。
その全件を一律ACTIVITYにしない。
以下の順で昇格させる:

1. OPEN_PUBLIC / GROUP_BOOKINGの体験・見学が現行公開
2. 学校見学・職場体験が現行公式で確認
3. インターン受入を現行公式で確認
4. 過去複数年の教育活動があり再開催性が高い
5. 上記未確認は INDUSTRY_SOURCE_CANDIDATE として残す

児島繊維で今回までに高優先SOURCEへ昇格:
- ベティスミス
- BIG JOHN
- 髙田織物
- ジャパンブルー
- 菅公学生服
- セロリー
- 明石被服興業
- 浦上染料店
- 坂本織物
- 松井織物
ほか継続確認中。

## 42. Next route — updated

Priority:
- こじまファクトリー残り企業の教育接点を全件スクリーニング
- 玉島ハーバーアイランド追加企業（明治 / J-オイルミルズ / 全農サイロ / JA西日本くみあい飼料 / 上組 / CR物流 / ナカシマプロペラ）の学校・一般見学逆引き
- 倉敷市内工業団地（倉敷クリエイティブパーク / 船穂産業団地 / 市場工業団地）立地企業マスター化
- 2026現在開催中の企業・産業イベントを別途 CURRENT_ACTIVITY として抽出
- 商工会議所・公民館・市民講座から企業SOURCEを逆発見
- 中学校「チャレンジ・ワーク14」の受入事業所名を学校側記録から抽出


## 43. Tamashima harbor + Kojima textile continuation — 2026-10-05

### ナカシマプロペラ 玉島工場 — INDUSTRIAL_SOURCE / FACTORY_TOUR_NOT_PUBLIC
Current official site:
- 玉島工場: 倉敷市玉島乙島8259-12
- 2005年に大型船用プロペラ製造拠点として完成
- 2026年5月、玉島ハーバーフェスティバルでプロペラ展示
- 一方、公式問い合わせページでは「原則として工場見学の受け入れは行っていない」と明記

Classification:
INDUSTRIAL_SOURCE_CANDIDATE
MARITIME / PROPULSION / ADVANCED_MANUFACTURING
PUBLIC_FACTORY_TOUR: NO_IN_PRINCIPLE
COMMUNITY_EVENT: VERIFIED_2026
Region: 玉島ハーバーアイランド

Evidence:
https://www.nakashima.co.jp/company/office
https://www.nakashima.co.jp/contact
https://www.nakashima.co.jp/news

GROWgle note:
工場見学不可でも、地域フェスで技術展示を行う企業は「教育接点なし」とは扱わない。
ACTIVITY単位で「工場見学不可」「地域イベント展示あり」を分離する。

### 上組 玉島支店 — LOGISTICS_SOURCE / LOCAL_EDU_UNVERIFIED
Current official:
- 水島港を拠点に、港湾荷役・通関・サイロ・定温倉庫・配送まで一貫物流
- 玉島支店・ハーバーアイランド物流センター・複数サイロを保有
- 玉島支店採用窓口あり
- 地域との関わりとして職場周辺清掃活動を公式記載

今回の一次情報検索では、子ども・学校向け見学や職場体験の玉島実績は未確認。

Classification:
INDUSTRIAL_SOURCE_CANDIDATE
LOGISTICS / PORT / FOOD_SUPPLY_CHAIN
ACTIVITY_STATUS: LOCAL_EDUCATION_UNVERIFIED
Region: 玉島ハーバーアイランド

Evidence:
https://www.kamigumi.co.jp/company/domestic/tamashima/
https://www.kamigumi.co.jp/recruit/entry/

### 全農サイロ 倉敷支店 — LOGISTICS / FOOD_INFRASTRUCTURE SOURCE
Current official:
- 玉島ハーバーアイランドの食料コンビナート
- サイロ110,000トン
- 120,000トン級本船バース
- 穀物・大豆ミール等を扱う大規模物流拠点

今回、子ども・学校向け見学の現行公開情報は未確認。

Classification:
INDUSTRIAL_SOURCE_CANDIDATE
FOOD / PORT / LOGISTICS / AGRICULTURE_INFRASTRUCTURE
ACTIVITY_STATUS: UNVERIFIED
Region: 玉島ハーバーアイランド

Evidence:
https://www.zsilo.co.jp/company/access/

### J-オイルミルズ 倉敷工場 — FOOD_INDUSTRY SOURCE
Official corporate release:
- 玉島乙島新湊8266
- 大豆搾油拠点
- JA西日本くみあい飼料、全農サイロと食料コンビナートを形成

今回の一次情報検索では、倉敷工場の子ども・学校向け工場見学は未確認。

Classification:
INDUSTRIAL_SOURCE_CANDIDATE
FOOD / AGRICULTURE / MANUFACTURING
ACTIVITY_STATUS: UNVERIFIED

Evidence:
https://www.j-oil.com/press/article/210512_002577.html

### 明治 倉敷工場 — FOOD / SPORTS_NUTRITION SOURCE
Official release:
- 玉島ハーバーアイランドにスポーツ栄養製品（ザバス等）の生産工場
- Current Meiji public factory-tour network lists other designated “なるほどファクトリー” sites, but 倉敷工場 is not in that public-tour list.

Therefore:
- 玉島工場の存在は確認
- 一般工場見学は現時点で確認できず
- 全国の明治工場見学制度を倉敷へ自動適用しない

Classification:
INDUSTRIAL_SOURCE_CANDIDATE
FOOD / SPORTS_NUTRITION / MANUFACTURING
PUBLIC_TOUR_STATUS: UNVERIFIED / NOT_LISTED_IN_PUBLIC_FACTORY_NETWORK

Evidence:
https://www.meiji.co.jp/corporate/pressrelease/2018/20180213_01.html
https://www.meiji.co.jp/learned/factory/

### シーアールグループ / 岡山シーアール物流 玉島 — LOGISTICS_SOURCE
Current official:
- 倉敷営業所: 玉島乙島新湊8263-29
- 飼料原料・家畜飼料配送等の物流
- 採用サイトに「会社説明・見学会」「長期インターンシップ」の導線あり
- 玉島・水島エリア求人を継続

ただし今回、子ども・中高生向けの玉島地域教育活動は未確認。

Classification:
INDUSTRIAL_SOURCE_CANDIDATE / STUDENT_CAREER_CANDIDATE
LOGISTICS / FOOD_SUPPLY_CHAIN
LOCAL_CHILD_ACTIVITY: UNVERIFIED

Evidence:
https://cr-logi.co.jp/group/okayama/
https://cr-logi.co.jp/recruit/entry/search_2.php

### ショーワ — STUDENT_FACTORY_VISIT / DENIM_PROCESS
岡山県公式で2024年のファッション専門校エスモード学生による工場見学を確認。
- 倉敷市児島稗田町
- デニムの染色・織布
- 専門学生が製造工程を見学

さらに2025年、児島観光ガイド協会が地域産業研修として工場見学。
- 整経
- 糸染色
- 分繊・サイジング
- 自動織機
- 生地仕上げ
を見学。

Classification:
STUDENT / PROFESSIONAL_EDUCATION / GROUP_VISIT
TEXTILE / STEAM / LOCAL_INDUSTRY
REPEAT_LIKELY
Region: 児島

Evidence:
https://www.pref.okayama.jp/page/931540.html
https://kojimaguide.com/showa/

GROWgle note:
一般公募型ではないが、専門教育・地域ガイド研修を受け入れる産業教育SOURCEとして昇格。

### ジョンブル — STUDENT_FACTORY_VISIT / RECURRING
岡山県公式で:
- 2019
- 2023
- 2024
- 2025
にファッション専門校学生の児島工場見学を確認。
主な学習:
- ジーンズ等の縫製
- 地場デニム産業
- ファッション産業の生産工程

Classification:
STUDENT_ONLY / PROFESSIONAL_EDUCATION
TEXTILE / DESIGN / WORKS
RECURRING_CONFIRMED
Region: 児島

Evidence:
https://www.pref.okayama.jp/page/639385.html
https://www.pref.okayama.jp/page/884679.html
https://www.pref.okayama.jp/page/931540.html
https://www.pref.okayama.jp/page/997814.html

### 豊和 — STUDENT_FACTORY_VISIT / LONG_CONTINUITY
岡山県公式で2019・2023・2024・2025に専門学生のデニム加工工場見学を確認。
- ジーンズの洗い加工
- 岡山デニム産地の製造工程
- 2025は玉野市玉原拠点だが、児島産業ネットワークの教育ルートとして継続

倉敷市立短期大学の過年度研究でも明石被服興業とともに工場見学先として登場。

Classification:
STUDENT / PROFESSIONAL_EDUCATION
TEXTILE / DESIGN / LOCAL_INDUSTRY
RECURRING_NETWORK_SOURCE

Evidence:
https://www.pref.okayama.jp/page/884679.html
https://www.pref.okayama.jp/page/931540.html
https://www.pref.okayama.jp/page/997814.html
https://www.kurashiki-cu.ac.jp/kk/index.php/2021fs4/

Note:
現行拠点が倉敷市外を含むため、Kurashiki point-sourceとしては活動場所を都度確認する。

## 44. Methodology refinement from batch

1. 「工場見学を受け入れない」企業も、地域フェス・技術展示で教育接点を持つ場合がある。
   SOURCE単位で0/1判定せず、ACTIVITY単位に分解する。

2. 産業クラスター企業は、所在地だけでACTIVE SOURCEにしない。
   工場見学・学校連携等が見つからない場合は SOURCE_CANDIDATE のまま保持する。

3. 全国企業の工場見学制度を倉敷拠点へ横展開して推定しない。
   明治のように、公開見学対象工場が限定されている場合がある。

4. 岡山県の産業人材・産地育成事業から、児島企業の教育受入実績を複数年で確認できる。
   自治体「産業振興」側も探索ルートへ常設追加。

5. 一般向けOPEN_PUBLICだけでなく、専門学校・大学生向けの産地研修は「地域産業を次世代へ継承する教育資源」として重要。

## 45. Next route

- こじまファクトリー残企業のうち、学生見学・職場体験・学校連携が見つかる企業を抽出
- 玉島食料コンビナート企業について、学校・大学・行政側から逆検索
- 玉島ハーバーフェスティバル2026の出展企業を抽出し、子ども向け技術展示の有無を確認
- 倉敷クリエイティブパーク / 船穂 / 市場工業団地の企業リスト化
- Challenge Work 14の学校別受入先抽出
