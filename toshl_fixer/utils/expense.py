import json
import logging

import pandas as pd

from toshl import Entry
from .common import DATA_DIR, client

logger = logging.getLogger(__name__)

entry = Entry(client)


class Mapping:
    def __init__(self):
        with open(DATA_DIR / "mapping.json") as f:
            mapping = json.load(f)
        self.tags = mapping["tags"]
        self.categories = mapping["categories"]

    def get_tag_id(self, tag):
        return self.tags.get(tag)

    def get_category_id(self, category):
        return self.categories[category]


def get_expenses(from_date=None, to_date=None):
    df = pd.read_csv(DATA_DIR / "expenses.csv")
    df = df.fillna("missing")
    if from_date and to_date:
        return df[(df.date > from_date) & (df.date < to_date)]
    return df


def update_toshl(entry_id, **updates):
    mapping = Mapping()
    if "tag" in updates:
        tag_id = mapping.get_tag_id(updates["tag"])
        updates["tag"] = [tag_id] if tag_id else []
    if "category" in updates:
        updates["category"] = mapping.get_category_id(updates["category"])

    entry.update_entry(entry_id, **updates)
