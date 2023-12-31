import unittest

from Database.session import session
from Database.model import User

from BusinessLogic.Database.main import Database
from BusinessLogic.Database.Book import Book

from Tests.Database.Base import Base

from .Data import Data, id_1, id_2, id_3



class TestPage(Base): 
    def setUp(self):
        super().setUp()   

        self.data = Data()
        self.data.create()

        db = Database()
        user = db.get_user(id_1)
        self.page = user.page

    def test_get_page_by_page_number_without_images(self):
        page = self.page.get(1)

        self.assertEqual(page.text, "In dolor condimentum dignissim")

    def test_get_page_by_page_number_with_images(self):
        page = self.page.get(2)
        
        self.assertEqual(len(page.images), 3)

    def test_save_bookmark(self):
        page = self.page.get(30)

        bookmark = self.page.get_bookmark()

        self.assertEqual(bookmark, 30)

    def test_get_current(self):
        page = self.page.get(31)

        page = self.page.get_current()

        self.assertEqual(page.text, "31 page")

    def test_get_next(self):
        page = self.page.get(31)

        page = self.page.get_next()

        self.assertEqual(page.text, "32 page")

    def test_get_previous(self):
        page = self.page.get(31)

        page = self.page.get_previous()

        self.assertEqual(page.text, "30 page")

    def test_get_part_of_page(self):
        page = self.page.get_part_of_page(33)
        self.assertEqual(page.text, '''Returns the result of calling the first argument, which
	must be a function, with the remaining arguments as parameters.''')

    def test_get_next_part_of_page(self):
        self.page._set_chars_from_start(235)

        page = self.page.get_part_of_page(33)
        self.assertEqual(page.text, '''The first argument must be the result of an evaluation
	that yields a value of function type (as distinct from
	a predefined function such as print).''')

    def test_get_part_of_two_pages(self):
        self.page._set_chars_from_start(540)

        page = self.page.get_part_of_page(33)
        self.assertEqual(page.text, '''d error value is non-nil, execution stops. When SQLAlchemy issues a single INSERT statement, to fulfill the contract of having the “last insert identifier” available, a RETURNING clause is added to the INSERT statement which specifies the primary key columns should be returned after the statement completes.''')


    def tearDown(self):
        super().tearDown()
        self.page._storage.delete_bucket()


if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestPage