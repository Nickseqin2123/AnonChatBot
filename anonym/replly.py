import json

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inlines import inline


router = Router(name=__name__)


class ReplyMessageState(StatesGroup):
    message = State()
    
    
@router.callback_query(F.func(lambda x: json.loads(x.data).get('type') == 'reply'))
async def teply_toanon(callback: CallbackQuery, state: FSMContext):
    data = json.loads(callback.data)
    
    await callback.message.answer(
        text='''
🌈 Добро пожаловать! Здесь ты можешь поделиться своим мнением анонимно с человеком, который создал эту ссылку.

🖋 Напиши всё, что хочешь передать, и уже через несколько секунд это сообщение будет у него. Он не узнает, кто отправил!

Можно отправить фото, видео, 💬 текст, 🔊 голосовые сообщения, 📷 видеосообщения и даже ✨ стикеры. Ждем твое сообщение!
''')
    await state.set_state(ReplyMessageState.message)
    await state.update_data(id_person=data['id'], reply_id=data['reply_id'])


@router.message(ReplyMessageState.message)
async def get_msg(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    person_id = data['id_person']
    
    if message.text:
        msg = f'Тебе пришло новое анонимное сообщение!\n\n{message.text}'
        await message.bot.send_message(chat_id=person_id, text=msg, reply_markup=await inline(
            Ответить={'id': message.from_user.id, 'type': 'reply', 'reply_id': message.message_id}
            ), reply_to_message_id=data['reply_id'])
    else:
        cap = 'К тебе пришло новое анонимное сообщение!'
        await message.bot.copy_message(chat_id=person_id, from_chat_id=message.chat.id, message_id=message.message_id, caption=cap, reply_markup=await inline(
            Ответить={'id': message.from_user.id, 'type': 'reply', 'reply_id': message.message_id}
            ), reply_to_message_id=data['reply_id'])
    
    await message.answer(
            text='Твое сообщение было отправлено!'
        )