from sqlalchemy.orm import Session
from ..model import Book as DBBook

from .Page import Page
from .Note import Note

class CreateBook:
    def __init__(self, name: str):
        self._name = name
    
    def addPage(self, text: str, number_of_images: int) -> None:
        pass

    def bind(self, user): # Tables.User
        # Добвить запись в таблицу 'UserBook'
        # Связать пользователя с книгой
        pass

    def save(self):
        pass

class Book:
    def __init__(self, book, user):
        self._book = book
        self._user = user

    @property
    def name(self):
        return book.name

    @property
    def numberOfPages(self) -> int:
        return book.number_of_pages

    @property
    def bookmark(self) -> int:
        return db.query(UserBook).filter().bookmark

    @bookmark.setter
    def bookmark(self, page: int) -> None:
        pass # write to db

    def getPage(self, page_number: int):
        return Page()

    def getNotes(self):
        notes = []
        for i in range(10):
            notes.append(Note(self._user, self._book, page, text))
        
        return notes

    def addNote(self, text: str):
        pass