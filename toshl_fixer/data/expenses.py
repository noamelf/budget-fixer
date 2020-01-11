import logging

import pandas as pd

from ..settings import MANUALLY_TAGGED_TO_DATE, MANUALLY_TAGGED_FROM_DATE, DATA_DIR

logger = logging.getLogger(__name__)

ALL_EXPENSES_PATH = DATA_DIR / 'expenses.csv'
RT_EXPENSES_PATH = DATA_DIR / 'rt_tagging.csv'


def get_expenses(from_date=None, to_date=None):
    df = pd.read_csv(ALL_EXPENSES_PATH)
    df = df.fillna("missing")
    if from_date and to_date:
        return df[(df.date >= from_date) & (df.date <= to_date)]
    return df


def get_training_expenses(from_date=None, to_date=None):
    df: pd.DataFrame = get_expenses(from_date=from_date, to_date=to_date)
    rt_expenses = load_real_time_tagged_expense()
    df.append(rt_expenses)
    return df


def get_tagged_training_expenses():
    return get_training_expenses(from_date=MANUALLY_TAGGED_FROM_DATE, to_date=MANUALLY_TAGGED_TO_DATE)


def write_real_time_tagged_expense(expense):
    df = load_real_time_tagged_expense()
    df = df.append(expense, ignore_index=True)
    df.write_csv(RT_EXPENSES_PATH)


def load_real_time_tagged_expense():
    try:
        df = pd.read_csv(RT_EXPENSES_PATH)
    except:
        df = pd.DataFrame()

    return df


def write_expenses(expenses):
    expenses.to_csv(ALL_EXPENSES_PATH, index=False)
