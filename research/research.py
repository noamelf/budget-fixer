# %%
import nltk
import pandas as pd
from sklearn.model_selection import train_test_split
from toshl_fixer.data.expenses import get_expenses
import mlflow

# %%

expenses = get_expenses()

# %%
expenses['label'] = expenses['category'] + '/' + expenses['tag']
expenses['desc'] = expenses['desc'].str.strip('🏷')
expenses = expenses[expenses['amount'] < 0]

data_set = expenses[['desc', 'label']]

# %%
train, test = train_test_split(data_set, test_size=0.2)


# %%

def format_for_nltk(row):
    return {word: True for word in row["desc"].upper().split()}


train_x = train.apply(format_for_nltk, axis=1)
test_x = test.apply(format_for_nltk, axis=1)
train_y = train["label"]
test_y = test["label"]

# %%
train_set = list(zip(train_x, train_y))
test_set = list(zip(test_x, test_y))

# %%
with mlflow.start_run():
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)

    print(f'{accuracy=}')
    mlflow.log_metric("accuracy", accuracy)

    train.to_csv('train-set.csv', index=False)
    mlflow.log_artifact('train-set.csv')

    test.to_csv('test-set.csv', index=False)
    mlflow.log_artifact('test-set.csv')


