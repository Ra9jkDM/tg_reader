from Database.session import session
from Database.model import *

from .main import Data

id = "9000123"

class BookUploaderData(Data):
    @session
    def _create_data(self, db):
        # create User
        user = User(social_id=id, preferences={}, current_book=2)

        self._save(db, [user])
        