from typing import NamedTuple

from Database.session import session
from Database.model import Book as DB_Book, UserBook, User
from .BookUploader import BookUploader

from FileStorage.FileStorageInterface import FileStorageInterface
from FileStorage.FileStorageController import FileStorageController
from FileStorage.MinIO import MinIO

class Book:
    def __init__(self, id, db):
        self._id = id
        self._db = db

        self._book_amount = -1

    def create(self, name, number_of_pages):
        return BookUploader(self._db , self._id, name, number_of_pages)

    def book_amount(self):
        return self._book_amount

    @session
    def page_amount(self, db):
        book = self._get_current_book(db)
        return book.number_of_pages

    @session
    def get_name(self, db):
        book = self._get_current_book(db)
        return book.name

    @session
    def edit_name(self, db, name):
        book = self._get_current_book(db)
        book.name = name

        self._db.commit(db)

    @session
    def get_all(self, db):
        books = self._db.get_all_user_books(db, self._id)
        self._book_amount = len(books)

        book_list = self._convert(books)
        book_list.sort(key = lambda x: x.name)

        return book_list

    @session
    def set(self, db, id):
        books = self.get_all()
        active_book = books[id - 1] # user choice

        user = self._get_user(db)
        user.current_book = active_book.id

        self._db.commit(db)

        return active_book.name

    @session
    def delete(self, db):
        book = self._get_current_book(db)

        minio: FileStorageInterface = MinIO()
        storage = FileStorageController()

        storage.delete_book(minio, book.id)
        self._db.delete(db, book)
        self._db.commit(db)

        try:
            self.set(1)
        except:
            pass

        return book.name

        



    def _get_user(self, db):
        return self._db.get_user(db, self._id)
    
    def _get_current_book(self, db):
        user = self._get_user(db)
        book = self._db.get_book(db, user.current_book)
        return book

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