import mlflow.pyfunc
import pandas as pd

loaded_model = mlflow.pyfunc.load_model(expenses_classifier_path)

test_predictions = loaded_model.predict(pd.DataFrame({'desc': train_x}))
print(test_predictions)