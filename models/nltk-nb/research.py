# %%
import os
import shutil

import mlflow.pyfunc
import nltk
import pandas as pd
import sys
from sklearn.model_selection import train_test_split

data_file = sys.argv[1] or '../toshl_fixer/db/expenses.csv'
expenses = pd.read_csv(data_file)

expenses['label'] = expenses['category'] + '/' + expenses['tag']
expenses['desc'] = expenses['desc'].str.strip('🏷')
expenses = expenses[expenses['amount'] < 0]

data_set = expenses[['desc', 'label']]
data_set = data_set.astype('str')
data_set = data_set.dropna()

train, test = train_test_split(data_set, test_size=0.2)


def format_for_nltk(row):
    return {word: True for word in row["desc"].upper().split()}


train_x = train.apply(format_for_nltk, axis=1)
test_x = test.apply(format_for_nltk, axis=1)
train_y = train["label"]
test_y = test["label"]

# %%
train_set = list(zip(train_x, train_y))
test_set = list(zip(test_x, test_y))


class ExpensesClassifier(mlflow.pyfunc.PythonModel):

    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input):
        return model_input.apply(classifier.classify)


os.mkdir('artifacts')

with mlflow.start_run():
    train.to_csv('artifacts/train-set.csv', index=False)
    test.to_csv('artifacts/test-set.csv', index=False)
    mlflow.log_artifact('artifacts/train-set.csv')
    mlflow.log_artifact('artifacts/test-set.csv')

    classifier = nltk.NaiveBayesClassifier.train(train_set)

    accuracy = nltk.classify.accuracy(classifier, test_set)
    print(f'{accuracy=}')
    mlflow.log_metric("accuracy", accuracy)

    # breakpoint()

    expenses_classifier_path = "expenses_classifier"
    expenses_classifier_model = ExpensesClassifier(classifier)
    mlflow.pyfunc.save_model(path=expenses_classifier_path, python_model=expenses_classifier_model,
                             conda_env='conda_env.yaml')
    mlflow.pyfunc.log_model(artifact_path=expenses_classifier_path, python_model=expenses_classifier_model,
                            conda_env='conda_env.yaml')

shutil.rmtree('artifacts')
shutil.rmtree('expenses_classifier')
