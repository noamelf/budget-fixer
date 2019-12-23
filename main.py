import logging
import os
from collections import defaultdict
from difflib import SequenceMatcher

import requests
from dotenv import load_dotenv

TOSHL_URL = 'https://api.toshl.com'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

load_dotenv()

TOKEN = os.getenv('TOKEN')
session = requests.Session()
session.auth = (TOKEN, '')


def similar(a, b):
    logger.debug('Before split: %s, %s', a, b)
    a, b = a.split('\n')[0], b.split('\n')[0]
    similarity = SequenceMatcher(isjunk=None, a=a.split('\n')[0], b=b.split('\n')[0]).ratio()
    logger.info('Items: %s, %s', a, b)
    logger.info(f'Similarity ratio: {similarity}')
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
    session.delete(url)


def get_entries(page=0):
    return session.get(f'{TOSHL_URL}/entries',
                       params={
                           'from': '2019-01-01',
                           'to': '2019-10-31',
                           'page': page
                       })


page = 0
entries = []

while True:
    result = get_entries(page)
    entries.extend(result.json())
    if not result.links.get('next'):
        break

    page += 1

comp_list = [(entry['id'], entry['amount'], entry['date']) for entry in entries]
by_id = {entry['id']: entry for entry in entries}

d = defaultdict(list)
for _id, amount, date in comp_list:
    d[(amount, date)].append(_id)

duplicates = [ids for entry, ids in d.items() if len(ids) >= 2]

for ids in duplicates:
    similarity = similar(by_id[ids[0]]['desc'], by_id[ids[1]]['desc'])
    logger.info(f'Amount: {by_id[ids[0]]["amount"]}')

    if similarity < 0.5:
        logger.info('Same amount but similarity score low, skipping')
    elif similarity > 0.7:
        logger.info('High similarity - deleting')
        delete_entry(ids[0])
    else:
        logger.info('Medium similarity score')
        ask_to_delete(_id)

for id, entry in by_id.items():
    if entry['desc'] == 'לאומי ויזה י':
        logger.info(f'Can I delete? {entry["desc"]}, {entry["amount"]}')
        ask_to_delete(entry['id'])
