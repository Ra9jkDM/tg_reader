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

    # @session
    # def _get_user(self, db, id):
    #     return db.query(User).filter(User.social_id == id).first()

    def tearDown(self):
        super().tearDown()
        self.page._storage.delete_bucket()


if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestPage