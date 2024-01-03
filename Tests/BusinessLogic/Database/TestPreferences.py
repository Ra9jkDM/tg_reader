import unittest

from Database.session import session
from Database.model import User

from BusinessLogic.Database.main import Database
from BusinessLogic.Database.Book import Book

from Tests.Database.Base import Base

from .Data.PreferencesData import PreferencesData, id



class TestPreferences(Base): 
    def setUp(self):
        super().setUp()   

        self.data = PreferencesData()
        self.data.create()

        db = Database()
        user = db.get_user(id)
        self.preferences = user.preferences

    def test_set_and_get_chars_on_page(self):
        self.preferences.chars_on_page = 350
        num = self.preferences.chars_on_page

        self.assertEqual(num, 350)


if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestPreferences