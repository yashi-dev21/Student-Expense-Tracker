from datetime import date

from .constants import (
    ALLOWED_CATEGORIES,
    ALLOWED_PAYMENT_METHODS,
)


def validate_expense(
    amount,
    category,
    expense_date,
    payment_method,
):
    errors = []

    # Validate amount
    try:
        amount_value = float(amount)

        if amount_value <= 0:
            errors.append("Amount must be greater than 0.")

    except (TypeError, ValueError):
        errors.append("Amount must be a valid number.")
        amount_value = None

    # Validate category
    if category not in ALLOWED_CATEGORIES:
        errors.append("Please select a valid category.")

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
    if payment_method not in ALLOWED_PAYMENT_METHODS:
        errors.append(
            "Please select a valid payment method."
        )

    return errors, amount_value