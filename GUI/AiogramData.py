from os import environ
from .AiogramWraps import message, callback

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import BinaryIO

TOKEN = environ.get('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# commands
# /start
# /set_lang
# /info

@dp.message(Command('start'))
@message
async def start(qa, message):
    if qa.is_user_exists():
        await message.answer(qa.welcome())
    else:
        qa.register_user()

        lang, buttons = _set_lang(qa, message)
        await message.answer(lang, reply_markup = buttons.as_markup())

@dp.message(Command('set_lang'))
@message
async def set_lang(qa, message):
    lang, buttons = _set_lang(qa, message)
    await message.answer(lang, reply_markup = buttons.as_markup())

def _set_lang(qa, message):
    qa_lang, buttons = qa.choose_language()

    lang = InlineKeyboardBuilder()

    lang.add(types.InlineKeyboardButton(text=buttons[0], callback_data="set_lang_ru"))
    lang.add(types.InlineKeyboardButton(text=buttons[1], callback_data="set_lang_en"))

    return qa_lang, lang


@dp.callback_query(F.data == "set_lang_ru")
@callback
async def set_lang_ru(qa, callback):
    notify =  qa.set_language("ru")
    await callback.message.edit_text(notify)
    await callback.message.answer(qa.welcome())

@dp.callback_query(F.data == "set_lang_en")
@callback
async def set_lang_ru(qa, callback):
    notify = qa.set_language("en")
    await callback.message.edit_text(notify)
    await callback.message.answer(qa.welcome())


@dp.message(Command('info'))
@message
async def info(qa, message):
    await message.answer(qa.welcome())


def _bytes_to_mbytes(bytes_value):
    return bytes_value/(1024*1024)


### !!!!!! Aiogram ограничение в 20MB на загрузку файлов


@dp.message()
@message
async def upload_book(qa, message):
    doc = message.document
    print(doc)
    # file = await bot.get_file(doc.file_id)
    # file_path = file.file_path

    if _bytes_to_mbytes(doc.file_size) < 51:
        # result: BinaryIO = await bot.download_file(file_path)
        # result = await bot.download(doc)
        doc.download()
        print(result)
        qa.upload_book(doc.file_name, result)
    else:
        await message.answer(qa.heavy_file())
