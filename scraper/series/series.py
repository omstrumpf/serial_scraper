from abc import ABC, abstractmethod

from scraper.chapter import Chapter


class Series(ABC):
    def __init__(self, state: {}):
        self.state = state

    @abstractmethod
    def scrape(self) -> [Chapter]:
        raise NotImplementedError()
