import concurrent
import datetime
import logging
import os
import threading
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from difflib import SequenceMatcher
from typing import Dict, List

import requests
from dotenv import load_dotenv

TOSHL_URL = 'https://api.toshl.com'

logging.basicConfig(level=logging.INFO, format='[%(threadName)s %(pathname)s %(levelname)s]: %(message)s')
logger = logging.getLogger()

load_dotenv()

TOKEN = os.getenv('TOSHL_TOKEN')
r = requests.Session()
r.auth = (TOKEN, '')


def similar(a, b):
    logger.debug('Before split: %s, %s', a, b)
    a, b = a.split('\n')[0], b.split('\n')[0]
    logger.debug('After split: %s, %s', a, b)
    similarity = SequenceMatcher(isjunk=None, a=a, b=b).ratio()
    return similarity


def ask_to_delete(_id):
    logger.handlers[0].flush()
    answer = input('Should I delete (y / n)')
    if answer == 'y':
        delete_entry(_id)
    else:
        logger.info('skipping')


def delete_entry(_id):
    url = f'{TOSHL_URL}/entries/{_id}'
    logger.debug(url)
    r.delete(url)


def get_entries(page=0):
    return r.get(f'{TOSHL_URL}/entries',
                 params={'from': '2018-01-01', 'to': str(datetime.date.today()), 'page': page, 'include_deleted': True})


def get_all_entries():
    page = 0
    total_entries = []
    while True:
        result = get_entries(page)
        total_entries.extend(result.json())
        if 'next' not in result.links:
            break
        page += 1

    entries_by_id = {entry['id']: entry for entry in total_entries}
    return entries_by_id


def find_duplicates(entries) -> List[List[Dict]]:
    counter = defaultdict(list)
    for entry in entries.values():
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


def delete_duplicates(entries):
    duplicates = find_duplicates(entries)
    for dup_entries in duplicates:
        delete_entry(dup_entries[0]['id'])


def delete_visa(entries_by_id):
    for _id, entry in entries_by_id.items():
        if entry['desc'] == 'לאומי ויזה י':
            logger.info(f'{entry["desc"]}, {entry["amount"]}')
            ask_to_delete(_id)


def create_tags_mapping(entries):
    relevant_entries = [entry for entry in entries.values()
                        if entry['date'] >= '2019-09-01'
                        and all(name not in entry['desc'] for name in ['העברה', 'הע.', 'שיק', 'כספו'])
                        and 'tags' in entry]
    tag_mapping = defaultdict(set)
    for entry in relevant_entries:
        tag_mapping[entry['tags'][0], entry['category']].add(entry['desc'].split('\n')[0])
    return tag_mapping


def update_entries_tags(entries, tag_mapping):
    relevant_entries = [entry for entry in entries.values()
                        if entry['date'] < '2019-09-01'
                        and 'transaction' not in entry]
    for entry in relevant_entries:
        for key, desc in tag_mapping.items():
            if entry['desc'] in desc:
                entry['tags'] = [key[0]]
                entry['category'] = key[1]
                yield entry


def update_entry(entry):
    refreshed_entity = r.get(f'{TOSHL_URL}/entries/{entry["id"]}').json()
    entry['modified'] = refreshed_entity['modified']
    response = r.put(f'{TOSHL_URL}/entries/{entry["id"]}', json=entry)
    logger.info(f'Done for {entry["id"]}')
    try:
        response.raise_for_status()
    except:
        logger.exception(f'Failed to update entry {entry["id"]}')

def create_entry(entry):
    del entry['deleted']
    response = r.post(f'{TOSHL_URL}/entries', json=entry)
    logger.info(f'Done for {entry["id"]}')
    try:
        response.raise_for_status()
    except:
        logger.exception(f'Failed to update entry {entry["id"]}')

def recreated_delete_entries(entries):
    relevant_entries = [entry for entry in entries.values()
                        if entry['date'] >= '2019-12-01'
                        and entry['deleted']]
    return relevant_entries

def main():
    entries: Dict[str, Dict] = get_all_entries()
    # tag_mapping = create_tags_mapping(entries)
    # newly_tag_entries = list(update_entries_tags(entries, tag_mapping))
    #
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     list(executor.map(update_entry, newly_tag_entries))

    # update_entries(newly_tag_entries)
    # delete_duplicates(entries)
    # delete_visa(entries)


if __name__ == '__main__':
    main()
