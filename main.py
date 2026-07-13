import asyncio
import asyncpg
import logging
from aiogram import Bot, Dispatcher

from config import *
from handlers import handlers_router
import database.dbmanager as dbmanager
import ai_service.airouter as airouter

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    pool = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
    )
    db = dbmanager.DataBaseManager(pool)
    dp.include_router(handlers_router)

    ai = airouter.AiRouterConnect()

    logging.info("The bot has been successfully launched.")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, db = db, ai = ai)
    finally:
        await pool.close()
        await bot.session.close()
        logging.info("Connections are closed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
