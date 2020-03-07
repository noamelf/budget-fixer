import shutil

import mlflow.pyfunc
import nltk

from .settings import MODEL_NAME
from .mlflow_helpers import ExpensesClassifier
from .prepare_data_set import get_data_sets


def save_model(classifier):
    model_args = {
        'path': MODEL_NAME,
        'python_model': ExpensesClassifier(classifier),
        'conda_env': 'conda_env.yaml'
    }

    mlflow.pyfunc.save_model(**model_args)
    mlflow.pyfunc.log_model(**model_args)


def train_model():
    train_set, test_set = get_data_sets()
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print(f'{accuracy=}')
    mlflow.log_metric("accuracy", accuracy)
    return classifier


def cleanup():
    shutil.rmtree('artifacts')
    shutil.rmtree('expenses_classifier')


def train():
    with mlflow.start_run():
        classifier = train_model()
        save_model(classifier)
    cleanup()
