class Button:
    def __init__(self, name, lang=None, text=None, function=None, command_queue=None, remove_buttons_from_previous_message=True):
        self.name = name
        self.lang = lang
        self.text = text
        self.function = function
        self.command_queue = command_queue
        self.remove_buttons_from_previous_message = remove_buttons_from_previous_message

    def __len__(self):
        return len(self.name)

    def __eq__(self, obj):
        if self.name == obj:
            return True
        else:
            return False

    def __str__(self):
        return self.name