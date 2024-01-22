from .Base import _get_user

def set_page(user_id, value):
    user = _get_user(user_id)
    _, text, images = user.page.get(value)
    return "succes"

def get_page_amount(user_id):
    user = _get_user(user_id)
    return user.book.page_amount()