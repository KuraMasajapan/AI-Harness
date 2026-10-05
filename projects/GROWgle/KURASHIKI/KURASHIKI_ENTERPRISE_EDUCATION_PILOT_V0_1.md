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
