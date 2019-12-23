import logging
import os
from collections import defaultdict
from difflib import SequenceMatcher

import requests
from dotenv import load_dotenv

TOSHL_URL = 'https://api.toshl.com'

logger = logging.getLogger()

load_dotenv()

TOKEN = os.getenv('TOKEN')
session = requests.Session()
session.auth = (TOKEN, '')


def similar(a, b):
    logger.debug('Before split:', a, b, end='\n')
    a, b = a.split('\n')[0], b.split('\n')[0]
    logger.debug('After split:', a, b, end='\n')
    return SequenceMatcher(isjunk=None, a=a.split('\n')[0], b=b.split('\n')[0]).ratio()


result = session.get(f'{TOSHL_URL}/entries',
                     params={
                         'from': '2019-11-01',
                         'to': '2019-11-30'
                     })
entries = result.json()

comp_list = [(entry['id'], entry['amount'], entry['date']) for entry in entries]
by_id = {entry['id']: entry for entry in entries}

d = defaultdict(list)
for _id, amount, date in comp_list:
    d[(amount, date)].append(_id)

duplicates = [ids for entry, ids in d.items() if len(ids) >= 2]

for ids in duplicates:
    logger.debug(ids)
    logger.debug(by_id[ids[0]]['amount'], by_id[ids[0]]['desc'])
    logger.debug(by_id[ids[0]]['amount'], by_id[ids[1]]['desc'])
    logger.debug(similar(by_id[ids[0]]['desc'], by_id[ids[1]]['desc']))

for ids in duplicates:
    url = f'{TOSHL_URL}/entries/{ids[1]}'
    logger.debug(url)
    session.delete(url)
