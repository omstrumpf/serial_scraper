import time
import feedparser
import bs4
import requests

from typing import List

from scraper.chapter import Chapter
from scraper.series import ScrapeFailedException
from .series import Series

FEED_URL = "https://www.royalroad.com/fiction/syndication/45534"

class ThisUsedToBeAboutDungeons(Series):
    @staticmethod
    def title() -> str:
        return "This Used to be About Dungeons"

    @staticmethod
    def author() -> str:
        return "Alexander Wales"

    @staticmethod
    def __scrape_chapter_body(url):
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise ScrapeFailedException()
        soup = bs4.BeautifulSoup(response.content, features="lxml")

        return str(soup.find("div", "chapter-content"))

    @staticmethod
    def __parse_title(raw_title: str):
        prefix = "This Used to be About Dungeons - "
        if raw_title.startswith(prefix):
            return raw_title[len(prefix):]

        return raw_title

    def scrape(self) -> List[Chapter]:
        feed = feedparser.parse(FEED_URL)

        chapters = [
            Chapter(
                ThisUsedToBeAboutDungeons.title(),
                ThisUsedToBeAboutDungeons.author(),
                ThisUsedToBeAboutDungeons.__parse_title(e.title),
                time.mktime(e.published_parsed),
                ThisUsedToBeAboutDungeons.__scrape_chapter_body(e.link),
            )
            for e in feed.entries
        ]

        if "timestamp" in self.state:
            chapters = filter(lambda x: x.timestamp > self.state["timestamp"], chapters)

        chapters = sorted(chapters)

        if chapters:
            self.state["timestamp"] = chapters[-1].timestamp

        return chapters
