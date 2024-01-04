import unittest

from Database.session import session
from Database.model import User

from BusinessLogic.Database.main import Database
from BusinessLogic.Database.Book import Book

from Tests.Database.Base import Base

from .Data.PageData import PageData, id



class TestPage(Base): 
    def setUp(self):
        super().setUp()   

        self.data = PageData()
        self.data.create()

        db = Database()
        self.user = db.get_user(id)
        self.page = self.user.page

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

    def test_get_next_part(self):
        page = self.page.get(33)
        page = self.page.get_next_part()
        self.assertEqual(page.text, '''as parameters.
Thus "call .X.Y 1 2" is, in Go notation, dot.X.Y(1, 2) where
Y is a func-valued field,''')

    def test_get_next_part_2(self):
        page = self.page.get(33)

        page = self.page.get_next_part()
        page = self.page.get_next_part()

        self.assertEqual(page.text, ''' map entry, or the like.
The first argument must be the result of an evaluation
that yields a value of ''')

    def test_get_next_part_on_next_page(self):
        self.user.preferences.chars_on_page = 5
        page = self.page.get(30)

        page = self.page.get_next_part()

        self.assertEqual(page.text, '''spt\nnum ''')

    def test_get_previous_part(self):
        page = self.page.get(33)

        page = self.page.get_next_part()
        page = self.page.get_next_part()

        page = self.page.get_previous_part()

        self.assertEqual(page.text, '''as parameters.\nThus "call .X.Y 1 2" is, in Go notation, dot.X.Y(1, 2) where\nY is a func-valued field,''')

    def test_get_previous_part_2(self):
        page_1 = self.page.get(33)

        page = self.page.get_next_part()
        page = self.page.get_next_part()
 
        page = self.page.get_previous_part()
        page = self.page.get_previous_part()

        self.assertEqual(page.text, page_1.text)

    def test_get_previous_part_on_previous_page(self):
        self.user.preferences.chars_on_page = 10
        page = self.page.get(31)

        self.page._set_chars_from_start(6)
        self.page._set_is_next(False)

        page = self.page.get_previous_part()

        self.assertEqual(page.text, "pAge spt\nnum 31")

    def test_get_previous_part_on_previous_page_2(self):
        self.user.preferences.chars_on_page = 4
        page = self.page.get(31)

        self.page._set_chars_from_start(3)
        self.page._set_is_next(False)

        page = self.page.get_previous_part()
        page = self.page.get_previous_part()

        self.assertEqual(page.text, "pAge ")

    def test_get_previous_part_on_previous_page_2_1(self):
        self.user.preferences.chars_on_page = 5
        page = self.page.get(31)

        self.page._set_chars_from_start(3)
        self.page._set_is_next(False)

        page = self.page.get_previous_part() # change page
        self.assertEqual(page.text, "spt\nnum")

        page = self.page.get_previous_part()
        self.assertEqual(page.text, "pAge ")

        page = self.page.get_previous_part() # change page
        self.assertEqual(page.text, "__eq__\n30 ")

    def test_get_previous_part_on_previous_page_3(self):
        self.user.preferences.chars_on_page = 9
        page = self.page.get(31)

        self.page._set_chars_from_start(3)
        self.page._set_is_next(False)

        page = self.page.get_previous_part()
        page = self.page.get_previous_part()

        self.assertEqual(page.text, "__eq__\n30 ")

    def test_get_previous_then_next_part(self):
        page = self.page.get(33)

        page = self.page.get_next_part()
        page = self.page.get_next_part()

        page = self.page.get_previous_part()
        page = self.page.get_next_part()

        self.assertEqual(page.text, ''' map entry, or the like.
The first argument must be the result of an evaluation
that yields a value of ''')

    def tearDown(self):
        super().tearDown()
        self.page._minio.delete_bucket()


if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestPage