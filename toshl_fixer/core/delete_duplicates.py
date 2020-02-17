import logging
from collections import defaultdict
from difflib import SequenceMatcher
from typing import List, Dict

import pandas as pd

from toshl_fixer.data.expenses import get_expenses
from toshl_fixer.toshl.entry import delete_entry_async

logger = logging.getLogger(__name__)


def delete_expense(entry):
    delete_entry_async(entry["id"])


def delete_duplicates(from_date, to_date):
    expenses = get_expenses(from_date, to_date)
    expenses = expenses[expenses.duplicated(subset=['amount', 'date'], keep=False)]
    merged = expenses.merge(right=expenses, on=['amount', 'date'])
    merged: pd.DataFrame = merged[merged['id_x'] != merged['id_y']]
    for _, row in merged.iloc[::2, :].iterrows():
        if input(f'{row}\n\nDelete expense? ') == 'y':
            delete_entry_async(row["id_x"])
