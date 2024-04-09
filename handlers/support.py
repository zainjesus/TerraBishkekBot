from config import bot
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class SupportState(StatesGroup):
    message = State()

group = "-4129796963"

@router.callback_query(F.data.startswith('support'))
async def support(call: CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "Чем мы можем вам помочь? Напишите свой вопрос сюда")
    await state.set_state(SupportState.message)


@router.message(SupportState.message)
async def reply(message: Message):
    if message.from_user.username:
        await bot.send_message(group, f"@{message.from_user.username} задал(-а) вопрос:")
    else:
        await bot.send_message(group, f"{message.from_user.first_name} задал(-а) вопрос:")
    await bot.forward_message(chat_id=group,
                              from_chat_id=message.chat.id,
                              message_id=message.message_id)
    await bot.send_message(message.from_user.id, "Отлично! Ваше обращение передано нашему волонтеру, скоро он свяжется с вами"
                           " в телеграм!")



