from os import environ

from BusinessLogic.Language.LanguageController import LanguageController

TEST = environ.get("TEST")

class BaseCommand:
    lang: LanguageController

    def __init__(self, command, function, answers, update_lang=False, display_value=True, is_conversation=False, tag=None):
        self._command = command
        self._answers = answers

        if not TEST:
            self._function = function
        else:
            self._function = lambda user, x: x

        self._is_conversation = is_conversation
        self._update_lang = update_lang
        self._display_value = display_value
        self._tag = tag

    def check(self, command: str):
        return self._command == command

    def button_check(self, command: str):
        return False

    def question(self, user, command) -> str:
        raise Exception("Empty question")
    
    # processes command from buttons
    def answer(self, user, command) -> str:
        pass

    # processes command with value from conversation
    def action(self, user, value) -> str:
        pass

    @property
    def command(self):
        return self._command
        
    def description(self, lang: LanguageController):
        return lang.get(f"{self._command}_description")

    @property
    def is_conversation(self):
        return self._is_conversation

    @property
    def tag(self):
        return self._tag