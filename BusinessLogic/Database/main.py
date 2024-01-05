from Database.session import session
from Database.model import User as DB_User
from Database.DatabaseController import DatabaseController
from .User import User

class Database:
    def __init__(self):
        self._db = DatabaseController()

    @session
    def get_user(self, db, social_id):
        user = self._db.get_user_by_social_id(db, social_id)

        if user:
            return User(user.id, self._db)

    @session
    def register_user(self, db, social_id):
        new_user = DB_User(social_id = social_id)
        self._db.save(db, new_user)
        return new_user
        

if __name__ == "__main__":
    db = Database()

    user = db.get_user(123)