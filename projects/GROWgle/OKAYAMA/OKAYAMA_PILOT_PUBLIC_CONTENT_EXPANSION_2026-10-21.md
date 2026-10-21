# GROWgle — Okayama Pilot Public Content Expansion

Date: 2026-10-21
State: ACTIVE
Scope: 岡山県限定パイロット
Goal: Research件数ではなく、GROWgleで実際に表示検討できるPUBLIC contentを増やす。

## 1. Baseline from Pilot v0.7 preview

Pilot preview structure:
- activity cards: 27
- research/community records: 87
- municipalities: 27
- municipalities with any research record: 24 / 27
- no captured content in preview:
  - 和気町
  - 久米南町
  - 新庄村

Important:
The apparent abundance of research records does not equal displayable content.
A large share of research records are SCHOOL_ONLY, historical, unresolved, or prototype-review pending.

Therefore research priority changes to:
PUBLIC_DISPLAYABLE_CONTENT_YIELD > RAW_RESEARCH_COUNT

## 2. Activity-card gap queue from v0.7

### 0 activity cards
- 和気町
- 新庄村
- 久米南町
- 玉野市
- 美作市
- 鏡野町
- 奈義町
- 美咲町
- 備前市
- 早島町
- 瀬戸内市
- 赤磐市

Note:
早島町 has already been recovered by a dedicated Second Pass after v0.7 and now has multiple PUBLIC_LIST candidates.
See:
`projects/GROWgle/OKAYAMA/HAYASHIMA_SECOND_PASS_2026-10-21.md`

### 1 activity card
- 津山市
- 新見市
- 笠岡市
- 勝央町
- 吉備中央町
- 高梁市
- 浅口市
- 矢掛町

### 2+ activity cards
lower priority unless CURRENT/public accessibility is weak.

## 3. Priority policy

For the Okayama Pilot, prioritize:
1. municipalities with 0 displayable activity cards
2. municipalities with 1 card only
3. municipalities whose records are mostly SCHOOL_ONLY / WATCH / historical
4. current OPEN_PUBLIC / direct-family opportunities
5. recurring public SOURCEs capable of generating future cards

Do not lower publication quality merely to increase counts.

Public Listing Gate remains mandatory.

---

# 4. ZERO recovery batch 1 — 和気町

## A. 和気町観光りんご園 — 2026 seasonal apple-picking

Current 2026:
- open: 2026-09-02 through late November, while fruit remains
- 09:00–15:00, final entry 14:30
- admission: 500 yen per person age elementary and above
- preschool: free
- take-home fruit charged separately
- 8 varieties / roughly 600 trees in current official tourism information

Classification:
OPEN_PUBLIC / DIRECT_ACCESS
FAMILY / CHILD
AGRICULTURE / FOOD / NATURE / LOCAL_INDUSTRY
SEASONAL_RECURRING
ACCESS_GATE = PASS
FEE_LEVEL = LOW
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Estimated Public Value Score: 80+
Reason:
low-cost direct access + actual harvesting + regional agriculture + seasonal recurrence.

Evidence:
https://www.okayama-kanko.jp/news/detail_305.html
https://www.town.wake.lg.jp/soshiki/sangyoshinko/gyomu/4/5/96.html

## B. 第1回交通安全フェスタ — CURRENT 2026

Current:
- 2026-10-31
- 09:00–12:00
- Wake Town Hall parking area
- children through adults
- anime-based traffic-rule learning
- traffic-safety experience games
- police car / motorcycle photo opportunity
- car inspection learning also available

Classification:
OPEN_PUBLIC
CHILD / FAMILY / GENERAL
LIFE_SKILLS / SAFETY / WORKS
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST

Estimated Public Value Score: high 60s–70s.
Reason:
easy access, direct learning / interactive layer, current event; first edition so recurrence unproven.

Evidence:
https://www.town.wake.lg.jp/news/3393.html

## C. 第24回佐伯タンチョウフェスタ — CURRENT 2026

Current:
- 2026-10-31
- Okayama Prefectural Nature Conservation Center
- admission free except actual expenses
- annual event; 24th edition
- crane-photo / drawing contest recognition
- stage / balloon event / regional festival elements
- Nature Conservation Center simultaneously marks its 35th anniversary and publishes crane / nature learning material

Classification:
OPEN_PUBLIC
FAMILY / GENERAL
NATURE / WILDLIFE / LOCAL_IDENTITY
RECURRING
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST

Estimated Public Value Score: 70s.
Regional uniqueness is especially high because the Nature Conservation Center has a major crane-conservation identity.

Evidence:
https://www.okayama-kanko.jp/event/detail_12706.html
https://www.okayama-shizenhogo-c.jp/news?c=2026-10

## D. 2026 金剛川 水辺の楽校「こどもの夏」

Current-year event:
- 2026-07-19
- 08:00–12:00
- 金剛川水辺の楽校
- long-running event family
- the national river office describes the annual activity family as:
  - fish catching
  - bamboo craft play
  - stone painting
  - water / nature observation

Classification:
OPEN_PUBLIC_FAMILY_ROUTE
CHILD / FAMILY
NATURE / RIVER / MAKING
RECURRING_ANNUAL
CURRENT_2026 = ENDED
PUBLIC_STATUS = WATCH_PUBLIC_NEXT_CYCLE

Evidence:
https://www.town.wake.lg.jp/soshiki/machikeiei/gyomu/7/1_1/1/3130.html
https://www.cgr.mlit.go.jp/okakawa/kawao/kawa/spot/yoshii-spot06.html

## E. 第4回和気町稲刈りまつり — CURRENT 2026 announcement

Current official:
- announcement 2026-10-03
- public direct application via Google Form / email / fax
- hand harvesting of Okayama "Asahi" rice
- traditional sun-drying
- local pesticide-free rice balls + local vegetable miso soup

Classification:
OPEN_PUBLIC_CANDIDATE
AGRICULTURE / FOOD / LOCAL_LIFE / HANDS_ON
CURRENT_2026
ACCESS_GATE = CONDITIONAL
PUBLIC_STATUS = WATCH_PUBLIC pending exact event date / fee / target normalization

Evidence:
https://www.town.wake.lg.jp/news/3376.html

### Wake recovery conclusion

Before:
`WAKE_ACTIVITY_CARDS = 0`

After targeted recovery:
- 3 strong PUBLIC_LIST / PRIORITY candidates
- 1 annual child event WATCH
- 1 agriculture event WATCH pending details

