import unittest

from Database.session import session
from BusinessLogic.Database.main import Database

from Tests.Database.Base import Base

from .Data.DatabaseData import DatabaseData, id, id_unknown


class TestDatabase(Base): 
    def setUp(self):
        super().setUp()   

        self.data = DatabaseData()
        self.data.create()
        
        self.db = Database()

    def test_get_existing_user(self):
        user = self.db.get_user(id)
        
        self.assertTrue(user, "Can not find existing user")

    def test_get_unknown_user(self):
        user = self.db.get_user(id_unknown)

        self.assertFalse(user)

    def test_register_new_user(self):
        self.db.register_user(id_unknown)

        user = self.db.get_user(id_unknown)
        
        self.assertTrue(user)


        

if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestDatabase