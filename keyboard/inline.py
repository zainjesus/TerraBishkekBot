from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_ik = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Что такое Терра? 🗂', callback_data='wit')
        ],
        [
            InlineKeyboardButton(text='Зарегистрироваться на 9 поток', callback_data='reg')
        ],
        [
            InlineKeyboardButton(text='Ознакомиться с наставниками', url='https://terra-bishkek.kg/')
        ],
    ]
)


reg_ik = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да ✅', callback_data='cancel_reg'),
            InlineKeyboardButton(text='Изменить ⬅️', callback_data='reapet_reg')
        ],

    ]
)



       