import unittest

from Database.session import setTestENV, getEngine
from Database.model import *

class Base(unittest.TestCase):
    def setUp(self):
        setTestENV()
        self.ENGINE = getEngine()
        create_db(self.ENGINE)

    def tearDown(self):
        delete_db(self.ENGINE)