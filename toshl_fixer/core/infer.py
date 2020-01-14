from functools import partial

from toshl_fixer.classifiers import naive_bayes, tfidf_tree


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