import unittest

from FileStorage.MinIO import MinIO

from Tests.testEnv import set_test_env

class TestMinIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_test_env()
        cls.storage = MinIO()

    def test_01_upload_file(self):
        try:
            self.storage.upload_file("txt", "1.txt", b"1234_test")
        except:
            self.fail("Can not upload fule to bucket")

    def test_02_download_file(self):
        file = self.storage.download_file("txt", "1.txt")

        self.assertEqual(file, b"1234_test")

    def test_03_remove_folder(self):
        try:
            self.storage.remove_folder("txt")
        except:
            self.fail("Can not remove folder in bucket")

    def test_list_folder(self):
        for i in range(1, 5):
            self.storage.upload_file("3/1", f"{i}.txt", b"1234_test")

        files = self.storage.list_folder("3/1/")

        self.assertEqual(len(files), 4)

    def test_download_files_from_list_folder_output(self):
        for i in range(1, 5):
            self.storage.upload_file("3/1", f"{i}.txt", b"1234_test")

        files = self.storage.list_folder("3/1/")

        downloaded_files = []
        for i in files:
            tmp = self.storage.download_file("", i)
            downloaded_files.append(tmp)

        self.assertEqual(len(downloaded_files), 4)

    def test_delete_not_empty_bucket(self):
        for i in range(1, 4):
            self.storage.upload_file("txt", f"{i}.txt", b"1234_test")
        
        for i in range(1, 7):
            self.storage.upload_file("upload", f"{i}.pdf", b"1234_test")
          

    @classmethod
    def tearDownClass(cls):
        cls.storage.delete_bucket()


if __name__ == "__main__":
    unittest.main()

# python -m Tests.FileStorage.TestMinIO