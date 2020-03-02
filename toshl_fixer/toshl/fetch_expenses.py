from functools import partial

import pandas as pd

from toshl import Entry
from .labels import LabelMapping
from ..settings import client


def _convert_id_to_name(expense, mapping: LabelMapping):
    expense['tag'] = mapping.get_tag_name_from_id(expense['tag'])
    expense['category'] = mapping.get_category_name_from_id(expense['category'])
    return expense


def _fetch_entries(from_date, to_date):
    entries = pd.DataFrame((Entry(client).list(from_date=from_date, to_date=to_date)))
    return entries


def _filter_expenses(entries):
    entries["desc"] = entries["desc"].str.split(pat="\n").str[0]
    filtered = entries.drop(entries[entries.desc == ""].index)
    filtered = filtered.drop(filtered[filtered.amount > 0].index)
    return filtered


def _adjust_columns(expenses):
    df = expenses[["id", "desc", "amount", "category", "tags", 'date']]
    df["tag"] = df["tags"].str[0]
    del df["tags"]
    return df


def _replace_numbers_for_labels(expenses):
    mapping = LabelMapping.create_from_toshl()
    expenses = expenses.apply(partial(_convert_id_to_name, mapping=mapping), axis=1)
    return expenses


def fetch_expenses(from_date, to_date):
    entries = _fetch_entries(from_date, to_date)
    expenses = _filter_expenses(entries)
    expenses = _adjust_columns(expenses)
    labeled_expenses = _replace_numbers_for_labels(expenses)
    return labeled_expenses
