from Database.session import session

from Database.model import User
from Database.preferences import *

class Preferences:
    def __init__(self, id, db):
        self._id = id
        self._db = db

    @property
    def chars_on_page(self):
        return self._get_setting(CHARS_ON_PAGE)

    @chars_on_page.setter
    def chars_on_page(self, number_of_chars):
        self._save_setting(CHARS_ON_PAGE, number_of_chars)        

    @property
    def language(self):
        return self._get_setting(LANGUAGE)
    
    @language.setter
    def language(self, lang):
        self._save_setting(LANGUAGE, lang)

    @property
    def remove_enters(self):
        return self._get_setting(REMOVE_ENTERS)
    
    @remove_enters.setter
    def remove_enters(self, value: bool):
        self._save_setting(REMOVE_ENTERS)

    @session
    def _get_setting(self, db, name):
        user = self._db.get_user(db, self._id)
        return user.preferences[name]

    @session
    def _save_setting(self, db, name, value):
        user = self._db.get_user(db, self._id)
        user.preferences[name] = value
        self._db.commit(db)