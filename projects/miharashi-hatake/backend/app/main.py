import os
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from .db import connect, init_db

API_TOKEN = os.environ.get("MIHARASHI_API_TOKEN", "miharashi-dev-token")

app = FastAPI(title="みはらし畑 API", version="0.1.0")


def get_conn():
    conn = connect()
    try:
        yield conn
    finally:
        conn.close()


def auth(x_api_token: str = Header(default="")) -> None:
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="invalid token")


@app.on_event("startup")
def startup() -> None:
    init_db()


def rows(conn, sql, params=()):
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


def insert(conn, sql, params):
    cur = conn.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def get_or_404(conn, table, row_id):
    row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"{table} {row_id} not found")
    return dict(row)


class FieldIn(BaseModel):
    name: str
    location_note: str = ""


class PlotIn(BaseModel):
    field_id: int
    name: str


class CropIn(BaseModel):
    plot_id: int
    name: str
    planted_on: str
    expected_harvest_note: str = ""


class WorkLogIn(BaseModel):
    date: str
    plot_id: int
    crop_id: Optional[int] = None
    work_type: str
    memo: str = ""


class HarvestIn(BaseModel):
    date: str
    crop_id: int
    amount: float
    unit: str
    memo: str = ""


@app.get("/fields", dependencies=[Depends(auth)])
def list_fields(conn=Depends(get_conn)):
    return rows(conn, "SELECT * FROM field ORDER BY id")


@app.post("/fields", dependencies=[Depends(auth)], status_code=201)
def create_field(body: FieldIn, conn=Depends(get_conn)):
    fid = insert(conn, "INSERT INTO field (name, location_note) VALUES (?, ?)", (body.name, body.location_note))
    return get_or_404(conn, "field", fid)


@app.get("/plots", dependencies=[Depends(auth)])
def list_plots(conn=Depends(get_conn)):
    return rows(conn, "SELECT * FROM plot ORDER BY id")


@app.post("/plots", dependencies=[Depends(auth)], status_code=201)
def create_plot(body: PlotIn, conn=Depends(get_conn)):
    get_or_404(conn, "field", body.field_id)
    pid = insert(conn, "INSERT INTO plot (field_id, name) VALUES (?, ?)", (body.field_id, body.name))
    return get_or_404(conn, "plot", pid)


@app.get("/crops", dependencies=[Depends(auth)])
def list_crops(conn=Depends(get_conn)):
    return rows(conn, "SELECT * FROM crop ORDER BY id")


@app.post("/crops", dependencies=[Depends(auth)], status_code=201)
def create_crop(body: CropIn, conn=Depends(get_conn)):
    get_or_404(conn, "plot", body.plot_id)
    cid = insert(
        conn,
        "INSERT INTO crop (plot_id, name, planted_on, expected_harvest_note) VALUES (?, ?, ?, ?)",
        (body.plot_id, body.name, body.planted_on, body.expected_harvest_note),
    )
    return get_or_404(conn, "crop", cid)


@app.get("/work-logs", dependencies=[Depends(auth)])
def list_work_logs(date_from: Optional[str] = None, date_to: Optional[str] = None, conn=Depends(get_conn)):
    sql = "SELECT * FROM work_log"
    params = []
    clauses = []
    if date_from:
        clauses.append("date >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("date <= ?")
        params.append(date_to)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY date, id"
    return rows(conn, sql, params)


@app.post("/work-logs", dependencies=[Depends(auth)], status_code=201)
def create_work_log(body: WorkLogIn, conn=Depends(get_conn)):
    get_or_404(conn, "plot", body.plot_id)
    if body.crop_id is not None:
        get_or_404(conn, "crop", body.crop_id)
    wid = insert(
        conn,
        "INSERT INTO work_log (date, plot_id, crop_id, work_type, memo) VALUES (?, ?, ?, ?, ?)",
        (body.date, body.plot_id, body.crop_id, body.work_type, body.memo),
    )
    return get_or_404(conn, "work_log", wid)


@app.get("/harvests", dependencies=[Depends(auth)])
def list_harvests(conn=Depends(get_conn)):
    return rows(conn, "SELECT * FROM harvest ORDER BY date, id")


@app.post("/harvests", dependencies=[Depends(auth)], status_code=201)
def create_harvest(body: HarvestIn, conn=Depends(get_conn)):
    get_or_404(conn, "crop", body.crop_id)
    hid = insert(
        conn,
        "INSERT INTO harvest (date, crop_id, amount, unit, memo) VALUES (?, ?, ?, ?, ?)",
        (body.date, body.crop_id, body.amount, body.unit, body.memo),
    )
    return get_or_404(conn, "harvest", hid)


@app.get("/summary/now", dependencies=[Depends(auth)])
def summary_now(conn=Depends(get_conn)):
    plots = rows(
        conn,
        "SELECT p.*, f.name AS field_name FROM plot p JOIN field f ON f.id = p.field_id ORDER BY p.id",
    )
    for plot in plots:
        plot["crops"] = rows(conn, "SELECT * FROM crop WHERE plot_id = ? ORDER BY id", (plot["id"],))
        plot["recent_work_logs"] = rows(
            conn,
            "SELECT * FROM work_log WHERE plot_id = ? ORDER BY date DESC, id DESC LIMIT 5",
            (plot["id"],),
        )
    return {"plots": plots}
