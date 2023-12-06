import unittest

from Database.session import session
from Database.Tables.User import User as TableUser
from Database.model import *

from ..Base import Base

id_1 = "99888"
id_2 = "222322"

class Data:
    def create(self):
        try:
            self._create_data()
        except:
            pass

    @session
    def _create_data(self, db):
        # create Users
        user1 = User(social_id=id_1, preferences={}, current_book=2)
        user2 = User(social_id=id_2, preferences={})

        self._save(db, [user1, user2])
        #create Books

        book1 = Book(name="Book 1", number_of_pages=500)
        book2 = Book(name="Book 2", number_of_pages=100)
        book3 = Book(name="Book 3", number_of_pages=40)

        self._save(db, [book1, book2, book3])
        # Associated books with users

        ub1 = UserBook(user_id = user1.id, book_id = book1.id)
        ub2 = UserBook(user_id = user1.id, book_id = book2.id)

        ub3 = UserBook(user_id = user2.id, book_id = book1.id)
        ub4 = UserBook(user_id = user2.id, book_id = book2.id)
        ub5 = UserBook(user_id = user2.id, book_id = book3.id)

        self._save(db, [ub1, ub2, ub3, ub4, ub5])

    def _save(self, db, obj: list):
        for i in obj:
            db.add(i)
        db.commit()

class TestUser(Base): 
    def setUp(self):
        super().setUp()   
        
        self.data = Data()
        self.data.create()

    def test_get_old_user(self):
        tmp = TableUser(id_1)
        self.assertFalse(tmp.isNewUser(), "Can not find user")

    def test_get_new_user(self):
        tmp = TableUser("ywqegqo")
        self.assertTrue(tmp.isNewUser(), "User already in db, but it is new user")

    def test_get_books(self):
        tmp = TableUser(id_1)

        books = tmp.getBooks()

        self.assertEqual(len(books), 2, "User have not got book, associated with him")

    def test_register_new_user(self):
        user = TableUser("awesome")
        user.registerNewUser()

        self.assertFalse(user.isNewUser(), "Can not create new user")
        

if __name__ == "__main__":
    unittest.main()

# python -m Tests.Database.Tables.TestUser