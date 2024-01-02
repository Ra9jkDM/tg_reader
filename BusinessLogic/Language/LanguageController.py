import json

# ToDo: Test
class LanguageController:
    _lang = "ru"

    def set_language(self, lang):
        self._lang = lang
        self._load_dict()

    def _load_dict(self):
        with open(f"data/{self._lang}") as file:
            self._data = json.load(file)


    def get(self, key):
        return self._data[key]