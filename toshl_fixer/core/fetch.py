from datetime import date

from toshl_fixer.data.expenses import write_expenses
from toshl_fixer.toshl.fetch_expenses import fetch_expenses


def fetch_data():
    expenses = fetch_expenses(from_date='01-01-2019', to_date=str(date.today()))
    write_expenses(expenses)
