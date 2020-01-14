from toshl_fixer.data.expenses import write_expenses
from toshl_fixer.toshl.expenses import fetch_expenses


def fetch_data(from_date, to_date):
    expenses = fetch_expenses(from_date, to_date)
    write_expenses(expenses)
