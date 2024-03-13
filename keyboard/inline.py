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


services = InlineKeyboardMarkup(
    inline_keyboard=[
        [
           InlineKeyboardButton(text='Инстаграм', callback_data='insta_stats') 
        ],
        [
           InlineKeyboardButton(text='Телеграм', callback_data='tg_stats') 
        ],
        [
           InlineKeyboardButton(text='Сайт', callback_data='site_stats') 
        ],
        [
           InlineKeyboardButton(text='Ватсап', callback_data='whats_stats') 
        ],
        [
           InlineKeyboardButton(text='Просмотреть статистику за дни', callback_data='days') 
        ],
    ]
)



back_ik = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back')
        ]    
    ]
)

       