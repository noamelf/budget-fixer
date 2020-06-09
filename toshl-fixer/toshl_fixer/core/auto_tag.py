import logging

import pandas as pd

from toshl_fixer.classifiers.remote_classification import predict
from toshl_fixer.core.fetch import fetch_data
from toshl_fixer.toshl.entry import update_entry_async

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _update_entries(expense):
    logger.info(f'Tagging: {expense}')
    category, tag = expense['label'].split('/')
    update_entry_async(expense['id'], category=category, tag=tag, desc=expense['desc'] + ' 🤖')


def auto_tag():
    expenses: pd.DataFrame = fetch_data()
    untagged_expenses = expenses[~expenses.desc.str.contains('🏷|🤖')].reset_index()
    predictions = predict(untagged_expenses)
    high_accuracy = predictions[predictions['probability'] > 0.7]
    logger.debug(f'{high_accuracy=}')
    labeled_expenses = untagged_expenses.merge(high_accuracy, left_index=True, right_index=True)
    labeled_expenses.apply(_update_entries, axis=1)


if __name__ == '__main__':
    auto_tag()
