from Database.model import User, UserBook, Page, Note

class DatabaseController:
    def save(self, db, obj):
        db.add(obj)
        db.commit()

    def commit(self, db):
        db.commit()

    def get_user_by_social_id(self, db, social_id):
        return db.query(User).filter(User.social_id == social_id).first()

    def get_user(self, db, id):
        return db.query(User).filter(User.id == id).first()
    
    def get_user_book(self, db, id, book):
        return db.query(UserBook).filter(UserBook.user_id == id, 
                                            UserBook.book_id == book).first()

    def get_all_user_books(self, db, id):
        return db.query(UserBook).filter(UserBook.user_id == id).all()

    def get_note(self, db, book, page):
        return db.query(Note).filter(Note.book_id == book,
                                        Note.page == page).first()

    def get_notes(self, db, book):
        return db.query(Note).filter(Note.book_id == book).all()

    def get_page(self, db, book, page_number):
        return db.query(Page).filter(Page.book_id == book, 
                                    Page.page_number == page_number).first()
    