from Database.session import session
from Database.model import *
from FileStorage.MinIO import MinIO

id_1 = "99888"
id_2 = "222322"
id_3 = "-999" # unknown_user

class Data:
    def create(self):
        try:
            self._create_data()
        except:
            pass

    @session
    def _create_data(self, db):
        # create Users
        user1 = User(social_id=id_1, preferences={}, current_book=2)
        user2 = User(social_id=id_2, preferences={})

        self._save(db, [user1, user2])
        #create Books

        book1 = Book(name="Book 1", number_of_pages=500)
        book2 = Book(name="Book 2", number_of_pages=100)
        book3 = Book(name="Book 3", number_of_pages=40)
        book4 = Book(name="Book 4", number_of_pages=55)

        self._save(db, [book1, book2, book3, book4])

        # Created pages

        page1 = Page(book_id=book2.id, page_number=1, text="In dolor condimentum dignissim", number_of_images=0)
        page2 = Page(book_id=book2.id, page_number=2, text="With images", number_of_images=3)
        
        page30 = Page(book_id=book2.id, page_number=30, text="30 page", number_of_images=0)
        page31 = Page(book_id=book2.id, page_number=31, text="31 page", number_of_images=0)
        page32 = Page(book_id=book2.id, page_number=32, text="32 page", number_of_images=0)

        self._save(db, [page1, page2, page30, page31, page32])

        # - Create images
        minio = MinIO()
        for i in range(1, 4):
            minio.upload_file(folder=f"{book2.id}/2", file_name=f"{i}.txt", file=b'test text')

        # Associated books with users

        ub1 = UserBook(user_id = user1.id, book_id = book1.id)
        ub2 = UserBook(user_id = user1.id, book_id = book2.id)

        ub4 = UserBook(user_id = user2.id, book_id = book2.id)
        ub5 = UserBook(user_id = user2.id, book_id = book3.id)
        ub3 = UserBook(user_id = user2.id, book_id = book4.id)

        self._save(db, [ub1, ub2, ub3, ub4, ub5])

    def _save(self, db, obj: list):
        for i in obj:
            db.add(i)
        db.commit()