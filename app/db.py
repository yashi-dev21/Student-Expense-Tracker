import os
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SCHEMA_FILE = BASE_DIR / "app" / "schema.sql"


# Local development:
#     C:\DEV\Projects\Student-Expense-Tracker\data
#
# Render:
#     Set DATABASE_DIR=/tmp/student-expense-tracker
DATABASE_DIR = Path(
    os.environ.get(
        "DATABASE_DIR",
        str(BASE_DIR / "data"),
    )
)

DATABASE = DATABASE_DIR / "expenses.db"


def get_db_connection():
    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        str(DATABASE)
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        str(DATABASE)
    )

    with open(
        SCHEMA_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        connection.executescript(
            file.read()
        )

    connection.commit()
    connection.close()