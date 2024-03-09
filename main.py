import asyncio
from config import dp, bot
from handlers import client, registration_fsm, arrival_submit, distibution_fsm
from common import utils
import logging
from database.db import sql_create


async def main():
    sql_create()
    dp.include_routers(
        utils.router,
        client.router,
        registration_fsm.router,
        arrival_submit.router,
        distibution_fsm.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())