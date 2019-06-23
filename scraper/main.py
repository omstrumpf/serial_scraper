import time
import click

from scraper.formatter import Formatter
from scraper.mailer import Mailer
from scraper.series.practical_guide import PracticalGuide
from scraper.state import State


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("SerialScraper Version 1.0")
    ctx.exit()


@click.command()
@click.option("--src-email", required=True, help="Email address to send documents from")
@click.option("--dst-email", required=True, help="Email address to send documents to")
@click.option(
    "--credentials", default="token.pickle", help="File with gmail credentials"
)
@click.option(
    "--state", "state_file", default="state.json", help="File with scraper state"
)
@click.option("--dry-run", is_flag=True, help="Don't send emails")
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print version info and exit.",
)
def scrape(
    src_email: str, dst_email: str, credentials: str, state_file: str, dry_run: bool
):
    state = State.load(state_file)

    series = [PracticalGuide(state)]

    mailer = Mailer(credentials, src_email, dst_email)

    for s in series:
        print(f"Processing series: {s.title()}...", end="")

        chapters = s.scrape()

        if chapters:
            print(f" found {len(chapters)} new chapters!")

        if dry_run:
            continue

        for chapter in chapters:
            print(f"\tSending chapter {chapter.title}                ", end="\r")
            mailer.send(chapter.title, Formatter.format(chapter))

            time.sleep(10)

    State.store(state_file, state)


if __name__ == "__main__":
    scrape()  # pylint: disable=no-value-for-parameter
