# GROWgle — Cross-Category Re-scan Checkpoint

更新: 2026-10-04
State: TODO / CHECKPOINT

## 目的

2026-10-04に `projects/GROWgle/RESEARCH_RULES.md` へ Cross-Category Capture ルールを追加した。

このルール追加前に調査した地域については、ENTRE以外のカテゴリ候補を十分な粒度で同時回収していない可能性があるため、後で必ず再走査する。

## 再走査対象

### 岡山県南部
対象:
- 岡山市
- 倉敷市
- 総社市
- 玉野市
- 早島町
- 井原市
- 矢掛町
- 浅口市
- 里庄町
- 笠岡市
- 赤磐市
- 瀬戸内市
- 備前市
- 吉備中央町

基準ログ:
- `projects/GROWgle/ENTRE/OKAYAMA_SOUTH_RESEARCH_V0_1.md`

### 岡山県北部
Cross-Category Capture導入前にFirst Pass / Second Passで確認した地域:
- 津山市
- 勝央町
- 奈義町
- 美咲町
- 鏡野町
- 真庭市
- 新庄村
- 美作市
- 西粟倉村
- 高梁市
- 新見市

基準ログ:
- `projects/GROWgle/ENTRE/OKAYAMA_NORTH_RESEARCH_V0_1.md`

## 再走査で追加回収するカテゴリ

最低限、以下を横断確認する。

- WORKS — 工場見学、企業見学、職業体験、産業、プロフェッショナル
- STEAM — 科学、技術、ロボット、電子工作、プログラミング、研究
- CREATIVE — デザイン、アート、映像、写真、音楽、工芸、建築
- NATURE — 自然、森林、農業、海・川、生態系、環境、アウトドア
- SPORTS — スポーツ、競技体験、プロチーム、eスポーツ
- 地域・社会参加系 — まちづくり、子ども会議、地域課題、ボランティア
- AI — 既存GROWgle AIとの重複・接続候補

## 再走査時の保存項目

他カテゴリ候補はその場で深掘りしすぎず、最低限以下を保存する。

- 名称
- 地域
- 対象年齢 / 学年
- 想定カテゴリ（複数可）
- 公開参加性
- 開催時期 / 常設性
- 主催者
- 公式URL / 一次情報
- 状態（INCLUDE / WATCH / HUMAN_REVIEW / CROSS_CATEGORY）
- 継続性の有無
- 次に確認すべきこと

## 実行タイミング

岡山県北部 ENTRE v1 を閉じた後、広島へ進む前、または各新カテゴリ本格調査を開始する直前に再走査する。

優先度:
1. 岡山県南部
2. 岡山県北部

## 完了条件

- 上記対象地域をCross-Category Captureルールで再確認済み
- 他カテゴリ候補を各カテゴリのBACKLOGへ引き渡し済み
- 「ENTRE探索時に見えていたが保存していなかった情報」が可能な限り回収済み
- 未確認箇所は明示的にBACKLOGへ残す

## 重要

この再走査は任意ではない。

**Cross-Category Capture導入以前の調査範囲は、後で必ず再走する。**


## 進捗更新 2026-10-04

State: IN_PROGRESS

### 岡山県南部
Cross-Category再走査 第1ブロック完了:
- [x] 岡山市
- [x] 倉敷市
- [x] 総社市
- [x] 玉野市（追加深掘りあり）
- [x] 早島町（追加深掘りあり）
- [ ] 井原市
- [ ] 矢掛町
- [ ] 浅口市
- [ ] 里庄町
- [ ] 笠岡市
- [ ] 赤磐市
- [ ] 瀬戸内市
- [ ] 備前市
- [ ] 吉備中央町

調査ログ:
- `projects/GROWgle/CROSS_CATEGORY/OKAYAMA_SOUTH_RESCAN_V0_1.md`

重要発見:
- 倉敷市はENTRE以外ではWORKS / STEAM / NATUREの継続情報源が厚い。
- 常設施設・年間プログラム・単発イベントを別タイプとして保持する必要がある。
- 「GLOBAL / COMMUNICATION」候補が発生したためHUMAN_REVIEWへ送る。
