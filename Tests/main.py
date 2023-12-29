import unittest

# BL
from Tests.BusinessLogic.Database.TestDatabase import *
from Tests.BusinessLogic.Database.TestBook import *
from Tests.BusinessLogic.Database.TestBookUploader import *

# Database
from Tests.Database.TestDatabase import *

# FileStorage
from Tests.FileStorage.TestMinIO import *

# Readers
from Tests.Readers.PDF.TestImage import *
from Tests.Readers.PDF.TestReader import *

if __name__ == "__main__":
    unittest.main()

# python -m Tests.main