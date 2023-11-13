from abc import ABC, abstractmethod

import io

class FileStorageInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def uploadFile(self, folder: str, fileName: str, file: io.BytesIO) -> None:
        pass

    @abstractmethod
    def downloadFile(self, folder: str, fileName: str) -> io.BytesIO:
        pass

    @abstractmethod
    def removeFolder(self, folder: str) -> None:
        pass

# baseFolder
            # /book1
                    # /book.pdf
                    # /img1.png
                    # /img2.png
            # /book2
