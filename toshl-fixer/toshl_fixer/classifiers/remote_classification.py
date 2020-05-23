import pandas as pd
import requests as r

from ..settings import EXPENSE_CLASSIFIER_URL


def predict(expenses: pd.DataFrame):
    expenses: pd.DataFrame = expenses[['desc']]
    formatted_data = expenses.to_dict(orient='split')
    result = r.post(EXPENSE_CLASSIFIER_URL, json=formatted_data)
    result.raise_for_status()
    result_set = pd.DataFrame(result.json())
    return result_set
