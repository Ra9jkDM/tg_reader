from BusinessLogic.Language.LanguageController import LanguageController
from ..Actions.Base import get_language, _get_user
from ..Message import Message

from Readers.ReaderInterface import ReaderInterface
from Readers.FileType import FileType
from Readers.PDF.Reader import PDFReader

class FileCommand:
    _extensions = [".pdf"]
    _max_file_size = 51

    def __init__(self, user_id):
        lang_text = get_language(user_id)
        self.lang = LanguageController(lang_text)
        self.user_id = user_id

    def check(self, extension, size):
        if not extension in self._extensions:
            return False, Message(text=self.lang.get("not_supported_file_format"))
        if size / (1024*1024) > self._max_file_size:
            return False, Message(text=self.lang.get("heavy_file").format(f"{self._max_file_size}MB"))
        return True, Message(text=self.lang.get("file_strart_downloading"))

    def upload(self,  name, extension, file):
        book_name = name[:-len(extension)]

        pdf: ReaderInterface = PDFReader(file, FileType.BYTES)
        pages_in_book = pdf.get_number_of_pages()

        user = _get_user(self.user_id)
        uploader = user.book.create(book_name, pages_in_book)

        uploader.create_book()
        uploader.upload_book(file, extension)

        for i in range(pages_in_book):
            pdf.set_page(i)
            text = pdf.get_text()
            imgs = pdf.get_images()

            uploader.save_page(text, imgs)

        return Message(text=self.lang.get("upload_book_success").format(book_name))

