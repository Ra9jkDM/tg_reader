import unittest

from BusinessLogic.Language.LanguageController import LanguageController

TEST_VALUE = "unit-test"

class TestLanguageController(unittest.TestCase):
    def setUp(self):
        self.lang = LanguageController()

    def test_ru_get_test_value(self):
        self.lang.set_language("ru")
        value = self.lang.get(TEST_VALUE)

        self.assertEqual(value, "Модульный тест")

    def test_en_get_test_value(self):
        self.lang.set_language("en")
        value = self.lang.get(TEST_VALUE)

        self.assertEqual(value, "Unit test")

if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Language.TestLanguageController