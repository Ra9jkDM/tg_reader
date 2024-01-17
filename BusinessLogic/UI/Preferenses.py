from BusinessLogic.Language.LanguageController import LanguageController
# json = [
#     {
#         "name": "lang",
#         "type": "text", 
#         "answers": ["ru", "en"]
#     },
#     {
#         "name": "chars_on_page",
#         "type": "num",
#         "min_limit": 1,
#         "max_limit": 4096
#     },
#     {
#         "name": "remove_enters",
#         "type": "bool"
#     }
# ]

class Base:
    lang: LanguageController

    def check(self, command: str):
        return command.startswith(self._command)

    def response(self, command):
        pass

class Buttons(Base):
    _button_postfix = "btn"

    def __init__(self, command, function, answers, update_lang=False, display_value=True):
        self._command = command
        self._function = function
        self._answers = answers

        self._update_lang = update_lang
        self._display_value = display_value

    def get_buttons(self):
        buttons = []

        for i in self._answers:
            tag = f"{self._command}_{i}_{self._button_postfix}"
            tmp = [self.lang.get(tag), tag]
            buttons.append(tmp)

        return buttons

    def response(self, command):
        if command == self._command: # Question
            return self.lang.get(self._command)

        # Action + Answer
        btn_command = self._get_postfix(command)
        index = self._answers.index(btn_command)
        answer = self._answers[index]

        if answer:
            self._function(btn_command)
            self._change_lang(answer)

            choice = ""
            if self._display_value:
                choice = self.lang.get(command)

            return self.lang.get(f"{self._command}_success").format(choice)
        else:
            return self.lang.get(f"{self._command}_error")
         
    def _get_postfix(self, command):
        start = len(f"{self._command}_")
        end = len(command) - len(f"_{self._button_postfix}")
        return command[start:end]
    
    def _change_lang(self, answer):
        if self._update_lang:
            self.lang.set_language(answer.lang)


class Number(Base):
    def __init__(self, command, function, min_limit, max_limit):
        self._command = command
        self.function = function
        self._min_limit = min_limit
        self._max_limit = max_limit

    def response(self, command):
        return self.lang.get(self._command)

    def action(self, number):
        # Action + Answer
        if number.isnumeric() and self._min_limit < int(number) <= self._max_limit:
            self.function(int(number))
            return self.lang.get(f"{self._command}_success").format(number)
        return self.lang.get(f"{self._command}_error")

class Boolean(Buttons):
    def __init__(self, command, function):
        super().__init__(command, function, ['yes', 'no'], display_value=False)

    def get_buttons(self):
        buttons = []

        for i in self._answers:
            tag = f"{self._command}_{i}_{self._button_postfix}"
            tmp = [self.lang.get(i), tag]
            buttons.append(tmp)

        return buttons

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

lang = LanguageController("ru")
mas = [Buttons("lang", lambda x: print("set lang "+x), [Button("ru", lang="ru"),
                        Button("en", lang="en")],
                update_lang=True),
        Buttons("test-color", lambda x: print("set color"+x), [Button("blue"),
                        Button("white"),
                        Button("yellow")]), 
        Number("chars_on_page", lambda x: print(f"set num {x}"), 0, 4096),
        Boolean("remove_enters", lambda x: print(f"set Bool {x}"))]



def init(lang):
    for i in mas:
        i.lang = lang

def handler(command: str):
    for i in mas:
        if i.check(command):
            tmp = i.response(command)
            print(tmp)
            if issubclass(type(i), Buttons):
                btn = i.get_buttons()
                print(f"Buttons: {btn}")
                return tmp, False
            else:
                return tmp, i

    return mas[0].lang.get("not_found"), False

def write(obj, value):
    return obj.action(value)


if __name__ == "__main__":
    lang = LanguageController("ru")

    init(lang)
    # handler("lang")

    handler("lang")
    handler("lang_en_btn")
    handler("lang_ru_btn")


    print(handler("-@-@-"))

    handler("test-color")
    handler("test-color_white_btn")

    text, obj = handler("chars_on_page")
    print(write(obj, "1000"))

    handler("remove_enters")
    handler("remove_enters_no_btn")



# python -m BusinessLogic.UI.Preferenses