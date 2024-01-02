from Database.session import session

from Database.DatabaseController import DatabaseController

from .Book import Book
from .Page import Page
from .Note import Note
from .Preferences import Preferences

class User:
    def __init__(self, id, db):
        self._id = id
        self._db = db

        self._book = Book(id, db)
        self._page = Page(id, db)
        self._note = Note(id, db)
        self._preferences = Preferences(id, db)

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