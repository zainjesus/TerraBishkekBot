from aiogram import Router, F
from aiogram.filters import Command
from config import bot
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from keyboard.inline import start_ik
from database.db import sql_command_insert


router = Router()


@router.message(Command('start'))
async def start(message: Message):
    image = FSInputFile('media/terra.jpeg')
    await bot.send_photo(message.from_user.id, image, caption='Привет! Добро пожаловать в чат-бот бизнес-клуба *Терра Бишкек.*\n\n'
                         'У нас сообщество сильных предпринимателей, объединённых идеей достичь всеобщего благополучия. Все продукты и мероприятия клуба бесплатные!\n\n'
                         'Здесь тебя ждёт:\n\n'
                         '*❤️‍🔥Запуск наставничества от TERRA🤩*\n'
                         '_Сильные предприниматели будут на протяжении 2-х месяцев помогать участникам достичь целей, увеличить показатели бизнеса, или запустить бизнес._\n\n'
                         'А также много других направлений на бесплатной основе:\n\n'
                         '▪️обучающие встречи с ТОПовыми экспертами-предпринимателями;\n'
                         '▪️мастермайнды;\n'
                         '▪️бизнес-завтраки, нетворкинги, бизнес-ужины;\n'
                         '▪️бизнес-игры.\n\n'
                         '*Расти и развивай наше комьюнити 🚀*\n\n'
                         'Выбирай по кнопке ниже мероприятие на которое хочешь зарегистрироваться 👇',
                         parse_mode='Markdown',
                         reply_markup=start_ik)
    await sql_command_insert(message.from_user.id)
    

@router.callback_query(F.data.startswith("wit"))
async def wita(call: CallbackQuery):
    media = []
    for i in range(1, 7):
        image = FSInputFile(f'media/wit_{i}.jpg')
        media.append(InputMediaPhoto(media=image))
    await bot.send_media_group(call.message.chat.id, media)
    await bot.send_message(call.message.chat.id, '*О ПРОЕКТЕ*\n\n'
                                'Бизнес-клуб «TERRA» — некоммерческая организация, объединяющая предпринимателей, желающих менять себя и мир вокруг.\n\n'
                                'Любые знания, связи и опыт в нашем клубе все получают абсолютно бесплатно. Неважно, на какой стадии находится развитие твоего бизнеса — при желании и системности ты получишь многократное ускорение своего роста.\n\n'
                                'Основным инструментом достижения участниками новых показателей является бесплатное наставничество — каждые два месяца проходит новый набор на обучение.\n\n'
                                'Также у нас есть кейсы, с которыми вы можете ознакомиться здесь: https://club-terra.ru/cases/',
                                parse_mode='Markdown')
    video = FSInputFile('media/terra_video.mp4')
    await bot.send_video(call.message.chat.id, video, caption='Короткое видео о *Терре*', parse_mode='Markdown')