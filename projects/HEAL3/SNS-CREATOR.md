# HEAL3 SNS Creator

## Purpose
HEALTHREE公式アプリの投稿用画像を素材として、誰でも軽快かつ簡単にSNS向け画像を編集・共有できるアプリを開発する。

高機能な画像編集ソフトを目指すのではなく、
「シンプル・軽い・素材が豊富」を中心価値とする。

## Core Problem
- HEALTHREE公式の投稿画像を、もう少し自分らしく加工したい
- 高機能な編集アプリは操作が複雑で重い
- HEALTHREE向けの専用素材やテンプレートが少ない
- X以外のSNSへ投稿するきっかけが少ない
- コミュニティで作られた素材が流れてしまい、再利用しにくい

## Product Direction
### Simple / Fast / Lots of Items
編集機能の多さではなく、動作の軽さと素材の豊富さで勝負する。

アプリ内にAI APIは搭載しない。
API利用料のかからない構成を基本とし、出来合いのテンプレートや素材を組み合わせて誰でも楽しめる体験を優先する。

AI生成画像など、外部ツールでユーザーが作った素材の持ち込みは歓迎する。

## Launch Experience
起動時は約3秒の固定タイトル動画を再生し、このアプリで作れる完成作品をテンポよく見せる。

タイトル動画は単なるロゴ表示ではなく、
- ブランド表示
- 「何が作れるアプリか」の再認識
- 創作意欲を起こす

という役割を兼ねる。

動画終了後は説明画面を挟まず、すぐに「投稿画像を選ぶ」ことを中心とした狭い入口へ遷移する。

### Title Movie
- 初期設定では毎回再生する
- 約3秒を目安とする
- 固定動画とし、軽量・安定・端末差の少ない実装を優先する
- 完成作品の複数パターンを短時間で見せ、機能説明を兼ねる
- 設定から「起動時にタイトル動画を再生しない」を選択できる

### Welcome Back Intro
タイトル動画をOFFにしているユーザーでも、最後の利用から30日以上経過している場合は、その起動時だけタイトル動画を1回再生する。

ユーザーが設定した「タイトル動画OFF」の状態そのものは変更しない。

例:
- 30日以上ぶりの起動 → その回だけタイトル動画を再生
- 翌日の起動 → OFF設定に従い再生しない

サーバーやAIは使わず、端末内に保存した最終起動日時との比較で実装する。

## Core Experience
1. HEALTHREE公式アプリの投稿用画像やスクリーンショットを読み込む
2. テンプレートを選ぶ
3. フレーム、スタンプ、背景、文字スタンプなどを追加する
4. 素材の位置・サイズ・角度・透明度などを調整する
5. 完成画像を保存する
6. X、Instagram、Discordなどへ共有する


## V1 End-to-End User Flow
V1では「すぐ完成できるが、触り始めると深く遊べる」体験を一貫させる。

基本フロー:
起動 → 約3秒の完成作品イントロ → 投稿画像を選択 → ✨おまかせ → 完成候補 → そのまま完成 / もう一回 / 自由編集 → 完成 → 書き出し → 保存・共有

### Quick Post
最短利用では、画像選択後に「おまかせ」を押すだけで完成候補を生成する。ユーザーにテンプレート、Motion、レイヤー、出力形式などを意識させない。

### Omakase Retry
「もう一回」で別のStyle Recipeを適用し、直近5候補を履歴として保持する。履歴候補から任意の案へ戻り、その状態を起点に編集できる。

### Add Item
素材一覧からItemをタップすると、キャンバス中央付近へ適正サイズで即配置する。既存Itemと重なりすぎる場合は少し位置をずらす。同一Itemの複数配置を許可する。ドラッグ＆ドロップを基本操作にはしない。

新規配置時は、そのItemに設定された推奨Motionを自動適用し、即座に動き始めた選択状態とする。

### Edit Item
配置後は直接操作で移動・拡大縮小・回転を行う。Motion変更も通常スタンプと文字スタンプで同じ入口から行い、そのItemに適した候補だけを一覧表示する。「なし」も選択可能とする。

