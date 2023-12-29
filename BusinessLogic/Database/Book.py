from typing import NamedTuple

from Database.session import session
from Database.model import Book as DB_Book, UserBook, User
from .BookUploader import BookUploader

class Book:
    def __init__(self, id):
        self._id = id

    def create(self, name, number_of_pages):
        return BookUploader(self._id, name, number_of_pages)

    @session
    def get_all(self, db):
        books = db.query(UserBook).filter(UserBook.user_id == self._id).all()

        book_list = []
        for book in books:
            tmp = BookDTO(**{"id": book.book_id,
                             "name": book.book.name,
                             "bookmark": book.bookmark, 
                             "number_of_pages": book.book.number_of_pages
                             })
            book_list.append(tmp)

        book_list.sort(key = lambda x: x.name)

        return book_list

    @session
    def set(self, db, id):
        books = self.get_all()
        active_book = books[id - 1]

        user = db.query(User).filter(User.id == self._id).first()
        user.current_book = active_book.id

        db.commit()



class BookDTO(NamedTuple):
    id: int
    name: str
    bookmark: int
    number_of_pages: int