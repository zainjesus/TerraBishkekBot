from aiogram import Router, F
from aiogram.filters import Command
from config import bot
from aiogram.types import Message, CallbackQuery
from keyboard.inline import services, back_ik
from database.db import sql_command_all
from google_sheets.sheets import GoogleSheet
from database.stats_db import get_all_users
from collections import defaultdict


router = Router()


@router.message(Command('stats'))
async def stats(message: Message):
    gs = GoogleSheet()
    
    sheet = gs.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GoogleSheet.SPREADSHEET_ID, range='Наставничество!A:A').execute() 
    data = result.get('values', [])


    users = await sql_command_all()
    await bot.send_message(message.from_user.id, f'Общее количество пользователей - {len(users)}\n'
                           f'Пользователей зарегистрировались - {len(data)-1}\n\n'
                           'Выберите откуда хотите просмотреть статистику'
                           ,reply_markup=services)


@router.callback_query(F.data.startswith('back'))
async def stats(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    gs = GoogleSheet()
    
    sheet = gs.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GoogleSheet.SPREADSHEET_ID, range='Наставничество!A:A').execute() 
    data = result.get('values', [])


    users = await sql_command_all()
    await bot.send_message(call.from_user.id, f'Общее количество пользователей - {len(users)}\n'
                           f'Пользователей зарегистрировались - {len(data)-1}\n\n'
                           'Выберите откуда хотите просмотреть статистику', reply_markup=services)
    


@router.callback_query(F.data.startswith('insta_stats'))
async def insta_stats(call: CallbackQuery):
    labels = [
        ('official_page', 'insta_official', 'insta_official_reg'),
        ('roman_marketing', 'insta_roman', 'insta_roman_reg'),
        ('nastavniki', 'insta_nastavniki', 'insta_nastavniki_reg'),
        ('wb', 'insta_wb', 'insta_wb_reg'),
        ('sm', 'insta_sm', 'insta_sm_reg'),
        ('shodim', 'insta_shodim', 'insta_shodim_reg'),
        ('repost', 'insta_repost', 'insta_repost_reg')
    ]

    message_text = ""
    for label, group, reg_table in labels:
        users = await get_all_users(group)
        reg_users = await get_all_users(reg_table) if reg_table else None
        message_text += f"Зашли по метке {label} - {len(users)}"
        if reg_users is not None:
            message_text += f"\nЗарегистрировались по метке {label} - {len(reg_users)}"
        message_text += "\n\n"

    await bot.send_message(call.from_user.id, message_text, reply_markup=back_ik)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@router.callback_query(F.data.startswith('tg_stats'))
async def tg_stats(call: CallbackQuery):
    labels = [
        ('official_page', 'tg_official', 'tg_official_reg'),
        ('chats', 'tg_chats', 'tg_chats_reg'),
        ('ataliev', 'tg_ataliev', 'tg_ataliev_reg')
    ]

    message_text = ""
    for label, group, reg_table in labels:
        users = await get_all_users(group)
        reg_users = await get_all_users(reg_table) if reg_table else None
        message_text += f"зашли по метке {label} - {len(users)}"
        if reg_users is not None:
            message_text += f"\nЗарегистрировались по метке {label} - {len(reg_users)}"
        message_text += "\n\n"

    await bot.send_message(call.from_user.id, message_text, reply_markup=back_ik)
    await bot.delete_message(call.message.chat.id, call.message.message_id)



@router.callback_query(F.data.startswith('site_stats'))
async def site_stats(call: CallbackQuery):
    site = await get_all_users('site')
    site_reg = await get_all_users('site_reg')
    await bot.send_message(call.from_user.id, f"Зашли по метке website - {len(site)}\n"
                           f"Зарегистрировались по метке website - {len(site_reg)}"
                           ,reply_markup=back_ik)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


    
@router.callback_query(F.data.startswith('whats_stats'))
async def tiktok_stats(call: CallbackQuery):
    whats = await get_all_users('whatsapp')
    whats_reg = await get_all_users('whatsapp_reg')
    await bot.send_message(call.from_user.id, f"Зашли по метке whatsapp - {len(whats)}\n"
                           f"Зарегистрировались по метке whatsapp - {len(whats_reg)}"
                           ,reply_markup=back_ik)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@router.callback_query(F.data.startswith('another_stats'))
async def another_stats(call: CallbackQuery):
    labels = [
        ('qr', 'qr', 'qr_reg'),
        ('events', 'events', 'events_reg'),
    ]

    message_text = ""
    for label, group, reg_table in labels:
        users = await get_all_users(group)
        reg_users = await get_all_users(reg_table) if reg_table else None
        message_text += f"зашли по метке {label} - {len(users)}"
        if reg_users is not None:
            message_text += f"\nЗарегистрировались по метке {label} - {len(reg_users)}"
        message_text += "\n\n"

    await bot.send_message(call.from_user.id, message_text, reply_markup=back_ik)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@router.callback_query(F.data.startswith('days'))
async def days_stats(call: CallbackQuery):
    gs = GoogleSheet()
    
    sheet = gs.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GoogleSheet.SPREADSHEET_ID, range='Наставничество!H:H').execute() 
    data = result.get('values', [])

    stats = defaultdict(int)
    
    for row in data[1:]:
        if row: 
            date = row[0]  
            stats[date] += 1  
    response = ""
    for date, count in stats.items():
        response += f"{date} - {count} зарегистрировались\n"
    
    await bot.send_message(call.from_user.id, response, reply_markup=back_ik)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


