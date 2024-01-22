from .ButtonsCommand import ButtonsCommand
from ..Message import Message

class PageCommand(ButtonsCommand):
    def answer(self, user, command):
        command = self._get_command(command)
        button = self._find_button(self._answers, command)
        self._button_queue = button.command_queue

        if callable(button.function):
            text, images= button.function(user)
            return Message(text=text, images=images, buttons=self.get_buttons(user), 
                            remove_buttons_from_previous_message=button.remove_buttons_from_previous_message)
        return Message(remove_buttons_from_previous_message=button.remove_buttons_from_previous_message)

    def _find_button(self, buttons, command):
        for i in buttons:
            if isinstance(i, list):
                result = self._find_button(i, command)
                if result:
                    return result
            if i == command:
                return i