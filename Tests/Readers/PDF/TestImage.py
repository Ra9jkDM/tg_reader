import unittest

from Readers.PDF.Image import Image

class TestImage(unittest.TestCase):
    def setUp(self):
        self.img = Image("img_name", {"ext": "png", "image":b"bytes"})

    def test_name(self):
        name = self.img.name

        self.assertEqual(name, "img_name", 
                "Wrong image name")

    def test_extension(self):
        ext = self.img.ext

        self.assertEqual(ext, "png",
                "Wrong image extension")

    def test_get_bytes(self):
        b = self.img.get_bytes()

        self.assertEqual(*b, b"bytes", 
                "Wrong byte object")


if __name__ == "__main__":
    unittest.main()

# python -m Tests.Readers.PDF.TestImage