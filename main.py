import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from db.config import cfg


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text='Бот анон'
    )


async def main():
    bot = Bot(token=cfg.token)
    logging.basicConfig(level=logging.INFO)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())