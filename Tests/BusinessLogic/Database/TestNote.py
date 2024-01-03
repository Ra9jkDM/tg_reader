import unittest

from Database.session import session
from Database.model import User

from BusinessLogic.Database.main import Database
from BusinessLogic.Database.Book import Book

from Tests.Database.Base import Base

from .Data.NoteData import NoteData, id, id_second


class TestNote(Base): 
    def setUp(self):
        super().setUp()   

        self.data = NoteData()
        self.data.create()

        db = Database()
        user = db.get_user(id)
        self.note = user.note

        user2 = db.get_user(id_second)
        self.note2 = user2.note

    def test_get_all_notes(self):
        notes = self.note.get_all()

        self.assertEqual(len(notes), 4)

    def test_create_note(self):
        self.note2.create("Some note")
        notes = self.note2.get_all()

        self.assertEqual(len(notes), 1)

    def test_create_more_notes_on_one_page(self):
        self.note2.create("Some note")
        self.note2.create("note2")
        self.note2.create("e3")

        notes = self.note2.get_all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, "Some note\nnote2\ne3")

    def test_delete_note(self):
        self.note.delete(31)

        notes = self.note.get_all()

        self.assertEqual(len(notes), 3)

if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestNote