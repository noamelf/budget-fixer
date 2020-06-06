# Expense Classifier

### Run

First see that you run the toshl-fixer and have data there. Then you can run:

```shell script
mlflow run . -P data_file=../toshl-fixer/data/expenses.csv
```

This will train and save a model

### Build docker image

```shell script
mlflow models build-docker  -n gcr.io/toshl-fixer/expence-classifier:latest -m "runs:/$RUN_NUMBER/expense-classifier-artifact"
```

