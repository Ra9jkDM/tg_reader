import unittest

from Database.session import session
from BusinessLogic.Database.main import Database

from Tests.Database.Base import Base

from .Data import Data, id_1, id_2, id_3



class TestDatabase(Base): 
    def setUp(self):
        super().setUp()   

        self.data = Data()
        self.data.create()
        
        self.db = Database()

    def test_get_existing_user(self):
        user = self.db.get_user(id_1)

        self.assertTrue(user, "Can not find existing user")

    def test_get_unknown_user(self):
        user = self.db.get_user(id_3)

        self.assertFalse(user)

    def test_register_new_user(self):
        self.db.register_user(id_3)

        user = self.db.get_user(id_3)
        
        self.assertTrue(user)


        

if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestDatabase