from .Base import _get_user

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