### Text Item
自由テキスト入力はV1に持ち込まず、公式ワード、定番フレーズ、ABC、数字、かな、記号、一文字漢字などを文字スタンプとして利用する。操作体系は通常スタンプと共通にし、内部ではText Motion Recipeによる文字専用演出を許容する。

### Cutout
BASE画像内のアバター等を素材として使いたい場合のみ「切り抜く」へ進む。切り抜いたパーツは通常Itemと同様に扱える方向とし、日常操作ではBASE画像をそのまま保つ。

### Complete and Export
「完成」を押すと編集UIを隠し、完成作品を大きく表示してMotionを再生し続ける。その表示中に裏側で書き出し処理を行い、完了後に「保存 / 共有 / 編集に戻る」を自然に表示する。

Motionなしの作品は静止画、Motionありの作品は動きを保持できる形式を基本とするが、具体的な出力形式はiPhone Safariおよび対象SNSでの実機PoC後に確定する。ユーザーにはファイル形式を毎回選択させない。

## Item Platform Architecture
SNS Creator本体と素材ライブラリを分離し、素材数が増えても本体開発やGitHub PR運用が素材数に比例して肥大化しない構造を採る。

構成:
- SNS Creator Core: Web Firstのアプリ本体。OSS化を前提に検討する
- Motion Recipe: Itemへ適用する高品質な動きの定義
- Item Schema: 公式・Community・個人素材で共通利用する素材規格
- Official Library: HEALTHREE公式素材、公式ワード、イベント素材等
- Community Library: ユーザー制作素材を共有・検索・利用するデータ層
- My Items: 個人が持ち込んだ素材や将来のCreator Pet等のPersonal Item

コードのOSSライセンスと、HEALTHREEのロゴ・公式画像・キャラクター等のブランド資産、Community作品の利用条件は同一視せず分離して設計する。具体的なライセンスは別途検討して確定する。

### Item Schema Direction
Itemは素材本体だけでなく、検索・表示・Motion・権利管理に必要なメタデータを持つ。最低限の候補は以下とする。
- id / version
- asset / thumbnail
- category / tags
- creator
- source type: Official / Community / Personal / Limited等
- recommended motion
- compatible motions
- license / usage / redistribution / modification
- AI-generated flag
- created / updated
- popularity / recommendation等の検索・表示用情報
- International素材では必要に応じてcountry / language等

Motionを画像へ固定的に焼き込まず、可能な限り素材本体とMotion Recipeを分離する。同じItemへ複数Motionを適用できる構造を基本とする。

### Large Library Strategy
大量素材を起動時に全件読み込まない。カテゴリ、タグ、人気、新着、Official / Community等を検索用インデックスとして利用し、必要な候補だけ取得する。

例: GAMEカテゴリを開く → 上位数十件を取得 → スクロールに応じて次の候補を追加取得。

総素材数が1万件、10万件以上へ増えても、クライアントが一度に扱う量を限定する。ランキングやおすすめは必要に応じて事前計算・キャッシュを利用する。大量化では速度だけでなく「欲しい素材を発見できること」を重視する。

### Community Library Flow
Community素材の追加をSNS Creator本体へのGitHub PRとして扱わない。

素材制作 → スタンプ開発アプリ等から登録 → 自動/運営ルールによるチェック → Community Library公開 → SNS Creatorから検索・利用、を基本フローとする。

将来的にはGood / Bad、人気素材、作者情報等をCommunity Library側へ追加し、素材の発見・整理・昇格に利用できるようにする。

### OSS Contribution Flow
GitHub PRはアプリ本体、Motionエンジン、バグ修正、性能改善など「機械そのもの」の変更に利用する。素材数の増加とPR数を直結させない。

外部PR → 自動テスト → AIレビュー → PRごとのPreview Deployment → 実機/UX確認 → developmentへ統合 → 本番、という運用を基本候補とする。

