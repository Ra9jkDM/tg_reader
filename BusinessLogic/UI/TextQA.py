from BusinessLogic.Database.main import Database
from BusinessLogic.Language.LanguageController import LanguageController

from Readers.ReaderInterface import ReaderInterface
from Readers.FileType import FileType
from Readers.PDF.Reader import PDFReader

EXT = [".pdf"] # supported file formats

class TextQA: # Questions & Answers
    def __init__(self, social_id):
        self._social_id = social_id

        db = Database()
        self._user = db.get_user(self._social_id)

        if self._user:
            lang = self._user.preferences.language
            self._answers = LanguageController(lang)
    
    def is_user_exists(self):
        db = Database()
        return db.get_user(self._social_id)

    def register_user(self):
        db = Database()
        self._user = db.register_user(self._social_id)
        

    def choose_language(self):
        return "Для продолжения выберите язык:\nSelect your language to continue:", ["Русский", "English"]

    def set_language(self, lang): # ru, en
        self._user.preferences.language = lang
        
        self._answers.set_language(lang)
        return self._answers.get("lang")
    
    def welcome(self):
        return self._answers.get("welcome")

    def chars_on_page(self):
        return self._answers.get("chars_on_page_q")

    def set_chars_on_page(self, num):
        if num.isnumeric() and int(num) < 1000:
            self._user.preferences.chars_on_page = int(num)
            return self._answers.get("chars_on_page_success").format(num)
        return self._answers.get("chars_on_page_error")
        

    def check_book(self, ext, size):
        if not ext in EXT:
            return False, self._answers.get("not_supported_file_format")
        elif size / (1024*1024) > 51:
            return False, self._answers.get("heavy_file").format("51MB")
        return True, ""

    def upload_book_notify(self):
        return self._answers.get("upload_book_notify")

    def upload_book(self, book_name, ext, file):
        book_name = book_name[:-len(ext)]

        pdf: ReaderInterface = PDFReader(file, FileType.BYTES)
        pages_in_book = pdf.get_number_of_pages()

        uploader = self._user.book.create(book_name, pages_in_book)

        uploader.create_book()
        uploader.upload_book(file, ext)

        for i in range(pages_in_book):
            pdf.set_page(i)
            text = pdf.get_text()
            imgs = pdf.get_images()

            uploader.save_page(text, imgs)

        return self._answers.get("upload_book_success").format(book_name)

    def list_books(self):
        book_list = self._answers.get("book_list") + "\n"

        books = self._user.book.get_all()
        for i, book in enumerate(books, start=1):
            book_list += f"{i}. [{book.bookmark}/{book.number_of_pages}] {book.name}\n"

        return book_list

    def read_book(self):
        return self._user.page.get_current()

    def navigate_buttons(self):
        return self._answers.get("previous"), self._answers.get("next")

    # Test bugs
    def get_next_page(self):
        result =  self._user.page.get_next_part()

        if not result.text:
            result = self._answers.get("book_end")
        return result

    # Test bugs
    def get_previous_page(self):
        result = self._user.page.get_previous_part()
        
        if not result.text:
            result = self._answers.get("book_start")
        return result

    def set_book_q(self):
        return self._answers.get("set_book_q") + "\n" + self.list_books()

    def set_book(self, num):
        if num.isnumeric() and 0 < int(num) <= self._user.book.book_amount():
            book_name = self._user.book.set(int(num))
            return self._answers.get("set_book_success").format(book_name)
        else:
            return self._answers.get("set_book_error")

    def edit_book_name_q(self):
        title = self._user.book.get_name()
        return self._answers.get("edit_book_name").format(title)

    def edit_book_name(self, book_name):
        self._user.book.edit_name(book_name)
        return self._answers.get("edit_book_name_success")

    def delete_book_q(self):
        title = self._user.book.get_name()
        return self._answers.get("delete_book").format(title)

    def delete_book(self, answer):
        if answer.lower() in ["да", "yes"]:
            title = self._user.book.delete()
            return self._answers.get("delete_book_success").format(title)
        else:
            return self._answers.get("delete_book_cancel")
        
    
    def set_page_q(self):
        self._max_page = self._user.book.page_amount()
        return self._answers.get("set_page").format(self._max_page)

    def set_page(self, page_number):
        if page_number.isnumeric() and 0 < int(page_number) <= self._max_page:
            return self._user.page.get(int(page_number))
        else:
            return self._answers.get("set_page_error")


    def note(self):
        return self._answers.get("note")

    def list_notes(self):
        result = self._answers.get("list_notes") + "\n"
        notes = self._user.note.get_all()

        for i in notes:
            result+= f"{i.page}. {i.text}\n"

        return result

    def create_note_q(self):
        return self._answers.get("create_note")

    def create_note(self, note):
        self._user.note.create(note)
        return self._answers.get("create_note_success")

    def delete_note_q(self):
        result = self._answers.get("delete_note") + "\n"
        result+=self.list_notes()
        return result

    def delete_note(self, notes):
        notes = notes.replace(' ', '').split(',')
        notes = list(map(int, notes))

        try:
            for i in notes:
                self._user.note.delete(i)
        except:
            pass

        return self._answers.get("delete_note_success")


 
