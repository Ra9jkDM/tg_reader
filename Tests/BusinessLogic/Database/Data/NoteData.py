from Database.session import session
from Database.model import *

from .main import Data

id = "9000123"
id_second = "opp017"

class NoteData(Data):
    @session
    def _create_data(self, db):
        # create User
        # current_book = global book.id
        user = User(social_id=id, preferences={}, current_book=2)
        user_second = User(social_id=id_second, preferences={}, current_book=3)

        self._save(db, [user, user_second])
        #create Books

        book1 = Book(name="Book 1", number_of_pages=500)
        book2 = Book(name="Book 2", number_of_pages=100)
        book3 = Book(name="Book 3", number_of_pages=100)

        self._save(db, [book1, book2, book3])

        # Associated books with user

        ub1 = UserBook(user_id = user.id, book_id = book1.id)
        ub2 = UserBook(user_id = user.id, book_id = book2.id)
        ub3 = UserBook(user_id = user_second.id, book_id = book3.id)

        self._save(db, [ub1, ub2, ub3])

        
        # Create notes

        note1 = Note(user_id=user.id, book_id=book2.id, page=1, text="Morbi condimentum feugiat luctus")
        note2 = Note(user_id=user.id, book_id=book2.id, page=2, text="Second note")
        note3 = Note(user_id=user.id, book_id=book2.id, page=31, text="3note")
        note4 = Note(user_id=user.id, book_id=book2.id, page=32, text="4-test-note")

        self._save(db, [note1, note2, note3, note4])