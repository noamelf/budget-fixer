import logging
import os
from enum import Enum

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

from .infer import tag_naive_bayes, tag_tfidf_tree
from ..data_access.expenses import get_not_tagged_expenses
from ..toshl.entry import update_entry_async
from ..toshl.labels import LabelMapping

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)


class OPTIONS(Enum):
    mark_tagged = 1
    use_nb = 2
    use_tt = 3
    tag_manually = 4
    skip = 5


def manual_input(expense):
    mapping = LabelMapping.create_from_local_copy()
    tags_completer = FuzzyWordCompleter(mapping.tags)
    category_completer = FuzzyWordCompleter(mapping.categories)
    if category := prompt("Enter category: ", completer=category_completer, search_ignore_case=True):
        if tag := prompt("Enter tag: ", completer=tags_completer, search_ignore_case=True):
            logger.info('Updating manual choice')
            update_entry_async(expense['id'], category=category, tag=tag, desc=expense['desc'] + ' 🏷')
            # update_rt_expense_tags(category, expense, tag)


def choose_option(expense):
    os.system('clear')
    print(expense)
    options = ', '.join(f'{option.value}-{option.name}' for option in OPTIONS)
    response = prompt(f"\nChoose option ({options}): ")

    return OPTIONS(int(response)) if response else OPTIONS.skip


def update_tags_in_toshl(expense):
    choice = choose_option(expense)
    desc = expense['desc'] + ' 🏷'
    if choice is OPTIONS.use_nb:
        logger.info('Using naive-bayes prediction')
        update_entry_async(expense['id'], desc=desc, category=expense['nb_category'], tag=expense['nb_tag'])
    elif choice is OPTIONS.use_tt:
        logger.info('Using tfidf tree prediction')
        update_entry_async(expense['id'], desc=desc, category=expense['tt_category'], tag=expense['tt_tag'])
    elif choice is OPTIONS.tag_manually:
        manual_input(expense)
    elif choice is OPTIONS.mark_tagged:
        logger.info('Marking as tagged')
        update_entry_async(expense['id'], desc=desc)


def update_tags(from_date, to_date):
    expenses = get_not_tagged_expenses(from_date, to_date)
    expenses = tag_naive_bayes(expenses)
    expenses = tag_tfidf_tree(expenses)
    expenses.apply(update_tags_in_toshl, axis=1)
