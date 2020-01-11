import click

from .tag_entries import update_tags
from .toshl.expenses import fetch_expenses


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--from-date",
    required=True,
    help="Date to start tagging from (e.g. 2019-12-01)",
)
@click.option("--to-date", required=True, help="Date to tag to (e.g. 2019-12-30)")
def tag(from_date, to_date):
    update_tags(from_date, to_date)


@click.command()
@click.option(
    "--from-date",
    default='2019-01-01',
    help="Date to fetch date from (e.g. 2019-12-01)",
)
@click.option("--to-date", default='2020-12-31', help="Date to fetch data to (e.g. 2019-12-30)")
def fetch(from_date, to_date):
    fetch_expenses(from_date, to_date)


cli.add_command(tag)
cli.add_command(fetch)

if __name__ == '__main__':
    cli()
