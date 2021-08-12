from abc import ABC, abstractmethod, abstractstaticmethod
from typing import List

from scraper.chapter import Chapter


class ScrapeFailedException(Exception):
    pass


class Series(ABC):
    def __init__(self, state: dict):
        self.state = state

    @abstractstaticmethod
    def title() -> str:
        raise NotImplementedError()

    @abstractstaticmethod
    def author() -> str:
        raise NotImplementedError()

    @abstractmethod
    def scrape(self) -> List[Chapter]:
        raise NotImplementedError()
