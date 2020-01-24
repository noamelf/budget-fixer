import logging
from collections import defaultdict
from difflib import SequenceMatcher
from typing import List, Dict

from toshl_fixer.data.expenses import get_expenses
from toshl_fixer.toshl.entry import delete_entry_async

logger = logging.getLogger(__name__)


def delete_expense(entry):
    delete_entry_async(entry["id"])


def delete_duplicates(from_date, to_date):
    expenses = get_expenses(from_date, to_date)
    expenses = expenses[expenses.duplicated(subset=['amount', 'date'], keep=False)]
    merged = expenses.merge(right=expenses, on=['amount', 'date'])
    # merged = merged[merged['desc_x'] != merged['desc_y']]
    print(merged)
    if input('Delete entries?') == 'y':
        merged.apply(delete_expense, axis=1)


def similar(a, b):
    logger.debug('Before split: %s, %s', a, b)
    a, b = a.split('\n')[0], b.split('\n')[0]
    logger.debug('After split: %s, %s', a, b)
    similarity = SequenceMatcher(isjunk=None, a=a, b=b).ratio()
    return similarity


def find_duplicates(entries) -> List[List[Dict]]:
    counter = defaultdict(list)
    for _id, entry in entries.items():
        entry_key = entry['amount'], entry['date']
        existing_entry = counter.get(entry_key)
        if existing_entry:
            existing_entry_desc = existing_entry[0]['desc']
            similarity = similar(existing_entry_desc, entry['desc'])
            logger.info(f'For entry {entry["desc"]}.\n'
                        f'Found existing one: {existing_entry_desc}.\n'
                        f'Similarity score is: {similarity}')
            if similarity > 0.7:
                logger.info('Adding to duplicates')
                counter[entry_key].append(entry)
            else:
                logger.info('Skipping')
        else:
            counter[entry_key].append(entry)
    duplicates = [dup_entries for dup_entries in counter.values() if len(dup_entries) >= 2]
    return duplicates
