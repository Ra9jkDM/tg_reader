from abc import ABC, abstractmethod

import io


class ImageInterface(ABC):
    @abstractmethod
    def __init__(self, name: str, baseImage: dict):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def ext(self) -> str:
        pass

    @abstractmethod
    def getBytes(self) -> io.BytesIO:
        pass