Set:
`WAKE = RECOVERED_NOT_EMPTY / PUBLIC_CONTENT_STRONG`

---

# 5. ZERO recovery batch 1 — 久米南町

## A. 就実大学薬学部 × 久米南町「わくわく科学実験教室」

2026:
- event date: 2026-10-03
- community center hall
- elementary-age children and younger + guardians
- free
- application required
- content:
  - colorful artificial salmon-roe style bead experiment
  - cooling pack experiment
  - slime making
  - additional experiments
- program label: つながる大学連携事業

Classification:
OPEN_PUBLIC / FREE / APPLICATION
CHILD / FAMILY
STEAM / CHEMISTRY / UNIVERSITY_X_MUNICIPALITY
CURRENT_2026 = ENDED
ACCESS_GATE = PASS when recruitment is active
PUBLIC_STATUS = WATCH_PUBLIC_NEXT_CYCLE

Estimated Public Value Score: 70s.
Strong hands-on depth; repeatability must be tracked.

Evidence:
https://www.pal.pref.okayama.jp/pal/search/searchdtl.aspx?knd=1&stdycd=14179

## B. 久米南町図書館「すくすくタイム」

Multiple 2026 dates independently recorded:
- 2026-06-22
- 2026-08-17

Content:
- picture-book reading
- panel theater
- hand-play / songs
- preschool children + guardians
- up to 5 pairs
- reservation through library

Classification:
DIRECT_APPLICATION
PRESCHOOL / FAMILY
READING / PLAY / EARLY_CHILDHOOD
REPEAT_CONFIRMED_2026
ACCESS_GATE = CONDITIONAL
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE / CURRENT_DATE_WATCH

Evidence:
https://www.pal.pref.okayama.jp/pal/search/searchdtl.aspx?stdycd=13841
https://www.pal.pref.okayama.jp/pal/search/searchdtl.aspx?stdycd=14039

## C. 久米南町 recurring parent-child programs

Current FY2026 official child-health / parent-child program page:
- すこやか親子交流会: 3 times/year
  - tasting
  - reading
  - hand-play songs
  - parent interaction
- 子育てにこにこ / すくすく教室: 8 times/year
  - ages 1–3 and 4–5
  - parent-child activity aimed at child development
- 赤ちゃん教室: 3 times/year
  - baby massage etc.
- nursery playground opening: each nursery twice/year

Classification:
LOCAL_CHILD_FAMILY_SOURCE
RECURRING
EARLY_CHILDHOOD / FAMILY
ACCESS_GATE = CONDITIONAL
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE only when direct enrollment / resident conditions and dates are resolved.

Evidence:
https://www.town.kumenan.lg.jp/living/childcare/kosodate/kodomo-kenshin.html

### Kumenan recovery conclusion

Before:
`KUMENAN_ACTIVITY_CARDS = 0`

After:
- science event route discovered
- recurring preschool / family source confirmed
- public content no longer zero

Set:
`KUMENAN = RECOVERED_NOT_EMPTY / STILL_THIN_FOR_ELEMENTARY_PLUS`

Next:
search library / community center / university collaboration / agriculture for elementary and junior-high public activities.

---

# 6. ZERO recovery batch 1 — 新庄村

## A. 新庄村 山まつり（毛無山）2026

2026:
- 2026-08-11
- 毛無山 / 田浪園地
- family attendance confirmed by current-year reporting
- 10 free / paid programs
- examples:
  - forest walk
  - spoon / wood making
  - dyeing / natural-material craft
  - charcoal-making / charcoal grilling
  - forest-related hands-on activity
- current format was newly reorganized in 2026, so annual recurrence in this exact format is not yet fully established

Classification:
OPEN_PUBLIC
FAMILY / GENERAL
NATURE / FOREST / MAKING / LOCAL_CULTURE
HANDS_ON = VERY_HIGH
CURRENT_2026 = ENDED
ACCESS_GATE = PASS for the event
PUBLIC_STATUS = WATCH_PUBLIC_NEXT_CYCLE

Estimated Public Value Score: 80+ if repeated.
Regional uniqueness and hands-on depth are very high.

Evidence:
https://www.okayama-kanko.jp/event/detail_1002619.html
https://tsuyamaasahi.co.jp/
https://news.ksb.co.jp/article/16801722

## B. 新庄村森林セラピー「ゆりかごの小径」

Current direct-access experience:
- 2 km / low elevation-difference forest course
- forest guide required
- children supported / family-compatible
- guide fee: 6,000 yen + 500 yen per participant
- generally guide 1 per 6 participants
- about 2.5 hours
- direct reservation
- natural beech forest / water / bird / forest sensory experience

Classification:
DIRECT_BOOKING
FAMILY / CHILD_COMPATIBLE
NATURE / FOREST / ECOLOGY / WELLBEING
CONSTANT / SEASONAL_CONDITION
ACCESS_GATE = CONDITIONAL
FEE_LEVEL = MODERATE
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE

Reason:
not a child-exclusive program, but family use and child support are explicit and the experience is direct-bookable.
Cost is moderate rather than low, so do not rank above low-barrier events.

Evidence:
https://www.okayama-kanko.jp/spot/detail_11709.html
https://fo-society.jp/facility/okayama/

## C. Seasonal snowshoe experience

2026 winter evidence:
- elementary children can participate
- weekends / holidays
- snow-season only
- reservation at least two weeks ahead
- guided by Shinjo forest-therapy route
- seasonal / snow conditions can cancel

Classification:
DIRECT_BOOKING / SEASONAL
ELEMENTARY+ / FAMILY_CANDIDATE
NATURE / SNOW / FOREST
ACCESS_GATE = CONDITIONAL
PUBLIC_STATUS = WATCH_PUBLIC_NEXT_WINTER

Evidence:
https://qkamura.or.jp/hiruzen/blog/detail/?id=114204

## D. OPEN HOUSE / Bosquerico farm — retain in Research Layer

Current:
- family / children explicitly described as learning through play
- year-round experiences:
  - sarunashi cultivation / harvest / processing
  - soybean cultivation / tofu / miso / harvest
  - nature / wildlife observation
  - basket work / charcoal burning etc.
- direct booking exists for accommodation

But:
- experience price is inquiry-based
- some short activities are tied to accommodation
- access by public transport is difficult

Classification:
HIGH_VALUE_SOURCE
NATURE / AGRICULTURE / LIFE_SKILLS
ACCESS_GATE = FAIL_OR_CONDITIONAL pending standalone child/family experience pricing
PUBLIC_STATUS = RESEARCH_ONLY for now

