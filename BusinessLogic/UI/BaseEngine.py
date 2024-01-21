from BusinessLogic.Language.LanguageController import LanguageController
from .Commands.BaseCommand import BaseCommand
from .Commands.ButtonsCommand import ButtonsCommand

from .Actions import get_language

class BaseEngine:
    _active_command: BaseCommand

    def __init__(self, commands: list, lang: LanguageController):
        self._commands = commands
        self._lang = lang

    def command(self, user, command: str):
        self._set_language(user)

        for i in self._commands:
            if i.check(command):
                i.lang = self._lang
                self._active_command = i

                text = i.question(user, command)
                buttons, is_conversation = self._get_buttons_and_dialogue_type(i)
                return {"text": text, "buttons": buttons, "is_conversation": is_conversation}

        return {"text": self._lang.not_found(), "buttons": None, "is_conversation": False}

    def button_handlers(self, user, command: str):
        self._set_language(user)

        for i in self._commands:
            if i.button_check(command):
                i.lang = self._lang
                return i.answer(user, command)

        return self._lang.not_found()

    def action(self, user, value: str) -> str:
        self._set_language(user)

        answer = self._active_command.action(user, value)
        self._active_command = None
        
        return answer

    def _get_buttons_and_dialogue_type(self, command: BaseCommand):
        conversation = False

        if issubclass(type(command), ButtonsCommand):
            buttons = command.get_buttons()
        else:
            buttons = None
            conversation = command.is_conversation

        return buttons, conversation

    def _set_language(self, user):
        lang = get_language(user)
        
        if lang:
            self._lang = LanguageController(lang)
