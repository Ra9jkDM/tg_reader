from .Base import _get_user, get_language
from BusinessLogic.Language.LanguageController import LanguageController

def list_books(user_id):
    lang_text = get_language(user_id)
    lang = LanguageController(lang_text)

    text = lang.get("book_list")
    text += text_list_books(user_id)
    
    return text

def _book_list_text(books):
    text = ""

    for i, book in enumerate(books, start=1):
        text += f"**{i}.** [{book.bookmark}/{book.number_of_pages}] {book.name}\n"

    return text

def read(user_id):
    user = _get_user(user_id)
    _, text, images = user.page.get_current()
    if len(text) == 0:
        text = "_"
    return text, images

def get_next_page(user_id):
    user = _get_user(user_id)
    _, text, images = user.page.get_next_part()
    if len(text) == 0:
        text = "_"
    return text, images

def get_previous_page(user_id):
    user = _get_user(user_id)
    _, text, images = user.page.get_previous_part()
    if len(text) == 0:
        text = "_"
    return text, images

def get_page_number(user_id):
    user = _get_user(user_id)
    number = user.page.get_bookmark()
    return number


def book_amount(user_id):
    user = _get_user(user_id)
    return len(user.book.get_all())

def text_list_books(user_id):
    lang_text = get_language(user_id)
    lang = LanguageController(lang_text)

    user = _get_user(user_id)

    books = user.book.get_all()
    text = _book_list_text(books)
    
    return text

def set_book(user_id, value):
    user = _get_user(user_id)
    user.book.set(value)

def edit_book_name(user_id, value):
    user = _get_user(user_id)
    user.book.edit_name(value)

def get_book_name(user_id):
    user = _get_user(user_id)
    return user.book.get_name()

def delete_book(user_id, value):
    user = _get_user(user_id)
    user.book.delete()