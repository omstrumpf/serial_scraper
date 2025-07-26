import sys
import click


from scraper.formatter import Formatter
from scraper.mailer import Mailer
from scraper.series import ScrapeFailedException
from scraper.series.bits_about_money import BitsAboutMoney
from scraper.series.money_stuff import MoneyStuff
from scraper.series.this_used_to_be_about_dungeons import ThisUsedToBeAboutDungeons
from scraper.series.pale_lights import PaleLights
from scraper.series.years_of_apocalypse import YearsOfApocalypse
from scraper.state import State


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("SerialScraper Version 1.1")
    ctx.exit()


@click.command()
@click.option(
    "--src-email",
    default="omstrumpf.auto@gmail.com",
    help="Email address to send documents from",
)
@click.option("--dst-email", help="Email address to send documents to")
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
    state = State(state_file)

    mailer = Mailer(credentials, src_email, dst_email)

    series = [
        # PracticalGuide(state.for_series(PracticalGuide)),
        # GodsAreBastards(state.for_series(GodsAreBastards)),
        # WorthTheCandle(state.for_series(WorthTheCandle)),
        # ThisUsedToBeAboutDungeons(state.for_series(ThisUsedToBeAboutDungeons)),
        MoneyStuff(state.for_series(MoneyStuff), mailer),
        BitsAboutMoney(state.for_series(BitsAboutMoney), mailer),
        # PaleLights(state.for_series(PaleLights)),
        YearsOfApocalypse(state.for_series(YearsOfApocalypse)),
    ]

    for s in series:
        print(f"Processing series: {s.title()}...", end="")
        sys.stdout.flush()

        try:
            chapters = s.scrape()
        except ScrapeFailedException:
            print(" scrape failed.")
            continue

        if chapters:
            print(f" found {len(chapters)} new chapters!")
        else:
            print(" up to date.")

        if dry_run:
            continue

        for chapter in chapters:
            print(f"\tSending chapter {chapter.title}                ", end="\r")
            sys.stdout.flush()
            mailer.send(chapter.title, Formatter.format(chapter))

    state.persist()


if __name__ == "__main__":
    scrape()  # pylint: disable=no-value-for-parameter
