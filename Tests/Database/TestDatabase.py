import unittest

from sqlalchemy.orm import Session
from Database.model import *

from functools import wraps

def session(func):
    @wraps(func)
    def test_create(self, *args, **kwargs):
        with Session(autoflush=True, bind=self.ENGINE) as db:
            func(self, db)
    
    return test_create


    

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.ENGINE = get_engine("_test")
        # print(f"Database: {self.ENGINE}")
        create_db(self.ENGINE)

    def _create_book(self, db):
        book = Book(name="Над пропастью во ржи", number_of_pages=336)
        db.add(book)
        db.commit()
        
        db.add(Page(book_id=book.id, page_number=1, text="Nulla porttitor facilisis magna."))
        db.add(Page(book_id=book.id, page_number=2, text="In dolor condimentum dignissim", number_of_images=5))
        db.add(Page(book_id=book.id, page_number=3, text="Curabitur nec cursus ipsum."))
        db.commit()

    @session
    def test_create_book_and_X_pages(self, db):
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

    def tearDown(self):
        delete_db(self.ENGINE)
        pass

if __name__ == "__main__":
    unittest.main()
# python -m Tests.Database.TestDatabase