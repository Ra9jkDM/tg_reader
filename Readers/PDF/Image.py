from ..ImageInterface import ImageInterface

import io

class Image(ImageInterface):
    def __init__(self, name: str, base_image: dict):
        self._name: str = name
        self._image: dict = base_image

    @property
    def name(self) -> str:
        return self._name

    @property
    def ext(self) -> str:
        return self._image["ext"]

    def get_bytes(self) -> io.BytesIO:
        image_bytes: bytes = self._image["image"]

        return io.BytesIO(image_bytes)
    
    def __str__(self) -> str:
        return f"Image({self.name}.{self.ext})"