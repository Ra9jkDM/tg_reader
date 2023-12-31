import unittest

from Database.session import session
from Database.model import *

from  .Base import Base

class TestDatabase(Base):
    # Book & Pages

    def _create_book(self, db):
        book = Book(name="Над пропастью во ржи", number_of_pages=336)
        db.add(book)
        db.commit()
        
        db.add(Page(book_id=book.id, page_number=1, text="Nulla porttitor facilisis magna."))
        db.add(Page(book_id=book.id, page_number=2, text="In dolor condimentum dignissim", number_of_images=5))
        db.add(Page(book_id=book.id, page_number=3, text="Curabitur nec cursus ipsum."))
        db.commit()

    @session
    def test_create_book_and_3_pages(self, db):
        self._create_book(db)

        number_of_pages = db.query(Page).count()
            
        self.assertEqual(number_of_pages, 3, 
                "Number of pages does not match")

    @session
    def test_delete_book_cascade(self, db):
        self._create_book(db)
            
        book = db.query(Book).all()[0]
        db.delete(book)
        db.commit()

        number_of_pages = db.query(Page).count()

        self.assertEqual(number_of_pages, 0, 
                "Cascading page deletion does not work")

    # # Users & Books

    @session
    def test_create_user(self, db):
        db.add(User(social_id = "123456789", preferences={"lang":"EN", "char": 140}))
        db.add(User(social_id = "9825710237", preferences={"lang":"RU", "char": 1000}))

        db.commit()

        amount = db.query(User).count()
        
        self.assertEqual(amount, 2, 
                "Can not create users")

    @session
    def test_edit_user_json_preferences(self, db):
        KEY = "lang"
        db.add(User(social_id = "123456789", preferences={KEY:"EN", "char": 140}))

        user = db.query(User).first()
        user.preferences[KEY] = "_RUS_"

        db.commit()

        tmp = db.query(User).first()
        self.assertEqual(tmp.preferences[KEY], "_RUS_", 
                "Can not edit JSON value")

    @session
    def test_add_new_key_in_user_json_preferences(self, db):
        KEY = "chars_on_page"
        db.add(User(social_id = "123456789", preferences={}))
        db.commit()
        
        user = db.query(User).first()
        user.preferences[KEY] = 200

        db.commit()

        tmp = db.query(User).first()
        self.assertEqual(tmp.preferences[KEY], 200, 
                "Can not add new key in JSON value")


    def _create_user_with_books(self, db):
        user = User(social_id = "123456789", preferences={"lang":"EN", "char": 140})
        book1 = Book(name="Alpha Crying", number_of_pages=150)
        book2 = Book(name="Zodiac Shadow", number_of_pages=601)
        book3 = Book(name="Crime of the Jilted Porter", number_of_pages=20)
        
        db.add(book1)
        db.add(book2)
        db.add(book3)
        db.add(user)

        db.commit()

        db.add(UserBook(user_id=user.id, book_id=book1.id))
        db.add(UserBook(user_id=user.id, book_id=book2.id))
        db.add(UserBook(user_id=user.id, book_id=book3.id))

        db.commit()

    @session
    def test_create_user_with_books(self, db):
        self._create_user_with_books(db)

        amount = len(db.query(User).first().books)

        self.assertEqual(amount, 3, 
            "I can not add books to a user's reading list")

    @session
    def test_delete_user(self, db):
        self._create_user_with_books(db)

        user = db.query(User).first()
        db.delete(user)

        db.commit()

        user_book_amount = db.query(UserBook).count()
        book_amount = db.query(Book).count()

        self.assertEqual(user_book_amount, 0,
                "Does not delete relationships in table 'UserBook'")
        self.assertEqual(book_amount, 3, 
                "Delete books associated with user")

    # Users & Notes

    def _create_notes(self, db):
        user = db.query(User).first()
        book = db.query(Book).first()

        db.add(Note(user_id=user.id, book_id=book.id, page=50, text="Morbi condimentum feugiat luctus"))
        db.add(Note(user_id=user.id, book_id=book.id, page=51, text="Sed maximus tellus ac augue rutrum, at facilisis felis pretium. "))
        db.add(Note(user_id=user.id, book_id=book.id, page=52, text="Aliquam commodo vestibulum neque eu dictum. "))

        db.commit()

    @session
    def test_create_notes(self, db):
        self._create_user_with_books(db)

        self._create_notes(db)

        amount = db.query(Note).count()

        self.assertEqual(amount, 3,
                "Can not add notes")

    @session
    def test_delete_book(self, db):
        self._create_user_with_books(db)
        self._create_notes(db)

        book = db.query(Book).first()
        db.delete(book)

        notes_amount = db.query(Note).count()
        users_amount = db.query(User).count()
        books_amount = db.query(Book).count()

        self.assertEqual(books_amount, 2, 
                "Do not delete book")
        self.assertEqual(notes_amount, 0, 
                "Can not delete notes associated with book")
        self.assertEqual(users_amount, 1, 
                "Delete user associated with book")

if __name__ == "__main__":
    unittest.main()

# python -m Tests.Database.TestDatabase