自動マージは行わず、技術面は自動テスト・AIレビューで補助し、最終的には公式版へ採用する価値があるかをProduct Maintainerが判断する。セキュリティ、外部通信、新規依存ライブラリ等の高リスク変更は追加の技術確認対象とする。


## Quick Start / Omakase Experience
投稿画像を選択した直後は、ゼロから編集を要求せず「おまかせ」を主役にする。

### Omakase
- 主操作として「✨ おまかせ」を表示する
- おまかせは完全ランダムではなく、デザインとして成立するStyle Recipeを選択して適用する
- Style Recipeはカテゴリー、素材セット、配置ルール、背景、マスク、文字スタイルなどの組み合わせで構成する
- POP / COOL / JAPANESE / CYBER / MINIMALなど、同系統の素材・デザインをまとめて使用し、無秩序な組み合わせを避ける
- 膨大なテンプレートや素材は一覧選択を強制せず、「おまかせ」の選択肢を豊かにする燃料として活用する
- ユーザーには内部のRecipe構造を意識させず、完成結果を見て判断してもらう
- 自由編集をしたいユーザー向けの導線は残すが、視覚的には「おまかせ」を主役とする

基本フロー:

投稿画像を選ぶ
→ ✨ おまかせ
→ 完成候補を表示
→ 気に入らなければ「✨ もう一回」
→ 気に入った候補を選ぶ
→ その候補を出発点として自由編集
→ 残す / 消す / 動かす / 追加する
→ 保存・投稿

狙いは、白紙からデザインを要求するのではなく、アプリが最初の案を提示し、ユーザーがそこから自分らしい作品へ育てる体験を作ること。

### Omakase History
「もう一回」で生成した候補は直近5件まで履歴として保持する。

- 画面上では小さなサムネイルなどで5候補を比較できる
- 6件目を生成すると最も古い候補から自然に履歴外へ送る
- 無限履歴にはしない
- 「さっきの方が良かった」を防ぎつつ、5案程度から選んで編集へ進みたくなるUXを狙う
- 履歴管理そのものをユーザーの作業にしない
- 実装時は可能であれば完成画像5枚ではなく、Recipe / Item Set / Layout / Background / Seedなど再現に必要な軽量データを保持する
- 履歴候補を選択したら、その状態を起点として編集モードへ移れる

テンプレート数や素材数が非常に多くなっても、ユーザーに巨大な一覧を最初から見せない。「選択肢の豊富さ」を「選択の負担」に変えないことを優先する。

## Editor Interaction

### Base Image and Decoration Model
HEALTHREE公式投稿画像は編集の土台となるBASEとして扱い、基本的に最下層で固定する。

日常的な使い方は、公式画像そのものを細かく編集するのではなく、その上へスタンプ、文字スタンプ、フレーム、マスクなどを重ねてオリジナリティを加えることとする。

元画像内の要素を素材として利用したい場合のみ、明示的な「切り抜く」操作から一段深い編集へ入る。切り抜きアイコンは、人型そのものの輪郭線をミシン目状の点線で表現する案を第一候補とする。

### No Layer Management
ユーザーに「レイヤー」という概念を意識させない。

- BASE画像は最下層で固定
- 後から追加した素材は、追加した順に手前へ重なる
- 前へ / 後ろへ等のレイヤー並べ替え機能は基本的に設けない
- 汎用画像編集アプリの機能をそのまま持ち込まず、「HEALTHREE投稿に本当に必要か」を機能採用の判断基準とする

### Bottom Action UI
編集画面下部には少数の丸いメニューアイコンを配置する。

現時点の基本候補:
- 素材
- 切り抜く

丸アイコンをタップすると少数の第一階層を扇状などで展開し、大量の素材を探す必要がある場合のみ下部パネルへ移行する「小さく開いて、必要なら深く入る」構造を第一候補とする。展開方式の細部はUIモック・実機検証で変更可能とする。

### Direct Manipulation
配置済み素材は、画面上で直接触って操作する。

- 移動: 1本指ドラッグ
- 拡大 / 縮小: ピンチ
- 回転: 2本指操作
- 専用のレイヤー管理画面や常設削除ボタンは設けない

