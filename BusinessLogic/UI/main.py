from .Tags import Tags

from .Commands.ButtonsCommand import ButtonsCommand as Buttons, Button
from .Commands.NumberCommand import NumberCommand as Number
from .Commands.BooleanCommand import BooleanCommand as Boolean
from .Commands.TextCommand import TextCommand as Text
from .Commands.StringCommand import StringCommand as String
from .Commands.PageCommand import PageCommand as Page

import BusinessLogic.UI.Actions.Base as Base
import BusinessLogic.UI.Actions.Books as Books
import BusinessLogic.UI.Actions.Notes as Notes
import BusinessLogic.UI.Actions.Pages as Pages
import BusinessLogic.UI.Actions.Settings as Settings

commands = [Text("info", lambda user: Base.create_info(user, commands), tag=Tags.ignore),
    Text("start", lambda user: Base.start(user, commands), tag=Tags.ignore),

    Text("list_books", Books.list_books, tag=Tags.book),
    Page("read", Books.read, answers=[[Button("previous", function=Books.get_previous_page), 
                                       Button("page", text=Books.get_page_number, command_queue=["page"]), 
                                       Button("next", function=Books.get_next_page)], 
                                      [Button("note", command_queue=["note"], remove_buttons_from_previous_message=False)]],
                                      content=Books.read, tag=Tags.book),
    Number("set_book", Books.set_book, min_limit=0, max_limit=Books.book_amount, question=Books.text_list_books, tag=Tags.book),
    String("edit_book_name", Books.edit_book_name, char_limit=250, old_value=Books.get_book_name, 
                                                                format_result=True, tag=Tags.book),
    Number("delete_book", Books.delete_book, min_limit=0, max_limit=Books.book_amount, 
                                            question=Books.text_list_books, tag=Tags.book),

    Number("page", Pages.set_page, min_limit=0, max_limit=Pages.get_page_amount, question=Pages.get_page_amount, 
                                                        format_result=True, command_queue=["read"], tag=Tags.page),

    Text("list_notes", Notes.list_notes, tag=Tags.note),
    String("note", Notes.create_note, char_limit=1000, tag=Tags.note),
    String("del_notes", Notes.delete_note, char_limit=500, old_value=Notes.text_list_notes, tag=Tags.note),

    Buttons("lang", Settings.set_language, answers=[Button("ru", lang="ru"),
                                                    Button("en", lang="en")], 
                                        update_lang=True, tag=Tags.setting),
    Number("chars_on_page", Settings.set_chars_on_page, min_limit=0, max_limit=4096, tag=Tags.setting),
    Boolean("remove_enters", Settings.set_remove_enters, tag=Tags.setting),
    Boolean("remove_dash", Settings.set_remove_dash, tag=Tags.setting)]


