import logging
from functools import partial

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

from toshl_fixer.utils.expense import Mapping
from .classifiers import tfidf_tree
from .classifiers import naive_bayes
from .utils import expense as expense_utils

logger = logging.getLogger(__name__)


def infer_nb(classifier, expense):
    category, probability = classifier.infer(expense["desc"])
    expense["nb_probability"] = probability
    expense["nb_category"] = category[0]
    expense["nb_tag"] = category[1]
    return expense


def tag_naive_bayes(expenses):
    classifier = naive_bayes.Classifier()
    classifier.train_classifier()
    expenses = expenses.apply(partial(infer_nb, classifier), axis=1)
    return expenses


def infer_tt(classifier: tfidf_tree.Classifier, expense):
    category, tag = classifier.infer(expense["id"])
    expense["tt_category"] = category
    expense["tt_tag"] = tag
    return expense


def tag_tfidf_tree(expenses):
    classifier = tfidf_tree.Classifier()
    classifier.train_classifier()
    expenses = expenses.apply(partial(infer_tt, classifier), axis=1)
    return expenses


def update_if_high_prediction(expense):
    mapping = Mapping()
    tags_completer = FuzzyWordCompleter(mapping.tags)
    category_completer = FuzzyWordCompleter(mapping.categories)

    logger.info(expense)
    if expense["nb_probability"] > 0.5:
        logger.info(f"Tagging automatically due to high nb probability")
        send_to_toshl(expense['id'], expense['nb_category'], expense['nb_tag'])
    elif expense["nb_probability"] > 0.3 and expense["nb_category"] == expense["tt_category"]:
        logger.info(f"NB and TT category are the same")
        response = input("Do you want me to auto tag it? [y/n]")
        if response == 'y':
            send_to_toshl(expense['id'], expense['tt_category'], expense['tt_tag'])
    else:
        if category := prompt("Enter category: ", completer=category_completer, search_ignore_case=True):
            if tag := prompt("Enter tag: ", completer=tags_completer, search_ignore_case=True):
                send_to_toshl(expense['id'], category, tag)


def send_to_toshl(entry_id, category, tag):
    expense_utils.update_toshl(entry_id, category=category, tag=tag)


def update_tags(from_date=None, to_date=None):
    expenses = expense_utils.get_expenses(from_date, to_date)
    expenses = tag_naive_bayes(expenses)
    expenses = tag_tfidf_tree(expenses)
    expenses.apply(update_if_high_prediction, axis=1)


if __name__ == "__main__":
    update_tags(from_date="2019-10-01", to_date="2019-10-31")
