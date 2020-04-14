import base64
import bs4

from scraper.chapter import Chapter
from scraper.mailer import Mailer
from .series import Series

GMAIL_QUERY = "label:mailing-lists-money-stuff newer_than:14d"


class MoneyStuff(Series):
    def __init__(self, state: {}, mailer: Mailer):
        super().__init__(state)
        self.mailer = mailer

    @staticmethod
    def title() -> str:
        return "Money Stuff"

    @staticmethod
    def author() -> str:
        return "Matt Levine"

    @staticmethod
    def _parse_body_from_message(message) -> str:
        body_data = message["payload"]["parts"][1]["body"]["data"]

        html = base64.urlsafe_b64decode(body_data).decode("utf-8")

        soup = bs4.BeautifulSoup(html, features="lxml")

        results = [str(x) for x in soup.find_all("table")]

        return max(results, key=len)

    def _get_message_ids(self) -> [str]:
        messages = self.mailer.list_matching_query(GMAIL_QUERY)

        return [m["id"] for m in messages]

    def _chapter_from_message_id(self, message_id) -> Chapter:
        message = self.mailer.get_message(message_id)

        title = Mailer.subject_from_message(message)
        timestamp = Mailer.timestamp_from_message(message)
        body = self._parse_body_from_message(message)

        return Chapter(MoneyStuff.title(), MoneyStuff.author(), title, timestamp, body)

    def scrape(self) -> [Chapter]:
        message_ids = self._get_message_ids()

        chapters = [self._chapter_from_message_id(mid) for mid in message_ids]

        if "timestamp" in self.state:
            chapters = filter(lambda x: x.timestamp > self.state["timestamp"], chapters)

        chapters = sorted(chapters)

        if chapters:
            self.state["timestamp"] = chapters[-1].timestamp

        return chapters