### Lift Interaction
素材を選択したときは、実際の作品データ上のサイズを変更せず、操作中だけ見た目を少し大きく表示する。

目的:
- 小さい素材を指で隠しにくくする
- 「今この素材をつかんでいる」ことを視覚的に伝える
- 編集用の選択枠や多数の操作ボタンへの依存を減らす

操作終了時には一時的な拡大表示を解除し、ユーザーが拡大・縮小した場合はその最終サイズに準じて通常表示へ戻す。画面端では必要に応じて表示が画面外へ逃げすぎないよう調整する。

### Drag to Delete
素材をドラッグし始めたとき、通常の下部メニューを一時的に削除エリアへ切り替える。

素材を削除エリアまでドラッグして離すと削除する。

- 通常時は削除UIを表示しない
- 削除エリアへ入ったことは視覚変化で明確に示す
- 誤削除対策として、削除直後のみ短時間「元に戻す」を表示する案を採用候補とする

### Haptic Feedback
触覚フィードバックは補助的な演出として扱い、必須要件にはしない。

対応端末・ブラウザでは、素材をつかんだ時や削除エリアへ入った時などに軽い触覚を付加してもよい。ただし触覚が利用できない環境でも、視覚だけですべての操作が成立することを必須とする。

## Animated Still Direction
HEAL3 SNS Creatorは動画編集アプリを目指さない。

HEALTHREEの静止した公式投稿画像を主役として保ち、その上に追加した文字・スタンプ・エフェクト等へ軽いモーションを与える「動く静止画（Animated Still）」を重要な成果物として扱う。

- BASE画像は基本的に静止したまま
- キラキラ、揺れ、ポップイン、回転、浮遊などの軽量モーションを装飾レイヤーへ付与できる
- タイムライン、カット編集、キーフレームなど本格的な動画編集UIは持ち込まない
- ユーザー体験は最後まで「投稿画像をデコレーションする」感覚を維持する
- おまかせStyle Recipeはデザインだけでなく、素材に適したMotion Recipeも組み合わせられる
- 動かしすぎて公式画像の情報を邪魔しないよう、主役モーションと控えめな環境エフェクトのバランスをRecipe側で管理する
- SNS投稿のため最終出力が動画形式等になる場合でも、それは出力上の都合であり、プロダクトを動画編集アプリ化しない

### Motion Quality Principle
Motionは数より質を優先し、安価に見える単調なループをできるだけ避ける。

初期Motion候補:
- 光る
- 跳ねる
- 揺れる
- 回る
- 浮く
- 流れる
- 弾ける
- 降る
- 踊る
- 鼓動する
- 飛び込む

「踊る」のような複合Motionは、ユーザーに細かなパラメータ編集を求めず、完成度の高いプリセットとして提供する。

品質基準:
- 機械的な等速運動を避ける
- 加速・減速、タメ、オーバーシュート、戻りの余韻などを使い、短い動きにも演出を持たせる
- 必要に応じて完全対称な動きを避け、自然なリズムを作る
- 1〜2秒程度の短い動きでも単調に見えないよう緩急を付ける
- 繰り返して見ても疲れにくいループを目指す
- 素材の形・意味・用途に合うMotionを優先する
- すべての素材へすべてのMotionを適用せず、素材ごとに相性の良いMotionを設定できるようにする
- Motionの内部パラメータは複雑でもよいが、その複雑さをユーザー操作には持ち込まない

### Web First / Lightweight
初期提供はスマートフォン向けブラウザアプリを第一候補とする。

- Mobile First
- Web First
- Lightweight
- 起動時に全素材を読み込まず、必要な素材だけ遅延読み込みする
- 編集中は静止BASE + レイヤー + 軽量モーションをリアルタイム表示し、完成物への変換は保存時のみ行う
- 動く成果物の書き出し方式は、iPhone Safari等の実機PoCで処理速度・メモリ・保存導線を確認して最終決定する
- SNSへの直接投稿を必須とせず、端末へ保存して写真アルバム等から投稿する導線も正式な利用方法として許容する

