from telethon import TelegramClient, events, sync
from os import environ
from functools import wraps
from io import BytesIO

from BusinessLogic.UI.TextQA import TextQA

api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")
api_token = environ.get("TOKEN")

bot = TelegramClient('session_name', api_id, api_hash)

# Commands
# /start
# /set_lang
# /info

def user(func):
    @wraps(func)
    def get_user(event, *args, **kwargs):
        id = str(event.sender_id)
        qa = TextQA(id)

        return func(event, qa, *args, **kwargs)
    return get_user

@bot.on(events.NewMessage(pattern='/start'))
@user
async def handler(event, qa):
    await event.respond('Hey!')
    await event.respond(qa.welcome())

@bot.on(events.NewMessage(pattern='/set_lang'))
@user
async def handler(event, qa):
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