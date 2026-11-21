# みはらし畑 バックエンド v0

FastAPI + SQLite（単一ファイルDB）の小さな REST API。家庭菜園の畑・区画・作物・作業記録・収穫を管理する。

## 起動方法

```bash
cd projects/miharashi-hatake/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- 1コマンドで起動（DB ファイルは初回起動時に `miharashi.db` として自動作成される）
- API ドキュメント: http://localhost:8000/docs
- ポート変更は `uvicorn app.main:app --port 8080` など

## 認証

v0 は共有トークン1本。全リクエストのヘッダに `x-api-token` を付ける。

- デフォルト: `miharashi-dev-token`
- 環境変数 `MIHARASHI_API_TOKEN` で変更可
- DB パスは環境変数 `MIHARASHI_DB_PATH` で変更可

```bash
curl -H "x-api-token: miharashi-dev-token" http://localhost:8000/fields
```

## API 一覧

| メソッド | パス | 説明 |
|---|---|---|
| GET / POST | `/fields` | 畑の一覧 / 作成（name, location_note） |
| GET / POST | `/plots` | 区画の一覧 / 作成（field_id, name） |
| GET / POST | `/crops` | 作物の一覧 / 作成（plot_id, name, planted_on, expected_harvest_note） |
| GET / POST | `/work-logs` | 作業記録の一覧 / 作成（date, plot_id, crop_id 任意, work_type, memo）。`?date_from=&date_to=` で日付範囲絞り込み |
| GET / POST | `/harvests` | 収穫記録の一覧 / 作成（date, crop_id, amount, unit, memo） |
| GET | `/summary/now` | 今どの区画で何が育っているか＋直近の作業（区画ごとに作物一覧と直近5件の作業記録） |

## データモデル

- `field`: id, name, location_note
- `plot`: id, field_id, name
- `crop`: id, plot_id, name, planted_on, expected_harvest_note
- `work_log`: id, date, plot_id, crop_id (任意), work_type（植付け/水やり/除草/収穫/その他）, memo
- `harvest`: id, date, crop_id, amount, unit, memo

## サンプルデータ

```bash
python3 scripts/seed_sample_data.py
```

畑1件・区画2件・作物2件・作業記録3件・収穫1件を投入する。

## テスト

```bash
python3 -m pytest tests/ -v
```

主要エンドポイントの正常系（認証、fields/plots/crops の作成と一覧、work-logs の日付絞り込み、harvests、summary/now）をカバー。
