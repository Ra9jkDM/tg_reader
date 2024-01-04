from functools import wraps
from aiogram import types

from BusinessLogic.UI.TextQA import TextQA

def callback(func):
    @wraps(func)
    def get_user(callback: types.CallbackQuery, *args, **kwargs):
        id = str(callback.from_user.id)
        qa = TextQA(id)

        return func(qa, callback, *args, **kwargs)
    return get_user

def message(func):
    @wraps(func)
    def get_user(message: types.Message, *args, **kwargs):
        id = str(message.from_user.id)
        qa = TextQA(id)

        return func(qa, message, *args, **kwargs)
    return get_user

