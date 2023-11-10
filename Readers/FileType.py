from enum import Enum

FileTypes = str | bytes

class FileType(Enum):
    PATH = 1
    BYTES = 2
