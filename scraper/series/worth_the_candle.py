from datetime import datetime
import bs4
import requests

from scraper.chapter import Chapter
from .series import Series, ScrapeFailedException

BASE_URL = "https://archiveofourown.org"


class WorthTheCandle(Series):
    @staticmethod
    def title() -> str:
        return "Worth the Candle"

    @staticmethod
    def author() -> str:
        return "cthuluraejepsen"

    @staticmethod
    def __scrape_chapter_body(url):
        try:
            response = requests.get(f"{BASE_URL}{url}")
        except requests.exceptions.ConnectionError:
            raise ScrapeFailedException()
        soup = bs4.BeautifulSoup(response.content, features="lxml")

        return str(soup.find("div", "chapter"))

    def __scrape_new(self):
        try:
            response = requests.get(f"{BASE_URL}/works/11478249/navigate")
        except requests.exceptions.ConnectionError:
            raise ScrapeFailedException()
        soup = bs4.BeautifulSoup(response.content, features="lxml")

        entries = soup.find("ol", class_="chapter index group").find_all("li")

        chapters = []

        for entry in entries[len(entries) - 10 :]:
            link = entry.find("a")
            date = entry.find("span")
            index = int(link.text[: link.text.find(".")])

            if index > self.state.get("max_index", 0):
                chapters.append(
                    Chapter(
                        WorthTheCandle.title(),
                        WorthTheCandle.author(),
                        link.text,
                        datetime.timestamp(datetime.strptime(date.text, "(%Y-%m-%d)")),
                        WorthTheCandle.__scrape_chapter_body(link.attrs["href"]),
                        index,
                    )
                )

        return sorted(chapters)

    def scrape(self) -> [Chapter]:
        chapters = self.__scrape_new()

        if chapters:
            self.state["max_index"] = max(
                self.state.get("max_index", 0), *[c.index for c in chapters]
            )

        return chapters
