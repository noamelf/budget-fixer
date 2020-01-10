# toshl-clean-duplicates [DRAFT]

(Still in draft mode)

Clean (delete) duplicate entries from Toshl budgeting app using their API. 
Toshl doesn't support checking string similarity for duplicates, so this script does it instead.

### Install 

```shell script
poetry install
```

### Run

```shell script
export TOSHL_TOKEN="YOUR-TOKEN"
poetry run python -m toshl_fixer.fetch_data
poetry run python -m toshl_fixer.tag_entries
```