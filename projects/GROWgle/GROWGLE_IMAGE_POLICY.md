# GROWgle — Official Image / Thumbnail Policy

Status: ACTIVE_POLICY
Scope: GROWgle platform UI / activity cards / detail pages
Purpose: 公式画像をできる限り活用しつつ、無断転載リスクを避け、サムネイル表示の一貫性を保つ。

## 1. Core policy

GROWgleでは、イベント内容を一目で理解できるよう、可能な限り主催者・運営主体の公式画像を優先して表示する。

ただし、公式サイトや公式SNSに掲載されている画像を無条件にコピーしてGROWgle側へ保存・転載する運用は行わない。

基本原則:

> 公式画像を最優先し、正規に表示できない場合のみGROWgle独自イラストを使用する。

## 2. Display priority

画像表示の優先順位は以下とする。

1. 主催者から掲載用として提供された画像
2. 再利用可能であることを確認できた公式画像
3. 公式サイト・公式SNS等の正規の埋め込み・リンクプレビュー
4. GROWgle独自のカテゴリイラスト

公式画像を安全に表示できない場合は、GROWgle共通イラストへフォールバックする。

## 3. What not to do

以下は原則として行わない。

- 公式サイト上の画像を、利用条件未確認のままGROWgleサーバーへコピー保存する
- 公式SNS投稿の写真を、正規の埋め込み機能を使わず転載する
- AIが画像の利用可否を推測して「利用可能」と判定する
- 出典や権利状態が不明な画像を恒久的なサムネイルとして保存する

「公式ページに掲載されている画像」であることと、「GROWgleが自由に転載できる画像」であることは分けて扱う。

## 4. Official website / SNS

公式情報源はWebサイトだけに限定しない。

対象例:
- 公式Webサイト
- 公式Instagram
- 公式Facebook
- 公式X
- 公式YouTube
- 自治体・学校等の公式掲載ページ
- 主催者が公開する告知ページ

各サービスが提供する正規の埋め込みやリンクプレビューなど、画像そのものをGROWgleへ転載しない方法で表示できる場合は優先的に検討する。

## 5. Thumbnail data fields

将来の実装では、最低限以下を保持する。

### thumbnail_type
- OFFICIAL_PROVIDED
- OFFICIAL_REUSABLE
- OFFICIAL_EMBED
- GROWGLE_ILLUSTRATION

### thumbnail_source_url
元画像、公式投稿、公式ページ等の参照先。

### thumbnail_rights_status
- PROVIDED
- REUSE_ALLOWED
- EMBED_ONLY
- UNKNOWN

## 6. Fallback illustration

公式画像を正規に表示できない場合は、画像なしにはせず、GROWgle独自のカテゴリイラストを表示する。

想定カテゴリ例:
- ものづくり
- AI / STEAM
- 医療
- 自然
- 交通
- 食・農業
- 文化
- スポーツ
- 地域活動

これにより、公式画像を持たないSOURCE / ACTIVITYでもカードUIの品質を維持する。

## 7. Future organizer upload

将来、主催者・運営者がGROWgleを直接編集できる仕組みを導入する場合は、主催者自身が掲載用画像を登録・差し替えできる機能を追加する。

期待効果:
- 正規の公式画像を増やせる
- GROWgle側の権利判断負担を減らせる
- イベントカードの魅力を高められる
- 画像差し替えを主催者側で最新化できる

## 8. Separation from publication rules

このファイルは「画像・サムネイル」に限定した独立ポリシーとする。

イベント本文の公開可否、Human確認状態、情報欠落、SOURCE / ACTIVITYの公開工程等は別ルールで管理し、本ポリシーに混在させない。
