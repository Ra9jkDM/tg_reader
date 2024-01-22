from .BaseCommand import BaseCommand
from .Button import Button
from ..Message import Message

class ButtonsCommand(BaseCommand):
    _button_postfix = "btn"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def button_check(self, command: str):
        return command.startswith(self._command) and len(command) != len(self._command)

    def get_buttons(self, user):
        buttons = self._get_buttons(self._answers, user)
        return buttons

    def _get_buttons(self, answers, user, nesting_level=1):
        if nesting_level > 2:
            raise Exception("Too many nested buttons")

        buttons = []
        for i in answers:
            if isinstance(i, list):
                btn = self._get_buttons(i, user, nesting_level+1)
            else:
                btn = self._create_button(i, user)
            
            buttons.append(btn)
        
        return buttons

    def _create_button(self, answer, user):
        text = ""
        if callable(answer.text):
            text = answer.text(user)

        tag = f"{self._command}_{answer}_{self._button_postfix}"
        button = {"name": self.lang.get(tag).format(text), "id": tag}
        return button


    def question(self, user, command):
        text = ""
        images = None
        if self._content:
            text, images = self._content(user)

        return Message(text=self.lang.get(self._command).format(text), images=images)
    
    def answer(self, user, command):
        btn_command = self._get_command(command)
        index = self._answers.index(btn_command)
        answer = self._answers[index]

        if answer:
            self._function(user, btn_command)
            self._change_lang(answer)
            if isinstance(answer, Button):
                self._button_queue = answer.command_queue

            choice = ""
            if self._display_value:
                choice = self.lang.get(command)

            return Message(text=self._get_answer("success").format(choice))
        else:
            return Message(text=self._get_answer("error"))
         
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