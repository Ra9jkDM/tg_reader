from BusinessLogic.Database.main import Database
from BusinessLogic.Language.LanguageController import LanguageController
from ..Tags import Tags

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
    tag = Tags.ignore
    for i in commands:
        if i.tag == Tags.ignore:
            continue

        if tag != i.tag and i.tag != None:
            tag = i.tag
            info += f"\n\n{lang.get(tag.value)}"

        info += f"\n/{i.command} - {i.description(lang)}"

    return info