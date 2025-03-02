import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.config import cfg
from requestsdb.user import getUserLink, setUser, searchUser
from keyboards.inlines import inline
from anonym.replly import router as reply_router


dp = Dispatcher()
dp.include_router(reply_router)


class MessageState(StatesGroup):
    message = State()
    

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    msg_args = message.text.split(maxsplit=1)

    if len(msg_args) > 1:
        await state.set_state(MessageState.message)
        
        hash_other = msg_args[-1]
        await state.update_data(hash_person=hash_other)
        
        await message.answer(
            text='Напишите сообщение или отправьте фото'
        )
    else:
        user_id = message.from_user.id
        
        user = await getUserLink(user_id)
        
        if isinstance(user, bool):
            await setUser(user_id)
        
        user = await getUserLink(user_id)
        
        await message.answer(
            text=f'''
🌟 Время получать анонимные вопросы! Начните прямо сейчас!

👉 t.me/sipsbe_bot?start={user}

Не забудьте разместить эту ссылку ☝️ в описании своего профиля в Telegram, TikTok или Instagram (stories), чтобы ваши подписчики могли смело писать вам 💬. Откройте новые возможности общения!'''
        )


@dp.message(MessageState.message)
async def gt_message(message: Message, state: FSMContext):
    data = await state.get_data()
    person = data['hash_person']
    
    await state.clear()
    user_id = await searchUser(person)
    
    if message.text:
        msg = f'Тебе пришло новое анонимное сообщение!\n\n{message.text}'
        await message.bot.send_message(chat_id=user_id, text=msg, reply_markup=await inline(
            Ответить={'id': message.from_user.id, 'type': 'reply', 'reply_id': message.message_id}
            ))
    else:
        cap = 'К тебе пришло новое анонимное сообщение!'
        await message.bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id, caption=cap, reply_markup=await inline(
            Ответить={'id': message.from_user.id, 'type': 'reply', 'reply_id': message.message_id}
            ))
    
    await message.answer(
            text='Твое сообщение было отправлено!'
    )
    

async def main():
    bot = Bot(token=cfg.token)
    logging.basicConfig(level=logging.INFO)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())