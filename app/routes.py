from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db_connection
from datetime import date
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
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        expense_date = request.form.get("expense_date", "").strip()
        payment_method = request.form.get("payment_method", "").strip()

        errors = []

        # Validate amount
        try:
            amount_value = float(amount)

            if amount_value <= 0:
                errors.append("Amount must be greater than 0.")

        except ValueError:
            errors.append("Amount must be a valid number.")

        # Validate category
        if not category:
            errors.append("Category is required.")

        # Validate date
        # Validate date
        if not expense_date:
            errors.append("Expense date is required.")
        else:
            try:
                selected_date = date.fromisoformat(expense_date)

                if selected_date > date.today():
                    errors.append("Expense date cannot be in the future.")

            except ValueError:
                errors.append("Please enter a valid date.")

                # Validate payment method
                allowed_methods = {"Cash", "UPI", "Card", "Other"}

                if payment_method not in allowed_methods:
                    errors.append("Please select a valid payment method.")

        # If validation fails
        if errors:
            return render_template(
                "add_expense.html",
                errors=errors,
                today=date.today().isoformat(),
            )

        # Save valid expense
        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO expenses
            (amount, category, description, expense_date, payment_method)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                amount_value,
                category,
                description,
                expense_date,
                payment_method,
            ),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("main.home"))

    return render_template(
        "add_expense.html",
        errors=[],
        today=date.today().isoformat(),
    )
# Edit an expense

@main.route("/edit/<int:expense_id>", methods=["GET", "POST"])
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
