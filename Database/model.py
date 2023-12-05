from __future__ import annotations
from typing import Final, List

from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey, select, Boolean, JSON, Index
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, mapped_column, Mapped, relationship, backref
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import text

from os import environ

USERNAME: Final = environ.get("DATABASE_USERNAME") 
PASSWORD: Final = environ.get("DATABASE_PASSWORD")

HOST: Final = environ.get("DATABASE_HOST")
PORT: Final = int(environ.get("DATABASE_PORT")) # type: ignore

DATABASE: Final = environ.get("DATABASE_NAME")
DIALECT: Final = environ.get("DATABASE_DIALECT")

def get_engine(postfix=""):
    return create_engine(f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE+postfix}") #, echo=True)

ENGINE = get_engine()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)

    social_id: Mapped[String] = mapped_column(String(15), unique=True, nullable=False)
    preferences: Mapped[JSON] = mapped_column(MutableDict.as_mutable(JSON), nullable=True)

    books: Mapped[List["UserBook"]] = relationship("UserBook", back_populates="user", cascade="all, delete", passive_deletes=True)
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="user", cascade="all, delete", passive_deletes=True)

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)

    name: Mapped[String] = mapped_column(String(250), nullable=False)
    number_of_pages: Mapped[int] =  mapped_column(Integer, nullable=False)

    pages: Mapped[List["Page"]] = relationship("Page", back_populates="book", cascade="all, delete", passive_deletes=True)
    users: Mapped[List["UserBook"]] = relationship("UserBook", back_populates="book", cascade="all, delete", passive_deletes=True)
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="book", cascade="all, delete", passive_deletes=True)

class Page(Base):
    __tablename__ = "page"

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)
    page_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    text: Mapped[String] = mapped_column(String(2000), nullable=True)
    number_of_images: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    book: Mapped["Book"] = relationship("Book", back_populates="pages")

class UserBook(Base):
    __tablename__ = "user_book"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)

    bookmark: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    number_of_chars: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="books")
    book: Mapped["Book"] = relationship("Book", back_populates="users")

class Note(Base):
    __tablename__ = "note"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)
    page: Mapped[int] = mapped_column(Integer, primary_key=True)

    text: Mapped[String] = mapped_column(String(1000), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="notes")
    book: Mapped["Book"] = relationship("Book", back_populates="notes")


def create_db(engine=ENGINE):
    Base.metadata.create_all(bind=engine)
 
    # page_index = Index("idx_page", Page.book_id, Page.page_number)
    with Session(autoflush=True, bind=ENGINE) as db:
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_page ON page (book_id, page_number);"))

def delete_db(engine=ENGINE):
    Base.metadata.drop_all(bind=engine)

    # page_index.drop(bind=engine)
    with Session(autoflush=True, bind=ENGINE) as db:
        db.execute(text("DROP INDEX IF EXISTS idx_page;"))
        db.commit()


if __name__ == "__main__":
    create_db()
    # delete_db()

