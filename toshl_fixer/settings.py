import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from toshl.client import ToshlClient

logging.basicConfig(level=logging.INFO, format='[%(pathname)s %(levelname)s]: %(message)s')

load_dotenv()

MANUALLY_TAGGED_FROM_DATE = os.getenv('MANUALLY_TAGGED_FROM_DATE')
MANUALLY_TAGGED_TO_DATE = os.getenv('MANUALLY_TAGGED_TO_DATE')
DATA_DIR = Path(os.path.abspath(__file__)).parent / 'db'
DATA_DIR.mkdir(exist_ok=True)

TOKEN = os.getenv('TOSHL_TOKEN')
client = ToshlClient(TOKEN)

EXPENSE_CLASSIFIER_URL = os.getenv('EXPENSE_CLASSIFIER_URL')
