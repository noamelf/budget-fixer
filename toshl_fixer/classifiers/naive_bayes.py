import nltk

from ..utils import expense as expense_utils


class Classifier:
    def __init__(self, from_date="2019-12-01", to_date="2019-12-31"):
        self.classifier = None
        self.from_date = from_date
        self.to_date = to_date

    @staticmethod
    def to_dict(desc):
        return {word: True for word in desc.upper().split()}

    def train_classifier(self):
        training_data = expense_utils.get_expenses(from_date=self.from_date, to_date=self.to_date)
        training_set = [
            (self.to_dict(row["desc"]), (row["category"], row["tag"])) for i, row in training_data.iterrows()
        ]  # Convert the data to NLTK format
        self.classifier = nltk.NaiveBayesClassifier.train(training_set)  # Train the classifier

    def infer(self, desc):
        features = self.to_dict(desc)
        category = self.classifier.classify(features)
        probs = self.classifier.prob_classify(features)
        probability = probs.prob(category)
        return category, probability
