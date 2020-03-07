import mlflow.pyfunc
import pandas as pd


class ExpensesClassifier(mlflow.pyfunc.PythonModel):

    def __init__(self, model):
        self.model = model

    def _helper(self, row):
        print(row)
        values = {word: True for word in row["desc"].upper().split()}
        return self.model.classify(values)

    def predict(self, context, model_input: pd.DataFrame):
        return model_input.apply(self._helper, axis=1)
