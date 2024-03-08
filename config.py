from aiogram import Bot, Dispatcher
from decouple import config

TOKEN = config('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()
ADMIN = [517935907, 167495608, 465483170, 415378588, 1090237197]