## MVP
- 画像読み込み
- テンプレート選択
- 素材配置
- 文字スタンプ配置
- 背景変更
- 移動 / 拡大縮小 / 回転 / 透明度
- 画像保存
- SNS共有

高度な写真補正、動画編集、AI生成などは初期MVPに含めない。

## Template Philosophy
完成度の高い「選ぶだけで使えるテンプレート」を基本とする。

同時に、ユーザーが必要に応じて素材・文字スタンプ・背景・配置などを自由に変更できるようにする。

初心者は選ぶだけ、凝りたいユーザーは自由に編集できる二層構造を目指す。

## Item Library
素材数そのものをアプリの競争力とする。

想定カテゴリ例:
- FRAME
- STICKER
- TEXT STICKER
- TITLE
- BADGE
- BACKGROUND
- EFFECT
- SEASON
- EVENT
- AVATAR
- RUNNING
- GAME
- JAPANESE
- RETRO
- POP
- CYBER

PNGだけでなくSVGなどの軽量素材も活用し、素材数が増えてもアプリ本体が重くならない設計を検討する。

### Text as Sticker
初期MVPでは自由テキスト入力機能を持たせず、文字表現もスタンプとして扱う。

- HEALTHREE公式アプリ内で使われるワードや定番フレーズは、デザイン済みの文字スタンプとして用意する
- ABC、数字、ひらがな、カタカナ、記号なども文字スタンプ素材として追加可能にする
- 漢字は全文字を網羅せず、「祝」「勝」「神」「超」「祭」など単発で使いやすい文字を素材候補とする
- 独自の文章や文字表現が必要なユーザーは、外部ツールまたは将来のスタンプ開発プラットフォームで文字スタンプを制作し、SNS Creatorへ持ち込む方向とする
- 文字スタンプも通常スタンプと同じ配置・拡大縮小・回転・削除の操作体系を使う
- ユーザーへのMotion選択UIも通常スタンプと統一する一方、内部では文字向けの専用Motion Recipeを持てるようにする
- 文字向けMotionは文字単位・単語単位・全文単位の演出、虹色発光など、通常スタンプとは異なる表現を許容する

この方針により、フォント選択、改行、文字組み、多言語入力などの汎用テキスト編集機能を初期MVPへ持ち込まず、SNS Creatorの軽さと単純な操作体系を維持する。

## Community Items
運営だけで素材を作るのではなく、ユーザー自身が素材を追加・配布できる仕組みを目指す。

ユーザーは画像編集ソフトや画像生成AIなど外部ツールを自由に使って素材を制作できる。

想定フロー:

ユーザーが素材を作る
→ スタンプ開発アプリ等からCommunity Libraryへ登録
→ 分類・チェック
→ Community素材として公開
→ SNS Creatorから必要な素材を取得して利用
→ 利用・共有・評価される
→ コミュニティ参加によって素材ライブラリが自然に増える

将来的にはGood / Bad評価、人気素材、作者別表示なども検討する。

## X and Discord
### X
新しい素材の発見・配布・拡散を担う。

### Discord
過去に配布された素材のアーカイブ、カテゴリ整理、検索、コミュニティ交流を担う。

役割分担:

X = 発見・拡散  
Discord = 保存・検索・交流  
App = 編集・利用

初期段階では手動運用でもよい。規模が大きくなった場合はBotなどによる整理・アーカイブを検討する。

## Personal / Avatar Items
素材は一般的な装飾だけでなく、ユーザー自身のHEALTHREEアバターなどパーソナルなものにも広げる。

想定区分:
- Personal: 自分専用
- Community: 誰でも利用可能
- Collab: 他ユーザーが交流目的で利用可能
- Official: 公式・運営素材
- Limited: イベントなど限定用途

アバター素材については、利用可能範囲や改変可否などを分かりやすく設定できる仕組みを将来的に検討する。

## Social Creation
他ユーザーが公開したアバター素材を組み合わせることで、単なる画像加工を超えたコミュニティコンテンツを作れる。

