from datetime import date

from toshl_fixer.data_access.expenses import write_expenses
from toshl_fixer.toshl.fetch_expenses import fetch_expenses


def fetch_data(save=True):
    expenses = fetch_expenses(from_date='01-01-2019', to_date=str(date.today()))
    if save:
        write_expenses(expenses)
    return expenses
