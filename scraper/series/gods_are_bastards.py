import time
import feedparser

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

    def scrape(self) -> [Chapter]:
        feed = feedparser.parse(FEED_URL)

        chapters = [
            Chapter(
                GodsAreBastards.title(),
                GodsAreBastards.author(),
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
