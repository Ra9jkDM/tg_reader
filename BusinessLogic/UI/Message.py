class Message:
    def __init__(self, text=None, buttons=None, images=None, is_conversation=False, 
                    remove_buttons_from_previous_message=True):
        self.text = text
        self.buttons = buttons
        self.images = images
        self.is_conversation = is_conversation
        self.remove_buttons_from_previous_message = remove_buttons_from_previous_message

    def is_displayable(self):
        return self.text != None

    def has_images(self):
        return self.images != None and len(self.images) > 0

    def has_buttons(self):
        return self.buttons != None 