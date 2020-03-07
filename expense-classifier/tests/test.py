import cloudpickle

with open(
        '/models/mlruns/0/6443ec3f3fbf4e7eb5098636d6fb019d/artifacts/expense-classifier-artifact/python_model.pkl',
        'rb') as f:
    p = cloudpickle.load(f)

print(p)
eval(p)
