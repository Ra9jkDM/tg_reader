from abc import ABC, abstractmethod

import io

class FileStorageInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def upload_file(self, folder: str, file_name: str, file: io.BytesIO) -> None:
        pass

    @abstractmethod
    def list_folder(self, folder: str):
        pass

    @abstractmethod
    def download_file(self, folder: str, file_name: str) -> io.BytesIO:
        pass

    @abstractmethod
    def remove_folder(self, folder: str) -> None:
        pass

# baseFolder
            # /book1
                    # /book.pdf
                    # /page1/img1.png
                    # /page2/img2.png
            # /book2
