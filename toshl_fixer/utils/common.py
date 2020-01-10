import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from toshl.client import ToshlClient

logging.basicConfig(level=logging.INFO, format='[%(threadName)s %(pathname)s %(levelname)s]: %(message)s')

load_dotenv()

TOKEN = os.getenv('TOSHL_TOKEN')
client = ToshlClient(TOKEN)
DATA_DIR = Path(os.path.abspath(__file__)).parent.parent / 'data'


def csv_name(from_date, to_date):
    return f"expenses-{from_date}--{to_date}.csv"
