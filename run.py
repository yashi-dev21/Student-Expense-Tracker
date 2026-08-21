# from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def home():
#     return "Student Expense Tracker is running!"


# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask
# from pathlib import Path
# import sqlite3

# app = Flask(__name__)

# DATABASE = Path(__file__).resolve().parent / "data" / "expenses.db"
# SCHEMA = Path(__file__).resolve().parent / "app" / "schema.sql"


# def init_database():
#     DATABASE.parent.mkdir(exist_ok=True)

#     connection = sqlite3.connect(DATABASE)

#     with open(SCHEMA, "r", encoding="utf-8") as file:
#         connection.executescript(file.read())

#     connection.commit()
#     connection.close()


# @app.route("/")
# def home():
#     return "Student Expense Tracker is running!"


# if __name__ == "__main__":
#     init_database()
#     app.run(debug=True)


from app import create_app
from pathlib import Path
import sqlite3

app = create_app()

DATABASE = Path(__file__).resolve().parent / "data" / "expenses.db"
SCHEMA = Path(__file__).resolve().parent / "app" / "schema.sql"


def init_database():
    DATABASE.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE)

    with open(SCHEMA, "r", encoding="utf-8") as file:
        connection.executescript(file.read())

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_database()
    app.run(debug=True)