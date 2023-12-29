from Database.session import session
from Database.model import Book as DB_Book, UserBook, Page

from FileStorage.FileStorageInterface import FileStorageInterface
from FileStorage.MinIO import MinIO

from Readers.ImageInterface import ImageInterface

class BookUploader:
    def __init__(self, id, name, number_of_pages):
        self._id = id
        self._name = name
        self._number_of_pages = number_of_pages
        self._page_number = 1

        self._storage: FileStorageInterface = MinIO()

    def upload_book(self, ext, file):
        self._storage.uploadFile(folder=self._book_id,
                                    fileName=f"{self._book_id}.{ext}", file=file)

    @session
    def create_book(self, db):
        book = DB_Book(name = self._name, number_of_pages = self._number_of_pages)
        db.add(book)
        db.commit()

        self._book_id = book.id

        user_book = UserBook(user_id = self._id, book_id = self._book_id)
        db.add(user_book)
        db.commit()

    @session
    def save_page(self, db, text, images: list[ImageInterface]):
        page = Page(book_id = self._book_id, page_number = self._page_number,
                     text = text, number_of_images = len(images))
        db.add(page)
        db.commit()

        for i, img in enumerate(images, start=1):
            self._storage.uploadFile(folder=f"{self._book_id}/{self._page_number}", 
                                    fileName=f"{i}.{img.ext}", file=img.getBytes())
        self._page_number+=1
        
