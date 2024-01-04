from telethon import TelegramClient, events, sync
from telethon.tl.custom import Button
from os import environ
from io import BytesIO

from BusinessLogic.UI.TextQA import TextQA
from .wraps import user

api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")
api_token = environ.get("TOKEN")

bot = TelegramClient('session_name', api_id, api_hash)

# Commands
# /start
# /set_lang
# /info


@bot.on(events.NewMessage(pattern='/start'))
@user
async def start(event, qa):
    if not qa.is_user_exists():
        qa.register_user()

        text, buttons = _set_lang(qa)
        await bot.send_message(event.chat_id, text, buttons=[buttons])

@bot.on(events.NewMessage(pattern='/info'))
@user
async def info(event, qa):
    await event.respond(qa.welcome())

@bot.on(events.NewMessage(pattern='/set_lang'))
@user
async def set_language(event, qa):
    text, buttons = _set_lang(qa)
    await bot.send_message(event.chat_id, text, buttons=[buttons])

def _set_lang(qa):
    text, lang = qa.choose_language()

    lang_buttons = [
        Button.inline(lang[0], b'set_lang_ru'),
        Button.inline(lang[1], b'set_lang_en')
    ]

    return text, lang_buttons

@bot.on(events.CallbackQuery(func=lambda e: e.data.startswith(b'set_lang')))
@user
async def set_lang(event, qa):
    lang = event.data.decode("utf-8")[-2:]
    notify = qa.set_language(lang)
    await bot.edit_message(event.sender_id, event.message_id, notify)
    await event.respond(qa.welcome())

@bot.on(events.NewMessage(pattern='/set_page'))
@user
async def set_language(event, qa):
    async with bot.conversation(event.sender_id) as c:
        await c.send_message("Set lang? [ru|en]")
        result = await c.get_response()
        await c.send_message("Your answer: "+result.text)


@bot.on(events.NewMessage(func=lambda e: e.file))
async def upload_book(event):
    print(dir(event.file))
    f = event.file
    print(f.name, f.ext, f.size)
    file = BytesIO()
    event.message.download_media(file)
    # path = await event.download_media()
    print('File saved to', file)

if __name__ == "__main__":
    bot.start(bot_token=api_token)
    bot.run_until_disconnected()



# python -m GUI.main