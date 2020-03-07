import mlflow.pyfunc
import pandas as pd

from ..settings import ARTIFACT_PATH

loaded_model = mlflow.pyfunc.load_model(ARTIFACT_PATH)

test_predictions = loaded_model.predict(pd.DataFrame({'desc': 'HOME MADE'}))
print(test_predictions)