例:
- ツーショット
- フレンド集合写真
- チーム / グループ写真
- イベント参加記念
- RPGパーティ風
- 応援画像
- 雑誌表紙風
- 「マイケルファミリー集合」のようなコミュニティ集合画像

集合テンプレートに空席を用意して「あと3人募集中」のような参加型投稿へ発展させることもできる。

素材を使う行為そのものが、ユーザー同士の交流になることを目指す。

## Item Metadata / Rights
コミュニティ素材には最低限の作者情報・利用条件を持たせることを検討する。

例:
- creator
- category
- license / usage
- redistribution
- modification
- AI-generated
- tags

著作権侵害や公式素材の誤用を防ぐため、投稿ルールと利用条件はサービス公開前に整理する。

## Design Principle
### Make posting playful.
「投稿するまでの面倒を減らす」だけではなく、
「投稿画像を作ること自体がHEALTHREEコミュニティの遊びになる」ことを目指す。

高機能化よりも、
- すぐ起動する
- 迷わない
- すぐ完成する
- 素材を選ぶのが楽しい
- 他人の素材を使うのが楽しい
- 自分の素材を配るのが楽しい

ことを優先する。

### Narrow Entrance, Deep Playground
入口から見える操作は極力少なくし、使い始めると想像以上に自由で奥行きのある編集体験が広がるUI / UXを目指す。

「機能を減らす」のではなく、「その瞬間に必要な機能だけを見せる」ことを基本とする。

想定する段階的な体験:
1. 起動時は「投稿画像を選ぶ」など、ごく少数の選択肢だけを見せる
2. 画像を選んだ後に「テンプレート / 素材 / 保存」など基本編集を見せる
3. 素材を選択した時だけ「移動 / 拡大縮小 / 回転 / 透明度 / 重ね順」など対象に必要な操作を見せる
4. より深く編集したいユーザーには「マスク / パーツ化 / マイ素材 / アバター / 集合写真」など高度な遊びを段階的に開放する
5. コミュニティ素材やアーカイブなどは編集画面を圧迫しない別導線に配置する

機能候補は単純な「採用 / 削除」の二択にせず、以下で選別する:
- 常に見せる
- 必要な時だけ見せる
- 別画面に置く
- 将来実装する
- 削除する

最終的に多くの機能を採用した場合でも、初心者が一度に考える選択肢を少なく保つ。

### Remember Nothing UX
ユーザーが前回の操作方法を覚えていることを前提にしない。

特に画像編集を低頻度で利用するユーザーは、前回覚えた操作や「どのアプリで何ができたか」を忘れる可能性がある。そのため、久しぶりの利用でも説明書やチュートリアルを読み直さず、自然に作業へ戻れることを目指す。

- 起動時の完成作品提示で「何ができるアプリか」を短時間で思い出せる
- 入口では次に行う操作を明確にする
- 機能一覧から探させるのではなく、触った対象に応じて必要な操作を表示する
- 高度な機能は必要になった文脈で発見できる位置に置く
- 「探させる」と「迷わせる」を区別し、機能は予測可能な場所に配置する

## Initial Target
- X
- Instagram
- Discord

最初は同じ素材を複数SNSで使い回せることを重視し、将来的に各SNSの特徴に合わせた最適化を検討する。

## Future Feature: Creator Pet (V1.1 / V2.0 Candidate)
優先順位の低い将来機能として、SNS Creatorの継続利用によって成長するペット要素を検討する。V1の完成を優先し、この機能を初期MVPへ混在させない。

基本構想:
- 作品を完成させた活動日を基準に、1日最大1成長ポイントを獲得する
- 同日に何作品作っても成長ポイントは1のみとし、連投を成長上有利にしない
- 連続日数ではなく累積活動日数を基本とし、休んでも過去の成長を失わない
- ペットの誕生キャラクターはランダムとし、「何が生まれるか分からない」体験を楽しさの核とする
- 将来的には成長先もランダム分岐させ、同じ初期系統でも異なる個体へ育つ可能性を持たせる
- リセマラを前提とせず、能力差や勝敗よりも「自分固有の個体」への愛着を重視する
- 成長による変化は見た目、表情、仕草、アクセサリー、専用Motionなどを中心候補とする
- 育ったペットはAnimated StampとしてSNS Creator内へ配置でき、HEALTHREEアバターの横などに置いて投稿作品へ参加させられる

