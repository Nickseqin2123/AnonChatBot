import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from db.config import cfg
from requestsdb.user import getUserLink, setUser


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    text = message.text.split('/start')
    
    if len(text) > 1:
        await message.answer(
            text='Напишите ему сообщение'
        )  
    else:
        user_id = message.from_user.id
        
        user = await getUserLink(user_id)
        
        if isinstance(user, bool):
            await setUser(user_id)
        
        user = await getUserLink(user_id)
        
        await message.answer(
            text=f'''
    Привет, я бот для анонимных сообщений. Вот твоя ссылка: https://t.me/anonimn_chat_cheb_bot?start={user}
    Выложи её в свой канал или добавь в описание, чтобы получать анонимные вопросы.
    Все данные конфиденциальны'''
        )


async def main():
    bot = Bot(token=cfg.token)
    logging.basicConfig(level=logging.INFO)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())