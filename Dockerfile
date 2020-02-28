FROM python:3.8

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock .env ./

RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY toshl_fixer toshl_fixer

CMD gunicorn --bind :${PORT-8080} --workers 1 --threads 8 toshl_fixer.app:app
