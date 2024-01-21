from .Tags import Tags

from .Commands.ButtonsCommand import ButtonsCommand as Buttons, Button
from .Commands.NumberCommand import NumberCommand as Number
from .Commands.BooleanCommand import BooleanCommand as Boolean
from .Commands.TextCommand import TextCommand as Text
from .Commands.StringCommand import StringCommand as String

from .Actions import *

commands = [Text("info", lambda user: create_info(user, commands), tag=Tags.ignore),
    Text("start", lambda user: start(user, commands), tag=Tags.ignore),

    Text("list_books", list_books, Tags.book),
    # ToDo
    # Buttons("read", read, [[Button("previous"), Button("page", Button("next"))], Button("note")], tag=Tags.book),
    Number("set_book", set_book, 0, book_amount, tag=Tags.book, question=text_list_books),
    String("edit_book_name", edit_book_name, 250, get_book_name, format_result=True, tag=Tags.book),
    Number("delete_book", delete_book, 0, book_amount, tag=Tags.book, question=text_list_books),

    Number("page", set_page, 0, get_page_amount, tag=Tags.page, question=get_page_amount, format_result=True),

    Text("list_notes", list_notes, tag=Tags.note),
    String("note", create_note, 1000, tag=Tags.note),
    String("del_notes", delete_note, 500, tag=Tags.note, old_value=text_list_notes),

    Buttons("lang", set_language, [Button("ru", lang="ru"),
                        Button("en", lang="en")], update_lang=True, tag=Tags.setting),
    Number("chars_on_page", set_chars_on_page, 0, 4096, tag=Tags.setting),
    Boolean("remove_enters", set_remove_enters, tag=Tags.setting),
    Boolean("remove_dash", set_remove_dash, tag=Tags.setting)]