Evidence:
https://www.okayama-kanko.jp/reserve/detail_101369.html
https://www.okayama-kanko.jp/okatabi/detail_1868.html

### Shinjo recovery conclusion

Before:
`SHINJO_ACTIVITY_CARDS = 0`

After:
- one high-value public annual-event candidate
- one directly bookable family-compatible forest experience
- one seasonal elementary-friendly snow experience
- one high-value but higher-access-difficulty farm SOURCE retained Research-only

Set:
`SHINJO = RECOVERED_NOT_EMPTY / NATURE_SOURCE_STRONG`

---

## 7. Immediate pilot impact

The three completely empty municipalities are no longer research-empty.

Strong / likely displayable additions from this batch alone:
- Wake apple-picking
- Wake traffic-safety festival
- Wake crane festival
- Kumenan science experiment event (next-cycle watch)
- Kumenan preschool recurring route
- Shinjo forest therapy
- Shinjo mountain festival (next-cycle watch)
- Shinjo snowshoe experience (seasonal watch)

In addition, Hayashima recovery has multiple public candidates that are not yet represented in Pilot v0.7 activity cards.

Therefore the immediate bottleneck is no longer "not enough research exists".
It is:
1. normalize newly recovered PUBLIC candidates
2. refresh current date / enrollment state
3. feed them into the Pilot activity-card dataset
4. continue the zero-card queue.

## 8. Next municipalities

Continue 0-activity-card recovery in this order:
1. 玉野市
2. 美作市
3. 鏡野町
4. 奈義町
5. 美咲町
6. 備前市
7. 瀬戸内市
8. 赤磐市

Hayashima is already under active recovery and should be integrated into Pilot data rather than re-researched from zero.


# 9. ZERO-card recovery batch 2 — activity-card promotion candidates

This batch targets municipalities that had research records in Pilot v0.7 but zero activity cards.

The priority is not to create more archival records.
The priority is to identify records that can be promoted to actual Pilot activity cards under the Public Listing Gate.

## A. 鏡野町 — zero-card status is no longer justified

### かがみのスポーツマルシェ — CURRENT 2026

Official current:
- 2026-11-01
- 10:00–15:00
- 鏡野町文化スポーツセンター / かがみのドーム等
- activities explicitly include:
  - pickleball
  - soccer
  - skateboard
  - BMX
  - drone race as e-sports
- local food / market layer also present
- new event in 2026

Classification:
OPEN_PUBLIC / CURRENT_2026
FAMILY / CHILD_COMPATIBLE
SPORTS / DIGITAL / COMMUNITY
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.town.kagamino.lg.jp/soshiki/20/16270.html

### かがみのプレーパーク — CURRENT recurring

Official page updated 2026-10-02:
- regular operation: every other week + one holiday session per month
- regular target: pregnancy / age 0 through preschool parent-child
- holiday session: age 0 through adults
- nature-based free play
- explicit emphasis on:
  - self-directed play
  - creativity
  - challenge
  - failure / recovery
  - interaction with others

Classification:
OPEN_PUBLIC / RECURRING
PRESCHOOL / FAMILY / MIXED_AGE_ON_HOLIDAYS
NATURE / PLAY / COMMUNITY
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://ns1.town.kagamino.lg.jp/site/kosodatesien/12320.html

### Kagamino conclusion
`KAGAMINO_ACTIVITY_CARDS = 0` in v0.7 is obsolete.

Promote at least:
- Sports Marche
- Kagamino Play Park

Set:
`KAGAMINO = PUBLIC_CONTENT_RECOVERED / STRONG`

---

## B. 美咲町 — library network is a current public-content SOURCE

### 美咲町内の図書館をめぐっちゃおう！

Official current:
- 2026-08-29 through 2026-12-06
- all-library common project
- current event index actively promotes participation

Classification:
OPEN_PUBLIC
CHILD / FAMILY_COMPATIBLE
READING / EXPLORATION / COMMUNITY
CURRENT_2026
PUBLIC_STATUS = PUBLIC_LIST

Evidence:
https://www.misaki-lib.jp/

### たのしく防災Day★

Official current:
- 2026-10-24
- central library
- library describes it as a fun disaster-preparedness event

Classification:
OPEN_PUBLIC_CANDIDATE
CHILD / FAMILY
LIFE_SKILLS / DISASTER_PREVENTION
CURRENT_2026
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE

Evidence:
https://www.misaki-lib.jp/

### ぬいぐるみのおとまり会

Official current:
- 2026-10-31
- 柵原図書館
- story reading together with child / stuffed animal
- stuffed animal stays overnight at library afterward
- actively recruiting / inviting participation in current site

Classification:
OPEN_PUBLIC_CANDIDATE
CHILD / FAMILY
READING / IMAGINATION / LIBRARY
CURRENT_2026
PUBLIC_STATUS = PUBLIC_LIST

Evidence:
https://www.misaki-lib.jp/

### Misaki conclusion
The town's library system alone can support multiple current activity cards.
Do not model the three libraries as unrelated one-off event providers; keep:
SOURCE = 美咲町立図書館 network
ACTIVITY = each event.

Set:
`MISAKI = PUBLIC_CONTENT_RECOVERED / LIBRARY_SOURCE_STRONG`

---

## C. 瀬戸内市 — current November public activities

### 第37回 喜之助人形劇フェスタ

Current official:
- 2026-11-21 to 2026-11-22
- 瀬戸内市中央公民館
- advance application required
- 37th edition
- professional puppet-theater troupes from across Japan gather
- city classifies as city/private cultural-art event

Classification:
OPEN_PUBLIC / APPLICATION
CHILD / FAMILY / GENERAL
CULTURE / PERFORMANCE / LOCAL_IDENTITY
RECURRING_LONG_RUNNING
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.city.setouchi.lg.jp/calendar/index.php?d=1&dsp=1&m=11&y=2026

### パパのためのスキルアップ講座「ボール遊びをしよう！」

Current official:
- 2026-11-28
- 邑久スポーツ公園
- target: age 4+ child + father / mother
- 30 pairs
- instructor: Setouchi Blue Shines players
- learn both child communication and physical development through ball play
- advance application required

Classification:
OPEN_PUBLIC / APPLICATION
PRESCHOOL_4_PLUS / FAMILY
SPORTS / PARENT_CHILD / COMMUNICATION
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST

