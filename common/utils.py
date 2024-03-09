from config import bot
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await bot.send_message(message.from_user.id, "Отменено!", reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(message.from_user.id, "Такой команады нет!")