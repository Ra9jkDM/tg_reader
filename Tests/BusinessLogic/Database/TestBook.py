import unittest

from Database.session import session
from Database.model import User

from BusinessLogic.Database.main import Database
from BusinessLogic.Database.Book import Book

from Tests.Database.Base import Base

from .Data.BookData import BookData, id

class TestBook(Base): 
    def setUp(self):
        super().setUp()   

        self.data = BookData()
        self.data.create()

        db = Database()
        user = db.get_user(id)
        self.book = user.book

    def test_get_all_books(self):
        books = self.book.get_all()

        self.assertEqual(len(books), 3, "Can not find books")

    def test_set_active_book(self):
        self.book.set(2)

        user = self._get_user(id)

        self.assertEqual(user.current_book, 3, "Set wrong 'current' book")

    @session
    def _get_user(self, db, id):
        return db.query(User).filter(User.social_id == id).first()


if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestBook