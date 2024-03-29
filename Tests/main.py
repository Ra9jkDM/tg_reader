import unittest

# BL
from Tests.BusinessLogic.TestPageSlicer import *

from Tests.BusinessLogic.Database.TestDatabase import *
from Tests.BusinessLogic.Database.TestBook import *
from Tests.BusinessLogic.Database.TestBookUploader import *
from Tests.BusinessLogic.Database.TestPage import *
from Tests.BusinessLogic.Database.TestNote import *
from Tests.BusinessLogic.Database.TestPreferences import *

# Database
from Tests.Database.TestDatabase import *

# FileStorage
from Tests.FileStorage.TestMinIO import *

# Readers
from Tests.Readers.PDF.TestImage import *
from Tests.Readers.PDF.TestReader import *

# Language
from Tests.BusinessLogic.Language.TestLanguageController import TestLanguageController

#UI

if __name__ == "__main__":
    unittest.main()

# python -m Tests.main