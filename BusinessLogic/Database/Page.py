from typing import NamedTuple

from Database.session import session

from Database.model import User, UserBook, Page as DB_Page
from FileStorage.MinIO import MinIO

class Page:
    def __init__(self, id):
        self._id = id

        self._storage = MinIO()

    @session
    def get(self, db, page_number):
        self._page_number = page_number
        active_book = self._get_active_book(db)

        self._set_bookmark(db, active_book)

        page = self._get_page(db, active_book)
        images = self._get_images(active_book)

        page = PageDTO(**{
            "page_number": page.page_number,
            "text": page.text,
            "images": images,
        })

        return page

    def get_bookmark(self):
        return self._get_bookmark()

    def get_current(self):
        bookmark = self._get_bookmark()
        return self.get(bookmark)

    def get_next(self):
        bookmark = self._get_bookmark()
        return self.get(bookmark + 1)

    def get_previous(self):
        bookmark = self._get_bookmark()
        return self.get(bookmark - 1)

    def _get_active_book(self, db):
        return db.query(User).filter(User.id == self._id).first().current_book
    
    def _get_page(self, db, active_book):
        return db.query(DB_Page).filter(DB_Page.book_id == active_book, 
                                    DB_Page.page_number == self._page_number).first()

    def _get_images(self, active_book):
        images = []

        files_name = self._storage.list_folder(folder=f"{active_book}/{self._page_number}/")
        for i in files_name:
            image = self._storage.download_file("", i)
            images.append(image)

        return images

    def _set_bookmark(self, db, active_book):
        obj = self._get_user_book(db, active_book)
        obj.bookmark = self._page_number
        db.commit()

    @session
    def _get_bookmark(self, db):
        active_book = self._get_active_book(db)
        obj = self._get_user_book(db, active_book)
        return obj.bookmark

    def _get_user_book(self, db, active_book):
        return db.query(UserBook).filter(UserBook.user_id == self._id, 
                                            UserBook.book_id == active_book).first()



class PageDTO(NamedTuple):
    page_number: int
    text: str
    images: list