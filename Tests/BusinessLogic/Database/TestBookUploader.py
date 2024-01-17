import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from io import BytesIO

from BusinessLogic.Database.main import Database
from BusinessLogic.Database.Book import Book
from BusinessLogic.Database.BookUploader import BookUploader

from Tests.Database.Base import Base
from Readers.ImageInterface import ImageInterface

from .Data.BookUploaderData import BookUploaderData, id


book_name = "ZTest book"

class TestBookUploader(Base): 
    def setUp(self):
        super().setUp()   

        self.data = BookUploaderData()
        self.data.create()

        db = Database()
        user = db.get_user(id)
        self.book = user.book
        self.uploader = self.book.create(book_name, 4)


    def test_create_book(self):
        self.uploader.create_book()

        book = self.book.get_all()[-1]

        self.assertEqual(book.name, book_name)

    def test_upload_book(self):
        self.uploader.create_book()
        self.uploader.upload_book(BytesIO( b'somebook8302'), "pdf")

    @patch.multiple(ImageInterface, __abstractmethods__ = set(),
        get_bytes = MagicMock(return_value=b'1234'), 
        ext=PropertyMock(return_value="png"),
        name=PropertyMock(return_value="test"))
    def test_mock(self):
        mock = ImageInterface("123", "aaa")

        self.assertEqual(mock.ext, 'png')
        self.assertEqual(mock.get_bytes(), b'1234')

    @patch.multiple(ImageInterface, __abstractmethods__ = set(),
        get_bytes = MagicMock(return_value=BytesIO(b'1234')), 
        ext=PropertyMock(return_value="png"),
        name=PropertyMock(return_value="test"))
    def test_upload_page_by_page(self):
        self.uploader.create_book()

        pages = [["Lorem pus", [ImageInterface("", BytesIO(b"")), ImageInterface("", BytesIO(b""))]],
                 ["Leom sim", [ImageInterface("", BytesIO(b""))]]]

        for text, img in pages:
            self.uploader.save_page(text, img)

    def tearDown(self):
        super().tearDown()
        self.uploader._minio.delete_bucket()



if __name__ == "__main__":
    unittest.main()

# python -m Tests.BusinessLogic.Database.TestBookUploader