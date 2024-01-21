from BusinessLogic.Database.main import Database
from BusinessLogic.Language.LanguageController import LanguageController
from .Tags import Tags

def _get_user(user_id):
    db = Database()
    return db.get_user(str(user_id))

def _register_user(user_id):
    db = Database()
    user = db.get_user(str(user_id))

    if not user:
        user = db.register_user(str(user_id))

    return user

def get_language(user_id):
    user = _get_user(user_id)

    if user:
        return user.preferences.language

def start(user_id, commands):
    _register_user(user_id)
    return create_info(user_id, commands)

def create_info(user_id, commands):
    lang_text = get_language(user_id)
    lang = LanguageController(lang_text)

    info = commands[0]

    info = info.description(lang).format(info.command)
    tag = None
    for i in commands:
        if i.tag == Tags.ignore:
            continue

        if tag != i.tag and i.tag != None:
            tag = i.tag
            info += f"\n\n{lang.get(tag.value)}"

        info += f"\n/{i.command} - {i.description(lang)}"

    return info

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
    pass

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



def set_page(user_id, value):
    pass

def get_page_amount(user_id):
    user = _get_user(user_id)
    return user.book.page_amount()


def list_notes(user_id):
    lang_text = get_language(user_id)
    lang = LanguageController(lang_text)

    text = lang.get("list_notes")
    text += text_list_notes(user_id)

    return text

def text_list_notes(user_id):
    user = _get_user(user_id)
    notes = sorted(user.note.get_all(), key=lambda x: x.page)

    result = ""
    for i in notes:
            result+= f"**{i.page}.** {i.text}\n"

    return result

def create_note(user_id, text):
    user = _get_user(user_id)
    user.note.create(text)

def delete_note(user_id, numbers):
    user = _get_user(user_id)

    notes = numbers.replace(' ', '').split(',')
    notes = list(map(int, notes))

    try:
        for i in notes:
            user.note.delete(i)
    except:
        pass

def set_language(user_id, lang):
    user = _get_user(user_id)
    user.preferences.language = lang

def set_chars_on_page(user_id, number):
    user = _get_user(user_id)
    user.preferences.chars_on_page = number

def set_remove_enters(user_id, value):
    user = _get_user(user_id)
    user.preferences.remove_enters = value

def set_remove_dash(user_id, value):
    user = _get_user(user_id)
    user.preferences.remove_dash = value