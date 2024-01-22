from telethon import TelegramClient, events, sync
from telethon.tl.custom import Button
from os import environ

from BusinessLogic.Language.LanguageController import LanguageController
from BusinessLogic.UI.BaseEngine import BaseEngine
from BusinessLogic.UI.main import commands
from io import BytesIO


api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")
api_token = environ.get("TOKEN")

bot = TelegramClient('session_name', api_id, api_hash)

lang = LanguageController("ru")
engine = BaseEngine(commands, lang)



@bot.on(events.NewMessage())
async def command(event, button_command=[]):
    user = event.sender_id
    chat = event.chat_id

    if button_command:
        commands=[*button_command]
    elif event.message.message != "":
        command = event.message.message

        if command[0] != "/":
            return None
        
        command = command[1:]
        commands = [command]
    else:
        return 

    for i in commands:
        message = engine.command(user, i)
        commands.extend(engine.get_command_queue())

        await send_images(chat, message)

        if message.is_conversation:
            async with bot.conversation(event.sender_id) as conv:
                await conv.send_message(message.text)
                answer = await conv.get_response()
                result = engine.action(user, answer.text)

                if result.has_images():
                    await conv.send_file(result.images)
                if result.is_displayable():
                    await conv.send_message(result.text)
        else:
            await send_text_with_buttons(chat, message)


def _create_buttons(buttons, nesting_level=1):
    if nesting_level > 2:
            raise Exception("Too many nested buttons")

    result = []
    for i in buttons:
        if isinstance(i, list):
            buttons = _create_buttons(i, nesting_level+1)
            result.append(buttons)
        else:
            result.append(Button.inline(i["name"], bytes(i["id"], "utf-8")))

    return result

@bot.on(events.CallbackQuery())
async def buttons(event):
    user_command = event.data.decode("utf-8")
    user = event.sender_id
    chat = event.chat_id

    new_message = engine.button_handlers(user, user_command)

    if new_message.remove_buttons_from_previous_message:
        message = await event.get_message()
        await bot.edit_message(user, event.message_id, message.message)

    await send_images(chat, new_message)
    await send_text_with_buttons(chat, new_message)

    queue = engine.get_button_queue()
    if queue:
        await command(event, button_command = queue)    


@bot.on(events.NewMessage(func=lambda e: e.file))
async def file(event):
    user = event.sender_id
    file_info = event.file
    chat = event.chat_id

    uploader = engine.upload_book(user)

    status, message = uploader.check(file_info.ext, file_info.size)

    await send_images(chat, message)
    await send_text_with_buttons(chat, message)

    if status:
        file = BytesIO()
        await event.message.download_media(file)

        message = uploader.upload(file_info.name, file_info.ext, file)

        await send_images(chat, message)
        await send_text_with_buttons(chat, message)


async def send_text_with_buttons(chat, message):
    if message.is_displayable():
        if message.has_buttons():
            await bot.send_message(chat, message.text, buttons=_create_buttons(message.buttons))
        else:
            await bot.send_message(chat, message.text)

async def send_images(chat, message):
    if message.has_images():
        await bot.send_file(chat, message.images)

if __name__ == "__main__":
    bot.start(bot_token=api_token)
    bot.run_until_disconnected()

# python -m GUI.TelegramEngine