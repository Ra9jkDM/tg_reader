# New interface
# id = 92432
# user = db.getUser(id)

# if not user:
#     user = db.registerUser(id)
#     # send Welcome messsage

# user.getBooks()

# # Upload book
# new_book = user.createBook(name)
# store = minio.createImageStore(new_book)
# store.uploadBook(book_file_io)

# for i in pages:
#     new_book.addPage(text, number_of_images)
#     store.upload(page, image)

# new_book.save()

# # Get content
# user.getBooks()
# choice = 1
# user.setBook(choice)
# #user.setBookmark(3)
# text, imgs = user.getPage()

from Database.session import session
from Database.model import User as DB_User
from .User import User

class Database:
    @session
    def get_user(self, db, social_id):
        user = db.query(DB_User).filter(DB_User.social_id == social_id).first()

        if user:
            return User(user.id)

    @session
    def register_user(self, db, social_id):
        new_user = DB_User(social_id = social_id)

        db.add(new_user)
        db.commit()
        

if __name__ == "__main__":
    db = Database()

    user = db.get_user(123)