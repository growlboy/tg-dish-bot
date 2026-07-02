import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from apirouter import datarequest

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432")    
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp_pool = None

async def onbot_startup():
    None

async def onbot_end():
    None

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username or "anonuser"

    try:
        # БД логика
        await message.answer(f"Привет, {username}. Можешь написать любое блюдо, я напишу все продукты которые нужны")

    except Exception as error:
        await message.answer("Так.. прости пока не могу ответить")
        print(error)

@dp.message(F.text)
async def prompt_handler(message: types.Message):
    user_prompt = message.text

    answer = await datarequest(user_prompt)

    await message.answer(answer)

async def main():
    dp.startup.register(onbot_startup)
    dp.shutdown.register(onbot_end)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())