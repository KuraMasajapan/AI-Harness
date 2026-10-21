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
