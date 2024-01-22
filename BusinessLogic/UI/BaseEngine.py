from BusinessLogic.Language.LanguageController import LanguageController
from .Commands.BaseCommand import BaseCommand
from .Commands.ButtonsCommand import ButtonsCommand
from .Commands.FileCommand import FileCommand
from .Message import Message

from .Actions.Base import get_language

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

                result = i.question(user, command)
                result.buttons, result.is_conversation = self._get_buttons_and_dialogue_type(i, user)
                return result

        return Message(text=self._lang.not_found())

    def button_handlers(self, user, command: str):
        self._set_language(user)

        for i in self._commands:
            if i.button_check(command):
                i.lang = self._lang

                result = i.answer(user, command)
                self._button_queue = i.button_queue
                return result

        return Message(text=self._lang.not_found())

    def action(self, user, value: str) -> str:
        self._set_language(user)

        answer = self._active_command.action(user, value)
        self._active_command = None
        
        return answer

    def upload_book(self, user):
        return FileCommand(user)

    def get_command_queue(self):
        return self._active_command.command_queue
    
    def get_button_queue(self):
        return self._button_queue

    def _get_buttons_and_dialogue_type(self, command: BaseCommand, user):
        conversation = False

        if issubclass(type(command), ButtonsCommand):
            buttons = command.get_buttons(user)
        else:
            buttons = None
            conversation = command.is_conversation

        return buttons, conversation

    def _set_language(self, user):
        lang = get_language(user)
        
        if lang:
            self._lang = LanguageController(lang)
