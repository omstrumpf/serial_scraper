import time
import feedparser

from scraper.chapter import Chapter
from .series import Series

FEED_URL = "https://practicalguidetoevil.wordpress.com/feed/"

AUTHOR = "Erratic Errata"

SERIES_TITLE = "A Practical Guide to Evil"


class PracticalGuide(Series):
    def scrape(self) -> [Chapter]:
        feed = feedparser.parse(FEED_URL)

        chapters = [
            Chapter(
                SERIES_TITLE,
                AUTHOR,
                e.title,
                time.mktime(e.published_parsed),
                e.content[0].value,
            )
            for e in feed.entries
        ]

        if "timestamp" in self.state:
            chapters = filter(lambda x: x.timestamp > self.state["timestamp"], chapters)

        return sorted(chapters)
