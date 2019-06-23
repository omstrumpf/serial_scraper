from abc import ABC, abstractmethod, abstractstaticmethod

from scraper.chapter import Chapter


class Series(ABC):
    def __init__(self, state: {}):
        self.state = state

    @abstractstaticmethod
    def title() -> str:
        raise NotImplementedError()

    @abstractstaticmethod
    def author() -> str:
        raise NotImplementedError()

    @abstractmethod
    def scrape(self) -> [Chapter]:
        raise NotImplementedError()
