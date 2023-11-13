from ..ReaderInterface import ReaderInterface
from ..ImageInterface import ImageInterface
from ..FileType import FileType, FileTypes

from .Image import Image

import fitz
from fitz.fitz import Document

class PDFReader(ReaderInterface):
    _pdfFile: Document
    _imgNameTemplate: str = "{}_{}"

    
    def __init__(self, file: FileTypes, fileType: FileType = FileType.PATH):
        if fileType == FileType.PATH:
            self._pdfFile = fitz.open(file)
        else:
            self._pdfFile = fitz.open(stream = file, filetype = "pdf")

    def getTitle(self) -> str:
        return self._pdfFile.metadata["title"]

    def getNumberOfPages(self) -> int:
        return self._pdfFile.page_count

    def setPage(self, index: int) -> None:
        self._index: int = index
        self._page = self._pdfFile[index]

    def getText(self) -> str:
        return self._page.get_text('text')

    def getImages(self) -> list[ImageInterface]:
        image_list = self._page.get_images(full=True)

        images: list[ImageInterface] = []

        for i, image in enumerate(image_list):
            img = self._getImage(image, i)
            images.append(img)

        return images

    def _getImage(self, image: tuple, pageNumber: int) -> ImageInterface:
        xref = image[0]

        baseImage: dict = self._pdfFile.extract_image(xref)
        imageName: str = self._imgNameTemplate.format(self._index, pageNumber)
        
        return Image(imageName, baseImage)


if __name__ == "__main__":
    book = "Tests/Readers/PDF/test_book.pdf"
    reader: ReaderInterface = PDFReader(book)
    reader.setPage(0)
    reader.getImages()

    with open(book ,"rb") as f:
        reader = PDFReader(f.read(), fileType = FileType.BYTES)
        reader.setPage(0)
        print(reader.getNumberOfPages(), reader.getText(), str(reader.getImages()),
        reader.getTitle())


# python -m Readers.PDF.Reader
# mypy -m Readers.PDF.Reader