Evidence:
https://www.city.setouchi.lg.jp/calendar/index.php?d=1&dsp=1&m=11&y=2026

### Setouchi conclusion
v0.7 zero activity-card status is obsolete.

Set:
`SETOUCHI = PUBLIC_CONTENT_RECOVERED`

---

## D. 玉野市 — high-value STEAM card confirmed

### 鏡づくりワークショップ

Current official:
- 2026-11-08
- 玉野市役所
- grade 4+
- elementary children require guardian
- fee: 500 yen
- total capacity: 10, split into two sessions
- make a metal mirror by:
  - learning about ancient mirrors
  - pouring alloy into mold
  - polishing

Classification:
OPEN_PUBLIC / APPLICATION
ELEMENTARY_HIGH / JUNIOR_HIGH / HIGH_SCHOOL / GENERAL
STEAM / METAL / ARCHAEOLOGY / CULTURE / MAKING
HANDS_ON = VERY_HIGH
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.city.tamano.lg.jp/soshiki/35/36229.html

### キッズビジネスタウンたまの

Existing current system evidence:
- grade 4+
- annual
- high-school students plan / operate a simulated town
- work -> wages -> tax -> shopping
- current official program description indicates 11th edition in 2026

Public card status:
WATCH_PUBLIC
Reason:
recurring source is strong, but exact 2026 recruitment / event date should be independently resolved before a current activity card is published.

Evidence:
https://www.city.tamano.lg.jp/soshiki/42/42032.html

### Tamano conclusion
At least one immediate activity card can be promoted.

Set:
`TAMANO = PUBLIC_CONTENT_RECOVERED / STEAM_STRONG`

---

## E. 赤磐市 — current parent-child disaster activity

### 親子で学ぶ防災あれこれ

Current official:
- 2026-11-29
- parent-child disaster learning
- cardboard-bed making
- quizzes
- explicit goal:
  "助けられる人から助ける人へ"
- provider: 赤磐市教育委員会 / 西山公民館

Classification:
OPEN_PUBLIC_CANDIDATE
CHILD / FAMILY
DISASTER_PREVENTION / LIFE_SKILLS / COMMUNITY
HANDS_ON = HIGH
GROWTH_ROUTE = PARTICIPATE -> HELP
ACCESS_GATE = PASS subject to final enrollment conditions
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.city.akaiwa.lg.jp/kosodate/sports/syougai/kouminkan/kouza_2/13830.html

### Akaiwa conclusion
v0.7 zero activity-card status can be corrected with a current high-value family activity.

Set:
`AKAIWA = PUBLIC_CONTENT_RECOVERED`

---

## F. 美作市 — current free family-cultural event

### かぼちゃの馬車の人形劇公演会

Current official:
- 2026-11-01
- 10:00
- 作東公民館
- admission free
- no application
- anyone may attend
- provider: volunteer group "かぼちゃの馬車"
- explicitly created to bring dreams / excitement to children
- performance elements are handmade:
  - stage
  - props
  - puppets
  - story
  - live music

Classification:
OPEN_PUBLIC / FREE / NO_RESERVATION
CHILD / FAMILY / GENERAL
CULTURE / PERFORMANCE / HANDMADE_CREATIVE
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.city.mimasaka.lg.jp/soshiki/kyouiku/shakaikyoiku/9011.html

### 美作市 sports / culture SOURCEs

Current official pages also show:
- FY2026 sports class recruitment
- sports youth-group recruitment
- public-hall / library events

Do not bulk-promote these yet.
Use the puppet show as the immediate current card and resolve specific child-access conditions for the recurring classes before promotion.

### Mimasaka conclusion
v0.7 zero card can be corrected immediately.

Set:
`MIMASAKA = PUBLIC_CONTENT_RECOVERED`

---

## G. 奈義町 — current industry festival + long-term child culture route

### 令和8年度奈義町産業まつり

Current official:
- 2026-11-01
- 10:00–14:00
- 奈義中央広場
- explicitly for children through adults
- current content includes:
  - 東山工業祭 company introduction / exhibition
  - science show
  - play park
  - local agriculture / food
  - stamp rally
  - mochi throwing

Classification:
OPEN_PUBLIC
CHILD / FAMILY / GENERAL
WORKS / STEAM / AGRICULTURE / COMMUNITY
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.town.nagi.okayama.jp/kankou/2026sanngyoumaturi_nouringyousai.html

### こども歌舞伎教室 — high-value recurring SOURCE

Official institutional evidence:
- running since 1996
- grades 1 through high school
- recruitment each year
- training starts in August
- children continue to appear in the autumn Yokosen Kabuki performance
- full instruction support from Yokosen Kabuki Preservation Society

Classification:
RECURRING / LOCAL_CHILD_YOUTH
CULTURE / PERFORMANCE / HERITAGE
GROWTH_ROUTE / SKILL_TRANSFER
PUBLIC_STATUS = WATCH_PUBLIC_CURRENT_RECRUITMENT

Evidence:
https://www.town.nagi.okayama.jp/gyousei/kosodate_kyouiku_bunka/bunka/yokosen/tsutaeru.html

Important:
The source page describing the child kabuki system is older (2021 update), so the underlying recurring system is valuable but current 2026 recruitment should be separately verified before making a current enrollment card.

### Nagi conclusion
At least one strong immediate public activity card:
- Nagi Industry Festival

Set:
`NAGI = PUBLIC_CONTENT_RECOVERED / CULTURE_SOURCE_STRONG`

---

## H. 備前市 — strong source, current-card gap is mostly timing

### 備前市埋蔵文化財管理センター workshop SOURCE

Current official confirms:
- the center runs approximately four making workshops per year
- 2026 summer examples:
  - Bizen-yaki making
  - original glass bead / tonbodama making
- public participation
- low to moderate cost
- children can participate with guardian conditions where needed

2026-10-17 / 18 Bizen-yaki Festival-linked outreach also provided:
- original tonbodama strap
- original tote-bag decoration
- about 30-minute sessions

Classification:
RECURRING_PUBLIC_SOURCE
CHILD / FAMILY / GENERAL
STEAM / CREATIVE / ARCHAEOLOGY / LOCAL_CULTURE
PUBLIC_STATUS = WATCH_PUBLIC_NEXT_CURRENT_SESSION

Evidence:
https://www.city.bizen.okayama.jp/site/bizen-maibun/38992.html
https://www.city.bizen.okayama.jp/site/bizen-maibun/39653.html

