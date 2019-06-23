from functools import total_ordering


@total_ordering
class Chapter:
    def __init__(
        self,
        series: str,
        author: str,
        title: str,
        timestamp: int,
        body: str,
        index: int = None,
    ):
        self.series = series
        self.author = author
        self.title = title
        self.timestamp = timestamp
        self.body = body
        self.index = index

    def __eq__(self, other) -> bool:
        if self.index is not None and other.index is not None:
            return self.index == other.index

        return self.timestamp == other.timestamp

    def __lt__(self, other) -> bool:
        if self.index is not None and other.index is not None:
            return self.index < other.index

        return self.timestamp < other.timestamp
