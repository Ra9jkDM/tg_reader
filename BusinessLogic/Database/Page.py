from typing import NamedTuple

from Database.session import session
from Database.preferences import *

from Database.model import User, UserBook, Page as DB_Page
from FileStorage.FileStorageController import FileStorageController
from FileStorage.MinIO import MinIO

class Page:
    def __init__(self, id, db):
        self._id = id
        self._db = db

        self._storage = FileStorageController()
        self._minio = MinIO()

    @session
    def _get(self, db, page_number):
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

    @session
    def get(self, db, page_number):
        self._page_number = page_number
        active_book = self._get_active_book(db)

        self._set_bookmark(db, active_book)

        page = self._get_page(db, active_book)
        images = self._get_images(active_book)

        chars_on_page = self._get_max_chars_on_page(db)
        chunk = page.text[:chars_on_page]
        page = self._convert(page_number, chunk, images)

        self._update_state(db, active_book, len(chunk))
        print(*page)
        return page        


    # ToDo: refactor this function    
    @session
    def get_part_of_page(self, db): #, page_number):
        # self._page_number = page_number
        self._page_number = self._get_bookmark(db)
        active_book = self._get_active_book(db)

        # bookmark = self._get_bookmark()
        chars_from_start = self._get_chars_from_start(db, active_book)
        chars_on_page = self._get_max_chars_on_page(db)

        page = self._get_page(db, active_book)
        # print(bookmark, chars_on_page, chars_from_start, len(page.text))


        if len(page.text) - chars_from_start > chars_on_page:
            end = page.text.find(".", chars_from_start+chars_on_page) + 1
            chunk = page.text[chars_from_start:end]

            page = self._convert(page.page_number, chunk, [])
            # update
            self._update_state(db, active_book, chars_from_start+len(chunk))

        else:
            remainder = page.text[chars_from_start:]

            self._page_number += 1
            page = self._get_page(db, active_book)
            images = self._get_images(active_book)

            end = page.text.find(".", chars_on_page) + 1
            chunk = remainder + " " + page.text[:end]

            page = self._convert(page.page_number, chunk, images)
            # update
            self._update_state(db, active_book, len(chunk))

        # print(len(chunk), chunk)

        return page

    def _convert(self, page_number, text, images):
        return PageDTO(**{
            "page_number": page_number,
            "text": text,
            "images": images,
        })

    def _update_state(self, db, book, chars_from_start):
        self._set_chars_from_start(chars_from_start)
        self._set_bookmark(db, book)

    @session
    def get_bookmark(self, db):
        return self._get_bookmark(db)

    # def get_current(self):
    #     bookmark = self._get_bookmark()
    #     return self.get(bookmark)

    # def get_next(self):
    #     bookmark = self._get_bookmark()
    #     return self.get(bookmark + 1)

    # def get_previous(self):
    #     bookmark = self._get_bookmark()
    #     return self.get(bookmark - 1)

    def _get_active_book(self, db):
        return self._db.get_user(db, self._id).current_book
    
    def _get_page(self, db, book):
        return self._db.get_page(db, book, self._page_number)

    def _get_images(self, book):
        return self._storage.download_images(self._minio, book, self._page_number)

    def _set_bookmark(self, db, active_book):
        obj = self._get_user_book(db, active_book)
        obj.bookmark = self._page_number
        self._db.commit(db)

    
    def _get_bookmark(self, db):
        active_book = self._get_active_book(db)
        obj = self._get_user_book(db, active_book)
        return obj.bookmark

    def _get_user_book(self, db, book):
        return self._db.get_user_book(db, self._id, book)

    def _get_chars_from_start(self, db, book):
        return self._get_user_book(db, book).number_of_chars

    @session
    def _set_chars_from_start(self, db, number):
        active_book = self._get_active_book(db)
        user = self._get_user_book(db, active_book)

        user.number_of_chars = number

        self._db.commit(db)
    
    def _get_max_chars_on_page(self, db):
        user = self._db.get_user(db, self._id)
        return user.preferences[CHARS_ON_PAGE]



class PageDTO(NamedTuple):
    page_number: int
    text: str
    images: list