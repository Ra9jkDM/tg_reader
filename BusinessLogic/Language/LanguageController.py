import json
import os

PATH = "BusinessLogic/Language/data"

class LanguageController:
    def __init__(self, lang="ru"):
        self.set_language(lang)

    def set_language(self, lang):
        self._lang = lang
        self._load_dict()

    def _load_dict(self):
        with open(f"{PATH}/{self._lang}.json") as file:
            self._data = json.load(file)


    def get(self, key):
        return self._data[key]
    
    def try_to_get(self, key):
        return self._data.get(key)

    def not_found(self):
        return self._data["not_found"]