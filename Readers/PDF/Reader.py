from ..ReaderInterface import ReaderInterface
from ..ImageInterface import ImageInterface
from ..FileType import FileType, FileTypes

from .Image import Image

import fitz
from fitz.fitz import Document

class PDFReader(ReaderInterface):
    _pdf_file: Document
    _img_name_template: str = "{}_{}"

    
    def __init__(self, file: FileTypes, file_type: FileType = FileType.PATH):
        if file_type == FileType.PATH:
            self._pdf_file = fitz.open(file)
        else:
            self._pdf_file = fitz.open(stream = file, filetype = "pdf")

    def get_title(self) -> str:
        return self._pdf_file.metadata["title"]

    def get_number_of_pages(self) -> int:
        return self._pdf_file.page_count

    def set_page(self, index: int) -> None:
        self._index: int = index
        self._page = self._pdf_file[index]

    def get_text(self) -> str:
        return self._page.get_text('text')

    def get_images(self) -> list[ImageInterface]:
        image_list = self._page.get_images(full=True)

        images: list[ImageInterface] = []

        for i, image in enumerate(image_list):
            img = self._get_image(image, i)
            images.append(img)

        return images

    def _get_image(self, image: tuple, page_number: int) -> ImageInterface:
        xref = image[0]

        base_image: dict = self._pdf_file.extract_image(xref)
        image_name: str = self._img_name_template.format(self._index, page_number)
        
        return Image(image_name, base_image)


if __name__ == "__main__":
    book = "Tests/Readers/PDF/test_book.pdf"
    reader: ReaderInterface = PDFReader(book)
    reader.set_page(0)
    reader.get_images()

    with open(book ,"rb") as f:
        reader = PDFReader(f.read(), file_type = FileType.BYTES)
        reader.set_page(0)
        print(reader.get_number_of_pages(), reader.get_text(), str(reader.get_images()),
        reader.get_title())


# python -m Readers.PDF.Reader
# mypy -m Readers.PDF.Reader