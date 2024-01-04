from functools import wraps
from BusinessLogic.UI.TextQA import TextQA

def user(func):
    @wraps(func)
    def get_user(event, *args, **kwargs):
        id = str(event.sender_id)
        qa = TextQA(id)

        return func(event, qa, *args, **kwargs)
    return get_user