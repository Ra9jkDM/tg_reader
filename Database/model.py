from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey, select, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, mapped_column, Mapped, relationship, backref

USERNAME = environ.get("DATABASE_USERNAME") 
PASSWORD = environ.get("DATABASE_PASSWORD")

HOST = environ.get("DATABASE_HOST")
PORT = int(environ.get("DATABASE_PORT"))

DATABASE = environ.get("DATABASE_NAME")
DIALECT = environ.get("DATABASE_DIALECT")


ENGINE = create_engine(f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}") #, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    preferences: Mapped[JSON] = mapped_column(JSON, nullable=True)
    current_book: Mapped[int] = mapped_column(Integer, nullable=True)

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    # user: Mapped[int] = mapped_column(Integer)

    # name: Mapped[String] = mapped_column(String(250), nullable=False)
    number_of_pages: Mapped[int] =  mapped_column(Integer, nullable=False)

# ToDo переписать все!!! Составить нормальную БД
# Кол-во страниц и "статус прочтения" книги хранить в отдельных таблицах
# + таблица Пользователь - Загруженные книги
# создать структуру БД и протестить в работе в MySQL
