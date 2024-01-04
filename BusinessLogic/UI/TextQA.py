from BusinessLogic.Database.main import Database
from .user import user


class TextQA: # Questions & Answers
    def __init__(self, social_id):
        self._social_id = social_id
    
    def is_user_exists(self):
        db = Database()
        return db.get_user(self._social_id)

    def register_user(self):
        db = Database()
        db.register_user(self._social_id)

    def choose_language(self):
        return "Для продолжения выберите язык:\nSelect your language to continue:", ["Русский", "English"]

    @user
    def set_language(self, user, answers, lang): # ru, en
        user.preferences.language = lang

        answers.set_language(lang)
        return answers.get("lang")
    
    @user
    def welcome(self, user, answers):
        return answers.get("welcome")

    @user
    def heavy_file(self, user, answer):
        return answer.get("heavy_file")

    @user
    def upload_book(self, user, answer, book_name, file):
        user.book.create()

    
