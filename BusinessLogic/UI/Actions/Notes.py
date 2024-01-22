from .Base import _get_user, get_language
from BusinessLogic.Language.LanguageController import LanguageController

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