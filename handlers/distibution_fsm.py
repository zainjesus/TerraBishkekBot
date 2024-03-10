from config import bot
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboard.reply import distribution_submit, distribution_photo, cancel
from database.db import sql_command_all
from config import ADMIN
from aiogram.types import Message, ReplyKeyboardRemove



router = Router()

class Distribution(StatesGroup):
    message = State()
    photo_or_video = State()
    submit = State()


@router.message(Command('send_message'))
async def send_message(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN and message.chat.type == 'private':
        await bot.send_message(message.from_user.id, "Данный бот доступен только для администраторов Terra!")
    elif message.chat.type == 'private':
        await state.set_state(Distribution.message)
        await bot.send_message(message.from_user.id, "Введите сообщение, которое хотите разослать", reply_markup=cancel)


@router.message(Distribution.message)
async def message_save(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(message=message.text)
        await bot.send_message(message.from_user.id, 'Если хотите прикрепить к сообщению фотографию/видео, отправьте'
                                                     ' ее/его мне\n(только одно фото/видео)',
                                                     reply_markup=distribution_photo)
        await state.set_state(Distribution.photo_or_video)
    else:
        await bot.send_message(message.from_user.id, "На этом этапе можно только ввести текст!")


@router.message(Distribution.photo_or_video)
async def photo_save(message: Message, state: FSMContext):
    if message.text == "Оставить без фото/видео":
        await state.set_state(Distribution.submit)
        await bot.send_message(message.from_user.id, 'Чтобы разослать это сообщение, нажмите "ДАЛЕЕ"',
                               reply_markup=distribution_submit)
    elif message.photo:
        await state.update_data(photo_or_video=message.photo[-1].file_id)
        await bot.send_message(message.from_user.id, 'Чтобы разослать это сообщение, нажмите "ДАЛЕЕ"',
                               reply_markup=distribution_submit)
        await state.set_state(Distribution.submit)
    elif message.video:
        await state.update_data(photo_or_video=message.video.file_id)
        await bot.send_message(message.from_user.id, 'Чтобы разослать это сообщение, нажмите "ДАЛЕЕ"',
                               reply_markup=distribution_submit)
        await state.set_state(Distribution.submit)
    else:
        await bot.send_message(message.from_user.id, "На этом этапе можно только прикрепить фото!")


@router.message(Distribution.submit)
async def submit(message: Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        data = await state.get_data()
        user_message = data.get('message')
        user_photo_or_video = data.get('photo_or_video')
        users = await sql_command_all()
        await bot.send_message(message.from_user.id, "Сообщение успешно разослано!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        for i in users:
            try:
                if user_photo_or_video:
                    try:
                        await bot.send_photo(i, photo=user_photo_or_video, caption=user_message)
                    except:
                        await bot.send_video(i, video=user_photo_or_video, caption=user_message)
                else:
                    await bot.send_message(i, user_message)
            except Exception as e:
                print(f"Error sending message to user {i}: {e}")
                continue
    elif message.text == "ОТМЕНИТЬ":
        await bot.send_message(message.from_user.id, "Рассылка отменена!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Нажмите "ДАЛЕЕ" или "ОТМЕНИТЬ"')