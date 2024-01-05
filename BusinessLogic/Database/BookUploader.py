from Database.session import session

from FileStorage.FileStorageController import FileStorageController

from Database.model import Book as DB_Book, UserBook, Page

from FileStorage.FileStorageInterface import FileStorageInterface
from FileStorage.MinIO import MinIO

from Readers.ImageInterface import ImageInterface

class BookUploader:
    def __init__(self, db, id, name, number_of_pages):
        self._id = id
        self._name = name
        self._number_of_pages = number_of_pages
        self._page_number = 1

        self._db = db
        self._minio: FileStorageInterface = MinIO()
        self._storage = FileStorageController()

    @session
    def create_book(self, db):
        book = DB_Book(name = self._name, number_of_pages = self._number_of_pages)
        self._db.save(db, book)
        self._book_id = book.id

        user = self._db.get_user(db, self._id)
        user.current_book = self._book_id

        user_book = UserBook(user_id = self._id, book_id = self._book_id)
        self._db.save(db, user_book)

    def upload_book(self, file, extension):
        self._storage.upload_book(self._minio, self._book_id, file, extension)

    @session
    def save_page(self, db, text, images: list[ImageInterface]):
        page = Page(book_id = self._book_id, page_number = self._page_number,
                     text = text, number_of_images = len(images))
        self._db.save(db, page)

        self._storage.upload_images(self._minio, self._book_id, self._page_number, images)
        self._page_number+=1
        
