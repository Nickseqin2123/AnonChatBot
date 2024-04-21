import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


bot = Bot(token="6998135939:AAGQw-daNhXFgQeQzlm5eaDhfiOz_TdHbMQ")
dp = Dispatcher()


class MessageUser(StatesGroup):
    messag = State()
    

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    mess = message.text.split()
    if len(mess) == 1 and message.text.split()[0] == r"/start":
        await message.answer(
            text=f"""Привет, я бот для анониминых сообщений.
Вот твоя реферальныя ссылка ->
t.me/anonimn_chat_cheb_bot?start={message.from_user.id}
Размести ее у себя в профиле и получай анонимные сообщения."""
                )
    else:
        if mess[0] == r"/start" and mess[-1].isdigit():
            await state.update_data(another=mess[-1])
            await state.set_state(MessageUser.messag)
            await message.answer(
                text="Напишите сообщение или отправте фото, которое увидит другой пользователь:"
                )
        


@dp.message(MessageUser.messag)
async def mess(message: Message, state: FSMContext):
    await state.update_data(mes=message.text)
    data = await state.get_data()
    await state.clear()
    
    await summary(message, data)


async def summary(message: Message, data: dict):
    await bot.send_message(
        int(data["another"]), 
        text=f"""Тебе отправили анонимное сообщение:
        
{data["mes"]}""")
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Отправить еще",
            callback_data=f"{data["another"]}"
        )
    )
    await message.answer(
        text="Сообщение отправлено! Хотите отправить еще?",
        reply_markup=builder.as_markup()
    )


@dp.callback_query()
async def call_bck(callback: CallbackQuery, state: FSMContext):
    await state.update_data(another=callback.data)
    await state.set_state(MessageUser.messag)
    await callback.message.answer(
        text=f"Напишите сообщение или отправте фото, которое увидит другой пользователь:"
    )
    

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token="6998135939:AAGQw-daNhXFgQeQzlm5eaDhfiOz_TdHbMQ")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())