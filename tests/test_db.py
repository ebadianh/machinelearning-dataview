"""Tester för SQLite-lagret."""

from backend.db.database import get_connection, init_db


def test_init_db_creates_tables(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    finally:
        conn.close()

    tables = {row["name"] for row in rows}
    assert {"datasets", "runs", "models"} <= tables
