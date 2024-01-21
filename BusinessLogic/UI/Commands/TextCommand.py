from .BaseCommand import BaseCommand

class TextCommand(BaseCommand):
    def __init__(self, command, function, tag=None):
        super().__init__(command, function, [], tag=tag)

    def question(self, user, command) -> str:
        return self._function(user)