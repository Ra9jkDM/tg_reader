from .BaseCommand import BaseCommand

class NumberCommand(BaseCommand):
    def __init__(self, command, function, min_limit, max_limit, tag=None, question=None, format_result=False):
        super().__init__(command, function, None, is_conversation=True, tag=tag)
        self._min_limit = min_limit
        self._max_limit = max_limit
        self._question = question
        self._format = format_result

    def question(self, user, command):
        text = self.lang.get(self._command)
        if callable(self._question):
            if self._format:
                text = text.format(str(self._question(user)))
            else:
                text +="\n"+self._question(user)
        return text

    def action(self, user, number):
        if callable(self._max_limit):
            max_limit = self._max_limit(user)
        else:
            max_limit = self._max_limit

        if number.isnumeric() and self._min_limit < int(number) <= max_limit:
            self._function(user, int(number))
            return self.lang.get(f"{self._command}_success").format(number)
        return self.lang.get(f"{self._command}_error")