import click


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("SerialScraper Version 1.0")
    ctx.exit()


@click.command()
@click.option("--src-email", required=True, help="Email address to send documents from")
@click.option("--dst-email", required=True, help="Email address to send documents to")
@click.option("--dry-run", is_flag=True, help="Don't send emails")
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print version info and exit.",
)
def scrape(src_email: str, dst_email: str, dry_run: bool):
    pass

if __name__ == "__main__":
    scrape()  # pylint: disable=no-value-for-parameter
