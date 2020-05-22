# toshl-clean-duplicates [DRAFT]

(Still in draft mode)

Clean (delete) duplicate entries from Toshl budgeting app using their API. 
Toshl doesn't support checking string similarity for duplicates, so this script does it instead.

### Install 

```shell script
conda create env -f environment.yaml
```

### Run

```shell script
conda activate toshl-fixer
python -m toshl_fixer.fetch
python -m toshl_fixer.tag_entries
```

### TODO

-[ ] Finish tagging nov
-[ ] Train november
-[ ] Tag october
-[ ] Remove duplicate entries
-[ ] Remove false entry - visa