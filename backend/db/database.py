"""SQLite-åtkomst med standardbibliotekets ``sqlite3``.

Databasfilen ligger i ``backend/storage/`` och är gitignorerad. Tabellerna
skapas av :func:`init_db`, som körs vid appstart.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "storage" / "dataview.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS datasets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    filename     TEXT NOT NULL,
    n_rows       INTEGER NOT NULL,
    n_cols       INTEGER NOT NULL,
    uploaded_at  TEXT NOT NULL DEFAULT (datetime('now')),
    profile_json TEXT
);

CREATE TABLE IF NOT EXISTS runs (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id   INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    target       TEXT NOT NULL,
    problem_type TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    status       TEXT NOT NULL DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS models (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    model_type    TEXT NOT NULL,
    is_best       INTEGER NOT NULL DEFAULT 0,
    metrics_json  TEXT,
    model_path    TEXT,
    features_json TEXT
);
"""


def get_connection(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    """Öppnar en anslutning till databasen och skapar mappen om den saknas."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path | str = DB_PATH) -> None:
    """Skapar tabellerna datasets, runs och models om de inte redan finns."""
    conn = get_connection(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Databas initierad: {DB_PATH}")
