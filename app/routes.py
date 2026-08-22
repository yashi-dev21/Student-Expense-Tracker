from collections import defaultdict
from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for

from .db import get_db_connection


main = Blueprint("main", __name__)


@main.route("/")
def home():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    payment_method = request.args.get("payment_method", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()

    connection = get_db_connection()

    query = "SELECT * FROM expenses WHERE 1=1"
    parameters = []

    # Search category or description
    if search:
        query += " AND (category LIKE ? OR description LIKE ?)"
        search_value = f"%{search}%"
        parameters.extend([search_value, search_value])

    # Category filter
    if category:
        query += " AND category = ?"
        parameters.append(category)

    # Payment method filter
    if payment_method:
        query += " AND payment_method = ?"
        parameters.append(payment_method)

    # Start date
    if start_date:
        query += " AND expense_date >= ?"
        parameters.append(start_date)

    # End date
    if end_date:
        query += " AND expense_date <= ?"
        parameters.append(end_date)

    query += " ORDER BY expense_date DESC, id DESC"

    expenses = connection.execute(
        query,
        parameters
    ).fetchall()

    # Get categories for filter dropdown
    categories = connection.execute(
        "SELECT DISTINCT category FROM expenses ORDER BY category"
    ).fetchall()

    # Summary calculations
    total_expenses = sum(
        float(expense["amount"])
        for expense in expenses
    )

    expense_count = len(expenses)

    if expense_count > 0:
        average_expense = total_expenses / expense_count

        highest_expense = max(
            float(expense["amount"])
            for expense in expenses
        )
    else:
        average_expense = 0
        highest_expense = 0

    # Spending by category
    category_totals = defaultdict(float)

    # Spending by payment method
    payment_totals = defaultdict(float)

    # Spending by month
    monthly_totals = defaultdict(float)

    for expense in expenses:
        amount = float(expense["amount"])

        category_totals[expense["category"]] += amount

        payment_totals[expense["payment_method"]] += amount

        month = expense["expense_date"][:7]

        monthly_totals[month] += amount

    connection.close()

    return render_template(
        "index.html",
        expenses=expenses,
        categories=categories,
        search=search,
        selected_category=category,
        selected_payment_method=payment_method,
        start_date=start_date,
        end_date=end_date,
        today=date.today().isoformat(),
        total_expenses=total_expenses,
        expense_count=expense_count,
        average_expense=average_expense,
        highest_expense=highest_expense,
        category_totals=dict(category_totals),
        payment_totals=dict(payment_totals),
        monthly_totals=dict(sorted(monthly_totals.items())),
    )


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
        if not expense_date:
            errors.append("Expense date is required.")
        else:
            try:
                selected_date = date.fromisoformat(expense_date)

                if selected_date > date.today():
                    errors.append(
                        "Expense date cannot be in the future."
                    )

            except ValueError:
                errors.append("Please enter a valid date.")

        # Validate payment method
        allowed_methods = {"Cash", "UPI", "Card", "Other"}

        if payment_method not in allowed_methods:
            errors.append(
                "Please select a valid payment method."
            )

        # Show validation errors
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
        if not expense_date:
            errors.append("Expense date is required.")
        else:
            try:
                selected_date = date.fromisoformat(expense_date)

                if selected_date > date.today():
                    errors.append(
                        "Expense date cannot be in the future."
                    )

            except ValueError:
                errors.append("Please enter a valid date.")

        # Validate payment method
        allowed_methods = {"Cash", "UPI", "Card", "Other"}

        if payment_method not in allowed_methods:
            errors.append(
                "Please select a valid payment method."
            )

        # Show validation errors
        if errors:
            connection.close()

            return render_template(
                "edit_expense.html",
                expense=expense,
                errors=errors,
                today=date.today().isoformat(),
            )

        # Update expense
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
                amount_value,
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

    return render_template(
        "edit_expense.html",
        expense=expense,
        errors=[],
        today=date.today().isoformat(),
    )


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