from io import BytesIO

class FileStorageController:
    def upload_book(self, db, book_id, file, extension):
        db.upload_file(folder=book_id,
                        file_name=f"{book_id}.{extension}", file=file)

    def upload_images(self, db, book_id, page_number, images):
        for i, img in enumerate(images, start=1):
            db.upload_file(folder=f"{book_id}/{page_number}",
                    file_name=f"{i}.{img.ext}", file=img.get_bytes()) 
 
    def download_images(self, db, book_id, page_number):
        images = []

        file_names = self._list_folder(db, book_id, page_number)
        for i in file_names:
            image = db.download_file("", i)

            image = BytesIO(image)
            image.name = i
            image.seek(0)
            
            images.append(image)

        return images

    def delete_book(self, db, book_id):
        db.remove_folder(str(book_id))

    def _list_folder(self, db, book_id, page_number):
        return db.list_folder(folder=f"{book_id}/{page_number}/")
