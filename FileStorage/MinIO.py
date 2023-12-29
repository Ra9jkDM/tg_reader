from typing import Final
from .FileStorageInterface import FileStorageInterface

from minio import Minio
from minio.deleteobjects import DeleteObject

import io
from os import environ

from Tests.testEnv import KEY

class MinIO(FileStorageInterface):
    _HOST: Final = environ.get("S3_HOST")
    _PORT: Final = environ.get("S3_PORT")
    _BUCKET: Final = environ.get("S3_BUCKET")

    # generate in MimIO web console [localhost/access-keys]
    _ACCESS_KEY: Final = environ.get("S3_ACCESS_KEY")
    _SECRET_KEY: Final = environ.get("S3_SECRET_KEY")
    _SECURE: Final = int(environ.get("S3_SECURE")) # type: ignore # Http -> False[0], Https -> True[1] 

    def __init__(self):
        if environ.get(KEY):
            self._BUCKET += "-test"

        self._client = Minio(f"{self._HOST}:{self._PORT}",
                access_key = self._ACCESS_KEY,
                secret_key = self._SECRET_KEY,
                secure = self._SECURE)
        
        found = self._client.bucket_exists(self._BUCKET)
        if not found:
            self._client.make_bucket(self._BUCKET)


    def upload_file(self, folder: str, file_name: str, file: io.BytesIO) -> None:
        response = self._client.put_object(
            self._BUCKET, f"{folder}/{file_name}", io.BytesIO(file), # type: ignore
                    length=-1, part_size=5*1024*1024
        )

    def list_folder(self, folder: str):
        files = self._client.list_objects(bucket_name = self._BUCKET, prefix=folder)
        
        file_list = []

        for i in files:
            file_list.append(i.object_name)
        
        return file_list

    def download_file(self, folder: str, file_name: str) -> io.BytesIO:
        data = None
        try:
            response = self._client.get_object(bucket_name = self._BUCKET, object_name = f"{folder}/{file_name}")
            data = response.data
        finally:
            response.close()
            response.release_conn()

        return data

    def remove_folder(self, folder: str) -> None:
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            self._client.list_objects(self._BUCKET, folder, recursive=True),
        )
        errors = self._client.remove_objects(self._BUCKET, delete_object_list)
        for error in errors:
            print("error occurred when deleting object", error)

    def delete_bucket(self):
        self.remove_folder('')
        self._client.remove_bucket(self._BUCKET)


if __name__ == "__main__":
    minio = MinIO()
    # with open("Tests/Readers/PDF/test_book.pdf", "rb") as f:
    #     minio.uploadFile("img", "i.txt", f.read())

    # file = minio.downloadFile("img", "i.txt")

    # with open("i.pdf", "wb") as f:
    #     f.write(file)

    # minio.removeFolder("img")

# python -m FileStorage.MinIO