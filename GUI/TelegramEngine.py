from telethon import TelegramClient, events, sync
from telethon.tl.custom import Button
from os import environ

from BusinessLogic.Language.LanguageController import LanguageController
from BusinessLogic.UI.BaseEngine import BaseEngine
from BusinessLogic.UI.main import commands

from .wraps import user


api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")
api_token = environ.get("TOKEN")

bot = TelegramClient('session_name', api_id, api_hash)

lang = LanguageController("ru")
engine = BaseEngine(commands, lang)


@bot.on(events.NewMessage())
@user
async def command(event, qa):
    command = event.message.message
    user = event.sender_id

    if command[0] != "/":
        return None
    
    command = command[1:]

    message = engine.command(user, command)

    if message["is_conversation"]:
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message(message["text"])
            answer = await conv.get_response()
            result = engine.action(user, answer.text)
            await conv.send_message(result)
    else:
        if message["buttons"]:
            buttons = _create_buttons(message["buttons"])
            await bot.send_message(event.chat_id, message["text"], buttons=buttons)
        else:
            await bot.send_message(event.chat_id, message["text"])


def _create_buttons(buttons):
    result = []
    for i in buttons:
        result.append(Button.inline(i[0], bytes(i[1], "utf-8")))
    return result

@bot.on(events.CallbackQuery())
@user
async def buttons(event, qa):
    command = event.data.decode("utf-8")
    user = event.sender_id

    text = engine.button_handlers(user, command)

    # Remove buttons on previous message
    message = await event.get_message()
    await bot.edit_message(event.sender_id, event.message_id, message.message)

    await bot.send_message(event.chat_id, text)


@bot.on(events.NewMessage(func=lambda e: e.file))
@user
async def file(event, qa):
    user = event.sender_id
    pass

if __name__ == "__main__":
    bot.start(bot_token=api_token)
    bot.run_until_disconnected()

# python -m GUI.TelegramEngine