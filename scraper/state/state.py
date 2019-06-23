import json
import os

STATE_FILE = "state.json"

class State:
    @staticmethod
    def load(state_path: str) -> {}:
        if os.path.exists(state_path):
            return json.loads(open(state_path, "r").read())

        return {}

    @staticmethod
    def store(state_path: str, state: {}):
        open(state_path, "w").write(json.dumps(state))
