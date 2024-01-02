from typing import NamedTuple

from Database.session import session

from Database.model import User, Note as DB_Note, UserBook


class Note:
    def __init__(self, id, db):
        self._id = id
        self._db = db

    @session
    def create(self, db, text):
        active_book = self._get_current_book(db)
        current_page = self._db.get_user_book(db, self._id, active_book).bookmark

        note = self._db.get_note(db, active_book, current_page)

        if note:
            self._append_note(db, note, text)
        else:
            self._create_note(db, active_book, current_page, text)


    @session
    def get_all(self, db):
        active_book = self._get_current_book(db)
        notes = self._db.get_notes(db, active_book)
        notes = self._convert(notes)
        
        return notes

    @session
    def delete(self, db, page_number):
        active_book = self._get_current_book(db)
        note = self._db.get_note(db, active_book, page_number)
        self._delete_note(db, note)


    def _get_current_book(self, db):
        return self._db.get_user(db, self._id).current_book

    def _create_note(self, db, active_book, current_page, text):
        note = DB_Note(user_id = self._id, book_id = active_book, page = current_page, text = text)
        self._db.save(db, note)

    def _delete_note(self, db, note):
        db.delete(note)
        self._db.commit(db)
    
    def _append_note(self, db, note, text):
        note.text += "\n" + text
        self._db.commit(db)

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