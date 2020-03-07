import pandas as pd
import sys
from sklearn.model_selection import train_test_split


def _format_for_nltk(row):
    return {word: True for word in row["desc"].upper().split()}


def _preprocess_data():
    data_file = sys.argv[1] or '../toshl_fixer/db/expenses.csv'
    expenses = pd.read_csv(data_file)
    expenses = expenses[~expenses['desc'].isna()]
    tagged_expenses = expenses[expenses['desc'].str.contains('🏷')]
    tagged_expenses['label'] = tagged_expenses['category'] + '/' + tagged_expenses['tag']
    tagged_expenses['desc'] = tagged_expenses['desc'].str.strip('🏷')
    tagged_expenses = tagged_expenses[tagged_expenses['amount'] < 0]
    data_set = tagged_expenses[['desc', 'label']]
    data_set = data_set.astype('str')
    data_set = data_set.dropna()
    return data_set


def feature_eng(train, test):
    train_x = train.apply(_format_for_nltk, axis=1)
    test_x = test.apply(_format_for_nltk, axis=1)
    train_y = train["label"]
    test_y = test["label"]
    train_set = list(zip(train_x, train_y))
    test_set = list(zip(test_x, test_y))
    return train_set, test_set


def get_data_sets():
    expenses_set = _preprocess_data()
    train, test = train_test_split(expenses_set, test_size=0.2)
    train_set, test_set = feature_eng(train, test)
    return train_set, test_set
