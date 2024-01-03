from Database.session import session
from Database.model import *

from .main import Data

id = "9000123"

class BookData(Data):
    @session
    def _create_data(self, db):
        # create User
        user = User(social_id=id, preferences={}, current_book=4)

        self._save(db, [user])
        #create Books

        book1 = Book(name="Book 1", number_of_pages=500)
        book2 = Book(name="Book 2", number_of_pages=100)
        book3 = Book(name="Book 3", number_of_pages=40)
        book4 = Book(name="Book 4", number_of_pages=55)

        self._save(db, [book1, book2, book3, book4])

        # Associated books with user

        ub4 = UserBook(user_id = user.id, book_id = book2.id)
        ub5 = UserBook(user_id = user.id, book_id = book3.id)
        ub6 = UserBook(user_id = user.id, book_id = book4.id)

        self._save(db, [ub4, ub5, ub6])