import asyncio
from datetime import datetime
import aiohttp
import bs4

from scraper.chapter import Chapter
from .series import Series

BASE_URL = "https://archiveofourown.org"


class WorthTheCandle(Series):
    @staticmethod
    def title() -> str:
        return "Worth the Candle"

    @staticmethod
    def author() -> str:
        return "cthuluraejepsen"

    @staticmethod
    async def __scrape_chapter_body(session, url):
        async with session.get(f"{BASE_URL}{url}") as resp:
            body = await resp.text()
            soup = bs4.BeautifulSoup(body, features="lxml")

            return str(soup.find("div", "chapter"))

    async def __scrape_new(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}/works/11478249/navigate", timeout=60
            ) as resp:
                soup = bs4.BeautifulSoup(await resp.text(), features="lxml")

                entries = soup.find("ol", class_="chapter index group").find_all("li")

                empty_chapters = []

                for entry in entries:
                    link = entry.find("a")
                    date = entry.find("span")
                    index = int(link.text[: link.text.find(".")])

                    if index > self.state.get("max_index", 0):
                        empty_chapters.append(
                            (
                                Chapter(
                                    WorthTheCandle.title(),
                                    WorthTheCandle.author(),
                                    link.text,
                                    datetime.timestamp(
                                        datetime.strptime(date.text, "(%Y-%m-%d)")
                                    ),
                                    None,
                                    index,
                                ),
                                link.attrs["href"],
                            )
                        )

            chapter_bodies = asyncio.gather(
                *(
                    WorthTheCandle.__scrape_chapter_body(session, url)
                    for (chapter, url) in empty_chapters
                )
            )

            chapters = [chapter for (chapter, url) in empty_chapters]

            for i, body in enumerate(await chapter_bodies):
                chapters[i].body = body

        return sorted(chapters)

    def scrape(self) -> [Chapter]:
        chapters = asyncio.run(self.__scrape_new())

        if chapters:
            self.state["max_index"] = max(
                self.state.get("max_index", 0), *[c.index for c in chapters]
            )

        return chapters
