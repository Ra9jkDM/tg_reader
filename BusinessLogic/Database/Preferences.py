from Database.session import session

from Database.model import User
from Database.preferences import *

class Preferences:
    def __init__(self, id):
        self._id = id

    @property
    def chars_on_page(self):
        return self._get_setting(CHARS_ON_PAGE)

    @chars_on_page.setter
    def chars_on_page(self, number_of_chars):
        self._save_setting(CHARS_ON_PAGE, number_of_chars)        

    @session
    def _get_setting(self, db, name):
        user = self._get_user(db)
        return user.preferences[name]

    @session
    def _save_setting(self, db, name, value):
        user = self._get_user(db)
        user.preferences[name] = value
        db.commit()

    def _get_user(self, db):
        return db.query(User).filter(User.id == self._id).first()