from toshl_fixer.data.expenses import get_expenses
from toshl_fixer.toshl.entry import delete_entry_async


def delete_expense(entry):
    delete_entry_async(entry["id"])


def delete_credit_entries(from_date, to_date):
    expenses = get_expenses(from_date, to_date)
    # expenses = expenses[expenses['desc'].str.contains('ויזה')]
    print(expenses)
    if input('Delete entries?') == 'y':
        expenses.apply(delete_expense, axis=1)
