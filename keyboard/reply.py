from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


distribution_submit = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ДАЛЕЕ"),
            KeyboardButton(text="ОТМЕНИТЬ")
        ]
    ],
    resize_keyboard=True,
)


distribution_photo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Оставить без фото/видео")
        ],
        [
            KeyboardButton(text='ОТМЕНА')
        ]
    ],
    resize_keyboard=True,
)


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ОТМЕНА')
        ]
    ],
    resize_keyboard=True
)


gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мужской'),
            KeyboardButton(text='Женский')
        ]
    ],
    resize_keyboard=True
)


