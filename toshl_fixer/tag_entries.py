import json
from functools import partial

import pandas as pd

from toshl import Entry
from toshl_fixer.common import DATA_DIR, csv_name, client
from toshl_fixer.tag_classifier import Classifier
import logging

logger = logging.getLogger(__name__)


def map_ids(data):
    with open(DATA_DIR / "mapping.json") as f:
        mapping = json.load(f)
    del mapping["categories"]["unsorted"]
    del mapping["categories"]["Reconciliation"]
    return data.replace({"est_cat": mapping["categories"], "est_tag": mapping["tags"]})


def infer(classifier, expense):
    category, probability = classifier.infer(expense["desc"])
    expense["category/tag"] = "/".join(category)
    expense["probability"] = probability
    expense["est_cat"] = category[0]
    expense["est_tag"] = category[1]
    return expense


def tag_expenses(from_date, to_date):
    expenses = pd.read_csv(DATA_DIR / csv_name(from_date, to_date))
    classifier = Classifier()
    classifier.train_classifier()
    loaded_infer = partial(infer, classifier)
    expenses = expenses.apply(loaded_infer, axis=1)
    return expenses


def update_tags(from_date="2019-11-01", to_date="2019-11-31"):
    expenses = tag_expenses(from_date, to_date)
    expenses: pd.DataFrame = map_ids(expenses)
    entry_client = Entry(client)
    for _, expense in expenses.iterrows():
        if expense['probability'] < 0.5:
            logger.info(f'Skipping {expense["desc"]}')
            continue
        entry = entry_client.get(expense['id'])
        entry['category'] = expense['est_cat']
        entry['tags'] = [expense['est_tag']]
        entry['desc'] = expense['desc']
        entry_client.put(entry)


if __name__ == '__main__':
    update_tags()
