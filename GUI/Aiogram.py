import asyncio
from aiogram import Bot, Dispatcher

from .AiogramData import bot, dp


async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())

# python -m GUI.Aiogram