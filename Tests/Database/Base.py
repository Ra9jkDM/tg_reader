import unittest

from Tests.testEnv import set_test_env

from Database.session import _get_engine
from Database.model import create_db, delete_db

class Base(unittest.TestCase):
    def setUp(self):
        set_test_env()
        self.ENGINE = _get_engine()
        create_db(self.ENGINE)

    def tearDown(self):
        delete_db(self.ENGINE)