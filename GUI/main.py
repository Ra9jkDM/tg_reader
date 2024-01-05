from telethon import TelegramClient, events, sync
from telethon.tl.custom import Button
from os import environ
from io import BytesIO

from BusinessLogic.UI.TextQA import TextQA
from BusinessLogic.Database.Page import PageDTO
from .wraps import user

api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")
api_token = environ.get("TOKEN")

bot = TelegramClient('session_name', api_id, api_hash)

# Commands
# /start
# /info

# book
# /list_books
# /read
# /set_book
# /edit_book_name
# /delete_book

# page

# note

# preferences
# /set_lang
# /set_chars_on_page


@bot.on(events.NewMessage(pattern='/start'))
@user
async def start(event, qa):
    if not qa.is_user_exists():
        qa.register_user()

        await _set_lang(event, qa)

@bot.on(events.NewMessage(pattern='/info'))
@user
async def info(event, qa):
    await event.respond(qa.welcome())

@bot.on(events.NewMessage(pattern='/set_lang'))
@user
async def set_language(event, qa):
    await _set_lang(event, qa)

async def _set_lang(event, qa):
    text, lang = qa.choose_language()

    buttons = [
        Button.inline(lang[0], b'set_lang_ru'),
        Button.inline(lang[1], b'set_lang_en')
    ]

    await bot.send_message(event.chat_id, text, buttons=[buttons])

@bot.on(events.CallbackQuery(func=lambda e: e.data.startswith(b'set_lang')))
@user
async def set_lang(event, qa):
    lang = event.data.decode("utf-8")[-2:]
    notify = qa.set_language(lang)
    await bot.edit_message(event.sender_id, event.message_id, notify)
    await event.respond(qa.welcome())

@bot.on(events.NewMessage(pattern='/set_chars_on_page'))
@user
async def set_chars_on_page(event, qa):
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message(qa.chars_on_page())
        answer = await conv.get_response()
        result = qa.set_chars_on_page(answer.text)
        await conv.send_message(result)

@bot.on(events.NewMessage(func=lambda e: e.file))
@user
async def upload_book(event, qa):
    file_info = event.file
    result, answer = qa.check_book(file_info.ext, file_info.size)

    if not result:
        await event.respond(answer)
    else:
        file = BytesIO()
        await event.message.download_media(file)

        result = qa.upload_book(file_info.name, file_info.ext, file)
        await event.respond(result)

@bot.on(events.NewMessage(pattern='/list_books'))
@user
async def list_books(event, qa):
    await event.respond(qa.list_books())

@bot.on(events.NewMessage(pattern='/read'))
@user
async def read_book(event, qa):
    page = qa.read_book()
    await send_page(event, page, qa)

@bot.on(events.CallbackQuery(func=lambda e: e.data.startswith(b'page')))
@user
async def next(event, qa):
    if event.data == b'page_next':
        page = qa.get_next_page()
    else:
        page = qa.get_previous_page()

    await send_page(event, page, qa)


async def send_page(event, page, qa):
    message = await event.get_message()

    await bot.edit_message(event.sender_id, event.message_id, message.message)

    if isinstance(page, PageDTO):
        previous, next = qa.navigate_buttons()
        note = qa.note()

        if len(page.images) > 0:
            await bot.send_file(event.chat_id, page.images)
        await bot.send_message(event.chat_id, page.text,
                buttons=[
                    [
                        Button.inline(previous, b'page_previous'),
                        Button.inline(str(page.page_number)),
                        Button.inline(next, b'page_next')
                    ],
                    [Button.inline(note, b'create_note')]
                ])
    else:
        await bot.send_message(event.chat_id, page)


@bot.on(events.NewMessage(pattern='/set_book'))
@user
async def set_book(event, qa):
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message(qa.set_book_q())
        result = await conv.get_response()
        await conv.send_message(qa.set_book(result.text))

@bot.on(events.NewMessage(pattern='/edit_book_name'))
@user
async def edit_book_name(event, qa):
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message(qa.edit_book_name_q())
        result = await conv.get_response()
        await conv.send_message(qa.edit_book_name(result.text))

@bot.on(events.NewMessage(pattern='/delete_book'))
@user
async def delete_book(event, qa):
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message(qa.delete_book_q())
        result = await conv.get_response()
        await conv.send_message(qa.delete_book(result.text))


# @bot.on(events.NewMessage(pattern='/set_page'))
# @user
# async def set_language_v1(event, qa):
#     async with bot.conversation(event.sender_id) as c:
#         await c.send_message(qa.set_book_q())
#         result = await c.get_response()
#         await c.send_message(qa.set_book(result.text))


# @bot.on(events.NewMessage(func=lambda e: e.file))
# async def upload_book(event):
#     print(dir(event.file))
#     f = event.file
#     print(f.name, f.ext, f.size)
#     file = BytesIO()
#     event.message.download_media(file)
#     # path = await event.download_media()
#     print('File saved to', file)

if __name__ == "__main__":
    bot.start(bot_token=api_token)
    bot.run_until_disconnected()



# python -m GUI.main