from .ButtonsCommand import ButtonsCommand
from .Button import Button

class BooleanCommand(ButtonsCommand):
    def __init__(self, command, function, *args, **kwargs):
        super().__init__(command, function, ['yes', 'no'], display_value=False, is_conversation=True, *args, **kwargs)
        self._mock_function()

    def get_buttons(self, user):
        buttons = []

        for i in self._answers:
            tag = f"{self._command}_{i}_{self._button_postfix}"
            tmp = {"name": self.lang.get(i), "id": tag}
            buttons.append(tmp)

        return buttons

    def _mock_function(self):
        func = self._function

        def convert_to_bool(user, value):
            value = True if value.lower() == "yes" else False
            func(user, value)

        self._function = convert_to_bool