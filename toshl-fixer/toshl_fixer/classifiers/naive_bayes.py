import nltk

from ..data_access import expenses


class Classifier:
    def __init__(self, ):
        self.classifier = None

    @staticmethod
    def to_dict(desc):
        return {word: True for word in desc.upper().split()}

    def train_classifier(self):
        training_data = expenses.get_tagged_training_expenses()
        training_set = [
            (self.to_dict(row["desc"]), (row["category"], row["tag"])) for i, row in training_data.iterrows()
        ]
        self.classifier = nltk.NaiveBayesClassifier.train(training_set)

    def infer(self, desc):
        features = self.to_dict(desc)
        category = self.classifier.classify(features)
        probs = self.classifier.prob_classify(features)
        probability = probs.prob(category)
        return category, probability
