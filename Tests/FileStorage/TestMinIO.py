import unittest

from FileStorage.MinIO import MinIO

class TestMinIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage = MinIO()

        # Create bucket for tests
        cls.storage._BUCKET = "test-minio-bucket"
        cls.storage.__init__()

    def test_01_upload_file(self):
        try:
            self.storage.uploadFile("txt", "1.txt", b"1234_test")
        except:
            self.fail("Can not upload fule to bucket")

    def test_02_download_file(self):
        file = self.storage.downloadFile("txt", "1.txt")

        self.assertEqual(file, b"1234_test")

    def test_03_remove_folder(self):
        try:
            self.storage.removeFolder("txt")
        except:
            self.fail("Can not remove folder in bucket")

    def test_delete_not_empty_bucket(self):
        for i in range(1, 4):
            self.storage.uploadFile("txt", f"{i}.txt", b"1234_test")
        
        for i in range(1, 7):
            self.storage.uploadFile("upload", f"{i}.pdf", b"1234_test")
          

    @classmethod
    def tearDownClass(cls):
        cls.storage.deleteBucket()


if __name__ == "__main__":
    unittest.main()

# python -m Tests.FileStorage.TestMinIO