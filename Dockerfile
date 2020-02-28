FROM python:3.8

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install poetry
RUN poetry install --no-dev

CMD exec poetry run gunicorn --bind :${PORT-8080} --workers 1 --threads 8 toshl_fixer.app:app