### 備前市民総合スポーツフェスティバル 2026

Official:
- 2026-10-12
- 09:00–12:00
- free
- no application
- explicitly promoted for families wanting children to try different sports

Classification:
OPEN_PUBLIC / FREE / NO_RESERVATION
CHILD / FAMILY
SPORTS
CURRENT_2026 = ENDED_RECENT
PUBLIC_STATUS = WATCH_PUBLIC_NEXT_CYCLE

Evidence:
https://www.city.bizen.okayama.jp/site/supo-tusinnkougakari/26018.html

### Child/family source network
Current city parenting page (updated 2026-10-01) confirms:
- わくわくるーむ
- うみっこ丸
- しずちゃん家
- 備前プレーパーク！森の冒険ひみつ基地
- multiple nursery / kindergarten open-yard programs
with current monthly communication.

This is an important SOURCE network, but individual public cards require current event-date extraction.

Evidence:
https://www.city.bizen.okayama.jp/soshiki/17/745.html

### Bizen conclusion
Bizen is not content-poor.
Its v0.7 zero-card state is mainly a normalization / CURRENT-timing problem.

Set:
`BIZEN = SOURCE_STRONG / CURRENT_CARD_NEEDS_REFRESH`

---

# 10. Immediate promotion yield from zero-card queue

High-confidence new/current Pilot-card candidates:
1. 鏡野町 — かがみのスポーツマルシェ
2. 鏡野町 — かがみのプレーパーク
3. 美咲町 — 図書館めぐり
4. 美咲町 — たのしく防災Day
5. 美咲町 — ぬいぐるみのおとまり会
6. 瀬戸内市 — 喜之助人形劇フェスタ
7. 瀬戸内市 — 親子ボール遊び
8. 玉野市 — 鏡づくりワークショップ
9. 赤磐市 — 親子防災
10. 美作市 — かぼちゃの馬車 人形劇
11. 奈義町 — 産業まつり

Plus previous recovery:
- 和気町: multiple
- 久米南町: multiple / watch
- 新庄村: multiple / watch
- 早島町: multiple

Interpretation:
Pilot public-card scarcity is now clearly a curation / normalization backlog as well as a research gap.

Before doing broad new research, newly recovered PASS candidates should be fed into the Pilot activity-card dataset in parallel with continued thin-region exploration.

Next:
- normalize Hayashima + this batch into Pilot activity records
- continue one-card municipalities
- continue Bizen current-event extraction
- resolve Nagi / Tamano recurring current recruitment.


# 11. One-card municipality expansion — batch 3

Goal:
upgrade municipalities with only one Pilot v0.7 activity card by finding CURRENT / direct-family public opportunities.

## A. 笠岡市 — agriculture / livestock hands-on layer

### 農フェス 2026

Current official:
- 2026-11-21
- 09:00–15:00
- 笠岡ふれあい青空市 / JA笠岡アグリセンター
- purpose explicitly includes learning about local agriculture / livestock
- activities:
  - butter making (3 sessions, 20 groups each, same-day signup)
  - simulated milking
  - drawing on hay / feed rolls
  - livestock disease-control clothing experience
  - cow-horn accessory workshop
  - large agricultural-machine display / riding
  - quiz rally
  - bus tour
  - agriculture / livestock exhibitions

Classification:
OPEN_PUBLIC
CHILD / FAMILY / GENERAL
AGRICULTURE / LIVESTOCK / FOOD / WORKS / MAKING
HANDS_ON = VERY_HIGH
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.city.kasaoka.okayama.jp/soshiki/29/62572.html
https://www.city.kasaoka.okayama.jp/life/sub/5/index-2.html

Date-verification note:
An older cached rendering of the same URL may show the 2025 edition.
The current city index and current search output identify a 2026-10-09 update and 2026-11-21 event.
When publishing, recheck the live official page once more to avoid cache-version confusion.

### Kasaoka impact
Pilot v0.7 had one activity card.
This adds a region-specific agriculture / livestock hands-on card with very high display value.

---

## B. 勝央町 — immediate free public sports + recurring play SOURCE

### 令和8年度ニュースポーツ教室

Current official:
- 2026-11-21
- 2026-11-28
- child through adult
- preschool requires guardian
- free
- Mollky etc.
- family participation explicitly invited
- electronic / paper application available

Classification:
OPEN_PUBLIC / FREE / APPLICATION
CHILD / FAMILY / GENERAL
SPORTS / COMMUNITY
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.town.shoo.lg.jp/site/kyoiku/7538.html

### きのこの森プレーパーク

Current 2026 program confirms:
- outdoor play / self-discovery / challenge
- elementary children + guardian
- free
- 2026 sessions include fire-making + rice cooking

Current published session checked in this pass is already ended, but SOURCE recurrence is strong.

Classification:
RECURRING_SOURCE
ELEMENTARY / FAMILY
NATURE / LIFE_SKILLS / PLAY
PUBLIC_STATUS = WATCH_PUBLIC_NEXT_SESSION

Evidence:
https://www.town.shoo.lg.jp/site/kyoiku/5254.html

### 勝央町立保育園開放

Current remaining 2026 dates include:
- 2026-11-10
- 2026-12-01
- 2027-03-05
- 10:00–11:00
- prior application period
- five town nursery schools

Classification:
LOCAL_PRESCHOOL_FAMILY
DIRECT_APPLICATION
EARLY_CHILDHOOD / COMMUNITY
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE

Evidence:
https://www.town.shoo.lg.jp/site/kosodate/5077.html

### Shoo impact
Existing Pilot card was focused on entrepreneurship.
This adds SPORTS / NATURE / PRESCHOOL access diversity.

---

## C. 浅口市 — CURRENT high-value public sports card

### 親子ウォーキングサッカー体験会

Current official:
- 2026-11-07
- 14:30–16:00
- ファジアーノ岡山スポーツパーク寄島
- children from preschool age through adults
- child-only participation: elementary+ with guardian
- 60 participants
- free
- current application:
  - city-resident priority: 10/18–10/27
  - common application including nonresidents: 10/28–11/05 if capacity remains
- Fagiano Okayama coaching staff
- ball play / passing / walking-soccer match
- equipment provided

Classification:
OPEN_PUBLIC / FREE / APPLICATION
PRESCHOOL+ / FAMILY / GENERAL
SPORTS / PARENT_CHILD / COMMUNITY
HANDS_ON = HIGH
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.city.asakuchi.lg.jp/page/22937.html

