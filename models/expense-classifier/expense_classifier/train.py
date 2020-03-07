import atexit
import shutil

import mlflow.pyfunc
import nltk

from .mlflow_helpers import ExpensesClassifier
from .prepare_data_set import get_data_sets
from .settings import ARTIFACT_PATH


def save_model(classifier):
    model_args = {
        'python_model': ExpensesClassifier(classifier),
        'conda_env': 'conda_env.yaml'
    }

    mlflow.pyfunc.save_model(path=ARTIFACT_PATH, **model_args)
    mlflow.pyfunc.log_model(artifact_path=ARTIFACT_PATH, **model_args)


def train_model():
    train_set, test_set = get_data_sets()
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print(f'{accuracy=}')
    mlflow.log_metric("accuracy", accuracy)
    return classifier


def cleanup():
    shutil.rmtree(ARTIFACT_PATH)


def train():
    atexit.register(cleanup)
    with mlflow.start_run():
        classifier = train_model()
        save_model(classifier)


if __name__ == '__main__':
    train()
