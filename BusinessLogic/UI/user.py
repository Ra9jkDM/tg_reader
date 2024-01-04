from functools import wraps

from BusinessLogic.Database.main import Database
from BusinessLogic.Language.LanguageController import LanguageController

def user(func):
    @wraps(func)
    def get_user(self, *args, **kwargs):
        db = Database()
        user = db.get_user(self._social_id)

        lang = user.preferences.language
        answers = LanguageController(lang)

        return func(self, user, answers, *args, **kwargs)

    return get_user