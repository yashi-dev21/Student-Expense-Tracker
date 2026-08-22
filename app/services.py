from .db import get_db_connection


def get_filtered_expenses(
    search="",
    category="",
    payment_method="",
    start_date="",
    end_date="",
):
    connection = get_db_connection()

    query = "SELECT * FROM expenses WHERE 1=1"
    parameters = []

    if search:
        query += " AND (category LIKE ? OR description LIKE ?)"
        search_value = f"%{search}%"
        parameters.extend([search_value, search_value])

    if category:
        query += " AND category = ?"
        parameters.append(category)

    if payment_method:
        query += " AND payment_method = ?"
        parameters.append(payment_method)

    if start_date:
        query += " AND expense_date >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND expense_date <= ?"
        parameters.append(end_date)

    query += " ORDER BY expense_date DESC, id DESC"

    expenses = connection.execute(
        query,
        parameters,
    ).fetchall()

    connection.close()

    return expenses