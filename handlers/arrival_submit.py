from aiogram import Router, F
from google_sheets.sheets import GoogleSheet
from config import bot
from aiogram.types import Message

router = Router()


@router.message(F.text.startswith('@'))
async def qr_read(message: Message):
    gs = GoogleSheet()
    
    sheet = gs.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GoogleSheet.SPREADSHEET_ID, range='Наставничество!A:F').execute()  
    data = result.get('values', [])
    usernames = [row[1] for row in data]

    if message.text in usernames:
        await bot.send_message(message.from_user.id, 'Человек под данным юзернеймом помечен как посетивший мероприятие')
        indexes = [i for i, username in enumerate(usernames) if username == message.text]
        last_index = indexes[-1]
        
        sheet.values().update(
            spreadsheetId=GoogleSheet.SPREADSHEET_ID,
            range=f'Наставничество!E{last_index+1}', 
            valueInputOption='RAW',
            body={'values': [['Посетил']]}
        ).execute()

        gs.updateCellBackground(f'E{last_index+1}', 'green')
    else:
        await bot.send_message(message.from_user.id, "В таблице нет человека под таким юзернеймом!")