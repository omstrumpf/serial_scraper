import time
import feedparser

from typing import List

from scraper.chapter import Chapter
from .series import Series

FEED_URL = "https://palelights.com/feed/"


class PaleLights(Series):
    @staticmethod
    def title() -> str:
        return "Pale Lights"

    @staticmethod
    def author() -> str:
        return "Erratic Errata"

    def scrape(self) -> List[Chapter]:
        feed = feedparser.parse(FEED_URL)

        chapters = [
            Chapter(
                PaleLights.title(),
                PaleLights.author(),
                f"Pale Lights: {e.title}",
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
