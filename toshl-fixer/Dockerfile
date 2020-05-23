FROM python:3.8-slim

RUN pip install poetry

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock .env ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY toshl_fixer toshl_fixer

# To install cli
RUN poetry install

CMD exec gunicorn --bind :${PORT-8080} --workers 1 --threads 8 toshl_fixer.app:app
