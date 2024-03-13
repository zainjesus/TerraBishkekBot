from config import bot
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from google_sheets.sheets import GoogleSheet
from keyboard.inline import reg_ik
from keyboard.reply import gender_kb
import datetime
import pyqrcode as qr
from database.stats_db import insert_user, get_all_users

router = Router()


class Registraion(StatesGroup):
    name = State()
    gender = State()
    age = State()
    number = State()
    niche = State()


@router.callback_query(F.data.startswith('reg'))
async def reg(call: CallbackQuery, state: FSMContext):
    gs = GoogleSheet()
    
    sheet = gs.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GoogleSheet.SPREADSHEET_ID, range='Наставничество!A:G').execute()  
    data = result.get('values', [])


    usernames = [row[1] for row in data] 

    if call.from_user.username is None:
        await bot.send_message(call.from_user.id, 'Чтобы зарегистрироваться на мероприятие, у вас должно быть задано'
                                ' "Имя пользователя" в телеграм! Зайдите в свой профиль, нажмите на "Имя пользователя"'
                                ' и задайте свое "Имя пользователя".')
    else:
        if f'@{call.from_user.username}' in usernames:
            indexes = [i for i, username in enumerate(usernames) if username == f'@{call.from_user.username}']
            index = indexes[-1]
            user_data = data[index]  

            await bot.send_message(call.message.chat.id, f'Вы уже зарегистрированы! Ваши данные:\n'
                                                        f'Имя: {user_data[0]}\n'
                                                        f'Номер телефона: {user_data[4]}\n'
                                                        f'Ниша: {user_data[5]}\n\n'
                                                        'Все верно?', reply_markup=reg_ik)  
        else:
            await state.set_state(Registraion.name)
            await bot.send_message(call.message.chat.id, 'Для регистрации нужно ответить всего на 3 вопроса')
            await bot.send_message(call.message.chat.id, '1️⃣ Напишите свою Фамилию и Имя (Пример: Иванов Иван)')


@router.callback_query(F.data.startswith('reapet_reg'))
async def reapet_reg(call: CallbackQuery, state: FSMContext):
    await state.set_state(Registraion.name)
    await bot.send_message(call.message.chat.id, 'Для регистрации нужно ответить всего на 5 вопросов')
    await bot.send_message(call.message.chat.id, '1️⃣ Напишите свою Фамилию и Имя (Пример: Иванов Иван)')


@router.callback_query(F.data.startswith('cancel_reg'))
async def cancel_reg(call: CallbackQuery, state: FSMContext):
    await bot.send_message(call.message.chat.id, "Отлично! Ждем вас 🤗")
    qr_code = qr.create(f'@{call.from_user.username}')
    qr_code.png('code.png', scale=6)
    photo = FSInputFile('code.png')
    await bot.send_photo(call.from_user.id, photo, caption='Ваш QR:')


@router.message(Registraion.name)
async def name_save(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, '2️⃣ Укажите свой пол', reply_markup=gender_kb)
    await state.set_state(Registraion.gender)


@router.message(Registraion.gender)
async def name_save(message: Message, state: FSMContext):
    if message.text.lower() not in ['мужской', 'женский']:
            await bot.send_message(message.from_user.id, "Укажите свой пол!")
    else:  
        await state.update_data(gender=message.text)
        await bot.send_message(message.from_user.id, '3️⃣ Укажите свой возраст', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registraion.age)


@router.message(Registraion.age)
async def name_save(message: Message, state: FSMContext):
    if len(message.text) > 4 or message.text.isalpha():
        await bot.send_message(message.from_user.id, "Укажите корректный возраст!")
    else:
        await state.update_data(age=message.text)
        await bot.send_message(message.from_user.id, '4️⃣ Напишите свой номер телефона (Пример: +966555555555)')
        await state.set_state(Registraion.number)

    
@router.message(Registraion.number)
async def number_save(message: Message, state: FSMContext):
    if len(message.text) < 9 or message.text.isalpha():
        await bot.send_message(message.from_user.id, 'Введён некорректный номер')
    else:
        await state.update_data(number=message.text)
        await bot.send_message(message.from_user.id, '5️⃣ Напишите свою нишу (Пример: Wildberries)')
        await state.set_state(Registraion.niche)


@router.message(Registraion.niche)
async def niche_save(message: Message, state: FSMContext):
    await state.update_data(niche=message.text)
    await bot.send_message(message.from_user.id, 'Cпасибо! Вы успешно зарегистрировались. Сейчас я пришлю вам QR-код, который нужно будет показать при входе.')
    qr_code = qr.create(f'@{message.from_user.username}')
    qr_code.png('code.png', scale=6)
    photo = FSInputFile('code.png')
    await bot.send_photo(message.from_user.id, photo, caption='Ваш QR:')
    await bot.send_message(message.from_user.id, '*Отлично! Добро пожаловать в Терру 🚀*\n\n'
                        '❗️Обязательно присоединяйтесь в общему чату участников. Там вы можете узнать все актуальные новости по поводу предстоящих мероприятий и не только! https://t.me/+U3qFrExcc19mZGMy\n\n'
                        'А также задавать вопросы и получать ответы напрямую от наставников!', parse_mode='Markdown')
    
    gs = GoogleSheet()
    data = await state.get_data()
    date = datetime.datetime.now().date()
    current_date = date.strftime("%d.%m.%Y")
    values = [[data.get('name'), f'@{message.from_user.username}', data.get('gender'), data.get('age'),
                data.get('number'), data.get('niche'), 'Зарегистрировался',
               current_date]]
    
    sheet = gs.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GoogleSheet.SPREADSHEET_ID, range='Наставничество!A:H').execute()
    num_rows = len(result.get('values', []))
    
    range_to_update = f'Наставничество!A{num_rows + 1}:H{num_rows + 1}'
    gs.updateRangeValues(range_to_update, values)
    
    last_cell = f'G{num_rows + 1}'
    gs.updateCellBackground(last_cell, "orange")
    await state.clear()

    groups = {
        "insta_official": "insta_official_reg",
        "insta_roman": "insta_roman_reg",
        "insta_nastavniki": "insta_nastavniki_reg",
        "insta_wb": "insta_wb_reg",
        "insta_sm": "insta_sm_reg",
        "insta_shodim": "insta_shodim_reg",
        "insta_repost": "insta_repost_reg",
        "tg_official": "tg_official_reg",
        "tg_chats": "tg_chats_reg",
        "tg_ataliev": "tg_ataliev_reg",
        "site": "site_reg",
        "whatsapp": "whatsapp_reg"
    }

    for group, reg_table in groups.items():
        users = await get_all_users(group)
        if message.from_user.id in users:
            await insert_user(reg_table, message.from_user.id)

