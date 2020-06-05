import click


@click.group(chain=True)
@click.option(
    "--from-date", required=False, help="Date to start from (e.g. 2019-12-01)"
)
@click.option("--to-date", required=False, help="Up to date (e.g. 2019-12-30)")
@click.pass_context
def cli(context, from_date, to_date):
    context.obj = {'from_date': from_date, 'to_date': to_date}


@click.command()
@click.pass_context
def tag(context):
    from .core.manual_tag import update_tags
    update_tags(**context.obj)


@click.command()
def fetch():
    from toshl_fixer.core.fetch import fetch_data
    fetch_data()


@click.command()
@click.pass_context
def delete_dup(context):
    from toshl_fixer.core.delete_duplicates import delete_duplicates
    delete_duplicates(**context.obj)


@click.command()
@click.pass_context
def delete_visa(context):
    from toshl_fixer.core.delete_credit_entries import delete_credit_entries
    delete_credit_entries(**context.obj)


cli.add_command(tag)
cli.add_command(fetch)
cli.add_command(delete_dup)
cli.add_command(delete_visa)

if __name__ == "__main__":
    cli()
