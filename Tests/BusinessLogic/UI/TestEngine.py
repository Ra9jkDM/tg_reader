import unittest

from Tests.testEnv import set_test_env
set_test_env()

from BusinessLogic.Language.LanguageController import LanguageController
from BusinessLogic.UI.BaseEngine import BaseEngine
from BusinessLogic.UI.main import commands


NOT_FOUND = "Command not found"
VALUE_UPDATED = "Value updated"
USER = None

class TestEngine(unittest.TestCase):
    def setUp(self):
        
        lang = LanguageController("en")
        self.engine = BaseEngine(commands, lang)

    def test_change_language(self):
        result = self.engine.command(USER, "lang")
        self.engine.button_handlers(USER, "lang_ru_btn")
        result2 = self.engine.command(USER, "lang")
        
        self.assertNotEqual(result["text"], result2["text"])

    def test_get_unknown_command(self):
        result = self.engine.command(USER, "-@-@-")

        self.assertTrue(result["text"].startswith(NOT_FOUND))

    def test_with_different_word_length(self):
        self.engine.command(USER, "remove_enters")
        result = self.engine.button_handlers(USER, "remove_enters_yes_btn")
        result = self.engine.button_handlers(USER, "remove_enters_no_btn")

    def test_create_conversation(self):
        result = self.engine.command(USER, "chars_on_page")
        result = self.engine.action(USER, "200")

        self.assertTrue(result.startswith(VALUE_UPDATED))

    def test_set_bool_value(self):
        self.engine.command(USER, "remove_enters")
        result = self.engine.button_handlers(USER, "remove_enters_no_btn")

        self.assertFalse(result.startswith(NOT_FOUND))

    def test_button_command_not_found(self):
        result = self.engine.command(USER, "remove_enters_no_btn")

        self.assertTrue(result["text"].startswith(NOT_FOUND))

if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.UI.TestEngine