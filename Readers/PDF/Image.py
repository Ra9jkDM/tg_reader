from ..ImageInterface import ImageInterface

import io

class Image(ImageInterface):
    def __init__(self, name: str, base_image):
        self._name = name
        self._image = base_image

    @property
    def name(self) -> str:
        return self._name

    @property
    def ext(self) -> str:
        return self._image["ext"]

    def getBytes(self) -> io.BytesIO:
        image_bytes = self._image["image"]

        return io.BytesIO(image_bytes)
    
    def __str__(self) -> str:
        return f"Image({self.name}.{self.ext})"