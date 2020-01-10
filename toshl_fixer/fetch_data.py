import json

import pandas as pd

from toshl import Category, Tag, Entry
from .utils.common import client, DATA_DIR


def name_categories(expenses, categories):
    categories = categories[["id", "name"]]
    categories.rename(columns={"id": "cat_id", "name": "cat_name"}, inplace=True)
    merged = expenses.merge(
        categories, left_on="category", right_on="cat_id", how="left",
    )
    del merged["cat_id"]
    del merged["category"]
    merged = merged.rename(columns={"cat_name": "category"})
    return merged


def name_tags(expenses, tags):
    tags = tags[["id", "name"]]
    tags.rename(columns={"id": "tag_id", "name": "tag_name"}, inplace=True)
    merged = expenses.merge(tags, left_on="tag", right_on="tag_id", how="left", )
    del merged["tag_id"]
    del merged["tag"]
    merged = merged.rename(columns={"tag_name": "tag"})
    return merged


def fetch_data(from_date, to_date):
    categories = pd.DataFrame.from_dict(Category(client).list())
    tags = pd.DataFrame.from_dict(Tag(client).list())
    entries = list(Entry(client).list(from_date=from_date, to_date=to_date))
    entries_df = pd.DataFrame(entries)
    return categories, tags, entries_df


def filter_expenses(entries, filter_empty_tags=True):
    relevant = entries[["id", "desc", "amount", "category", "tags", 'date']]
    relevant["desc"] = relevant["desc"].str.split(pat="\n").str[0]
    filtered = relevant.drop(relevant[relevant.desc == ""].index)
    filtered = filtered.drop(filtered[filtered.amount > 0].index)
    if filter_empty_tags is True:
        filtered = filtered[filtered["tags"].notnull()]
    filtered["tag"] = relevant["tags"].str[0]
    del filtered["tags"]
    return filtered


def merge_labels(expenses, categories, tags):
    merged = name_categories(expenses, categories)
    merged = name_tags(merged, tags)
    return merged


def write_to_csv(expenses):
    expenses.to_csv(DATA_DIR / 'expenses.csv', index=False)


def dump_cat_and_tags_mapping(categories, tags):
    mapping = {
        "categories": categories.set_index('name').to_dict()['id'],
        "tags": tags.set_index('name').to_dict()['id']
    }
    with open(DATA_DIR / 'mapping.json', 'w') as f:
        json.dump(mapping, f, indent=4, sort_keys=True)


def main(from_date="2019-01-01", to_date="2020-01-31", filter_empty_tags=False):
    categories, tags, entries = fetch_data(from_date, to_date)
    expenses = filter_expenses(entries, filter_empty_tags)
    labeled_expenses = merge_labels(expenses, categories, tags)
    write_to_csv(labeled_expenses)
    dump_cat_and_tags_mapping(categories, tags)


def run():
    main(from_date="2019-01-01", to_date="2020-01-31", filter_empty_tags=False)


if __name__ == "__main__":
    run()
