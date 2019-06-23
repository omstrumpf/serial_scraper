import time
import feedparser

from scraper.chapter import Chapter
from .series import Series

FEED_URL = "https://practicalguidetoevil.wordpress.com/feed/"

AUTHOR = "Erratic Errata"

SERIES_TITLE = "A Practical Guide to Evil"


class PracticalGuide(Series):
    def scrape(self) -> [Chapter]:
        if "practical-guide" not in self.state:
            self.state["practical-guide"] = {}

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

        if "timestamp" in self.state["practical-guide"]:
            chapters = filter(
                lambda x: x.timestamp > self.state["practical-guide"]["timestamp"],
                chapters,
            )

        return sorted(chapters)
