from typing import NamedTuple

from Database.session import session
from Database.model import Book as DB_Book, UserBook, User
from .BookUploader import BookUploader

class Book:
    def __init__(self, id, db):
        self._id = id
        self._db = db

    def create(self, name, number_of_pages):
        return BookUploader(self._db , self._id, name, number_of_pages)

    @session
    def get_all(self, db):
        books = self._db.get_all_user_books(db, self._id)

        book_list = self._convert(books)
        book_list.sort(key = lambda x: x.name)

        return book_list

    @session
    def set(self, db, id):
        books = self.get_all()
        active_book = books[id - 1] # user choice

        user = self._db.get_user(db, self._id)
        user.current_book = active_book.id

        self._db.commit(db)

    def _convert(self, books):
        book_list = []

        for book in books:
            tmp = BookDTO(**{"id": book.book_id,
                             "name": book.book.name,
                             "bookmark": book.bookmark, 
                             "number_of_pages": book.book.number_of_pages
                             })
            book_list.append(tmp)

        return book_list



class BookDTO(NamedTuple):
    id: int
    name: str
    bookmark: int
    number_of_pages: int