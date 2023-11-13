from ..ImageInterface import ImageInterface

import io

class Image(ImageInterface):
    def __init__(self, name: str, baseImage: dict):
        self._name: str = name
        self._image: dict = baseImage

    @property
    def name(self) -> str:
        return self._name

    @property
    def ext(self) -> str:
        return self._image["ext"]

    def getBytes(self) -> io.BytesIO:
        imageBytes: bytes = self._image["image"]

        return io.BytesIO(imageBytes)
    
    def __str__(self) -> str:
        return f"Image({self.name}.{self.ext})"