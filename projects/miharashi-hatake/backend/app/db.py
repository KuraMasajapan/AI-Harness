import os
import sqlite3

DB_PATH = os.environ.get("MIHARASHI_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "miharashi.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS field (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location_note TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS plot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_id INTEGER NOT NULL REFERENCES field(id),
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS crop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plot_id INTEGER NOT NULL REFERENCES plot(id),
    name TEXT NOT NULL,
    planted_on TEXT NOT NULL,
    expected_harvest_note TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS work_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    plot_id INTEGER NOT NULL REFERENCES plot(id),
    crop_id INTEGER REFERENCES crop(id),
    work_type TEXT NOT NULL,
    memo TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS harvest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    crop_id INTEGER NOT NULL REFERENCES crop(id),
    amount REAL NOT NULL,
    unit TEXT NOT NULL,
    memo TEXT DEFAULT ''
);
"""


def connect(path: str | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(path or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: str | None = None) -> None:
    with connect(path) as conn:
        conn.executescript(SCHEMA)