### Existing annual child-experience SYSTEM

2026 child experience classes remain current:
- chorus
- science making
- Japanese drums
- tea ceremony
- etc.
- preschool / elementary / junior-high depending on class
- very low annual fee for many classes

Evidence:
https://www.city.asakuchi.lg.jp/page/10836.html

Public rule:
Do not publish every annual class automatically.
Use individual classes only after current vacancy / application status is resolved.

### Asakuchi impact
Pilot card count can immediately increase with walking soccer while the continuing class system supplies future cards.

---

## D. 新見市 — current family/community participatory festival

### 源流の里 大佐ふるさとまつり 2026

Current official:
- 2026-11-01
- 09:30–14:30
- おおさ総合センター周辺
- participation / experience layer:
  - local elementary students' workshop
  - dojo-sukui
  - work-vehicle exhibition
  - Hoyoku tricycle race
  - local school performances
  - local food / product village

Classification:
OPEN_PUBLIC
CHILD / FAMILY / GENERAL
COMMUNITY / LOCAL_CULTURE / WORKS / PLAY
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST

Evidence:
https://www.city.niimi.okayama.jp/kanko/event/event_detail/index/936
https://www.city.niimi.okayama.jp/kurashi/kurashi_detail/index/726

### にいみde子育て体験事業2026

Current remaining recruitment:
- 2027-01-16 through 02-14 receiving period
- application deadline: 2026-10-30
- 1–2 families
- for non-Niimi residents with children age 1–5
- 1–2 week stay
- child experiences local nursery / nature; family experiences local life
- childcare: 1,800 yen/day per child
- lodging: 2,000 yen/night

Classification:
DIRECT_APPLICATION / SELECTIVE
PRESCHOOL / FAMILY
REGIONAL_LIFE / NATURE / CHILDCARE / MIGRATION_EXPERIENCE
ACCESS_GATE = CONDITIONAL
PUBLIC_STATUS = WATCH_PUBLIC_OR_SPECIAL_FEATURE

Reason:
high experience depth but narrow target and longer stay commitment.

Evidence:
https://www.city.niimi.okayama.jp/gyosei/gyosei_detail/index/16736

### Niimi impact
Existing Pilot single card can be supplemented with an easy-access local festival, while the migration-experience program can be surfaced separately if long-stay opportunities are supported in UI.

---

## E. 矢掛町 — current family / local access layer

### やかげエンジョイウォーキング

Current official:
- 2026-12-13
- free
- 1 km town-walk course still accepting when checked
- other 3.5 km / 6.5 km courses already full
- application deadline: 2026-11-25 or earlier if full
- historic townscape + natural landscape
- finish at Outdoor Village Yakage

Classification:
OPEN_PUBLIC / FREE / APPLICATION
FAMILY / GENERAL
SPORTS / LOCAL_CULTURE / NATURE
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST

Evidence:
https://www.town.yakage.okayama.jp/news/2026/10/1213.html

### 子育て支援センター「あおぞらキッズ」

Current 2026 future dates:
- 2026-10-29
- 2026-11-13
- outdoor free-play / walking at town parks
- parent-child program
- free participation / no advance booking indicated in source description

Classification:
DIRECT_ACCESS_CANDIDATE
PRESCHOOL / FAMILY
OUTDOOR_PLAY / COMMUNITY
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE

Evidence:
https://www.town.yakage.okayama.jp/kosodate/odekake/kosodate-center.html

### イングリッシュデイ

2026 schedule includes:
- 2026-10-24
- 2026-12-19
- 2027-02-06
- elementary / junior-high separate sessions
- ALT country introduction, English games, singing, conversation
- application through school-parent distribution system

Classification:
LOCAL_STUDENT / DIRECT_BUT_SCHOOL_DISTRIBUTED
GLOBAL / COMMUNICATION
PUBLIC_STATUS = RESEARCH_ONLY_OR_LOCAL_CONDITIONAL

Evidence:
https://www.town.yakage.okayama.jp/kosodate/manabi/

Do not treat as unrestricted OPEN_PUBLIC.

### Yakage impact
The town now has current family / sports cards beyond the existing cultural route.

---

## F. 吉備中央町 — public family event pipeline

### ケロポンズファミリーコンサート

Current official calendar:
- 2026-10-31
- 14:00 start
- ロマン高原かよう総合会館
- no advance application indicated in town calendar

Classification:
OPEN_PUBLIC_CANDIDATE
CHILD / FAMILY
MUSIC / PERFORMANCE / MOVEMENT
CURRENT_2026
ACCESS_GATE = CONDITIONAL pending fee / ticket-condition confirmation
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE

Evidence:
https://www.town.kibichuo.lg.jp/calendar/
https://www.town.kibichuo.lg.jp/site/kanko/

### 2026 秋の読書週間

Current:
- 2026-10-24 to 11-08
- children through adults
- library bingo / coloring-sugoroku / reading activities / message-card project
- no special membership condition indicated
- multiple library locations

Classification:
OPEN_PUBLIC
CHILD / FAMILY / GENERAL
READING / COMMUNITY / CREATIVE
CURRENT_2026
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST

Evidence:
https://www.town.kibichuo.lg.jp/site/kibichuolibrary/20925.html

### Parent-child interaction class

Current:
- recurring through FY2026
- 2026-11-12
- 2026-12-07
- small-group parent-child play / making
- reservation required

Classification:
LOCAL_PARENT_CHILD
PRESCHOOL / FAMILY
CREATIVE / DEVELOPMENT / COMMUNITY
ACCESS_GATE = CONDITIONAL
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE only after target / resident conditions are resolved

Evidence:
https://www.town.kibichuo.lg.jp/soshiki/9/19719.html

### Kibi-Chuo impact
Existing one-card representation can be diversified with library / family / early-childhood content.

---

## G. 高梁市 — one SOURCE generates multiple future cards

### たかはし広がる子どもの夢事業

Current official FY2026 program:
- multiple experiential child programs
- future / upcoming items listed as of 2026-10-21:
  - free climbing: around November
  - winter stargazing: around December
  - piano relay concert: 2026-12-19
  - kids pastry-chef class: around February
- earlier 2026 modules included:
  - electronic music-box making
  - manga / illustrator career experience

Classification:
RECURRING_PROGRAM_SOURCE
CHILD / STUDENT
STEAM / CREATIVE / SPORTS / CAREER / FOOD
PUBLIC_STATUS = WATCH_PUBLIC / PROMOTE_EACH_ACTIVITY_WHEN_DETAIL_OPENS

