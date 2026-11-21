import os
import tempfile

os.environ["MIHARASHI_DB_PATH"] = tempfile.mktemp(suffix=".db")
os.environ["MIHARASHI_API_TOKEN"] = "test-token"

from fastapi.testclient import TestClient  # noqa: E402

from app.db import init_db  # noqa: E402
from app.main import app  # noqa: E402

init_db()
client = TestClient(app)
HEADERS = {"x-api-token": "test-token"}


def test_auth_required():
    assert client.get("/fields").status_code == 401
    assert client.get("/fields", headers={"x-api-token": "wrong"}).status_code == 401


def test_fields_crud():
    r = client.post("/fields", json={"name": "北の畑", "location_note": "駅から5分"}, headers=HEADERS)
    assert r.status_code == 201
    assert r.json()["name"] == "北の畑"
    r = client.get("/fields", headers=HEADERS)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_plots_and_crops():
    r = client.post("/plots", json={"field_id": 1, "name": "A区画"}, headers=HEADERS)
    assert r.status_code == 201
    r = client.get("/plots", headers=HEADERS)
    assert len(r.json()) == 1

    r = client.post(
        "/crops",
        json={"plot_id": 1, "name": "トマト", "planted_on": "2026-04-10", "expected_harvest_note": "7月頃"},
        headers=HEADERS,
    )
    assert r.status_code == 201
    assert r.json()["name"] == "トマト"
    r = client.get("/crops", headers=HEADERS)
    assert len(r.json()) == 1

    # bad references -> 404
    r = client.post("/plots", json={"field_id": 999, "name": "X"}, headers=HEADERS)
    assert r.status_code == 404
    r = client.post(
        "/crops",
        json={"plot_id": 999, "name": "X", "planted_on": "2026-01-01"},
        headers=HEADERS,
    )
    assert r.status_code == 404


def test_work_logs_filter():
    assert (
        client.post(
            "/work-logs",
            json={"date": "2026-05-01", "plot_id": 1, "crop_id": 1, "work_type": "植付け", "memo": "苗3本"},
            headers=HEADERS,
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/work-logs",
            json={"date": "2026-06-01", "plot_id": 1, "work_type": "水やり"},
            headers=HEADERS,
        ).status_code
        == 201
    )
    r = client.get("/work-logs", headers=HEADERS)
    assert len(r.json()) == 2
    r = client.get("/work-logs?date_from=2026-05-15&date_to=2026-06-15", headers=HEADERS)
    logs = r.json()
    assert len(logs) == 1
    assert logs[0]["work_type"] == "水やり"


def test_harvests():
    r = client.post(
        "/harvests",
        json={"date": "2026-07-20", "crop_id": 1, "amount": 12, "unit": "個", "memo": "初収穫"},
        headers=HEADERS,
    )
    assert r.status_code == 201
    r = client.get("/harvests", headers=HEADERS)
    assert len(r.json()) == 1
    assert r.json()[0]["amount"] == 12


def test_summary_now():
    r = client.get("/summary/now", headers=HEADERS)
    assert r.status_code == 200
    plots = r.json()["plots"]
    assert len(plots) == 1
    assert plots[0]["field_name"] == "北の畑"
    assert plots[0]["crops"][0]["name"] == "トマト"
    assert plots[0]["recent_work_logs"][0]["work_type"] == "水やり"
