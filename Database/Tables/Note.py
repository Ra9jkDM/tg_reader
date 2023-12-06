

class Note:
    def __init__(user, book, page, text):
        self._user = user
        self._book = book
        self._page = page
        self._text = text

    @property
    def page(self):
        return self._page

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value): # edit comment
        self._text = text
        #db.'update text'
    

    def delete(self): # delete comment
        self.__del__()
        pass
