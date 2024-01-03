from typing import NamedTuple

from Database.session import session
from Database.preferences import *

from Database.model import User, UserBook, Page as DB_Page
from FileStorage.FileStorageController import FileStorageController
from FileStorage.MinIO import MinIO

from BusinessLogic.PageSlicer import PageSlicer

class Page:
    def __init__(self, id, db):
        self._id = id
        self._db = db

        self._storage = FileStorageController()
        self._minio = MinIO()

        self._slicer = PageSlicer()

    @session
    def get(self, db, page_number):
        self._page_number = page_number

        page = self._get_full_page(db)
        chunk = self._slicer.slice(page.text, 0, self._chars_on_page)
        page = self._convert(self._page_number, chunk.text, page.images)

        self._update_state(db, chunk.amount, len(chunk.text))
        
        return page       

    @session
    def get_next_part(self, db):
        self._page_number = self._get_bookmark(db)
        page = self._get_full_page(db)
        start = self._get_chars_from_start(db)

        if self._slicer.check_is_enough(page.text, start, self._chars_on_page):
            chunk = self._slicer.slice(page.text, start, self._chars_on_page)
            page = self._convert(self._page_number, chunk.text, [])
        else:
            self._page_number += 1
            page2 = self._get_full_page(db)

            chunk = self._slicer.slice_2_pages(page.text, page2.text, start, self._chars_on_page)
            page = self._convert(self._page_number, chunk.text, page2.images)

        self._update_state(db, chunk.amount, len(chunk.text))

        return page

    @session
    def get_previous_part(self, db):
        self._page_number = self._get_bookmark(db)
        page = self._get_full_page(db)
        start = self._get_chars_from_start(db)
        chunk_size = self._get_chunk_size(db)

        # print(start, self._chars_on_page, len(page.text), self._page_number,
        # self._slicer.check_is_enough_previous(page.text, start-chunk_size, self._chars_on_page))

        if self._slicer.check_is_enough_previous(page.text, start, self._chars_on_page): # self._chars_on_page
            chunk = self._slicer.previous_slice(page.text, start, self._chars_on_page, chunk_size)
            chunk = self._slicer.previous_slice(page.text, chunk.amount, self._chars_on_page)
            page = self._convert(self._page_number, chunk.text, [])
            # print(chunk)

            
            # print("ch:", chunk.amount, len(chunk.text))
            self._update_state(db, chunk.amount+len(chunk.text), len(chunk.text))
        else:
            self._page_number -= 1
            self._set_bookmark(db)

            page2 = self._get_full_page(db)
            chunk = self._slicer.previous_slice_2_pages(page2.text, page.text, start, self._chars_on_page)
            # print(chunk)

            page = self._convert(self._page_number, chunk.text, page.images)

            
            # print("ch:", chunk.amount, len(page2.text))

            # if chunk.amount < 0:
            #     chunk.amount *= -1
        
        
            self._update_state(db, chunk.amount, len(chunk.text))

        return page

    def _get_full_page(self, db):
        self._load_user_info(db)

        self._set_bookmark(db)

        page = self._get_page(db)
        images = self._get_images()

        return self._convert(self._page_number, page.text, images)


    def _convert(self, page_number, text, images):
        return PageDTO(**{
            "page_number": page_number,
            "text": text,
            "images": images,
        })

    def _update_state(self, db, chars_from_start, chunk_size):
        self._set_chars_from_start(chars_from_start)
        self._set_bookmark(db)
        self._set_chunk_size(db, chunk_size)


    
    
    def _get_page(self, db):
        return self._db.get_page(db, self._book, self._page_number)

    def _get_images(self):
        return self._storage.download_images(self._minio, self._book, self._page_number)

    def _get_chars_from_start(self, db):
        return self._get_user_book(db).number_of_chars

    @session
    def _set_chars_from_start(self, db, number):
        user = self._get_user_book(db)
        user.number_of_chars = number
        self._db.commit(db)

    @session
    def get_bookmark(self, db):
        return self._get_bookmark(db)

    def _set_bookmark(self, db):
        obj = self._get_user_book(db)
        obj.bookmark = self._page_number
        self._db.commit(db)

    def _get_bookmark(self, db):
        obj = self._get_user_book(db)
        return obj.bookmark

    def _set_chunk_size(self, db, chunk_size):
        obj = self._get_user_book(db)
        obj.chunk_size = chunk_size
        self._db.commit(db)
    
    def _get_chunk_size(self, db):
        obj = self._get_user_book(db)
        return obj.chunk_size

    def _get_user_book(self, db):
        return self._db.get_user_book(db, self._id, self._book)
    
    def _load_user_info(self, db):
        user = self._db.get_user(db, self._id)

        self._book = user.current_book
        self._chars_on_page = user.preferences[CHARS_ON_PAGE]



class PageDTO(NamedTuple):
    page_number: int
    text: str
    images: list