Evidence:
https://www.city.takahashi.lg.jp/site/kyouikuiinkai/hirogarukodomonoyume2026.html

Research interpretation:
Instead of representing the town with only one generic card, this program can generate a rolling set of current cards as each recruitment page opens.

### Takahashi impact
The main issue is not lack of content but failure to explode a strong recurring SOURCE into time-specific public cards.

---

## H. 津山市 — strong SOURCE but current-card extraction still unresolved

### 津山まなびの鉄道館

Current:
- standard public access
- elementary / junior-high: 100 yen
- preschool: free
- recurring special child/family programming in 2026 included:
  - parent-child summer special
  - mini diorama workshop
  - quiz-gacha
  - Yokono-washi lighting workshop
- current news stream active through October 2026

Classification:
CONSTANT_PUBLIC_SOURCE
FAMILY / CHILD
RAILWAY / INDUSTRIAL_HERITAGE / MAKING / LOCAL_CULTURE
PUBLIC_STATUS = PUBLIC_LIST_SOURCE / CURRENT_ACTIVITY_DETAIL_PENDING

Evidence:
https://www.tsuyamakan.jp/manabi/eHUC_PPB

Do not manufacture a November 2026 activity card from the older cached November-event page.
Need next pass:
resolve exact upcoming special event / workshop dates from the 2026 news feed.

### Tsuyama impact
Research is strong; current-event normalization is the remaining bottleneck.

---

# 12. Batch-3 immediate promotion list

High-confidence / current:
1. 笠岡市 — 農フェス 2026
2. 勝央町 — ニュースポーツ教室
3. 浅口市 — 親子ウォーキングサッカー
4. 新見市 — 大佐ふるさとまつり
5. 矢掛町 — やかげエンジョイウォーキング
6. 吉備中央町 — 秋の読書週間

Near-current / source-driven:
7. 吉備中央町 — ケロポンズファミリーコンサート (fee/ticket final check)
8. 高梁市 — 広がる子どもの夢 upcoming modules (activity detail pages)
9. 津山市 — まなびの鉄道館 upcoming special-event detail
10. 勝央町 — 保育園開放
11. 矢掛町 — あおぞらキッズ

Conclusion:
The one-card municipalities are also not truly content-poor.
The Pilot bottleneck remains:
`PUBLIC_CARD_NORMALIZATION + CURRENT_STATE_RESOLUTION`
more than raw discovery alone.

Next:
- resolve remaining 1-card / 2-card towns with CURRENT public yield
- build a promotion-ready queue with exact fields required by Pilot JSON
- prioritize 2026-10-21 onward dates
- separately retain strong recurring SOURCEs for rolling refresh.


# 13. Deepening batch 4 — PUBLIC cards + COMMUNITY records + SOURCE visibility

Purpose:
Do not evaluate pilot richness only through OPEN_PUBLIC event cards.
This batch explicitly captures:
1. current public activity cards
2. non-public / community activity records
3. recurring SOURCEs that explain the regional learning ecosystem

---

## A. 備前市 — daily child-experience infrastructure is stronger than event count suggests

### 備前プレーパーク！森の冒険ひみつ基地

Current official:
- field: natural satoyama in Kugui, with Seto Inland Sea / island views
- opening:
  - Tuesday–Saturday
  - 10:00–15:00
- weather cancellation only
- city describes it as:
  "森でいっぱい遊ぼう！野外の交流ひろば"

Classification:
CONSTANT_PUBLIC_SOURCE
CHILD / FAMILY
NATURE / FREE_PLAY / COMMUNITY / RISK_JUDGMENT
ACCESS_GATE = PASS_OR_LOW_BARRIER
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY / SOURCE_FEATURE

Evidence:
https://www.city.bizen.okayama.jp/site/aka/746.html

Research significance:
This should not be modeled merely as an occasional event.
It is close to a weekly permanent child-experience infrastructure.

### Parent-child gathering network

Official current:
- わくわくるーむ
- うみっこ丸
- しずちゃん家
- 子育て支援センター

For preschool children + guardians:
- direct drop-in / local use
- recurring weekday opening
- monthly activity calendar
- parenting consultation / play / interaction

Current hours include:
- わくわくるーむ: 10:00–15:00 on weekday / alternate-Saturday pattern
- うみっこ丸: weekdays 09:00–14:00
- しずちゃん家: weekdays 09:00–14:00
- 子育て支援センター: recurring week / weekend opening

Classification:
EARLY_CHILDHOOD_SOURCE_NETWORK
PRESCHOOL / FAMILY
COMMUNITY / PLAY / PARENT_SUPPORT
CONSTANT

Display:
SOURCE layer + selected current activities
Do not create a separate event card for every routine opening.

Evidence:
https://www.city.bizen.okayama.jp/site/aka/746.html
https://www.city.bizen.okayama.jp/soshiki/17/745.html

### 8-city smartphone walk rally — do NOT child-list

Current:
- 2026-10-01 through 11-30
- includes Bizen / Okayama / Tsuyama / Setouchi / Hayashima / Kumenan / Misaki / Nagi
- free
- BUT official target is age 18+ residents / workers / students

Classification:
ADULT_PROGRAM
PUBLIC_STATUS = EXCLUDE_FROM_CHILD_ACTIVITY
Retain only if later used as regional-network metadata.

Evidence:
https://www.city.bizen.okayama.jp/soshiki/13/34288.html

### Bizen correction

Previous state:
`BIZEN = SOURCE_STRONG / CURRENT_CARD_NEEDS_REFRESH`

New state:
`BIZEN = CHILD_INFRASTRUCTURE_STRONG / PUBLIC_EVENT_CARD_TIMING_THIN`

Meaning:
Even when the current event calendar is sparse, the town page should not look empty.
Use:
- constant play SOURCE
- parent-child SOURCE network
- cultural / making recurring SOURCEs
- community records
alongside current event cards.

---

## B. 奈義町 — contemporary-art hands-on card

### AIRN vol.7 workshop "紙で高い塔を作ろう！"

Current official:
- 2026-11-01
- 13:30
- Nagi MOCA
- paper + stapler construction challenge
- create the tallest possible tower
- capacity: 10
- age: unrestricted
- low elementary and younger require guardian
- fee: free
- reservation: phone / email

