from abc import ABC, abstractmethod
from .FileType import FileType, FileTypes
from .ImageInterface import ImageInterface

class ReaderInterface(ABC):
    @abstractmethod
    def __init__(self, file: FileTypes, file_type: FileType):
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_number_of_pages(self) -> int:
        pass

    @abstractmethod
    def set_page(self, index: int) -> None:
        pass

    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def get_images(self) -> list[ImageInterface]:
        pass

