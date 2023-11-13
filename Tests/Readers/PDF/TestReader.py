import unittest

import fitz

from Readers.PDF.Reader import PDFReader
from Readers.FileType import FileType

BOOK_PATH = "Tests/Readers/PDF/test_book.pdf"

class TestReaderCreate(unittest.TestCase):
    def test_load_pdf_from_path(self):
        try:
            pdf = PDFReader(BOOK_PATH)
        except:
            self.fail("Can not load PDF from path")

    def test_load_pdf_from_memory(self):
        try:
            with open(BOOK_PATH, "rb") as f:
                pdf = PDFReader(f.read(), fileType = FileType.BYTES)
        except:
            self.fail("Can not load PDF from memory stream")

class TestReader(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.reader = PDFReader(BOOK_PATH)

    def test_book_title(self):
        self.assertEqual(self.reader.getTitle(), "Test_sample",
                "The title of the book is incorrect")

    def test_number_of_pages(self):
        self.assertEqual(self.reader.getNumberOfPages(), 3, 
                "The number of pages in the book is incorrect.")

    def test_set_page_in_range(self):
        try:
            self.reader.setPage(2)
        except:
            self.fail("Can not set page in book")

    def test_set_page_out_of_range(self):
        with self.assertRaises(Exception):
            self.reader.setPage(3)

    def test_set_page_out_of_range_under_zero(self):
        try:
            self.reader.setPage(-4)
        except:
            self.fail("Api changed")

    def test_get_text(self):
        self.reader.setPage(2)
        text = self.reader.getText()

        self.assertEqual(text, "Third page\n", 
                "Wrong text")

    def test_get_zero_image(self):
        self.reader.setPage(1)
        images = self.reader.getImages()

        self.assertEqual(len(images), 0,
            "Can not detect images")
    
    def test_get_one_image(self):
        self.reader.setPage(0)
        images = self.reader.getImages()

        self.assertEqual(len(images), 1,
            "Can not detect images")

    def test_get_much_images(self):
        self.reader.setPage(2)
        images = self.reader.getImages()

        self.assertEqual(len(images), 5,
            "Can not detect images")


if __name__ == "__main__":
    unittest.main()

# python -m Tests.Readers.PDF.TestReader