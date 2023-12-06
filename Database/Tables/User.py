from ..session import session, getEngine

from ..model import User as DBUser, Book as DBBook, UserBook

from .Book import CreateBook, Book


class User:
    def __init__(self, id: str):
        self._id = id
       
    @session
    def isNewUser(self, db):
        self._get_user(db)

        if self._user:
            return False
        return True

    @session
    def registerNewUser(self, db):
        db.add(DBUser(social_id = self._id))
        db.commit()

    # TODO
    def addBook(self):
        return CreateBook

    @session
    def getBooks(self, db):
        self._get_user(db)
        books = self._user.books
        book_list =[]

        for i in books:
            book_list.append(Book(i, self._user))
        
        return book_list

    # TODO
    def deleteBook(self, id):
        pass

    def _get_user(self, db):
        self._user = db.query(DBUser).filter(DBUser.social_id == self._id).first()

if __name__ == "__main__":
    user = User("123")
    book = user.addBook()

    book("Book name")
    book.bind(user)
    for _ in range(10):
        book.addPage("", 0)

    books = user.getBooks()

    book = books[0]
    print(book.name, book.bookmark, book.numberOfPages) # All statistic
    page = book.getPage(book.bookmark)
    print(page.text) # Get page
    book.bookmark+=1 # Navigation
    page.addNote("Some text") # Add note

    notes = book.getNotes() # Get notes
    for i in notes:
        print(i.page, i.text)
        i.text += "some value" # Edit note
    notes[1].delete() # delete note

# ToDo 'create' VS 'add'
