import time
import feedparser

from typing import List

from scraper.chapter import Chapter
from .series import Series

FEED_URL = "https://tiraas.net/feed/"


class GodsAreBastards(Series):
    @staticmethod
    def title() -> str:
        return "The Gods are Bastards"

    @staticmethod
    def author() -> str:
        return "D. D. Webb"

    def scrape(self) -> List[Chapter]:
        feed = feedparser.parse(FEED_URL)

        chapters = [
            Chapter(
                GodsAreBastards.title(),
                GodsAreBastards.author(),
                "The Gods are Bastards: " + e.title,
                time.mktime(e.published_parsed),
                e.content[0].value,
            )
            for e in feed.entries
        ]

        # filter out protected chapters
        chapters = filter(lambda x: "protected" not in x.title.lower(), chapters)

        if "timestamp" in self.state:
            chapters = filter(lambda x: x.timestamp > self.state["timestamp"], chapters)

        chapters = sorted(chapters)

        if chapters:
            self.state["timestamp"] = chapters[-1].timestamp

        return chapters
