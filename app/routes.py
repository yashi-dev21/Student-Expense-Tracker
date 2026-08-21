from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db_connection

main = Blueprint("main", __name__)


@main.route("/")
def home():
    connection = get_db_connection()
    expenses = connection.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
    ).fetchall()
    connection.close()

    return render_template("index.html", expenses=expenses)


@main.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        expense_date = request.form["expense_date"]
        payment_method = request.form["payment_method"]

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO expenses
            (amount, category, description, expense_date, payment_method)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                amount,
                category,
                description,
                expense_date,
                payment_method,
            ),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("main.home"))

    return render_template("add_expense.html")