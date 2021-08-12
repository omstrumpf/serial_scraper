import hashlib
import json
import os

from scraper.series import Series

STATE_FILE = "state.json"


class State:
    def __init__(self, state_path: str):
        self.path = state_path

        if os.path.exists(state_path):
            self.state = json.loads(open(state_path, "r").read())
        else:
            self.state = {}

    def persist(self):
        open(self.path, "w").write(json.dumps(self.state))

    def for_series(self, series: Series) -> dict:
        key = hashlib.md5(series.title().encode("utf-8")).hexdigest()

        if key not in self.state:
            self.state[key] = {}

        return self.state[key]
