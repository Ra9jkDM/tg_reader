from abc import ABC, abstractmethod

import io


class ImageInterface(ABC):
    @abstractmethod
    def __init__(self, name: str, base_image: dict):
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
    def get_bytes(self) -> io.BytesIO:
        pass