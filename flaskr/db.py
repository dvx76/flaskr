import sqlite3
from pathlib import Path

from flask import current_app, g

LOCAL_DIRECTORY = Path(__file__).parent
SQLITE_DB_FILE = str(LOCAL_DIRECTORY / "flaskr.sqlite")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], uri=True)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exc=None):
    if "db" in g:
        g.db.close()


def init_db(database: str = SQLITE_DB_FILE):
    db = sqlite3.connect(database, uri=True)

    with open(LOCAL_DIRECTORY / "schema.sql") as schema:
        db.executescript(schema.read())

    print("SQLite schema created. Tables in DB:")
    result = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(result.fetchall())


if __name__ == "__main__":
    init_db()
