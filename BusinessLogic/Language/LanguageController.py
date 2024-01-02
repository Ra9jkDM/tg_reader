import json
import os

PATH = "BusinessLogic/Language/data"

class LanguageController:
    _lang = "ru"

    def set_language(self, lang):
        self._lang = lang
        self._load_dict()

    def _load_dict(self):
        with open(f"{PATH}/{self._lang}.json") as file:
            self._data = json.load(file)


    def get(self, key):
        return self._data[key]