from typing import NamedTuple

from Database.session import session
from Database.preferences import *

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

    # ToDo: refactor this function
    @session
    def get_part_of_page(self, db, page_number):
        self._page_number = page_number
        active_book = self._get_active_book(db)

        bookmark = self._get_bookmark()
        chars_from_start = self._get_chars_from_start(db, active_book)
        chars_on_page = self._get_max_chars_on_page(db)

        page = self._get_page(db, active_book)
        # print(bookmark, chars_on_page, chars_from_start, len(page.text))


        if len(page.text) - chars_from_start > 100:
            end = page.text.find(".", chars_from_start+chars_on_page) + 1
            chunk = page.text[chars_from_start:end]
            page = PageDTO(**{
                "page_number": page.page_number,
                "text": chunk,
                "images": [],
            })

            # update
            self._set_chars_from_start(chars_from_start + len(page.text))

        else:
            remainder = page.text[chars_from_start:]

            self._page_number += 1
            page = self._get_page(db, active_book)
            images = self._get_images(active_book)

            end = page.text.find(".", chars_on_page) + 1
            chunk = remainder + " " + page.text[:end]

            page = PageDTO(**{
                "page_number": page.page_number,
                "text": chunk,
                "images": images,
            })

            # update
            self._set_chars_from_start(len(page.text))
            self._set_bookmark(db, active_book)

        # print(len(chunk), chunk)

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

    def _get_chars_from_start(self, db, book):
        return self._get_user_book(db, book).number_of_chars

    @session
    def _set_chars_from_start(self, db, number):
        active_book = self._get_active_book(db)
        user = self._get_user_book(db, active_book)

        user.number_of_chars = number

        db.commit()
    
    def _get_max_chars_on_page(self, db):
        user = db.query(User).filter(User.id == self._id).first()
        return user.preferences[CHARS_ON_PAGE]



class PageDTO(NamedTuple):
    page_number: int
    text: str
    images: list