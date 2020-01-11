import logging
from functools import partial

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter, WordCompleter

from ..classifiers import naive_bayes
from ..classifiers import tfidf_tree
from ..data.expenses import write_real_time_tagged_expense, get_expenses
from ..toshl.labels import LabelMapping
from ..toshl.update import update_toshl

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


def update_rt_expense_tags(category, expense, tag):
    expense['category'] = category
    expense['tag'] = tag
    write_real_time_tagged_expense(expense['id', 'desc', 'amount', 'date', 'category', 'tag'])


def update_tags_in_toshl(expense):
    options = {
        "1": "skip",
        "2": "Use NB",
        "3": "Use TT",
        "4": "Tag manually",
    }
    choice = WordCompleter(options)

    logger.info(expense)

    if expense["nb_probability"] > 0.5:
        logger.info(f"Tagging automatically due to high nb probability")
        update_toshl(expense['id'], category=expense['nb_category'], tag=expense['nb_tag'])
        return

    response = prompt("Choose option: ", completer=choice)
    if response == '1':
        return
    elif response == '2':
        logger.info('Using naive-bayes prediction')
        update_toshl(expense['id'], category=expense['nb_category'], tag=expense['nb_tag'])
    elif response == '3':
        logger.info('Using tfidf tree prediction')
        update_toshl(expense['id'], category=expense['tt_category'], tag=expense['tt_tag'])
    elif response == '4':
        manual_input(expense)


def manual_input(expense):
    mapping = LabelMapping.create_from_local_copy()
    tags_completer = FuzzyWordCompleter(mapping.tags)
    category_completer = FuzzyWordCompleter(mapping.categories)
    if category := prompt("Enter category: ", completer=category_completer, search_ignore_case=True):
        if tag := prompt("Enter tag: ", completer=tags_completer, search_ignore_case=True):
            logger.info('Updating manual choice')
            update_toshl(expense['id'], category=category, tag=tag)
            # update_rt_expense_tags(category, expense, tag)


def update_tags(from_date, to_date):
    expenses = get_expenses(from_date, to_date)
    expenses = tag_naive_bayes(expenses)
    expenses = tag_tfidf_tree(expenses)
    expenses.apply(update_tags_in_toshl, axis=1)
