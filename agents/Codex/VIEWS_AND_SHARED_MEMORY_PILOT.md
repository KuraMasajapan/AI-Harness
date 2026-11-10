# 進捗HTML・Notion共有メモリの小規模試行

2026-11-07。ユーザーが優先2・3（進捗HTML、Notion共有メモリ）を指定。
Jev/hunch導入や分類モデル比較はこの工程の対象外。

## 完了条件と状態の分離

1. 同じローカルHTMLを手動更新し、現在の目的・次工程・branch/HEAD・検証と未確認を表示。
2. 3回の更新で旧スナップショットを保持し、失敗時に成功したような更新をしない。
3. 共有候補は明示リストからのみ下書き化。出典bytesの変更・期限切れ・重複ID・非共有分類を拒否。

これはローカル実装の合格条件。実作業の時間/token/再読込削減は別途観測し、
Humanの正式採用判断と分ける。元M2の8回は再実行・再採点しない。
モデル/API呼出し予算0のまま。常駐・hook・外部送信は実装しない。

## 進捗HTML

```powershell
python -B tools/codex_views.py dashboard environment-m2-pilot
```

同じignored `.harness-runtime/views/environment-m2-pilot/index.html`へ生成する。
既存のcheckpoint/operation/environment gateを読み、独自の合否判定を新設しない。
失効済み検証をPASSへ読み替えず、理由も表示。HTMLエスケープ・ネットワーク不要・
外部アセットなし・静的HTML・キーボードで使える標準リンク/開閉・狭幅対応。
保存時点の表示であり、経過時間にかかわらず再生成確認が必要と常時明示する。
state.jsonと更新ごとのJSON/HTMLをローカル保持。原証跡を上書きしない。
履歴の自動削除なし。表示に個別運用情報を含むため共有GitやPagesへ出さない。

生成失敗ならCLIはNOT_UPDATEDで停止する。旧ページは保存時点のまま残る。
各ファイルの置換はatomicだが、複数派生ファイル全体のトランザクションではない。
元記録は複数の読み取り中に変わり得る。厳密な同時点スナップショットではなく、
新たな検証証跡にもならない。重要操作前は既存入口で再照合する。

## Notionに渡す前の下書き

`tools/codex_views.py memory-draft PACKET.json`で、新しいignoredフォルダにreview.mdと
出典packet/outputのhashを生成。ネットワーク呼出し0。checkpoint全体や生ログを収集しない。

packetはschema=1、sharing=DRAFT_NOT_SENT、非空entries配列。
各entry: id、正整数revision、classification=SHARED_CANDIDATE、
status（ACTIVE/SUPERSEDED/RETRACTED）、project、text、source_path、
source_sha256、タイムゾーン付きexpires_at。
source_pathは許可されたrepo内Markdownのみに限定し、実bytesを照合する。
textが出典の意味と一致することや秘密を含まないことは機械認定しない。
SHARED_CANDIDATEというラベル自体は共有承認ではなく、人が内容をレビューする。
非ACTIVE項目は失効・撤回情報として扱い、現行指示へ昇格させない。

### 保存先・競合・訂正の運用設計

- GitHub/ローカルの一次記録を維持。Notionは選別した派生文脈。
- 利用時はproject・期限・出典hash・最新ユーザー指示を照合。失効/相違は利用保留。
- 同じIDの異なる内容を自動上書きしない。revisionと出典を比較して差分を示す。
- 訂正は新revisionと訂正理由を一次記録に残し、旧Notion記憶の更新/失効も明示確認する。
- Notion上での手編集はGitHubへ自動反映しない。衝突時は一次記録とユーザー判断へ戻る。
- 一方の撤回が他クライアントへ即時反映されると仮定しない。
- 下書き生成は同期でもNotion native Memory API互換の保証でもない。

### 次の接続試験（未実施）

plugin検索ではNotionはAVAILABLE / installed=false。現セッションにNotion操作ツールなし。
接続前にアカウント・workspace・user-backed接続か、Memoriesが有効かを確認する。
公式仕様では同じaccount/workspaceにつながるクライアント間で記憶を利用できるが、
接続だけで他クライアントの会話は自動取り込みされない。

準備した下書きをレビュー後、まずダミー記憶1件で保存→検索→訂正→再取得を確認する。
2クライアント目は初回試験後。実プロジェクトの共有情報は別に選別する。
外部ページ作成・プラグイン接続・公開は、このローカル実装では行わない。

公式資料を2026-11-07に確認:
- https://developers.notion.com/guides/mcp/tools-skills-agents
- https://developers.notion.com/guides/mcp/mcp-security-best-practices

## 試験運用の観測

まずこの改修を実案件として、明示したローカル更新3回、失敗1回、出典変更/期限切れの
負例を確認する。生成時間/出力bytesは測れても実token削減には換算しない。
再開時に表示だけで目的・未確認・次工程を復元できるかを後続の作業で観測する。
比較対照を置いていない初期試行から一般性能向上を認定しない。
