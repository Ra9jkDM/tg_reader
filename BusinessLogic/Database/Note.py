from typing import NamedTuple

from Database.session import session

from Database.model import User, Note as DB_Note, UserBook


class Note:
    def __init__(self, id):
        self._id = id

    @session
    def create(self, db, text):
        active_book = self._get_current_book(db)
        current_page = self._get_current_page(db, active_book)

        note = self._get_note(db, active_book, current_page)

        if note:
            self._append_note(db, note, text)
        else:
            self._create_note(db, active_book, current_page, text)


    @session
    def get_all(self, db):
        active_book = self._get_current_book(db)
        notes = self._get_notes(db, active_book)
        notes = self._convert(notes)
        
        return notes

    @session
    def delete(self, db, page_number):
        active_book = self._get_current_book(db)
        note = self._get_note(db, active_book, page_number)
        self._delete_note(db, note)


    def _get_current_book(self, db):
        user = db.query(User).filter(User.id == self._id).first()
        return user.current_book

    def _get_note(self, db, book, page):
        note = db.query(DB_Note).filter(DB_Note.book_id == book,
                                        DB_Note.page == page).first()
        return note

    def _get_notes(self, db, active_book):
        notes = db.query(DB_Note).filter(DB_Note.user_id == self._id,
                                    DB_Note.book_id == active_book).all()
        return notes

    def _get_current_page(self, db, active_book):
        page = db.query(UserBook).filter(UserBook.user_id == self._id,
                                        UserBook.book_id == active_book).first().bookmark
        return page

    def _create_note(self, db, active_book, current_page, text):
        note = DB_Note(user_id = self._id, book_id = active_book, page = current_page, text = text)
        db.add(note)
        db.commit()

    def _delete_note(self, db, note):
        db.delete(note)
        db.commit()
    
    def _append_note(self, db, note, text):
        note.text += "\n" + text
        db.commit()

    def _convert(self, notes):
        result = []
        for i in notes:
            tmp = NoteDTO(**{
                "page": i.page,
                "text": i.text,
            })
            result.append(tmp)

        return result


class NoteDTO(NamedTuple):
    page: int
    text: str