狙いは育成ゲームを別に作ることではなく、Creatorを長く使った履歴が「自分だけの動くスタンプ」として育ち、次の作品制作へ戻ってくる循環を作ること。

## Future
- ユーザー制作テンプレート
- コミュニティ素材共有
- Good / Bad評価
- 人気素材ランキング
- 作者プロフィール
- イベント限定素材
- 季節素材
- アバター公開 / コラボ設定
- 集合写真テンプレート
- Discordアーカイブ連携
- 素材インポート用共有リンク / ID
- SNSごとの出力最適化

---

## Current Checkpoint — 2026-09-19

This section records the current product direction after recent real-device PoCs. It is a working checkpoint, not a permanent final specification.

### Current Product Direction
- Continue developing the existing HEAL3 SNS-Creator rather than creating a separate app.
- Keep the product focused on making official HEAL3 result images easier and more enjoyable to post, rather than turning it into a general-purpose image editor.
- Prefer simple, immediately understandable transformations over deep editing workflows.
- The next major product direction to explore is **layout presets** that reorganize the official result image, reduce unused space, and make the avatar or key information more visually prominent.

### Avatar / Image Cutout Status
- MediaPipe Interactive Segmentation PoC succeeded on iPhone Safari using the `.task` model path.
- Real HEAL3 result images were successfully segmented with useful quality, including a difficult character example that became substantially cleaner when the result-screen background color provided better contrast.
- The cutout capability is considered a valuable **technical asset**, but the visible "Cut Out" action is temporarily removed from the primary product path.
- Reasons:
  - The source avatar image itself is not always high resolution.
  - Enlarging the extracted avatar can expose source-image quality limits.
  - The original avatar remains in the base result image, which can create a duplicated or overly edited look.
  - This can drift away from the product concept of making the official result image "a little nicer" with low effort.
- Preserve the segmentation implementation and findings for reuse in future scenarios where extracting a specific object is genuinely useful.

### Mask Feature Status
Mask is now a confirmed product direction: a whole-image atmosphere/effect layer placed above the base image and below user-added stamps/text.

Current rendering order:
```text
Base Image
→ Mask
→ User-added Stamps / Text
```

Preview and export should continue to use the same rendering logic.

#### Autumn Mask
- Status: **Strong adoption candidate / practical quality reached**
- Animated autumn leaves with depth layers and Weak / Medium / Strong intensity levels.
- Real-device evaluation found all three strengths useful without feeling excessive or insufficient.
- Further micro-tuning produced little perceptible difference, so avoid polishing it indefinitely.

#### Sunlight Mask
- Status: **Usable but not yet at the desired expressive quality**
- Initial particle-based version felt like rising carbonation bubbles.
- A later god-ray version produced an unacceptable dark/cheap spotlight appearance.
- The current revision is improved and no longer has the severe dark-band problem, but even Strong still feels visually restrained and motion is weaker than desired.
- Pause further refinement for now; preserve the implementation and revisit later if stronger moving light / broad radiant illumination becomes worth pursuing.

### Near-Term Priority
1. Treat Mask infrastructure as established and continue adding masks later rather than perfecting one effect indefinitely.
2. Explore **layout presets** as the next major UX/product experiment.
3. Keep the cutout engine available as a reusable technical capability, but do not make it a primary user-facing action for now.
4. Continue validating visually sensitive features on real iPhone output; implementation reports are not sufficient acceptance evidence.

### Product Principle Reinforced by These PoCs
A technically impressive capability is not automatically a good primary product feature.

For HEAL3 SNS-Creator, prefer features that:
- improve the official result image without making it feel over-edited,
- preserve fast and simple UX,
- create an immediate visual payoff,
- and remain understandable without requiring the user to remember editing concepts.
