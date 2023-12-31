from Database.session import session

from .Book import Book
from .Page import Page
from .Note import Note
from .Preferences import Preferences

class User:
    def __init__(self, id):
        self._id = id

        self._book = Book(id)
        self._page = Page(id)
        self._note = Note(id)
        self._preferences = Preferences(id)

    @property
    def book(self):
        return self._book


    @property
    def page(self):
        return self._page

    @property
    def note(self):
        return self._note

    @property
    def preferences(self):
        return self._preferences