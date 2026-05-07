import json
import os


class JsonManager:
    def __init__(self, filename):
                self.filename = filename

    def initialize(self):
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)

    def load(self):
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
