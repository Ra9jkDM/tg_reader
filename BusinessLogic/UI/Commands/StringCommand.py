from .BaseCommand import BaseCommand


class StringCommand(BaseCommand):
    def __init__(self, command, function, char_limit, old_value=None, tag=None, format_result=False):
        super().__init__(command, function, None, is_conversation=True, tag=tag)

        self._char_limit = char_limit
        self._old_value = old_value
        self._format_result = format_result

    def question(self, user, command):
        if callable(self._old_value):
            value = self._old_value(user)
        else:
            value = self._old_value

        text = self.lang.get(self._command)

        if self._format_result:
            text = text.format(value)
        else:
            text = text + "\n" + value
        return text

    def action(self, user, text):
        if len(text) <= self._char_limit:
            self._function(user, text)
            return self.lang.get(f"{self._command}_success")
        return self.lang.get(f"{self._command}_error")
