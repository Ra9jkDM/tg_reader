from .BaseCommand import BaseCommand
from ..Message import Message

class TextCommand(BaseCommand):
    def __init__(self, command, function, *args, **kwargs):
        super().__init__(command, function, [], *args, **kwargs)

    def question(self, user, command) -> str:
        return Message(text=self._function(user))