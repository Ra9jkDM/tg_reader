import unittest

from Tests.Database.Base import Base

from BusinessLogic.UI.TextQA import TextQA
from .Data.TextQAData import TextQAData, id

class TestTextQA(Base):
    def setUp(self):
        super().setUp()
        data = TextQAData()
        data.create()

        self.ui = TextQA(id)

    def test_is_user_exists(self):
        result = self.ui.is_user_exists()
        self.assertTrue(result)

    def test_register_user(self):
        id = "unknown"
        ui = TextQA(id)

        ui.register_user()
        ui.set_language("en")


    def test_set_language(self):
        self.ui.set_language("en")

    def test_welcome(self):
        message = self.ui.welcome()

        self.assertTrue(len(message) > 0)


if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.UI.TestTextQA