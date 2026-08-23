import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "data"
DATABASE = DATABASE_DIR / "expenses.db"

SCHEMA_FILE = BASE_DIR / "app" / "schema.sql"


def get_db_connection():
    # Make sure the database directory exists
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(DATABASE))

    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    # Make sure the database directory exists
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(DATABASE))

    with open(
        SCHEMA_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        connection.executescript(file.read())

    connection.commit()
    connection.close()