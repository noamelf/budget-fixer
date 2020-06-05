FROM python:3.8-slim

RUN pip install poetry

ENV APP_HOME /app
ENV APP_DATA $APP_HOME/data
RUN mkdir -p $APP_DATA

WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock .env ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY toshl_fixer toshl_fixer

# To install cli
RUN poetry install

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["serve"]
