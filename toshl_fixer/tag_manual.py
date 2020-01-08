import json

import pandas as pd
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

from toshl import Entry
from toshl_fixer.common import DATA_DIR, csv_name, client

with open(DATA_DIR / "mapping.json") as f:
    mapping = json.load(f)

tags_completer = FuzzyWordCompleter(list(mapping["tags"].keys()))
category_completer = FuzzyWordCompleter(list(mapping["categories"].keys()))

expenses = pd.read_csv(DATA_DIR / csv_name("2019-11-01", "2019-11-31"))
entry_client = Entry(client)
for _, expense in expenses.iterrows():
    print(f"{expense['desc']}: {expense['category']}/{expense['tag']} {expense['amount']}")
    category = prompt("Enter category: ", completer=category_completer, search_ignore_case=True)
    tag = prompt("Enter tag: ", completer=tags_completer)
    if category == "" or tag == "":
        continue

    entry = entry_client.get(expense["id"])
    entry["category"] = mapping["categories"][category]
    entry["tags"] = [mapping["tags"][tag]]
    entry["desc"] = expense["desc"]
    entry_client.put(entry)
