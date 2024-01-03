from Database.session import session
from Database.model import *
from FileStorage.MinIO import MinIO

id_1 = "99888"
id_2 = "222322"
id_3 = "-999" # unknown_user

class Data:
    long_text = '''Returns the result of calling the first argument, which
	must be a function, with the remaining arguments as parameters.
	Thus "call .X.Y 1 2" is, in Go notation, dot.X.Y(1, 2) where
	Y is a func-valued field, map entry, or the like.
	The first argument must be the result of an evaluation
	that yields a value of function type (as distinct from
	a predefined function such as print). The function must
	return either one or two result values, the second of which
	is of type error. If the arguments don't match the function
	or the returned error value is non-nil, execution stops.'''

    long_text2 = '''When SQLAlchemy issues a single INSERT statement, to fulfill the contract of having the “last insert identifier” available, a RETURNING clause is added to the INSERT statement which specifies the primary key columns should be returned after the statement completes. The RETURNING functionality only takes place if PostgreSQL 8.2 or later is in use. As a fallback approach, the sequence.'''

    def create(self):
        try:
            self._create_data()
        except:
            pass

    @session
    def _create_data(self, db):
        # create Users
        user1 = User(social_id=id_1, preferences={CHARS_ON_PAGE: 100}, current_book=2)
        user2 = User(social_id=id_2, preferences={}, current_book=4)

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
        page33 = Page(book_id=book2.id, page_number=33, text=self.long_text, number_of_images=0)
        page34 = Page(book_id=book2.id, page_number=34, text=self.long_text2, number_of_images=0)
        page35 = Page(book_id=book2.id, page_number=35, text="s35 text__text_123.", number_of_images=0)
        page36 = Page(book_id=book2.id, page_number=36, text="end", number_of_images=0)

        self._save(db, [page1, page2, page30, page31, page32, page33, page34, page35, page36])

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

        # Create notes

        note1 = Note(user_id=user1.id, book_id=book2.id, page=1, text="Morbi condimentum feugiat luctus")
        note2 = Note(user_id=user1.id, book_id=book2.id, page=2, text="Second note")
        note3 = Note(user_id=user1.id, book_id=book2.id, page=31, text="3note")
        note4 = Note(user_id=user1.id, book_id=book2.id, page=32, text="4-test-note")
        
        note_x = Note(user_id=user1.id, book_id=book1.id, page=20, text="x-test-note")

        self._save(db, [ub1, ub2, ub3, ub4, ub5, note1, note2, note3, note4, note_x])

    def _save(self, db, obj: list):
        for i in obj:
            db.add(i)
        db.commit()