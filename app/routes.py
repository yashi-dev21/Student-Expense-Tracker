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

# Add a new expense
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
@main.route("/edit/<int:expense_id>", methods=["GET", "POST"])

# Edit an expense
def edit_expense(expense_id):
    connection = get_db_connection()

    expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,),
    ).fetchone()

    if expense is None:
        connection.close()
        return "Expense not found", 404

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        expense_date = request.form["expense_date"]
        payment_method = request.form["payment_method"]

        connection.execute(
            """
            UPDATE expenses
            SET amount = ?,
                category = ?,
                description = ?,
                expense_date = ?,
                payment_method = ?
            WHERE id = ?
            """,
            (
                amount,
                category,
                description,
                expense_date,
                payment_method,
                expense_id,
            ),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("main.home"))

    connection.close()

    return render_template("edit_expense.html", expense=expense)

# Delete an expense
@main.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("main.home"))
