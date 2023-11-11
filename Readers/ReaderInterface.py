from abc import ABC, abstractmethod
from .FileType import FileType, FileTypes
from .ImageInterface import ImageInterface

class ReaderInterface(ABC):
    @abstractmethod
    def __init__(self, file: FileTypes, fileType: FileType):
        pass

    @abstractmethod
    def getTitle(self) -> str:
        pass

    @abstractmethod
    def getNumberOfPages(self) -> int:
        pass

    @abstractmethod
    def setPage(self, index: int) -> None:
        pass

    @abstractmethod
    def getText(self) -> str:
        pass

    @abstractmethod
    def getImages(self) -> list[ImageInterface]:
        pass

