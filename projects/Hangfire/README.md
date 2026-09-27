# Hangfire Codex Form

Hangfireゲーム開発で、毎回のCodex指示を同じ形式で作るための常設フォーム。

## 開くファイル

`CODEX_TASK_FORM.html`

ブラウザで開く。

## 役割

固定仕様はフォーム内に保持し、毎回変更する項目だけ入力する。

- CURRENT_LAYER
- TARGET
- ALLOWED_FILES
- DO_NOT_TOUCH
- ACCEPTANCE
- STATUS

「Markdown生成」でCodex用の指示全文を生成する。

## 出力

- 画面表示
- クリップボードへコピー
- `HANGFIRE_TASK.md` として保存

## 注意

このHTML自体はゲームコードを実行・変更しない。
Codexへ渡すMarkdownを生成するだけ。

Source of Truthとなる固定仕様を変更する場合は、フォーム内の固定仕様も明示的に更新する。
