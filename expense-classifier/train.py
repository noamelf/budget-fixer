import atexit
import shutil

import mlflow.pyfunc
import nltk
import pandas as pd

from prepare_data_set import get_data_sets
from settings import ARTIFACT_PATH


class ExpensesClassifier(mlflow.pyfunc.PythonModel):

    def __init__(self, model):
        self.model = model

    def _helper(self, row):
        print(row)
        values = {word: True for word in row["desc"].upper().split()}
        classification = self.model.classify(values)
        probs = self.model.prob_classify(values)
        probability = probs.prob(classification)
        return pd.Series([classification, probability], index=['label', 'probability'])

    def predict(self, context, model_input: pd.DataFrame):
        return model_input.apply(self._helper, axis=1)


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
