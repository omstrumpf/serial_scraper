import time
import feedparser

from typing import List

from scraper.chapter import Chapter
from .series import Series

FEED_URL = "https://practicalguidetoevil.wordpress.com/feed/"


class PracticalGuide(Series):
    @staticmethod
    def title() -> str:
        return "A Practical Guide to Evil"

    @staticmethod
    def author() -> str:
        return "Erratic Errata"

    def scrape(self) -> List[Chapter]:
        feed = feedparser.parse(FEED_URL)

        chapters = [
            Chapter(
                PracticalGuide.title(),
                PracticalGuide.author(),
                e.title,
                time.mktime(e.published_parsed),
                e.content[0].value,
            )
            for e in feed.entries
        ]

        if "timestamp" in self.state:
            chapters = filter(lambda x: x.timestamp > self.state["timestamp"], chapters)

        chapters = sorted(chapters)

        if chapters:
            self.state["timestamp"] = chapters[-1].timestamp

        return chapters
