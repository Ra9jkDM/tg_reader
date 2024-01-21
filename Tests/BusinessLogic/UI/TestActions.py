import unittest

from Tests.Database.Base import Base

from BusinessLogic.UI.Actions import *

class TestActions(Base):
    def setUp(self):
        super().setUp()

    def test_info(self):
        result = create_info(self.engine._commands)
        print(result)
    


if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.UI.TestActions