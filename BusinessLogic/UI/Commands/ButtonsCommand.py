from .BaseCommand import BaseCommand

class ButtonsCommand(BaseCommand):
    _button_postfix = "btn"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def button_check(self, command: str):
        return command.startswith(self._command) and len(command) != len(self._command)

    def get_buttons(self):
        buttons = []

        for i in self._answers:
            tag = f"{self._command}_{i}_{self._button_postfix}"
            tmp = [self.lang.get(tag), tag]
            buttons.append(tmp)

        return buttons

    def question(self, user, command):
        return self.lang.get(self._command)
    
    def answer(self, user, command):
        btn_command = self._get_command(command)
        index = self._answers.index(btn_command)
        answer = self._answers[index]

        if answer:
            self._function(user, btn_command)
            self._change_lang(answer)

            choice = ""
            if self._display_value:
                choice = self.lang.get(command)

            return self._get_answer("success").format(choice)
        else:
            return self._get_answer("error")
         
    def _get_command(self, command):
        start = len(f"{self._command}_")
        end = len(command) - len(f"_{self._button_postfix}")
        return command[start:end]
    
    def _change_lang(self, answer):
        if self._update_lang:
            self.lang.set_language(answer.lang)

    def _get_answer(self, postfix: str):
        answer = self.lang.try_to_get(f"{self._command}_{postfix}")

        if not answer:
            answer = self.lang.get(postfix)

        return answer

class Button:
    def __init__(self, name, lang=None):
        self.name = name
        self.lang = lang

    def __len__(self):
        return len(self.name)

    def __eq__(self, obj):
        if self.name == obj:
            return True
        else:
            return False

    def __str__(self):
        return self.name