Classification:
OPEN_PUBLIC / FREE / APPLICATION
CHILD / FAMILY / GENERAL
CREATIVE / ART / ENGINEERING_THINKING / MAKING
HANDS_ON = VERY_HIGH
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_PRIORITY

Evidence:
https://www.town.nagi.okayama.jp/moca/news/20261010.html

GROWgle note:
Nagi's public content can now show multiple local axes:
- industry / agriculture / science through Industry Festival
- contemporary art / making through Nagi MOCA
- local performing heritage through child Kabuki SOURCE

Do not represent Nagi only as "arts tourism" or only as "sports".

---

## C. 美作市 — forest / body experience card

### 第5回ツリークライミング体験会

Current official:
- 2026-11-15
- 09:30–12:00
- location: summit plaza of Mt. Koshobo
- meet at Ohara Community Center at 08:00
- approx. 1.6 km / 40-minute approach from trailhead
- certified Tree Climbing Japan instructors
- tree climbing with dedicated gear
- slackline
- fee: 1,000 yen

Classification:
OPEN_PUBLIC_CANDIDATE
FAMILY / CHILD_COMPATIBLE / GENERAL
NATURE / FOREST / PHYSICAL / CHALLENGE
HANDS_ON = VERY_HIGH
ACCESS_GATE = CONDITIONAL
PUBLIC_STATUS = PUBLIC_LIST_CANDIDATE

Conditional reason:
official text accessed in this pass does not expose explicit age / minimum-age restriction in machine-readable text.
Do not publish a child-age claim until flyer / application details are checked.

Evidence:
https://www.city.mimasaka.lg.jp/kanko/info/9137.html

### Mimasaka growth in page content

Current public card candidates now include:
- puppet theater
- tree climbing

Research / community layer also includes:
- Hayashino High School "みまさか学"
- student regional inquiry / activities

This gives the town page both:
- public family participation
- youth provider / regional learning record

---

## D. 美咲町 — town-wide event / parenting-source density

### Current event density

Current official LINE/event feed updated 2026-10-09 shows:
- 2026-10-22 konnyaku-making class
- 2026-10-24 fire / disaster-prevention festival in Asahi
- 2026-10-26 pediatric outreach lecture
- 2026-10-31 one-day forestry experience
plus multiple child-support-center programs.

Classification:
TOWN_EVENT_SOURCE = STRONG
PUBLIC / FAMILY / ADULT mix
Need each activity's target / direct-application conditions normalized separately.

Evidence:
https://www.town.okayama-misaki.lg.jp/kakuka/misakikyoso/gyomu/6/1/3705.html

### Child-support-center distributed network

Current monthly schedule contains:
- parent-child yoga
- handprint art
- sweet-potato digging
- cooking
- festival play
- Halloween
- story reading
- nursery-yard opening
- outreach childcare
etc.

Classification:
EARLY_CHILDHOOD_SYSTEM_SOURCE
PRESCHOOL / FAMILY
RECURRING / DISTRIBUTED
COMMUNITY / PLAY / CREATIVE / FOOD / PHYSICAL

Evidence:
https://www.town.okayama-misaki.lg.jp/calendar.html
https://www.town.okayama-misaki.lg.jp/kakuka/kyoikusomu/gyomu/5/1/shien_event_2609/index.html

GROWgle note:
Do not make every support-center date a top-level event card.
Town page should show:
SOURCE = 美咲町子育て支援センター network
ACTIVITY = selected current family programs

This is a strong example of how a small municipality can look rich without inflating event-card count.

---

## E. 津山市 — current public event stream + strong permanent SOURCE

### 津山まなびの鉄道館 — permanent child/family SOURCE

Current:
- opening 09:00–16:00
- elementary / junior-high: 100 yen
- preschool: free
- current 2026 event history includes:
  - parent-child summer special
  - mini diorama workshop
  - quiz-gacha
  - washi-lighting workshop

Classification:
CONSTANT_PUBLIC_SOURCE
CHILD / FAMILY
RAILWAY / INDUSTRIAL_HERITAGE / STEAM / MAKING
ACCESS_GATE = PASS
PUBLIC_STATUS = PUBLIC_LIST_SOURCE

Evidence:
https://www.tsuyamakan.jp/manabi/eHUC_PPB

### November current city event stream

Current official tourism feed confirms:
- 2026-11-01: 令和作州城東むかし町
- 2026-11-01: かも谷まつり
- 2026-11-14: 勝北ふるさと祭り
- 2026-11-22: レトロリレーバス
- additional long-running November cultural events

Classification:
COMMUNITY / CULTURE / REGIONAL_IDENTITY
PUBLIC_GENERAL
Not all should automatically become child activity cards.
Use as:
- town/region activity records
- family/general event cards only when child hands-on content is confirmed

Evidence:
https://www.tsuyamakan.jp/
https://www.tsuyamakan.jp/event

### Tsuyama interpretation

Current state:
`TSUYAMA = SOURCE_RICH / CHILD_ACTIVITY_CARD_NORMALIZATION_LAG`

This is not a research-poor municipality.
The next useful action is to resolve which current city events have explicit child participation / hands-on content.

---

## F. Public-card vs wider GROWgle display rule reinforced

For Pilot content expansion, use three display layers:

### 1. PUBLIC ACTIVITY
Direct-family participation / application possible.
Fields:
date / fee / age / application / current state.

### 2. COMMUNITY RECORD
School-only / youth project / company-school / completed activity / region-specific learning record.
Clearly label:
"currently not recruiting" / "school activity" / "activity record".

### 3. SOURCE
Recurring generator:
- library
- play park
- museum
- child-support network
- annual program
- high school / university / NPO
- company / association

Do not force SOURCE into event-card format.

## 14. Immediate new promotion / display candidates from batch 4

PUBLIC:
- Nagi MOCA paper-tower workshop
- Mimasaka tree climbing (after age restriction check)
- Bizen Play Park as constant public experience
- Bizen parent-child gathering SOURCE network
- Misaki support-center network
- Tsuyama Railway Museum SOURCE

COMMUNITY / SOURCE visibility:
- Misaki distributed parenting programs
- Mimasaka school-youth regional inquiry
- Nagi child Kabuki heritage SOURCE
- Tsuyama November community-cultural stream

Next:
- continue CURRENT child-participation verification for Tsuyama November events
- resolve Mimasaka tree-climbing age condition
- search Bizen November/December current child activities from monthly child calendars
- continue 1–2 card municipalities and promote recurring SOURCEs, not only event cards.
