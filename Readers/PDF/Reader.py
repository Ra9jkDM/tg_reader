from ..ReaderInterface import ReaderInterface
from ..ImageInterface import ImageInterface
from ..FileType import FileType, FileTypes

from .Image import Image

import fitz


class PDFReader(ReaderInterface):
    _img_name_template: str = "{}_{}"

    def __init__(self, file: FileTypes, fileType: FileType = FileType.PATH):
        if fileType == FileType.PATH:
            self._pdf_file = fitz.open(file)
        else:
            self._pdf_file = fitz.open(stream = file, filetype = "pdf")

    def getNumberOfPages(self) -> int:
        return self._pdf_file.page_count

    def setPage(self, index: int) -> None:
        self._index: int = index
        self._page = self._pdf_file[index]

    def getText(self) -> str:
        return self._page.get_text('text')

    def getImages(self) -> list[ImageInterface]:
        image_list = self._page.get_images(full=True)

        images: list[ImageInterface] = []

        for i, image in enumerate(image_list):
            img = self._get_image(image, i)
            images.append(img)

        return images

    def _get_image(self, image, page_number: int) -> ImageInterface:
        xref = image[0]

        base_image = self._pdf_file.extract_image(xref)
        image_name = self._img_name_template.format(self._index, page_number)
        
        return Image(image_name, base_image)


if __name__ == "__main__":
    book = "tmp_x/pdf/ref.pdf"
    reader: ReaderInterface = PDFReader(book)
    reader.setPage(12)
    reader.getImages()

    with open(book ,"rb") as f:
        reader = PDFReader(f.read(), fileType = FileType.BYTES)
        reader.setPage(12)
        print(reader.getNumberOfPages(), reader.getText(), str(reader.getImages()[0]))


# python -m Readers.PDF.Reader
# mypy -m Readers.PDF.Reader