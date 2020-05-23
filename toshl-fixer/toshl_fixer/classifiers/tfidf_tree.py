import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

from ..data.expenses import get_training_expenses
from ..settings import MANUALLY_TAGGED_FROM_DATE, MANUALLY_TAGGED_TO_DATE


class Classifier:
    def __init__(self,):
        self.classifier = None
        self._vector = None

    def vectorize_desc(self, data):
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(data)
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        denselist = dense.tolist()
        return pd.DataFrame(denselist, columns=feature_names)

    def create_vector(self, data):
        df = self.vectorize_desc(data["desc"])
        df["amount"] = data["amount"]
        df["id"] = data["id"]
        return df

    def train_classifier(self, from_date=MANUALLY_TAGGED_FROM_DATE, to_date=MANUALLY_TAGGED_TO_DATE):
        expenses = get_training_expenses()
        vector = self.create_vector(expenses)
        self._vector = vector

        training_expenses = expenses[
            (expenses.date > from_date) & (expenses.date < to_date)
        ]
        training_vec = vector[vector.index.isin(training_expenses.index)]

        del training_vec["id"]

        X = training_vec
        Y = training_expenses[['category', 'tag']]
        clf = DecisionTreeClassifier().fit(X, Y)
        self.classifier = clf

    def infer(self, expense_id):
        expense_vec = self._vector.loc[self._vector['id'] == expense_id].iloc[0]
        del expense_vec['id']
        return self.classifier.predict((expense_vec.values.reshape(1, -1)))[0]
