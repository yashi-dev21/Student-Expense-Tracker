# Student Expense Tracker

A Flask-based web application for recording, managing, filtering, analyzing, and exporting student expenses.

## Features

- Add expenses
- View expenses
- Edit expenses
- Delete expenses
- Input validation
- Future-date prevention
- Category and payment-method validation
- Search expenses
- Filter by category
- Filter by payment method
- Filter by date range
- Dynamic spending summaries
- Spending analytics
- Category chart
- Payment-method chart
- Monthly spending chart
- CSV export
- Excel export
- SQLite database
- Git version control

## Tech Stack

- Python 3.11
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js
- openpyxl
- Git / GitHub

## Project Structure

```text
Student-Expense-Tracker/
│
├── app/
│   ├── __init__.py
│   ├── constants.py
│   ├── db.py
│   ├── routes.py
│   ├── services.py
│   ├── validators.py
│   ├── templates/
│   └── static/
│
├── data/
│   └── expenses.db
│
├── .gitignore
├── requirements.txt
├── README.md
└── run.py 