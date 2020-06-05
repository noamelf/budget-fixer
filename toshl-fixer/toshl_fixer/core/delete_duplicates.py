import logging
from difflib import SequenceMatcher

import pandas as pd

from toshl_fixer.data_access.expenses import get_expenses
from toshl_fixer.toshl.entry import delete_entry_async

logger = logging.getLogger(__name__)


def delete_expense(entry):
    logger.info(f'{entry}')
    delete_entry_async(entry["id_x"])


def similar(row):
    return SequenceMatcher(isjunk=None, a=row['desc_x'], b=row['desc_y']).ratio()


def delete_duplicates(from_date=None, to_date=None, expenses: pd.DataFrame = None):
    if (not from_date or not to_date) and expenses.empty:
        expenses = get_expenses(from_date, to_date)
    expenses = expenses[expenses.duplicated(subset=['amount', 'date'], keep=False)]
    merged = expenses.merge(right=expenses, on=['amount', 'date'])
    merged: pd.DataFrame = merged[merged['id_x'] != merged['id_y']]
    merged = merged.iloc[::2, :]
    merged['score'] = merged.apply(similar, axis=1)
    duplicates = merged[merged['score'] > 0.6]
    logger.info(f'Duplicate entries: {"none" if duplicates.empty else duplicates}')
    duplicates.apply(delete_expense, axis=1)
