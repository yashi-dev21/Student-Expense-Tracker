import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "data" / "expenses.db"
SCHEMA_FILE = BASE_DIR / "app" / "schema.sql"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE)

    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        connection.executescript(file.read())

    connection.commit()
    connection.close()