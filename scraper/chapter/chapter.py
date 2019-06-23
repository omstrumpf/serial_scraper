from functools import total_ordering


@total_ordering
class Chapter:
    def __init__(self, series: str, author: str, title: str, timestamp: int, body: str):
        self.series = series
        self.author = author
        self.title = title
        self.timestamp = timestamp
        self.body = body

    def __eq__(self, other) -> bool:
        return self.timestamp == other.timestamp

    def __lt__(self, other) -> bool:
        return self.timestamp < other.timestamp
