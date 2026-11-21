"""Insert sample data into the みはらし畑 database.

Usage: python3 scripts/seed_sample_data.py
Uses MIHARASHI_DB_PATH if set, otherwise the default miharashi.db next to this script's parent.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import connect, init_db  # noqa: E402


def main() -> None:
    init_db()
    conn = connect()
    try:
        field_id = conn.execute(
            "INSERT INTO field (name, location_note) VALUES (?, ?)",
            ("みはらし畑", "丘の上、日当たり良好"),
        ).lastrowid
        plot_a = conn.execute(
            "INSERT INTO plot (field_id, name) VALUES (?, ?)", (field_id, "A区画")
        ).lastrowid
        plot_b = conn.execute(
            "INSERT INTO plot (field_id, name) VALUES (?, ?)", (field_id, "B区画")
        ).lastrowid
        tomato = conn.execute(
            "INSERT INTO crop (plot_id, name, planted_on, expected_harvest_note) VALUES (?, ?, ?, ?)",
            (plot_a, "トマト", "2026-04-10", "7月上旬〜9月"),
        ).lastrowid
        edamame = conn.execute(
            "INSERT INTO crop (plot_id, name, planted_on, expected_harvest_note) VALUES (?, ?, ?, ?)",
            (plot_b, "枝豆", "2026-05-05", "7月下旬"),
        ).lastrowid
        conn.execute(
            "INSERT INTO work_log (date, plot_id, crop_id, work_type, memo) VALUES (?, ?, ?, ?, ?)",
            ("2026-04-10", plot_a, tomato, "植付け", "中玉トマトの苗を3本"),
        )
        conn.execute(
            "INSERT INTO work_log (date, plot_id, crop_id, work_type, memo) VALUES (?, ?, ?, ?, ?)",
            ("2026-06-01", plot_a, tomato, "水やり", None),
        )
        conn.execute(
            "INSERT INTO work_log (date, plot_id, crop_id, work_type, memo) VALUES (?, ?, ?, ?, ?)",
            ("2026-06-15", plot_b, edamame, "除草", None),
        )
        conn.execute(
            "INSERT INTO harvest (date, crop_id, amount, unit, memo) VALUES (?, ?, ?, ?, ?)",
            ("2026-07-20", tomato, 12, "個", "初収穫"),
        )
        conn.commit()
    finally:
        conn.close()
    print("Sample data inserted.")


if __name__ == "__main__":
    main()
