FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yaml .env ./
RUN conda env create -f environment.yaml

COPY toshl_fixer toshl_fixer

CMD conda run -n toshl-fixer gunicorn --bind :${PORT-8080} --workers 1 --threads 8 toshl_fixer.app:app
