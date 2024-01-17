from telethon import TelegramClient, events, sync
from telethon.tl.custom import Button
from os import environ

from .wraps import user

from BusinessLogic.UI.Preferenses import init, lang, mas, Buttons

api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")
api_token = environ.get("TOKEN")

bot = TelegramClient('session_name', api_id, api_hash)

init(lang)

@bot.on(events.NewMessage())
@user
async def command(event, qa):
    command = event.message.message

    if command[0] != "/":
        # await bot.send_message(event.chat_id, "Fix unknown command")
        return None
    
    command = command[1:]

    for i in mas:
        if i.check(command):
            text = i.response(command)

            if issubclass(type(i), Buttons):
                buttons = i.get_buttons()
                buttons = _create_buttons(buttons)

                await bot.send_message(event.chat_id, text, buttons=buttons)
            else:
                async with bot.conversation(event.sender_id) as conv:
                    await conv.send_message(text)
                    answer = await conv.get_response()
                    result = i.action(answer.text)
                    await conv.send_message(result)

    # else: # Fix
    #     await bot.send_message(event.chat_id, "Fix unknown command")

def _create_buttons(buttons):
    result = []
    for i in buttons:
        result.append(Button.inline(i[0], bytes(i[1], "utf-8")))
    return result

@bot.on(events.CallbackQuery())
@user
async def buttons(event, qa):
    command = event.data.decode("utf-8")

    for i in mas:
        if i.check(command):
            text = i.response(command)

            # Remove buttons on previous message
            message = await event.get_message()
            await bot.edit_message(event.sender_id, event.message_id, message.message)

            await bot.send_message(event.chat_id, text)

@bot.on(events.NewMessage(func=lambda e: e.file))
@user
async def file(event, qa):
    pass

if __name__ == "__main__":
    bot.start(bot_token=api_token)
    bot.run_until_disconnected()

# python -m GUI.main2_test